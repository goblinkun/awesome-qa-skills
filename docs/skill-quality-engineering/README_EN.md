<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Skill Quality Engineering Toolkit (SQET)

> Version: 1.0  
> Core model: Skill Quality Evaluation Model (SQEM)  
> Current status: Pilot validation

SQET is the Skill quality-engineering methodology layer for Awesome QA Skills. It covers Agent Skill design, evaluation, validation, evolution, and review. It is documentation and standards, not an installable Skill and not a second Eval Engine.

## Documentation entrypoints

- [Skill Quality Evaluation Model (SQEM)](./SKILL_QUALITY_EVALUATION_MODEL_EN.md): seven quality domains, L1-L4 validation levels, E1-E4 evidence levels, and the Quality Claim Gate.
- [Skill Eval Contract](./SKILL_EVAL_CONTRACT_EN.md): case types, judges, run metadata, failure classification, and evidence states.
- [SQEM Pilot](./SKILL_QUALITY_PILOT_EN.md): five SQEM methodology Pilot candidates, stages, metrics, and exit criteria.

### Templates

- [Behavior Contract](./templates/SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md)
- [Evidence Report](./templates/SKILL_EVIDENCE_REPORT_TEMPLATE.md)
- [Quality CI Guide](./templates/SKILL_QUALITY_CI_GUIDE.md)
- [Quality Profile](./templates/SKILL_QUALITY_PROFILE_TEMPLATE.md)
- [Risk Profile](./templates/SKILL_RISK_PROFILE_TEMPLATE.md)

## Relationship to other repository layers

- `skills/{zh,en}/skill-engineering/` contains callable Agent Skills. SQET describes quality methods and standards; it does not replace those Skills.
- `evals/` contains each Skill's Eval configuration and cases. SQET does not create a second repository-wide case store.
- `evidence/skill-quality/` contains reviewed or runner-generated quality evidence. Without runtime evidence, keep results at `NOT_RUN`, `BLOCKED`, `UNASSESSED`, `NOT_SCORED`, or `INSUFFICIENT_EVIDENCE`.
- Website articles are site content, not Toolkit methodology entrypoints.

## Existing sources of truth

SQET reuses the repository's existing governance contracts instead of redefining the same rules:

- [Quality Score and minimum Eval contract](../governance/QUALITY_SCORE_EVAL_CONTRACT_EN.md) owns the nine-dimensional Quality Score and minimum Eval requirements.
- [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT_EN.md) owns evidence states, failure classification, and structured Router `skill.selection` / `selected_skills` evidence.
- [Skill Evaluation Quality Loop](../governance/SKILL_EVALUATION_DESIGN_EN.md) owns the existing `skill-up`, local trace rules, and evaluation workflow boundaries.
- [Existing Skill Evaluation Pilots](../governance/SKILL_EVALUATION_PILOTS_EN.md) records the existing `requirements-analysis`, `ui-test-playwright`, and `discover-testing` Pilots.

The current SQET conclusion is therefore **Pilot validation**, not repository-wide runtime-quality proof, cross-model compatibility proof, business acceptance, or release approval. The central rule is:

```text
Quality Claim <= Available Evidence
```

When real Agents, target environments, cross-model sampling, or business-acceptance evidence are unavailable, documents and reports must state the limitation. Static gates and `skill-up validate` must not be presented as runtime-effectiveness conclusions.
