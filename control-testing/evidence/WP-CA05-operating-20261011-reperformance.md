# WP-CA05-operating-20261011-reperformance

**Control.** CA-05, test suite covering the classification gates, with a regression file.

**Test method and reason.** Reperformance, per PLAN.md section 4, the fitting
method for an executable detective control: fresh clone, fresh venv,
`pip install -e ".[dev]"`, `pytest -q`, full output captured. This is the
reperformance half of CA-05's operating test; the automated half, the
`pytest -q` step in CI run 33065206756, is WP-CA05-operating-20261011. The
filename carries the `-reperformance` suffix per B. Struve's ruling 5 of
11 October 2026. Deviation: the venv is created in the session scratchpad
(`<SCRATCH>/ca05r`) rather than as `.venv` in the clone, as in sessions one
and two. Environment note: the local interpreter is Python 3.14.4, which
satisfies `requires-python >=3.11` but lies outside the CI matrix of 3.11
and 3.12; the CI run covers those two.

**Population and regime.** Not applicable; single reperformance of the full
suite in a clean environment. Object under test: fresh clone taken at
2026-10-11 11:59:55 UTC, `main` at `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`,
working tree clean before the run (0 lines from `git status --short`).

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
S=<SCRATCH>
cd repo_under_test
echo "=== git log -1 --format='%H'; git status --short | wc -l ==="; git log -1 --format='%H'; git status --short | wc -l
rm -rf $S/ca05r
echo "=== python3 -m venv <SCRATCH>/ca05r && source <SCRATCH>/ca05r/bin/activate ==="
python3 -m venv $S/ca05r && source $S/ca05r/bin/activate; echo "EXIT: $?"
echo "=== python --version; which python ==="; python --version; which python | sed "s|$S|<SCRATCH>|"
echo "=== pip install -e \".[dev]\" ==="; pip install -e ".[dev]"; echo "EXIT: $?"
echo "=== pytest -q ==="; pytest -q; echo "EXIT: $?"
echo "=== pip freeze ==="; pip freeze | sed "s|$S|<SCRATCH>|"
deactivate
```

**Evidence.**
```
=== git log -1 --format='%H'; git status --short | wc -l ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
0
=== python3 -m venv <SCRATCH>/ca05r && source <SCRATCH>/ca05r/bin/activate ===
EXIT: 0
=== python --version; which python ===
Python 3.14.4
<SCRATCH>/ca05r/bin/python
=== pip install -e ".[dev]" ===
Obtaining file:///home/bastian/agents/work/control-assurance-pack/repo_under_test
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Collecting pytest>=8 (from aiact-triage==0.5.0)
  Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
Collecting iniconfig>=1.0.1 (from pytest>=8->aiact-triage==0.5.0)
  Downloading iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging>=22 (from pytest>=8->aiact-triage==0.5.0)
  Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest>=8->aiact-triage==0.5.0)
  Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pygments>=2.7.2 (from pytest>=8->aiact-triage==0.5.0)
  Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
Downloading iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Downloading packaging-26.3-py3-none-any.whl (129 kB)
Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 4.6 MB/s eta 0:00:00
Building wheels for collected packages: aiact-triage
  Building editable for aiact-triage (pyproject.toml): started
  Building editable for aiact-triage (pyproject.toml): finished with status 'done'
  Created wheel for aiact-triage: filename=aiact_triage-0.5.0-0.editable-py3-none-any.whl size=7356 sha256=212c4dbafac4aba95c075de56ea3eb67458290a8fb5db9bf465b3c49955078c7
  Stored in directory: /tmp/pip-ephem-wheel-cache-0eijfw3o/wheels/e1/d8/69/74654a6aadb39dcb0445372817b17cad0f300833d7025ef67e
Successfully built aiact-triage
Installing collected packages: pygments, pluggy, packaging, iniconfig, aiact-triage, pytest

Successfully installed aiact-triage-0.5.0 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
EXIT: 0
=== pytest -q ===
......................................                                   [100%]
38 passed in 0.11s
EXIT: 0
=== pip freeze ===
-e git+https://github.com/beestru/eu-ai-act-triage@7aab9f95065f9cf69cbdefe5a9aed64c361386ce#egg=aiact_triage
iniconfig==2.3.1
packaging==26.3
pluggy==1.6.0
Pygments==2.21.0
pytest==9.1.1
```

**Executed.** 2026-10-11, 13:05 BST.

**Conclusion.** Operating effectively: in a fresh venv the editable install succeeded and `pytest -q` passed 38 of 38 tests, the same count collected in WP-CA05-design-20261011 and passed on both CI legs in WP-CA05-operating-20261011.
