# Third-party AI due-diligence questionnaire

A structured questionnaire for assessing a vendor-supplied AI system before contract, at renewal, and on any material change to the system. Each question carries the framework anchor it evidences and the artefact to request. It pairs with the triage tool: run the classification first, because the depth of diligence should scale with the AI Act tier and, in a financial firm, the SS1/23 model tier. A minimal-risk meeting summariser does not need the same interrogation as a high-risk credit model, and pretending otherwise produces diligence theatre rather than diligence.

Framework anchors used below: ISO/IEC 42001:2023 Annex A (A.10.2 allocating responsibilities, A.10.3 suppliers, A.7 data for AI systems, A.8 information for interested parties); DORA (Regulation (EU) 2022/2554, Articles 28 to 30) where the deployer is a financial entity; the EU AI Act; PRA SS1/23 Principle 2.6 for firms in scope; OWASP LLM Top 10 (2025) for the security section where the system contains a language-model component.

How to complete: one questionnaire per system, attached to the system's row in the AI inventory and its triage record. Answers without evidence are recorded as assertions, not answers. Close with the verdict block.

## A. Supplier and system identification

1. Legal entity supplying the system, its ultimate parent, and the full subcontracting chain behind the AI functionality, including any upstream foundation-model provider. Evidence: corporate structure statement; list of material subcontractors. Anchors: ISO A.10.2; DORA Art. 28 (register of information records the chain, not just the counterparty).
2. System name, version, deployment model (SaaS, on-premise, API), and release cadence, including whether the underlying model can change without a version change. Evidence: product documentation; release policy. Anchors: ISO A.10.3; DORA Art. 30(2) service description.
3. The supplier's role under the AI Act for this system (provider, importer, distributor) and confirmation of the deployer's role, including the Article 25 triggers under which the deployer would become a provider (rebranding, substantial modification, repurposing into high-risk use). Evidence: supplier's written role statement. Anchors: AI Act Arts. 3, 25.
4. Whether the system is, or contains, a general-purpose AI model, and if so which upstream obligations (Articles 53 to 55) the model provider carries and how compliance is evidenced downstream. Evidence: GPAI provider documentation; model provenance statement. Anchors: AI Act Arts. 53 to 55; ISO A.10.2.

## B. Regulatory posture

5. The AI Act risk classification the supplier asserts for the system in the deployer's intended use, with the basis for it. Compare against the deployer's own triage result; investigate any mismatch before contract. Evidence: supplier classification memo. Anchors: AI Act Art. 6; this toolkit's triage record.
6. For asserted or triaged high-risk use: conformity assessment status, CE marking, and EU database registration status, on the amended timeline. Evidence: declaration of conformity or a dated compliance roadmap against 2 December 2027 (Annex III) or 2 August 2028 (Annex I). Anchors: AI Act Arts. 43, 47 to 49.
7. Availability and adequacy of instructions for use sufficient for the deployer to meet its Article 26 duties, in particular human oversight design and the characteristics of input data the system expects. Evidence: the instructions themselves, reviewed against Art. 26(1), (2) and (4). Anchors: AI Act Arts. 13, 26; ISO A.8.
8. For systems generating synthetic content or interacting with people: how the supplier meets Article 50, including machine-readable marking of outputs from 2 December 2026, and what the deployer must configure to stay compliant. Evidence: marking specification; disclosure mechanics. Anchors: AI Act Art. 50.
9. Named regulatory contacts: EU authorised representative where applicable (Article 22 for third-country providers of high-risk systems; Article 54 for third-country providers of general-purpose AI models, except where the model is released under a free and open-source licence with publicly available parameters and does not present systemic risk, Art. 54(6)), and the escalation contact for regulator or market-surveillance enquiries. Evidence: contact schedule in the contract. Anchors: AI Act Arts. 22, 54.

## C. Model and data

10. Training data provenance at summary level: sources, rights basis, whether deployer data is or will be used for training or fine-tuning, and the opt-out mechanics. Evidence: data provenance statement; contractual no-training clause where required. Anchors: ISO A.7; UK/EU GDPR.
11. Personal data processing: roles (controller/processor), the data processing agreement, sub-processor list and change notification, international transfer mechanism. Evidence: DPA; transfer impact assessment where relevant. Anchors: GDPR Arts. 28, 44 et seq.
12. Model documentation available to the deployer: model card or technical documentation, version history, and whether documentation access survives contract termination for records purposes. Evidence: the documentation itself. Anchors: ISO A.8; AI Act Art. 13.
13. Known limitations the supplier discloses: conditions under which performance degrades, populations or inputs where accuracy drops, and known failure modes. A supplier that discloses no limitations has not tested for them. Evidence: limitations section of documentation. Anchors: ISO A.8; SS1/23 (limitations recorded in the inventory).
14. Bias and fairness testing: what was tested, on which populations, with which metrics, and when last repeated. Evidence: test methodology and results summary. Anchors: ISO A.7; AI Act Art. 10 (for high-risk providers).

## D. Evaluation and testing

15. Pre-release evaluation results relevant to the deployer's use case, distinguishing generic benchmarks from use-case-specific evaluations. Evidence: evaluation report. Anchors: ISO A.10.3; SS1/23 2.6 (vendor models validated to the firm's own standards).
16. Red-teaming or adversarial testing: scope, date, internal or independent, and material findings with remediation status. Evidence: summary attestation; independent report where available. Anchors: ISO A.10.3; OWASP LLM Top 10 as the reference threat frame.
17. Regression assurance on updates: how the supplier tests that model or system updates do not degrade the deployer's use case, and whether the deployer is notified before or after changes take effect. Evidence: change management policy. Anchors: DORA Art. 30(3); SS1/23 2.6.
18. Deployer's own testing rights: API or environment access to run independent evaluations before go-live and periodically after. A refusal here is a finding in itself. Evidence: contractual testing clause. Anchors: ISO A.10.3; DORA Art. 30(3) audit and access rights.

## E. Security of the AI component (systems with an LLM component)

19. Prompt-injection resistance (LLM01) and system-prompt leakage (LLM07): what defences exist against instructions embedded in user inputs or processed documents, whether the system prompt is treated as disclosable and kept free of secrets, and what the residual risk statement says. Evidence: security architecture note; test results.
20. Output handling (LLM05): supplier guidance on treating model outputs as untrusted, including schema validation and sanitisation before downstream use. Evidence: integration guidance.
21. Model supply chain (LLM03) and training-data poisoning controls (LLM04): provenance of base models and fine-tuning data, and integrity controls over them. Evidence: supply chain statement.
22. Abuse and consumption controls (LLM10): rate limiting, quota management, and cost-containment mechanics available to the deployer. Evidence: technical documentation.

## F. Operational resilience and exit

23. Incident definition and notification: what counts as an incident (including model-behaviour incidents, not only availability), notification timescales, and the deployer's obligations it must support, including AI Act serious-incident reporting for high-risk systems. Evidence: incident schedule in the contract. Anchors: DORA Arts. 28, 30(3); AI Act Arts. 26(5), 73.
24. Audit, inspection and access rights for the deployer and its regulators, including over material subcontractors. Evidence: contract clause. Anchors: DORA Art. 30(3).
25. Exit strategy: data return and deletion, format and timescale, transition assistance, and what continuity looks like if the supplier fails or the contract terminates abruptly. Evidence: exit plan. Anchors: DORA Arts. 28(8), 30(3).
26. Sub-outsourcing changes: notification of material changes to the subcontracting chain and the deployer's right to object. Evidence: contract clause. Anchors: DORA Art. 30(2).
27. Concentration: the supplier's own dependency on a single upstream model or cloud provider, and the deployer's aggregate exposure to that upstream across its vendor estate. Evidence: dependency disclosure; deployer's own register analysis. Anchors: DORA Arts. 28(4), 29.

## G. Contract checklist (key provisions)

Before signature, confirm the contract contains: a complete service description including AI functionality and model change policy; data processing locations; availability and performance commitments; incident support and notification obligations; audit and access rights; testing rights; exit and data-return provisions; sub-outsourcing conditions; the no-training clause where required; and the regulatory cooperation clause. Anchors: DORA Art. 30(2) and (3) as the checklist spine, applied proportionately outside financial services.

## H. Ongoing monitoring

28. Performance and drift reporting: what the supplier provides on an ongoing basis, at what cadence, and which metrics map to the deployer's Article 26(5) monitoring duty. Evidence: reporting specification.
29. Material-change triggers: the defined changes (model swap, retraining, purpose extension) that trigger renotification, re-triage under this toolkit, and where relevant re-validation under SS1/23. Evidence: change notification clause; internal re-triage procedure.
30. Re-diligence cycle: this questionnaire re-run at contract renewal and at least annually for high-risk systems, with deltas recorded against the prior version. Evidence: completed prior questionnaires on file.

## Verdict

Outcome (one of): proceed; proceed with conditions (list them, with owners and dates); decline. Rationale in three sentences or fewer, referencing the question numbers that drove the outcome. Attach to the system's inventory row and triage record. Assessor, date, and next review date.

---

Sources and confidence: ISO/IEC 42001:2023 Annex A structure and control numbering (A.2 to A.10, 38 controls; A.10.2, A.10.3) cited at control level against multiple independent practitioner analyses, as the standard's text is paywalled. DORA anchors cited at article level from Regulation (EU) 2022/2554. OWASP references use the LLM Top 10 2025 edition. AI Act dates are verified against Regulation (EU) 2026/1744 as published in the Official Journal; see the packaged `timeline.json` rule file. Verification of these anchors is recorded in the commit history, not asserted here.
