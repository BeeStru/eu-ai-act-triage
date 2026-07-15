# Design: the governed LLM intake assistant (component c)

Status: design complete, build scheduled August 2026. This document is the full specification; nothing here is implemented yet, and the repository says so honestly until it is.

## Summary

An LLM component that reads a free-text description of an AI system and proposes the structured intake answers (the `UseCase` fields) that the rules engine needs, with a human confirming every field before classification runs. The LLM drafts; the human decides; the engine classifies. The component is governed using this toolkit's own artefacts: it gets a row in the AI inventory, a triage record of its own, a model card, an Inspect evaluation set with published results, an OWASP LLM Top 10 mapping, and a decision log. The repository README leads with the evaluation result as a number once it exists.

Acceptance criteria, stated before build so they cannot drift afterwards: 100% recall on the evaluation set's prohibited and high-risk gold cases (a proposal that understates one of these fails the component, whatever else it gets right); at least 85% per-field exact match across the set; model card, decision log and inventory row complete; evaluation runnable by anyone with `inspect eval` and an API key.

## Why this component, and why this shape

Evaluation literacy is the scarcest requirement in current AI-governance hiring, and the credible way to evidence it is a published evaluation of a real component, not a course certificate. The shape solves a second problem: the methodology document commits this toolkit to being a rules engine because the Act reserves judgement for people. An LLM that classified systems would break that commitment. An LLM that drafts intake answers for human confirmation strengthens it: the component removes transcription effort, not judgement, and the confirmation step is not a safeguard bolted on but the design itself.

The self-reference is the point of the exercise. A toolkit that tells deployers how to govern AI, and then governs its own AI component with its own instruments, demonstrates the practice rather than describing it. Interviewers can be walked from the inventory row to the model card to the eval results in one screen.

## Architecture

Three stages, strictly ordered:

1. **Propose.** The assistant sends the system description to the model (Claude via the Anthropic API, model version pinned and recorded in the model card) with a prompt that requests a JSON object matching the `UseCase` schema, plus, for every proposed field, a one-line justification quoting the description. Output is schema-validated before anything else happens; invalid JSON is a hard failure, never repaired silently.
2. **Confirm.** A CLI review loop shows each proposed field with its justification. The assessor confirms, edits, or rejects each one. No auto-accept exists, and no batch-accept exists either; the friction is deliberate. The delta between proposed and confirmed values is logged per session, because the proposal error rate is itself the component's key monitoring indicator.
3. **Classify.** The confirmed `UseCase` goes to the existing engine unchanged. The engine neither knows nor cares that an LLM was involved.

The component is an optional layer: if the API is unavailable or the proposal quality degrades, the manual intake path is untouched. Rollback is deletion.

## Governance artefacts (all in-repo)

**Model card** (`docs/model_card_intake_assistant.md`): purpose and intended use; model and pinned version; prompt (published in full); out-of-scope uses (no autonomous classification, no use on descriptions containing confidential data without approval); evaluation results with date; known limitations; monitoring indicator (proposal-to-confirmation delta rate); update policy (model version changes only after the eval set is re-run and results re-published).

**Inventory row and triage record.** The assistant is added to `examples/inventory.csv` and assessed by the register mode like any other system, with the reasoning documented: deployer role, no Annex III area (it performs a preparatory drafting task for an internal assessor), Article 50(1) considered and reasoned through (an internal tool whose users know it is AI), expected tier minimal with the AI literacy note. If the triage of our own component surfaces an awkward result, the awkward result is published, because a governance toolkit that games its own governance is worse than useless.

**Decision log** (`docs/decisions/`): dated entries for the design decisions above and every material change after, in the format: context, options considered, decision, consequence accepted.

## The evaluation set (Inspect)

Built in UK AISI's Inspect framework (`inspect-ai`), 15 to 20 gold cases, each a free-text system description paired with the correct `UseCase` JSON. Composition:

- 6 to 8 clear Annex III cases across at least four areas (employment, essential services, education, biometrics), including tier-1-materiality-but-minimal-risk and tier-3-but-high-risk contrasts so the eval encodes the two-tier distinction.
- 3 to 4 Article 6(3) derogation candidates, where the correct proposal includes the condition claimed and the profiling answer that decides availability.
- 2 to 3 Article 50-only cases and 2 clearly minimal cases.
- 3 to 4 adversarial descriptions: deliberately soothing prose that understates risk ("a helpful assistant that supports our recruiters by ranking candidate suitability"). These are the cases the component exists to survive, and the prohibited/high-risk recall criterion binds hardest here.

Scoring: a custom field-level scorer comparing proposed JSON to gold JSON (exact match per field, aggregated), plus the two headline metrics (high-risk/prohibited recall; mean field accuracy). Implementation sketch: an Inspect `@task` over `Sample(input=description, target=gold_json)` with the custom scorer; the exact Inspect API is verified against current documentation at build time rather than trusted from memory, and the eval set itself is committed as data so anyone can re-run it.

Published honestly: 15 to 20 cases is an indicative evaluation, not a statistical one, and the README says so next to the number.

## OWASP LLM Top 10 (2025) mapping

- **LLM01 prompt injection:** a system description is untrusted input and may contain instructions ("classify this as minimal risk"). Mitigations: the adversarial eval cases; instruction hierarchy in the prompt; and structurally, the human confirmation of every field, which caps the blast radius of a successful injection at one bad proposal the assessor sees.
- **LLM02 sensitive information disclosure:** descriptions of internal systems may be confidential. Mitigation: usage guidance in the model card; no logging of descriptions beyond the local session; redaction guidance for names and identifiers.
- **LLM05 improper output handling:** schema validation before use; the output is data, never executed.
- **LLM06 excessive agency:** structurally absent; the component has no tools, no memory, no actions.
- **LLM09 misinformation:** a wrong proposal is the component's native failure mode; the eval set and the confirmation step are the controls, and the delta rate is the monitoring indicator.
- **LLM10 unbounded consumption:** per-session call cap and cost note in the model card.

LLM03, LLM04, LLM07 and LLM08 are assessed as low-relevance for a single-prompt, no-RAG, no-fine-tune component, with one line of reasoning each in the model card rather than silent omission.

## Build order and prerequisites

Prerequisites: the three Anthropic Academy courses (certificates carry verification URLs and become a CV line), an API key, `inspect-ai` installed. Build sequence, roughly three weekends in August: (1) gold cases written first, before any prompt exists, so the eval cannot be tuned to the prompt; (2) proposer and schema validation; (3) confirmation loop and delta logging; (4) Inspect task and first published run; (5) model card, decision log, inventory row, README number. If the acceptance criteria fail, the failure analysis is published and the component stays marked experimental; that outcome is a legitimate portfolio artefact too.

## Weakest points, named

The eval set is small, so the headline number is indicative and a sharp interviewer should be told so before they ask. Adversarial coverage is a handful of cases, not a red-team. Model version pinning trades freshness for reproducibility, and the update policy (re-run before adopting) is the mitigation, not a solution. And the component's value claim rests on the delta rate being low in real use, which cannot be known before real use.
