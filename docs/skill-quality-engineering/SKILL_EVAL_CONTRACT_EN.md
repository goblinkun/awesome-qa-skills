<div align="right"><a href="./SKILL_EVAL_CONTRACT.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Skill Eval Contract

> Version: 1.0  
> Related specification: Skill Quality Evaluation Model (SQEM)

## 1. Purpose

The Skill Eval Contract defines a portable conceptual structure for describing how an Agent Skill should be evaluated.

It is runner-independent. Implementations may map it to Skill-Up, OpenAI evaluation workflows, repository scripts, custom Agent harnesses, or CI pipelines.

## Repository alignment boundary

Within this repository, the contract reuses the [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT_EN.md) for evidence states, failure classification, and report structure. Quality Score ownership remains with the [Quality Score and minimum Eval contract](../governance/QUALITY_SCORE_EVAL_CONTRACT_EN.md). This contract introduces neither a second scoring system nor a replacement for the existing `skill-up` evaluation engine.

For Router cases, observed selection must come from a structured `skill.selection` trace or an explicit trace adapter that provides `route`, `primary`, `optional`, and `selected_skills`. `selected_skills` must be exactly one primary Skill plus at most one optional Skill; missing or invalid fields are `BLOCKED`, while mismatches or extra selections are `FAIL`. Plain-text recommendations, Composition Recipes, or static configuration alone do not prove a real selection.

## 2. Eval Case Model

A Skill Eval Case SHOULD contain:

```yaml
id: unique-case-id
skill: canonical-skill-name
type: positive

task:
  input: |
    User task goes here.

context:
  files: []
  environment: {}

expected:
  trigger: true

behavior:
  must: []
  should: []
  must_not: []

artifacts:
  required: []
  forbidden: []

side_effects:
  allowed: []
  forbidden: []

evaluation:
  methods: []

evidence:
  capture:
    - output
    - trajectory
    - artifacts
```

Not every field is required for every case.

## 3. Case Types

```text
positive
negative
boundary
behavior
regression
paraphrase
adversarial
benchmark
compatibility
trajectory
side_effect
```

## 4. Positive Case

Purpose: verify that the Skill is selected and behaves correctly for a representative intended task.

```yaml
id: functional-testing-positive-001
skill: functional-testing
type: positive

task:
  input: |
    Design functional tests for an e-commerce checkout flow.

expected:
  trigger: true

behavior:
  must:
    - identify_primary_business_flow
    - cover_positive_path
    - cover_negative_paths
    - identify_test_data

  must_not:
    - invent_missing_business_rules
```

## 5. Negative Case

Purpose: verify that the Skill does not activate for an unrelated task.

```yaml
id: functional-testing-negative-001
skill: functional-testing
type: negative

task:
  input: |
    Fix this Playwright locator.

expected:
  trigger: false
```

## 6. Boundary Case

Purpose: verify differentiation between adjacent Skills.

```yaml
id: functional-testing-boundary-001
skill: functional-testing
type: boundary

task:
  input: |
    Review this requirement and determine whether it is testable
    before functional test design begins.

expected:
  preferred_skill:
    - testability-analysis

  unexpected_skill:
    - functional-testing
```

## 7. Behavior Case

Purpose: verify observable Skill behavior.

```yaml
id: requirement-quality-behavior-001
skill: requirement-quality-review
type: behavior

behavior:
  must:
    - identify_requirement_gaps
    - separate_fact_from_assumption
    - identify_missing_evidence

  should:
    - prioritize_findings

  must_not:
    - invent_business_rules
    - provide_unsupported_release_approval
```

## 8. Regression Case

Every regression case SHOULD contain provenance.

```yaml
id: functional-testing-regression-017
skill: functional-testing
type: regression

provenance:
  source: real_failure
  reference: issue-17
  first_observed_version: 1.5.2

failure:
  description: >
    Skill omitted the negative payment path when the requirement
    contained an incomplete payment rule.

expected:
  behavior:
    must:
      - identify_missing_payment_rule
      - preserve_unknown_business_boundary
```

Regression cases should explain why they exist.

## 9. Benchmark Case

Benchmark cases compare controlled configurations.

```yaml
id: functional-testing-benchmark-001
skill: functional-testing
type: benchmark

variants:
  - without_skill
  - with_skill

controls:
  same_task: true
  same_model: true
  same_agent: true
  same_environment: true

metrics:
  - task_success
  - critical_coverage
  - unsupported_claims
  - tokens
  - latency
```

Avoid changing multiple independent variables between variants.

## 10. Compatibility Case

```yaml
id: functional-testing-compatibility-001
skill: functional-testing
type: compatibility

matrix:
  agents:
    - codex
    - claude-code

  models:
    - configured-model-a
    - configured-model-b

behavior:
  must:
    - preserve_core_behavior_contract
```

Only report environments actually executed.

## 11. Behavior Contract

Use MUST, SHOULD, and MUST NOT. Contracts should focus on observable behavior.

Bad:

```yaml
must:
  - provide_a_good_answer
```

Better:

```yaml
must:
  - identify_missing_acceptance_criteria
  - distinguish_fact_from_assumption
```

## 12. Evaluation Methods

### Deterministic
File exists, exit code, schema validity, required field, forbidden file absence.

### Rule-based
Required section, known risk categories, forbidden pattern.

### Script / Domain Evaluator
Use custom code for domain-specific checks.

### Agent Judge
Use when semantic judgment is required. Criteria must be explicit.

Bad: `Is this answer good?`

Better: `Does the output distinguish documented requirements from assumptions introduced by the model?`

### Human Review
Use for ambiguous cases, high-impact evaluation, Judge calibration, and real-world effectiveness review.

## 13. Evidence Capture

Potential evidence:

```text
Input
Skill version
Agent
Model
Environment
Output
Trajectory
Tool calls
Artifacts
Token usage
Latency
Judge result
Failure reason
```

Capture only what is useful for diagnosis and reproducibility.

## 14. Repeated Runs

For non-deterministic behavior, a runner may execute multiple runs, for example:

```yaml
runs:
  count: 3
```

Important cases may require larger samples. One run is not stability evidence.

## 15. Eval Result

Recommended conceptual result:

```yaml
result:
  status: PASS
  evidence_level: E2

  checks:
    trigger: PASS
    behavior: PASS
    artifacts: PASS

  observations: []
  limitations: []
```

Allowed statuses:

```text
PASS
FAIL
NOT_RUN
BLOCKED
NOT_SCORED
UNASSESSED
INSUFFICIENT_EVIDENCE
```

`NOT_SCORED` means that no valid Quality Score exists, `UNASSESSED` means that the dimension was outside the current evaluation scope, and `INSUFFICIENT_EVIDENCE` means that some trace exists but does not support a strong claim. None is a passing state.

## 16. Eval Quality

Review important Eval Cases for:

- realism;
- coverage;
- discriminative power;
- repeatability;
- independence;
- Judge reliability.

An Eval that cannot distinguish a useful Skill from the baseline may need improvement.

## 17. Contract Portability

The contract defines semantic intent:

```text
Skill Eval Contract
       |
       +-- Skill-Up Adapter
       +-- OpenAI Eval Adapter
       +-- Custom Harness Adapter
       +-- CI Adapter
```

This prevents the quality model from depending on one Eval framework.
