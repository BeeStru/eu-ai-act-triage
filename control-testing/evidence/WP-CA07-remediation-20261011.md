# WP-CA07-remediation-20261011

**Control.** CA-07, rule-data citation and verification-date discipline.

**Original result.** Operating exception (WP-CA07-operating-20261011,
committed e6e2bfe): citation coverage below the 100% criterion, because the
timeline milestone `sandboxes` carried no article citation ("National AI
regulatory sandboxes"). This is condition (a) in B. Struve's rulings of
11 October 2026 (STATE.md). The original result stands unedited; this
workpaper records the retest of the remediated condition only.

**Remediation commit.** `b5cb97c9366f7dc526ef1c8571b6549e759385ea`, "Cite
Article 57(1) on the sandboxes timeline milestone", one line changed in
`src/aiact_triage/data/timeline.json` (the `sandboxes` provision field; the
dates, status and note are unchanged, as the diff below shows). It reached
`main` in one push, `7aab9f9` to `22ad85f`, at 2026-10-11T12:42:50Z, together
with the two CA-08 remediation commits. CI run 38140312149 (workflow
"tests", event push, head `22ad85f`) completed with conclusion success, and
every step on both matrix legs succeeded, `pytest -q` and the packaged-data
step included. Sources: the committed captures
WP-CA08-remediation-20261011-runs.json,
WP-CA08-remediation-20261011-run-38140312149-steps.tsv and
WP-CA08-remediation-20261011-activity.jsonl (b751bcb), captured outside
the sandbox by B. Struve, with the commands recorded in
WP-CA08-remediation-20261011-capture-commands.txt; read out in this session
in WP-CA08-remediation-20261011.

**Test method and reason.** Inspection of the full population of rule
entries across `src/aiact_triage/data/`, the same method as
WP-CA07-operating-20261011, because the remediation is tested against the
same criterion that failed: an article citation on every rule, at 100%. The
helper script is byte-identical to the one reproduced in the original
workpaper: it was extracted from lines 61 to 116 of that committed file, and
the two SHA-256 values in the evidence match. The same mechanical tier rule
applies ("none", "grouping", "article-level"). Per B. Struve's ruling of
11 October 2026, entries cited at chapter or Annex level are observations,
not exceptions, because Article 113 states those application dates at
chapter level. Scope of the retest: citation coverage only. The
verification-date and staleness limbs passed in the original test and were
not retested, because their inputs (`last_verified` and the `_meta` sources)
are untouched: the diff of the data directory between `7aab9f9` and
`22ad85f` is the one provision line shown below. The retest checks that a
citation is present at article level. It does not check that Article 57(1)
is the correct article; that is a legal question the criterion does not
reach. Deviation from the original: none in method; the audit-record
generation of original deviation 6 belonged to the verification-date limb
and was not repeated.

**Population and regime.** Manual regime, full population: 47 rule entries in
six files, the same population as the original test. Object under test:
fresh clone of the public repository into `repo_under_test/` at
2026-10-11 12:48:13 UTC, HEAD `22ad85f3276040aceec29bff4eba34caacdd1d53`,
`git ls-remote` confirming `main` at the same commit, 48 commits, tags
v0.1.0 to v0.5.0. `7aab9f9..22ad85f` holds exactly three commits, no merges,
and no other commit follows `7aab9f9`.

**Procedure executed.** Run from the pack directory, with `<SCRATCH>` the
session scratchpad. Helper script: as reproduced in WP-CA07-operating-20261011,
lines 61 to 116, extracted with
`sed -n 61,116p evidence/WP-CA07-operating-20261011.md > <SCRATCH>/scripts/citations.py`.
Capture script, reproduced in full:
```
S=$1
D=repo_under_test/src/aiact_triage/data
echo "=== git -C repo_under_test log -1 --format='%H' ==="; git -C repo_under_test log -1 --format='%H'
echo "=== sha256sum of the helper and of lines 61 to 116 of WP-CA07-operating-20261011.md ==="
sha256sum $S/scripts/citations.py | sed "s|$S|<SCRATCH>|"; sed -n 61,116p evidence/WP-CA07-operating-20261011.md | sha256sum
echo "=== git -C repo_under_test diff 7aab9f9 22ad85f -- src/aiact_triage/data/ ==="; git -C repo_under_test diff 7aab9f9 22ad85f -- src/aiact_triage/data/
echo "##### CITATION COVERAGE #####"
echo "=== python3 -I citations.py \$D ==="; python3 -I $S/scripts/citations.py $D
```

**Evidence.**
```
=== git -C repo_under_test log -1 --format='%H' ===
22ad85f3276040aceec29bff4eba34caacdd1d53
=== sha256sum of the helper and of lines 61 to 116 of WP-CA07-operating-20261011.md ===
31c30ab4bf5ad58a38e85b588db9cfcf86ce06b16170643a30cc67cab224716b  <SCRATCH>/scripts/citations.py
31c30ab4bf5ad58a38e85b588db9cfcf86ce06b16170643a30cc67cab224716b  -
=== git -C repo_under_test diff 7aab9f9 22ad85f -- src/aiact_triage/data/ ===
diff --git a/src/aiact_triage/data/timeline.json b/src/aiact_triage/data/timeline.json
index 25cb0c3..739e5a4 100644
--- a/src/aiact_triage/data/timeline.json
+++ b/src/aiact_triage/data/timeline.json
@@ -75,7 +75,7 @@
     },
     {
       "id": "sandboxes",
-      "provision": "National AI regulatory sandboxes",
+      "provision": "Article 57(1) national AI regulatory sandboxes",
       "original_date": "2026-08-02",
       "amended_date": "2027-08-02",
       "status": "postponed_by_omnibus",
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
| timeline.json | milestones/sandboxes | provision | Article 57(1) national AI regulatory sandboxes | article-level |
| transparency.json | duties/disclose_ai_interaction | article | Art. 50(1) | article-level |
| transparency.json | duties/mark_synthetic_content | article | Art. 50(2) | article-level |
| transparency.json | duties/disclose_emotion_or_biometric | article | Art. 50(3) | article-level |
| transparency.json | duties/disclose_deepfake | article | Art. 50(4) | article-level |
| cross_framework.json | rules/ss1_23_inventory | framework (+ provisions named in note) | PRA SS1/23 | note refs: Principle 1 | article-level |
| cross_framework.json | rules/ss1_23_lifecycle_alignment | framework (+ provisions named in note) | PRA SS1/23 | note refs: Article 26; Principles 3 to 5; Principle 2.6 | article-level |
| cross_framework.json | rules/dora_third_party | framework (+ provisions named in note) | DORA | note refs: Article 28(3); Article 30 | article-level |
| cross_framework.json | rules/iso42001_supplier | framework (+ provisions named in note) | ISO/IEC 42001 | note refs: Annex A | grouping |
| cross_framework.json | rules/gdpr_special_category | framework (+ provisions named in note) | UK/EU GDPR | note refs: Article 9; Article 9; Article 35(3)(b) | article-level |

tiers: {'article-level': 44, 'grouping': 3}
not article-level: ['timeline.json:milestones/high_risk_annex_iii (grouping)', 'timeline.json:milestones/high_risk_annex_i (grouping)', 'cross_framework.json:rules/iso42001_supplier (grouping)']

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
```

What the output shows. 47 rule entries, the same population as the original.
All 42 entries that have a dedicated citation field carry a non-empty value.
By tier: 44 article-level, 3 grouping, 0 none. The `sandboxes` milestone,
the one entry tiered "none" at `7aab9f9`, now reads "Article 57(1) national
AI regulatory sandboxes" and tiers as article-level. The three grouping-level
entries are unchanged (the `high_risk_annex_iii` and `high_risk_annex_i`
timeline milestones at Chapter III level, and the ISO/IEC 42001
cross-framework flag at Annex A level), and the ruling of 11 October 2026
treats them as observations. Against the criterion as ruled, every rule now
carries an article citation.

**Executed.** 2026-10-11, 13:49 BST.

**Conclusion.** Status: remediated during fieldwork. The one rule without an article citation now carries one (Article 57(1), commit `b5cb97c`), giving 0 of 47 entries without a citation at `22ad85f`. The original operating exception in WP-CA07-operating-20261011 stands as the result at the scope-freeze commit.
