# WP-CA06-operating-20261011

**Control.** CA-06, zero-runtime-dependency policy.

**Test method and reason.** Automated regime for the automated verification
half of CA-06, per PLAN.md sections 4 and 5: CI's matrix extends the
zero-dependency proof across both Python versions, by cross-reference to
CA-03's test-of-one run. Inspected: what pip resolved and installed in
step 4 (`pip install -e ".[dev]"`) and step 6 (`pip install .`) of run
33065206756, both legs. Scope limit, stated: the reperformance PLAN.md
section 4 specifies (clean venv, non-editable `pip install .`, `pip freeze`)
belongs to Phase 2 session three and is not performed here. Limitation of
this evidence: the CI environment at step 6 is not clean, because step 4 has
already installed pytest and its dependencies; a runtime dependency that was
already present would appear as "Requirement already satisfied", and the
search below covers that phrase. Sources:
`WP-CA03-operating-20261011-run-33065206756-logs.zip`, unpacked as recorded
in WP-CA03-operating-20261011, and
`WP-CA03-operating-20261011-run-33065206756-steps.tsv`, captured outside the
sandbox by B. Struve on 11 October 2026 and committed in 9b60dc2. No venv was
created.

**Population and regime.** Automated regime, test of one: steps 4 and 6 of
run 33065206756 on `main` at `7aab9f9`, both matrix legs (CPython 3.11.16
and 3.12.14, per WP-CA03-operating-20261011).

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
L=<SCRATCH>/logs_33065206756
echo "=== step 4 and step 6 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ==="
awk -F'\t' '$2==4 || $2==6' evidence/WP-CA03-operating-20261011-run-33065206756-steps.tsv
cd "$L"
for f in "0_test (3.11).txt" "1_test (3.12).txt"; do
  echo "=== $f: sed -n '/##\[group\]Run pip install -e/,/Successfully installed/p' | sed 's/\x1b/^[/g' ==="
  sed -n '/##\[group\]Run pip install -e/,/Successfully installed/p' "$f" | sed 's/\x1b/^[/g'
  echo "=== $f: grep -n -E 'Collecting|Requirement already satisfied|Installing collected packages|Successfully installed' | sed 's/\x1b/^[/g' ==="
  grep -n -E 'Collecting|Requirement already satisfied|Installing collected packages|Successfully installed' "$f" | sed 's/\x1b/^[/g'
done
```
The final `sed` on each extract shows each escape byte as `^[`.

**Evidence.**
```
=== step 4 and step 6 rows of WP-CA03-operating-20261011-run-33065206756-steps.tsv ===
test (3.12)	4	Run pip install -e ".[dev]"	success
test (3.12)	6	prove non-editable install carries the rule data	success
test (3.11)	4	Run pip install -e ".[dev]"	success
test (3.11)	6	prove non-editable install carries the rule data	success
=== 0_test (3.11).txt: sed -n '/##\[group\]Run pip install -e/,/Successfully installed/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:56:52.4202884Z ##[group]Run pip install -e ".[dev]"
2026-08-27T10:56:52.4204647Z ^[[36;1mpip install -e ".[dev]"^[[0m
2026-08-27T10:56:52.4254520Z shell: /usr/bin/bash -e {0}
2026-08-27T10:56:52.4255806Z env:
2026-08-27T10:56:52.4257152Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:52.4259682Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib/pkgconfig
2026-08-27T10:56:52.4261910Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:52.4264001Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:52.4266090Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.16/x64
2026-08-27T10:56:52.4268390Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.16/x64/lib
2026-08-27T10:56:52.4270223Z ##[endgroup]
2026-08-27T10:56:53.4748203Z Obtaining file:///home/runner/work/eu-ai-act-triage/eu-ai-act-triage
2026-08-27T10:56:53.4763890Z   Installing build dependencies: started
2026-08-27T10:56:54.5059117Z   Installing build dependencies: finished with status 'done'
2026-08-27T10:56:54.5066124Z   Checking if build backend supports build_editable: started
2026-08-27T10:56:54.8091357Z   Checking if build backend supports build_editable: finished with status 'done'
2026-08-27T10:56:54.8096980Z   Getting requirements to build editable: started
2026-08-27T10:56:55.0903482Z   Getting requirements to build editable: finished with status 'done'
2026-08-27T10:56:55.0911594Z   Preparing editable metadata (pyproject.toml): started
2026-08-27T10:56:55.2517740Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-08-27T10:56:55.3566608Z Collecting pytest>=8 (from aiact-triage==0.5.0)
2026-08-27T10:56:55.4066974Z   Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
2026-08-27T10:56:55.4274486Z Collecting iniconfig>=1.0.1 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:55.4312992Z   Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
2026-08-27T10:56:55.4535639Z Collecting packaging>=22 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:55.4571918Z   Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
2026-08-27T10:56:55.5241743Z Collecting pluggy<2,>=1.5 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:55.5278456Z   Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
2026-08-27T10:56:55.5529029Z Collecting pygments>=2.7.2 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:55.5563241Z   Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
2026-08-27T10:56:55.5652730Z Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
2026-08-27T10:56:55.6202026Z Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
2026-08-27T10:56:55.6263298Z Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
2026-08-27T10:56:55.6320775Z Downloading packaging-26.3-py3-none-any.whl (129 kB)
2026-08-27T10:56:55.6381509Z Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
2026-08-27T10:56:55.6632440Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 52.3 MB/s  0:00:00
2026-08-27T10:56:55.6881120Z Building wheels for collected packages: aiact-triage
2026-08-27T10:56:55.6885188Z   Building editable for aiact-triage (pyproject.toml): started
2026-08-27T10:56:55.8705690Z   Building editable for aiact-triage (pyproject.toml): finished with status 'done'
2026-08-27T10:56:55.8711568Z   Created wheel for aiact-triage: filename=aiact_triage-0.5.0-0.editable-py3-none-any.whl size=7336 sha256=bd0655c6ad7b5eb7c51ae5613fb0a90efaa94e2e93cb9278ddd832013f7ff10a
2026-08-27T10:56:55.8713570Z   Stored in directory: /tmp/pip-ephem-wheel-cache-jswtd2gw/wheels/c4/37/69/a411c0add45a4a33c56439db91e9849df874ab00ac36e6d496
2026-08-27T10:56:55.8738971Z Successfully built aiact-triage
2026-08-27T10:56:55.8921699Z Installing collected packages: pygments, pluggy, packaging, iniconfig, aiact-triage, pytest
2026-08-27T10:56:56.6982577Z 
2026-08-27T10:56:56.6993906Z Successfully installed aiact-triage-0.5.0 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
=== 0_test (3.11).txt: grep -n -E 'Collecting|Requirement already satisfied|Installing collected packages|Successfully installed' | sed 's/\x1b/^[/g' ===
151:2026-08-27T10:56:55.3566608Z Collecting pytest>=8 (from aiact-triage==0.5.0)
153:2026-08-27T10:56:55.4274486Z Collecting iniconfig>=1.0.1 (from pytest>=8->aiact-triage==0.5.0)
155:2026-08-27T10:56:55.4535639Z Collecting packaging>=22 (from pytest>=8->aiact-triage==0.5.0)
157:2026-08-27T10:56:55.5241743Z Collecting pluggy<2,>=1.5 (from pytest>=8->aiact-triage==0.5.0)
159:2026-08-27T10:56:55.5529029Z Collecting pygments>=2.7.2 (from pytest>=8->aiact-triage==0.5.0)
173:2026-08-27T10:56:55.8921699Z Installing collected packages: pygments, pluggy, packaging, iniconfig, aiact-triage, pytest
175:2026-08-27T10:56:56.6993906Z Successfully installed aiact-triage-0.5.0 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
218:2026-08-27T10:56:59.0579446Z Installing collected packages: aiact-triage
219:2026-08-27T10:56:59.0742110Z Successfully installed aiact-triage-0.5.0
=== 1_test (3.12).txt: sed -n '/##\[group\]Run pip install -e/,/Successfully installed/p' | sed 's/\x1b/^[/g' ===
2026-08-27T10:56:51.9849947Z ##[group]Run pip install -e ".[dev]"
2026-08-27T10:56:51.9851725Z ^[[36;1mpip install -e ".[dev]"^[[0m
2026-08-27T10:56:51.9934760Z shell: /usr/bin/bash -e {0}
2026-08-27T10:56:51.9935570Z env:
2026-08-27T10:56:51.9936341Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:51.9937751Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib/pkgconfig
2026-08-27T10:56:51.9938992Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:51.9940259Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:51.9941727Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.14/x64
2026-08-27T10:56:51.9942935Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.14/x64/lib
2026-08-27T10:56:51.9943952Z ##[endgroup]
2026-08-27T10:56:55.3932518Z Obtaining file:///home/runner/work/eu-ai-act-triage/eu-ai-act-triage
2026-08-27T10:56:55.3948361Z   Installing build dependencies: started
2026-08-27T10:56:56.4292035Z   Installing build dependencies: finished with status 'done'
2026-08-27T10:56:56.4297603Z   Checking if build backend supports build_editable: started
2026-08-27T10:56:56.8335627Z   Checking if build backend supports build_editable: finished with status 'done'
2026-08-27T10:56:56.8344058Z   Getting requirements to build editable: started
2026-08-27T10:56:57.2059536Z   Getting requirements to build editable: finished with status 'done'
2026-08-27T10:56:57.2068116Z   Preparing editable metadata (pyproject.toml): started
2026-08-27T10:56:57.3997725Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-08-27T10:56:57.5211405Z Collecting pytest>=8 (from aiact-triage==0.5.0)
2026-08-27T10:56:57.5949893Z   Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
2026-08-27T10:56:57.6190198Z Collecting iniconfig>=1.0.1 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:57.6323518Z   Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
2026-08-27T10:56:57.6591544Z Collecting packaging>=22 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:57.6723225Z   Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
2026-08-27T10:56:57.6955985Z Collecting pluggy<2,>=1.5 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:57.7088667Z   Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
2026-08-27T10:56:57.7400236Z Collecting pygments>=2.7.2 (from pytest>=8->aiact-triage==0.5.0)
2026-08-27T10:56:57.7531890Z   Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
2026-08-27T10:56:57.7711849Z Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
2026-08-27T10:56:57.8349767Z Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
2026-08-27T10:56:57.8500067Z Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
2026-08-27T10:56:57.8649785Z Downloading packaging-26.3-py3-none-any.whl (129 kB)
2026-08-27T10:56:57.8814891Z Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
2026-08-27T10:56:57.9226669Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 27.6 MB/s  0:00:00
2026-08-27T10:56:57.9414679Z Building wheels for collected packages: aiact-triage
2026-08-27T10:56:57.9422253Z   Building editable for aiact-triage (pyproject.toml): started
2026-08-27T10:56:58.1620961Z   Building editable for aiact-triage (pyproject.toml): finished with status 'done'
2026-08-27T10:56:58.1626788Z   Created wheel for aiact-triage: filename=aiact_triage-0.5.0-0.editable-py3-none-any.whl size=7336 sha256=6ecb551740eafe7980e9b20d0a50dd4dc95f71f9684b00582d05218c2350d7eb
2026-08-27T10:56:58.1628908Z   Stored in directory: /tmp/pip-ephem-wheel-cache-v5rom8nz/wheels/51/da/47/67f32f63cb9a4c8f44aa95930ab19be9eff3286fdb5e8c2441
2026-08-27T10:56:58.1647684Z Successfully built aiact-triage
2026-08-27T10:56:58.1848247Z Installing collected packages: pygments, pluggy, packaging, iniconfig, aiact-triage, pytest
2026-08-27T10:56:59.3380160Z 
2026-08-27T10:56:59.3393623Z Successfully installed aiact-triage-0.5.0 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
=== 1_test (3.12).txt: grep -n -E 'Collecting|Requirement already satisfied|Installing collected packages|Successfully installed' | sed 's/\x1b/^[/g' ===
151:2026-08-27T10:56:57.5211405Z Collecting pytest>=8 (from aiact-triage==0.5.0)
153:2026-08-27T10:56:57.6190198Z Collecting iniconfig>=1.0.1 (from pytest>=8->aiact-triage==0.5.0)
155:2026-08-27T10:56:57.6591544Z Collecting packaging>=22 (from pytest>=8->aiact-triage==0.5.0)
157:2026-08-27T10:56:57.6955985Z Collecting pluggy<2,>=1.5 (from pytest>=8->aiact-triage==0.5.0)
159:2026-08-27T10:56:57.7400236Z Collecting pygments>=2.7.2 (from pytest>=8->aiact-triage==0.5.0)
173:2026-08-27T10:56:58.1848247Z Installing collected packages: pygments, pluggy, packaging, iniconfig, aiact-triage, pytest
175:2026-08-27T10:56:59.3393623Z Successfully installed aiact-triage-0.5.0 iniconfig-2.3.0 packaging-26.3 pluggy-1.6.0 pygments-2.21.0 pytest-9.1.1
218:2026-08-27T10:57:02.2584518Z Installing collected packages: aiact-triage
219:2026-08-27T10:57:02.2765776Z Successfully installed aiact-triage-0.5.0
```

What the output shows. In step 4 the only requirement pip resolved from the
package was `pytest>=8`, the `dev` extra; the other four packages collected
are pytest's own dependencies. In step 6 (log lines 218 and 219) pip
installed `aiact-triage` alone with no "Collecting" line, and no
"Requirement already satisfied" line appears anywhere in either log. The two legs are identical in
this respect.

**Executed.** 2026-10-11, 12:36 BST (final capture run; earlier runs of the
same script at 12:35 and 12:36 differed only in how escape bytes were
shown).

**Conclusion.** Operating effectively, for the automated half tested here: on Python 3.11 and 3.12 the non-editable install in step 6 installed `aiact-triage` and nothing else, and the only requirement pip resolved from the package in step 4 was the `dev` extra's pytest, consistent with `dependencies = []`.
