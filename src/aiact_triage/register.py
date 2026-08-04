"""Batch assessment over an AI register (inventory).

A single classification is easy to do by hand. What cannot be done reliably
by hand is two hundred systems, assessed the same way each time, each with a
dated record citing the articles relied on, kept correct as the timeline
shifts. This module is that: it reads an inventory (CSV or JSON), runs the
triage over every entry, and writes one audit record per system plus a
portfolio summary.

The CSV format is deliberately the shape of a real AI inventory. Columns
matching UseCase fields drive the assessment; any other column (owner,
vendor, internal reference) passes through into the audit record untouched.
"""

from __future__ import annotations

import csv
import datetime
import json
import re
from dataclasses import fields
from pathlib import Path

from . import rules
from .engine import classify
from .models import Assessment, RiskTier, UseCase

_BOOL_FIELDS = {
    "annex_i_product",
    "profiling_of_natural_persons",
    "interacts_with_natural_persons",
    "generates_synthetic_content",
    "emotion_recognition",
    "biometric_categorisation",
    "deepfake",
    "fria_relevant",
    "workplace_use",
    "financial_services_context",
    "vendor_supplied",
}
_LIST_FIELDS = {"prohibited_flags", "art_6_3_conditions"}
_TRUE = {"y", "yes", "true", "1"}
_FALSE = {"n", "no", "false", "0", ""}

TIER_LABELS = {
    RiskTier.PROHIBITED: "PROHIBITED (Article 5)",
    RiskTier.HIGH_RISK: "HIGH-RISK (Article 6)",
    RiskTier.TRANSPARENCY: "LIMITED RISK: transparency duties (Article 50)",
    RiskTier.MINIMAL: "MINIMAL RISK",
}


def _parse_bool(field_name: str, value: str) -> bool:
    cleaned = value.strip().lower()
    if cleaned in _TRUE:
        return True
    if cleaned in _FALSE:
        return False
    raise ValueError(f"Cannot read {field_name}={value!r} as yes/no")


def _coerce_csv_row(row: dict[str, str]) -> dict:
    """Turn one CSV row of strings into the typed dict UseCase expects."""
    record: dict = {}
    for key, value in row.items():
        if key is None or value is None:
            continue
        key = key.strip()
        value = value.strip()
        if key in _BOOL_FIELDS:
            record[key] = _parse_bool(key, value)
        elif key in _LIST_FIELDS:
            record[key] = [item.strip() for item in value.split(";") if item.strip()]
        elif key == "annex_iii_area":
            record[key] = value or None
        elif value != "":
            record[key] = value
    return record


def load_register(path: str | Path) -> list[UseCase]:
    """Load an inventory from .csv or .json (a JSON list of case objects)."""
    path = Path(path)
    if path.suffix.lower() == ".json":
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            raise ValueError("A JSON register must be a list of case objects")
        return [UseCase.from_dict(item) for item in raw]
    if path.suffix.lower() == ".csv":
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [UseCase.from_dict(_coerce_csv_row(row)) for row in reader]
    raise ValueError(f"Unsupported register format: {path.suffix!r} (use .csv or .json)")


def assess_register(cases: list[UseCase]) -> list[Assessment]:
    return [classify(case) for case in cases]


def _effective_date(obligation) -> str | None:
    """The planning-baseline date: amended where one exists, else original."""
    return obligation.applies_from_amended or obligation.applies_from_original


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "unnamed"


def render_audit_record(
    case: UseCase, assessment: Assessment, assessor: str | None = None
) -> str:
    """One dated, citable markdown record for one system."""
    from . import __version__

    meta = rules.timeline_meta()
    today = datetime.date.today().isoformat()
    lines = [
        f"# AI Act triage record: {case.name}",
        "",
        f"Assessed {today} with aiact-triage {__version__}. "
        f"Rule set last verified {meta['last_verified']}.",
        f"Assessor: {assessor or 'not recorded'}.",
    ]
    if assessment.needs_review:
        lines += [
            "",
            "**STATUS: NEEDS REVIEW. The intake data contained errors "
            "(see DATA ERROR notes). Do not rely on this record until "
            "corrected and re-run.**",
        ]
    lines += [
        "",
        f"## Classification: {TIER_LABELS[assessment.tier]}",
        "",
        "## Basis",
        "",
    ]
    for f in assessment.findings:
        lines.append(f"- **[{f.article}]** {f.title}: {f.rationale}")
    lines += [
        "",
        "## Obligations",
        "",
        "| Article | Obligation | Applies from (original) | As amended (Omnibus) | Status |",
        "|---|---|---|---|---|",
    ]
    for o in assessment.obligations:
        lines.append(
            f"| {o.article} | {o.summary} | {o.applies_from_original or 'n/a'} | "
            f"{o.applies_from_amended or 'unchanged'} | {o.date_status} |"
        )
    if assessment.notes:
        lines += ["", "## Notes", ""]
        lines += [f"- {note}" for note in assessment.notes]
    lines += ["", "## Answers as recorded", ""]
    for field_def in fields(case):
        if field_def.name in {"name", "metadata"}:
            continue
        value = getattr(case, field_def.name)
        value = value.value if hasattr(value, "value") else value
        lines.append(f"- {field_def.name}: {value}")
    for key, value in case.metadata.items():
        lines.append(f"- {key} (inventory field): {value}")
    lines.append("")
    return "\n".join(lines)


def render_summary(pairs: list[tuple[UseCase, Assessment]]) -> str:
    """Portfolio view: tier counts, attention items, deadline calendar."""
    meta = rules.timeline_meta()
    today = datetime.date.today()
    lines = [
        "# AI register triage summary",
        "",
        f"{len(pairs)} systems assessed {today.isoformat()}. "
        f"Rule set last verified {meta['last_verified']}.",
        "",
        f"Legal status of the amended dates: {meta['amendment_status']}",
        "",
        "## Systems by tier",
        "",
    ]
    tier_order = [
        RiskTier.PROHIBITED,
        RiskTier.HIGH_RISK,
        RiskTier.TRANSPARENCY,
        RiskTier.MINIMAL,
    ]
    by_tier: dict[RiskTier, list[str]] = {tier: [] for tier in tier_order}
    for case, assessment in pairs:
        # A held row is provisionally classified pending data correction,
        # a different claim from a confirmed tier; the headline list says so.
        label = case.name + (" (NEEDS REVIEW)" if assessment.needs_review else "")
        by_tier[assessment.tier].append(label)
    for tier in tier_order:
        names = by_tier[tier]
        lines.append(f"- {TIER_LABELS[tier]}: {len(names)}")
        for name in names:
            lines.append(f"    - {name}")

    attention: list[str] = []
    for case, assessment in pairs:
        if assessment.needs_review:
            attention.append(
                f"{case.name}: NEEDS REVIEW, intake data errors recorded. "
                "Correct the inventory row and re-run before relying on "
                "this classification."
            )
    for case, assessment in pairs:
        if assessment.tier is RiskTier.PROHIBITED:
            attention.append(
                f"{case.name}: prohibited practice recorded. Escalate; "
                "no compliance pathway exists."
            )
        if any("registered in the EU database" in note for note in assessment.notes):
            attention.append(
                f"{case.name}: relies on the Art. 6(3) derogation; the "
                "assessment must be documented and the system registered."
            )
        if any(o.article == "Art. 27" for o in assessment.obligations):
            attention.append(
                f"{case.name}: fundamental rights impact assessment (Art. 27) "
                "required before first use."
            )
    if attention:
        lines += ["", "## Attention items", ""]
        lines += [f"- {item}" for item in attention]

    # Deadline calendar on the amended date where one exists, split into
    # what already applies and what is coming.
    calendar: dict[tuple[str, str], set[str]] = {}
    for case, assessment in pairs:
        for o in assessment.obligations:
            date = _effective_date(o)
            if date is None:
                continue
            calendar.setdefault((date, o.article), set()).add(case.name)
    applying = [(d, a, names) for (d, a), names in calendar.items() if d <= today.isoformat()]
    upcoming = [(d, a, names) for (d, a), names in calendar.items() if d > today.isoformat()]

    def _count(names: set[str]) -> str:
        return "1 system" if len(names) == 1 else f"{len(names)} systems"

    lines += ["", "## Deadline calendar", ""]
    if applying:
        lines.append("Already applying:")
        for date, article, names in sorted(applying):
            lines.append(f"- {date}  {article}  ({_count(names)})")
    if upcoming:
        lines.append("")
        lines.append("Upcoming:")
        for date, article, names in sorted(upcoming):
            lines.append(f"- {date}  {article}  ({_count(names)})")
    lines.append("")
    lines.append(
        "The calendar uses the Omnibus amended date where one exists. The "
        "amended dates are the binding law (Regulation (EU) 2026/1744, in "
        "force since 27 July 2026); each system's record shows both dates."
    )
    lines.append("")
    return "\n".join(lines)


def write_register_outputs(
    pairs: list[tuple[UseCase, Assessment]],
    out_dir: str | Path,
    assessor: str | None = None,
) -> list[Path]:
    """Write one record per system plus the summary. Returns written paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, (case, assessment) in enumerate(pairs, start=1):
        path = out / f"{index:02d}-{slugify(case.name)}.md"
        path.write_text(render_audit_record(case, assessment, assessor), encoding="utf-8")
        written.append(path)
    summary_path = out / "_summary.md"
    summary_path.write_text(render_summary(pairs), encoding="utf-8")
    written.append(summary_path)
    return written
