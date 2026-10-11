# WP-CA04-operating-20261011

**Control.** CA-04, packaged-data integrity check in CI (non-editable reinstall).

**Test method and reason.** Inspection of the packaged-data step's log inside
CA-03's test-of-one run, per PLAN.md section 4, because an automated control
that ran in a recorded run is evidenced by that run's own log. Configuration
stability is shared with CA-03 by cross-reference, not duplicate capture:
WP-CA03-operating-20261011 part (b) shows the step's text unchanged since the
workflow was introduced in `73fd4b0`. Sources:
`WP-CA03-operating-20261011-run-33065206756-logs.zip`, unpacked to
`<SCRATCH>/logs_33065206756` as recorded in WP-CA03-operating-20261011, and
`WP-CA03-operating-20261011-run-33065206756-steps.tsv`, both captured
outside the sandbox by B. Struve on 11 October 2026 and committed in
9b60dc2. No deviation beyond those recorded in WP-CA03-operating-20261011.
No venv was created.

**Population and regime.** Automated regime, test of one: step 6 ("prove
non-editable install carries the rule data") of run 33065206756 on `main` at
`7aab9f9`, both matrix legs.

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
L=<SCRATCH>/logs_33065206756
echo "=== step 6 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ==="
awk -F'\t' '$2==6' evidence/WP-CA03-operating-20261011-run-33065206756-steps.tsv
cd "$L"
for f in "0_test (3.11).txt" "1_test (3.12).txt"; do
  echo "=== $f: sed -n '/##\[group\]Run pip uninstall -y aiact-triage/,/Z packaged data ok$/p' | sed 's/\x1b/^[/g' ==="
  sed -n '/##\[group\]Run pip uninstall -y aiact-triage/,/Z packaged data ok$/p' "$f" | sed 's/\x1b/^[/g'
done
```
The final `sed` shows each escape byte in the log's colour codes as `^[`
rather than writing raw control characters into this file.

**Evidence.**
```
=== step 6 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ===
test (3.12)	6	prove non-editable install carries the rule data	success
test (3.11)	6	prove non-editable install carries the rule data	success
=== 0_test (3.11).txt: sed -n '/##\[group\]Run pip uninstall -y aiact-triage/,/Z packaged data ok$/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:56:57.2396204Z ##[group]Run pip uninstall -y aiact-triage
2026-08-27T10:56:57.2396666Z ^[[36;1mpip uninstall -y aiact-triage^[[0m
2026-08-27T10:56:57.2397043Z ^[[36;1mpip install .^[[0m
2026-08-27T10:56:57.2397690Z ^[[36;1mcd /tmp && python -c "import aiact_triage.rules as r; r.timeline(); print('packaged data ok')"^[[0m
2026-08-27T10:56:57.2424140Z shell: /usr/bin/bash -e {0}
2026-08-27T10:56:57.2424509Z env:
2026-08-27T10:56:57.2424948Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:57.2425448Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-08-27T10:56:57.2426055Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:57.2426489Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:57.2426907Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:57.2427380Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-08-27T10:56:57.2427987Z ##[endgroup]
2026-08-27T10:56:57.5042398Z Found existing installation: aiact-triage 0.5.0
2026-08-27T10:56:57.5056197Z Uninstalling aiact-triage-0.5.0:
2026-08-27T10:56:57.5772291Z   Successfully uninstalled aiact-triage-0.5.0
2026-08-27T10:56:57.8755903Z Processing ./.
2026-08-27T10:56:57.8771326Z   Installing build dependencies: started
2026-08-27T10:56:58.3226894Z   Installing build dependencies: finished with status 'done'
2026-08-27T10:56:58.3233044Z   Getting requirements to build wheel: started
2026-08-27T10:56:58.6960252Z   Getting requirements to build wheel: finished with status 'done'
2026-08-27T10:56:58.6968097Z   Preparing metadata (pyproject.toml): started
2026-08-27T10:56:58.8573059Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-08-27T10:56:58.8592796Z Building wheels for collected packages: aiact-triage
2026-08-27T10:56:58.8599531Z   Building wheel for aiact-triage (pyproject.toml): started
2026-08-27T10:56:59.0373950Z   Building wheel for aiact-triage (pyproject.toml): finished with status 'done'
2026-08-27T10:56:59.0394253Z   Created wheel for aiact-triage: filename=aiact_triage-0.5.0-py3-none-any.whl size=32394 sha256=096d0f0637a17dd0c0f8c6fef294552053cedde127f2f61be2a51e49d545404b
2026-08-27T10:56:59.0395945Z   Stored in directory: /tmp/pip-ephem-wheel-cache-43afq2rc/wheels/c4/37/69/a411c0add45a4a33c56439db91e9849df874ab00ac36e6d496
2026-08-27T10:56:59.0410687Z Successfully built aiact-triage
2026-08-27T10:56:59.0579446Z Installing collected packages: aiact-triage
2026-08-27T10:56:59.0742110Z Successfully installed aiact-triage-0.5.0
2026-08-27T10:56:59.1472459Z packaged data ok
=== 1_test (3.12).txt: sed -n '/##\[group\]Run pip uninstall -y aiact-triage/,/Z packaged data ok$/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:57:00.0985128Z ##[group]Run pip uninstall -y aiact-triage
2026-08-27T10:57:00.0985516Z ^[[36;1mpip uninstall -y aiact-triage^[[0m
2026-08-27T10:57:00.0985813Z ^[[36;1mpip install .^[[0m
2026-08-27T10:57:00.0986274Z ^[[36;1mcd /tmp && python -c "import aiact_triage.rules as r; r.timeline(); print('packaged data ok')"^[[0m
2026-08-27T10:57:00.1030405Z shell: /usr/bin/bash -e {0}
2026-08-27T10:57:00.1030681Z env:
2026-08-27T10:57:00.1030964Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:57:00.1031725Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib/pkgconfig
2026-08-27T10:57:00.1032174Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:57:00.1032558Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:57:00.1032929Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:57:00.1033298Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib
2026-08-27T10:57:00.1033624Z ##[endgroup]
2026-08-27T10:57:00.4136578Z Found existing installation: aiact-triage 0.5.0
2026-08-27T10:57:00.4162825Z Uninstalling aiact-triage-0.5.0:
2026-08-27T10:57:00.4532219Z   Successfully uninstalled aiact-triage-0.5.0
2026-08-27T10:57:00.8105463Z Processing ./.
2026-08-27T10:57:00.8121817Z   Installing build dependencies: started
2026-08-27T10:57:01.3373135Z   Installing build dependencies: finished with status 'done'
2026-08-27T10:57:01.3379542Z   Getting requirements to build wheel: started
2026-08-27T10:57:01.8183191Z   Getting requirements to build wheel: finished with status 'done'
2026-08-27T10:57:01.8193382Z   Preparing metadata (pyproject.toml): started
2026-08-27T10:57:02.0146936Z   Preparing metadata (pyproject.toml): finished with status 'done'
2026-08-27T10:57:02.0170431Z Building wheels for collected packages: aiact-triage
2026-08-27T10:57:02.0178186Z   Building wheel for aiact-triage (pyproject.toml): started
2026-08-27T10:57:02.2390555Z   Building wheel for aiact-triage (pyproject.toml): finished with status 'done'
2026-08-27T10:57:02.2396999Z   Created wheel for aiact-triage: filename=aiact_triage-0.5.0-py3-none-any.whl size=32394 sha256=3c72d84e6e525ac93ca7783915d30d8ff6e082cb7da20a9a72f844a890eb86d8
2026-08-27T10:57:02.2398579Z   Stored in directory: /tmp/pip-ephem-wheel-cache-4trqonub/wheels/51/da/47/67f32f63cb9a4c8f44aa95930ab19be9eff3286fdb5e8c2441
2026-08-27T10:57:02.2424257Z Successfully built aiact-triage
2026-08-27T10:57:02.2584518Z Installing collected packages: aiact-triage
2026-08-27T10:57:02.2765776Z Successfully installed aiact-triage-0.5.0
2026-08-27T10:57:02.3585744Z packaged data ok
```

**Executed.** 2026-10-11, 12:36 BST (final capture run; a run at 12:35 ended
the `sed` range at the echoed command line instead of the step's output and
was corrected to the `Z packaged data ok$` anchor shown; a run at 12:36
differed only in how escape bytes were shown).

**Conclusion.** Operating effectively: on both legs the step uninstalled the editable package, built and installed a non-editable wheel, and printed "packaged data ok" after importing `aiact_triage.rules` and calling `timeline()` from `/tmp`, and `steps.tsv` records step 6 as success on both.
