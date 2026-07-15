"""Register (batch) mode tests.

These cover the parts the single-case tests cannot: CSV parsing, metadata
passthrough, the audit record, and the portfolio summary logic.
"""

from pathlib import Path

import pytest

from aiact_triage.models import RiskTier, Role, UseCase
from aiact_triage.register import (
    assess_register,
    load_register,
    render_audit_record,
    render_summary,
    slugify,
    write_register_outputs,
)

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _pairs():
    cases = load_register(EXAMPLES / "inventory.csv")
    return list(zip(cases, assess_register(cases)))


def test_csv_loads_all_rows_with_types():
    cases = load_register(EXAMPLES / "inventory.csv")
    assert len(cases) == 7
    cv = cases[0]
    assert cv.role is Role.DEPLOYER
    assert cv.annex_iii_area == "employment"
    assert cv.profiling_of_natural_persons is True
    assert cv.workplace_use is True


def test_unknown_columns_flow_into_metadata():
    cases = load_register(EXAMPLES / "inventory.csv")
    assert cases[0].metadata["owner"] == "HR Operations"
    assert cases[0].metadata["vendor"] == "TalentTools Ltd"


def test_context_fields_parse_no_as_false(tmp_path):
    # A CSV "no" in the context columns must load as False, not as the
    # truthy string "no".
    csv_file = tmp_path / "ctx.csv"
    csv_file.write_text(
        "name,role,financial_services_context,vendor_supplied\n"
        "Thing,deployer,no,no\n",
        encoding="utf-8",
    )
    loaded = load_register(csv_file)[0]
    assert loaded.financial_services_context is False
    assert loaded.vendor_supplied is False


def test_expected_tiers_across_the_inventory():
    tiers = {case.name: assessment.tier for case, assessment in _pairs()}
    assert tiers["CV screening assistant"] is RiskTier.HIGH_RISK
    assert tiers["Credit scoring model"] is RiskTier.HIGH_RISK
    assert tiers["Workplace wellbeing emotion monitor (pilot)"] is RiskTier.PROHIBITED
    assert tiers["Exam-marking consistency checker"] is not RiskTier.HIGH_RISK
    assert tiers["Meeting transcription and summariser"] is RiskTier.MINIMAL


def test_audit_record_contains_citations_dates_and_inventory_fields():
    case, assessment = _pairs()[0]
    record = render_audit_record(case, assessment, assessor="B. Struve")
    assert "Annex III, 4" in record
    assert "2026-08-02" in record and "2027-12-02" in record
    assert "owner (inventory field): HR Operations" in record
    assert "Assessor: B. Struve." in record


def test_summary_surfaces_attention_items_and_calendar():
    summary = render_summary(_pairs())
    assert "PROHIBITED (Article 5): 1" in summary
    assert "Escalate" in summary
    assert "Art. 6(3) derogation" in summary
    assert "fundamental rights impact assessment" in summary.lower() or "Art. 27" in summary
    assert "Upcoming:" in summary
    assert "2027-12-02" in summary


def test_write_register_outputs_creates_records_and_summary(tmp_path):
    written = write_register_outputs(_pairs(), tmp_path, assessor="B. Struve")
    # Seven records plus the summary.
    assert len(written) == 8
    assert (tmp_path / "_summary.md").exists()
    assert (tmp_path / "01-cv-screening-assistant.md").exists()


def test_bad_boolean_raises_a_readable_error(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "name,role,workplace_use\nThing,deployer,maybe\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="workplace_use"):
        load_register(bad)


def test_json_register_and_slug_edge_cases():
    import json as jsonlib

    cases = [{"name": "A/B tester!!", "role": "provider"}]
    path = EXAMPLES.parents[0] / "examples" / "_tmp_register.json"
    path.write_text(jsonlib.dumps(cases), encoding="utf-8")
    try:
        loaded = load_register(path)
        assert loaded[0].role is Role.PROVIDER
        assert slugify(loaded[0].name) == "a-b-tester"
    finally:
        path.unlink()
