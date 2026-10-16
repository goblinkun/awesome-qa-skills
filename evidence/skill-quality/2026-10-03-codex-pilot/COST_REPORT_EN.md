<div align="right"><a href="./COST_REPORT.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Pilot Cost Report

Use this report to review engineering overhead, **not as an invoice or cost-acceptance decision**. Per-call records are in [cost-ledger.json](./cost-ledger.json).

| Scope | Codex calls | Observed input tokens | Observed output tokens | Unknown usage |
| --- | ---: | ---: | ---: | ---: |
| Selected current core | 34 | 1,774,125 | 56,687 | 0 |
| Selected second-model sample | 5 | 373,842 | 11,321 | 0 |
| All archived judge calls | 14 | 262,200 | 11,246 | 0 |
| All archived native calls, including the rows above | 85 | 4,113,159 | 139,377 | 1 |

The final row includes initial/repaired runs, Benchmarks, calibration judges, one portable-configuration smoke, and one blocked request. It is not 85 independent acceptance cases, and the rows must not be added together. The initial incompletely isolated smoke, September 30 legacy runs, and synthetic calibration main answers are excluded.

`input_tokens` comes from Codex CLI completion events and already includes cached input. The ledger lists the observed cached subset separately; **do not count it again**. Tool interactions can increase input usage, so it is not the prompt's word count. The blocked request has no usage and remains `unknown`; native zero fields do not establish free execution.

## Selected Benchmark Main-Run Cost

| Skill | Variant | Main seconds | Main input + output tokens |
| --- | --- | ---: | ---: |
| functional-testing | with / without | 177.407 / 202.515 | 55,484 / 69,496 |
| testability-analysis | with / without | 157.598 / 123.741 | 55,829 / 85,010 |
| skill-evaluation | with / without | 93.166 / 94.581 | 54,307 / 67,095 |

This table excludes judge time and usage, which are in the ledger. The skill-evaluation baseline failed its precondition and did not invoke a semantic judge, so total pipeline cost is not directly comparable. Each variant has one sample; order and load may influence latency. No stable savings are established.

## Unmeasured Cost

- Actual USD cost / account invoice: `unknown`; list pricing was not used to infer actual payment.
- Eval authoring, maintenance, and manual triage time: `unknown`; no reliable timer was available.
- CI model execution cost: `NOT_RUN`; no automatic paid model calls were added to CI.
- Acceptable budget / long-term maintenance cost: `UNASSESSED`; an accountable owner must set limits and evaluate repeated samples.

For the next round, set a finite budget and stop conditions before repeating representative core cases and a few difficult Benchmarks. Regrade captured answers first when diagnosing assertions, then perform necessary real reruns after confirming an Eval Defect. This recommendation does not authorize quota resets or purchases.
