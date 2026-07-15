"""Regression tests for the pre-release hostile review.

Each test pins a behaviour that review demanded and that has shipped
since 0.1.0: fail-closed on unknown ids, consistency warnings on
contradictory answers, the legal-status note on prohibited records, and
Article 26(11) coverage. If any of these regresses, the tool has
reacquired a failure mode a governance tool must not have.
"""

from aiact_triage.engine import classify
from aiact_triage.models import RiskTier, Role, UseCase
from aiact_triage.register import render_audit_record, render_summary


def test_unknown_annex_iii_area_fails_closed_to_high_risk_needs_review():
    result = classify(
        UseCase(
            name="CV screener",
            role=Role.DEPLOYER,
            annex_iii_area="employmnet",  # deliberate typo
            profiling_of_natural_persons=True,
        )
    )
    assert result.needs_review is True
    assert result.tier is RiskTier.HIGH_RISK  # holding position, not minimal
    assert any(n.startswith("DATA ERROR") for n in result.notes)
    # The valid ids are listed so the correction is one glance away.
    assert any("employment" in n for n in result.notes if n.startswith("DATA ERROR"))


def test_unknown_prohibited_flag_fails_closed_to_high_risk_needs_review():
    result = classify(
        UseCase(name="Thing", role=Role.PROVIDER, prohibited_flags=["socail_scoring"])
    )
    assert result.needs_review is True
    assert result.tier is RiskTier.HIGH_RISK  # holding position, not minimal
    assert result.tier is not RiskTier.PROHIBITED  # a hold is not a verdict
    assert any(n.startswith("DATA ERROR") for n in result.notes)


def test_prohibited_hold_attaches_only_the_art_4_baseline():
    result = classify(
        UseCase(name="Thing", role=Role.DEPLOYER, prohibited_flags=["socail_scoring"])
    )
    assert result.tier is RiskTier.HIGH_RISK
    assert result.needs_review is True
    # The hold is a stop-and-fix state, not a duty state: pending correction
    # the outcome is either terminal PROHIBITED (no duties to report) or a
    # reclassification, so no Annex-route duties attach to the held record.
    assert [o.article for o in result.obligations] == ["Art. 4"]


def test_prohibited_record_carries_the_legal_status_note():
    result = classify(
        UseCase(
            name="Emotion monitor",
            role=Role.DEPLOYER,
            prohibited_flags=["emotion_inference_work_education"],
        )
    )
    assert result.tier is RiskTier.PROHIBITED
    assert any("Official Journal" in n for n in result.notes)


def test_emotion_at_work_without_art5_answer_gets_consistency_warning():
    result = classify(
        UseCase(
            name="Interview scorer",
            role=Role.DEPLOYER,
            annex_iii_area="employment",
            profiling_of_natural_persons=True,
            emotion_recognition=True,
            workplace_use=True,
        )
    )
    assert any("Consistency check" in n and "5(1)(f)" in n for n in result.notes)


def test_essential_services_profiling_without_fria_gets_consistency_warning():
    result = classify(
        UseCase(
            name="Credit scorer",
            role=Role.DEPLOYER,
            annex_iii_area="essential_services",
            profiling_of_natural_persons=True,
            fria_relevant=False,
        )
    )
    assert any("Consistency check" in n and "Art. 27" in n for n in result.notes)


def test_annex_iii_deployer_owes_art_26_11_inform_affected_persons():
    result = classify(
        UseCase(
            name="CV screening tool",
            role=Role.DEPLOYER,
            annex_iii_area="employment",
            profiling_of_natural_persons=True,
        )
    )
    assert any(o.article == "Art. 26(11)" for o in result.obligations)


def test_deployer_6_3_note_points_at_provider_verification():
    result = classify(
        UseCase(
            name="Duplicate detector",
            role=Role.DEPLOYER,
            annex_iii_area="education",
            art_6_3_conditions=["narrow_procedural"],
        )
    )
    assert any("verify the provider's documented" in n for n in result.notes)


def test_needs_review_is_loud_in_record_and_summary():
    case = UseCase(name="Typo system", role=Role.DEPLOYER, annex_iii_area="hr")
    assessment = classify(case)
    record = render_audit_record(case, assessment)
    assert "STATUS: NEEDS REVIEW" in record
    summary = render_summary([(case, assessment)])
    assert "NEEDS REVIEW" in summary
