<div align="right"><a href="./performance-testing.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# performance-testing Pilot Profile

Use this profile for performance-test plans, not actual load-test results. Identity: canonical `performance-testing`, `skills/{zh,en}/testing-types/performance-testing/`; version: [source-manifest.json](../source-manifest.json); date: 2026-10-03; reviewer: Codex; no human business approval.

## Quality Profile

Target: L2 plus partial L3. Formal current level: `UNASSESSED`. This round has L2-oriented text cases and scoped Codex E3 samples, not real load experiments/E4.

| Domain | State | Evidence and limits |
| --- | --- | --- |
| Q1 Specification | `PASS` | Entry/directory/metadata align; snapshot is reviewable |
| Q2 Design | `PASS` | Scoped review separates performance objectives/load/metrics from other specialties |
| Q3 Package | `PASS` | Fresh repository quality gate passed; commands/logs in [verification.json](../verification.json), not behavior or business acceptance |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | Bilingual text cases 6/6 PASS; real load and natural selection unproven |
| Q5 Effectiveness | `NOT_RUN` | Not among the three selected Benchmarks; no uplift claim |
| Q6 Compatibility | `PASS` | Primary bilingual Codex and second-model Chinese success case, not a full domain-correctness matrix |
| Q7 Evidence/Evolution | `PASS` | Missing-input assertion repair and real rerun are traceable |

Supported: text plans for scope/objectives, load assumptions, test types, criteria, and environments. Unsupported: measured QPS/p95/capacity/improvements, real load tests, stability, or business acceptance. Cases are in [results.json](../results.json).

## Risk Profile

Qualitative judgments; reassess actual target risk.

| Dimension | Level | Rationale |
| --- | --- | --- |
| Reasoning complexity | HIGH | Load models, metrics, bottlenecks, and environment differences interact |
| Trigger ambiguity | MEDIUM | Near capacity planning and performance diagnosis |
| Side effects | LOW | Plans only here; real load can be HIGH and needs separate authority |
| Tool dependency | LOW | Text here; real load needs tools, monitoring, and a target |
| Impact | HIGH | Invalid criteria/load assumptions can mislead capacity/release decisions |
| Model sensitivity | HIGH | Domain advice and unsupported numbers can vary |
| Failure detectability | HIGH | Plausible plans need real data and performance experts |

Required Evals: success, missing objectives/environment, domain boundaries, load/units/criteria, and model sensitivity. Real load requires separate inputs, budget, stop thresholds, and recovery. These checks do not replace actual tools.

## Behavior Contract

Derived from `SKILL.md` and `prompts/performance-testing.md`.

- MUST: read the main prompt; identify scope, objectives, transactions, traffic/concurrency assumptions, types, success criteria, data, environment, monitoring, and risks; separate facts and assumptions.
- SHOULD: prioritize high-risk transactions; provide executable plans/validation methods; mark unknown criteria and distinguish proposed numbers from requirements.
- MUST NOT: invent interfaces, environments, capacity, measurements, or causes; replace load objectives with functional/security cases; present unrun load tests as passes.

Trigger expectation: 性能测试/performance testing and load/stress/spike/endurance/capacity objectives; natural selection BLOCKED. Boundary expectation: plans are not executed load tests or accepted optimizations. Output expectation: linked load/metrics/environment/data/limits, not one required “pending confirmation” phrase. Failure handling: give a bounded draft and enumerate gaps blocking measurements.

Side effects: no target traffic in this round. Next: real SLOs, sanitized transactions, approved load environment, traffic budget, stop conditions, and monitoring; do not stress production without authority.
