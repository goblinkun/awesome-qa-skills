<div align="right"><a href="./FINDINGS.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Findings and Repair Record

Use this record to understand Eval changes, superseded results, and remaining limits. Native FAIL is retained; regrading a captured answer is distinct from generating another answer.

| Finding | Classification | Action and verification |
| --- | --- | --- |
| Old temporary transport returned only text, losing JSONL/usage; install target and plugin isolation were unclear | Infrastructure Defect | SessionResult, explicit `.agents/skills/<name>`, disabled global/plugin Skills, closed stdin; six unit tests and actual catalog checks |
| Output covered failures, assumptions, evidence, or actions but missed an exact phrase/case/Chinese heading | Eval Defect | Remove duplicate literal requirements or recognize equivalent official-template wording; retain risk, boundary, gaps, and actionable-output checks |
| Valid `NOT_RUN` failed a regex allowing only `not run` | Eval Defect | Accept spaces and underscores while retaining valid canonical labels |
| Functional risk answer gave login→order→pay without saying “critical path” | Eval Defect | Accept the explicit ordered business chain without weakening priority, fallback, or residual-risk assertions |
| Scope case directly requested an engine replacement but treated “mentions skill-up” as proof of rejecting it | Eval Defect | Reframe as scope review within the current Skill, explicitly no implementation; assert boundary language and existing flow; both full three-case suites rerun successfully |
| Very sparse skill-evaluation input had previously produced natural-language states only | Skill Defect, already repaired | Both Skill/prompt languages require applicable canonical states in the minimum report; full suites passed here without promoting old evidence to business acceptance |
| Semantic judge accepted natural language as canonical-state compliance | Eval Defect | Add the same deterministic precondition to both variants; retain a near-miss negative and rerun the Benchmark without lowering the rubric |
| Initial functional positive golden lacked sufficient expected outcomes and residual risks | Eval Defect, calibration fixture | Enrich the golden and rerun; retain old FAIL and revised PASS without changing the threshold |
| Provider blocked the unsafe seam request before an answer | Infrastructure Defect / provider_safety_filter | Retain native ERROR, report BLOCKED, withhold equivalent English request; no refusal-quality conclusion or filter bypass |
| No canonical selection event | Missing observability, not a confirmed Trigger Defect | `BLOCKED`; output similarity, catalogs, and file reads are not substitutes |
| Redaction handled complete workspaces but missed macOS temporary ancestors in AGENTS probes | Infrastructure Defect, evidence export | Add ancestor redaction on 2026-10-04; both regressions fail before and pass after repair, and the whole-package scan passes. Retain the original hash and update one trace's export hash without rerunning models or changing results |

## Traceability

`artifacts/core/` retains initial core runs; `postfix/` holds affected suites after Eval repairs; `final/` contains both final complete skill-evaluation suites after scope-case correction. `cross-model/` and `cross-model-postfix/` remain separate. [results.json](./results.json) selects current suites instead of counting all historical attempts as passes.

`diagnostics/grade-*-red.json` and `grade-*-green.json` are **deterministic regrades of the same captured answer**, demonstrating repaired assertions. They are not new model generations or previous/current Skill version regression. Files without red/green suffixes retain the input and grading configuration.

`artifacts/benchmark/` retains the initial comparisons; `benchmark-postfix/` holds the canonical-state precondition correction. `calibration/` retains initial synthetic fixtures, `calibration-postfix/` the enriched functional positive, and `calibration-near-miss/` the state-contract near-miss that must fail. Synthetic main answers do not consume a generation model; judge calls are recorded separately.

## Limits

No Skill was automatically changed merely because a run failed. The core largely uses explicit text assertions, which cannot establish correctness of every domain recommendation. Calibration uses a small set of authored labels, not independently approved business-reviewer labels. Regex and semantic checks cannot replace high-risk domain acceptance. The final failing without-Skill Benchmark is a valid observation, not an error to be “fixed until green.”
