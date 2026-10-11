# phase4-reperformance-20261011: reperformance of every workpaper command

Before publication, B. Struve re-ran every command in every 20261011
workpaper himself, outside the testing environment, on 11 October 2026, from
a checklist that reproduces each workpaper's commands. The AI assistant,
Claude Code, compared the new output with each workpaper and wrote the
comparison below; B. Struve reviewed that comparison and made the ruling it
records. This file is made from his results log and that comparison. The
checklist, the run log and the saved outputs it cites are kept in the
author's local working directory and are not published here.

## Results log, as B. Struve recorded it

Sections 0, 1.1 and 1.2 were run one block at a time and logged here; the
remaining sections were run in file order from one command.

```
2026-10-11 15:33 | 0 | match | set-up; ls-remote main at 22ad85f
2026-10-11 15:34 | 1.1 | match | 
2026-10-11 15:45 | 1.2 | match |
```

## Comparison

Written 11 October 2026 by the AI assistant (Claude Code), from B. Struve's
saved output of the same day. B. Struve re-ran every block outside the
sandbox: sections 0, 1.1 and 1.2 one block at a time (`phase4/results.txt`),
every remaining block in file order from one command (`phase4/runall.log`,
15:45:51 to 15:46:58). The assistant ran no checklist block. It compared each
`phase4/<workpaper>/output*.txt` with the workpaper's evidence lines by
`diff`, recomputed from the saved files for every section that has a range to
compare (22 diffs; every result agrees with the diff-aid output in
`runall.log` where one was logged), and read the remaining outputs against the
Compare entries of `drafts/REPERFORMANCE.md` (a3a4ba5).

## Result

Every Compare value in every section matches. Two sections, 7.1 and
10.1, also show a difference that their May-differ entries do not name: the
link count of a parent directory in an `ls -la` listing. Under the
checklist's own definition ("every difference is one the section or the
general lists name") those two rows are not a match, so publication was held
for a ruling. Ruling needed: see "Differences outside May-differ" below.

## Ruling, 11 October 2026

B. Struve's ruling of 11 October 2026, after reading this comparison: every
difference listed below is accepted as covered. The link counts in 7.1 and
10.1 come from build directories that earlier sections left in the shared
clone; the tracked files match. The editable wheel size in 5.1 and 5.3 comes
from the longer source path. The one-line protection response in 2.1 is gh's
output format when piped. No section is a mismatch. The four steps listed
under "Not reperformed as written" stand as listed.

## Per section

Line numbers are evidence lines in the named workpaper unless stated.

| Section | Workpaper | Result | Values compared | Differences, and what covers them | Not compared |
|---|---|---|---|---|---|
| 0 | Set-up | Match on B. Struve's record | No saved output; corroborated by later outputs: first clone HEAD `7aab9f9...` (1.1 output line 1; 5.3 output, status count `0`), second clone HEAD `22ad85f...` with `0` (11.1 and 11.2 outputs, identical to WP-CA07-remediation line 76 and WP-CA08-remediation lines 182 to 183). gh calls in 2.1, 3.2, 10.1 and 11.2 all returned data. | None seen | The block was not teed, so `git ls-remote`, `python3 --version`, `gh --version` and `gh auth status` were not saved. results.txt records `main` at `22ad85f`. |
| 1.1 | WP-CA01-design-20261011 | Match | Diff against lines 48 to 160: HEAD line, `45`, five tags, author and committer counts (44 and 1), the 31 tracked paths, `Successfully installed aiact-triage-0.5.0`, `Version: 0.5.0`, empty `Requires:`, the `Files:` list, `RECONCILED: no differences`, all identical. Non-editable wheel size `32394` identical. | `===` headers and `EXIT: 0` absent; `Processing` and `Location` paths; wheel `sha256`; `pip-ephem-wheel-cache` name. All named (general list; section list). | None |
| 1.2 | WP-CA01-operating-20261011 | Match | Diff against lines 86 to 166: no differences. `7aab9f9...`, `45`, the 45-commit listing, `1 E` and `44 N`, the history check rows and tag lines, `('BeeStru', 163428440): 11`. | None | None |
| 2.1 | WP-CA02-design-20261011 | Match | Protection endpoint: `"message":"Branch not protected"`, `"status":"404"`, then `gh: Branch not protected (HTTP 404)` (lines 41 to 46); `exit 1`, the expected non-zero. Rulesets and branch rules `[]` with `exit 0`, both (`WP-CA02-design-20261011-rulesets.txt` lines 3 and 5). | The JSON is printed on one line here and indented over five lines in the workpaper (gh indents only when writing to a terminal; the rerun was teed). Same keys, same values. Read as the same response; see note 2. | Screenshot page not re-opened (see "Not reperformed as written"). |
| 2.2 | WP-CA02-operating-20261011 | n/a, no command | `9b60dc2` printed; pack log shows both basis files committed (`4c63f22` and `9b60dc2`). | None | None |
| 3.1 | WP-CA03-design-20261011 | Match | Diff against lines 28 to 57: `tests.yml`, 611 bytes; file text identical. | `===` headers absent; `ls -la` times. Named. | None |
| 3.2 | WP-CA03-operating-20261011 | Match | Block 1: five `exit 0`; events feed `1` record. Comparison aid: activity `11 of 11` unchanged (new capture 12); runs `10` present and identical (new capture 11); `steps.tsv IDENTICAL`; log archive SHA-256 `dc7c15e3...` on both copies (line 207). Block 2, diff against lines 206 to 400: no differences. | Events feed `1` where fieldwork had none (capture-commands line 4): named, the 30-day feed lists the 11 October push. New activity record and run: named. `run-view-log.txt` 0 bytes, as at fieldwork. | Run page screenshot not re-opened. Log archive: same hash, so not expired. |
| 4.1 | WP-CA04-design-20261011 | Match | Last five lines identical to lines 26 to 30; whole output identical to WP-CA03-design lines 34 to 57. | None | None |
| 4.2 | WP-CA04-operating-20261011 | Match | Diff against lines 39 to 107: no differences. | None | None |
| 5.1 | WP-CA05-design-20261011 | Match | Diff against lines 38 to 192: `38 tests collected` and the 38 IDs; four test files at 4182, 6713, 4751, 4494 bytes; README lines 15 and 105 only (the `-i` flag noted in the checklist changes nothing); the four `sed` extracts, all identical. | `===` headers and `EXIT:` lines absent; `Obtaining file://` path; `Using cached` in place of `Downloading` and a different download speed; editable wheel `size=7356` now `7362` and its hash; cache directory; `ls -la` times. Named, except the editable wheel size: see note 1. | None |
| 5.2 | WP-CA05-operating-20261011 | Match | Diff against lines 38 to 68: no differences, timings included. | None | None |
| 5.3 | WP-CA05-operating-20261011-reperformance | Match | Diff against lines 40 to 94: `7aab9f9...` and `0`; `EXIT: 0` three times; `38 passed`; freeze line `-e git+...@7aab9f9...#egg=aiact_triage` and the five dependencies at the same versions, all identical. | `Obtaining file://` path; `Using cached`; editable wheel `size=7356` now `7362` and hash; cache directory; `38 passed in 0.11s` now `0.05s`. Named, except the editable wheel size: see note 1. | None |
| 6.1 | WP-CA06-design-20261011 | Match | Diff against lines 28 to 61: no differences. `dependencies = []`, `dev = ["pytest>=8"]`, README lines 15 and 80. | None | None |
| 6.2 | WP-CA06-operating-20261011 | Match | Diff against lines 45 to 161: no differences. | None | None |
| 6.3 | WP-CA06-operating-20261011-reperformance | Match | Diff against lines 43 to 74: HEAD; empty freeze before install; `Successfully installed aiact-triage-0.5.0` alone, `EXIT: 0`; `Name`, `Version: 0.5.0`, empty `Requires:`, all identical. Wheel size `32394` identical. | `Processing` path; wheel hash; cache directory; `file://` path in the freeze line. Named. | None |
| 7.1 | WP-CA07-design-20261011 | **Not a match by the checklist's definition** | Diff against lines 48 to 162: six data files at 4895, 3501, 3901, 5520, 4219, 3457 bytes; README line 105; the whole of `timeline.json`; `last_verified: 2026-08-04`; `sources: 2`; `milestones: 9`; `9` with provision; the nine provisions, all identical. | `ls -la` times: named. **The `..` line (`src/aiact_triage/`) shows link count `4` where the workpaper shows `3`: not named.** See "Differences outside May-differ". | None |
| 7.2 | WP-CA07-operating-20261011 | Match | Diff against lines 158 to 274: no differences. | None | None |
| 8.1 | WP-CA08-operating-20261011 | Match | Diff against lines 181 to 526: clean-start listing, `7aab9f9...`, `0`; Parts 1 to 4 identical, including `EOFError` and `EXIT: 1` for `interactive < /dev/null`, the piped run ending `Tier:     MINIMAL RISK`, `EXIT: 0`, `38 passed`, both `missing lines: 0`, the four `7 of 7` counts, `30`, `30`, `23`, `18 passed, 20 deselected`, `date lines changed: 0`, and Part 4's `3 failed, 35 passed` with the same three failures. Register assessment date identical (run on the fieldwork date). | Five traceback file paths; `ls -la` times on three tracked files (sizes identical). Named. | Step 2, type by hand: see "Not reperformed as written". |
| 9.1 | WP-CA09-design-20261011 | Match | Block 1, diff against lines 53 to 117: no differences. Block 2, diff against lines 121 to 147: plan lines 1 to 5, `405:- **D5, commit granularity**`, lines 405 to 409 and 75 to 81, count `0`, `EXIT: 1`, all identical. | Block 2: the plan's `ls -la` line, 112,216 bytes at 12:03 now 114,499 bytes at 13:46. Named in the section. | None |
| 9.2 | WP-CA09-operating-20261011 | Match | Diff against lines 49 to 118: no differences. Five tags only. | None | None |
| 10.1 | WP-CA10-design-20261011 | **Not a match by the checklist's definition** | Block 1, diff against lines 59 to 90: `44` and `1` in shortlog; committers 44 and 1; `0` merges; `workflows` only in `.github/`; the grep `EXIT: 1`; `records: 11` and the counter; `runs: 10`, `{'push': 9, 'dynamic': 1}`; the rulesets file; PLAN.md line 70, all identical. Block 2: one contributor, `BeeStru	48`, `exit 0`; pull requests `[]`, `exit 0`. | `ls -la` times: named. **The `..` line (clone root) shows link count `13` where the workpaper shows `9`, and the link-count column of the three `.github/` lines is padded one space wider as a result: not named.** See "Differences outside May-differ". | None |
| 11.1 | WP-CA07-remediation-20261011 | Match | Diff against lines 75 to 159: no differences. Block 2: `1380:(22) Article 57 is amended as follows:` and `1386:national level, which shall be operational by 2 August 2027. ...`. | None | None |
| 11.2 | WP-CA08-remediation-20261011 | Match | Block 1, diff against lines 181 to 240: no differences. Block 2, diff against lines 244 to 321: one difference only. Block 4, diff against lines 325 to 338: no differences. Block 5: three `exit 0`; comparison aid `12 of 12`, `committed runs: 11 present and identical: 11`, `steps.tsv IDENTICAL`. | Block 2: `38 passed in 0.10s` now `0.11s`. Named (general list, pytest timings). | Step 3, type by hand: see "Not reperformed as written". |

## Differences outside May-differ

1. **7.1.** `drwxrwxr-x 3 ... ..` (line 53) now reads `drwxrwxr-x 4 ... ..`.
   The directory is `src/aiact_triage/`. In the rerun clone it holds
   `data/` and an untracked `__pycache__/`, left by the pytest runs of
   sections 5.1 to 5.3 in the shared clone; the fieldwork listing came from a
   fresh clone taken at 11:31:07 UTC (line 18), which had only `data/`. The
   six tracked files' names and sizes are identical.
2. **10.1.** `drwxrwxr-x 9 ... ..` (line 72) now reads
   `drwxrwxr-x 13 ... ..`, and the three lines' link-count column widens by
   one space. The directory is the clone root, which now also holds the
   untracked, gitignored `.pytest_cache/`, `.venv/`, `audit/` and `build/`
   left by earlier sections; the fieldwork listing came from a fresh clone
   (line 23). `.github/` itself still holds only `workflows`.

The section entries name only "`ls -la` dates", and the general list names
"`ls -la` timestamps, owners and directory sizes (file sizes of tracked files
must match)". A link count is none of those. The assistant's reading is that
both differences come from untracked build directories in the shared clone
and change no compared value, but the plan leaves that call to B. Struve, not
to the session. Ruling needed: accept both as covered, or rerun 7.1 and 10.1
on a fresh clone at `7aab9f9`.

## Notes on differences read as covered

1. **Editable wheel size, 5.1 and 5.3.** `size=7356` at fieldwork, `7362` now.
   The general list covers "pip's build details" (naming the hash, the cache
   name and download detail) and absolute paths. An editable wheel records the
   absolute source path, which grew by `phase4/`; the non-editable wheel,
   which records no path, is `32394` bytes at fieldwork and now (1.1, 6.3).
   Read as covered; named here because size is not in the list's examples.
2. **JSON layout, 2.1.** Same keys and values, indented at fieldwork, one
   line now. The Compare entry names values, which match. Read as the same
   response.

## Not reperformed as written

- **8.1, step 2, and 11.2, step 3, type by hand.** Both ran inside the
  single scripted run with no input attached, so `aiact-triage interactive`
  stopped at the first prompt with `EOFError: EOF when reading a line`
  (`runall.log` lines 1564 to 1576 and 2042 to 2054). The interactive walk
  through to `Tier:     MINIMAL RISK` at a real terminal was not done. The
  workpaper's own piped-answer run, inside 8.1 block 1, did reproduce
  identically, ending `Tier:     MINIMAL RISK`, `EXIT: 0`.
- **2.1 and 3.2, browser re-checks.** The settings page
  (`WP-CA02-design-20261011-settings.png`) and the run page
  (`WP-CA03-operating-20261011-run.png`) were not re-opened. Indirect
  corroboration only: the branch-protection and ruleset API responses are
  unchanged, and the run's `steps.tsv` and log archive are identical.

## Not compared

- Section 0's own output (not saved).
- `runall.log` covers sections 2.1 onwards; the diff aids for 1.1 and 1.2
  were not logged, so the assistant computed both diffs from the saved
  output.
