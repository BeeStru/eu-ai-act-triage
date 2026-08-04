# Methodology and classification framework

This document explains the classification engine: what it does, the framework it applies, and the reasoning behind the design choices. It is the reference for a reader who wants to understand the classification logic rather than just run the tool, and it assumes familiarity with the EU AI Act only at a general level. The engine is the core of a wider toolkit; the AI inventory template, the vendor due-diligence questionnaire, and the design for the LLM intake assistant carry their own reasoning in `docs/INVENTORY.md`, the questionnaire itself, and `docs/DESIGN_llm_component.md`.

## 1. Why the tool exists

Organisations use the same AI systems for very different things, and the EU AI Act regulates the use, not the system. Classification turns on deployed purpose: the same base model is minimal-risk drafting marketing copy, high-risk screening job applicants or scoring loans, and prohibited if pointed at social scoring. An enterprise running one model across forty purposes therefore has forty classifications to make, not one, and each classification carries its own obligations and its own dates.

This is what makes AI inventory work hard, and it defines what a triage tool should and should not do. Classifying one system is easy for a competent assessor; three questions often settle it. Classifying a whole register the same way every time, with a dated record per system citing the articles relied on, and keeping the dates right while the law itself is mid-amendment, is not something anyone does reliably by hand. So the tool automates the mechanical layer (the classification order, the obligation mapping, the citations, the dual calendar) and leaves the judgement layer with the person. It is a simple compliance tool on purpose: its value is consistency, auditability and legal currency maintained by hand, not algorithmic cleverness.

## 2. Purpose and scope

The engine performs the first step of AI Act compliance: deciding, for an AI use case, which risk tier it falls into and which obligations follow, one system at a time or across a whole inventory. It is built for the deployer's position (an organisation using an AI system), though it also handles the provider case and flags where a deployer crosses into provider status.

In scope: the four risk tiers under Regulation (EU) 2024/1689; the Article 5 prohibitions; high-risk classification under Article 6 via Annex I and Annex III; the Article 6(3) derogation; Article 50 transparency duties; the deployer obligations under Article 26 and the Article 27 fundamental rights impact assessment; and the application dates under both the original Act and the Digital Omnibus amendments.

Out of scope: general-purpose AI model obligations (Articles 51 to 56), which sit with foundation-model providers rather than deployers; the internal detail of conformity assessment procedures; and per-instrument treatment of Annex I product legislation, which is handled at the level of "covered by Annex I harmonisation legislation" rather than device by device.

Because classification attaches to the use case (section 1), the unit of assessment is a use case, and the tool runs in two modes: a single assessment, and a register mode that assesses a whole inventory and writes one audit record per system plus a portfolio summary. The register mode is where the tool earns its place; the single mode exists so one assessment can be inspected and discussed on its own.

## 3. The classification framework

The Act sorts AI systems into four tiers by the risk they present. The tool applies them in the Act's own order, and that order does work in the assessment rather than being cosmetic.

**Prohibited (Article 5).** A small set of practices that may not be placed on the market, put into service, or used in the EU at all. This gate runs first and is terminal: if a system is prohibited, there is no compliance pathway to compute, so the tool stops. Reporting obligations for a system that cannot lawfully exist would be misleading.

**High-risk (Article 6).** Systems permitted but subject to the heaviest requirements. Two routes in: Annex I, where the AI is a safety component of, or is itself, a product already regulated under EU harmonisation legislation (medical devices, lifts); and Annex III, a closed list of eight use-case areas (biometrics, critical infrastructure, education, employment, essential services, law enforcement, migration, justice and democratic processes). Most workplace AI questions land in the Annex III employment area.

**Limited risk: transparency (Article 50).** Duties to tell people they are dealing with AI: disclosing that a chatbot is a machine, marking synthetic media, disclosing deepfakes. These are not a separate box lower than high-risk; they stack. A high-risk recruitment chatbot still owes the Article 50 disclosure on top of its Article 26 duties. The tool treats Article 50 as an overlay, not an alternative.

**Minimal risk.** Everything else. No specific obligations beyond the standing Article 4 duty to support AI literacy among staff, which applies to almost all organisational use and so is always noted.

## 4. The decision logic, gate by gate

### Gate 1: Article 5

The assessor answers a yes/no screen against each prohibited practice (the eight original prohibitions plus the new Omnibus prohibition on systems for generating non-consensual intimate imagery or child sexual abuse material). Any "yes" classifies the system as prohibited and stops the assessment. The prohibition's own application date is attached: 2 February 2025 for the original eight, 2 December 2026 for the new one.

### Gate 2: Article 6, with the Article 6(3) derogation

If the system is an Annex I product, it is high-risk and the assessment attaches the provider obligations (or, for a deployer, the Article 26 deployer duties), dated to the Annex I calendar (originally 2 August 2027, amended to 2 August 2028).

Otherwise the assessor selects the matching Annex III area, if any. Selecting one does not automatically make the system high-risk, because Article 6(3) provides a derogation: an Annex III system is not high-risk where it does not pose a significant risk of harm to health, safety or fundamental rights, and it meets at least one of four conditions (it performs a narrow procedural task; it improves the result of a completed human activity; it detects patterns without replacing or influencing a human assessment; or it performs a preparatory task).

The tool encodes one hard rule that catches people out: the derogation is unavailable where the system performs profiling of natural persons, regardless of the conditions. So a credit-scoring model that profiles applicants cannot use the derogation and is high-risk, while a duplicate-application detector that performs a narrow procedural task and does no profiling can. Where the derogation applies, the tool records that the assessment must be documented and the system registered in the EU database, a duty the Omnibus specifically retained.

This gate is where the tool draws its firmest line between its job and the assessor's. The tool applies the profiling rule and the condition logic mechanically. It does not decide whether a system "poses a significant risk of harm", because that is a judgement the Act assigns to a person. The tool structures that judgement; it does not make it. See section 6.

### Gate 3: Article 50

Independently of the high-risk result, the assessor answers whether the system interacts with people, generates synthetic content, does emotion recognition or biometric categorisation, or produces deepfakes. Each trigger attaches the corresponding duty, and each duty is assigned to the right party. Article 50(1) and 50(2) are provider duties; 50(3) and 50(4) are deployer duties. This matters for the deployer case: when a deployer runs a vendor's chatbot, the provider's Article 50(1) duty is surfaced as a counterparty note for vendor due diligence rather than logged as the deployer's own obligation. A checklist that ignored the split would hand the deployer a duty that is legally the vendor's.

## 5. The dual-timeline design

The tool reports two application dates for every obligation. This shapes more of the design than anything else in the tool.

The Digital Omnibus on AI, Regulation (EU) 2026/1744, was published in the Official Journal on 24 July 2026 and entered into force on 27 July 2026. It amends the Act's timeline, most significantly postponing the high-risk obligations for stand-alone Annex III systems from 2 August 2026 to 2 December 2027, and for Annex I systems from 2 August 2027 to 2 August 2028. It gives providers of generative systems placed on the market before 2 August 2026 until 2 December 2026 to comply with the Article 50(2) marking duty, and it adds the new Article 5 prohibition, which applies from 2 December 2026. Since entry into force, the amended dates are the binding law.

The original dates stay in the schema as historical and audit context, and keeping them is a design position, not a leftover. A register is an audit artefact: assessments recorded before 27 July 2026 were made under the original calendar and can only be audited against it, and obligations that were already applying before the amendment, such as the prohibitions and the Article 4 literacy duty, carry original dates the Omnibus never moved. So every obligation keeps both dates and a status flag (in application, unchanged, postponed by the Omnibus, or introduced by the Omnibus), and the output states the legal status in full. The amendment itself exercised the design: when the Official Journal text was published, every encoded date was re-verified against it and survived unchanged, and the realignment was committed data file by data file with the Official Journal citation, the correction in one place that section 8 promised.

## 6. What the tool decides, and what the assessor decides

The tool runs fixed rules over the answers an assessor gives it. It is deliberately not a language model and does not read free-text descriptions of systems. Where the line falls between the two is a deliberate choice, not an accident of what was easy to build.

The tool owns the parts that should be consistent and are error-prone by hand: applying the classification order, attaching the correct obligations to the correct party, mapping each obligation to its article, and reporting the right dates under both regimes. These are exactly the tasks where a person working across many systems makes slips.

The assessor owns the judgement the Act reserves for a person: whether a described system genuinely falls in an Annex III area, whether it profiles natural persons, and whether it poses a significant risk of harm for the purposes of the derogation. An intake instrument that claimed to make those calls would be giving false comfort. Structuring the judgement, recording it, and applying the legal consequences consistently is more useful than automating it away.

## 7. Cross-framework flags

An AI Act classification rarely travels alone. The same system usually has a home in the deployer's model risk framework, its ICT third-party register, or its data protection obligations, and a triage that ignored those homes would hand the assessor a result stripped of its context. So the engine raises knock-on flags from a dedicated rule file (`src/aiact_triage/data/cross_framework.json`): financial-services context flags the system into the PRA SS1/23 model inventory and tiering expectations, and, for high-risk systems, maps the Article 26 duties onto the SS1/23 lifecycle principles; a vendor-supplied system in a financial entity is flagged into DORA's register of information (Article 28(3)) and its contract checked against the key contractual provisions (Article 30); any vendor-supplied system is flagged to the ISO/IEC 42001 supplier controls; and emotion recognition or biometric categorisation is flagged for a GDPR data protection impact assessment (Article 35(3)(b)) where Article 9 special-category data may be engaged.

The flags are deliberately shallow. Each names the adjacent obligation and where it lives; none attempts to assess it, because each of those frameworks has its own assessment discipline and pretending to perform it in passing would be false comfort. Prohibited systems receive no flags: their only next step is escalation. One vocabulary point the flags enforce: the SS1/23 model tier (the firm's own materiality-and-complexity ranking) and the AI Act risk tier (a legal classification) answer different questions, and the inventory template records both without conflating them.

## 8. Sources and verification

All legal content is held in the package data directory (`src/aiact_triage/data/`) as JSON, separate from the engine, with an article citation on every rule and a metadata block recording sources; the rule set's verification date is recorded in the timeline data and carried into every audit record. Encoding is drawn from Regulation (EU) 2024/1689 and, for the amendments, from Regulation (EU) 2026/1744 (OJ L, 24.7.2026), both as published in the Official Journal.

The tool does not parse the full text of the Regulation and it does not update itself. It encodes a curated subset, the provisions that bear on classification, maintained by hand. This is a deliberate choice: ingesting the whole Act or scraping for changes would add fragility and a maintenance burden out of proportion to the tool's purpose, and it would work against the aim of keeping every rule readable and individually citable. The trade is stated so a reader knows what they are relying on. What the tool guarantees is that the provisions it covers are cited and were correct on the verification date recorded in the data files. What it does not guarantee is completeness across every article of the Act, or currency without a human updating it.

The amended dates were encoded from the compromise text and re-verified against the Official Journal text of Regulation (EU) 2026/1744 on its publication on 24 July 2026; every date survived unchanged, and the alignment was committed file by file with the Official Journal citation. Because the legal content sits in versioned data files, those commits are themselves a record that the law was tracked to source.

## 9. Known limits

The Annex I route is handled at the level of "product under Annex I harmonisation legislation" rather than per instrument, which is adequate for a deployer triage but coarser than a specialist product-safety assessment would need. The law-enforcement exceptions inside the real-time biometric identification prohibition are surfaced in the intake question rather than modelled individually.

Article 26 coverage is deliberately partial and here is the boundary: the engine encodes 26(1), (2), (4), (5), (6), (7) and (11), plus Article 27. The remaining paragraphs (registration verification for public deployers, the DPIA linkage, the law-enforcement authorisation regime for post-remote biometric identification, and the duty to cooperate with authorities) are situational duties better handled in the audit record's notes than as universal rows, and a deployer in those situations should read Article 26 in full.

Two safety behaviours bound what the engine will tolerate rather than what it covers. Unknown rule ids fail closed: a typo in a prohibited-practice flag or an Annex III area holds the system at high-risk and marks the assessment as needing review, because silently under-classifying on corrupted input is the one failure a register tool must not have. And consistency checks flag answer combinations the Act makes consequential (emotion recognition at work with the Article 5(1)(f) screen answered no; essential-services profiling with the Article 27 trigger answered no) instead of letting them pass. The engine still assesses one system at a time against the assessor's answers; it is an intake and classification instrument, not a full compliance-management system.
