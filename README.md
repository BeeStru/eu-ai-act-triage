# EU AI Act deployer-readiness toolkit

A set of instruments for an organisation that deploys AI systems: classify each use case under the EU AI Act, record the result defensibly, and carry the classification through into the model inventory and vendor due diligence. The working core is a triage engine that assesses a whole AI inventory in one pass and writes a dated audit record per system, with obligation dates shown under both the original Act and the Digital Omnibus amendments.

## The problem this addresses

Organisations use the same handful of AI systems for very different things, and the EU AI Act regulates the thing, not the system: classification turns on the deployed purpose, not the base model underneath. The same foundation model is minimal-risk when it drafts marketing copy, high-risk when it screens CVs or scores a loan, and prohibited if pointed at social scoring. "Everyone uses the same models" is true and beside the point: an enterprise running one model across forty purposes has forty classifications to make, because it is the use that is regulated, not the licence.

That is what makes an AI inventory hard. The difficult part is not recording which models are in use; it is mapping every distinct thing they have been pointed at, classifying each one the same way, and keeping the resulting obligations and dates right as the law moves. Any competent practitioner can classify one system by hand. Nobody can classify two hundred consistently, each with a defensible record, by hand. That gap is what these instruments narrow: they make the classification consistent and the record citable, while the intake answers remain the assessor's judgement.

## What is in the repository

Four components, with their status stated plainly so nothing here is oversold:

- **Triage engine and register mode** (`aiact-triage`, the Python package). Working and tested (38 tests, no runtime dependencies). Classifies one use case or a whole inventory and produces the audit records. This is the core; the rest builds on the classification it produces.
- **AI inventory template** in PRA SS1/23 vocabulary (`templates/ai_inventory_template.csv`). Complete. A single file that is both a model-risk inventory and the engine's input, so the inventory and the AI register cannot drift apart. Documented in [docs/INVENTORY.md](docs/INVENTORY.md).
- **Third-party AI due-diligence questionnaire** (`templates/third_party_ai_due_diligence.md`). Complete. Thirty questions for assessing a vendor-supplied AI system, each carrying the framework anchor it evidences (ISO/IEC 42001 Annex A, DORA Articles 28 to 30, the AI Act, PRA SS1/23, or the OWASP LLM Top 10).
- **Governed LLM intake assistant** ([docs/DESIGN_llm_component.md](docs/DESIGN_llm_component.md)). Designed, not yet built. An LLM front-end that drafts intake answers for a human to confirm, governed by the toolkit's own instruments. Its evaluation results will be published here when they exist and not before.

The rest of this README covers the engine in depth, then the companion components.

## The triage engine

### What it outputs

For a single system, a findings-and-obligations report:

```
$ aiact-triage assess examples/cv_screening.json

Use case: CV screening tool for graduate recruitment
Role:     deployer
Tier:     HIGH-RISK (Article 6)

Findings:
  [Art. 6(2), Annex III, 4] High-risk: Employment, workers' management...

Obligations and dates (original -> as amended by the Digital Omnibus):
  [Art. 26(2)] Assign human oversight to natural persons with the necessary competence...
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
```

For an inventory, one markdown audit record per system plus a portfolio summary:

```
$ aiact-triage register examples/inventory.csv --out audit --assessor "B. Struve"

## Systems by tier
- PROHIBITED (Article 5): 1
    - Workplace wellbeing emotion monitor (pilot)
- HIGH-RISK (Article 6): 2
    - CV screening assistant
    - Credit scoring model
...
## Attention items
- Credit scoring model: fundamental rights impact assessment (Art. 27) required before first use.
- Exam-marking consistency checker: relies on the Art. 6(3) derogation; the
  assessment must be documented and the system registered.
- Workplace wellbeing emotion monitor (pilot): prohibited practice recorded. Escalate; no compliance pathway exists.

## Deadline calendar
Upcoming:
- 2027-12-02  Art. 26(2)  (2 systems)
```

Each audit record carries the assessment date, the tool version, the rule-set verification date, the assessor, the answers as recorded, and every obligation with both dates. That record is the artefact a governance function actually needs: something dated and citable that can be put in front of an internal audit or a market-surveillance question. The register mode is where the engine earns its place; the single-assessment mode exists so one classification can be inspected and discussed on its own.

### Why the dual dates

As of July 2026 the Digital Omnibus on AI has passed the European Parliament (16 June 2026) and the Council (29 June 2026) and was signed on 8 July 2026, but has not yet been published in the Official Journal. Until publication, the original dates remain the binding law while the amended dates (Annex III high-risk obligations moving to 2 December 2027, Annex I to 2 August 2028, the Article 50(2) marking grace to 2 December 2026) are the operative planning baseline. Both facts are true at once, so every obligation is reported with both dates and a status flag, and the legal status is stated on every output. Classification guides written before mid-2026 mostly show a calendar that is now wrong; this engine shows both calendars and says which one binds.

### How classification works, briefly

Three gates, in the Act's own order. Article 5 first: a prohibited practice ends the assessment, since no compliance pathway exists. Then Article 6 high-risk, via Annex I (AI in regulated products) or Annex III (the eight listed use-case areas), applying the Article 6(3) derogation where claimed, and blocking it where the system profiles natural persons. Then Article 50 transparency duties, which stack with high-risk rather than replacing it. Provider and deployer duties are kept apart throughout: a deployer running a vendor's chatbot sees the vendor's Article 50(1) duty as a counterparty note for due diligence, not as its own obligation.

The full framework, the reasoning behind each design choice, and the line between what the engine decides and what the assessor decides are in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Install and run

Python 3.11+, no runtime dependencies.

```
pip install -e ".[dev]"
aiact-triage interactive                 # walk the intake for one system
aiact-triage assess case.json            # assess one saved case
aiact-triage register inventory.csv --out audit   # assess a whole inventory
pytest                                   # worked classification cases
```

The register accepts CSV (the shape of a real AI inventory; unknown columns such as owner or vendor pass through into the audit record) or a JSON list of cases. See `examples/`.

## The inventory template and cross-framework flags

`templates/ai_inventory_template.csv` is an AI inventory in PRA SS1/23 vocabulary that runs directly through the register mode: the model risk columns (model id, owner, tier, validation cycle, known limitations) pass through into each system's audit record, while the classification columns drive the triage. One file is both the model inventory and the assessment input, which is the practical answer to inventories and AI registers drifting apart. Field-by-field definitions and the SS1/23 anchors are in [docs/INVENTORY.md](docs/INVENTORY.md).

Classifications also rarely travel alone, so the engine raises knock-on flags into adjacent frameworks from `src/aiact_triage/data/cross_framework.json`: a system in a regulated financial firm is flagged into the SS1/23 model inventory and tiering expectations; a vendor-supplied system in a financial entity is flagged into the DORA register of information (Article 28(3)) and its contract checked against the key contractual provisions (Article 30); any vendor-supplied system is flagged to the ISO/IEC 42001 supplier controls; and emotion recognition or biometric categorisation is flagged for a GDPR data protection impact assessment where Article 9 special-category data may be engaged. The flag names the adjacent obligation; it does not assess it.

## The due-diligence questionnaire

`templates/third_party_ai_due_diligence.md` assesses a vendor-supplied AI system before contract, at renewal, and on any material change. Run the classification first: the depth of diligence scales with the AI Act tier and, in a financial firm, the SS1/23 model tier, so a minimal-risk summariser is not interrogated like a high-risk credit model. Each of the thirty questions names the framework anchor it evidences and the artefact to request, and answers without evidence are recorded as assertions rather than answers. It closes with a proceed, proceed-with-conditions, or decline verdict attached to the system's inventory row and triage record.

## Where the rules live

All legal content sits in `src/aiact_triage/data/*.json`, separate from the engine, with an article citation on every rule and a metadata block recording sources; the rule set's verification date is recorded in the timeline data and carried into every audit record. The encoding draws from Regulation (EU) 2024/1689 and, for the amendments, Regulation (EU) 2026/1744, both as published in the Official Journal. When the Omnibus was published on 24 July 2026, every encoded date was re-verified against the Official Journal text and survived unchanged; any future date correction remains a one-file change, and the tests that assert dates read from the same file.

The engine encodes a curated, hand-maintained subset of the Act (the provisions bearing on classification), not the full text, and it does not update itself. That trade is deliberate and is set out in the methodology document.

## Scope, limits and status

Built for the deployer's position; the provider case is handled at summary level. General-purpose AI model obligations (Articles 51 to 56) are out of scope. Annex I is handled at the level of "product under Annex I harmonisation legislation" rather than per instrument. The Omnibus dates are verified against Regulation (EU) 2026/1744 as published in the Official Journal. The LLM intake assistant is a design, not running code, until its evaluation results appear here. Not legal advice.
