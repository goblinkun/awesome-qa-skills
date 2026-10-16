<div align="right"><a href="./skill-evaluation.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# skill-evaluation Pilot Profile

Use this profile for evaluation design and evidence interpretation. The supplied `skill-evaluation-design` maps to existing canonical `skill-evaluation`, with no alias package. Directory: `skills/{zh,en}/skill-engineering/skill-evaluation/`; version: [source-manifest.json](../source-manifest.json); date: 2026-10-03; reviewer: Codex; no human business approval.

## Quality Profile

The table preserves the original 2026-10-03 round. [2026-10-05 follow-up sampling](../../2026-10-05-codex-benchmark-repeat/README_EN.md) observed with 3/3 and without 0/3, still only a task-specific canonical-state difference; baseline semantic judges did not run.

Target: L3. Formal current level: `UNASSESSED`; core and partial L3/E3 evidence, no E4.

| Domain | State | Evidence and limits |
| --- | --- | --- |
| Q1 Specification | `PASS` | Canonical identity/entry/metadata align; independent package |
| Q2 Design | `PASS` | Scoped review retains skill-up and existing score/state contracts, no second engine |
| Q3 Package | `PASS` | Fresh repository quality gate passed; commands/logs in [verification.json](../verification.json), not behavior or business acceptance |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | Latest full bilingual suites 6/6 PASS; sparse input retains canonical states; natural selection BLOCKED |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | Single-trial state-contract difference; baseline semantic judge did not run, no generalized uplift |
| Q6 Compatibility | `PASS` | Primary bilingual Codex and second-model Chinese success sample; Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | Old scope/judge misjudgments, near-miss negative, and real reruns are retained |

Supported: minimum evaluation design, states under missing runtime evidence, and scope review preserving the engine. Unsupported: natural selection, completed business evaluation, overall scoring, release approval, or previous/current version regression. See [results.json](../results.json).

## Risk Profile

Qualitative review, not a new score.

| Dimension | Level | Rationale |
| --- | --- | --- |
| Reasoning complexity | HIGH | Outcome/Process, validity, judges, and evidence layers must be separated |
| Trigger ambiguity | HIGH | Overlap with verification, governance, and ordinary test design |
| Side effects | MEDIUM | Authorized evaluations invoke models and create files; this round's main answers are text |
| Tool dependency | HIGH | Real evaluation depends on skill-up, runtime, traces, and judges |
| Impact | HIGH | False PASS/scores can mislead repository quality/release decisions |
| Model sensitivity | HIGH | State semantics and rubric selection can vary |
| Failure detectability | HIGH | Plausible reports can conflate static, trigger, and business evidence |

Required Evals: success, sparse input, state enums, scope review, missing trigger evidence, Benchmark versus regression, and positive/negative/near-miss judge calibration. Runtime depth follows task authority; evaluation design is not completed evaluation.

## Behavior Contract

Derived from `SKILL.md` and `prompts/skill-evaluation.md`.

- MUST: read the target contract and main prompt; use skill-up; prefer deterministic checks; select/calibrate semantic judges when needed; record metadata, cases, judges, limits, and failure classification; retain applicable canonical evidence states in minimal reports.
- SHOULD: select meaningful behavior/trigger/boundary/regression cases; derive Skill regressions only from diagnosed real failures; choose the least costly effective validation.
- MUST NOT: introduce a global Engine/Judge/Benchmark/Quality Score within this Skill workflow; invent traces/scores; infer observed triggers from similar outputs; promote static/single observations to business/release claims; automatically modify Skills indefinitely.

Trigger expectation: Skill evaluation/design/interpretation/regression; selection observation BLOCKED. Boundary expectation: scope review preserves the current flow; **Skill prose does not authorize ignoring separately authorized, higher-priority architecture requests**. Output expectation: scope, results, states, blocked checks, and actions without requiring translation of official English headings. Failure handling: unknown remains unknown; missing trace BLOCKED, unrun NOT_RUN, unscored NOT_SCORED.

Side effects: design is read/text only; real model/script execution stays within authority and must not automatically change Skills. Next: human-confirmed judge anchors, natural selection events, and real-project acceptance of the report's use.
