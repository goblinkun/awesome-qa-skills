From [artifacts/runs.json](../../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-comparable-runs.yaml), this is a **Version Regression** comparison: previous/current Skill versions, rather than a with/without-Skill benchmark. No engine was run for this interpretation (`NOT_RUN`).

| Run | Skill | Date (UTC) | Reported passes |
|---|---|---|---|
| `run-prev` | `v1` | October 1, 2026 | 8/10 — 80% |
| `run-current` | `v2` | October 2, 2026 | 6/10 — 60% |

**Factual change:** **−20 percentage points**, with two fewer passes overall. This does not establish exactly two newly regressed cases; individual outcomes are absent.

**Comparability basis:** Both reports declare Eval `e1`, skill-up `0.12.0`, engine `codex`, model `model-fixture`, temperature `0`, seed `7`, input identifier `cases-A`, judge `rubric-A`, environment `sandbox-A`, and 10 cases. These matching fields support a descriptive comparison. Underlying snapshots and actual execution settings remain unverified; provider identity is `unknown`.

| Evidence area | Assessment |
|---|---|
| Coverage and case results | `UNASSESSED`: assertions, coverage, individual outcomes, and failure details are missing. |
| Outcome evidence | Aggregate pass counts reported under `rubric-A`; not independently reproduced. |
| Trigger evidence | `BLOCKED`: no observed `skill.selection` trace. |
| Process, artifacts, semantic judgment | `UNASSESSED`: traces, outputs, and judge calibration are unavailable. |
| With/without-Skill benchmark | `NOT_RUN`; this report supplies version comparison only. |
| Flakiness, infrastructure, failure attribution | `unknown`; no evidence separates Skill, Eval, or Infrastructure defects. |
| Eval validity and uncertainty | One reported run per version over 10 cases. Repeatability, judge reliability, and statistical uncertainty are unknown. |
| Quality Score | `NOT_SCORED`. |
| Release conclusion | `INSUFFICIENT_EVIDENCE`. |

Before a release conclusion, obtain paired case outcomes and original outputs/traces; verify Skill/Eval snapshots, inputs, judge rubric/calibration, and runtime metadata; assess repeated comparable runs and critical success, incomplete-input, boundary, and trigger coverage against explicit release criteria. Investigate any confirmed regressions and retain evidence of remediation.

Evidence vocabulary: `PASS`/`FAIL` mean an assertion was satisfied/violated; `BLOCKED` means required evidence or prerequisites are unavailable; `NOT_RUN` means execution did not occur; `NOT_SCORED` means no score was produced; `UNASSESSED` means no assessment was made; `INSUFFICIENT_EVIDENCE` means the available evidence cannot support the conclusion.
