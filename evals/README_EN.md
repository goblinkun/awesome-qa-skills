<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Root Skill Eval Directory Boundary

## Default source of truth

Each Skill's local `eval.yaml` and `cases/` are the default source of truth for its Eval, located at:

```text
skills/{zh,en}/<category>/<skill>/evals/
```

Evaluation design, configuration, and cases should be maintained with the corresponding Skill so that the Skill remains independently installable, reviewable, and evolvable. The root `evals/` directory does not move, copy, or redeclare existing Skill-local cases.

## What may live at the root

Only separately designed assets with an explicit owner belong at the root, such as:

- runner-adapted cross-Skill composition assets;
- aggregation or comparison assets that explicitly serve multiple Skills;
- evaluation guidance coupled to repository governance gates.

Every new root asset must state its input sources, scope, execution method, evidence artifacts, and relationship to Skill-local Evals. It must not become a second Eval Engine or an implicit repository-wide case store.

## Quality-claim boundary

An Eval configuration can pass static or structural checks without proving model, Agent, target-environment, or business outcomes. Content that was not executed must remain `NOT_RUN`, `BLOCKED`, `UNASSESSED`, `NOT_SCORED`, or `INSUFFICIENT_EVIDENCE`; it must not be promoted to a quality pass, runtime-compatibility claim, or release approval.

See the [SQET entrypoint](../docs/skill-quality-engineering/README_EN.md) and [Skill Evaluation Contract](../docs/governance/SKILL_EVALUATION_CONTRACT_EN.md) for methodology and status definitions.
