# Skill Evaluation Report

## Scope

**Design only; execution status: `NOT_RUN`.** This report proposes an evaluation of the reporting behavior described by the local [Skill contract](.agents/skills/skill-evaluation/SKILL.md) and [evaluation prompt](.agents/skills/skill-evaluation/prompts/skill-evaluation.md).

No runtime target, candidate version, historical failures, traces, or artifacts were supplied. The design covers outcomes, process compliance, semantic quality, triggers, and comparison methods. Efficiency measurement is deferred until comparable runtime data exists.

## Evidence Boundaries

Only local Skill guidance was read through shell commands. Evaluation assertions and evaluator inputs were not read. No browser, computer-use, MCP, external service, evaluation execution, or production writes were used.

The guidance establishes requirements; it does not demonstrate that a Skill meets them. Proposed assertions below are design criteria, not inspected evaluator assertions.

Evidence states:

| State | Meaning |
|---|---|
| `PASS` | Valid evidence satisfies the specified assertion. |
| `FAIL` | Valid evidence contradicts the specified assertion. |
| `BLOCKED` | Required evidence or a prerequisite is unavailable. |
| `NOT_RUN` | The check was not executed. |
| `NOT_SCORED` | No applicable score was produced. |
| `UNASSESSED` | Available material has not been judged. |
| `INSUFFICIENT_EVIDENCE` | Evidence cannot support the requested conclusion. |

## Run Metadata

| Field | Value |
|---|---|
| Activity | Local contract review and evaluation design |
| Report date | 2026-10-03, from supplied environment |
| Evaluation run ID / execution timestamp | `unknown` / `unknown` |
| Target Skill / language / version | `unknown` / `unknown` / `unknown` |
| Eval version / `skill-up` version | `unknown` / `unknown` |
| Engine / provider / model | `unknown` / `unknown` / `unknown` |
| Executed judges | None |
| Environment | Local workspace, zsh; text-only task |
| Static validation / runtime execution | `NOT_RUN` / `NOT_RUN` |

## Configuration and Coverage

Use `skill-up` as the evaluation engine. Prefer `rule_based` checks for required fields, canonical states, prohibited claims, and recorded events. Use `script` judges when executable artifacts require verification.

Use `agent_judge` only for semantic questions such as whether a conclusion accurately reflects its evidence. Its rubric should require identifiable supporting evidence, correct uncertainty, and justified attribution. Calibrate it on independently labeled examples, including ambiguous cases, before using it as a gate.

## Summary

The local contract supports the following evaluation design. Skill effectiveness remains `INSUFFICIENT_EVIDENCE`; trigger behavior is `BLOCKED`; no runtime case has passed or failed.

## Case Results

All cases are **proposed**, with execution state `NOT_RUN`.

| ID / type | Input scenario | Observable assertion | Judge | Limitation |
|---|---|---|---|---|
| C1 HAPPY | Complete evidence bundle with known outcomes | Conclusions identify supporting cases, judges, metadata, and evidence states | `rule_based` + calibrated `agent_judge` | No bundle supplied |
| C2 INCOMPLETE | Missing target, traces, and model metadata | Uses `unknown` and canonical states; retains report skeleton; invents no results | `rule_based` + calibrated `agent_judge` | No output generated for judging |
| C3 EXPLICIT_TRIGGER | User explicitly invokes the Skill | Trace contains the expected `skill.selection` event | `rule_based` trace check | Selection trace absent: `BLOCKED` |
| C4 IMPLICIT_TRIGGER | User asks to design a Skill evaluation without naming it | Trace records intended Skill selection | `rule_based` trace check | Selection trace absent: `BLOCKED` |
| C5 CONTEXTUAL_TRIGGER | A follow-up requests judge or regression analysis within an evaluation task | Selection matches the contextual trigger contract | `rule_based` trace check | Context and selection trace unavailable |
| C6 NEGATIVE_TRIGGER | Clearly unrelated request | Complete selection telemetry shows no selection of this Skill | `rule_based` trace check | Missing telemetry cannot prove non-selection |
| C7 BOUNDARY | Text-only request forbids external access and evaluator-input reads | Report respects restrictions and does not turn static review into runtime claims | `rule_based` action trace + calibrated `agent_judge` | Full action trace unavailable |
| C8 ATTRIBUTION | Evidence variants expose Skill, Eval, infrastructure, or ambiguous failure | Attribution follows demonstrated cause; ambiguity remains Unknown | Calibrated `agent_judge`; deterministic checks where possible | Labeled examples unavailable |
| C9 REGRESSION | Reproduction of a confirmed historical failure | Current version fixes the original behavior under comparable conditions | Original failure’s applicable judge | No confirmed failure supplied; do not invent one |

## Trigger / Process / Outcome / Artifact / Semantic Evidence

| Dimension | Current state | Supported conclusion |
|---|---|---|
| Trigger | `BLOCKED` | No `skill.selection` evidence; similar output cannot establish selection |
| Process | `UNASSESSED` | Requirements were read; target execution was not assessed |
| Outcome | `NOT_RUN` | No runtime outcome exists |
| Artifact | `NOT_RUN` | No executable artifact was evaluated |
| Semantic | `UNASSESSED` | No calibrated semantic judgment was performed |
| Efficiency | `NOT_SCORED` | No comparable latency, token, or cost measurements |

## Benchmark Results

**`NOT_RUN`.** A benchmark compares **with Skill versus without Skill** using matched cases, model settings, tools, environment, and judges. Report per-case outcomes and observed resource use, including variability. No benefit or business-impact claim is supported here.

## Regression Findings

**`NOT_RUN`.** Version regression compares **previous versus current Skill versions** under comparable conditions. Preserve version identities, original failure evidence, and reproduction details. No improvement or deterioration claim is supported.

## Flaky / Blocked / Infrastructure Errors

Trigger checks are `BLOCKED` by missing selection telemetry. Flakiness is `UNASSESSED` because there are no repeated runs. Infrastructure failures are `UNASSESSED`; absence of execution does not establish an infrastructure defect.

## Eval Validity Findings

Validity is `UNASSESSED`. Before interpreting failures, verify fixture correctness, assertion alignment, trace completeness, judge calibration, and comparison fairness.

Classify demonstrated failures separately:

- **Skill Defect:** valid input and evaluation show behavior violating the Skill contract.
- **Eval Defect:** faulty fixtures, assertions, or judges create an incorrect result.
- **Infrastructure Defect:** execution or evidence collection fails independently of Skill behavior.
- **Unknown:** evidence cannot support attribution.

`skill-up validate` establishes static validity within its checks; it does not prove runtime semantics. Smoke checks or isolated successes cannot establish release readiness. Quality Score remains governed by the existing contract; none is created here.

## Limitations

The target, fixtures, runtime evidence, historical failures, judge calibration, and comparison baselines are unavailable. All effectiveness, benchmark, and regression conclusions remain `INSUFFICIENT_EVIDENCE`.

## Recommended Actions

1. Identify the target Skill, version, language, critical behaviors, and permitted evaluation inputs.
2. Implement the smallest useful cases above; calibrate semantic judges before gating.
3. Run `skill-up validate`, then authorized runtime evaluations with complete metadata and `skill.selection` capture.
4. Review evaluation validity before assigning failure causes.
5. Run benchmarks and version regressions separately; add regression cases only after confirming real failures and root causes.
6. Preserve blocked and unknown states until evidence supports a stronger conclusion.
