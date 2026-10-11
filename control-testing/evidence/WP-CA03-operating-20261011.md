# WP-CA03-operating-20261011

**Control.** CA-03, CI runs the full test suite on every push and pull request.

**Test method and reason.** Automated regime, PLAN.md section 5, in three
parts: (a) test of one, a single completed run inspected end to end, both
matrix legs; (b) configuration stability, the workflow file's own history
over the period, every change inspected for weakening; (c) completeness,
every push to `main` in the period reconciled against the run list.
Reperformance deliberately not used: re-running CI proves the runner works
today, not that the control operated during the period. Deviations, four:

1. Sources. `gh` and outbound HTTP are unavailable in this sandbox, so
   `gh run list` was not run here. The GitHub-side evidence was captured
   outside the sandbox by B. Struve on 11 October 2026 and committed before
   this test, in 9b60dc2: `WP-CA03-operating-20261011-activity.jsonl` (push
   population), `WP-CA03-operating-20261011-runs.json` (run list),
   `WP-CA03-operating-20261011-run-33065206756-logs.zip` (full logs of the
   run), `WP-CA03-operating-20261011-run-33065206756-steps.tsv` (step
   results), with `WP-CA03-operating-20261011-capture-note.txt` (captured
   2026-10-11T11:25:32Z) and
   `WP-CA03-operating-20261011-run-33065206756-logs-error.txt` (empty). How
   those files were captured is recorded by B. Struve in
   `WP-CA03-operating-20261011-capture-commands.txt` (gh 2.46.0): the
   activity feed fetched with `--paginate` at `per_page=100`, and the run
   list with `gh run list --limit 100`, which returned 10 runs.
2. Push population. PLAN.md names no source for it. The repository events
   feed no longer covers the period (STATE.md, 11 October 2026), so the
   population is the repository activity feed: 11 records, the first being
   the branch creation of 2026-07-14T18:06:35Z.
3. Reconciliation rule, as B. Struve fixed it for this session and
   consistent with PLAN.md section 4 as amended by D9. The unit is the push
   activity. A push expects one run of the workflow named "tests" whose head
   SHA equals the push's "after" SHA when `.github/workflows/tests.yml`
   exists in the tree at "after"; a push whose "after" predates the commit
   that introduced the file expects none. Runs of any other workflow are
   excluded and listed. Runs on tag refs are matched to the push whose
   "after" SHA equals the tag's target commit. Any unmatched push or run is
   an operating exception.
4. Test of one evidenced from the logs rather than only a screenshot. The
   archive was unpacked into the session scratchpad (`<SCRATCH>`) with
   Python's zipfile; its SHA-256 is recorded before and after, and the
   archive was not modified. Screenshot of the test (3.12) job page with
   step 6 expanded: described below.

No venv was created for this test.

**Population and regime.** Automated regime. Pushes: 11 activity records on
`refs/heads/main`, 10 pushes and 1 branch creation, 2026-07-14 to
2026-08-27, all reconciled. Runs: 10 listed, 9 of workflow "tests" and 1 of
"Dependency Graph", all reconciled or excluded. Configuration history: 2
commits touch the workflow file. Test of one: run 33065206756, the run on the
scope-freeze commit `7aab9f9` and the last push of the period, selected by
B. Struve, both matrix legs. Pull requests: none exist in the period
(WP-CA10-design-20261011), so the `pull_request` trigger had no population.

**Procedure executed.** Run from the pack directory. Unpacking helper,
reproduced in full:
```
import sys, zipfile
zf = zipfile.ZipFile(sys.argv[1])
for i in zf.infolist():
    print(f"{i.file_size:>8} {i.date_time} {i.filename}")
zf.extractall(sys.argv[2])
print("extracted to", sys.argv[2])
```
Reconciliation script, `reconcile.py`, reproduced in full:
```
"""CA-03 completeness: reconcile push activities against workflow runs.

Usage: python3 -I reconcile.py REPO ACTIVITY_JSONL RUNS_JSON
Unit: the push activity. A push expects one run of workflow "tests" whose
headSha equals the push's "after" SHA if .github/workflows/tests.yml exists
in the tree at "after"; otherwise it expects no run. Runs on tag refs are
matched to the push whose "after" SHA equals the tag's target commit. Runs of
any other workflow are excluded and listed.
"""
import json
import subprocess
import sys

repo, activity_path, runs_path = sys.argv[1:4]
WF = ".github/workflows/tests.yml"


def git(*args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


pushes = [json.loads(line) for line in open(activity_path) if line.strip()]
pushes.sort(key=lambda p: p["timestamp"])
runs = json.load(open(runs_path))
tags = git("tag", "-l")[1].split()
tag_target = {t: git("rev-parse", t + "^{commit}")[1] for t in tags}

print(f"activity records: {len(pushes)}; runs listed: {len(runs)}")
print("activity types:", sorted({p['activity_type'] for p in pushes}))
print("refs:", sorted({p['ref'] for p in pushes}))
print("actors:", sorted({p['actor']['login'] for p in pushes}))
print("tag targets:", ", ".join(f"{t}={c[:7]}" for t, c in tag_target.items()))
print()

disposition = {}
push_exceptions = 0
print("PUSHES")
print("| # | timestamp (UTC) | type | before | after | commits | tests.yml at after | expected | matched run(s) | result |")
print("|---|---|---|---|---|---|---|---|---|---|")
for n, p in enumerate(pushes, 1):
    before, after = p["before"], p["after"]
    rng = after if set(before) == {"0"} else f"{before}..{after}"
    commits = git("rev-list", "--count", rng)[1]
    has_wf = git("cat-file", "-e", f"{after}:{WF}")[0] == 0
    expected = "1 run" if has_wf else "no run"
    matched = []
    for r in runs:
        if r["workflowName"] != "tests" or r["headSha"] != after:
            continue
        ref = r["headBranch"]
        if ref == p["ref"].removeprefix("refs/heads/"):
            matched.append(f"{r['databaseId']} (main, {r['conclusion']})")
            disposition[r["databaseId"]] = f"push #{n}"
        elif ref in tags and tag_target[ref] == after:
            matched.append(f"{r['databaseId']} (tag {ref}, {r['conclusion']})")
            disposition[r["databaseId"]] = f"push #{n}, tag {ref}"
    branch_runs = [m for m in matched if "(main" in m]
    if has_wf:
        result = "MATCHED" if len(branch_runs) == 1 else f"EXCEPTION ({len(branch_runs)} branch runs)"
    else:
        result = "NO RUN EXPECTED, NONE FOUND" if not matched else "EXCEPTION (run where none expected)"
    push_exceptions += result.startswith("EXCEPTION")
    print(f"| {n} | {p['timestamp']} | {p['activity_type']} | {before[:7]} | {after[:7]} | {commits} "
          f"| {'yes' if has_wf else 'no'} | {expected} | {'; '.join(matched) or 'none'} | {result} |")

print()
print("RUNS")
print("| run id | workflow | event | ref | head SHA | created (UTC) | conclusion | disposition |")
print("|---|---|---|---|---|---|---|---|")
for r in sorted(runs, key=lambda r: (r["createdAt"], r["databaseId"])):
    if r["workflowName"] != "tests":
        d = "EXCLUDED (not the tests workflow)"
    else:
        d = disposition.get(r["databaseId"], "UNMATCHED")
    print(f"| {r['databaseId']} | {r['workflowName']} | {r['event']} | {r['headBranch']} | {r['headSha'][:7]} "
          f"| {r['createdAt']} | {r['conclusion']} | {d} |")

print()
unmatched = [r for r in runs if r["workflowName"] == "tests" and r["databaseId"] not in disposition]
print("push exceptions:", push_exceptions)
print("tests runs matched:", len(disposition))
print("tests runs unmatched:", len(unmatched))
print("runs excluded:", sum(r["workflowName"] != "tests" for r in runs))
print("pushes expecting a run:", sum(git("cat-file", "-e", f"{p['after']}:{WF}")[0] == 0 for p in pushes))
```
Capture script, reproduced in full (the working copy of the logs had been
unpacked to `<SCRATCH>/logs_33065206756` with the same helper before it
ran):
```
S=<SCRATCH>
L="$S/logs_33065206756"
E=evidence
echo "=== sha256sum of the committed archive, before and after unpacking ==="
sha256sum $E/WP-CA03-operating-20261011-run-33065206756-logs.zip
python3 -I $S/scripts/unzip_logs.py $E/WP-CA03-operating-20261011-run-33065206756-logs.zip "$L.check" | sed "s|$S|<SCRATCH>|"
sha256sum $E/WP-CA03-operating-20261011-run-33065206756-logs.zip
diff -r "$L" "$L.check" && echo "UNPACKED TREE IDENTICAL TO WORKING COPY"
echo
echo "##### (c) COMPLETENESS #####"
echo "=== git -C repo_under_test log -1 --format='%H' ==="; git -C repo_under_test log -1 --format='%H'
echo "=== git -C repo_under_test log --diff-filter=A --format='%H %ci %s' -- .github/workflows/tests.yml ==="
git -C repo_under_test log --diff-filter=A --format='%H %ci %s' -- .github/workflows/tests.yml
echo "=== python3 -I reconcile.py repo_under_test activity.jsonl runs.json ==="
python3 -I $S/scripts/reconcile.py repo_under_test $E/WP-CA03-operating-20261011-activity.jsonl $E/WP-CA03-operating-20261011-runs.json
echo
echo "##### (b) CONFIGURATION STABILITY #####"
echo "=== git -C repo_under_test log --follow --format='%H %ci %an %s' -- .github/workflows/tests.yml ==="
git -C repo_under_test log --follow --format='%H %ci %an %s' -- .github/workflows/tests.yml
echo "=== git -C repo_under_test log --follow -p --format='commit %H %ci %s' -- .github/workflows/tests.yml ==="
git -C repo_under_test log --follow -p --format='commit %H %ci %s' -- .github/workflows/tests.yml
echo "=== git -C repo_under_test diff a30bc34 7aab9f9 -- .github/workflows/tests.yml | wc -l ==="
git -C repo_under_test diff a30bc34 7aab9f9 -- .github/workflows/tests.yml | wc -l
echo "=== grep -n -i -E 'Download action repository|node' (both legs) ==="
grep -n -i -E 'Download action repository|node' "$L/0_test (3.11).txt" "$L/1_test (3.12).txt" | sed "s|$L/||"
echo
echo "##### (a) TEST OF ONE: RUN 33065206756 #####"
echo "=== run 33065206756 in WP-CA03-operating-20261011-runs.json ==="
python3 -I -c 'import json,sys; [print(json.dumps(r)) for r in json.load(open(sys.argv[1])) if r["databaseId"]==33065206756]' $E/WP-CA03-operating-20261011-runs.json
echo "=== cat WP-CA03-operating-20261011-run-33065206756-steps.tsv ==="
cat $E/WP-CA03-operating-20261011-run-33065206756-steps.tsv
echo "=== wc -c WP-CA03-operating-20261011-run-33065206756-logs-error.txt ==="
wc -c < $E/WP-CA03-operating-20261011-run-33065206756-logs-error.txt
cd "$L"
for leg in "test (3.11)" "test (3.12)"; do
  echo "=== cat '$leg/system.txt' ==="; cat "$leg/system.txt"; echo
done
for f in "0_test (3.11).txt" "1_test (3.12).txt"; do
  echo "=== $f: job name, checkout, interpreter, outcomes ==="
  grep -n -E 'Complete job name|fetch --no-tags|Successfully set up CPython|##\[group\]Run |passed in|failed|packaged data ok' "$f" | sed 's/\x1b/^[/g'
  echo "--- grep -n -A1 'git log -1 --format=%H'"; grep -n -A1 'git log -1 --format=%H' "$f"
  echo "--- grep -c -E '##\[(error|warning)\]'"; grep -c -E '##\[(error|warning)\]' "$f"
done
```

**Evidence.**
```
=== sha256sum of the committed archive, before and after unpacking ===
dc7c15e34b9673f4ac00e082b8c19040d77055ce56776313dfc78f4c27310996  evidence/WP-CA03-operating-20261011-run-33065206756-logs.zip
   22098 (1980, 0, 0, 0, 0, 0) 0_test (3.11).txt
     575 (1980, 0, 0, 0, 0, 0) test (3.11)/system.txt
   22100 (1980, 0, 0, 0, 0, 0) 1_test (3.12).txt
     575 (1980, 0, 0, 0, 0, 0) test (3.12)/system.txt
extracted to <SCRATCH>/logs_33065206756.check
dc7c15e34b9673f4ac00e082b8c19040d77055ce56776313dfc78f4c27310996  evidence/WP-CA03-operating-20261011-run-33065206756-logs.zip
UNPACKED TREE IDENTICAL TO WORKING COPY

##### (c) COMPLETENESS #####
=== git -C repo_under_test log -1 --format='%H' ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
=== git -C repo_under_test log --diff-filter=A --format='%H %ci %s' -- .github/workflows/tests.yml ===
73fd4b01d5132044b4b8db7d7fb296a40488379b 2026-07-15 15:15:51 +0100 Add CI: tests on Python 3.11 and 3.12 with a non-editable install check
=== python3 -I reconcile.py repo_under_test activity.jsonl runs.json ===
activity records: 11; runs listed: 10
activity types: ['branch_creation', 'push']
refs: ['refs/heads/main']
actors: ['BeeStru']
tag targets: v0.1.0=0271732, v0.2.0=48330a5, v0.3.0=66bb1f6, v0.4.0=83d704c, v0.5.0=f817735

PUSHES
| # | timestamp (UTC) | type | before | after | commits | tests.yml at after | expected | matched run(s) | result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-07-14T18:06:35Z | branch_creation | 0000000 | d24953d | 4 | no | no run | none | NO RUN EXPECTED, NONE FOUND |
| 2 | 2026-07-15T11:58:07Z | push | d24953d | 0271732 | 9 | no | no run | none | NO RUN EXPECTED, NONE FOUND |
| 3 | 2026-07-15T12:14:01Z | push | 0271732 | 48330a5 | 3 | no | no run | none | NO RUN EXPECTED, NONE FOUND |
| 4 | 2026-07-15T14:03:12Z | push | 48330a5 | 66bb1f6 | 5 | no | no run | none | NO RUN EXPECTED, NONE FOUND |
| 5 | 2026-07-15T14:15:52Z | push | 66bb1f6 | 73fd4b0 | 2 | yes | 1 run | 29422786125 (main, success) | MATCHED |
| 6 | 2026-07-15T14:24:39Z | push | 73fd4b0 | a30bc34 | 1 | yes | 1 run | 29423426673 (main, success) | MATCHED |
| 7 | 2026-07-15T15:18:31Z | push | a30bc34 | 83d704c | 4 | yes | 1 run | 29427506507 (tag v0.4.0, success); 29427506420 (main, success) | MATCHED |
| 8 | 2026-08-04T09:22:11Z | push | 83d704c | f817735 | 11 | yes | 1 run | 30896015071 (main, success); 30896014594 (tag v0.5.0, success) | MATCHED |
| 9 | 2026-08-27T10:41:58Z | push | f817735 | db46969 | 4 | yes | 1 run | 33064159235 (main, success) | MATCHED |
| 10 | 2026-08-27T10:47:30Z | push | db46969 | 8771a60 | 1 | yes | 1 run | 33064547178 (main, success) | MATCHED |
| 11 | 2026-08-27T10:56:45Z | push | 8771a60 | 7aab9f9 | 1 | yes | 1 run | 33065206756 (main, success) | MATCHED |

RUNS
| run id | workflow | event | ref | head SHA | created (UTC) | conclusion | disposition |
|---|---|---|---|---|---|---|---|
| 29422786125 | tests | push | main | 73fd4b0 | 2026-07-15T14:15:59Z | success | push #5 |
| 29423426673 | tests | push | main | a30bc34 | 2026-07-15T14:24:43Z | success | push #6 |
| 29427506420 | tests | push | main | 83d704c | 2026-07-15T15:18:33Z | success | push #7 |
| 29427506507 | tests | push | v0.4.0 | 83d704c | 2026-07-15T15:18:33Z | success | push #7, tag v0.4.0 |
| 29512895018 | Dependency Graph | dynamic | main | 83d704c | 2026-07-16T15:49:35Z | success | EXCLUDED (not the tests workflow) |
| 30896014594 | tests | push | v0.5.0 | f817735 | 2026-08-04T09:22:14Z | success | push #8, tag v0.5.0 |
| 30896015071 | tests | push | main | f817735 | 2026-08-04T09:22:14Z | success | push #8 |
| 33064159235 | tests | push | main | db46969 | 2026-08-27T10:42:01Z | success | push #9 |
| 33064547178 | tests | push | main | 8771a60 | 2026-08-27T10:47:32Z | success | push #10 |
| 33065206756 | tests | push | main | 7aab9f9 | 2026-08-27T10:56:47Z | success | push #11 |

push exceptions: 0
tests runs matched: 9
tests runs unmatched: 0
runs excluded: 1
pushes expecting a run: 7

##### (b) CONFIGURATION STABILITY #####
=== git -C repo_under_test log --follow --format='%H %ci %an %s' -- .github/workflows/tests.yml ===
a30bc34d5c1387fb2e5ae6610bc625005d8ca173 2026-07-15 15:24:38 +0100 Bastian Struve Bump CI actions to current majors on the Node 24 runtime
73fd4b01d5132044b4b8db7d7fb296a40488379b 2026-07-15 15:15:51 +0100 Bastian Struve Add CI: tests on Python 3.11 and 3.12 with a non-editable install check
=== git -C repo_under_test log --follow -p --format='commit %H %ci %s' -- .github/workflows/tests.yml ===
commit a30bc34d5c1387fb2e5ae6610bc625005d8ca173 2026-07-15 15:24:38 +0100 Bump CI actions to current majors on the Node 24 runtime

diff --git a/.github/workflows/tests.yml b/.github/workflows/tests.yml
index 9615741..a0adb56 100644
--- a/.github/workflows/tests.yml
+++ b/.github/workflows/tests.yml
@@ -11,8 +11,8 @@ jobs:
       matrix:
         python-version: ["3.11", "3.12"]
     steps:
-      - uses: actions/checkout@v4
-      - uses: actions/setup-python@v5
+      - uses: actions/checkout@v7
+      - uses: actions/setup-python@v6
         with:
           python-version: ${{ matrix.python-version }}
       - run: pip install -e ".[dev]"
commit 73fd4b01d5132044b4b8db7d7fb296a40488379b 2026-07-15 15:15:51 +0100 Add CI: tests on Python 3.11 and 3.12 with a non-editable install check

diff --git a/.github/workflows/tests.yml b/.github/workflows/tests.yml
new file mode 100644
index 0000000..9615741
--- /dev/null
+++ b/.github/workflows/tests.yml
@@ -0,0 +1,24 @@
+name: tests
+
+on:
+  push:
+  pull_request:
+
+jobs:
+  test:
+    runs-on: ubuntu-latest
+    strategy:
+      matrix:
+        python-version: ["3.11", "3.12"]
+    steps:
+      - uses: actions/checkout@v4
+      - uses: actions/setup-python@v5
+        with:
+          python-version: ${{ matrix.python-version }}
+      - run: pip install -e ".[dev]"
+      - run: pytest -q
+      - name: prove non-editable install carries the rule data
+        run: |
+          pip uninstall -y aiact-triage
+          pip install .
+          cd /tmp && python -c "import aiact_triage.rules as r; r.timeline(); print('packaged data ok')"
=== git -C repo_under_test diff a30bc34 7aab9f9 -- .github/workflows/tests.yml | wc -l ===
0
=== grep -n -i -E 'Download action repository|node' (both legs) ===
0_test (3.11).txt:30:2026-08-27T10:56:50.8066475Z Download action repository 'actions/checkout@v7' (SHA:3d3c42e5aac5ba805825da76410c181273ba90b1)
0_test (3.11).txt:31:2026-08-27T10:56:50.9568923Z Download action repository 'actions/setup-python@v6' (SHA:ece7cb06caefa5fff74198d8649806c4678c61a1)
1_test (3.12).txt:30:2026-08-27T10:56:50.6205023Z Download action repository 'actions/checkout@v7' (SHA:3d3c42e5aac5ba805825da76410c181273ba90b1)
1_test (3.12).txt:31:2026-08-27T10:56:50.7628556Z Download action repository 'actions/setup-python@v6' (SHA:ece7cb06caefa5fff74198d8649806c4678c61a1)

##### (a) TEST OF ONE: RUN 33065206756 #####
=== run 33065206756 in WP-CA03-operating-20261011-runs.json ===
{"conclusion": "success", "createdAt": "2026-08-27T10:56:47Z", "databaseId": 33065206756, "event": "push", "headBranch": "main", "headSha": "7aab9f95065f9cf69cbdefe5a9aed64c361386ce", "status": "completed", "workflowName": "tests"}
=== cat WP-CA03-operating-20261011-run-33065206756-steps.tsv ===
test (3.12)	1	Set up job	success
test (3.12)	2	Run actions/checkout@v7	success
test (3.12)	3	Run actions/setup-python@v6	success
test (3.12)	4	Run pip install -e ".[dev]"	success
test (3.12)	5	Run pytest -q	success
test (3.12)	6	prove non-editable install carries the rule data	success
test (3.12)	11	Post Run actions/setup-python@v6	success
test (3.12)	12	Post Run actions/checkout@v7	success
test (3.12)	13	Complete job	success
test (3.11)	1	Set up job	success
test (3.11)	2	Run actions/checkout@v7	success
test (3.11)	3	Run actions/setup-python@v6	success
test (3.11)	4	Run pip install -e ".[dev]"	success
test (3.11)	5	Run pytest -q	success
test (3.11)	6	prove non-editable install carries the rule data	success
test (3.11)	11	Post Run actions/setup-python@v6	success
test (3.11)	12	Post Run actions/checkout@v7	success
test (3.11)	13	Complete job	success
=== wc -c WP-CA03-operating-20261011-run-33065206756-logs-error.txt ===
0
=== cat 'test (3.11)/system.txt' ===
2026-08-27T10:56:48.0970000Z Evaluating test.if
2026-08-27T10:56:48.0970000Z Evaluating: success()
2026-08-27T10:56:48.0970000Z Result: true
2026-08-27T10:56:48.0980000Z Requested labels: ubuntu-latest
2026-08-27T10:56:48.0980000Z Job defined at: BeeStru/eu-ai-act-triage/.github/workflows/tests.yml@refs/heads/main
2026-08-27T10:56:48.0980000Z Waiting for a runner to pick up this job...
2026-08-27T10:56:48.3380000Z Job is waiting for a hosted runner to come online.
2026-08-27T10:56:48.3390000Z Job is about to start running on the hosted runner: GitHub Actions 1000000018
=== cat 'test (3.12)/system.txt' ===
2026-08-27T10:56:48.0960000Z Evaluating test.if
2026-08-27T10:56:48.0960000Z Evaluating: success()
2026-08-27T10:56:48.0960000Z Result: true
2026-08-27T10:56:48.0980000Z Requested labels: ubuntu-latest
2026-08-27T10:56:48.0980000Z Job defined at: BeeStru/eu-ai-act-triage/.github/workflows/tests.yml@refs/heads/main
2026-08-27T10:56:48.0980000Z Waiting for a runner to pick up this job...
2026-08-27T10:56:48.3380000Z Job is about to start running on the hosted runner: GitHub Actions 1000000017
2026-08-27T10:56:48.3380000Z Job is waiting for a hosted runner to come online.
=== 0_test (3.11).txt: job name, checkout, interpreter, outcomes ===
32:2026-08-27T10:56:51.1574700Z Complete job name: test (3.11)
33:2026-08-27T10:56:51.2217133Z ##[group]Run actions/checkout@v7
100:2026-08-27T10:56:51.5652846Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +7aab9f95065f9cf69cbdefe5a9aed64c361386ce:refs/remotes/origin/main
119:2026-08-27T10:56:52.2678203Z ##[group]Run actions/setup-python@v6
129:2026-08-27T10:56:52.4024351Z Successfully set up CPython (3.11.16)
131:2026-08-27T10:56:52.4202884Z ##[group]Run pip install -e ".[dev]"
176:2026-08-27T10:56:56.7710870Z ##[group]Run pytest -q
188:2026-08-27T10:56:57.2140852Z 38 passed in 0.08s
189:2026-08-27T10:56:57.2396204Z ##[group]Run pip uninstall -y aiact-triage
192:2026-08-27T10:56:57.2397690Z ^[[36;1mcd /tmp && python -c "import aiact_triage.rules as r; r.timeline(); print('packaged data ok')"^[[0m
220:2026-08-27T10:56:59.1472459Z packaged data ok
--- grep -n -A1 'git log -1 --format=%H'
117:2026-08-27T10:56:52.2316457Z [command]/usr/bin/git log -1 --format=%H
118-2026-08-27T10:56:52.2338658Z 7aab9f95065f9cf69cbdefe5a9aed64c361386ce
--- grep -c -E '##\[(error|warning)\]'
0
=== 1_test (3.12).txt: job name, checkout, interpreter, outcomes ===
32:2026-08-27T10:56:51.0378100Z Complete job name: test (3.12)
33:2026-08-27T10:56:51.1103919Z ##[group]Run actions/checkout@v7
100:2026-08-27T10:56:51.3764186Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +7aab9f95065f9cf69cbdefe5a9aed64c361386ce:refs/remotes/origin/main
119:2026-08-27T10:56:51.8229062Z ##[group]Run actions/setup-python@v6
129:2026-08-27T10:56:51.9596898Z Successfully set up CPython (3.12.14)
131:2026-08-27T10:56:51.9849947Z ##[group]Run pip install -e ".[dev]"
176:2026-08-27T10:56:59.4054674Z ##[group]Run pytest -q
188:2026-08-27T10:57:00.0710225Z 38 passed in 0.10s
189:2026-08-27T10:57:00.0985128Z ##[group]Run pip uninstall -y aiact-triage
192:2026-08-27T10:57:00.0986274Z ^[[36;1mcd /tmp && python -c "import aiact_triage.rules as r; r.timeline(); print('packaged data ok')"^[[0m
220:2026-08-27T10:57:02.3585744Z packaged data ok
--- grep -n -A1 'git log -1 --format=%H'
117:2026-08-27T10:56:51.7906546Z [command]/usr/bin/git log -1 --format=%H
118-2026-08-27T10:56:51.7937698Z 7aab9f95065f9cf69cbdefe5a9aed64c361386ce
--- grep -c -E '##\[(error|warning)\]'
0
```
The script exits 1 because its last command, `grep -c`, found no
annotations; the count printed is 0.

Screenshot: `WP-CA03-operating-20261011-run.png`, captured by B. Struve on
11 October 2026, full window, URL bar and system clock visible. The system
clock reads 11 Oct 12:54. The URL bar reads
`github.com/BeeStru/eu-ai-act-triage/actions/runs/33065206756/job/98493477620`.
The page is run "Update README.md #9" of workflow "tests", with jobs
test (3.11) and test (3.12) both marked green in the side panel and
test (3.12) selected, headed "succeeded on Aug 27 in 15s". Its step list
shows nine steps, each with a completed tick: Set up job; Run
actions/checkout@v7; Run actions/setup-python@v6; Run pip install -e
".[dev]"; Run pytest -q; prove non-editable install carries the rule data;
Post Run actions/setup-python@v6; Post Run actions/checkout@v7; Complete
job. Step 6, "prove non-editable install carries the rule data", is
expanded, showing log lines 1 and 13 to 31, from "Run pip uninstall -y
aiact-triage" to "packaged data ok", including the wheel hash
`3c72d84e6e525ac93ca7783915d30d8ff6e082cb7da20a9a72f844a890eb86d8` and
cache directory `pip-ephem-wheel-cache-4trqonub`, which match the 3.12 leg's
step 6 in the log archive (WP-CA04-operating-20261011). The test (3.11)
job is not expanded in the image; that leg is evidenced by the logs above.
An earlier capture showing only the run summary page was checked on
11 October and not accepted (STATE.md).

What the output shows.

(c) Completeness. The workflow file was introduced by `73fd4b0` on
2026-07-15. Pushes 1 to 4 have "after" commits that predate it and expect no
run; none was found. Pushes 5 to 11 each expect one run, and each has exactly
one run of "tests" on `main` with the push's "after" SHA, all with
conclusion success. The two tag-ref runs, `v0.4.0` (29427506507) and
`v0.5.0` (30896014594), match pushes 7 and 8, whose "after" SHAs equal those
tags' targets. The Dependency Graph run 29512895018 (event `dynamic`) is
excluded and listed. No push and no run is unmatched: zero exceptions.
Tags `v0.1.0` to `v0.3.0` target `0271732`, `48330a5` and `66bb1f6`, all
before the workflow existed, and have no runs; the activity feed lists
`refs/heads/main` only and carries no tag-push records. Completeness of
the two sources: per `WP-CA03-operating-20261011-capture-commands.txt` the
activity feed was paginated and the run list returned 10 runs against a
limit of 100, so neither was truncated.
Observation for the record: the 27 August pre-flight in STATE.md counted
"10 completed CI workflow runs, all green"; the list holds 10 runs, one of
which is the Dependency Graph run, so 9 are runs of the tests workflow.

(b) Configuration stability. Two commits touch the file. `73fd4b0` creates
it. `a30bc34`, nine minutes later, changes only the two `uses:` lines:
`actions/checkout` from `v4` to `v7` and `actions/setup-python` from `v5` to
`v6`. Nothing has changed since (`git diff a30bc34 7aab9f9` on the file is
empty). Inspected for weakening: the triggers (`push` and `pull_request`, no
branch or path filter), the matrix (3.11, 3.12), the `python-version` input,
the install step, the `pytest -q` step and the packaged-data step are
identical before and after `a30bc34`. The change replaces the code behind
the two setup steps, not what the workflow runs or when it runs, so it is
not a weakening, and the run on `a30bc34` itself (29423426673) and every
later run succeeded. The commit message says the new majors run on the
Node 24 runtime; that could not be checked from this sandbox, which cannot
reach the actions' repositories, and the logs do not name the Node runtime
(a case-insensitive search for "node" adds no line beyond the two download
lines the same pattern matches). The conclusion does not depend on it.
Observed, not classified: both actions are referenced by movable
major-version tags rather than commit SHAs. On 27 August the logs resolve
them to `checkout` `3d3c42e5aac5ba805825da76410c181273ba90b1` and
`setup-python` `ece7cb06caefa5fff74198d8649806c4678c61a1`, so an unchanged
workflow file does not by itself fix the action code that executes.

(a) Test of one, run 33065206756. The run list records workflow "tests",
event `push`, head `7aab9f9`, conclusion success. On both legs the job was
defined from `tests.yml@refs/heads/main`, the checkout fetched and checked
out `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`, the interpreter was CPython
3.11.16 and 3.12.14 respectively, `pytest -q` reported "38 passed", the
packaged-data step printed "packaged data ok", and the log carries no
`##[error]` or `##[warning]` annotation. `steps.tsv` records every step of
both legs as success.

**Executed.** 2026-10-11, 12:36 BST (final capture run; earlier runs of the
same script at 12:35 and 12:36 differed only in how escape bytes were
shown).

**Conclusion.** Operating effectively: every push after the workflow's introduction has exactly one matching successful run of the tests workflow and no run is unaccounted for, the file's single change did not weaken it, and the test-of-one run passed all 38 tests on Python 3.11 and 3.12.
