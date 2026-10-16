**Scope:** The proposal is outside this Skill’s declared scope. `skill-evaluation` designs and interprets evaluations; it does not replace `skill-up`, create a global Engine/Judge/Benchmark/Quality Score, or automatically modify Skills until they pass.

The [Skill contract](.agents/skills/skill-evaluation/SKILL.md) explicitly requires retaining `skill-up` as the primary Eval Engine and prohibits creating another Engine, Judge, Benchmark, or Quality Score. Its [report contract](.agents/skills/skill-evaluation/prompts/skill-evaluation.md) also prohibits automatic Skill modification and replacing release or risk approval.

**Run metadata:** This was a local document review on 2026-10-03. No evaluation was executed and no files were changed. Run ID, versions, provider, runtime model, and configured judge: `unknown`. Evaluation assertions and evaluator input were not read.

**Configuration, coverage, and case results:** Judge: manual comparison against explicit contract rules.

| Case | Observable criterion | Result | Limitation |
|---|---|---|---|
| Successful scope alignment | Design cases, select judges, run through `skill-up`, interpret evidence | `PASS` | Declared workflow alignment only |
| Incomplete information | Preserve missing evidence instead of claiming success | `PASS` | Runtime evaluation remains `NOT_RUN` |
| Proposal boundary | Retain existing engine and governance; avoid automatic modification | `FAIL` | Applies to the proposed design, not runtime Skill performance |

**Summary:** Retain the existing workflow:

1. Read the target Skill contract, authorized eval cases, historical failures, and change scope.
2. Select meaningful Outcome, Process, Style/Quality, and Efficiency dimensions.
3. Prefer deterministic `rule_based` judges; use `script` for executable artifacts and calibrated `agent_judge` for necessary semantic judgments.
4. Run `skill-up validate`, then authorized runtime evaluations. Record metadata, traces, artifacts, and limitations.
5. Check evaluation validity, classify failures, and recommend bounded changes. Add regression cases only after confirming a real failure’s root cause.

**Trigger / process / outcome / artifact / semantic evidence:** Trigger verification is `BLOCKED` because no observed `skill.selection` trace was assessed. Runtime process, outcome, artifact, and semantic effectiveness are `UNASSESSED`. Static validation alone cannot establish runtime effectiveness or release readiness.

**Benchmark results:** `NOT_RUN`. Benchmark means comparing with versus without the Skill.

**Regression findings:** `NOT_RUN`. Version Regression means comparing previous versus current versions under comparable conditions.

**Flaky / blocked / infrastructure errors:** Flakiness and infrastructure behavior are `UNASSESSED`; no execution occurred.

**Eval validity findings:** The proposal conflicts with explicit scope constraints. Evidence is insufficient to attribute any runtime Skill, Eval, or Infrastructure defect; attribution remains `Unknown`. Quality Score remains owned by the existing governance contract.

**Limitations and evidence states:** `PASS` means a criterion is satisfied; `FAIL`, contradicted; `BLOCKED`, required evidence is unavailable; `NOT_RUN`, execution did not occur; `NOT_SCORED`, no score was assigned; `UNASSESSED`, a dimension was not examined; `INSUFFICIENT_EVIDENCE`, evidence cannot support a conclusion. Quality Score is `NOT_SCORED`; effectiveness claims have `INSUFFICIENT_EVIDENCE`.

**Recommended actions:** Reject the replacement architecture and automatic modification loop. Identify concrete gaps in the existing workflow, address them through bounded case or judge improvements, and rerun authorized evaluations through `skill-up`. Keep Skill edits separately reviewed and preserve existing scoring and release governance.
