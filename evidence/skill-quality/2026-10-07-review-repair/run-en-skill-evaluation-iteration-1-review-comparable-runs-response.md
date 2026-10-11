**Comparison type: Version Regression (`v1` → `v2`).** [runs.json](../../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-comparable-runs.yaml) records:

| Run | Skill | Timestamp (UTC) | Reported pass rate |
|---|---|---|---|
| `run-prev` | `v1` | 2026-10-01 09:00 | 8/10 = 80% |
| `run-current` | `v2` | 2026-10-02 09:00 | 6/10 = 60% |

The factual change is **−20 percentage points, with two fewer passes**. No engine was run; new execution is `NOT_RUN`.

**Comparability basis:** both records specify Eval `e1`, skill-up `0.12.0`, engine `codex`, model `model-fixture`, temperature `0`, seed `7`, input hash `cases-A`, judge `rubric-A`, environment `sandbox-A`, and 10 cases. This supports a comparison at the recorded metadata level. Actual inputs, configurations, and judge implementation have not been independently verified. Provider, target Skill path, and language are `unknown`.

| Report area | Finding and evidence state |
|---|---|
| Scope / Summary | Interpret the supplied aggregates; release readiness is `INSUFFICIENT_EVIDENCE`. |
| Configuration / Coverage | Matching configuration labels; case content and behavioral coverage are `UNASSESSED`. |
| Case Results / Regression Findings | Aggregate deterioration is reported. Individual verdicts are `UNASSESSED`; two fewer passes does not identify exactly two newly failing cases. Non-pass outcomes are unspecified. |
| Trigger / Process / Outcome / Artifact / Semantic Evidence | Aggregate outcome is available. Trigger evidence is `BLOCKED` without `skill.selection`; process, underlying artifacts, and semantic correctness are `UNASSESSED`. |
| Benchmark Results | With/without-Skill effectiveness is `UNASSESSED`; these records compare versions. |
| Flaky / Infrastructure Errors / Eval Validity | `UNASSESSED`; failure attribution remains `Unknown`, with no basis to distinguish Skill, Eval, or Infrastructure Defects. |
| Limitations / Uncertainty | One run per version and ten cases provide no estimate of repeatability or variance. Matching temperature and seed do not establish reproducibility. Statistical significance and causal attribution to the Skill change remain `INSUFFICIENT_EVIDENCE`. |

Before a release conclusion, obtain:

1. Exact Skill snapshots and diff, case fixtures, full configurations, and judge rubric with appropriate validation or calibration.
2. Paired case outputs, verdicts, and traces to identify changed outcomes and classify their causes; selection traces where trigger claims matter.
3. Repeated comparable evaluations, representative critical and boundary coverage, and results assessed against explicit release criteria.

Evidence vocabulary: `PASS` = assertion met; `FAIL` = assertion violated; `BLOCKED` = required evidence or prerequisite unavailable; `NOT_RUN` = execution not performed; `NOT_SCORED` = no governed score produced; `UNASSESSED` = dimension not assessed; `INSUFFICIENT_EVIDENCE` = evidence cannot support the conclusion. No Quality Score was produced (`NOT_SCORED`).
