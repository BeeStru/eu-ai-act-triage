# Control matrix

Ten controls over the eu-ai-act-triage repository, tested at `main` =
`7aab9f95065f9cf69cbdefe5a9aed64c361386ce`, the scope-freeze commit, with
fieldwork on 11 October 2026. Remediation retests for CA-07 and CA-08 ran
the same day at `22ad85f3276040aceec29bff4eba34caacdd1d53`; the original
results stand, with the remediation status beside them. Owner throughout: B. Struve, sole maintainer;
the concentration that creates is itself tested by CA-10. Every result cell
cites the workpaper that supports it, in [`evidence/`](evidence/).

| ID | Control | Objective | Type | Mode | Frequency | Criteria anchor | Design effectiveness | Operating effectiveness |
|---|---|---|---|---|---|---|---|---|
| CA-01 | Version control over all source, rule data and documentation | Every change is tracked, attributable and reversible | Preventive, with a detective audit trail | Automated substrate, manual discipline | Continuous | SSDF PS.1 | Design effective ([WP-CA01-design-20261011](evidence/WP-CA01-design-20261011.md)) | Operating effectively ([WP-CA01-operating-20261011](evidence/WP-CA01-operating-20261011.md)) |
| CA-02 | Protected main branch | Changes cannot reach `main` without passing required checks | Preventive | Automated (configuration) | Continuous | SSDF PS.1; ISO 27001 A.8.32 | Design deficiency ([WP-CA02-design-20261011](evidence/WP-CA02-design-20261011.md)) | Not applicable ([WP-CA02-operating-20261011](evidence/WP-CA02-operating-20261011.md)) |
| CA-03 | CI runs the full test suite on every push and pull request | Regressions in classification logic are detected before persisting on `main` | Detective | Automated | Each push and PR | ISO 27001 A.8.32 (corrected 11 October 2026); the CI workflow's declared behaviour | Design effective ([WP-CA03-design-20261011](evidence/WP-CA03-design-20261011.md)) | Operating effectively ([WP-CA03-operating-20261011](evidence/WP-CA03-operating-20261011.md)) |
| CA-04 | Packaged-data integrity check in CI (non-editable reinstall) | The installed package a user receives carries the legal rule data | Detective | Automated | Each CI run | ISO 27001 A.8.32 (corrected 11 October 2026); the CI workflow's declared behaviour | Design effective ([WP-CA04-design-20261011](evidence/WP-CA04-design-20261011.md)) | Operating effectively ([WP-CA04-operating-20261011](evidence/WP-CA04-operating-20261011.md)) |
| CA-05 | Test suite covering the classification gates, with a regression file | Errors in Article 5, 6 and 50 logic are caught by named worked cases | Detective | Automated suite, manual maintenance | Each CI run | ISO 27001 A.8.32 (corrected 11 October 2026); the README's own test-count claim | Design effective ([WP-CA05-design-20261011](evidence/WP-CA05-design-20261011.md)) | Operating effectively ([WP-CA05-operating-20261011](evidence/WP-CA05-operating-20261011.md); [WP-CA05-operating-20261011-reperformance](evidence/WP-CA05-operating-20261011-reperformance.md)) |
| CA-06 | Zero-runtime-dependency policy | Classification behaviour cannot change through a third-party dependency update | Preventive | Manual policy, automated verification | Each release | The README's own zero-dependency claim (corrected 11 October 2026) | Design effective ([WP-CA06-design-20261011](evidence/WP-CA06-design-20261011.md)) | Operating effectively ([WP-CA06-operating-20261011](evidence/WP-CA06-operating-20261011.md); [WP-CA06-operating-20261011-reperformance](evidence/WP-CA06-operating-20261011-reperformance.md)) |
| CA-07 | Rule-data citation and verification-date discipline | Every encoded legal rule traces to its article and a dated verification | Preventive | Manual | Each rule-data change | The repository's own metadata convention | Design effective ([WP-CA07-design-20261011](evidence/WP-CA07-design-20261011.md), with the correction recorded in [WP-CA07-operating-20261011](evidence/WP-CA07-operating-20261011.md)) | Operating exception ([WP-CA07-operating-20261011](evidence/WP-CA07-operating-20261011.md)). Remediation: remediated during fieldwork ([WP-CA07-remediation-20261011](evidence/WP-CA07-remediation-20261011.md)) |
| CA-08 | Documentation accuracy (claims written after the code works) | README status claims match observable behaviour | Detective | Manual | Each README change | The README's own statements. Each status claim is tested against what the repository actually does. (Corrected 11 October 2026.) | Not applicable: design and operating collapse into one test ([WP-CA08-operating-20261011](evidence/WP-CA08-operating-20261011.md)) | Operating exception ([WP-CA08-operating-20261011](evidence/WP-CA08-operating-20261011.md)). Remediation: claims 6, 17, 18 and 23 remediated during fieldwork; claim 24 open ([WP-CA08-remediation-20261011](evidence/WP-CA08-remediation-20261011.md)); claim 25 remediated during fieldwork ([WP-CA07-remediation-20261011](evidence/WP-CA07-remediation-20261011.md)) |
| CA-09 | Release versioning discipline | Published tags correspond to the package version and a reproducible tree state | Preventive | Manual | Each release | SSDF PS.3, task PS.3.1 (corrected 11 October 2026) | Design effective ([WP-CA09-design-20261011](evidence/WP-CA09-design-20261011.md)) | Operating effectively ([WP-CA09-operating-20261011](evidence/WP-CA09-operating-20261011.md)) |
| CA-10 | Independent review of changes (segregation of duties) | No change reaches `main` on one person's judgement alone | Preventive | Manual | Each change | ISO 27001 A.5.3; SSDF PW.7, task PW.7.2 (corrected 11 October 2026) | Design deficiency ([WP-CA10-design-20261011](evidence/WP-CA10-design-20261011.md)) | Not applicable: the control does not exist to operate ([WP-CA10-design-20261011](evidence/WP-CA10-design-20261011.md)) |

**Criteria anchors corrected, 11 October 2026.** After fieldwork, every anchor
was checked against the text of NIST SP 800-218 (SSDF v1.1) and the titles of
the ISO/IEC 27001:2022 Annex A controls. An anchor stays only where the
practice text, or the ISO control title with its published implementation
guidance, names the activity the control performs.
Five did not, and were replaced. The tests, their evidence and their results
are unchanged.

- CA-03 and CA-05: A.8.29, "Security testing in development and acceptance",
  replaced by A.8.32, "Change management". These tests check classification
  logic, not security properties. Testing of changes is part of change
  management: the ISO/IEC 27002:2022 implementation guidance for 8.32 names
  it, as read in a secondary source (isms.online), not the standard's text.
- CA-04: SSDF PW.8, which tests executable code to identify vulnerabilities
  and verify security requirements, replaced by A.8.32 for the same reason.
  The check proves the installed package carries the rule data; it looks for
  no vulnerability.
- CA-09: SSDF PS.2, which covers integrity verification information for
  acquirers (published hashes, code signing), replaced by PS.3, "Archive and
  Protect Each Software Release", task PS.3.1. The control publishes no hashes
  or signatures; what the tags do is preserve each release as an identifiable
  tree.
- CA-10: A.8.32 and SSDF PW.8 replaced by A.5.3, "Segregation of duties", and
  SSDF PW.7, code review and analysis, whose task PW.7.2 gives peer review of
  code as its first example.

CA-03 and CA-04 also name the CI workflow's declared behaviour, the
repository's own commitment that their design tests inspected. Confirmed
unchanged: CA-01 (PS.1, task PS.1.1, example 2: version control tracking
every change with accountability to the individual account), CA-02 (PS.1;
A.8.32), CA-06 (PW.4, task PW.4.4: third-party components verified against
the organisation's requirements), CA-07 and CA-08 (the repository's own
conventions).

**Further criteria corrections, 11 October 2026, by B. Struve's ruling.**
These supersede the count of five and the CA-06 and CA-08 confirmations
above: six anchors were corrected, and CA-08's criterion restated. The tests, their
evidence and their results are unchanged.

- CA-06: SSDF PW.4 removed, leaving the README's own zero-dependency claim
  (README lines 15 and 80) as the criterion. PW.4 is "Reuse Existing,
  Well-Secured Software When Feasible Instead of Duplicating
  Functionality", and its task PW.4.4 verifies third-party
  components; the control's point is that there are none, so the practice
  does not name what the control does.
- CA-08: "The repository's own convention" replaced by "The README's own
  statements. Each status claim is tested against what the repository
  actually does." The convention first named is not written in the
  published tree.
