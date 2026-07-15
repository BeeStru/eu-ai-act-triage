"""Classification engine.

Order of assessment follows the Act's own logic:

1. Article 5 prohibited practices. Terminal: a prohibited system gets no
   compliance pathway.
2. High-risk under Article 6: Annex I (embedded in regulated products) or
   Annex III (stand-alone use cases), with the Article 6(3) derogation
   applied where claimed and available.
3. Article 50 transparency duties. These stack: a high-risk chatbot still
   owes Article 50(1).
4. Minimal risk, with the standing Article 4 AI literacy measure noted.

The engine is deliberately a rules engine, not a language model. It applies
the law to structured answers; it does not interpret descriptions.

Two safety properties the engine enforces on top of the legal logic:

- Unknown rule ids fail closed. A typo in an Annex III area or a prohibited
  practice id marks the whole assessment needs_review rather than silently
  producing a lower tier. False assurance at scale is the failure mode a
  register tool must not have.
- Consistency checks. Where the assessor's answers contradict each other in
  ways the Act makes consequential (emotion recognition at work with the
  Article 5(1)(f) screen answered no; essential-services profiling with the
  Article 27 trigger answered no), the engine says so instead of staying
  quiet. The judgement remains the assessor's; the silence does not.
"""

from __future__ import annotations

from . import rules
from .models import Assessment, Finding, Obligation, RiskTier, Role, UseCase


def _obligation_from_timeline(article: str, summary: str, timeline_id: str) -> Obligation:
    milestone = rules.timeline()[timeline_id]
    return Obligation(
        article=article,
        summary=summary,
        applies_from_original=milestone["original_date"],
        applies_from_amended=milestone["amended_date"],
        date_status=milestone["status"],
    )


def _data_error(assessment: Assessment, message: str) -> None:
    assessment.needs_review = True
    assessment.notes.append(f"DATA ERROR: {message} This assessment must not "
                            "be relied on until the intake data is corrected.")


def _check_prohibited(case: UseCase, assessment: Assessment) -> tuple[bool, bool]:
    """Article 5 screen.

    Returns (hit, hold): hit is True if a prohibition applies; hold is True
    if an unmatchable prohibited-practice id requires a high-risk holding
    classification instead.
    """
    catalogue = rules.prohibitions()
    hit = False
    unknown = False
    for flag in case.prohibited_flags:
        practice = catalogue.get(flag)
        if practice is None:
            unknown = True
            _data_error(
                assessment,
                f"Unknown prohibited-practice id {flag!r}. "
                f"Valid ids: {', '.join(sorted(catalogue))}.",
            )
            continue
        hit = True
        assessment.findings.append(
            Finding(
                article=practice["article"],
                title="Prohibited practice",
                rationale=practice["summary"],
            )
        )
        assessment.obligations.append(
            _obligation_from_timeline(
                article=practice["article"],
                summary="Prohibited: the practice may not be placed on the market, "
                "put into service or used in the EU",
                timeline_id=practice["timeline_id"],
            )
        )
    if unknown and not hit:
        # Fail closed: an unmatchable prohibited-practice id cannot
        # demonstrate the prohibition applies, but the assessor answered yes
        # at the Article 5 screen, so the safe holding position is high-risk
        # pending correction, not minimal.
        assessment.findings.append(
            Finding(
                article="Art. 5",
                title="High-risk (holding classification pending data correction)",
                rationale="The recorded prohibited-practice id does not match "
                "the rule set, so the Article 5 screen cannot run. Held at "
                "high-risk until the intake is corrected.",
            )
        )
        return False, True
    return hit, False


def _check_high_risk(case: UseCase, assessment: Assessment) -> bool:
    """Article 6 screen. Returns True if the system is high-risk."""
    if case.annex_i_product:
        assessment.findings.append(
            Finding(
                article="Art. 6(1), Annex I",
                title="High-risk: embedded in a regulated product",
                rationale="Safety component of, or itself a product covered by, "
                "Annex I Union harmonisation legislation subject to third-party "
                "conformity assessment",
            )
        )
        _attach_high_risk_obligations(case, assessment, "high_risk_annex_i")
        return True

    if case.annex_iii_area is None:
        return False

    areas = rules.annex_iii_areas()
    area = areas.get(case.annex_iii_area)
    if area is None:
        _data_error(
            assessment,
            f"Unknown Annex III area id {case.annex_iii_area!r}. "
            f"Valid ids: {', '.join(sorted(areas))}.",
        )
        # Fail closed: an unmatchable area cannot demonstrate the system is
        # outside Annex III, so the safe holding position is high-risk
        # pending correction, not minimal.
        assessment.findings.append(
            Finding(
                article="Art. 6(2), Annex III",
                title="High-risk (holding classification pending data correction)",
                rationale="The recorded Annex III area id does not match the "
                "rule set, so the derogation logic cannot run. Held at "
                "high-risk until the intake is corrected.",
            )
        )
        _attach_high_risk_obligations(case, assessment, "high_risk_annex_iii")
        return True

    # Article 6(3) derogation: unavailable where the system profiles
    # natural persons; otherwise available if a listed condition is claimed.
    derogation = rules.art_6_3()
    valid_conditions = {c["id"] for c in derogation["conditions"]}
    claimed = [c for c in case.art_6_3_conditions if c in valid_conditions]
    unknown_conditions = [c for c in case.art_6_3_conditions if c not in valid_conditions]
    if unknown_conditions:
        _data_error(
            assessment,
            f"Unknown Art. 6(3) condition id(s) {unknown_conditions!r}. "
            f"Valid ids: {', '.join(sorted(valid_conditions))}.",
        )

    if claimed and not case.profiling_of_natural_persons:
        condition_texts = [
            c["text"] for c in derogation["conditions"] if c["id"] in claimed
        ]
        assessment.findings.append(
            Finding(
                article="Art. 6(3)",
                title="Annex III use case, derogation claimed: not high-risk",
                rationale=f"Falls in {area['name']} ({area['point']}) but the "
                "assessor records that it does not pose a significant risk of "
                "harm and meets: " + "; ".join(condition_texts),
            )
        )
        if case.role is Role.DEPLOYER:
            assessment.notes.append(
                "Art. 6(3) documentation and EU database registration are the "
                "provider's duties. As deployer, verify the provider's "
                "documented Art. 6(3) assessment and that the system is "
                "registered in the EU database, and keep the evidence with "
                "this record. The assessment can be challenged by market "
                "surveillance authorities."
            )
        else:
            assessment.notes.append(
                "Art. 6(3) reliance must be documented before placing on the "
                "market and the system registered in the EU database (duty "
                "retained by the Digital Omnibus). The assessment can be "
                "challenged by market surveillance authorities."
            )
        return False

    if claimed and case.profiling_of_natural_persons:
        assessment.notes.append(
            "Art. 6(3) derogation claimed but unavailable: the system performs "
            "profiling of natural persons (Art. 6(3), final subparagraph)."
        )

    assessment.findings.append(
        Finding(
            article=f"Art. 6(2), {area['point']}",
            title=f"High-risk: {area['name']}",
            rationale=f"Stand-alone Annex III use case. Area examples: {area['examples']}",
        )
    )
    _attach_high_risk_obligations(case, assessment, "high_risk_annex_iii")
    return True


def _attach_high_risk_obligations(
    case: UseCase, assessment: Assessment, timeline_id: str
) -> None:
    catalogue = rules.obligations()
    if case.role is Role.DEPLOYER:
        for item in catalogue["high_risk_deployer"]:
            if item["id"] == "fria" and not case.fria_relevant:
                continue
            if item["id"] == "inform_workers" and not case.workplace_use:
                continue
            if item["id"] == "inform_affected_persons" and timeline_id != "high_risk_annex_iii":
                continue  # Art. 26(11) attaches to Annex III systems
            assessment.obligations.append(
                _obligation_from_timeline(item["article"], item["summary"], timeline_id)
            )
        triggers = catalogue["deployer_becomes_provider"]
        assessment.notes.append(
            f"Deployer becomes provider ({triggers['article']}) on any of: "
            + "; ".join(triggers["triggers"])
        )
    else:
        summary = catalogue["high_risk_provider_summary"]
        assessment.obligations.append(
            _obligation_from_timeline(summary["article"], summary["summary"], timeline_id)
        )


def _check_transparency(case: UseCase, assessment: Assessment) -> bool:
    """Article 50 screen. Returns True if any duty attaches."""
    trigger_state = {
        "interacts_with_natural_persons": case.interacts_with_natural_persons,
        "generates_synthetic_content": case.generates_synthetic_content,
        "emotion_recognition_or_biometric_categorisation": (
            case.emotion_recognition or case.biometric_categorisation
        ),
        "deepfake_or_public_interest_text": case.deepfake,
    }
    hit = False
    for duty in rules.transparency_duties():
        if not trigger_state.get(duty["trigger"], False):
            continue
        if duty["role"] != case.role.value:
            # Record the counterparty duty as a note; useful in vendor review.
            assessment.notes.append(
                f"Counterparty duty ({duty['role']}): {duty['article']}, {duty['summary']}"
            )
            continue
        hit = True
        assessment.findings.append(
            Finding(
                article=duty["article"],
                title="Transparency duty",
                rationale=duty["summary"],
            )
        )
        assessment.obligations.append(
            _obligation_from_timeline(duty["article"], duty["summary"], duty["timeline_id"])
        )
    return hit


def _consistency_checks(case: UseCase, assessment: Assessment) -> None:
    """Flag answer combinations the Act makes consequential.

    The engine does not overrule the assessor; it refuses to stay quiet
    while the answers contradict each other.
    """
    if (
        case.emotion_recognition
        and case.workplace_use
        and "emotion_inference_work_education" not in case.prohibited_flags
    ):
        assessment.notes.append(
            "Consistency check: emotion recognition is recorded in a workplace "
            "context, but the Art. 5(1)(f) screen was answered no. That "
            "prohibition covers emotion inference at work outside medical or "
            "safety uses; confirm an exemption applies and record the basis."
        )
    if (
        case.role is Role.DEPLOYER
        and case.annex_iii_area == "essential_services"
        and case.profiling_of_natural_persons
        and not case.fria_relevant
    ):
        assessment.notes.append(
            "Consistency check: an essential-services use with profiling is "
            "recorded, but the Art. 27 trigger was answered no. Deployers of "
            "credit-scoring and life or health insurance pricing systems "
            "(Annex III 5(b), 5(c)) owe a fundamental rights impact "
            "assessment; confirm the system is outside those points and "
            "record the basis."
        )


def classify(case: UseCase) -> Assessment:
    """Run the full triage for one use case."""
    assessment = Assessment(use_case=case.name, role=case.role, tier=RiskTier.MINIMAL)
    meta = rules.timeline_meta()

    prohibited, prohibited_hold = _check_prohibited(case, assessment)
    if prohibited:
        assessment.tier = RiskTier.PROHIBITED
        # Terminal: no compliance pathway exists. The record still carries
        # the legal-status stamp like every other record.
        assessment.notes.append(meta["amendment_status"])
        return assessment

    high_risk = _check_high_risk(case, assessment)
    transparency = _check_transparency(case, assessment)

    if high_risk or prohibited_hold:
        assessment.tier = RiskTier.HIGH_RISK
    elif transparency:
        assessment.tier = RiskTier.TRANSPARENCY
    else:
        assessment.tier = RiskTier.MINIMAL
        assessment.findings.append(
            Finding(
                article="Art. 6, Art. 50",
                title="Minimal risk",
                rationale="No prohibited practice, no Annex I or Annex III "
                "listing, no Article 50 trigger recorded",
            )
        )

    literacy = rules.obligations()["ai_literacy"]
    assessment.obligations.append(
        _obligation_from_timeline(literacy["article"], literacy["summary"], "ai_literacy")
    )
    _consistency_checks(case, assessment)
    assessment.notes.append(meta["amendment_status"])
    return assessment
