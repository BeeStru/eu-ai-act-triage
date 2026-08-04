"""Command-line interface.

Two modes:

  aiact-triage assess case.json     Non-interactive: reads structured answers
  aiact-triage interactive          Walks the intake questionnaire

The report shows both the original AI Act dates and the Digital Omnibus
amended dates, with the legal status stated. The amended dates are the
binding law (Regulation (EU) 2026/1744, in force since 27 July 2026); the
original dates are kept for the record.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from . import rules
from .engine import classify
from .models import Assessment, RiskTier, Role, UseCase

TIER_LABELS = {
    RiskTier.PROHIBITED: "PROHIBITED (Article 5)",
    RiskTier.HIGH_RISK: "HIGH-RISK (Article 6)",
    RiskTier.TRANSPARENCY: "LIMITED RISK: transparency duties (Article 50)",
    RiskTier.MINIMAL: "MINIMAL RISK",
}


def render(assessment: Assessment) -> str:
    lines = [
        f"Use case: {assessment.use_case}",
        f"Role:     {assessment.role.value}",
        f"Tier:     {TIER_LABELS[assessment.tier]}",
    ]
    if assessment.needs_review:
        lines.append(
            "Status:   NEEDS REVIEW: intake data errors recorded; do not rely "
            "on this result until corrected"
        )
    lines += [
        "",
        "Findings:",
    ]
    for f in assessment.findings:
        lines.append(f"  [{f.article}] {f.title}")
        lines.append(f"      {f.rationale}")
    lines.append("")
    lines.append("Obligations and dates (original -> as amended by the Digital Omnibus):")
    for o in assessment.obligations:
        original = o.applies_from_original or "n/a"
        amended = o.applies_from_amended or "unchanged"
        lines.append(f"  [{o.article}] {o.summary}")
        lines.append(f"      applies from: {original} -> {amended}  ({o.date_status})")
    if assessment.notes:
        lines.append("")
        lines.append("Notes:")
        for n in assessment.notes:
            lines.append(f"  - {n}")
    return "\n".join(lines)


def _ask_yes_no(question: str) -> bool:
    while True:
        answer = input(f"{question} [y/n]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer y or n.")


def build_case_interactively() -> UseCase:
    name = input("Name of the AI system or use case: ").strip() or "unnamed"
    role_answer = input("Your role, provider or deployer [deployer]: ").strip().lower()
    role = Role.PROVIDER if role_answer == "provider" else Role.DEPLOYER

    print("\n-- Article 5 screen (prohibited practices) --")
    prohibited_flags = [
        practice_id
        for practice_id, practice in rules.prohibitions().items()
        if _ask_yes_no(practice["question"])
    ]

    print("\n-- High-risk screen (Article 6) --")
    annex_i = _ask_yes_no(
        "Is the system a safety component of, or itself a product covered by, "
        "Annex I Union harmonisation legislation (e.g. medical devices, lifts) "
        "requiring third-party conformity assessment?"
    )
    annex_iii_area = None
    profiling = False
    conditions: list[str] = []
    if not annex_i:
        print("Annex III areas:")
        for area in rules.annex_iii_areas().values():
            print(f"  {area['id']:<24} {area['name']}")
        raw = input("Enter the matching area id, or press Enter for none: ").strip()
        annex_iii_area = raw or None
        if annex_iii_area:
            profiling = _ask_yes_no("Does the system perform profiling of natural persons?")
            if not profiling and _ask_yes_no(
                "Do you consider it poses no significant risk of harm and want "
                "to claim the Article 6(3) derogation?"
            ):
                for condition in rules.art_6_3()["conditions"]:
                    if _ask_yes_no(condition["text"] + "?"):
                        conditions.append(condition["id"])

    print("\n-- Article 50 screen (transparency) --")
    case = UseCase(
        name=name,
        role=role,
        prohibited_flags=prohibited_flags,
        annex_i_product=annex_i,
        annex_iii_area=annex_iii_area,
        profiling_of_natural_persons=profiling,
        art_6_3_conditions=conditions,
        interacts_with_natural_persons=_ask_yes_no(
            "Does the system interact directly with natural persons (e.g. a chatbot)?"
        ),
        generates_synthetic_content=_ask_yes_no(
            "Does the system generate synthetic audio, image, video or text?"
        ),
        emotion_recognition=_ask_yes_no("Is it an emotion recognition system?"),
        biometric_categorisation=_ask_yes_no("Is it a biometric categorisation system?"),
        deepfake=_ask_yes_no(
            "Does it generate or manipulate deepfake content, or AI text "
            "published to inform the public on matters of public interest?"
        ),
        fria_relevant=_ask_yes_no(
            "Are you a public body, a private provider of public services, or "
            "a deployer of credit-scoring or life/health insurance pricing systems?"
        ),
        workplace_use=_ask_yes_no("Will the system be used in a workplace context?"),
        financial_services_context=_ask_yes_no(
            "Is the deploying entity a regulated financial firm (PRA/FCA or "
            "equivalent)?"
        ),
        vendor_supplied=_ask_yes_no(
            "Is the system supplied by a third-party vendor rather than built "
            "in-house?"
        ),
    )
    return case


def load_case(path: str) -> UseCase:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return UseCase.from_dict(raw)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aiact-triage",
        description="EU AI Act risk-classification triage (deployer-readiness toolkit)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    assess = sub.add_parser("assess", help="Assess a case from a JSON answers file")
    assess.add_argument("case_file", help="Path to the structured answers JSON")
    assess.add_argument("--json", action="store_true", help="Emit the assessment as JSON")

    register = sub.add_parser(
        "register", help="Assess a whole AI inventory (CSV or JSON) in batch"
    )
    register.add_argument("register_file", help="Path to the inventory (.csv or .json)")
    register.add_argument(
        "--out",
        help="Directory for per-system audit records and the portfolio summary",
    )
    register.add_argument("--assessor", help="Name recorded on each audit record")

    sub.add_parser("interactive", help="Walk the intake questionnaire")

    args = parser.parse_args(argv)

    if args.command == "assess":
        assessment = classify(load_case(args.case_file))
        if args.json:
            print(json.dumps(asdict(assessment), indent=2, default=str))
        else:
            print(render(assessment))
    elif args.command == "register":
        from .register import assess_register, load_register, render_summary, write_register_outputs

        cases = load_register(args.register_file)
        pairs = list(zip(cases, assess_register(cases)))
        if args.out:
            written = write_register_outputs(pairs, args.out, args.assessor)
            print(f"Wrote {len(written)} files to {args.out}/")
        print(render_summary(pairs))
    else:
        assessment = classify(build_case_interactively())
        print("\n" + render(assessment))
    return 0


if __name__ == "__main__":
    sys.exit(main())
