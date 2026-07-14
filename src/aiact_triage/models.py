"""Data structures for the EU AI Act triage engine.

The engine works on structured answers to intake questions, not free text.
Classification judgement stays with the human assessor; the tool structures
the assessment and applies the legal logic and dates consistently.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum


class Role(str, Enum):
    PROVIDER = "provider"
    DEPLOYER = "deployer"


class RiskTier(str, Enum):
    PROHIBITED = "prohibited"
    HIGH_RISK = "high_risk"
    TRANSPARENCY = "transparency"
    MINIMAL = "minimal"


@dataclass
class UseCase:
    """Structured intake answers for one AI system or use case.

    Every field maps to an intake question; defaults are the conservative
    'no' so that an empty answer never silently removes an obligation.
    """

    name: str
    role: Role = Role.DEPLOYER

    # Article 5 screen: ids from data/prohibitions.json the assessor has
    # answered 'yes' to.
    prohibited_flags: list[str] = field(default_factory=list)

    # High-risk screen.
    annex_i_product: bool = False  # safety component of / product under Annex I legislation
    annex_iii_area: str | None = None  # id from data/annex_iii.json, or None
    profiling_of_natural_persons: bool = False
    art_6_3_conditions: list[str] = field(default_factory=list)  # derogation condition ids claimed

    # Article 50 screen.
    interacts_with_natural_persons: bool = False
    generates_synthetic_content: bool = False
    emotion_recognition: bool = False
    biometric_categorisation: bool = False
    deepfake: bool = False

    # Context.
    fria_relevant: bool = False  # public body, public-service provider, or Annex III 5(b)/(c) deployer
    workplace_use: bool = False
    financial_services_context: bool = False  # PRA/FCA-regulated financial entity
    vendor_supplied: bool = False  # third-party system rather than in-house build

    # Inventory passthrough: columns the assessment does not use (owner,
    # vendor, internal ids) are carried into the audit record untouched.
    metadata: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict) -> "UseCase":
        """Build a UseCase from a plain dict, routing unknown keys to metadata.

        Real inventories always carry extra columns; refusing to load them
        would make the tool unusable on real data, and silently dropping
        them would lose audit-relevant context.
        """
        data = dict(raw)
        known = {f.name for f in fields(cls)}
        metadata = dict(data.pop("metadata", None) or {})
        for key in list(data):
            if key not in known:
                metadata[key] = data.pop(key)
        if "role" in data and not isinstance(data["role"], Role):
            data["role"] = Role(str(data["role"]).strip().lower())
        return cls(metadata=metadata, **data)


@dataclass
class Finding:
    """One legal conclusion with its basis."""

    article: str
    title: str
    rationale: str


@dataclass
class Obligation:
    """One obligation with the dates that govern it."""

    article: str
    summary: str
    applies_from_original: str | None
    applies_from_amended: str | None
    date_status: str  # e.g. 'in_application', 'unchanged', 'postponed_by_omnibus'


@dataclass
class Assessment:
    """The triage output for one use case."""

    use_case: str
    role: Role
    tier: RiskTier
    findings: list[Finding] = field(default_factory=list)
    obligations: list[Obligation] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    # Set when intake data contained errors (unknown rule ids). A tier is
    # still computed so the record is inspectable, but it must not be relied
    # on until the data is corrected. Fail closed, loudly.
    needs_review: bool = False
