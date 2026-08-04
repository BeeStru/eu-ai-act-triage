# Changelog

## 0.5.0 (August 2026)

Alignment with the published Digital Omnibus. Regulation (EU) 2026/1744
(OJ L, 24.7.2026, in force since 27 July 2026) replaces the Council press
release and compromise-text citations as the amendment source throughout
the data files, documents and output strings. Every encoded date was
re-verified against the Official Journal text and survived unchanged, so
this release corrects status prose, not dates: the amended dates are the
binding law, and the original dates remain in every record as historical
and audit context, with the dual-date rationale in the README and
methodology recast accordingly. The NCII/CSAM screening question is
tightened to the final Article 5(1a)-(1b) text: the reproducibility
qualifier, the five foreseeable-outcome trigger bases, the
correct-observed-misuse limb, the statutory media list, and the
manipulation carve-out scoped to the intimate-imagery limb only. Radio
equipment is dropped from the Annex I examples, since the new Article
6(1c) makes it a boundary case rather than an illustration, and the
deadline calendar loses its "(planning baseline)" label.

## 0.4.0 (July 2026)

Hardening and release readiness. Regression suite pinning the safety
behaviours the engine has carried since 0.1.0 (unknown rule ids failing
closed to high-risk with NEEDS REVIEW loud in the record, the CLI report and
the portfolio summary; consistency checks on contradictory intake answers;
the legal-status note on prohibited records; the role-aware Article 6(3)
note), so none can regress silently. CI on Python 3.11 and 3.12, including a
non-editable install check proving a plain `pip install .` ships the JSON
rule data. Full README and methodology documentation.

## 0.3.0 (July 2026)

Cross-framework flags (PRA SS1/23, DORA, ISO/IEC 42001, GDPR Article 9) from
a dedicated rule file, driven by the financial-services and vendor-supplied
context fields; the flag names the adjacent obligation, it does not assess
it. Regression test pinning that an in-house, non-financial-services row
raises no flags. SS1/23-vocabulary AI inventory template that runs directly
through register mode, with field definitions in docs/INVENTORY.md.
Third-party AI due-diligence questionnaire and the design specification for
the governed LLM intake assistant added as documents.

## 0.2.0 (July 2026)

Register mode: batch assessment over a CSV or JSON inventory, one dated
audit record per system, portfolio summary with tier counts, attention items
and a deadline calendar on the planning baseline. Unknown inventory columns
pass through into the audit record. All boolean columns, including the two
context fields, are parsed strictly: yes/no and equivalents only, a malformed
value is a readable error, and a "no" is never carried as a truthy string
(fixes a defect found in the pre-release reference design). Systems held
pending data correction are marked NEEDS REVIEW by name in the summary's
tier list, not only in the attention items.

## 0.1.0 (July 2026)

Initial triage engine, first public release. Built from a design that had
already been through a hostile review, so the safety behaviours ship from the
start rather than arriving as fixes: unknown rule ids fail closed to
high-risk and mark the assessment NEEDS REVIEW; consistency checks flag
contradictory intake answers without overriding the assessor. Classification
in the Act's own order: Article 5 screen (nine practices including the
Omnibus NCII/CSAM prohibition), terminal; Article 6 high-risk via Annex I or
Annex III with the Article 6(3) derogation, its profiling bar, and role-aware
derogation notes; Article 50 transparency duties, which stack, with the
deployer/provider duty split (a counterparty's duty is a note, not an
obligation); minimal risk with the standing Article 4 literacy measure.
Deployer obligations under Article 26 (including 26(11)) and Article 27.
Every obligation carries both the original Act date and the Digital
Omnibus-amended date with a status flag, read from verified data files, and
the amendment's legal status is stated on every output. Single-case CLI
(assess and interactive).
