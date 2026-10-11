# Findings memo: control testing over the eu-ai-act-triage repository

As at 11 October 2026. Published 11 October 2026.

## 1. Purpose and intended readers

This memo reports the results of a control-testing programme over the development controls of the eu-ai-act-triage repository. It is written for reviewers of this repository, including prospective employers assessing control-testing capability. It is not for reliance; the restriction at the end of this document applies to every conclusion in it.

The programme was also an exercise in running several AI agents, each with a defined task, under one person's direction and checks. The author is new to control testing, and building this programme was part of learning it.

## 2. Scope, subject matter and period

The subject matter is the ten controls identified in [`control_matrix.md`](control_matrix.md), CA-01 to CA-10, covering version control, change management, continuous integration, the test suite, dependency policy, legal rule-data discipline, documentation accuracy, release versioning and segregation of duties, as they existed in the public repository at 11 October 2026.

Every test that needed the repository's tree ran against a fresh clone of `https://github.com/beestru/eu-ai-act-triage` with `main` at `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`, the commit at which scope froze on fieldwork day one: 45 commits and five release tags, `v0.1.0` to `v0.5.0`. The tests of GitHub's settings and CI runs used GitHub's own records, captured on 11 October 2026, and the CA-09 design test also read the maintainer's execution plan, which is not in the repository. Three commits pushed later the same day fix conditions reported in section 8. They were retested only for those conditions, and no other commit followed them at the time of the retest.

The repository has been public since 16 July 2026; repository created 14 July 2026, a period of 89 days holding 9 completed CI runs of the tests workflow at the scope freeze, and one more on the remediation push of 11 October 2026. That history is too short to support a conclusion that controls operated over a period. This document therefore assesses design effectiveness as at 11 October 2026, with operating tests performed at a point in time within the fieldwork window. The distinction is the one between a SOC 2 Type I report, which addresses design at a point in time, and a Type II report, which addresses operation over a period: this pack is the former, and a period-based operating conclusion will only be supportable once more history exists.

Point-in-time testing was performed on 11 October 2026; all fieldwork in the window ran on that day.

## 3. Framing against ISAE 3000

This document is structured to follow the conventions of ISAE 3000 (Revised). It is not an assurance engagement under that standard, was not performed under ISQM 1, and does not claim to be either. It is a self-assessment presented in the form an assurance practitioner would recognise.

## 4. Independence

This test programme was designed and performed by the same person who built the system under test. No independent practitioner has reviewed the control design or reperformed the testing. The independence that assurance standards assume between practitioner and responsible party is absent here by construction. The value of this document is not third-party assurance; it is evidence of the practitioner's ability to design a test programme to a recognised standard's conventions, execute it honestly enough to report adverse findings about his own work, and state this limitation plainly rather than let the format imply an independence that does not exist.

## 5. Criteria

Controls were evaluated against two classes of criteria: the repository's own documented commitments (its README claims, the declared behaviour of its CI workflow, and its rule-data metadata convention), and generally accepted secure-development practice, an anchor per control: a named practice in NIST SSDF v1.1 or ISO/IEC 27001:2022 Annex A where one applies directly, or the repository's own documented convention where that is the honest criterion. No criterion is cited by analogy. The anchor for each control is stated in the control matrix and is not repeated here. After fieldwork, every anchor was checked against the text of NIST SP 800-218 and the titles of the ISO/IEC 27001:2022 Annex A controls; six did not name the activity their control performs. Five were replaced, and CA-06's was removed, leaving the README's own zero-dependency claim as its criterion. CA-08's criterion was restated as the README's own statements, each status claim tested against what the repository actually does, because the convention it first named is not written in the published tree. All seven corrections were made on 11 October 2026, and the matrix records each one. No test or result changed.

## 6. Approach

Each control was tested separately for design effectiveness (whether the control, as designed and implemented, would achieve its objective if operated as described; tested by inspection of configuration and documents) and operating effectiveness (whether it actually operated; tested against the population of events). Automated controls were tested by inspecting one instance end to end and evidencing that the controlling configuration was stable across the period from the configuration file's own version history, with a completeness reconciliation where the control's value depends on it; sampling repeated runs of an unchanged automated control adds volume, not evidence. Manual controls were tested against their full population where that population held 25 items or fewer, the more persuasive choice for populations this small, consistent with the logic of ISA 530. Each finding states its provenance: whether the condition was known when the programme was designed or was identified by the testing itself. The distinction is stated because a self-assessed programme that presented known conditions as discoveries would be staging its own results.

There are three departures from that pattern. CA-08 is an ad hoc manual control, for which design and operating effectiveness collapse into one test, so it was tested once for both. CA-02 and CA-10 had no operating test, because neither control exists to operate. Three manual populations held more than 25 items and were tested in full all the same: 45 commits (CA-01), 47 rule entries (CA-07) and 37 README status claims (CA-08). Conditions identified by testing and fixed inside the fieldwork window were retested in their own dated workpapers; the original result stands, and the remediation status is reported beside it.

Every test is evidenced by a dated workpaper in [`evidence/`](evidence/), dated on capture and committed on the day of capture to a local version-control log; the log is the author's own, is available on request, and no claim of tamper-evidence attaches to it. Before publication, the author re-ran every command himself, outside the testing environment, on 11 October 2026; the AI assistant described in the next paragraph compared the new output with each workpaper; the author reviewed that comparison (phase4-reperformance-20261011). Four steps were not reperformed as written. Two runs of the interactive mode at a real terminal, one for WP-CA08-operating-20261011 and one for WP-CA08-remediation-20261011, ran with no input attached and stopped at the first prompt; the workpapers' own runs of that mode, with input from `/dev/null` and with answers piped in, were reproduced. The two screenshotted pages, the branch settings page (WP-CA02-design-20261011) and the CI run page (WP-CA03-operating-20261011), were not re-opened.

An AI coding assistant, Claude Code, executed the test commands in the testing environment, wrote the workpapers from the captured output, drew first-pass conclusions and drafted this memo, with further AI agents checking facts and wording, all under the author's direction. It was never permitted to compose or edit command output. Where a command reshaped its own output (scratch paths shown as `<SCRATCH>`, escape bytes shown as `^[`), the reshaping is part of the recorded command. STATE.md, the programme's running record, is kept in the same local log. Every ruling recorded there was made by the author, several on the recommendation of a second AI model used as reviewer. Those recommendations were made in separate review sessions and are not part of this pack. The author captured the GitHub-side evidence (section 10) and, before publication, re-ran every command himself, as the previous paragraph states.

## 7. Results

| Control | Design effectiveness | Operating effectiveness | Workpapers |
|---|---|---|---|
| CA-01 Version control over all source, rule data and documentation | Design effective | Operating effectively | [WP-CA01-design-20261011](evidence/WP-CA01-design-20261011.md); [WP-CA01-operating-20261011](evidence/WP-CA01-operating-20261011.md) |
| CA-02 Protected main branch | Design deficiency | Not applicable | [WP-CA02-design-20261011](evidence/WP-CA02-design-20261011.md); [WP-CA02-operating-20261011](evidence/WP-CA02-operating-20261011.md) |
| CA-03 CI runs the full test suite on every push and pull request | Design effective | Operating effectively | [WP-CA03-design-20261011](evidence/WP-CA03-design-20261011.md); [WP-CA03-operating-20261011](evidence/WP-CA03-operating-20261011.md) |
| CA-04 Packaged-data integrity check in CI (non-editable reinstall) | Design effective | Operating effectively | [WP-CA04-design-20261011](evidence/WP-CA04-design-20261011.md); [WP-CA04-operating-20261011](evidence/WP-CA04-operating-20261011.md) |
| CA-05 Test suite covering the classification gates, with a regression file | Design effective | Operating effectively | [WP-CA05-design-20261011](evidence/WP-CA05-design-20261011.md); [WP-CA05-operating-20261011](evidence/WP-CA05-operating-20261011.md); [WP-CA05-operating-20261011-reperformance](evidence/WP-CA05-operating-20261011-reperformance.md) |
| CA-06 Zero-runtime-dependency policy | Design effective | Operating effectively | [WP-CA06-design-20261011](evidence/WP-CA06-design-20261011.md); [WP-CA06-operating-20261011](evidence/WP-CA06-operating-20261011.md); [WP-CA06-operating-20261011-reperformance](evidence/WP-CA06-operating-20261011-reperformance.md) |
| CA-07 Rule-data citation and verification-date discipline | Design effective | Operating exception | [WP-CA07-design-20261011](evidence/WP-CA07-design-20261011.md); [WP-CA07-operating-20261011](evidence/WP-CA07-operating-20261011.md); retest [WP-CA07-remediation-20261011](evidence/WP-CA07-remediation-20261011.md) |
| CA-08 Documentation accuracy (claims written after the code works) | Not applicable: one test covers design and operation | Operating exception | [WP-CA08-operating-20261011](evidence/WP-CA08-operating-20261011.md); retest [WP-CA08-remediation-20261011](evidence/WP-CA08-remediation-20261011.md) |
| CA-09 Release versioning discipline | Design effective | Operating effectively | [WP-CA09-design-20261011](evidence/WP-CA09-design-20261011.md); [WP-CA09-operating-20261011](evidence/WP-CA09-operating-20261011.md) |
| CA-10 Independent review of changes (segregation of duties) | Design deficiency | Not applicable | [WP-CA10-design-20261011](evidence/WP-CA10-design-20261011.md) |

The CA-07 and CA-08 results are those at the scope-freeze commit. Their remediation statuses are given with Findings 3 and 4.

## 8. Findings

### Finding 1: no review of changes by anyone other than the author (CA-10)

**Condition.** All 45 commits on `main` carry one account address, and every change reached `main` by direct push from that account, with no pull request, no merge, no recorded approval by anyone else and no configuration requiring review (WP-CA10-design-20261011). Review by a second person has not operated on any change in the period. The test suite does record a pre-release review whose demands became the regression file (WP-CA05-design-20261011). That review was carried out by the author working with an AI model as hostile reviewer. It is recorded here because it is the nearest thing to independent challenge the repository has had, but it is not review by a second person: the author chose what it reviewed and which of its demands to accept.

**Criteria.** ISO/IEC 27001:2022 A.5.3, segregation of duties, and NIST SSDF PW.7, whose task PW.7.2 calls for code review and gives peer review of code as its first example. Assessment: an author approving their own change combines the duties that segregation exists to keep apart.

**Cause.** Sole-maintainer repository. No second contributor exists.

**Effect.** The automated detective controls (CA-03, CA-04, CA-05) share a single mind with the code they test: the tests encode the author's understanding of the EU AI Act, and so does the engine. An error of legal interpretation, a rule encoded wrongly but consistently with the author's misreading, passes every automated gate, because the gate was built from the same misreading. Assessment: this is the error a second reviewer exists to catch, and in a tool that classifies under the law it is the one that matters most. The same concentration extends to the evidence in this pack: the version-control history used to demonstrate configuration stability is kept by the person under test, so the evidence trail inherits the limitation, anchored externally only by the repository's GitHub creation date, GitHub's own push and workflow-run records, and the stability of published tag targets.

**Compensating controls, graded.** CI on every push since the workflow's introduction on 15 July 2026 (CA-03), the regression suite (CA-05) and the packaged-data check (CA-04) operate and were tested. They compensate partially: they detect deviations from the author's intent, not defects in the intent itself.

**Provenance.** Known at programme design. The condition is structural to a sole-maintainer repository and required no testing to identify.

**Status.** Open and structural until a second reviewer exists.

### Finding 2: main branch unprotected (CA-02)

**Condition.** No branch protection was configured on `main` at 11 October 2026. Commits could be pushed directly without the CI checks passing. GitHub's branch-protection endpoint returned "Branch not protected" (HTTP 404), the settings page stated that classic branch protections had not been configured, and the rulesets and branch-rules endpoints returned empty lists (WP-CA02-design-20261011, with WP-CA02-design-20261011-rulesets.txt). The route was used. Every change in the period reached `main` by direct push (WP-CA10-design-20261011). The scope-freeze commit, `7aab9f9`, is an edit made in the GitHub web interface directly on `main` (WP-CA01-operating-20261011). The fixes for Findings 3 and 4 went the same way on 11 October 2026: three commits in one direct push, with no pull request, and CI running after the push, not before it (WP-CA08-remediation-20261011).

**Criteria.** NIST SSDF PS.1 asks that code be protected from unauthorised changes, inadvertent as well as intentional, and ISO/IEC 27001:2022 A.8.32, change management, that changes pass through a defined procedure. On GitHub, the configuration that enforces both on `main` is branch protection; without it, both rest on the maintainer's discipline.

**Cause.** No branch protection was configured at the declaration of 16 July 2026 or when tested at fieldwork on 11 October 2026 (WP-CA02-design-20261011).

**Effect.** The CI gate (CA-03) is advisory rather than preventive: a commit with failing tests can reach `main`, and nothing but the author's habit prevents it. Required status checks work without a second reviewer, so a sole maintainer could have configured them.

**Provenance.** Known at declaration (16 July 2026), confirmed by testing at fieldwork.

**Status.** Known at declaration (16 July 2026); open.

### Finding 3: README claims that did not match the repository (CA-08)

**Condition.** Of 37 factual status claims in the README tested at the scope-freeze commit, 6 did not match what the repository does, from four distinct conditions (WP-CA08-operating-20261011). The lead condition is still open. README line 105 states that "All legal content sits in `src/aiact_triage/data/*.json`", but `register.py` lines 259 and 260 hard-code a legal statement into the register summary the tool prints: that the amended dates are the binding law, and that Regulation (EU) 2026/1744 has been in force since 27 July 2026 (claim 24). The same test found two further conditions. Question 30 of the third-party due-diligence questionnaire named no framework anchor, while the README said every question carries one (claims 6 and 23). Two commands in the README's install block, `aiact-triage assess case.json` and the register command reading `inventory.csv`, stopped with `FileNotFoundError` when run as written, because both files exist only under `examples/` (claims 17 and 18). The fourth condition, a rule that named no provision, is Finding 4 seen from the README (claim 25).

**Criteria.** The README's own statements. Each status claim is tested against what the repository actually does.

**Cause.** CA-08 is a manual control that operates when the README changes. Nothing in it runs when code or templates change, and no CI step runs the README's own commands (WP-CA03-design-20261011). Each condition is a general statement in the README that one part of the repository did not meet: one legal statement in code, one question without an anchor, two commands pointing at the repository root.

**Effect.** A legal statement held in code sits outside the verification discipline applied to the data files (CA-07), so a change in the legal position could be made in the data and leave the printed summary saying something else. A first-time reader following the install block as written hit a traceback on two of its six lines. Assessment: each condition is small. Together they matter, because readers judge the large claims by the small ones.

**Provenance.** Identified by testing at fieldwork.

**Status.** Given per condition.

- Legal statement in code (claim 24): open. The fix is to move the statement into `timeline.json` and have `register.py` read it. That is a functional change needing its own tests and release, so it was not made inside the fieldwork window; at `22ad85f`, `register.py` is unchanged (WP-CA08-remediation-20261011).
- Questionnaire question 30 (claims 6 and 23): remediated during fieldwork. Commit `22ad85f` changed README lines 17 and 101, and the questionnaire's own line 3, to say that question 30 sets the toolkit's own review cadence and carries no framework anchor. On retest the claims match the questionnaire (WP-CA08-remediation-20261011).
- Install commands (claims 17 and 18): remediated during fieldwork. Commit `933144d` points both commands at `examples/`. Run as written from a fresh clone, both exit 0 (WP-CA08-remediation-20261011).

The two remediated conditions are reported even though fixed, because quietly correcting them would defeat the control being tested. The original operating exception stands as the result at the scope-freeze commit.

### Finding 4: a rule that named no provision (CA-07)

**Condition.** Of 47 rule entries across the six rule-data files, one named no provision at all at the scope-freeze commit: the timeline milestone `sandboxes`, whose provision field read "National AI regulatory sandboxes" (WP-CA07-operating-20261011). The verification-date and Omnibus staleness checks in the same test raised no operating exception.

**Criteria.** The repository's own convention, as README line 105 states it: "an article citation on every rule". Coverage criterion: 100%.

**Cause.** The convention is applied by hand when a rule is written. The test suite passed 38 of 38 with the uncited entry in place (WP-CA05-operating-20261011-reperformance), so no automated gate caught it.

**Effect.** A reader checking the sandboxes date against the Regulation had no provision to check it against, and the README's claim of a citation on every rule was untrue in one place (Finding 3).

**Provenance.** Identified by testing at fieldwork. The design test the same day recorded all nine timeline milestones as carrying a citation and missed that one named no provision; the operating test corrected the record (section 9).

**Status.** Remediated during fieldwork. Commit `b5cb97c` changed that one field to "Article 57(1) national AI regulatory sandboxes", leaving the dates, status and note unchanged. Retested at `22ad85f`, 0 of 47 entries lack a citation (WP-CA07-remediation-20261011); three still cite at chapter or Annex A level, not a named article (section 9). The retest checks that an article-level citation is present. It does not check that Article 57(1) is the right article, a legal question this criterion does not reach. The original operating exception stands as the result at the scope-freeze commit.

## 9. Observations

Recorded in the workpapers and classified as observations, not operating exceptions. None changes a result in section 7.

About the repository:

- The CI workflow names its two actions by movable major-version tags (`actions/checkout@v7`, `actions/setup-python@v6`), not commit SHAs, so an unchanged workflow file does not by itself fix the action code that runs (WP-CA03-operating-20261011).
- The versioning convention, one release commit carrying both version-string bumps and the changelog entry under an annotated `vX.Y.0` tag, is written in the maintainer's execution plan, which is not in the published tree. A reader can see the practice in the tags and the changelog, but not the rule (WP-CA09-design-20261011).
- Three rule entries cite at chapter or Annex level, not a named article: two timeline milestones at Chapter III, because Article 113, third paragraph, point (c), as replaced by Regulation (EU) 2026/1744, sets those application dates for Chapter III, Sections 1, 2 and 3, and the ISO/IEC 42001 cross-framework flag at Annex A, which the file's own metadata discloses as deliberate pending verification against the standard (WP-CA07-operating-20261011, WP-CA07-remediation-20261011). For these three, the README's "an article citation on every rule" holds only at chapter or annex level.
- Six questionnaire questions (19 to 22, 28 and 29) carry their framework anchor inside the question text, not under "Anchors:" (WP-CA08-operating-20261011).
- Noted after the remediation retest, outside the claims tested: the questionnaire's line 5 list of framework anchors omits GDPR, which questions 10 and 11 cite under "Anchors:" (WP-CA08-remediation-20261011). It was not tested and is not remediated.
- One of the 45 commits, `7aab9f9`, carries the account login `BeeStru` as its author name where the other 44 carry `Bastian Struve`; it was made in the GitHub web interface. All 45 share one account address, which matches the single account behind every push, so author identity was classified as consistent. The web-interface route onto `main` is open because of Finding 2 (WP-CA01-operating-20261011).
- `aiact-triage interactive` ends in an `EOFError` traceback when its input closes without a terminal. With answers piped in, it completes, and the README makes no claim about the no-terminal case (WP-CA08-operating-20261011).

About the testing:

- The message of commit `a30bc34` says the new action versions run on the Node 24 runtime. That could not be checked from the testing environment, and the CA-03 conclusion does not depend on it (WP-CA03-operating-20261011).
- The local reperformances ran on Python 3.14.4, which the package's `requires-python >=3.11` admits but which lies outside the CI matrix of 3.11 and 3.12; the CI run covers those two (WP-CA05-operating-20261011-reperformance, WP-CA06-design-20261011).
- WP-CA07-design-20261011 recorded all nine timeline milestones as carrying a citation. One named no provision. The design conclusion stands, and the correction is recorded in WP-CA07-operating-20261011, because a committed workpaper is never edited.

## 10. Limitations

- The tester is the maintainer. Every test was designed, run and concluded by the person who built the repository. Section 4 states what that removes, and Finding 1 states what it does to the evidence.
- Claude Code executed and drafted; the author ruled. The AI coding assistant (section 6) executed the test commands, wrote the workpapers from captured output, drew first-pass conclusions and drafted this memo, with further AI agents checking facts and wording, all under the author's direction. It was never permitted to compose or edit command output. Every ruling recorded in STATE.md was made by the author, several on the recommendation of a second AI model used as reviewer. Those recommendations were made in separate review sessions and are not part of this pack. The author captured the GitHub-side evidence. Before publication he re-ran every command himself, outside the testing environment, on 11 October 2026; the AI assistant compared the new output with each workpaper; the author reviewed that comparison. Four steps were not reperformed as written; section 6 names them.
- Commit timestamps are author-set, so git dates prove nothing on their own. The external anchors are the repository's GitHub creation date, 14 July 2026, and GitHub's own push and workflow-run records. The first commit is dated 12 July 2026, two days before the creation date (WP-CA01-operating-20261011), consistent with the repository having been deleted and re-created on GitHub during 13 to 14 July, as recorded at the declaration of 16 July 2026. The flip to public on 16 July 2026 rests on the author's own declaration.
- GitHub-side evidence was captured by the maintainer outside the testing environment. That environment had no authenticated GitHub CLI (`gh` exited 4, asking for `gh auth login`), and the GitHub API was not used from it, so every GitHub-side item (the branch-protection and ruleset responses, both screenshots, the activity feeds, the run lists, the run logs and the step results) was captured by the maintainer on 11 October 2026 outside it, with the capture commands recorded beside the files (WP-CA03-operating-20261011-capture-commands.txt, WP-CA08-remediation-20261011-capture-commands.txt). Those files rest on the same person as the rest of this pack.
- The events feed was out of retention. GitHub's repository events feed returned no records on 11 October 2026. GitHub documents the feed as covering only the past 30 days (docs.github.com/en/rest/activity/events, read 11 October 2026), and the period's last push, on 27 August, was 45 days earlier. The push population for CA-01 and CA-03 was therefore taken from the repository activity feed, 11 records: 10 pushes and the branch creation (WP-CA03-operating-20261011). The test plan named no source for that population.
- The first fieldwork window broke and was restarted. Fieldwork opened on 27 August 2026; one session ran, and the seven-day window closed on 2 September with two sessions unrun. The window was restarted as a whole on 11 October 2026 with a fresh clone and a new scope freeze, and all testing cited in this memo ran on that day. The 27 August design workpapers are superseded, kept unedited in [`evidence/superseded/`](evidence/superseded/), and not cited elsewhere in this memo.
- Changes after the scope freeze were tested narrowly. The three remediation commits were the only changes to `main` after `7aab9f9` at the time of the retest, and each was retested for the condition it addresses and nothing else (WP-CA07-remediation-20261011, WP-CA08-remediation-20261011).
- The law itself was not checked. The Official Journal and EUR-Lex were not consulted during fieldwork. The Omnibus staleness check rests on the rule files' own sources and on the publication date recorded at pre-flight (WP-CA07-operating-20261011), and claims about the Official Journal text are verified only as far as the repository shows (WP-CA08-operating-20261011). Whether each encoded rule and citation is legally correct is outside every test here, which is the class of error Finding 1 describes. The one reading of the law in this memo, Article 113 in section 9, was made from the Official Journal text when the memo was drafted, after fieldwork.
- Several populations are small: five tags (CA-09), seven pushes that expected a CI run (CA-03), and no pull requests at all, so the `pull_request` trigger was never exercised (WP-CA09-operating-20261011, WP-CA03-operating-20261011). Five matching tags show the convention followed five times, and no more than that.

## 11. Conclusion

At the scope-freeze commit on 11 October 2026, the testing supports design effectiveness for seven of the ten controls and operating effectiveness, at that point in time, for six of them. It supports no conclusion that any control operated over a period, and it does not test whether the encoded law is right. Two controls carry a design deficiency, no branch protection and no review by a second person, and two carry an operating exception, in the README's claims and in the rule data. Of the conditions behind those findings, three were remediated during fieldwork, and the two design deficiencies and the legal statement held in code remain open.

## 12. Restriction on use

Prepared as a demonstration of control-testing method over the author's own repository. Not to be relied upon as assurance over the repository or its outputs.
