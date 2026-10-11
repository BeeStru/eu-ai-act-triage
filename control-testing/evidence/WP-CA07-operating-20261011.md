# WP-CA07-operating-20261011

**Control.** CA-07, rule-data citation and verification-date discipline.

**Test method and reason.** Inspection of the full population of rule entries
across `src/aiact_triage/data/`, per PLAN.md section 4, because a manual data
discipline operates or fails entry by entry. Three tests: citation coverage
(criterion 100%); the verification date, tested against the convention the
repository documents; and the Omnibus staleness check. Deviations, six:

1. Verification-date criterion, per B. Struve's ruling 4 of 11 October 2026
   (STATE.md). PLAN.md's "verification date in every file" misdescribes the
   repository's convention. The test is against the convention as README
   line 105 states it: "the rule set's verification date is recorded in the
   timeline data and carried into every audit record." The second limb is
   tested by generating audit records in register mode.
2. Population. 47 rule entries, above the 25 at which PLAN.md section 5
   prescribes a sample; tested in full, as B. Struve's instruction for this
   session requires.
3. Rule entries and their citation fields, as found: `point` for the eight
   Annex III areas, `source` for the Article 6(3) derogation (its four
   conditions are sub-items of that one rule and carry no field of their
   own), `article` for obligations, prohibitions and transparency duties,
   `provision` for timeline milestones. `cross_framework.json` has no
   citation field: its five flags name a `framework`, and any provision
   reference sits in the `note` text, which is where the script looks.
4. The tiering of citation values is a mechanical rule written for this
   test and printed in the script below: "none" where no article, annex,
   chapter, section or principle is named; "grouping" where the value starts
   with "Chapter" or the only reference is "Annex A"; otherwise
   "article-level".
5. Staleness. EUR-Lex was not checked: outbound HTTP is unavailable in this
   sandbox. Per B. Struve's instruction, the check runs from the rule files'
   sources as they stand. The fact of Official Journal publication on
   24 July 2026 rests on the 27 August pre-flight entry in STATE.md and on
   the files' own text.
6. Audit records were generated with the system Python in isolated mode,
   importing the package from `repo_under_test/src`, into a scratchpad
   directory (`<SCRATCH>/ca07_audit`); no venv was created and nothing was
   written to the clone.

Correction to WP-CA07-design-20261011, recorded here because a committed
workpaper is never edited: that workpaper says all nine timeline milestones
"carry a non-empty `provision` citation". All nine are non-empty, but the
`sandboxes` milestone's value, "National AI regulatory sandboxes", names no
provision. The design conclusion, which rests on the convention's structure
being present, is unaffected; the content gap is an operating matter and is
reported below.

**Population and regime.** Manual regime, full population: 47 rule entries in
six files (annex_iii 9, obligations 11, prohibitions 9, timeline 9,
transparency 4, cross_framework 5); six `_meta` blocks; every audit record
produced from `examples/inventory.csv` (7 records and a summary) and from
`templates/ai_inventory_template.csv` (1 record and a summary). Object under
test: fresh clone taken at 2026-10-11 11:59:55 UTC, `main` at
`7aab9f95065f9cf69cbdefe5a9aed64c361386ce`.

**Procedure executed.** Run from the pack directory. Helper script,
reproduced in full:
```
"""CA-07 citation coverage over every rule entry in the data directory.
Usage: python3 -I citations.py DATA_DIR"""
import json, re, sys, os
d = sys.argv[1]
load = lambda f: json.load(open(os.path.join(d, f)))
entries = []  # (file, rule, citation field, value)
a = load("annex_iii.json")
entries += [("annex_iii.json", f"areas/{x['id']}", "point", x.get("point")) for x in a["areas"]]
der = a["art_6_3_derogation"]
entries.append(("annex_iii.json", "art_6_3_derogation", "source", der.get("source")))
o = load("obligations.json")
entries += [("obligations.json", f"high_risk_deployer/{x['id']}", "article", x.get("article")) for x in o["high_risk_deployer"]]
for k in ("high_risk_provider_summary", "deployer_becomes_provider", "ai_literacy"):
    entries.append(("obligations.json", k, "article", o[k].get("article")))
p = load("prohibitions.json")
entries += [("prohibitions.json", f"practices/{x['id']}", "article", x.get("article")) for x in p["practices"]]
t = load("timeline.json")
entries += [("timeline.json", f"milestones/{x['id']}", "provision", x.get("provision")) for x in t["milestones"]]
tr = load("transparency.json")
entries += [("transparency.json", f"duties/{x['id']}", "article", x.get("article")) for x in tr["duties"]]
c = load("cross_framework.json")
for x in c["rules"]:
    refs = re.findall(r"(?:Article|Art\.)\s*\d+(?:\(\w+\))*|Principles?\s*\d+(?:\.\d+)?(?:\s*to\s*\d+)?|Annex A", x["note"])
    entries.append(("cross_framework.json", f"rules/{x['id']}", "framework (+ provisions named in note)",
                    f"{x['framework']} | note refs: {'; '.join(refs) or 'none'}"))
def tier(e):
    """Mechanical tiers. 'none': no article, annex, chapter, section or
    principle named. 'grouping': the value starts with 'Chapter', or the only
    reference is 'Annex A'. Otherwise 'article-level' (an article, paragraph,
    annex point or principle is named)."""
    v = e[3].split("note refs: ")[-1] if e[0] == "cross_framework.json" else e[3]
    if not v or v == "none" or not re.search(r"Art\.|Arts\.|Article|Annex|Chapter|Section|Principle", v):
        return "none"
    if v.startswith("Chapter") or v.strip() == "Annex A":
        return "grouping"
    return "article-level"
print("| file | rule | citation field | value | tier |")
print("|---|---|---|---|---|")
for e in entries:
    print("| " + " | ".join(str(v) for v in e) + f" | {tier(e)} |")
from collections import Counter
print()
print("tiers:", dict(Counter(tier(e) for e in entries)))
print("not article-level:", [f"{e[0]}:{e[1]} ({tier(e)})" for e in entries if tier(e) != "article-level"])
print()
print("rule entries:", len(entries))
fielded = [e for e in entries if e[0] != "cross_framework.json"]
print("entries with a dedicated citation field (article/point/provision/source):", len(fielded),
      "non-empty:", sum(1 for e in fielded if e[3]))
print("cross_framework entries (no dedicated citation field):", len(entries) - len(fielded))
print("annex_iii art_6_3_derogation conditions (sub-items, no own field):",
      [k for k in der["conditions"][0].keys()], len(der["conditions"]))
print()
for f in sorted(os.listdir(d)):
    m = load(f).get("_meta")
    print(f"_meta {f}: present={m is not None} keys={list(m) if m else None}")
```
Capture script, reproduced in full:
```
S=<SCRATCH>
D=repo_under_test/src/aiact_triage/data
echo "=== git -C repo_under_test log -1 --format='%H' ==="; git -C repo_under_test log -1 --format='%H'
echo "##### CITATION COVERAGE #####"
echo "=== python3 -I citations.py \$D ==="; python3 -I $S/scripts/citations.py $D
echo
echo "##### VERIFICATION DATE, AGAINST THE README CONVENTION #####"
echo "=== sed -n 105p repo_under_test/README.md | cut -d';' -f2 ==="; sed -n 105p repo_under_test/README.md | cut -d';' -f2
echo "=== grep -n 'last_verified' \$D/*.json ==="; grep -n 'last_verified' $D/*.json
echo "=== grep -n 'last_verified' repo_under_test/src/aiact_triage/register.py ==="; grep -n 'last_verified' repo_under_test/src/aiact_triage/register.py
OUT=$S/ca07_audit; rm -rf $OUT
for inv in examples/inventory.csv templates/ai_inventory_template.csv; do
  echo "=== register mode over repo_under_test/$inv into <SCRATCH>/ca07_audit/$(basename $inv .csv) (package imported from repo_under_test/src) ==="
  python3 -I -c 'import sys; sys.path.insert(0, "repo_under_test/src"); from aiact_triage.cli import main; sys.exit(main(sys.argv[1:]))' \
    register repo_under_test/$inv --out $OUT/$(basename $inv .csv) --assessor "B. Struve" > /dev/null; echo "EXIT: $?"
  echo "--- records written, and records containing 'Rule set last verified 2026-08-04' ---"
  ls $OUT/$(basename $inv .csv) | sed "s|$S|<SCRATCH>|"
  echo "files: $(ls $OUT/$(basename $inv .csv) | wc -l)"
  echo "files containing the date line: $(grep -l 'Rule set last verified 2026-08-04' $OUT/$(basename $inv .csv)/* | wc -l)"
  echo "files without it: $(grep -L 'Rule set last verified 2026-08-04' $OUT/$(basename $inv .csv)/* | sed "s|$OUT/||" | tr '\n' ' ')"
done
echo
echo "##### OMNIBUS STALENESS, FROM THE RULE FILES' SOURCES AS THEY STAND #####"
echo "=== grep -n -i -E 'compromise|9247|press release|not yet published|provisionally|pending publication' \$D/*.json ==="
grep -n -i -E 'compromise|9247|press release|not yet published|provisionally|pending publication' $D/*.json; echo "EXIT: $?"
echo "=== grep -c '2026/1744' \$D/*.json ==="; grep -c '2026/1744' $D/*.json
echo "=== _meta source fields ==="
python3 -I -c '
import json, os, sys
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    m = json.load(open(os.path.join(d, f)))["_meta"]
    print(f, "|", m.get("source") or m.get("sources"))
' $D
```

**Evidence.**
```
=== git -C repo_under_test log -1 --format='%H' ===
7aab9f95065f9cf69cbdefe5a9aed64c361386ce
##### CITATION COVERAGE #####
=== python3 -I citations.py $D ===
| file | rule | citation field | value | tier |
|---|---|---|---|---|
| annex_iii.json | areas/biometrics | point | Annex III, 1 | article-level |
| annex_iii.json | areas/critical_infrastructure | point | Annex III, 2 | article-level |
| annex_iii.json | areas/education | point | Annex III, 3 | article-level |
| annex_iii.json | areas/employment | point | Annex III, 4 | article-level |
| annex_iii.json | areas/essential_services | point | Annex III, 5 | article-level |
| annex_iii.json | areas/law_enforcement | point | Annex III, 6 | article-level |
| annex_iii.json | areas/migration | point | Annex III, 7 | article-level |
| annex_iii.json | areas/justice_democracy | point | Annex III, 8 | article-level |
| annex_iii.json | art_6_3_derogation | source | Article 6(3), Regulation (EU) 2024/1689 | article-level |
| obligations.json | high_risk_deployer/use_per_instructions | article | Art. 26(1) | article-level |
| obligations.json | high_risk_deployer/human_oversight | article | Art. 26(2) | article-level |
| obligations.json | high_risk_deployer/input_data_control | article | Art. 26(4) | article-level |
| obligations.json | high_risk_deployer/monitor_and_report | article | Art. 26(5) | article-level |
| obligations.json | high_risk_deployer/log_retention | article | Art. 26(6) | article-level |
| obligations.json | high_risk_deployer/inform_workers | article | Art. 26(7) | article-level |
| obligations.json | high_risk_deployer/inform_affected_persons | article | Art. 26(11) | article-level |
| obligations.json | high_risk_deployer/fria | article | Art. 27 | article-level |
| obligations.json | high_risk_provider_summary | article | Arts. 8-15 (Chapter III Section 2), the provider obligations within Section 3 (Arts. 16-22), and Arts. 43, 49 and 72 | article-level |
| obligations.json | deployer_becomes_provider | article | Art. 25(1) | article-level |
| obligations.json | ai_literacy | article | Art. 4 | article-level |
| prohibitions.json | practices/subliminal_manipulation | article | Art. 5(1)(a) | article-level |
| prohibitions.json | practices/exploiting_vulnerabilities | article | Art. 5(1)(b) | article-level |
| prohibitions.json | practices/social_scoring | article | Art. 5(1)(c) | article-level |
| prohibitions.json | practices/predictive_policing_profiling | article | Art. 5(1)(d) | article-level |
| prohibitions.json | practices/untargeted_face_scraping | article | Art. 5(1)(e) | article-level |
| prohibitions.json | practices/emotion_inference_work_education | article | Art. 5(1)(f) | article-level |
| prohibitions.json | practices/biometric_categorisation_sensitive | article | Art. 5(1)(g) | article-level |
| prohibitions.json | practices/realtime_remote_biometric_id | article | Art. 5(1)(h) | article-level |
| prohibitions.json | practices/ncii_csam_generation | article | Art. 5(1), first subpara, points (ba) and (bb), and Art. 5(1a)-(1b) (inserted by Regulation (EU) 2026/1744) | article-level |
| timeline.json | milestones/prohibitions_original | provision | Article 5 prohibited practices, points (a) to (h) | article-level |
| timeline.json | milestones/prohibition_ncii_csam | provision | Article 5(1), new points (ba) and (bb): AI systems for generating non-consensual intimate imagery or child sexual abuse material | article-level |
| timeline.json | milestones/ai_literacy | provision | Article 4 AI literacy | article-level |
| timeline.json | milestones/gpai | provision | Articles 51 to 56 (Chapter V), general-purpose AI model obligations | article-level |
| timeline.json | milestones/transparency_core | provision | Article 50(1), 50(3) and 50(4) transparency obligations | article-level |
| timeline.json | milestones/transparency_marking | provision | Article 50(2) machine-readable marking of synthetic content | article-level |
| timeline.json | milestones/high_risk_annex_iii | provision | Chapter III, Sections 1, 2 and 3 (except Article 6(5)), for stand-alone high-risk AI systems (Annex III) | grouping |
| timeline.json | milestones/high_risk_annex_i | provision | Chapter III obligations for high-risk AI embedded in Annex I regulated products | grouping |
| timeline.json | milestones/sandboxes | provision | National AI regulatory sandboxes | none |
| transparency.json | duties/disclose_ai_interaction | article | Art. 50(1) | article-level |
| transparency.json | duties/mark_synthetic_content | article | Art. 50(2) | article-level |
| transparency.json | duties/disclose_emotion_or_biometric | article | Art. 50(3) | article-level |
| transparency.json | duties/disclose_deepfake | article | Art. 50(4) | article-level |
| cross_framework.json | rules/ss1_23_inventory | framework (+ provisions named in note) | PRA SS1/23 | note refs: Principle 1 | article-level |
| cross_framework.json | rules/ss1_23_lifecycle_alignment | framework (+ provisions named in note) | PRA SS1/23 | note refs: Article 26; Principles 3 to 5; Principle 2.6 | article-level |
| cross_framework.json | rules/dora_third_party | framework (+ provisions named in note) | DORA | note refs: Article 28(3); Article 30 | article-level |
| cross_framework.json | rules/iso42001_supplier | framework (+ provisions named in note) | ISO/IEC 42001 | note refs: Annex A | grouping |
| cross_framework.json | rules/gdpr_special_category | framework (+ provisions named in note) | UK/EU GDPR | note refs: Article 9; Article 9; Article 35(3)(b) | article-level |

tiers: {'article-level': 43, 'grouping': 3, 'none': 1}
not article-level: ['timeline.json:milestones/high_risk_annex_iii (grouping)', 'timeline.json:milestones/high_risk_annex_i (grouping)', 'timeline.json:milestones/sandboxes (none)', 'cross_framework.json:rules/iso42001_supplier (grouping)']

rule entries: 47
entries with a dedicated citation field (article/point/provision/source): 42 non-empty: 42
cross_framework entries (no dedicated citation field): 5
annex_iii art_6_3_derogation conditions (sub-items, no own field): ['id', 'text'] 4

_meta annex_iii.json: present=True keys=['source', 'note']
_meta cross_framework.json: present=True keys=['purpose', 'sources', 'confidence_note']
_meta obligations.json: present=True keys=['source', 'note']
_meta prohibitions.json: present=True keys=['source', 'note']
_meta timeline.json: present=True keys=['regulation', 'amendment_status', 'last_verified', 'sources']
_meta transparency.json: present=True keys=['source', 'note']

##### VERIFICATION DATE, AGAINST THE README CONVENTION #####
=== sed -n 105p repo_under_test/README.md | cut -d';' -f2 ===
 the rule set's verification date is recorded in the timeline data and carried into every audit record. The encoding draws from Regulation (EU) 2024/1689 and, for the amendments, Regulation (EU) 2026/1744, both as published in the Official Journal. When the Omnibus was published on 24 July 2026, every encoded date was re-verified against the Official Journal text and survived unchanged
=== grep -n 'last_verified' $D/*.json ===
repo_under_test/src/aiact_triage/data/timeline.json:5:    "last_verified": "2026-08-04",
=== grep -n 'last_verified' repo_under_test/src/aiact_triage/register.py ===
123:        f"Rule set last verified {meta['last_verified']}.",
178:        f"Rule set last verified {meta['last_verified']}.",
=== register mode over repo_under_test/examples/inventory.csv into <SCRATCH>/ca07_audit/inventory (package imported from repo_under_test/src) ===
EXIT: 0
--- records written, and records containing 'Rule set last verified 2026-08-04' ---
01-cv-screening-assistant.md
02-customer-support-chatbot.md
03-credit-scoring-model.md
04-marketing-copy-generator.md
05-meeting-transcription-and-summariser.md
06-exam-marking-consistency-checker.md
07-workplace-wellbeing-emotion-monitor-pilot.md
_summary.md
files: 8
files containing the date line: 8
files without it: 
=== register mode over repo_under_test/templates/ai_inventory_template.csv into <SCRATCH>/ca07_audit/ai_inventory_template (package imported from repo_under_test/src) ===
EXIT: 0
--- records written, and records containing 'Rule set last verified 2026-08-04' ---
01-retail-credit-scoring-model.md
_summary.md
files: 2
files containing the date line: 2
files without it: 

##### OMNIBUS STALENESS, FROM THE RULE FILES' SOURCES AS THEY STAND #####
=== grep -n -i -E 'compromise|9247|press release|not yet published|provisionally|pending publication' $D/*.json ===
EXIT: 1
=== grep -c '2026/1744' $D/*.json ===
repo_under_test/src/aiact_triage/data/annex_iii.json:0
repo_under_test/src/aiact_triage/data/cross_framework.json:0
repo_under_test/src/aiact_triage/data/obligations.json:2
repo_under_test/src/aiact_triage/data/prohibitions.json:3
repo_under_test/src/aiact_triage/data/timeline.json:4
repo_under_test/src/aiact_triage/data/transparency.json:1
=== _meta source fields ===
annex_iii.json | Annex III and Article 6, Regulation (EU) 2024/1689
cross_framework.json | PRA SS1/23 (including the April 2026 update), Bank of England AI supervisory work (February 2026 roundtables), DORA (Regulation (EU) 2022/2554), ISO/IEC 42001:2023, UK/EU GDPR. Verification of these anchors is recorded in the commit history, not asserted here.
obligations.json | Articles 4, 16, 25, 26, 27 and Chapter III Sections 2 and 3, Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744
prohibitions.json | Article 5, Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI), published in the Official Journal on 24 July 2026 and in force since 27 July 2026. Points (ba), (bb) and paragraphs 1a and 1b apply from 2 December 2026.
timeline.json | ['Regulation (EU) 2026/1744, OJ L, 24.7.2026', 'Regulation (EU) 2024/1689, OJ L, 12 July 2024']
transparency.json | Article 50, Regulation (EU) 2024/1689; amended dates per Regulation (EU) 2026/1744 (Digital Omnibus on AI), published in the Official Journal on 24 July 2026 and in force since 27 July 2026
```

What the output shows.

Citation coverage. 47 rule entries. All 42 entries that have a dedicated
citation field carry a non-empty value. By the tiers: 43 name an article,
paragraph, annex point or principle; 3 cite only at grouping level (the
`high_risk_annex_iii` and `high_risk_annex_i` timeline milestones, both at
Chapter III level, and the ISO/IEC 42001 cross-framework flag, at
"Annex A" level, which the file's `_meta` discloses as deliberate pending
verification against the standard); 1 names no provision at all, the
`sandboxes` timeline milestone ("National AI regulatory sandboxes"). Against
the criterion, an article citation on every rule at 100%, the `sandboxes`
entry fails on any reading. Whether the three grouping-level entries also
fail changes the count, 43 or 46 of 47 passing, but not the result.

Verification date. `timeline.json` is the only file with `last_verified`
(`2026-08-04`), which is where the convention puts it, and `register.py`
writes it into the record text. All 10 files register mode produced (8
audit records and 2 summaries) contain "Rule set last verified 2026-08-04".
Both limbs of the convention hold.

Staleness. No rule file contains "compromise", "9247", "press release",
"not yet published", "provisionally" or "pending publication" (exit 1).
Four files cite Regulation (EU) 2026/1744 in their sources or text, and
`timeline.json` records `last_verified` 2026-08-04, after the 24 July 2026
publication. `annex_iii.json` cites only Regulation (EU) 2024/1689; its
`_meta` note states that the eight Annex III areas are unchanged by the
Omnibus. `cross_framework.json` cites no AI Act source by design. The
exception condition in PLAN.md section 4, files still citing the
compromise text after Official Journal publication, is not met: the check
passes substantively, exercised by a real amendment.

**Executed.** 2026-10-11, 13:03 BST (final capture run; a run at 13:03
without the tier column and with a looser note regex differed only in
those two respects).

**Conclusion.** Operating exception: citation coverage is below the 100% criterion, because the timeline milestone `sandboxes` carries no article citation (with three further entries cited only at chapter or Annex A level), while the verification date and the Omnibus staleness check both pass.
