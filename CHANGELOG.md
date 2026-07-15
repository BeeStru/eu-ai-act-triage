# Changelog

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
