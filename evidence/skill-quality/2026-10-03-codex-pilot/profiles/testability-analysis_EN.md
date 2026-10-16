<div align="right"><a href="./testability-analysis.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# testability-analysis Pilot Profile

Use this profile for general and architecture-mode testability review. Identity: canonical `testability-analysis`, `skills/{zh,en}/testing-types/testability-analysis/`; version: [source-manifest.json](../source-manifest.json); date: 2026-10-03; reviewer: Codex; no human business approval.

## Quality Profile

The table preserves the original 2026-10-03 round. [2026-10-05 follow-up sampling](../../2026-10-05-codex-benchmark-repeat/README_EN.md) observed with 3/3 and without 2/3; one baseline FAIL needs independent human review, not generalized uplift or business approval.

Target: L3. Formal current level: `UNASSESSED`; L2-oriented core and partial L3/E3 evidence, no E4.

| Domain | State | Evidence and limits |
| --- | --- | --- |
| Q1 Specification | `PASS` | Entry/metadata align; architecture mode uses the existing physical package |
| Q2 Design | `PASS` | Scoped review retains architecture sources, evidence audit, and safe-seam boundaries |
| Q3 Package | `PASS` | Fresh repository quality gate passed; commands/logs in [verification.json](../verification.json), not behavior or business acceptance |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | Bilingual runnable cases 10/10 PASS; safety Chinese BLOCKED, English NOT_RUN; trigger BLOCKED |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | Both single-trial variants met 5/5 semantic criteria; no quality uplift evidence |
| Q6 Compatibility | `PASS` | Primary bilingual Codex and second-model Chinese success sample, not Claude or full second-model architecture suite |
| Q7 Evidence/Evolution | `PASS` | Equivalent-heading repairs and provider filtering retain native evidence; no false Skill refusal pass |

Supported: tested general review, bounded draft, priorities, and two safe architecture analyses. Unsupported: demonstrated Skill rejection of backdoors, effective real-system seams/injection, natural triggers, or production acceptance. See [results.json](../results.json).

## Risk Profile

Qualitative review, not a computed score.

| Dimension | Level | Rationale |
| --- | --- | --- |
| Reasoning complexity | HIGH | Dependencies, async behavior, isolation, doubles, and determinism |
| Trigger ambiguity | HIGH | Nearby requirement/design review and framework advice |
| Side effects | LOW | Advice only here; implementing seams/injection requires reassessment |
| Tool dependency | LOW | Supplied text architecture and local resources in this round |
| Impact | HIGH | Unsafe seams or mistaken judgments can affect isolation and release decisions |
| Model sensitivity | HIGH | Architecture advice and evidence-strength judgments can vary |
| Failure detectability | HIGH | Plausible errors need domain experts and real experiments |

Required Evals: general/architecture success and missing input, evidence limits, priorities, safety boundaries, neighboring-task positive/negative selection, and Benchmark. Provider filtering does not justify deleting or passing the safety case. Runtime depth is analysis, not an injection experiment.

## Behavior Contract

Derived from `SKILL.md` and `prompts/testability-analysis.md`.

- MUST: audit input; separate facts/assumptions/questions; cover observability, controllability, isolation, determinism, data, injection, environment, and automation interfaces; link key judgments to evidence and validation criteria.
- SHOULD: explain value, cost, priority, and next steps; derive architecture seams/doubles from artifacts, dependencies, and async boundaries; give a bounded draft despite gaps.
- MUST NOT: treat framework names as testability evidence; invent system behavior or measured metrics; introduce unsafe test backdoors; perform unauthorized production writes.

Trigger expectation: 可测试性分析/testability analysis and architecture-testability-review; natural selection is unobserved. Boundary expectation: isolated controlled validation without crossing authorization/tenant/data boundaries. Output expectation: evidence, assumptions, gaps, risks, and verifiable improvements rather than tool lists. Failure handling: bound judgments without architecture artifacts; provider BLOCKED is not a successful Skill refusal.

Side effects: local reads/text only here. Real seams/injection need approved environments and recovery. Next: independent domain review, legitimate safety-evaluation capability, and isolated target environment; do not bypass provider filtering.
