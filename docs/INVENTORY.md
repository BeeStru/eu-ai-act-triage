# The AI inventory template

`templates/ai_inventory_template.csv` is an AI inventory in PRA SS1/23 vocabulary that doubles as the input to this tool's register mode. One file serves both purposes: the columns a model risk function needs for its inventory, and the columns the triage engine needs for AI Act classification. Run it directly:

```
aiact-triage register templates/ai_inventory_template.csv --out audit
```

## Why one artefact

Firms that treat the AI Act as a separate compliance exercise end up with two lists: a model inventory owned by risk and an "AI register" owned by compliance, drifting apart from the day they are created. SS1/23 already expects a comprehensive inventory covering vendor and in-house models alike. The PRA's model definition is broad enough that most AI systems in a financial firm are SS1/23 models. So the practical design is a single inventory carrying both vocabularies, where the model risk fields pass through into each system's audit record and the classification fields drive the triage. Adding a new system means adding one row.

Two classifications live side by side in this file and must not be conflated. The SS1/23 model tier is the firm's own risk-based ranking by materiality and complexity, set under Principle 1 and used to allocate validation effort. The AI Act tier is a legal classification with fixed consequences. A Tier 3 model of low materiality can still be high-risk under the Act (a small CV-screening pilot), and a Tier 1 model of the highest materiality can be minimal-risk under the Act (a market risk pricing model with no Annex III footprint). The template records both; the audit record shows both.

## Field definitions: model risk columns (pass through into the audit record)

**model_id.** The firm's unique identifier. SS1/23 Principle 1 expects the inventory to identify every model in scope, in-house and vendor alike.

**description.** Purpose, use and outputs. The inventory is expected to record what the model is for and how it is actually used, including divergence between intended and actual use.

**business_owner.** The accountable owner. SS1/23 places accountability with identified owners under the governance principle (Principle 2); recording ownership per model is the inventory's contribution to that chain.

**developer / vendor.** Who built it and, where external, who supplies it. Vendor models sit inside SS1/23 scope and attract Principle 2.6: the firm satisfies itself that vendor models are validated to the same standard as its own.

**model_status.** In development, in use, restricted, or decommissioned. The PRA expects decommissioned models to remain on the inventory with the rationale for retirement.

**model_tier / tier_rationale.** The firm's risk-based tier under Principle 1, weighing materiality and complexity. The complexity factors named by SS1/23 include interpretability, explainability, transparency and the potential for designer or data bias, which is where AI systems earn higher tiers than their materiality alone would suggest. The rationale column exists because a tier without a recorded basis does not survive validation review.

**upstream_dependencies / data_inputs.** Feeder models and data sources. Model interdependencies are part of the inventory's job, and input data quality and bias are tiering-relevant.

**known_limitations.** Documented weaknesses and the conditions under which outputs degrade. SS1/23 expects limitations, post-model adjustments and expert-judgement overlays to be recorded rather than carried in heads.

**validation_status / last_validated / next_validation_due.** The independent validation cycle under Principle 4, periodic and event-driven. For AI Act high-risk systems, the validation calendar is also where Article 26 monitoring naturally attaches.

**exceptions_open.** Open exceptions, restrictions or conditions of use, per the policies-and-procedures expectations on restricting or limiting model use.

## Field definitions: classification columns (drive the triage)

These are the UseCase fields documented in the methodology: role, annex_i_product, annex_iii_area, profiling_of_natural_persons, art_6_3_conditions, prohibited_flags, and the Article 50 trigger columns (interacts_with_natural_persons, generates_synthetic_content, emotion_recognition, biometric_categorisation, deepfake), plus fria_relevant and workplace_use. Booleans are yes/no; list fields are semicolon-separated ids from the data files.

Two context columns added in v0.3.0 drive the cross-framework flags:

**financial_services_context.** Yes where the deploying entity is a PRA or FCA regulated financial firm. Triggers the SS1/23 flags and, with vendor_supplied, the DORA third-party flag.

**vendor_supplied.** Yes where the system is bought rather than built. Triggers the ISO/IEC 42001 supplier-controls flag and feeds the due-diligence questionnaire.

## Sources

PRA SS1/23, Model risk management principles for banks (May 2023, updated April 2026), read alongside practitioner analyses of the inventory and tiering expectations; verification of these anchors is recorded in the commit history, not asserted here. Anchors are cited at principle level rather than paragraph level, deliberately: the template borrows the vocabulary and the expectations, and it does not claim to be a compliance artefact for SS1/23 itself.
