# WP-CA08-operating-20261011

**Control.** CA-08, documentation accuracy (claims written after the code works).

**Test method and reason.** Inspection, per PLAN.md section 4. For an ad hoc
manual control, design and operating effectiveness collapse into one test,
and this workpaper is that single test; the control matrix cites it in both
columns. Every factual status claim in the README is verified against the
state established by CA-05 and CA-06 (WP-CA05-operating-20261011,
WP-CA05-operating-20261011-reperformance, WP-CA06-operating-20261011,
WP-CA06-operating-20261011-reperformance), CA-07
(WP-CA07-operating-20261011) and the tree, including the install commands
run exactly as written. It runs after the CA-05 and CA-06 reperformances per
B. Struve's ruling 3 of 11 October 2026. Every claim is listed as verified or
exception; nothing is skipped and nothing in the repository is fixed.

Selection rule for "factual status claim": a statement about the
repository's own contents, state or behaviour that observation could
falsify. Excluded, with reasons: lines 7 and 9 (argument about the problem,
not about the repository); the purpose sentences of line 66 and the
rationale sentences of line 70 (why, not what); the usage guidance in
line 101 ("Run the classification first", the depth of diligence scaling
with tier); the legal analysis of Annex I Section B in line 111 (a reading
of the law, not a repository fact; whether it is right is a legal question
outside CA-08); "Not legal advice" (a disclaimer); and lines 13 and 20
(signposting).

Deviations, five here and one under population: (1) the install block was run exactly as written, in the
clone root, so its `.venv` sits inside the clone rather than the scratchpad;
generated files left by earlier runs (`.venv`, `audit`, the `egg-info`
directory, all gitignored) were removed first, as the script shows;
(2) `aiact-triage interactive` needs a terminal, which this session lacks:
run as written with stdin closed it stops with `EOFError` at the first
prompt, so it was also run with a scripted answer set piped in, and the
verdict on that line rests on the piped run; (3) the date-pinning claim was
tested by mutation on a local clone of `repo_under_test` in the scratchpad
(`<SCRATCH>/ca08_mut`), with a separate venv holding only pytest and the
package imported from the copy (`PYTHONPATH=src`, import path printed); the
object under test was not modified; (4) the Official Journal text was not
consulted (no outbound HTTP), so claims about it are verified only as far
as the tree shows, as stated per claim; (5) the comparison helper
`compare.py` checks that every line shown in a README example appears in
the real output, treating a shown line ending in "..." as a prefix.

**Population and regime.** Manual regime, full population: 37 factual status
claims identified in `README.md` at `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`
under the selection rule above. That is above the 25 at which PLAN.md
section 5 prescribes a sample; every claim was tested, as PLAN.md section 4
("Nothing skipped") and B. Struve's instruction for this session require, a
sixth deviation. Object under
test: fresh clone taken at 2026-10-11 11:59:55 UTC.

**Procedure executed.** Run from the pack directory. Comparison helper,
reproduced in full:
```
"""Check that each line shown in a README example block appears in actual output.
Usage: python3 -I compare.py README FIRST_LINE LAST_LINE OUTPUT_FILE...
A shown line ending in '...' is checked as a prefix (the README truncates it);
the '$ ' command line, code-fence lines, blank lines and lines that are only
'...' are skipped."""
import sys
readme, first, last, *outs = sys.argv[1:]
shown = open(readme).read().splitlines()[int(first) - 1:int(last)]
actual = "\n".join(open(o).read() for o in outs)
actual_lines = [l.rstrip() for l in actual.splitlines()]
missing = 0
for n, line in enumerate(shown, int(first)):
    s = line.rstrip()
    if not s or s.startswith("$ ") or s.startswith("```") or s.strip() == "...":
        continue
    if s.endswith("..."):
        ok = any(a.startswith(s[:-3]) for a in actual_lines) or s[:-3].strip() in actual
    else:
        ok = s in actual_lines or s.strip() in actual
    missing += not ok
    print(f"README:{n} {'FOUND  ' if ok else 'MISSING'} {s}")
print("missing lines:", missing)
```
Capture script, reproduced in full:
```
S=<SCRATCH>
R=repo_under_test
O=$S/ca08_out; rm -rf $O; mkdir -p $O
cd $R
echo "=== remove generated files left by earlier runs (.venv, audit, egg-info; all gitignored) ==="
rm -rf .venv audit src/aiact_triage.egg-info; ls -a | tr '\n' ' '; echo
echo "=== git log -1 --format='%H'; git status --short | wc -l ==="; git log -1 --format='%H'; git status --short | wc -l
echo
echo "##### PART 1: README 'Install and run' block, lines 83 to 88, run as written in the clone root #####"
echo "=== sed -n 82,89p README.md ==="; sed -n 82,89p README.md
echo "--- python3 -m venv .venv && source .venv/bin/activate"
python3 -m venv .venv && source .venv/bin/activate; echo "EXIT: $?"; python --version
echo "--- pip install -e \".[dev]\""
pip install -e ".[dev]" > $O/pip.txt 2>&1; echo "EXIT: $?"; tail -2 $O/pip.txt
echo "--- aiact-triage interactive   (stdin from /dev/null: no terminal in this session)"
timeout 20 aiact-triage interactive < /dev/null 2>&1 | tail -15; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- aiact-triage interactive, with a scripted answer set piped in: a name, default role, 'n' to the nine Article 5 questions, 'n' to Annex I, no Annex III area, 'n' to the nine Article 50 and context questions"
{ printf 'Interactive walk test\n\n'; for i in $(seq 9); do echo n; done; echo n; echo; for i in $(seq 9); do echo n; done; } | timeout 20 aiact-triage interactive 2>&1 | tail -12; echo "EXIT: ${PIPESTATUS[1]}"
echo "--- aiact-triage assess case.json"
aiact-triage assess case.json 2>&1 | tail -5; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- aiact-triage register inventory.csv --out audit"
aiact-triage register inventory.csv --out audit 2>&1 | tail -5; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- pytest"
pytest 2>&1 | tail -3; echo "EXIT: ${PIPESTATUS[0]}"
echo "--- ls case.json inventory.csv examples/"; ls case.json inventory.csv examples/ 2>&1
echo "--- git status --short (after the block)"; git status --short; echo "(end)"
echo
echo "##### PART 2: README example outputs, commands as shown at lines 29 and 46 #####"
echo "=== aiact-triage assess examples/cv_screening.json ==="
aiact-triage assess examples/cv_screening.json > $O/assess.txt 2>&1; echo "EXIT: $?"; cat $O/assess.txt
echo "=== aiact-triage register examples/inventory.csv --out audit --assessor \"B. Struve\" ==="
rm -rf audit
aiact-triage register examples/inventory.csv --out audit --assessor "B. Struve" > $O/register.txt 2>&1; echo "EXIT: $?"; cat $O/register.txt
echo "--- ls audit"; ls audit
echo "=== compare README 28-41 with the assess output ==="
python3 -I $S/scripts/compare.py README.md 28 41 $O/assess.txt
echo "=== compare README 45-64 with the register output and audit/_summary.md ==="
python3 -I $S/scripts/compare.py README.md 45 64 $O/register.txt audit/_summary.md
echo "=== README 66: fields in audit/01-cv-screening-assistant.md ==="
grep -n -E '^Assessed |^Assessor:|^## Answers as recorded|^\| Article \| Obligation \| Applies from \(original\) \| As amended' audit/01-cv-screening-assistant.md
echo "records with the header line 'Assessed ... with aiact-triage 0.5.0. Rule set last verified 2026-08-04.': $(grep -l 'with aiact-triage 0.5.0. Rule set last verified 2026-08-04.' audit/0*.md | wc -l) of $(ls audit/0*.md | wc -l)"
echo "records with an 'Answers as recorded' section: $(grep -l '^## Answers as recorded' audit/0*.md | wc -l) of $(ls audit/0*.md | wc -l)"
echo "records with 'Assessor: B. Struve.': $(grep -l '^Assessor: B. Struve.' audit/0*.md | wc -l) of $(ls audit/0*.md | wc -l)"
echo "records with the two-date obligations table header: $(grep -l '^| Article | Obligation | Applies from (original) | As amended (Omnibus) | Status |' audit/0*.md | wc -l) of $(ls audit/0*.md | wc -l)"
echo "=== README 70: legal status line on the assess output; amended dates in timeline.json ==="
grep -n -i -E 'Regulation \(EU\) 2026/1744|->' $O/assess.txt | head -5
python3 -I -c 'import json; m={x["id"]: (x["original_date"], x["amended_date"]) for x in json.load(open("src/aiact_triage/data/timeline.json"))["milestones"]}; [print(k, m[k]) for k in ("high_risk_annex_iii","high_risk_annex_i","transparency_marking")]'
echo
echo "##### PART 3: claims checked against the tree #####"
echo "=== README 16, 95: template and docs present; template through register mode; pass-through columns ==="
ls -la templates/ai_inventory_template.csv docs/INVENTORY.md
rm -rf $O/tpl; aiact-triage register templates/ai_inventory_template.csv --out $O/tpl > /dev/null 2>&1; echo "EXIT: $?"; ls $O/tpl
grep -n -E 'model_id|business_owner|model_tier|validation_status|known_limitations' $O/tpl/01-*.md | head -6
echo "=== README 17, 101: questionnaire ==="
Q=templates/third_party_ai_due_diligence.md
echo "numbered questions: $(grep -c -E '^[0-9]+\. ' $Q)"
echo "questions with 'Evidence:': $(grep -E '^[0-9]+\. ' $Q | grep -c 'Evidence:')"
echo "questions with 'Anchors:': $(grep -E '^[0-9]+\. ' $Q | grep -c 'Anchors:')"
echo "--- questions without 'Anchors:' (number and first 160 characters):"
grep -E '^[0-9]+\. ' $Q | grep -v 'Anchors:' | cut -c1-160
echo "--- verdict block:"; grep -n -E '^## Verdict|^Outcome' $Q | cut -c1-200
echo "=== README 18, 111: LLM intake assistant designed, not built ==="
ls -la docs/DESIGN_llm_component.md; ls src/aiact_triage/
grep -r -n -i -E 'anthropic|openai|llm' src/aiact_triage/ ; echo "EXIT: $?"
ls docs/model_card_intake_assistant.md 2>&1
echo "=== README 74: annex III areas; named behaviours ==="
python3 -I -c 'import json; print("annex_iii areas:", len(json.load(open("src/aiact_triage/data/annex_iii.json"))["areas"]))'
pytest -v -k "provider_side_note or social_scoring or derogation_blocked or high_risk_and_transparency_stack or fails_closed or consistency_warning or unknown_columns or json_register or cross_framework" 2>&1 | grep -E 'PASSED|FAILED|ERROR|passed|failed'
echo "=== README 97: cross-framework rules ==="
python3 -I -c 'import json; [print(r["id"], "|", r["framework"], "|", r["trigger"]) for r in json.load(open("src/aiact_triage/data/cross_framework.json"))["rules"]]'
echo "=== README 105: metadata blocks; dates unchanged across the Omnibus alignment (83d704c..f817735) ==="
python3 -I -c 'import json,glob; [print(f, "_meta" in json.load(open(f))) for f in sorted(glob.glob("src/aiact_triage/data/*.json"))]'
git diff 83d704c f817735 -- src/aiact_triage/data/ | grep -E '^[-+].*"(original_date|amended_date)"' ; echo "date lines changed: $(git diff 83d704c f817735 -- src/aiact_triage/data/ | grep -c -E '^[-+].*"(original_date|amended_date)"')"
git diff 83d704c f817735 --stat -- src/aiact_triage/data/
echo "=== README 105: legal statements in package code (outside data/*.json) ==="
grep -n -E '2026/1744|in force|Official Journal' src/aiact_triage/*.py
echo "--- sed -n 255,261p src/aiact_triage/register.py"; sed -n 255,261p src/aiact_triage/register.py
echo "--- sed -n 1,12p src/aiact_triage/cli.py"; sed -n 1,12p src/aiact_triage/cli.py
echo "--- sed -n 1,8p src/aiact_triage/rules.py"; sed -n 1,8p src/aiact_triage/rules.py
echo "=== README 107: no network or self-update code in the package ==="
grep -r -n -E 'urllib|requests|http\.client|socket|urlopen' src/aiact_triage/ ; echo "EXIT: $?"
echo "=== README 111: provider summary-level; GPAI not classified ==="
python3 -I -c 'import json; o=json.load(open("src/aiact_triage/data/obligations.json")); print("provider entries:", [k for k in o if "provider" in k])'
grep -n -i 'gpai\|general-purpose' src/aiact_triage/*.py ; echo "EXIT: $?"
grep -n -i 'annex_i_product\|section' src/aiact_triage/models.py
deactivate
echo
echo "##### PART 4: README 105, 'a moved date fails the suite', on a scratch copy #####"
rm -rf $S/ca08_mut $S/ca08m; cd /home/bastian/agents/work/control-assurance-pack
git clone -q --no-hardlinks $R $S/ca08_mut 2>&1
cd $S/ca08_mut
python3 -I -c 'import json; p="src/aiact_triage/data/timeline.json"; d=json.load(open(p)); m=[x for x in d["milestones"] if x["id"]=="high_risk_annex_iii"][0]; print("before:", m["amended_date"]); m["amended_date"]="2027-12-03"; json.dump(d, open(p,"w"), indent=2, ensure_ascii=False); print("after:", m["amended_date"])'
git diff --stat
python3 -m venv $S/ca08m && $S/ca08m/bin/pip install -q "pytest>=8" > /dev/null 2>&1; echo "venv EXIT: $?"
PYTHONPATH=src $S/ca08m/bin/python -c 'import aiact_triage, sys; print("imported from:", aiact_triage.__file__.replace(sys.argv[1], "<SCRATCH>"))' $S
PYTHONPATH=src $S/ca08m/bin/python -m pytest -q 2>&1 | tail -6
```

**Evidence.**
```
=== remove generated files left by earlier runs (.venv, audit, egg-info; all gitignored) ===
. .. .git .github .gitignore .pytest_cache CHANGELOG.md LICENSE README.md build docs examples pyproject.toml src templates tests 
=== git log -1 --format='%H'; git status --short | wc -l ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
0

##### PART 1: README 'Install and run' block, lines 83 to 88, run as written in the clone root #####
=== sed -n 82,89p README.md ===
```
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
aiact-triage interactive                 # walk the intake for one system
aiact-triage assess case.json            # assess one saved case
aiact-triage register inventory.csv --out audit   # assess a whole inventory
pytest                                   # worked classification cases
```
--- python3 -m venv .venv && source .venv/bin/activate
EXIT: 0
Python 3.14.4
--- pip install -e ".[dev]"
EXIT: 0

Successfully installed aiact-triage-0.5.0 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
--- aiact-triage interactive   (stdin from /dev/null: no terminal in this session)
Name of the AI system or use case: Traceback (most recent call last):
  File "/home/bastian/agents/work/control-assurance-pack/repo_under_test/.venv/bin/aiact-triage", line 8, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/bastian/agents/work/control-assurance-pack/repo_under_test/src/aiact_triage/cli.py", line 198, in main
    assessment = classify(build_case_interactively())
                          ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/bastian/agents/work/control-assurance-pack/repo_under_test/src/aiact_triage/cli.py", line 77, in build_case_interactively
    name = input("Name of the AI system or use case: ").strip() or "unnamed"
           ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError: EOF when reading a line
EXIT: 1
--- aiact-triage interactive, with a scripted answer set piped in: a name, default role, 'n' to the nine Article 5 questions, 'n' to Annex I, no Annex III area, 'n' to the nine Article 50 and context questions
Tier:     MINIMAL RISK

Findings:
  [Art. 6, Art. 50] Minimal risk
      No prohibited practice, no Annex I or Annex III listing, no Article 50 trigger recorded

Obligations and dates (original -> as amended by the Digital Omnibus):
  [Art. 4] Take measures to support the development of AI literacy among staff and other persons dealing with AI systems on the organisation's behalf (Article 4 as replaced by Regulation (EU) 2026/1744, in force since 27 July 2026; the original text required measures to ensure, to their best extent, a sufficient level of AI literacy)
      applies from: 2025-02-02 -> unchanged  (in_application)

Notes:
  - Digital Omnibus on AI: adopted as Regulation (EU) 2026/1744 of 8 July 2026, published in the Official Journal on 24 July 2026 (OJ L, 24.7.2026) and in force since 27 July 2026 (third day after publication). The amended dates are the binding law; the original dates are kept for the record.
EXIT: 0
--- aiact-triage assess case.json
                          ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/bastian/agents/work/control-assurance-pack/repo_under_test/src/aiact_triage/cli.py", line 152, in load_case
    with open(path, encoding="utf-8") as f:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'case.json'
EXIT: 1
--- aiact-triage register inventory.csv --out audit
    cases = load_register(args.register_file)
  File "/home/bastian/agents/work/control-assurance-pack/repo_under_test/src/aiact_triage/register.py", line 91, in load_register
    with open(path, encoding="utf-8", newline="") as f:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'inventory.csv'
EXIT: 1
--- pytest
tests/test_review_regressions.py .........                               [100%]

============================== 38 passed in 0.05s ==============================
EXIT: 0
--- ls case.json inventory.csv examples/
ls: cannot access 'case.json': No such file or directory
ls: cannot access 'inventory.csv': No such file or directory
examples/:
customer_chatbot_provider.json
cv_screening.json
inventory.csv
--- git status --short (after the block)
(end)

##### PART 2: README example outputs, commands as shown at lines 29 and 46 #####
=== aiact-triage assess examples/cv_screening.json ===
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
=== aiact-triage register examples/inventory.csv --out audit --assessor "B. Struve" ===
EXIT: 0
Wrote 8 files to audit/
# AI register triage summary

7 systems assessed 2026-10-11. Rule set last verified 2026-08-04.

Legal status of the amended dates: Digital Omnibus on AI: adopted as Regulation (EU) 2026/1744 of 8 July 2026, published in the Official Journal on 24 July 2026 (OJ L, 24.7.2026) and in force since 27 July 2026 (third day after publication). The amended dates are the binding law; the original dates are kept for the record.

## Systems by tier

- PROHIBITED (Article 5): 1
    - Workplace wellbeing emotion monitor (pilot)
- HIGH-RISK (Article 6): 2
    - CV screening assistant
    - Credit scoring model
- LIMITED RISK: transparency duties (Article 50): 0
- MINIMAL RISK: 4
    - Customer support chatbot
    - Marketing copy generator
    - Meeting transcription and summariser
    - Exam-marking consistency checker

## Attention items

- Credit scoring model: fundamental rights impact assessment (Art. 27) required before first use.
- Exam-marking consistency checker: relies on the Art. 6(3) derogation; the assessment must be documented and the system registered.
- Workplace wellbeing emotion monitor (pilot): prohibited practice recorded. Escalate; no compliance pathway exists.

## Deadline calendar

Already applying:
- 2025-02-02  Art. 4  (6 systems)
- 2025-02-02  Art. 5(1)(f)  (1 system)

Upcoming:
- 2027-12-02  Art. 26(1)  (2 systems)
- 2027-12-02  Art. 26(11)  (2 systems)
- 2027-12-02  Art. 26(2)  (2 systems)
- 2027-12-02  Art. 26(4)  (2 systems)
- 2027-12-02  Art. 26(5)  (2 systems)
- 2027-12-02  Art. 26(6)  (2 systems)
- 2027-12-02  Art. 26(7)  (1 system)
- 2027-12-02  Art. 27  (1 system)

The calendar uses the Omnibus amended date where one exists. The amended dates are the binding law (Regulation (EU) 2026/1744, in force since 27 July 2026); each system's record shows both dates.

--- ls audit
01-cv-screening-assistant.md
02-customer-support-chatbot.md
03-credit-scoring-model.md
04-marketing-copy-generator.md
05-meeting-transcription-and-summariser.md
06-exam-marking-consistency-checker.md
07-workplace-wellbeing-emotion-monitor-pilot.md
_summary.md
=== compare README 28-41 with the assess output ===
README:31 FOUND   Use case: CV screening tool for graduate recruitment
README:32 FOUND   Role:     deployer
README:33 FOUND   Tier:     HIGH-RISK (Article 6)
README:35 FOUND   Findings:
README:36 FOUND     [Art. 6(2), Annex III, 4] High-risk: Employment, workers' management...
README:38 FOUND   Obligations and dates (original -> as amended by the Digital Omnibus):
README:39 FOUND     [Art. 26(2)] Assign human oversight to natural persons with the necessary competence...
README:40 FOUND         applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
missing lines: 0
=== compare README 45-64 with the register output and audit/_summary.md ===
README:48 FOUND   ## Systems by tier
README:49 FOUND   - PROHIBITED (Article 5): 1
README:50 FOUND       - Workplace wellbeing emotion monitor (pilot)
README:51 FOUND   - HIGH-RISK (Article 6): 2
README:52 FOUND       - CV screening assistant
README:53 FOUND       - Credit scoring model
README:55 FOUND   ## Attention items
README:56 FOUND   - Credit scoring model: fundamental rights impact assessment (Art. 27) required before first use.
README:57 FOUND   - Exam-marking consistency checker: relies on the Art. 6(3) derogation; the
README:58 FOUND     assessment must be documented and the system registered.
README:59 FOUND   - Workplace wellbeing emotion monitor (pilot): prohibited practice recorded. Escalate; no compliance pathway exists.
README:61 FOUND   ## Deadline calendar
README:62 FOUND   Upcoming:
README:63 FOUND   - 2027-12-02  Art. 26(2)  (2 systems)
missing lines: 0
=== README 66: fields in audit/01-cv-screening-assistant.md ===
3:Assessed 2026-10-11 with aiact-triage 0.5.0. Rule set last verified 2026-08-04.
4:Assessor: B. Struve.
14:| Article | Obligation | Applies from (original) | As amended (Omnibus) | Status |
34:## Answers as recorded
records with the header line 'Assessed ... with aiact-triage 0.5.0. Rule set last verified 2026-08-04.': 7 of 7
records with an 'Answers as recorded' section: 7 of 7
records with 'Assessor: B. Struve.': 7 of 7
records with the two-date obligations table header: 7 of 7
=== README 70: legal status line on the assess output; amended dates in timeline.json ===
9:Obligations and dates (original -> as amended by the Digital Omnibus):
11:      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
13:      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
15:      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
17:      applies from: 2026-08-02 -> 2027-12-02  (postponed_by_omnibus)
high_risk_annex_iii ('2026-08-02', '2027-12-02')
high_risk_annex_i ('2027-08-02', '2028-08-02')
transparency_marking ('2026-08-02', '2026-12-02')

##### PART 3: claims checked against the tree #####
=== README 16, 95: template and docs present; template through register mode; pass-through columns ===
-rw-rw-r-- 1 bastian bastian 5372 Oct 11 12:59 docs/INVENTORY.md
-rw-rw-r-- 1 bastian bastian 1079 Oct 11 12:59 templates/ai_inventory_template.csv
EXIT: 0
01-retail-credit-scoring-model.md
_summary.md
49:- model_id (inventory field): MDL-0042
51:- business_owner (inventory field): Head of Retail Credit Risk
55:- model_tier (inventory field): Tier 1
59:- known_limitations (inventory field): Performance degrades on thin-file applicants; documented in validation report
60:- validation_status (inventory field): validated
=== README 17, 101: questionnaire ===
numbered questions: 30
questions with 'Evidence:': 30
questions with 'Anchors:': 23
--- questions without 'Anchors:' (number and first 160 characters):
19. Prompt-injection resistance (LLM01) and system-prompt leakage (LLM07): what defences exist against instructions embedded in user inputs or processed documen
20. Output handling (LLM05): supplier guidance on treating model outputs as untrusted, including schema validation and sanitisation before downstream use. Evide
21. Model supply chain (LLM03) and training-data poisoning controls (LLM04): provenance of base models and fine-tuning data, and integrity controls over them. E
22. Abuse and consumption controls (LLM10): rate limiting, quota management, and cost-containment mechanics available to the deployer. Evidence: technical docum
28. Performance and drift reporting: what the supplier provides on an ongoing basis, at what cadence, and which metrics map to the deployer's Article 26(5) moni
29. Material-change triggers: the defined changes (model swap, retraining, purpose extension) that trigger renotification, re-triage under this toolkit, and whe
30. Re-diligence cycle: this questionnaire re-run at contract renewal and at least annually for high-risk systems, with deltas recorded against the prior versio
--- verdict block:
64:## Verdict
66:Outcome (one of): proceed; proceed with conditions (list them, with owners and dates); decline. Rationale in three sentences or fewer, referencing the question numbers that drove the outcome. Attac
=== README 18, 111: LLM intake assistant designed, not built ===
-rw-rw-r-- 1 bastian bastian 8701 Oct 11 12:59 docs/DESIGN_llm_component.md
__init__.py
__main__.py
__pycache__
cli.py
data
engine.py
models.py
register.py
rules.py
EXIT: 1
ls: cannot access 'docs/model_card_intake_assistant.md': No such file or directory
=== README 74: annex III areas; named behaviours ===
annex_iii areas: 8
tests/test_cross_framework.py::test_fs_high_risk_gets_ss1_23_inventory_and_lifecycle_flags PASSED [  5%]
tests/test_cross_framework.py::test_fs_vendor_system_gets_dora_and_iso42001_flags PASSED [ 11%]
tests/test_cross_framework.py::test_non_fs_vendor_system_gets_iso42001_but_not_dora_or_ss1_23 PASSED [ 16%]
tests/test_cross_framework.py::test_emotion_recognition_outside_workplace_gets_gdpr_flag PASSED [ 22%]
tests/test_cross_framework.py::test_prohibited_system_gets_no_cross_framework_flags PASSED [ 27%]
tests/test_cross_framework.py::test_csv_no_in_context_fields_yields_no_cross_framework_flags PASSED [ 33%]
tests/test_cross_framework.py::test_inventory_template_runs_through_register_mode PASSED [ 38%]
tests/test_engine.py::test_customer_chatbot_is_limited_risk_with_provider_side_note PASSED [ 44%]
tests/test_engine.py::test_social_scoring_is_prohibited_and_terminal PASSED [ 50%]
tests/test_engine.py::test_art_6_3_derogation_blocked_by_profiling PASSED [ 55%]
tests/test_engine.py::test_unknown_prohibited_flag_fails_closed_to_high_risk PASSED [ 61%]
tests/test_engine.py::test_high_risk_and_transparency_stack PASSED       [ 66%]
tests/test_register.py::test_unknown_columns_flow_into_metadata PASSED   [ 72%]
tests/test_register.py::test_json_register_and_slug_edge_cases PASSED    [ 77%]
tests/test_review_regressions.py::test_unknown_annex_iii_area_fails_closed_to_high_risk_needs_review PASSED [ 83%]
tests/test_review_regressions.py::test_unknown_prohibited_flag_fails_closed_to_high_risk_needs_review PASSED [ 88%]
tests/test_review_regressions.py::test_emotion_at_work_without_art5_answer_gets_consistency_warning PASSED [ 94%]
tests/test_review_regressions.py::test_essential_services_profiling_without_fria_gets_consistency_warning PASSED [100%]
====================== 18 passed, 20 deselected in 0.04s =======================
=== README 97: cross-framework rules ===
ss1_23_inventory | PRA SS1/23 | {'all': ['financial_services_context']}
ss1_23_lifecycle_alignment | PRA SS1/23 | {'all': ['financial_services_context'], 'tier_in': ['high_risk']}
dora_third_party | DORA | {'all': ['financial_services_context', 'vendor_supplied']}
iso42001_supplier | ISO/IEC 42001 | {'all': ['vendor_supplied']}
gdpr_special_category | UK/EU GDPR | {'any': ['emotion_recognition', 'biometric_categorisation']}
=== README 105: metadata blocks; dates unchanged across the Omnibus alignment (83d704c..f817735) ===
src/aiact_triage/data/annex_iii.json True
src/aiact_triage/data/cross_framework.json True
src/aiact_triage/data/obligations.json True
src/aiact_triage/data/prohibitions.json True
src/aiact_triage/data/timeline.json True
src/aiact_triage/data/transparency.json True
date lines changed: 0
 src/aiact_triage/data/obligations.json  |  4 ++--
 src/aiact_triage/data/prohibitions.json | 10 +++++-----
 src/aiact_triage/data/timeline.json     | 19 +++++++++----------
 src/aiact_triage/data/transparency.json |  4 ++--
 4 files changed, 18 insertions(+), 19 deletions(-)
=== README 105: legal statements in package code (outside data/*.json) ===
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
--- sed -n 1,12p src/aiact_triage/cli.py
"""Command-line interface.

Two modes:

  aiact-triage assess case.json     Non-interactive: reads structured answers
  aiact-triage interactive          Walks the intake questionnaire

The report shows both the original AI Act dates and the Digital Omnibus
amended dates, with the legal status stated. The amended dates are the
binding law (Regulation (EU) 2026/1744, in force since 27 July 2026); the
original dates are kept for the record.
"""
--- sed -n 1,8p src/aiact_triage/rules.py
"""Loads the rule set from the data directory.

The rules live in JSON, not in code, for two reasons: the legal content can
be reviewed without reading Python, and when the Digital Omnibus was
published in the Official Journal (Regulation (EU) 2026/1744, OJ L,
24.7.2026) the alignment was made in the data files, in one place.
"""

=== README 107: no network or self-update code in the package ===
EXIT: 1
=== README 111: provider summary-level; GPAI not classified ===
provider entries: ['high_risk_provider_summary', 'deployer_becomes_provider']
EXIT: 1
42:    annex_i_product: bool = False  # safety component of / product under Annex I legislation

##### PART 4: README 105, 'a moved date fails the suite', on a scratch copy #####
before: 2027-12-02
after: 2027-12-03
 src/aiact_triage/data/timeline.json | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
venv EXIT: 0
imported from: <SCRATCH>/ca08_mut/src/aiact_triage/__init__.py
tests/test_register.py:84: AssertionError
=========================== short test summary info ============================
FAILED tests/test_engine.py::test_cv_screening_is_high_risk_annex_iii_employment
FAILED tests/test_register.py::test_audit_record_contains_citations_dates_and_inventory_fields
FAILED tests/test_register.py::test_summary_surfaces_attention_items_and_calendar
3 failed, 35 passed in 0.13s
```

Claims, each with its result.

| # | README line | Claim | Evidence | Result |
|---|---|---|---|---|
| 1 | 3 | The engine assesses a whole inventory in one pass and writes a dated audit record per system, with both dates | Part 2: one register run, 7 records and a summary, each record dated, two-date table in 7 of 7 | Verified |
| 2 | 15 | "Working and tested (38 tests" | 38 passed in the reperformance (WP-CA05-operating-20261011-reperformance), on both CI legs (WP-CA05-operating-20261011), and in Part 1 | Verified |
| 3 | 15, 80 | "no runtime dependencies" | Clean install pulls in nothing else, empty `Requires:` (WP-CA06-operating-20261011-reperformance); same on 3.11 and 3.12 (WP-CA06-operating-20261011) | Verified |
| 4 | 15 | Classifies one use case or a whole inventory and produces the audit records | Part 2: `assess` and `register` both exit 0 with output | Verified |
| 5 | 16 | Inventory template complete, one file that is both inventory and engine input, documented in docs/INVENTORY.md | Part 3: both files present; template through register mode, exit 0, 1 record | Verified |
| 6 | 17 | Questionnaire complete, "Thirty questions", "each carrying the framework anchor it evidences" | Part 3: 30 numbered questions; 23 carry "Anchors:"; 19 to 22 name OWASP LLM codes inline, 28 names Article 26(5), 29 names SS1/23; question 30 names no framework anchor | Exception |
| 7 | 18 | LLM intake assistant "Designed, not yet built"; evaluation results not yet published | Part 3: design document present; no LLM code in the package (grep exit 1); no model card; no results in the tree | Verified |
| 8 | 28 to 41 | The `assess examples/cv_screening.json` output shown | Part 2: compare, 0 shown lines missing | Verified |
| 9 | 45 to 64 | The `register examples/inventory.csv` output shown | Part 2: compare, 0 shown lines missing | Verified |
| 10 | 66 | Each record carries the assessment date, tool version, verification date, assessor, answers and every obligation with both dates | Part 2: header line 7 of 7, assessor 7 of 7, answers section 7 of 7, two-date table 7 of 7 | Verified |
| 11 | 70 | Annex III from 2 December 2027, Annex I from 2 August 2028, Article 50(2) grace to 2 December 2026; both dates and a status flag on every obligation; legal status on every output | Part 2: `timeline.json` values; `assess` prints "original -> amended (status)" per obligation and the legal-status note; summary prints its legal-status line | Verified |
| 12 | 74 | Gates in the Act's order; derogation blocked by profiling; Article 50 stacks; provider duty a note for a deployer; unknown ids fail closed; consistency checks; eight Annex III areas | Part 3: 18 named tests passed; 8 areas | Verified |
| 13 | 80 | "Python 3.11+" | `requires-python >=3.11` (WP-CA06-design-20261011); CI on 3.11 and 3.12 (WP-CA03-operating-20261011); Python 3.14.4 here | Verified |
| 14 | 83 | `python3 -m venv .venv && source .venv/bin/activate` | Part 1: exit 0 | Verified |
| 15 | 84 | `pip install -e ".[dev]"` | Part 1: exit 0 | Verified |
| 16 | 85 | `aiact-triage interactive` walks the intake for one system | Part 1: as written with no terminal, `EOFError` at the first prompt; with piped answers, completes, MINIMAL RISK, exit 0 | Verified |
| 17 | 86 | `aiact-triage assess case.json` | Part 1: as written, `FileNotFoundError: ... 'case.json'`, exit 1; no `case.json` exists in the repository | Exception |
| 18 | 87 | `aiact-triage register inventory.csv --out audit` | Part 1: as written, `FileNotFoundError: ... 'inventory.csv'`, exit 1; the file exists only as `examples/inventory.csv` | Exception |
| 19 | 88 | `pytest` runs the worked classification cases | Part 1: 38 passed | Verified |
| 20 | 91 | Register accepts CSV, unknown columns pass through, or a JSON list; see `examples/` | Part 3: `test_unknown_columns_flow_into_metadata` and `test_json_register_and_slug_edge_cases` passed; `examples/` present | Verified |
| 21 | 95 | Template's model-risk columns pass through into each record; field definitions in docs/INVENTORY.md | Part 3: record shows `model_id`, `business_owner`, `model_tier`, `known_limitations`, `validation_status` as inventory fields | Verified |
| 22 | 97 | Cross-framework flags as described (SS1/23; DORA Articles 28(3) and 30; ISO/IEC 42001; GDPR Article 9) | Part 3: five rules and triggers as described; seven cross-framework tests passed | Verified |
| 23 | 101 | Each of the thirty questions names its framework anchor and the artefact to request; answers without evidence are assertions; closes with a three-way verdict | Part 3: "Evidence:" 30 of 30; verdict block present with proceed, proceed with conditions, decline; anchor as claim 6, question 30 has none | Exception |
| 24 | 105 | "All legal content sits in `src/aiact_triage/data/*.json`" | Part 3: `register.py` line 259 hard-codes, in the summary it prints, that the amended dates are the binding law and that Regulation (EU) 2026/1744 has been "in force since 27 July 2026"; the `cli.py` and `rules.py` hits are docstrings | Exception |
| 25 | 105 | "an article citation on every rule" | WP-CA07-operating-20261011: the `sandboxes` timeline milestone carries none | Exception |
| 26 | 105 | "a metadata block recording sources" | Part 3: `_meta` in 6 of 6 files | Verified |
| 27 | 105 | Verification date recorded in the timeline data and carried into every audit record | WP-CA07-operating-20261011; Part 2: 7 of 7 records | Verified |
| 28 | 105 | The encoding draws from Regulation (EU) 2024/1689 and Regulation (EU) 2026/1744 | File sources and text (WP-CA07-operating-20261011); the Official Journal text itself not consulted | Verified |
| 29 | 105 | On publication every encoded date was re-verified and survived unchanged | Part 3: no `original_date` or `amended_date` line changed between `83d704c` and `f817735`; `last_verified` 2026-08-04. The re-verification act itself is not observable in the tree; what is observable agrees | Verified |
| 30 | 105 | A date correction is a one-file change and a moved date fails the suite | Part 4: one value moved in `timeline.json` only; 3 tests failed, 35 passed | Verified |
| 31 | 107 | A curated subset that does not update itself | Part 3: no network code in the package (grep exit 1) | Verified |
| 32 | 111 | Deployer position; provider case at summary level | Part 3: provider content is `high_risk_provider_summary` and `deployer_becomes_provider` only | Verified |
| 33 | 111 | GPAI obligations out of scope | Part 3: no GPAI handling in package code (grep exit 1) | Verified |
| 34 | 111 | Annex I handled at product level, without the Section A/B split | Part 3: a single `annex_i_product` boolean | Verified |
| 35 | 111 | Omnibus dates verified against Regulation (EU) 2026/1744 as published | As claims 28 and 29 | Verified |
| 36 | 111 | The LLM intake assistant is a design, not running code | As claim 7 | Verified |
| 37 | 76 | Methodology in docs/METHODOLOGY.md | Tracked at this HEAD (WP-CA01-design-20261011, `git ls-files`) | Verified |

Totals: 37 claims, 31 verified, 6 exceptions (claims 6, 17, 18, 23, 24, 25).
The 6 exceptions come from 4 distinct conditions: question 30 of the
questionnaire carries no framework anchor (claims 6 and 23); the install
block names `case.json` and `inventory.csv`, which do not exist in the
repository (claims 17 and 18); one legal statement lives in package code
(claim 24); and one rule lacks an article citation (claim 25, from CA-07).
The test-count claim, claim 2, holds, so pre-drafted Finding 4 is not live.

**Executed.** 2026-10-11, 13:10 BST (final capture run; runs at 13:08 and
13:09 lacked, respectively, the fence-skipping fix in `compare.py` and the
egg-info exclusion in the LLM grep, then the assessor and table counts, the
provider-note test and the package-code legal-statement check).

**Conclusion.** Operating exception: 6 of 37 README status claims do not match observable state (four distinct conditions: an unanchored questionnaire item, two install commands naming files that do not exist, a legal statement held in code, and a rule without an article citation), while the other 31, including the 38-test claim, are verified.
