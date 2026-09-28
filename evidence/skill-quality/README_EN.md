<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Skill Quality Evidence

This directory is for reviewed or runner-generated Skill quality evidence guidance and report assets. This change creates the directory boundary only: it does not create an Evidence Report instance or claim any runtime result.

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
