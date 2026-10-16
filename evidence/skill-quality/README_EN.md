<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Skill Quality Evidence

This directory stores reviewed or runner-generated Skill quality guidance and report assets. Each report must state its own runtime scope, models, versions, unrun checks, and supported claims; one Pilot cannot establish repository-wide acceptance.

## Available Reports

- [2026-10-05 Codex Benchmark repeated sampling](./2026-10-05-codex-benchmark-repeat/README_EN.md): two more pairs per existing Chinese task, three samples per variant including the original; interrupted calls/costs retained separately, not business acceptance or statistical uplift.
- [2026-10-03 Codex SQET Pilot](./2026-10-03-codex-pilot/README_EN.md): five Skills' bilingual text core runs, three selected single-trial Benchmarks, second-model sampling, cost, and native evidence. Natural triggers, the blocked safety boundary, Claude, and business acceptance retain the report's unverified states.

## Minimum record fields

Reviewable evidence should record at least:

- Skill commit or version;
- Eval version and case id;
- engine, provider, and requested/observed model;
- judge type and judge model, when applicable;
- environment and timestamp;
- result, failure classification, and trace/artifact locations;
- limitations;
- the quality claims the evidence does and does not support.

Use `unknown` for unavailable values; do not guess. Do not write credentials, cookies, Bearer tokens, or unnecessary sensitive content into evidence.

## Evidence states and claim boundary

Evidence reports should use the repository's existing `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_SCORED`, `UNASSESSED`, and `INSUFFICIENT_EVIDENCE` semantics. Without real Agent, target-environment, cross-model, or business-acceptance evidence, keep the result at `NOT_RUN`, `BLOCKED`, or `INSUFFICIENT_EVIDENCE`; static gates and `skill-up validate` cannot be promoted to runtime-quality, compatibility, business-effectiveness, or release-approval claims.

Evidence may support only quality claims proportionate to its level:

```text
Quality Claim <= Available Evidence
```

See [SQET](../../docs/skill-quality-engineering/README_EN.md) for methodology and [Skill Evaluation Contract](../../docs/governance/SKILL_EVALUATION_CONTRACT_EN.md) for states and report structure.
