# WP-CA02-operating-20261011

**Control.** CA-02, protected main branch.

**Test method and reason.** None performed, because PLAN.md section 4 runs the
CA-02 operating test only if protection is enabled.

**Population and regime.** Not applicable; no protection configuration exists
whose operation could form a population.

**Procedure executed.**
```
None. Basis: WP-CA02-design-20261011 (committed in 4c63f22) and
WP-CA02-design-20261011-rulesets.txt.
```

**Evidence.** Cross-reference only. WP-CA02-design-20261011 records
"Branch not protected" (HTTP 404) for `main` and a settings page stating
that classic branch protections have not been configured;
`WP-CA02-design-20261011-rulesets.txt` records empty lists, exit 0, from
the rulesets endpoint and the branch-rules endpoint for `main`.

**Executed.** 2026-10-11, 12:37 BST.

**Conclusion.** Not applicable: no branch protection or ruleset existed on `main` at the test date, so there is no configured control whose operation could be tested.
