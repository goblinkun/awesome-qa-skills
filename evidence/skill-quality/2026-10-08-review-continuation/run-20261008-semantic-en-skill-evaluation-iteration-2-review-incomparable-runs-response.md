[runs.json](../../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-incomparable-runs.yaml) records these **numerical observations**:

| Run | Skill | Model | Input hash | Recorded passes |
|---|---|---|---|---|
| `run-prev` | `v1` | `model-fixture` | `cases-A` | 8/10 — 80% |
| `run-current` | `v2` | `model-other` | `cases-B` | 6/10 — 60% |

The difference is **−2 passes and −20 percentage points**. These are descriptive observations.

**Version-regression conclusion: `INSUFFICIENT_EVIDENCE`.** Skill version, model, and inputs all changed. The decrease cannot be attributed to `v2`; equal case counts do not establish comparable cases.

Recorded controls match: Eval `e1`, `skill-up 0.12.0`, engine `codex`, temperature `0`, seed `7`, judge `rubric-A`, and environment `sandbox-A`. Timestamps are October 1 and 2, 2026, respectively, at 09:00 UTC. Provider, target Skill path/language, and judge implementation/calibration are `unknown`.

| Report area | Evidence state and limitation |
|---|---|
| Coverage / case results | `UNASSESSED`: no cases, assertions, or individual judgments supplied |
| Trigger evidence | `BLOCKED`: no `skill.selection` traces |
| Process / artifact / semantic evidence | `UNASSESSED`: only aggregate metadata available |
| With/without Skill benchmark | `NOT_RUN` |
| Flakiness / infrastructure | `UNASSESSED`; failure attribution is `UNKNOWN` |
| Quality Score | `NOT_SCORED` |
| Validation / controlled rerun | `NOT_RUN`: no runnable target or original inputs supplied |

**Smallest controlled rerun:** run **`v2` once on the original 10 `cases-A` inputs using `model-fixture`**, preserving every matched setting above. Pin the actual cases and judge implementation, and retain case-level outputs, judgments, run metadata, and selection traces. Compare against `run-prev` if its baseline provenance is recoverable.

If that baseline cannot be established, rerun **both `v1` and `v2`** under those identical conditions—20 case executions total—with Skill version as the sole experimental difference.

State meanings: `PASS`/`FAIL` = assertion met/not met; `BLOCKED` = prerequisite missing; `NOT_RUN` = execution absent; `NOT_SCORED` = score absent; `UNASSESSED` = assessment absent; `INSUFFICIENT_EVIDENCE` = available evidence cannot support the conclusion.
