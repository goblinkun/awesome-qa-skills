<div align="right"><a href="./SQEM_V1_1_PROPOSAL.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# SQEM v1.1 Improvement Proposal

State: **proposal, not a released standard**. Use it to review validity, observability, and maintenance issues found in this Pilot. It introduces no Engine, Judge, or Quality Score.

## Keep and Simplify

| Proposal | Pilot evidence | Acceptance method |
| --- | --- | --- |
| Prefer behavior, reduce duplicate fixed-word checks | Real answers falsely failed headings, case, or equivalents | Correctly grade the captured positive and a real negative, not just produce green |
| Separate prose from machine enums | Semantic judge accepted natural-language missing-run states as canonical | Deterministic enum preconditions; semantic rubrics only for needed judgments |
| Calibrate positive, negative, and near-miss anchors | Initial golden was incomplete; state near-miss exposed false acceptance | Independent business-reviewer labels, expected/actual/disagreement retained; current seven fixtures are smoke only |
| Include host installation/isolation in minimum metadata | Old transport returned text only and had unclear target/plugin exposure | Per-call target/catalog/isolation, native JSONL, models, and usage |
| Separate availability/read from selection | CLI has no canonical selection event | Keep BLOCKED without events; no natural-trigger inference from outputs/reads |
| Separate scope review from separately authorized architecture work | Old replacement request was not a valid boundary test | Explicit current-flow review scope; authorize/design replacement separately |
| Separate main/judge/unknown usage | One filtered request had no usage; cache must not be counted twice | Per-call ledger, unknown not zero, no invoice inference from model list pricing |
| Layer core, comparison, and business evidence | 34 text passes cannot prove real load/business/release success | State supported/unsupported claims per layer; business needs project and owner |

## Next Finite Experiment

Retain the five core suites rather than expanding every combination. For the three selected Skills, choose a few domain-reviewed sparse/difficult inputs, then repeat controlled with/without trials within an approved budget. Control parameters, order, and judge; report cases/variants rather than only an average score. Stop equivalent requests after safety filtering; do not switch models or rephrase to bypass it.

Compatibility should next add representative Claude sampling with authorized credentials. Trigger checks need a host producing real selection events. Start business validation with one authorized project's minimum critical path. These experiments have not run and are excluded from current PASS counts.

## Not Proposed

- A global score, second Eval Engine, or automatic “optimize until green” loop.
- The same large mandatory Eval quota for every Skill.
- L3 awards or broad effectiveness claims based on one Benchmark trial.
- Provider filtering counted as a passing Skill negative behavior.

Formal v1.1 adoption still needs budget decisions, business acceptance, human judge calibration, and outstanding checks. This proposal supplies actionable directions only.
