# WP-CA05-operating-20261011

**Control.** CA-05, test suite covering the classification gates, with a regression file.

**Test method and reason.** Automated regime for the automated half of
CA-05, per PLAN.md section 5: inspection of the `pytest -q` step in CA-03's
test-of-one run, both legs, with configuration stability by cross-reference
to WP-CA03-operating-20261011 part (b), which shows the step unchanged since
the workflow was introduced. Scope limit, stated: the reperformance PLAN.md
section 4 specifies for CA-05 (fresh clone, fresh venv,
`pip install -e ".[dev]"`, `pytest -q`) belongs to Phase 2 session three and
is not performed here; this workpaper does not stand in for it. Sources:
`WP-CA03-operating-20261011-run-33065206756-logs.zip`, unpacked as recorded
in WP-CA03-operating-20261011, and
`WP-CA03-operating-20261011-run-33065206756-steps.tsv`, captured outside the
sandbox by B. Struve on 11 October 2026 and committed in 9b60dc2. No venv was
created.

**Population and regime.** Automated regime, test of one: step 5
(`pytest -q`) of run 33065206756 on `main` at `7aab9f9`, both matrix legs.

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
L=<SCRATCH>/logs_33065206756
echo "=== step 5 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ==="
awk -F'\t' '$2==5' evidence/WP-CA03-operating-20261011-run-33065206756-steps.tsv
cd "$L"
for f in "0_test (3.11).txt" "1_test (3.12).txt"; do
  echo "=== $f: sed -n '/##\[group\]Run pytest -q/,/passed in/p' | sed 's/\x1b/^[/g' ==="
  sed -n '/##\[group\]Run pytest -q/,/passed in/p' "$f" | sed 's/\x1b/^[/g'
done
```
The final `sed` shows each escape byte as `^[`.

**Evidence.**
```
=== step 5 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ===
test (3.12)	5	Run pytest -q	success
test (3.11)	5	Run pytest -q	success
=== 0_test (3.11).txt: sed -n '/##\[group\]Run pytest -q/,/passed in/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:56:56.7710870Z ##[group]Run pytest -q
2026-08-27T10:56:56.7711244Z ^[[36;1mpytest -q^[[0m
2026-08-27T10:56:56.7737380Z shell: /usr/bin/bash -e {0}
2026-08-27T10:56:56.7737957Z env:
2026-08-27T10:56:56.7738400Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:56.7738918Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-08-27T10:56:56.7739404Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:56.7739878Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:56.7740320Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:56.7740776Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-08-27T10:56:56.7741185Z ##[endgroup]
2026-08-27T10:56:57.2139975Z ......................................                                   [100%]
2026-08-27T10:56:57.2140852Z 38 passed in 0.08s
=== 1_test (3.12).txt: sed -n '/##\[group\]Run pytest -q/,/passed in/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:56:59.4054674Z ##[group]Run pytest -q
2026-08-27T10:56:59.4055014Z ^[[36;1mpytest -q^[[0m
2026-08-27T10:56:59.4097599Z shell: /usr/bin/bash -e {0}
2026-08-27T10:56:59.4097876Z env:
2026-08-27T10:56:59.4098155Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:59.4098622Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib/pkgconfig
2026-08-27T10:56:59.4099052Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:59.4099435Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:59.4099811Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:59.4100203Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib
2026-08-27T10:56:59.4100537Z ##[endgroup]
2026-08-27T10:57:00.0709486Z ......................................                                   [100%]
2026-08-27T10:57:00.0710225Z 38 passed in 0.10s
```

**Executed.** 2026-10-11, 12:36 BST (final capture run; earlier runs of the
same script at 12:35 and 12:36 differed only in how escape bytes were
shown).

**Conclusion.** Operating effectively, for the automated half tested here: step 5 ran `pytest -q` on both legs at the scope-freeze commit and reported "38 passed" each time, with `steps.tsv` recording success, a count equal to the 38 collected in WP-CA05-design-20261011.
