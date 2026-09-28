<div align="right"><a href="./SKILL_QUALITY_PILOT.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# SQEM Pilot Plan for Awesome QA Skills

> Version: 1.0<br>
> Purpose: Validate SQEM before repository-wide adoption.

## 1. Objective

The Pilot determines whether SQEM is understandable, practical, cost-effective, capable of finding real Skill defects, and maintainable at Awesome QA Skills scale.

The Pilot does not assume that SQEM v1.0 is correct. SQEM itself is a system under test.

The five Skills listed here are SQEM methodology Pilot candidates. They do not replace the repository's existing `requirements-analysis` analysis Pilot, `ui-test-playwright` executable Pilot, or `discover-testing` Router Composition Pilot. The existing Pilot configuration, evidence states, and execution boundaries are owned by the [existing Pilot contract](../governance/SKILL_EVALUATION_PILOTS_EN.md); this document adds SQEM quality-domain, risk, and method validation only.

## 2. Pilot Skills

### P1 - functional-testing
Type: General QA Skill<br>
Target: L3 Evaluated<br>
Focus: Trigger, Behavior, Benchmark, bilingual parity.

### P2 - testability-analysis
Type: Analytical QA Skill<br>
Target: L3 Evaluated<br>
Focus: Boundary, contrastive selection, unsupported assumptions, evidence handling.

### P3 - performance-testing
Type: Domain-specific QA Skill<br>
Target: L2 Verified + selected L3 evaluation<br>
Focus: Behavior, domain correctness, model sensitivity.

### P4 - skill-evaluation-design
Type: Skill Engineering<br>
Target: L3 Evaluated<br>
Focus: Behavior Contract, Eval design, Judge usage, risk-based selection.

### P5 - skill-change-verification
Type: Skill Engineering / Regression<br>
Target: L3 Evaluated<br>
Focus: Change impact, regression selection, evidence comparison, failure handling.

## 3. Pilot Stages

### Stage 1 - Inventory

For each Skill collect:

```text
Canonical name
Current structure
English variant
Chinese variant
References
Scripts
Current Evals
Known issues
Adjacent Skills
```

### Stage 2 - Risk Profile

Assess:

```text
Reasoning complexity
Trigger ambiguity
Side effects
Tool dependency
Impact
Model sensitivity
Failure detectability
```

Use LOW / MEDIUM / HIGH.

### Stage 3 - Q1-Q3 Validation

Execute specification validation, design review, package validation, and localization consistency checks.

### Stage 4 - Behavior Contract

Define MUST, SHOULD, and MUST NOT for each Pilot Skill. Focus on capability-defining behavior and avoid over-specification.

### Stage 5 - Core Eval Suite

Guidance per Pilot:

```text
2-3 Positive
2 Negative
2 Boundary where applicable
2 Behavior
Existing Regression Cases
```

This is guidance, not a universal quota.

### Stage 6 - Runtime Evaluation

Run selected Evals in at least one real supported Agent environment. Capture trigger, output, useful trajectory, artifacts, failures, and runtime metadata.

When a real Agent, target environment, cross-model matrix, or business-acceptance evidence is unavailable, keep the result at `NOT_RUN`, `BLOCKED`, `NOT_SCORED`, or `INSUFFICIENT_EVIDENCE`. Static checks and `skill-up validate` must not be used as substitutes for runtime conclusions.

### Stage 7 - Benchmark

For selected Pilot Skills:

```text
functional-testing
testability-analysis
skill-evaluation-design
```

compare Without Skill vs With Skill under controlled conditions.

### Stage 8 - Compatibility Sampling

Do not test every combination. Use representative environments.

| Skill | Codex | Claude Code | Other selected Agent |
|---|---|---|---|
| functional-testing | Required | Recommended | Optional |
| testability-analysis | Required | Recommended | Optional |
| performance-testing | Required | Optional | Optional |
| skill-evaluation-design | Required | Recommended | Optional |
| skill-change-verification | Required | Recommended | Optional |

Exact environments depend on available runtime support.

### Stage 9 - Bilingual Parity

Validate EN/ZH capability parity, trigger parity, behavior parity, boundary parity, and output language.

Do not duplicate the entire Eval suite unless needed. Use representative bilingual cases.

## 4. Pilot Metrics

### Quality findings

Track:

- specification defects;
- package defects;
- trigger defects;
- boundary defects;
- behavior defects;
- regression defects;
- compatibility differences.

### Engineering cost

Track:

- Eval authoring time;
- Eval maintenance time;
- runtime cost;
- token cost;
- CI duration;
- failure triage time.

### Framework usefulness

Record whether SQEM:

- finds issues static checks miss;
- improves Skill boundaries;
- improves regression confidence;
- provides useful benchmark evidence;
- creates excessive maintenance.

## 5. Pilot Exit Criteria

The Pilot is successful if:

1. SQEM can be applied consistently to all five Pilot Skills.
2. Authors can understand the seven quality domains.
3. Core Eval Cases are practical to maintain.
4. Behavioral evaluation finds information unavailable from static checks alone.
5. Benchmark results provide actionable evidence.
6. Compatibility testing can use sampling rather than exhaustive execution.
7. Bilingual validation does not require full duplicate maintenance.
8. Regression Cases can be traced to real failures.
9. Runtime cost is measurable.
10. Redundant framework complexity can be identified before SQEM v1.1.

## 6. Expected Outputs

```text
5 Skill Quality Profiles
5 Risk Profiles
5 Behavior Contracts
Core Eval Suites
Selected Benchmarks
Compatibility Evidence
Pilot Cost Report
SQEM v1.1 Change Proposal
```

## 7. Decision after Pilot

Possible decisions:

```text
ADOPT
ADOPT_WITH_CHANGES
LIMITED_ADOPTION
REWORK
```
