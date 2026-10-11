# WP-CA09-operating-20261011

**Control.** CA-09, release versioning discipline.

**Test method and reason.** Inspection of the full tag population, per
PLAN.md section 4: every tag reconciled against the `pyproject.toml` and
`src/aiact_triage/__init__.py` versions at its tagged commit, with tag type
recorded, because a manual release discipline either produced a tag that
matches the shipped version or it did not. Each release commit was also
checked against the documented convention quoted in WP-CA09-design-20261011
(rule D5 and the "Version arc" paragraph of the maintainer's execution
plan): one commit carrying both version-string bumps and the changelog
entry, under an annotated `vX.Y.0` tag. The plan's 0.1.0 release step is
captured below because it bears on the first release. No deviation. No venv
was created.

**Population and regime.** Manual regime, full population: 5 tags, `v0.1.0`
to `v0.5.0`, below the 25 at which PLAN.md section 5 would permit sampling.
Object under test: fresh clone taken at 2026-10-11 11:59:55 UTC, `main` at
`7aab9f95065f9cf69cbdefe5a9aed64c361386ce`. A five-item population is
small, and that limits how persuasive the result is; it is stated, not
padded.

**Procedure executed.** Run from the pack directory as one script, reproduced
in full:
```
cd repo_under_test
echo "=== git log -1 --format='%H' ==="; git log -1 --format='%H'
for t in $(git tag -l); do
  c=$(git rev-parse "$t^{commit}")
  echo "=== $t ==="
  echo "type: $(git cat-file -t $t)   target: $c   subject: $(git log -1 --format=%s $c)"
  git for-each-ref --format='tagger: %(taggername) %(taggerdate:iso)   message: %(contents:subject)' refs/tags/$t
  echo "pyproject.toml at target:   $(git show $c:pyproject.toml | grep '^version')"
  echo "__init__.py at target:      $(git show $c:src/aiact_triage/__init__.py | grep '__version__')"
  echo "pyproject.toml at parent:   $(git show $c^:pyproject.toml 2>/dev/null | grep '^version' || echo 'absent')"
  echo "__init__.py at parent:      $(git show $c^:src/aiact_triage/__init__.py 2>/dev/null | grep '__version__' || echo 'absent')"
  echo "CHANGELOG heading at target: $(git show $c:CHANGELOG.md | grep -m1 "^## ${t#v} " || echo 'none')"
  echo "files changed by the release commit (git show --stat --format= $c):"
  git show --stat --format= $c
done
cd ..
F=~/agents/work/GitHub_project_EU_AI_Act_July_2026/EXECUTION_PLAN.md
echo "=== sed -n 277,280p \$F (the plan's 0.1.0 release step) ==="; sed -n 277,280p $F
```

**Evidence.**
```
=== git log -1 --format='%H' ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
=== v0.1.0 ===
type: tag   target: 0271732d477a51078616e955524c4ec4aba26f95   subject: Release 0.1.0
tagger: Bastian Struve 2026-07-15 12:55:59 +0100   message: First public release: triage engine, CLI, worked examples
pyproject.toml at target:   version = "0.1.0"
__init__.py at target:      __version__ = "0.1.0"
pyproject.toml at parent:   version = "0.1.0"
__init__.py at parent:      __version__ = "0.1.0"
CHANGELOG heading at target: ## 0.1.0 (July 2026)
files changed by the release commit (git show --stat --format= 0271732d477a51078616e955524c4ec4aba26f95):
 CHANGELOG.md | 20 ++++++++++++++++++++
 1 file changed, 20 insertions(+)
=== v0.2.0 ===
type: tag   target: 48330a5a4996b0716d89efbe762876b0578a5cf0   subject: Release 0.2.0
tagger: Bastian Struve 2026-07-15 13:13:59 +0100   message: Register mode: batch inventory assessment, audit records, portfolio summary
pyproject.toml at target:   version = "0.2.0"
__init__.py at target:      __version__ = "0.2.0"
pyproject.toml at parent:   version = "0.1.0"
__init__.py at parent:      __version__ = "0.1.0"
CHANGELOG heading at target: ## 0.2.0 (July 2026)
files changed by the release commit (git show --stat --format= 48330a5a4996b0716d89efbe762876b0578a5cf0):
 CHANGELOG.md                 | 12 ++++++++++++
 pyproject.toml               |  2 +-
 src/aiact_triage/__init__.py |  2 +-
 3 files changed, 14 insertions(+), 2 deletions(-)
=== v0.3.0 ===
type: tag   target: 66bb1f65714138f23de28f63f174f5725d91070d   subject: Release 0.3.0
tagger: Bastian Struve 2026-07-15 15:03:11 +0100   message: Cross-framework layer, inventory template, due-diligence questionnaire, LLM component design
pyproject.toml at target:   version = "0.3.0"
__init__.py at target:      __version__ = "0.3.0"
pyproject.toml at parent:   version = "0.2.0"
__init__.py at parent:      __version__ = "0.2.0"
CHANGELOG heading at target: ## 0.3.0 (July 2026)
files changed by the release commit (git show --stat --format= 66bb1f65714138f23de28f63f174f5725d91070d):
 CHANGELOG.md                 | 11 +++++++++++
 pyproject.toml               |  2 +-
 src/aiact_triage/__init__.py |  2 +-
 3 files changed, 13 insertions(+), 2 deletions(-)
=== v0.4.0 ===
type: tag   target: 83d704ca7c0942d5e85b69f1521042712b038ae3   subject: Release 0.4.0
tagger: Bastian Struve 2026-07-15 16:17:47 +0100   message: Release 0.4.0
pyproject.toml at target:   version = "0.4.0"
__init__.py at target:      __version__ = "0.4.0"
pyproject.toml at parent:   version = "0.3.0"
__init__.py at parent:      __version__ = "0.3.0"
CHANGELOG heading at target: ## 0.4.0 (July 2026)
files changed by the release commit (git show --stat --format= 83d704ca7c0942d5e85b69f1521042712b038ae3):
 CHANGELOG.md                 | 11 +++++++++++
 pyproject.toml               |  2 +-
 src/aiact_triage/__init__.py |  2 +-
 3 files changed, 13 insertions(+), 2 deletions(-)
=== v0.5.0 ===
type: tag   target: f81773505d09bb4f8507300d0660cd77a161787d   subject: Release 0.5.0
tagger: Bastian Struve 2026-08-04 10:16:31 +0100   message: Release 0.5.0
pyproject.toml at target:   version = "0.5.0"
__init__.py at target:      __version__ = "0.5.0"
pyproject.toml at parent:   version = "0.4.0"
__init__.py at parent:      __version__ = "0.4.0"
CHANGELOG heading at target: ## 0.5.0 (August 2026)
files changed by the release commit (git show --stat --format= f81773505d09bb4f8507300d0660cd77a161787d):
 CHANGELOG.md                 | 19 +++++++++++++++++++
 pyproject.toml               |  2 +-
 src/aiact_triage/__init__.py |  2 +-
 3 files changed, 21 insertions(+), 2 deletions(-)
=== sed -n 277,280p $F (the plan's 0.1.0 release step) ===
disposition findings (fixes get their own commits). Then the release commit:
create the repo's `CHANGELOG.md` with the 0.1.0 entry (month filled in),
confirm both version strings read 0.1.0, tag `v0.1.0`, push with
`--follow-tags`. Acceptance: smoke run prints HIGH-RISK with Annex III, 4 and
```

What the output shows.

| Tag | Type | Target | pyproject.toml | `__init__.py` | CHANGELOG heading | Release commit changes |
|---|---|---|---|---|---|---|
| v0.1.0 | annotated | `0271732` | 0.1.0 | 0.1.0 | 0.1.0 (July 2026) | CHANGELOG.md only |
| v0.2.0 | annotated | `48330a5` | 0.2.0 | 0.2.0 | 0.2.0 (July 2026) | CHANGELOG.md, pyproject.toml, `__init__.py` |
| v0.3.0 | annotated | `66bb1f6` | 0.3.0 | 0.3.0 | 0.3.0 (July 2026) | CHANGELOG.md, pyproject.toml, `__init__.py` |
| v0.4.0 | annotated | `83d704c` | 0.4.0 | 0.4.0 | 0.4.0 (July 2026) | CHANGELOG.md, pyproject.toml, `__init__.py` |
| v0.5.0 | annotated | `f817735` | 0.5.0 | 0.5.0 | 0.5.0 (August 2026) | CHANGELOG.md, pyproject.toml, `__init__.py` |

Every tag is annotated, every tag name equals both version strings at its
target, and the changelog at each target carries the matching heading.
Releases 0.2.0 to 0.5.0 each consist of exactly the three files D5 names,
with both strings moving from the previous version. The 0.1.0 release
commit changes only `CHANGELOG.md`: both strings already read 0.1.0 at its
parent, so there was nothing to bump. That is what the convention itself
prescribes for the first release: the version arc starts both strings at
0.1.0, and the plan's 0.1.0 release step reads "create the repo's
`CHANGELOG.md` with the 0.1.0 entry (month filled in), confirm both
version strings read 0.1.0, tag `v0.1.0`". Recorded as found, not counted as
a departure. Each tag's target is also the head of the push that published
it, and the two tag-ref CI runs recorded the same heads
(WP-CA01-operating-20261011), so the tagged tree states have not moved.

**Executed.** 2026-10-11, 13:05 BST (final capture run; a run at 13:04
lacked only the last block, the plan's 0.1.0 release step).

**Conclusion.** Operating effectively: all five tags are annotated and each matches both version strings and the changelog heading at its target, with each release commit taking the form the documented convention prescribes, including the first release, which had no bump to make.
