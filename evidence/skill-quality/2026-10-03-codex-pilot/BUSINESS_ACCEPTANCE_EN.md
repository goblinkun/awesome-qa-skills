<div align="right"><a href="./BUSINESS_ACCEPTANCE.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Real Business Acceptance: Not Run

Use this checklist to establish that Skill artifacts help accomplish real business testing, not merely pass text Evals. Current state: **`NOT_RUN`**. Prerequisites are missing; Codex must not choose another project, load production, or sign on behalf of an accountable owner.

## Required Inputs

- Real project path or authorized requirement/design material, version, and business objectives.
- Acceptance criteria, priorities, and permitted sanitized samples/test accounts.
- Target environment and allowed reads/writes, API/UI, injection, and load actions; retain explicit production prohibitions.
- Tools, credential injection method (no secrets pasted into documents), budget, stop conditions, and recovery.
- Accountable acceptance owner and decisions requiring their confirmation. Without that decision, the report is only candidate acceptance evidence.

## Minimum Execution Plan

| Skill | Real input | Acceptance to execute | Evidence to retain |
| --- | --- | --- | --- |
| functional-testing | Business flow, requirements, environment | Review and execute critical cases in the approved environment; compare actual/expected | Requirement mapping, cases, runs, defects, omissions |
| testability-analysis | Architecture/dependencies/current seams | Expert review plus one isolated seam or controlled experiment | Sources, value/cost, safety boundary, before/after evidence |
| performance-testing | SLOs, transactions, traffic, data, load authority | Validate load model/units/metrics; run representative load only when authorized | Script/version, target, metrics, traffic budget, stops/recovery |
| skill-evaluation | Real Skill changes/evaluation need | Run the designed minimum suite; review judges and state claims | Source/case/model/judge/trace, actual failure classification |
| skill-change-verification | Real diff, project rules/commands | Execute recommended checks; confirm coverage and bounded claims | Run/unrun checks, results, residual risk, acceptance decision |

Confirm inputs and authority before each step. Review artifacts read-only before performing explicitly permitted actions. Missing environment/capability remains `BLOCKED`/`NOT_RUN`; plans, dry-runs, model claims, or green static gates are not substitutes.

## Acceptance Record

Record project/version, Skill snapshot, actual requirement/case, runtime/model, approved scope, actual/expected, original evidence, issues, and the owner's decision. Criteria come from real requirements. High-risk gaps, unrun critical paths, or unrecovered side effects prevent a business `PASS`.

Engineering runs are reported in [README_EN.md](./README_EN.md); they do not fill these business-measurement fields. All five business executions, business effectiveness, E4, and final sign-off remain incomplete.
