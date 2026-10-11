# Test scripts

The procedures for the ten controls in [`control_matrix.md`](control_matrix.md), as executed on 11 October 2026. Each test names the workpaper in [`evidence/`](evidence/) that holds its exact commands and full output. Where execution departed from the written procedure, the departure is marked "Deviation" at the step it affects. Each control's criterion is shown as corrected on 11 October 2026; the control matrix gives the reason for each correction.

## Conditions that apply to every test

- Object under test: a fresh clone of `https://github.com/beestru/eu-ai-act-triage`, taken at the start of each fieldwork session. Scope froze on fieldwork day one, 11 October 2026, at `main` = `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`: 45 commits, tags `v0.1.0` to `v0.5.0`. Each later session confirmed `main` unmoved before testing. The remediation retests ran on a fresh clone at `22ad85f3276040aceec29bff4eba34caacdd1d53`.
- Fieldwork window: the window opened on 27 August 2026 broke after one session and was restarted as a whole on 11 October 2026. Every test below ran on 11 October 2026; the 27 August workpapers are superseded, kept in `evidence/superseded/`, and not cited.
- Deviation, all GitHub-side evidence: the testing environment had no authenticated `gh` (exit 4), and the GitHub API was not used from it. Every GitHub-side item was captured outside it by B. Struve on 11 October 2026 and committed the same day, before or with the workpaper that uses it. How each file was captured is recorded in `WP-CA03-operating-20261011-capture-commands.txt` and `WP-CA08-remediation-20261011-capture-commands.txt`; the CA-02 items sit in the slots of WP-CA02-design-20261011, and the ruleset responses in `WP-CA02-design-20261011-rulesets.txt`.
- Execution: the commands run in the testing environment were executed by an AI coding assistant, Claude Code, under B. Struve's direction. It was never permitted to compose or edit output; where a command reshaped its own output (scratch paths shown as `<SCRATCH>`, escape bytes as `^[`), the reshaping is part of the recorded command. B. Struve re-ran every command himself, outside the testing environment, on 11 October 2026; the AI assistant compared the new output with each workpaper; B. Struve reviewed that comparison (phase4-reperformance-20261011). Four steps were not reperformed as written; section 6 of the findings memo names them.
- Sampling: automated controls (CA-02, CA-03, CA-04 and the automated halves of CA-05 and CA-06) by test of one, configuration stability from the configuration file's own history, and a completeness reconciliation where completeness matters. Manual controls (CA-01 discipline, CA-07, CA-08, CA-09, CA-10) by full population where it holds 25 items or fewer; above 25, the plan prescribes a haphazard sample of 25, stratified across the period.

## CA-01 Version control over all source, rule data and documentation

Criterion: SSDF PS.1.

Design test, inspection ([WP-CA01-design-20261011](evidence/WP-CA01-design-20261011.md)):

1. List author and committer identities over the commit population (`git log --format='%an %ae' | sort -u`, with counts), for attributability.
2. Install the package non-editably in a clean venv (`pip install .`), list what it installed (`pip show -f aiact-triage`), and reconcile that list against `git ls-files src/aiact_triage`, excluding the console-script launcher, packaging metadata and compiled bytecode. Deviation: the venv was created in the session scratchpad, not `/tmp`.

Result: design effective.

Operating test, inspection of the full commit population ([WP-CA01-operating-20261011](evidence/WP-CA01-operating-20261011.md)):

1. Author name, author address, committer and signature status for every commit on `main`; consistent author identity is the criterion.
2. History rewriting: from the repository activity feed, any force push and any break in the chain of each push's "before" and the previous push's "after"; whether every pushed "after" is an ancestor of HEAD; and each tag's target compared with the push that published it and with the head SHA GitHub recorded for its tag-ref CI run. Deviation: the activity feed stands in for the events endpoint the plan names "if useful", which returned no records because the period was outside its retention window.
3. Population: all 45 commits, 11 activity records and 5 tags. Deviation: 45 commits exceed the 25 at which the sampling rule prescribes a sample; all 45 were tested, as the plan's CA-01 procedure ("the full commit population") requires.

Result: operating effectively.

## CA-02 Protected main branch

Criterion: SSDF PS.1; ISO/IEC 27001:2022 A.8.32.

Design test, inspection of the branch-protection settings ([WP-CA02-design-20261011](evidence/WP-CA02-design-20261011.md)):

1. `gh api repos/beestru/eu-ai-act-triage/branches/main/protection`. Deviation: the command exited 4 in the testing environment (`gh` not authenticated); the output was captured by B. Struve outside it and entered in the workpaper's slot before its first commit.
2. Full-window screenshot of Settings > Branches, URL bar and system clock visible. Deviation: captured by B. Struve outside the testing environment, `WP-CA02-design-20261011-settings.png`.
3. Deviation, added scope: both planned items address classic branch protection only, so the rulesets endpoint and the branch-rules endpoint for `main` were captured as well (`WP-CA02-design-20261011-rulesets.txt`, both empty lists, exit 0). This closes that scope limit.

Result: design deficiency.

Operating test ([WP-CA02-operating-20261011](evidence/WP-CA02-operating-20261011.md)): not performed, because the plan runs it only if protection is enabled. No deviation.

Result: not applicable.

## CA-03 CI runs the full test suite on every push and pull request

Criterion: ISO/IEC 27001:2022 A.8.32, corrected from A.8.29 on 11 October 2026; the CI workflow's declared behaviour.

Design test, inspection of `.github/workflows/tests.yml` ([WP-CA03-design-20261011](evidence/WP-CA03-design-20261011.md)): triggers cover `push` and `pull_request` with no branch or path filter; the matrix covers Python 3.11 and 3.12; a `pytest -q` step runs the full suite. No deviation.

Result: design effective.

Operating test, automated regime ([WP-CA03-operating-20261011](evidence/WP-CA03-operating-20261011.md)):

1. Test of one: run 33065206756, the run on the scope-freeze commit, inspected end to end on both matrix legs from the run list, the step results and the full log archive (SHA-256 recorded before and after unpacking). Deviation: the run list, step results and logs were captured outside the testing environment. Deviation: the screenshot shows the test (3.12) job page with step 6 expanded, not the expanded run page for both legs; the 3.11 leg rests on the logs.
2. Configuration stability: `git log --follow -p` on the workflow file over the period, every change inspected for weakening.
3. Completeness: every push to `main` in the period reconciled against the run list (`gh run list --limit 100`, 10 runs returned, so not truncated). Deviation: the plan names no source for the push population, and the events feed no longer covered the period, so the population is the repository activity feed (11 records). Deviation: the reconciliation rule was fixed by B. Struve for the session. The unit is the push; a push whose "after" commit predates the workflow's introduction in `73fd4b0` expects no run; runs on tag refs are matched to the push whose "after" equals the tag's target; runs of any other workflow (one Dependency Graph run) are excluded and listed.
4. Reperformance deliberately not used: re-running CI proves the runner works today; it does not prove that the control operated during the period.

Result: operating effectively.

## CA-04 Packaged-data integrity check in CI (non-editable reinstall)

Criterion: ISO/IEC 27001:2022 A.8.32, corrected from SSDF PW.8 on 11 October 2026; the CI workflow's declared behaviour.

Design test, inspection of the workflow step ([WP-CA04-design-20261011](evidence/WP-CA04-design-20261011.md)): the step uninstalls the editable install, reinstalls with `pip install .`, and imports `aiact_triage.rules` and calls `timeline()` from `/tmp`, outside the checkout, so it tests the artefact a user receives, not the developer's source tree. No deviation.

Result: design effective.

Operating test ([WP-CA04-operating-20261011](evidence/WP-CA04-operating-20261011.md)): inspection of step 6's log inside CA-03's test-of-one run, both legs. Deviation: the logs were captured outside the testing environment, as for CA-03. Configuration stability rests on CA-03 step 2 by cross-reference, as the plan specifies, not on a duplicate capture.

Result: operating effectively.

## CA-05 Test suite covering the classification gates, with a regression file

Criterion: ISO/IEC 27001:2022 A.8.32, corrected from A.8.29 on 11 October 2026; the README's own test-count claim.

Design test, inspection of the test inventory ([WP-CA05-design-20261011](evidence/WP-CA05-design-20261011.md)):

1. `pytest --collect-only -q` in a clean venv after `pip install -e ".[dev]"`. Deviation: the venv was created in the session scratchpad, not `/tmp`.
2. Presence of the regression file, `tests/test_review_regressions.py`, as evidence that found errors become permanent cases.
3. Spot-read of three tests, one per gate the control objective names: Article 5, Article 6 (Annex III) and Article 50.

Result: design effective.

Operating test, automated half ([WP-CA05-operating-20261011](evidence/WP-CA05-operating-20261011.md)): the `pytest -q` step of CA-03's test-of-one run on both legs; configuration stability by cross-reference to CA-03. Deviation: this file covers the automated half only; the reperformance is in its own file.

Operating test, reperformance ([WP-CA05-operating-20261011-reperformance](evidence/WP-CA05-operating-20261011-reperformance.md)): fresh clone, fresh venv, `pip install -e ".[dev]"`, `pytest -q`, full output captured. Deviation: the venv was created in the session scratchpad, not as `.venv` in the clone. The local interpreter was Python 3.14.4, outside the CI matrix; the CI run covers 3.11 and 3.12. A test count differing from the README's claim would be recorded under CA-08, not here.

Result: operating effectively.

## CA-06 Zero-runtime-dependency policy

Criterion: the README's own zero-dependency claim (lines 15 and 80); SSDF PW.4 removed on 11 October 2026.

Design test, inspection of `pyproject.toml` and the README claim ([WP-CA06-design-20261011](evidence/WP-CA06-design-20261011.md)): `dependencies = []`, with pytest confined to the optional `dev` extra; README lines 15 and 80 state the policy. No deviation.

Result: design effective.

Operating test, automated half ([WP-CA06-operating-20261011](evidence/WP-CA06-operating-20261011.md)): what pip resolved and installed in steps 4 and 6 of CA-03's test-of-one run, both legs, which extends the proof across Python 3.11 and 3.12. Deviation: this file covers the automated half only; the reperformance is in its own file. Limitation stated in the workpaper: the CI environment at step 6 is not clean, because step 4 has already installed pytest and its dependencies, so the log was also searched for "Requirement already satisfied" (no hits).

Operating test, reperformance ([WP-CA06-operating-20261011-reperformance](evidence/WP-CA06-operating-20261011-reperformance.md)): empty venv, `pip freeze` before the install, `pip install .`, `pip freeze` and `pip show aiact-triage` after. Deviation: the venv was created in the session scratchpad, not `/tmp`. Deviation: a second venv, separate from CA-05's, because a venv already holding pytest could not show a clean freeze.

Result: operating effectively.

## CA-07 Rule-data citation and verification-date discipline

Criterion: the repository's own metadata convention (README line 105).

Design test, inspection of one rule-data file ([WP-CA07-design-20261011](evidence/WP-CA07-design-20261011.md)): `timeline.json`, the only file in which the metadata block, the verification-date field and a citation field on every rule can be inspected together. No deviation. Its statement that all nine timeline milestones carry a citation was corrected by the operating test: one names no provision.

Result: design effective.

Operating test, inspection of the full population ([WP-CA07-operating-20261011](evidence/WP-CA07-operating-20261011.md)):

1. Citation coverage across all six files, criterion 100%. Deviation: 47 rule entries exceed the 25 at which the sampling rule prescribes a sample; all 47 were tested. Deviation: `cross_framework.json` has no citation field, so provisions were sought in each rule's note text. Deviation: the citation tiers ("none", "grouping", "article-level") are a mechanical rule written for this test and printed in the workpaper.
2. Verification date. Deviation: per B. Struve's ruling of 11 October 2026, the plan's criterion "verification date in every file" misdescribes the repository's convention, so the test is against README line 105: the date is recorded in the timeline data and carried into every record the tool writes. Deviation: to test the second limb, register mode was run with the system Python in isolated mode, importing the package from the clone and writing into the session scratchpad; nothing was written to the clone.
3. Omnibus staleness: whether any rule file still cites the compromise text after Official Journal publication. Deviation: EUR-Lex was not checked from the testing environment; the check ran from the rule files' own sources, with the publication date taken from the 27 August 2026 pre-flight record.

Result: operating exception.

Remediation retest ([WP-CA07-remediation-20261011](evidence/WP-CA07-remediation-20261011.md)): step 1 rerun at `22ad85f` on the same 47 entries with the same helper script, extracted from the committed operating workpaper and confirmed byte-identical by SHA-256. Steps 2 and 3 were not retested, because their inputs are untouched: the data-directory diff between the two commits is one provision line. The retest checks that a citation is present at article level. It does not check that the citation names the right article.

Status: remediated during fieldwork.

## CA-08 Documentation accuracy (claims written after the code works)

Criterion: The README's own statements. Each status claim is tested against what the repository actually does. Corrected from "the repository's own convention" on 11 October 2026.

Design and operating test in one, inspection ([WP-CA08-operating-20261011](evidence/WP-CA08-operating-20261011.md)). For an ad hoc manual control the two collapse into one test, run after the CA-05 and CA-06 reperformances per B. Struve's ruling of 11 October 2026.

1. Every factual status claim in the README, identified under the selection rule stated in the workpaper, verified against the state established by CA-05, CA-06, CA-07 and the tree. Deviation: 37 claims exceed the 25 at which the sampling rule prescribes a sample; all 37 were tested.
2. The install block (README lines 83 to 88) run exactly as written. Deviation: run in the clone root, so its `.venv` sits inside the clone; generated files left by earlier runs were removed first. Deviation: `aiact-triage interactive` needs a terminal, which the testing environment lacks; it was run as written (stopping with `EOFError` at the first prompt) and again with a scripted answer set piped in, and the verdict rests on the piped run.
3. The README's example outputs compared line by line with real output. Deviation: the comparison helper treats a shown line ending in "..." as a prefix, because the README truncates those lines.
4. The claim that a moved date fails the suite, tested by mutation. Deviation: the mutation ran on a scratchpad copy of the clone with its own venv; the object under test was not modified.
5. Claims about the Official Journal text. Deviation: the Official Journal was not consulted, so those claims are verified only as far as the tree shows.

Result: operating exception. Design: not applicable, one test covers both.

Remediation retest ([WP-CA08-remediation-20261011](evidence/WP-CA08-remediation-20261011.md)): the claims behind the three conditions in Finding 3, at `22ad85f`. Claims 6 and 23 and the questionnaire's line 3 re-inspected against the questionnaire; claim 24 confirmed unchanged (`register.py` blob identical at both commits); the install block executed line by line from the README's own text (`eval "$(sed -n Np README.md)"`). Deviation: the install block ran in a second fresh clone and venv in the scratchpad, not the clone root. Deviation: `aiact-triage interactive` ran only as written, with stdin closed; the piped run was not repeated, because claim 16 was verified originally and its line is unchanged. Deviation: claims outside the three conditions were not retested; the README diff touches lines 17, 86, 87 and 101 only. Deviation: the Official Journal was not consulted.

Status: claims 6, 17, 18 and 23 remediated during fieldwork; claim 24 open; claim 25 under CA-07.

## CA-09 Release versioning discipline

Criterion: SSDF PS.3, task PS.3.1, corrected from PS.2 on 11 October 2026.

Design test, inspection for a documented versioning convention ([WP-CA09-design-20261011](evidence/WP-CA09-design-20261011.md)): the whole tracked tree searched for any versioning or tagging rule (none found), and the places that record the version listed (`pyproject.toml`, `src/aiact_triage/__init__.py`, one CHANGELOG heading per release). Deviation: per B. Struve's ruling of 11 October 2026, the documented convention was inspected in the maintainer's execution plan (rule D5 and its "Version arc" paragraph), which sits outside the published tree.

Result: design effective.

Operating test, full population ([WP-CA09-operating-20261011](evidence/WP-CA09-operating-20261011.md)): all 5 tags, each reconciled against the version in `pyproject.toml` and `__init__.py` at its target, the CHANGELOG heading at its target, the tag type, and the files the release commit changed, checked against the documented convention. No deviation.

Result: operating effectively.

## CA-10 Independent review of changes (segregation of duties)

Criterion: ISO/IEC 27001:2022 A.5.3; SSDF PW.7, task PW.7.2; corrected from A.8.32 and SSDF PW.8 on 11 October 2026.

Design test, inquiry plus inspection ([WP-CA10-design-20261011](evidence/WP-CA10-design-20261011.md)). Inquiry is legitimate here because the control's absence is a structural fact about a sole-maintainer repository that no configuration artefact can contradict, and the inquiry is of the maintainer, who is also the tester.

1. Contributor list. Deviation: taken from author and committer identities in the clone, because the GitHub API was not used from the testing environment.
2. Self-merged pull requests and any change reaching `main` other than by direct push. Deviation: pull-request history was evidenced from the activity feed and the CI run list captured outside the testing environment, not from the pull-requests API.
3. Any file or setting that requires review: CODEOWNERS, pull-request template, contributing guide, branch protection, rulesets.
4. Inquiry. Deviation: evidenced by the maintainer's written statement in the programme plan ("Owner throughout: B. Struve, sole maintainer"); no separate oral inquiry took place.

Result: design deficiency, with compensating controls CA-03, CA-04 and CA-05 graded partial.

Operating test: not performed, because the control does not exist to operate.

Result: not applicable.
