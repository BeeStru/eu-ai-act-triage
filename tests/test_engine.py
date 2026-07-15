"""Worked classification cases.

Each test is a case an interviewer could reasonably probe. The expected
outcomes are derived from the Act's text as amended by the Digital Omnibus;
the dates assert against data/timeline.json so a future date correction
only touches the data layer.
"""

from aiact_triage.engine import classify
from aiact_triage.models import RiskTier, Role, UseCase


def _articles(assessment):
    return [o.article for o in assessment.obligations]


def test_cv_screening_is_high_risk_annex_iii_employment():
    case = UseCase(
        name="CV screening tool for graduate recruitment",
        role=Role.DEPLOYER,
        annex_iii_area="employment",
        profiling_of_natural_persons=True,
        workplace_use=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.HIGH_RISK
    # Deployer obligations attach, including informing workers.
    assert "Art. 26(2)" in _articles(result)
    assert "Art. 26(7)" in _articles(result)
    # Annex III dates: original Aug 2026, amended Dec 2027.
    high_risk = [o for o in result.obligations if o.article.startswith("Art. 26")]
    assert all(o.applies_from_original == "2026-08-02" for o in high_risk)
    assert all(o.applies_from_amended == "2027-12-02" for o in high_risk)


def test_customer_chatbot_is_limited_risk_with_provider_side_note():
    case = UseCase(
        name="Customer service chatbot",
        role=Role.DEPLOYER,
        interacts_with_natural_persons=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.MINIMAL or result.tier is RiskTier.TRANSPARENCY
    # Art. 50(1) is a provider duty; for a deployer it appears as a
    # counterparty note, not an obligation.
    assert "Art. 50(1)" not in _articles(result)
    assert any("Art. 50(1)" in n for n in result.notes)


def test_provider_chatbot_owes_art_50_1_from_aug_2026():
    case = UseCase(
        name="Chatbot product",
        role=Role.PROVIDER,
        interacts_with_natural_persons=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.TRANSPARENCY
    duty = next(o for o in result.obligations if o.article == "Art. 50(1)")
    assert duty.applies_from_original == "2026-08-02"
    assert duty.applies_from_amended is None  # unchanged by the Omnibus


def test_generative_provider_marking_postponed_to_dec_2026():
    case = UseCase(
        name="Marketing image generator",
        role=Role.PROVIDER,
        generates_synthetic_content=True,
    )
    result = classify(case)
    duty = next(o for o in result.obligations if o.article == "Art. 50(2)")
    assert duty.applies_from_original == "2026-08-02"
    assert duty.applies_from_amended == "2026-12-02"
    assert duty.date_status == "postponed_by_omnibus"


def test_social_scoring_is_prohibited_and_terminal():
    case = UseCase(
        name="Citizen trust score",
        role=Role.PROVIDER,
        prohibited_flags=["social_scoring"],
        interacts_with_natural_persons=True,  # must NOT produce Art. 50 duties
    )
    result = classify(case)
    assert result.tier is RiskTier.PROHIBITED
    assert "Art. 50(1)" not in _articles(result)
    prohibition = next(o for o in result.obligations if "5(1)(c)" in o.article)
    assert prohibition.applies_from_original == "2025-02-02"


def test_ncii_generation_prohibited_from_dec_2026():
    case = UseCase(
        name="Undressing app",
        role=Role.PROVIDER,
        prohibited_flags=["ncii_csam_generation"],
    )
    result = classify(case)
    assert result.tier is RiskTier.PROHIBITED
    prohibition = result.obligations[0]
    assert prohibition.applies_from_amended == "2026-12-02"
    assert prohibition.date_status == "introduced_by_omnibus"


def test_art_6_3_derogation_available_without_profiling():
    case = UseCase(
        name="Duplicate-application detector in admissions",
        role=Role.DEPLOYER,
        annex_iii_area="education",
        profiling_of_natural_persons=False,
        art_6_3_conditions=["narrow_procedural"],
    )
    result = classify(case)
    assert result.tier is not RiskTier.HIGH_RISK
    assert any("registered in the EU database" in n for n in result.notes)


def test_art_6_3_derogation_blocked_by_profiling():
    case = UseCase(
        name="Credit scoring model",
        role=Role.DEPLOYER,
        annex_iii_area="essential_services",
        profiling_of_natural_persons=True,
        art_6_3_conditions=["preparatory_task"],
        fria_relevant=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.HIGH_RISK
    assert any("unavailable" in n for n in result.notes)
    # Credit scoring deployer owes a fundamental rights impact assessment.
    assert "Art. 27" in _articles(result)


def test_annex_i_product_uses_2028_amended_date():
    case = UseCase(
        name="AI perception module in a medical device",
        role=Role.PROVIDER,
        annex_i_product=True,
    )
    result = classify(case)
    assert result.tier is RiskTier.HIGH_RISK
    provider = next(o for o in result.obligations if "Chapter III" in o.article)
    assert provider.applies_from_original == "2027-08-02"
    assert provider.applies_from_amended == "2028-08-02"


def test_spam_filter_is_minimal_but_literacy_still_noted():
    case = UseCase(name="Inbound email spam filter", role=Role.DEPLOYER)
    result = classify(case)
    assert result.tier is RiskTier.MINIMAL
    assert "Art. 4" in _articles(result)


def test_high_risk_and_transparency_stack():
    case = UseCase(
        name="Emotion-aware candidate interview scorer",
        role=Role.DEPLOYER,
        annex_iii_area="employment",
        profiling_of_natural_persons=True,
        emotion_recognition=True,
        workplace_use=True,
    )
    result = classify(case)
    # Note: emotion inference at work is Art. 5(1)(f) territory; this case
    # models the assessor answering 'no' at the Article 5 screen (e.g. a
    # claimed safety exemption) so the stacking logic can be tested. The
    # engine classifies what the assessor records.
    assert result.tier is RiskTier.HIGH_RISK
    assert "Art. 50(3)" in _articles(result)
