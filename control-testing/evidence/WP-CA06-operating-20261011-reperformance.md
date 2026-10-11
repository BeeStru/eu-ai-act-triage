# WP-CA06-operating-20261011-reperformance

**Control.** CA-06, zero-runtime-dependency policy.

**Test method and reason.** Reperformance, per PLAN.md section 4, because the
control's operation is directly executable: a clean non-editable install
either carries runtime dependencies or it does not. Clean venv,
`pip install .`, `pip freeze` captured. This is the reperformance half of
CA-06's operating test; the automated half, extending the proof across
Python 3.11 and 3.12 from CI run 33065206756, is WP-CA06-operating-20261011.
The filename carries the `-reperformance` suffix per B. Struve's ruling 5 of
11 October 2026. Deviations: (1) the venv is created in the session
scratchpad (`<SCRATCH>/ca06r`) rather than `/tmp/ca06` as in the
TEMPLATES.md worked example; (2) it is a second venv, separate from the
CA-05 reperformance venv, because a venv that already holds pytest could not
show a clean freeze; an empty `pip freeze` before the install is captured to
evidence the starting state.

**Population and regime.** Not applicable; single reperformance in a clean
environment, extended across Python 3.11 and 3.12 by cross-reference to
WP-CA06-operating-20261011. Object under test: fresh clone taken at
2026-10-11 11:59:55 UTC, `main` at `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`.

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
S=<SCRATCH>
cd repo_under_test
echo "=== git log -1 --format='%H' ==="; git log -1 --format='%H'
rm -rf $S/ca06r
echo "=== python3 -m venv <SCRATCH>/ca06r && source <SCRATCH>/ca06r/bin/activate ==="
python3 -m venv $S/ca06r && source $S/ca06r/bin/activate; echo "EXIT: $?"
echo "=== python --version; pip freeze (before install) ==="; python --version; pip freeze; echo "(end of freeze)"
echo "=== pip install . ==="; pip install .; echo "EXIT: $?"
echo "=== pip freeze ==="; pip freeze; echo "EXIT: $?"
echo "=== pip show aiact-triage | grep -E '^(Name|Version|Requires|Location):' ==="
pip show aiact-triage | grep -E '^(Name|Version|Requires|Location):' | sed "s|$S|<SCRATCH>|"
deactivate
```

**Evidence.**
```
=== git log -1 --format='%H' ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
=== python3 -m venv <SCRATCH>/ca06r && source <SCRATCH>/ca06r/bin/activate ===
EXIT: 0
=== python --version; pip freeze (before install) ===
Python 3.14.4
(end of freeze)
=== pip install . ===
Processing /home/bastian/agents/work/control-assurance-pack/repo_under_test
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: aiact-triage
  Building wheel for aiact-triage (pyproject.toml): started
  Building wheel for aiact-triage (pyproject.toml): finished with status 'done'
  Created wheel for aiact-triage: filename=aiact_triage-0.5.0-py3-none-any.whl size=32394 sha256=b6aa5839ce0f33cce804ca33c9a0c0a970f9b8d30a3db60b4af68da3cb83fe13
  Stored in directory: /tmp/pip-ephem-wheel-cache-k5xlhf3w/wheels/e1/d8/69/74654a6aadb39dcb0445372817b17cad0f300833d7025ef67e
Successfully built aiact-triage
Installing collected packages: aiact-triage
Successfully installed aiact-triage-0.5.0
EXIT: 0
=== pip freeze ===
aiact-triage @ file:///home/bastian/agents/work/control-assurance-pack/repo_under_test
EXIT: 0
=== pip show aiact-triage | grep -E '^(Name|Version|Requires|Location):' ===
Name: aiact-triage
Version: 0.5.0
Location: <SCRATCH>/ca06r/lib/python3.14/site-packages
Requires: 
```

**Executed.** 2026-10-11, 13:06 BST.

**Conclusion.** Operating effectively: from an empty venv, `pip install .` installed `aiact-triage` alone, `pip freeze` afterwards lists only the package itself, and `pip show` reports an empty `Requires:`, consistent with the README claim and `dependencies = []`.
