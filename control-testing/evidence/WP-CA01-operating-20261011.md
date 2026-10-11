# WP-CA01-operating-20261011

**Control.** CA-01, version control over all source, rule data and documentation.

**Test method and reason.** Inspection of the full commit population, per
PLAN.md section 4, because the discipline half of this control is manual and
its operation is visible only in what the history records: consistent author
identity across every commit, and no evidence of history rewriting on `main`.
History rewriting is tested two ways, per B. Struve's instruction for this
session: the committed repository activity feed
(`WP-CA03-operating-20261011-activity.jsonl`, captured outside the sandbox
by B. Struve on 11 October 2026, capture recorded in
`WP-CA03-operating-20261011-capture-commands.txt`) for force pushes and for
breaks in the before/after chain of pushes, and the stability of tag targets
against two external records, the push "after" SHAs in that feed and the
head SHAs GitHub recorded for the tag-ref CI runs
(`WP-CA03-operating-20261011-runs.json`). Deviations: (1) the population is
45 commits, above the 25 at which PLAN.md section 5 prescribes a haphazard
sample of 25; it was tested in full, as section 4 ("the full commit
population") and B. Struve's instruction for this session both require, and
a full scripted test of 45 covers any sample of 25; (2) the `gh api .../events`
route PLAN.md mentions "if useful" returned no records (outside its retention
window, per the capture-commands file), so the activity feed stands in for
it. No venv was created.

**Population and regime.** Manual regime, full population: all 45 commits on
`main` at `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`, 2026-07-12 to
2026-08-27; all 11 activity records (10 pushes, 1 branch creation); all
5 tags. Object under test: a fresh clone of
`https://github.com/beestru/eu-ai-act-triage` taken at 2026-10-11
11:59:55 UTC for fieldwork session three.

**Procedure executed.** Run from the pack directory. Helper script,
reproduced in full:
```
"""CA-01 history-rewrite check. Usage: python3 -I history_check.py REPO ACTIVITY_JSONL RUNS_JSON"""
import json, subprocess, sys
repo, act, runs_path = sys.argv[1:4]
def git(*a):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()
rows = sorted((json.loads(l) for l in open(act) if l.strip()), key=lambda r: r["timestamp"])
print("activity types:", {t: sum(r["activity_type"] == t for r in rows) for t in sorted({r["activity_type"] for r in rows})})
print("force_push records:", sum(r["activity_type"] == "force_push" for r in rows))
prev = None
for n, r in enumerate(rows, 1):
    chain = "first record" if prev is None else ("continuous" if r["before"] == prev else "BREAK")
    anc = git("merge-base", "--is-ancestor", r["after"], "HEAD")[0] == 0
    print(f"{n:>2} {r['timestamp']} {r['activity_type']:<15} before={r['before'][:7]} after={r['after'][:7]} chain={chain} after_reachable_from_HEAD={anc}")
    prev = r["after"]
afters = {r["after"]: n for n, r in enumerate(rows, 1)}
runs = json.load(open(runs_path))
print()
for t in git("tag", "-l")[1].split():
    typ = git("cat-file", "-t", t)[1]
    obj = git("rev-parse", t)[1]
    target = git("rev-parse", t + "^{commit}")[1]
    tagger = git("for-each-ref", "--format=%(taggerdate:iso)", "refs/tags/" + t)[1]
    run_heads = sorted({r["headSha"] for r in runs if r["headBranch"] == t})
    print(f"{t} type={typ} object={obj[:7]} target={target[:7]} tagger_date={tagger} "
          f"target_is_push_after=#{afters.get(target, 'none')} tag_run_head={','.join(h[:7] for h in run_heads) or 'no tag run'} "
          f"match={'yes' if run_heads == [target] else ('n/a' if not run_heads else 'NO')}")
```
Capture script, reproduced in full:
```
S=<SCRATCH>
E=evidence
cd repo_under_test
echo "=== git log -1 --format='%H'; git rev-list --count HEAD ==="; git log -1 --format='%H'; git rev-list --count HEAD
echo "=== git log --reverse --date=iso --format='%h | %an <%ae> | %cn <%ce> | %ad | %s' ==="
git log --reverse --date=iso --format='%h | %an <%ae> | %cn <%ce> | %ad | %s' | nl -w2 -s'. '
echo "=== git log --format='%ae' | sort | uniq -c ==="; git log --format='%ae' | sort | uniq -c
echo "=== git log --format='%an' | sort | uniq -c ==="; git log --format='%an' | sort | uniq -c
echo "=== git log --format='%H | %an | %cn <%ce> | %ad | %s' --date=iso --author='^BeeStru ' ==="
git log --format='%H | %an | %cn <%ce> | %ad | %s' --date=iso --author='^BeeStru '
echo "=== git log --format='%G?' | sort | uniq -c ==="; git log --format='%G?' | sort | uniq -c
cd ..
echo "=== python3 -I history_check.py repo_under_test activity.jsonl runs.json ==="
python3 -I $S/scripts/history_check.py repo_under_test $E/WP-CA03-operating-20261011-activity.jsonl $E/WP-CA03-operating-20261011-runs.json
echo "=== activity actor per record (login, id) ==="
python3 -I -c 'import json,sys,collections; print(collections.Counter((json.loads(l)["actor"]["login"], json.loads(l)["actor"]["id"]) for l in open(sys.argv[1]) if l.strip()))' $E/WP-CA03-operating-20261011-activity.jsonl
```

**Evidence.**
```
=== git log -1 --format='%H'; git rev-list --count HEAD ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
45
=== git log --reverse --date=iso --format='%h | %an <%ae> | %cn <%ce> | %ad | %s' ===
 1. f12964c | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-12 16:39:25 +0100 | Add licence, gitignore and stub README
 2. 13d22df | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 18:06:01 +0100 | Add timeline.json: AI Act application dates, original and Omnibus-amended
 3. 967eb5f | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 18:29:50 +0100 | Add prohibitions.json: Article 5 prohibited practices
 4. d24953d | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 18:58:09 +0100 | Add annex_iii.json: high-risk areas and the Article 6(3) derogation
 5. fb8025d | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 21:20:13 +0100 | Add package skeleton and data models
 6. cf8cfe2 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 21:22:36 +0100 | Add rules loader
 7. 5d17cb0 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 21:37:44 +0100 | Add transparency.json: Article 50 transparency duties
 8. 6dd3010 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-14 21:44:51 +0100 | Add obligations.json: deployer and provider duty texts
 9. 29f0612 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 12:29:31 +0100 | Add classification engine with worked-case tests
10. f08bb5a | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 12:40:12 +0100 | Add command-line interface
11. 28d0269 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 12:40:12 +0100 | Add worked example cases
12. dd2ed85 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 12:52:37 +0100 | Fail closed on unknown prohibited-practice ids
13. 0271732 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 12:55:59 +0100 | Release 0.1.0
14. a521803 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 13:06:06 +0100 | Add register mode: batch assessment over an AI inventory
15. c630923 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 13:12:06 +0100 | Mark held rows in the portfolio tier list
16. 48330a5 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 13:13:59 +0100 | Release 0.2.0
17. b31dea3 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 13:29:49 +0100 | Add cross-framework layer: SS1/23, DORA, ISO 42001 and GDPR flags
18. a5bd0de | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 13:47:39 +0100 | Add SS1/23-vocabulary AI inventory template with field definitions
19. c36e8f2 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 14:59:23 +0100 | Add third-party AI due-diligence questionnaire
20. f091952 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 14:59:39 +0100 | Add design specification for the governed LLM intake assistant
21. 66bb1f6 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:03:11 +0100 | Release 0.3.0
22. 5e14f67 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:15:19 +0100 | Add regression suite for the pre-release review behaviours
23. 73fd4b0 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:15:51 +0100 | Add CI: tests on Python 3.11 and 3.12 with a non-editable install check
24. a30bc34 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:24:38 +0100 | Bump CI actions to current majors on the Node 24 runtime
25. d7b6766 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:44:29 +0100 | Add the full README, replacing the construction stub
26. 73eae06 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 15:58:45 +0100 | Add the methodology and classification framework document
27. a99b308 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 16:13:30 +0100 | Pin the prohibited-hold obligations baseline
28. 83d704c | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-07-15 16:17:47 +0100 | Release 0.4.0
29. 82aef37 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:33:00 +0100 | Align the timeline with the published Digital Omnibus
30. 786e836 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:33:19 +0100 | Align the NCII/CSAM prohibition entry with the OJ text
31. 13bc1df | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:33:32 +0100 | Align the transparency status block with the published Omnibus
32. 4c24e69 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:33:47 +0100 | Align the AI literacy entry with the in-force Article 4
33. 8763405 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:50:48 +0100 | Align the code output strings with the in-force Omnibus
34. f2ac83b | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:51:12 +0100 | Drop radio equipment from the Annex I question's examples
35. 6be39f8 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 09:55:07 +0100 | Update the document sources and promises to the published Omnibus
36. acb9e80 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 10:15:25 +0100 | Recast the dual-date rationale for the in-force Omnibus
37. 273f62f | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 10:15:57 +0100 | Drop radio equipment from the methodology's Annex I examples
38. 32eff43 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 10:15:57 +0100 | Update the questionnaire's date-source note to the published Omnibus
39. f817735 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-04 10:16:31 +0100 | Release 0.5.0
40. 5e0a019 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-27 11:36:04 +0100 | Disclose the Annex I Section B limitation in the scope and known limits
41. 234bc09 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-27 11:36:23 +0100 | Clarify the README for a first-time reader
42. 91ce9bc | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-27 11:36:38 +0100 | Make the quickstart survive PEP 668 and keep the clone clean
43. db46969 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-27 11:36:38 +0100 | Drop the build month from the LLM component design status
44. 8771a60 | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | Bastian Struve <163428440+BeeStru@users.noreply.github.com> | 2026-08-27 11:47:28 +0100 | Correct the test docstring's account of how dates are pinned
45. 7aab9f9 | BeeStru <163428440+BeeStru@users.noreply.github.com> | GitHub <noreply@github.com> | 2026-08-27 11:56:45 +0100 | Update README.md
=== git log --format='%ae' | sort | uniq -c ===
     45 163428440+BeeStru@users.noreply.github.com
=== git log --format='%an' | sort | uniq -c ===
     44 Bastian Struve
      1 BeeStru
=== git log --format='%H | %an | %cn <%ce> | %ad | %s' --date=iso --author='^BeeStru ' ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce | BeeStru | GitHub <noreply@github.com> | 2026-08-27 11:56:45 +0100 | Update README.md
=== git log --format='%G?' | sort | uniq -c ===
      1 E
     44 N
=== python3 -I history_check.py repo_under_test activity.jsonl runs.json ===
activity types: {'branch_creation': 1, 'push': 10}
force_push records: 0
 1 2026-07-14T18:06:35Z branch_creation before=0000000 after=d24953d chain=first record after_reachable_from_HEAD=True
 2 2026-07-15T11:58:07Z push            before=d24953d after=0271732 chain=continuous after_reachable_from_HEAD=True
 3 2026-07-15T12:14:01Z push            before=0271732 after=48330a5 chain=continuous after_reachable_from_HEAD=True
 4 2026-07-15T14:03:12Z push            before=48330a5 after=66bb1f6 chain=continuous after_reachable_from_HEAD=True
 5 2026-07-15T14:15:52Z push            before=66bb1f6 after=73fd4b0 chain=continuous after_reachable_from_HEAD=True
 6 2026-07-15T14:24:39Z push            before=73fd4b0 after=a30bc34 chain=continuous after_reachable_from_HEAD=True
 7 2026-07-15T15:18:31Z push            before=a30bc34 after=83d704c chain=continuous after_reachable_from_HEAD=True
 8 2026-08-04T09:22:11Z push            before=83d704c after=f817735 chain=continuous after_reachable_from_HEAD=True
 9 2026-08-27T10:41:58Z push            before=f817735 after=db46969 chain=continuous after_reachable_from_HEAD=True
10 2026-08-27T10:47:30Z push            before=db46969 after=8771a60 chain=continuous after_reachable_from_HEAD=True
11 2026-08-27T10:56:45Z push            before=8771a60 after=7aab9f9 chain=continuous after_reachable_from_HEAD=True

v0.1.0 type=tag object=98ee8dd target=0271732 tagger_date=2026-07-15 12:55:59 +0100 target_is_push_after=#2 tag_run_head=no tag run match=n/a
v0.2.0 type=tag object=8d55060 target=48330a5 tagger_date=2026-07-15 13:13:59 +0100 target_is_push_after=#3 tag_run_head=no tag run match=n/a
v0.3.0 type=tag object=5592cf1 target=66bb1f6 tagger_date=2026-07-15 15:03:11 +0100 target_is_push_after=#4 tag_run_head=no tag run match=n/a
v0.4.0 type=tag object=92a56f2 target=83d704c tagger_date=2026-07-15 16:17:47 +0100 target_is_push_after=#7 tag_run_head=83d704c match=yes
v0.5.0 type=tag object=277782f target=f817735 tagger_date=2026-08-04 10:16:31 +0100 target_is_push_after=#8 tag_run_head=f817735 match=yes
=== activity actor per record (login, id) ===
Counter({('BeeStru', 163428440): 11})
```

What the output shows.

Author identity, as found. One account address on all 45 commits:
`163428440+BeeStru@users.noreply.github.com`, the GitHub no-reply address of
account 163428440. Two display names on that address:
- `Bastian Struve`: 44 commits, numbers 1 to 44 in the listing above,
  `f12964c` to `8771a60`, each committed under the same name and address.
- `BeeStru`: 1 commit, number 45, `7aab9f95065f9cf69cbdefe5a9aed64c361386ce`
  "Update README.md", 2026-08-27 11:56:45 +0100, committer
  `GitHub <noreply@github.com>`, the signature of an edit made in the GitHub
  web interface. It is also the only commit carrying a signature (`%G?` = `E`,
  a signature whose key is not available locally to check); the other 44 are
  unsigned (`N`).
The activity feed attributes all 11 pushes, including the push that carried
`7aab9f9` (record 11), to one actor, login `BeeStru`, id 163428440, the same
account the address names.

Classification against "consistent author identity", and the reasoning.
The criterion serves the control's objective that every change be
attributable. Attribution in git and on GitHub resolves through the address,
and here the address is a no-reply address bound to a single account id,
identical on all 45 commits and matching the push actor on every push. The
display name is free text: the web-interface commit carries the account's
login, `BeeStru`, where the 44 locally made commits carry the name
`Bastian Struve`, and the variance identifies nobody new. Read that way, identity is consistent and every commit is
attributable to the one account. The stricter reading, that identity is the
name and address pair, would make commit 45 a variance; it is not adopted,
because the pair's name half carries no attribution weight the address does
not already carry, and the variance is recorded in full above rather than
dropped. The same commit's route, an edit made directly to `main` in the web
interface, is possible because no branch protection exists (CA-02); it is
CA-02's condition, not CA-01's.

History rewriting. The feed holds no `force_push` record (types: 10 `push`,
1 `branch_creation`). Every push's "before" equals the previous push's
"after", so the chain from the branch creation to `7aab9f9` is unbroken, and
every pushed "after" is an ancestor of the current HEAD. All five tags are
annotated (`type=tag`). Each tag's target equals the "after" of the push
that published its release (pushes 2, 3, 4, 7 and 8), and for the two tags
that triggered CI runs, GitHub's recorded head SHA for the tag-ref run on
15 July and 4 August equals the target today. No evidence of rewriting.

**Executed.** 2026-10-11, 13:01 BST.

**Conclusion.** Operating effectively: all 45 commits carry one account address that resolves to the single account behind every push, with the one display-name variance (`7aab9f9`, web interface) recorded and assessed above, and neither the activity feed nor the tag targets show any history rewriting.
