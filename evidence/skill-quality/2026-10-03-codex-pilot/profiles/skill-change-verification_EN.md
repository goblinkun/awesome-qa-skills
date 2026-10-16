<div align="right"><a href="./skill-change-verification.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# skill-change-verification Pilot Profile

Use this profile for change-impact verification selection and evidence claims. Identity: canonical `skill-change-verification`, `skills/{zh,en}/skill-engineering/skill-change-verification/`; version: [source-manifest.json](../source-manifest.json); date: 2026-10-03; reviewer: Codex; no human business approval.

## Quality Profile

Target: L3. Formal current level: `UNASSESSED`; core and partial compatibility E3, no E4.

| Domain | State | Evidence and limits |
| --- | --- | --- |
| Q1 Specification | `PASS` | Canonical identity, entry, metadata, and language directories align |
| Q2 Design | `PASS` | Scoped review retains change classification, minimum sufficient checks, and claim boundaries |
| Q3 Package | `PASS` | Fresh repository quality gate passed; commands/logs in [verification.json](../verification.json), not behavior or business acceptance |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | Bilingual text cases 6/6 PASS; advice cannot prove executed verification or natural selection |
| Q5 Effectiveness | `NOT_RUN` | Not among selected Benchmarks; no uplift claim |
| Q6 Compatibility | `PASS` | Primary bilingual Codex and second-model Chinese success sample; Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | Cases, native answers/grading, scope, and unknowns are traceable |

Supported: verification selection for supplied changes, incomplete input, and evidence-boundary reports. Unsupported: suggested commands executed, version regression passed, or business/release approval. See [results.json](../results.json).

## Risk Profile

Qualitative review, not an automatic score.

| Dimension | Level | Rationale |
| --- | --- | --- |
| Reasoning complexity | MEDIUM | Changes must map to the right verification layers |
| Trigger ambiguity | MEDIUM | Near evaluation design, code review, and release gates |
| Side effects | LOW | Selection/reporting here; reassess real commands by their effects |
| Tool dependency | MEDIUM | Real verification needs repository commands and runtime |
| Impact | HIGH | Gaps or exaggerated claims can cause incorrect delivery decisions |
| Model sensitivity | MEDIUM | Minimum check selection and evidence layering may vary |
| Failure detectability | HIGH | A full green gate can hide change-specific gaps |

Required Evals: supplied changes, unknown changes/commands, scope/risk, static versus runtime evidence, and real-failure regression. Runtime depth here is reporting, not executing tests in arbitrary projects.

## Behavior Contract

Derived from `SKILL.md` and `prompts/skill-change-verification.md`.

- MUST: classify content, metadata/directories, scripts, Evals, and runtime impact; choose matching checks; record executed/unexecuted checks, results, and reasons; state residual risks and supported/unsupported claims.
- SHOULD: choose the minimum sufficient checks covering actual changes; separate static, structural, evaluation, runtime, and human review.
- MUST NOT: treat skill-up validate as runtime semantic success; invent unknown project commands; hide actual gaps behind full-suite checks; present unrun checks as executed.

Trigger expectation: Skill 变更验证/quality gates/evidence level; natural selection BLOCKED. Boundary expectation: advice does not grant release/business approval. Output expectation: commands, evidence layers, unknowns, residual risk, and actions. Failure handling: without diff/rules/commands, give bounded verification options and preserve unknowns.

Side effects: local Skill reads/text only here; generated files/external actions from real checks remain within user scope. Next: real change diff and runnable project, execute selected checks, then have the accountable owner confirm claim boundaries.
