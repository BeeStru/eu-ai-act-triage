"""Cross-framework flag tests.

The flags name adjacent obligations (SS1/23, DORA, ISO 42001, GDPR); these
tests pin down when each fires and, as importantly, when it stays silent.
"""

from aiact_triage.engine import classify
from aiact_triage.models import RiskTier, Role, UseCase


def _cross_notes(assessment):
    return [n for n in assessment.notes if n.startswith("Cross-framework:")]


def test_fs_high_risk_gets_ss1_23_inventory_and_lifecycle_flags():
    case = UseCase(
        name="Credit scoring model",
        role=Role.DEPLOYER,
        annex_iii_area="essential_services",
        profiling_of_natural_persons=True,
        fria_relevant=True,
        financial_services_context=True,
    )
    notes = _cross_notes(classify(case))
    assert any("SS1/23" in n and "model inventory" in n for n in notes)
    assert any("Principles 3 to 5" in n for n in notes)
    # In-house build: no DORA third-party flag.
    assert not any("DORA" in n for n in notes)


def test_fs_vendor_system_gets_dora_and_iso42001_flags():
    case = UseCase(
        name="Vendor chatbot",
        role=Role.DEPLOYER,
        interacts_with_natural_persons=True,
        financial_services_context=True,
        vendor_supplied=True,
    )
    notes = _cross_notes(classify(case))
    assert any("DORA" in n and "register of information" in n for n in notes)
    assert any("ISO/IEC 42001" in n for n in notes)


def test_non_fs_vendor_system_gets_iso42001_but_not_dora_or_ss1_23():
    case = UseCase(
        name="Vendor summariser",
        role=Role.DEPLOYER,
        vendor_supplied=True,
    )
    notes = _cross_notes(classify(case))
    assert any("ISO/IEC 42001" in n for n in notes)
    assert not any("DORA" in n for n in notes)
    assert not any("SS1/23" in n for n in notes)


def test_emotion_recognition_outside_workplace_gets_gdpr_flag():
    # Emotion recognition at work is Art. 5(1)(f) territory; this case is a
    # deployer analysing consenting focus-group participants, so it lands as
    # an Art. 50(3) transparency duty plus the GDPR special-category flag.
    case = UseCase(
        name="Focus group emotion analysis",
        role=Role.DEPLOYER,
        emotion_recognition=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.TRANSPARENCY
    assert any("Article 9" in n for n in _cross_notes(result))


def test_prohibited_system_gets_no_cross_framework_flags():
    case = UseCase(
        name="Workplace emotion monitor",
        role=Role.DEPLOYER,
        prohibited_flags=["emotion_inference_work_education"],
        financial_services_context=True,
        vendor_supplied=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.PROHIBITED
    assert _cross_notes(result) == []


def test_csv_no_in_context_fields_yields_no_cross_framework_flags(tmp_path):
    # End-to-end guard on the boolean parsing of the two context fields: a
    # CSV "no" must stay False all the way through classification, never a
    # truthy string that fires the SS1/23, DORA and ISO 42001 flags.
    from aiact_triage.register import load_register

    csv_file = tmp_path / "inventory.csv"
    csv_file.write_text(
        "name,role,annex_iii_area,profiling_of_natural_persons,"
        "financial_services_context,vendor_supplied\n"
        "CV screener,deployer,employment,yes,no,no\n",
        encoding="utf-8",
    )
    case = load_register(csv_file)[0]
    result = classify(case)
    assert result.tier is RiskTier.HIGH_RISK
    assert _cross_notes(result) == []
