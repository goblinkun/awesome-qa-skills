<div align="right"><a href="./functional-testing.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# functional-testing Pilot Profile

Use this profile to review scope, behavior, and evidence. Identity: canonical `functional-testing`, `skills/{zh,en}/testing-types/functional-testing/`; version: [base plus worktree snapshot](../source-manifest.json); date: 2026-10-03; reviewer: Codex; no human business approval.

## Quality Profile

The table preserves the original 2026-10-03 round. [2026-10-05 follow-up sampling](../../2026-10-05-codex-benchmark-repeat/README_EN.md) passed all three trials per variant on the same task, without upgrading levels or statistical-uplift claims.

Target: L3. Current formal level: `UNASSESSED`. L2-oriented core and partial L3 evidence were collected, up to scoped E3, not E4.

| Domain | State | Evidence and limits |
| --- | --- | --- |
| Q1 Specification | `PASS` | Entry/frontmatter/metadata align; current files have SHA256 identities; specification only |
| Q2 Design | `PASS` | Scoped review separates functional coverage from performance/security specialties; contract below |
| Q3 Package | `PASS` | Fresh repository quality gate passed; commands/logs in [verification.json](../verification.json), not behavior or business acceptance |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | Bilingual explicit-use text cases 6/6 PASS; natural selection BLOCKED, no overall reliability claim |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | Both single-trial variants met 5/5 semantic criteria; no quality uplift observed |
| Q6 Compatibility | `PASS` | Bilingual primary Codex plus second-model Chinese success sampling; Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | Native results, historical assertion failures, regrades, reruns, and limits are traceable |

Supported: the tested risk-oriented plan, incomplete-input draft, and scope/priority boundary succeeded. Unsupported: automatic trigger, executed functional tests, statistical uplift, production/release acceptance. See this Skill's cases in [results.json](../results.json).

## Risk Profile

These are review judgments, not automatic scores. Target systems can change risk.

| Dimension | Level | Rationale |
| --- | --- | --- |
| Reasoning complexity | MEDIUM | Relating flows, data, and failure paths |
| Trigger ambiguity | MEDIUM | Overlap with daily testing, API/UI, and strategy tasks |
| Side effects | LOW | This Pilot outputs plans; execution needs separate authority |
| Tool dependency | LOW | Text planning needs only local Skill resources |
| Impact | HIGH | Missing payment, fulfillment, or permission risk can mislead release decisions |
| Model sensitivity | MEDIUM | Risk ranking and gap handling can vary |
| Failure detectability | MEDIUM | Text coverage is checkable; omissions need domain review |

Required Evals: success, incomplete input, priorities, domain boundaries, positive/negative triggers, difficult-task Benchmark, and real-failure regression. Compatibility is limited to reported Codex samples. Runtime depth is text, not UI/API execution.

## Behavior Contract

Derived from current `SKILL.md` and `prompts/functional-testing.md`; it adds no execution authority.

- MUST: read the main prompt; cover scope, critical flows, positive/failure/boundary cases, roles, data, and integrations; prioritize by business risk; distinguish facts, assumptions, and gaps.
- SHOULD: give actionable scenarios, expected outcomes, and next steps; provide a bounded draft with incomplete input; default to Markdown and honor explicit format requests.
- MUST NOT: invent interfaces, fields, environments, or causes; give everything the same priority; present plans as executed tests or unknown items as passes.

Trigger expectation: 功能测试/functional testing and functional plans/cases. Natural positive/negative selection is unobserved. Boundary expectation: this plan cannot replace specialist performance or penetration testing. Output expectation: concrete risks/cases and explicit gaps; fixed Chinese wording is not domain quality. Failure handling: preserve assumptions/questions when requirements or environment are missing; never fabricate results.

Side effects: local resource reads and text artifacts only in this round; no production writes authorized. Next: domain-reviewed requirements, natural selection traces, and finite repeated Benchmarks with sparse/difficult input.
