# WP-CA08-remediation-20261011

**Control.** CA-08, documentation accuracy (claims written after the code works).

**Original result.** Operating exception (WP-CA08-operating-20261011,
committed e72ff47): 6 of 37 README status claims did not match observable
state, from four distinct conditions, which B. Struve's rulings of
11 October 2026 (STATE.md) name as follows. (a) The timeline milestone
`sandboxes` carried no article citation: claim 25, retested from the CA-07
side in WP-CA07-remediation-20261011 and not repeated here. (b) Question 30
of the questionnaire named no framework anchor: claims 6 and 23. (c) The
install-block commands `aiact-triage assess case.json` and `aiact-triage
register inventory.csv --out audit` failed as written: claims 17 and 18.
(d) `register.py` line 259 holds a legal statement in code: claim 24. The
remediation ruling of the same day puts (a), (b) and (c) through the
repository's normal gates inside the window and leaves (d) open. The
original result stands unedited; this workpaper records the retests only.

**Remediation commits.**
- (b): `22ad85f3276040aceec29bff4eba34caacdd1d53`, "State that question 30 of
  the questionnaire carries no framework anchor". Files: `README.md` lines 17
  and 101, the text of claims 6 and 23; and
  `templates/third_party_ai_due_diligence.md` line 3, the questionnaire's own
  statement of the same claim. The commit also adds GDPR to the README's list
  of anchor frameworks in line 17 (its message gives the reason, questions 10
  and 11). That addition sits inside claim 6, so it is tested below.
- (c): `933144d18e4521406c33ab29b06deab778ab9cd3`, "Point the install block's
  assess and register lines at the examples". Files: `README.md` lines 86
  and 87 only.
- (d): no remediation commit. `register.py` is unchanged.

All three remediation commits (these two and CA-07's `b5cb97c`) reached
`main` in one push, `7aab9f9` to `22ad85f`, at 2026-10-11T12:42:50Z. It is
the only activity record after the scope-freeze push. One CI run followed
for that push head: run 38140312149, workflow "tests", event push, on
`main` at `22ad85f`, conclusion success. On both matrix legs, steps 5
(`pytest -q`) and 6 (packaged-data check) succeeded, and no step on either
leg failed. Sources: the committed captures
WP-CA08-remediation-20261011-runs.json,
WP-CA08-remediation-20261011-run-38140312149-steps.tsv and
WP-CA08-remediation-20261011-activity.jsonl (b751bcb), captured outside the
sandbox by B. Struve with the commands in
WP-CA08-remediation-20261011-capture-commands.txt, and read out in this
session as Part 3 below.

**Test method and reason.** Inspection, the same method as
WP-CA08-operating-20261011, applied to the claims behind each remediated or
open condition, because a retest asks whether the condition that failed has
been cleared. The criterion is unchanged: the repository's own convention
that README claims describe what the repository actually does.
- (b) Claims 6 and 23, and questionnaire line 3, against the questionnaire
  as it now stands. Same counts as the original Part 3 (numbered questions,
  "Evidence:", "Anchors:", and the questions without "Anchors:" listed). The
  inline-anchor reading is unchanged from the original: questions 19 to 22
  name OWASP LLM codes, 28 names Article 26(5) and 29 names SS1/23. The
  11 October ruling makes inline anchors an observation, not an exception.
  Added because the remediation added it: the GDPR anchors of questions 10
  and 11, and the "assertions" sentence of claim 23.
- (c) Claims 17 and 18: the README install block run exactly as written,
  from a fresh clone of the public repository and a fresh venv in the
  session scratchpad, per this session's instruction (the original ran in
  the `repo_under_test/` root, a deviation from the original's location
  only). Each line is executed as `eval "$(sed -n Np README.md)"`, so the
  shell runs the README's own text and not a retyped copy.
- (d) Claim 24: confirmation that `register.py` is unchanged and the
  condition is still present. The original Part 3 grep and `sed` are rerun,
  with the file's blob identity at both commits.

Deviations: (1) the install block ran in a scratchpad clone, as above.
(2) `aiact-triage interactive` (line 85, claim 16, not under retest) ran
only as written with stdin from `/dev/null`. It stopped at the first prompt
with `EOFError`, as in the original's as-written run, and the piped-answer
run was not repeated because claim 16 was verified originally and its line
is unchanged. (3) The Official Journal was not consulted. (4) Claims outside
the four conditions were not retested at `22ad85f`. Between `7aab9f9` and
`22ad85f`, the README diff touches lines 17, 86, 87 and 101 only (every
change a one-for-one line replacement, so line numbers hold). The rest of
the README text behind the other 31 claims is unchanged.

**Population and regime.** Manual regime. Population: the claims behind
conditions (b), (c) and (d), that is claims 6, 23, 17, 18 and 24 of
WP-CA08-operating-20261011, plus questionnaire line 3. All tested. Objects
under test: `repo_under_test/`, a fresh clone of the public repository at
2026-10-11 12:48:13 UTC, HEAD `22ad85f3276040aceec29bff4eba34caacdd1d53`
(`git ls-remote` confirming `main` there, 48 commits, tags v0.1.0 to
v0.5.0, `7aab9f9..22ad85f` exactly three commits with no merges, nothing
after `22ad85f`), for (b) and (d); and `<SCRATCH>/ca08_install`, a second
fresh clone at the same HEAD, for (c).

**Procedure executed.** `<SCRATCH>` is the session scratchpad. Part 1, (b)
and (d), run from the pack directory, reproduced in full:
```
cd repo_under_test
Q=templates/third_party_ai_due_diligence.md
echo "=== git log -1 --format='%H'; git status --short | wc -l ==="; git log -1 --format='%H'; git status --short | wc -l
echo
echo "##### (b) CLAIMS 6 AND 23, QUESTIONNAIRE LINE 3, AGAINST THE QUESTIONNAIRE AS IT NOW STANDS #####"
echo "=== sed -n 17p README.md ==="; sed -n 17p README.md
echo "=== sed -n 101p README.md ==="; sed -n 101p README.md
echo "=== sed -n 3p $Q ==="; sed -n 3p $Q
echo "=== sed -n 5p $Q ==="; sed -n 5p $Q
echo "numbered questions: $(grep -c -E '^[0-9]+\. ' $Q)"
echo "questions with 'Evidence:': $(grep -E '^[0-9]+\. ' $Q | grep -c 'Evidence:')"
echo "questions with 'Anchors:': $(grep -E '^[0-9]+\. ' $Q | grep -c 'Anchors:')"
echo "--- questions without 'Anchors:', in full:"
grep -E '^[0-9]+\. ' $Q | grep -v 'Anchors:'
echo "--- questions naming GDPR (number, then the text from 'Anchors:'):"
grep -E '^[0-9]+\. ' $Q | grep 'GDPR' | sed -E 's/^([0-9]+)\. .*(Anchors:.*)$/\1. ... \2/' 
echo "--- lines with 'assertion':"; grep -n -i 'assertion' $Q | cut -c1-200
echo "--- verdict block:"; grep -n -E '^## Verdict|^Outcome' $Q | cut -c1-200
echo "=== git diff --stat 7aab9f9 22ad85f -- $Q README.md ==="; git diff --stat 7aab9f9 22ad85f -- $Q README.md
echo
echo "##### (d) CLAIM 24: register.py UNCHANGED, CONDITION STILL PRESENT #####"
echo "=== git log --oneline 7aab9f9..22ad85f -- src/aiact_triage/register.py ==="; git log --oneline 7aab9f9..22ad85f -- src/aiact_triage/register.py; echo "(end)"
echo "=== git rev-parse 7aab9f9:src/aiact_triage/register.py 22ad85f:src/aiact_triage/register.py ==="; git rev-parse 7aab9f9:src/aiact_triage/register.py 22ad85f:src/aiact_triage/register.py
echo "=== git diff --stat 7aab9f9 22ad85f -- src/aiact_triage/ ==="; git diff --stat 7aab9f9 22ad85f -- src/aiact_triage/
echo "=== sed -n 105p README.md | cut -d';' -f1 ==="; sed -n 105p README.md | cut -d';' -f1
echo "=== grep -n -E '2026/1744|in force|Official Journal' src/aiact_triage/*.py ==="; grep -n -E '2026/1744|in force|Official Journal' src/aiact_triage/*.py
echo "--- sed -n 255,261p src/aiact_triage/register.py"; sed -n 255,261p src/aiact_triage/register.py
```
Part 2, (c), run as `bash ca08_c_retest.sh <SCRATCH>`, reproduced in
full:
```
S=$1
C=$S/ca08_install
rm -rf $C
echo "=== git clone https://github.com/beestru/eu-ai-act-triage <SCRATCH>/ca08_install ==="
git clone -q https://github.com/beestru/eu-ai-act-triage $C 2>&1; echo "EXIT: $?"
cd $C
echo "=== git log -1 --format='%H'; git status --short | wc -l; ls -a ==="; git log -1 --format='%H'; git status --short | wc -l; ls -a | tr '\n' ' '; echo
echo "=== sed -n 82,89p README.md ==="; sed -n 82,89p README.md
echo "##### each line below is executed as eval \"\$(sed -n Np README.md)\", the README text itself #####"
echo "--- line 83: $(sed -n 83p README.md)"
eval "$(sed -n 83p README.md)"; echo "EXIT: $?"; echo "python: $(command -v python | sed "s|$S|<SCRATCH>|")"; python --version
echo "--- line 84: $(sed -n 84p README.md)"
eval "$(sed -n 84p README.md)" > $S/ca08_c_pip.txt 2>&1; echo "EXIT: $?"; tail -1 $S/ca08_c_pip.txt
echo "--- line 85: $(sed -n 85p README.md)   (stdin from /dev/null: no terminal in this session)"
eval "timeout 20 $(sed -n 85p README.md)" < /dev/null 2>&1 | tail -3 | sed "s|$S|<SCRATCH>|g"; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- line 86: $(sed -n 86p README.md)"
eval "$(sed -n 86p README.md)" > $S/ca08_c_assess.txt 2>&1; echo "EXIT: $?"; cat $S/ca08_c_assess.txt
echo "--- line 87: $(sed -n 87p README.md)"
eval "$(sed -n 87p README.md)" > $S/ca08_c_register.txt 2>&1; echo "EXIT: $?"; head -3 $S/ca08_c_register.txt
echo "--- ls audit"; ls audit
echo "--- line 88: $(sed -n 88p README.md)"
eval "$(sed -n 88p README.md)" 2>&1 | tail -1; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- git status --short (after the block)"; git status --short; echo "(end)"
deactivate
```
Part 3, the committed CI and activity captures, run from the pack
directory, reproduced in full:
```
E=evidence
echo "=== git log --format='%h %ci %s' -1 -- \$E/WP-CA08-remediation-20261011-runs.json ==="; git log --format='%h %ci %s' -1 -- $E/WP-CA08-remediation-20261011-runs.json
echo "=== runs.json: runs whose headSha is 22ad85f, and run count ==="
python3 -I -c '
import json, sys
r = json.load(open(sys.argv[1]))
print("runs listed:", len(r))
for x in r:
    if x["headSha"].startswith("22ad85f"):
        print(x["databaseId"], x["workflowName"], x["event"], x["headBranch"], x["headSha"], x["status"], x["conclusion"], x["createdAt"])
' $E/WP-CA08-remediation-20261011-runs.json
echo "=== steps.tsv for run 38140312149: steps 5 and 6, and any step not success ==="
awk -F'\t' '$2==5 || $2==6' $E/WP-CA08-remediation-20261011-run-38140312149-steps.tsv
echo "steps not success: $(awk -F'\t' '$4!="success"' $E/WP-CA08-remediation-20261011-run-38140312149-steps.tsv | wc -l)"
echo "=== activity.jsonl: records, and records after 2026-08-27T10:56:45Z ==="
python3 -I -c '
import json, sys
recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
print("records:", len(recs))
for d in recs:
    if d["timestamp"] > "2026-08-27T10:56:45Z":
        print(d["timestamp"], d["activity_type"], d["ref"], d["before"], "->", d["after"])
' $E/WP-CA08-remediation-20261011-activity.jsonl
```

**Evidence.**

Part 1, (b) and (d):
```
=== git log -1 --format='%H'; git status --short | wc -l ===
22ad85f3276040aceec29bff4eba34caacdd1d53
0

##### (b) CLAIMS 6 AND 23, QUESTIONNAIRE LINE 3, AGAINST THE QUESTIONNAIRE AS IT NOW STANDS #####
=== sed -n 17p README.md ===
- **Third-party AI due-diligence questionnaire** (`templates/third_party_ai_due_diligence.md`). Complete. Thirty questions for assessing a vendor-supplied AI system. Twenty-nine carry the framework anchor they evidence (ISO/IEC 42001 Annex A, DORA Articles 28 to 30, the AI Act, GDPR, PRA SS1/23 or the OWASP LLM Top 10); the thirtieth, the re-diligence cycle, sets the toolkit's own review cadence and has no framework anchor.
=== sed -n 101p README.md ===
`templates/third_party_ai_due_diligence.md` assesses a vendor-supplied AI system before contract, at renewal, and on any material change. Run the classification first: the depth of diligence scales with the AI Act tier and, in a financial firm, the SS1/23 model tier, so a minimal-risk summariser is not interrogated like a high-risk credit model. Each of the thirty questions names the artefact to request. Each except question 30 also names the framework anchor it evidences. Answers without evidence are recorded as assertions. It closes with a proceed, proceed-with-conditions, or decline verdict attached to the system's inventory row and triage record.
=== sed -n 3p templates/third_party_ai_due_diligence.md ===
A structured questionnaire for assessing a vendor-supplied AI system before contract, at renewal, and on any material change to the system. Each question names the artefact to request. Each except question 30, the re-diligence cycle, also carries the framework anchor it evidences; question 30 sets the toolkit's own review cadence. It pairs with the triage tool: run the classification first, because the depth of diligence should scale with the AI Act tier and, in a financial firm, the SS1/23 model tier. A minimal-risk meeting summariser does not need the same interrogation as a high-risk credit model, and pretending otherwise produces diligence theatre rather than diligence.
=== sed -n 5p templates/third_party_ai_due_diligence.md ===
Framework anchors used below: ISO/IEC 42001:2023 Annex A (A.10.2 allocating responsibilities, A.10.3 suppliers, A.7 data for AI systems, A.8 information for interested parties); DORA (Regulation (EU) 2022/2554, Articles 28 to 30) where the deployer is a financial entity; the EU AI Act; PRA SS1/23 Principle 2.6 for firms in scope; OWASP LLM Top 10 (2025) for the security section where the system contains a language-model component.
numbered questions: 30
questions with 'Evidence:': 30
questions with 'Anchors:': 23
--- questions without 'Anchors:', in full:
19. Prompt-injection resistance (LLM01) and system-prompt leakage (LLM07): what defences exist against instructions embedded in user inputs or processed documents, whether the system prompt is treated as disclosable and kept free of secrets, and what the residual risk statement says. Evidence: security architecture note; test results.
20. Output handling (LLM05): supplier guidance on treating model outputs as untrusted, including schema validation and sanitisation before downstream use. Evidence: integration guidance.
21. Model supply chain (LLM03) and training-data poisoning controls (LLM04): provenance of base models and fine-tuning data, and integrity controls over them. Evidence: supply chain statement.
22. Abuse and consumption controls (LLM10): rate limiting, quota management, and cost-containment mechanics available to the deployer. Evidence: technical documentation.
28. Performance and drift reporting: what the supplier provides on an ongoing basis, at what cadence, and which metrics map to the deployer's Article 26(5) monitoring duty. Evidence: reporting specification.
29. Material-change triggers: the defined changes (model swap, retraining, purpose extension) that trigger renotification, re-triage under this toolkit, and where relevant re-validation under SS1/23. Evidence: change notification clause; internal re-triage procedure.
30. Re-diligence cycle: this questionnaire re-run at contract renewal and at least annually for high-risk systems, with deltas recorded against the prior version. Evidence: completed prior questionnaires on file.
--- questions naming GDPR (number, then the text from 'Anchors:'):
10. ... Anchors: ISO A.7; UK/EU GDPR.
11. ... Anchors: GDPR Arts. 28, 44 et seq.
--- lines with 'assertion':
7:How to complete: one questionnaire per system, attached to the system's row in the AI inventory and its triage record. Answers without evidence are recorded as assertions, not answers. Close with th
--- verdict block:
64:## Verdict
66:Outcome (one of): proceed; proceed with conditions (list them, with owners and dates); decline. Rationale in three sentences or fewer, referencing the question numbers that drove the outcome. Attac
=== git diff --stat 7aab9f9 22ad85f -- templates/third_party_ai_due_diligence.md README.md ===
 README.md                                 | 8 ++++----
 templates/third_party_ai_due_diligence.md | 2 +-
 2 files changed, 5 insertions(+), 5 deletions(-)

##### (d) CLAIM 24: register.py UNCHANGED, CONDITION STILL PRESENT #####
=== git log --oneline 7aab9f9..22ad85f -- src/aiact_triage/register.py ===
(end)
=== git rev-parse 7aab9f9:src/aiact_triage/register.py 22ad85f:src/aiact_triage/register.py ===
2eb9ddfeff3906d53eadcd5e028eafb2a37b84fa
2eb9ddfeff3906d53eadcd5e028eafb2a37b84fa
=== git diff --stat 7aab9f9 22ad85f -- src/aiact_triage/ ===
 src/aiact_triage/data/timeline.json | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
=== sed -n 105p README.md | cut -d';' -f1 ===
All legal content sits in `src/aiact_triage/data/*.json`, separate from the engine, with an article citation on every rule and a metadata block recording sources
=== grep -n -E '2026/1744|in force|Official Journal' src/aiact_triage/*.py ===
src/aiact_triage/cli.py:10:binding law (Regulation (EU) 2026/1744, in force since 27 July 2026); the
src/aiact_triage/register.py:259:        "amended dates are the binding law (Regulation (EU) 2026/1744, in "
src/aiact_triage/rules.py:5:published in the Official Journal (Regulation (EU) 2026/1744, OJ L,
--- sed -n 255,261p src/aiact_triage/register.py
            lines.append(f"- {date}  {article}  ({_count(names)})")
    lines.append("")
    lines.append(
        "The calendar uses the Omnibus amended date where one exists. The "
        "amended dates are the binding law (Regulation (EU) 2026/1744, in "
        "force since 27 July 2026); each system's record shows both dates."
    )
```
Part 2, (c):
````
=== git clone https://github.com/beestru/eu-ai-act-triage <SCRATCH>/ca08_install ===
EXIT: 0
=== git log -1 --format='%H'; git status --short | wc -l; ls -a ===
22ad85f3276040aceec29bff4eba34caacdd1d53
0
. .. .git .github .gitignore CHANGELOG.md LICENSE README.md docs examples pyproject.toml src templates tests 
=== sed -n 82,89p README.md ===
```
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
aiact-triage interactive                 # walk the intake for one system
aiact-triage assess examples/cv_screening.json   # assess one saved case
aiact-triage register examples/inventory.csv --out audit   # assess a whole inventory
pytest                                   # worked classification cases
```
##### each line below is executed as eval "$(sed -n Np README.md)", the README text itself #####
--- line 83: python3 -m venv .venv && source .venv/bin/activate
EXIT: 0
python: <SCRATCH>/ca08_install/.venv/bin/python
Python 3.14.4
--- line 84: pip install -e ".[dev]"
EXIT: 0
Successfully installed aiact-triage-0.5.0 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
--- line 85: aiact-triage interactive                 # walk the intake for one system   (stdin from /dev/null: no terminal in this session)
    name = input("Name of the AI system or use case: ").strip() or "unnamed"
           ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
EXIT: 1
--- line 86: aiact-triage assess examples/cv_screening.json   # assess one saved case
EXIT: 0
Use case: CV screening tool for graduate recruitment
Role:     deployer
Tier:     HIGH-RISK (Article 6)

Findings:
  [Art. 6(2), Annex III, 4] High-risk: Employment, workers' management and access to self-employment
      Stand-alone Annex III use case. Area examples: Recruitment and selection (CV screening, targeted job ads, candidate evaluation), decisions affecting terms of work-related relationships including promotion and termination, task allocation based on behaviour or traits, monitoring and evaluation of performance and behaviour

Obligations and dates (original -> as amended by the Digital Omnibus):
  [Art. 26(1)] Take appropriate technical and organisational measures to use the system in accordance with its instructions for use
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(2)] Assign human oversight to natural persons with the necessary competence, training, authority and support
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(4)] To the extent the deployer controls input data, ensure it is relevant and sufficiently representative for the intended purpose
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(5)] Monitor operation per the instructions for use; inform the provider and authorities of risks or serious incidents and suspend use where indicated
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(6)] Keep automatically generated logs under the deployer's control for a period appropriate to the intended purpose, at least six months unless applicable Union or national law, in particular on the protection of personal data, provides otherwise
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(7)] Before putting a workplace high-risk system into service or using it, deployers who are employers inform workers' representatives and the affected workers
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 26(11)] Inform natural persons that they are subject to the use of a high-risk Annex III system that makes or assists decisions relating to them; for systems used for law enforcement purposes, Article 13 of Directive (EU) 2016/680 applies instead
      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
  [Art. 4] Take measures to support the development of AI literacy among staff and other persons dealing with AI systems on the organisation's behalf (Article 4 as replaced by Regulation (EU) 2026/1744, in force since 27 July 2026; the original text required measures to ensure, to their best extent, a sufficient level of AI literacy)
      applies from: 2025-02-02 -> unchanged  (in_application)

Notes:
  - Deployer becomes provider (Art. 25(1)) on any of: Putting your name or trademark on a high-risk system already on the market; Making a substantial modification to a high-risk system that keeps it high-risk; Modifying the intended purpose of a non-high-risk system so it becomes high-risk
  - Digital Omnibus on AI: adopted as Regulation (EU) 2026/1744 of 8 July 2026, published in the Official Journal on 24 July 2026 (OJ L, 24.7.2026) and in force since 27 July 2026 (third day after publication). The amended dates are the binding law; the original dates are kept for the record.
--- line 87: aiact-triage register examples/inventory.csv --out audit   # assess a whole inventory
EXIT: 0
Wrote 8 files to audit/
# AI register triage summary

--- ls audit
01-cv-screening-assistant.md
02-customer-support-chatbot.md
03-credit-scoring-model.md
04-marketing-copy-generator.md
05-meeting-transcription-and-summariser.md
06-exam-marking-consistency-checker.md
07-workplace-wellbeing-emotion-monitor-pilot.md
_summary.md
--- line 88: pytest                                   # worked classification cases
============================== 38 passed in 0.10s ==============================
EXIT: 0
--- git status --short (after the block)
(end)
````
Part 3, CI and activity captures:
```
=== git log --format='%h %ci %s' -1 -- $E/WP-CA08-remediation-20261011-runs.json ===
b751bcb 2026-10-11 13:47:07 +0100 Capture CI and activity evidence for the remediation push, 11 October 2026
=== runs.json: runs whose headSha is 22ad85f, and run count ===
runs listed: 11
38140312149 tests push main 22ad85f3276040aceec29bff4eba34caacdd1d53 completed success 2026-10-11T12:42:52Z
=== steps.tsv for run 38140312149: steps 5 and 6, and any step not success ===
test (3.12)	5	Run pytest -q	success
test (3.12)	6	prove non-editable install carries the rule data	success
test (3.11)	5	Run pytest -q	success
test (3.11)	6	prove non-editable install carries the rule data	success
steps not success: 0
=== activity.jsonl: records, and records after 2026-08-27T10:56:45Z ===
records: 12
2026-10-11T12:42:50Z push refs/heads/main 7aab9f95065f9cf69cbdefe5a9aed64c361386ce -> 22ad85f3276040aceec29bff4eba34caacdd1d53
```

Claims retested, each with its result.

| # | Line | Claim as it now stands | Evidence | Original result | Retest result |
|---|---|---|---|---|---|
| 6 | README 17 | Thirty questions; twenty-nine carry their framework anchor (ISO/IEC 42001 Annex A, DORA Articles 28 to 30, the AI Act, GDPR, PRA SS1/23 or the OWASP LLM Top 10); the thirtieth, the re-diligence cycle, has no framework anchor | Part 1: 30 numbered questions; 23 carry "Anchors:"; 19 to 22, 28 and 29 carry theirs inline (as read in the original), making 29; question 30, printed in full, names none; GDPR under "Anchors:" in questions 10 and 11 | Exception | Verified |
| 23 | README 101 | Each of the thirty questions names the artefact to request; each except question 30 also names its framework anchor; answers without evidence are recorded as assertions; closes with a three-way verdict | Part 1: "Evidence:" 30 of 30; anchors as claim 6; line 7 records unevidenced answers as assertions; verdict block at lines 64 and 66 with proceed, proceed with conditions, decline | Exception | Verified |
| Q3 | Questionnaire 3 | Each question names the artefact to request; each except question 30 also carries its framework anchor; question 30 sets the toolkit's own review cadence | Part 1: as claims 6 and 23 | Not tested separately (the original's claim 6 rested on it) | Verified |
| 17 | README 86 | `aiact-triage assess examples/cv_screening.json` assesses one saved case | Part 2: run as written, exit 0, full assessment printed (HIGH-RISK, Article 6) | Exception | Verified |
| 18 | README 87 | `aiact-triage register examples/inventory.csv --out audit` assesses a whole inventory | Part 2: run as written, exit 0, "Wrote 8 files to audit/", 7 records and `_summary.md` listed | Exception | Verified |
| 24 | README 105 | "All legal content sits in `src/aiact_triage/data/*.json`" | Part 1: no commit in `7aab9f9..22ad85f` touches `register.py`; blob `2eb9ddf...` identical at both commits; line 259 still holds the binding-law statement and the 27 July 2026 in-force date of Regulation (EU) 2026/1744; README line 105 still makes the claim | Exception | Exception, unchanged |

The rest of the block also ran clean in Part 2: lines 83 and 84 exit 0,
line 88 `pytest` 38 passed, and `git status --short` was empty after the
block.

Observations, not classified, for B. Struve:
1. The questionnaire's line 5, "Framework anchors used below", lists ISO/IEC
   42001, DORA, the AI Act, PRA SS1/23 and the OWASP LLM Top 10 but not
   GDPR. Questions 10 and 11 cite GDPR under "Anchors:", and README line 17
   now lists it. Line 5 is not a README claim and the remediation did not
   touch it.
2. The three remediation commits reached `main` by direct push, with no
   pull request (activity record `push`, `7aab9f9` to `22ad85f`). This is
   the route CA-02's condition leaves open. CI ran after the push, not
   before it. One push, one run, consistent with CA-03's reconciliation
   unit.

**Executed.** 2026-10-11: Part 1 at 13:49 BST, Part 2 at 13:50 BST, Part 3 at
13:51 BST.

**Conclusion.** Status, per condition: (b) remediated during fieldwork, claims 6 and 23 and questionnaire line 3 now match the questionnaire (commit `22ad85f`); (c) remediated during fieldwork, both install commands run as written with exit 0 (commit `933144d`); (d) open, `register.py` unchanged and claim 24 still an exception, the fix as ruled being to move the legal statement into `timeline.json` and have `register.py` read it, a functional change needing its own tests and release; (a), claim 25, as recorded in WP-CA07-remediation-20261011. The original operating exception in WP-CA08-operating-20261011 stands as the result at the scope-freeze commit.
