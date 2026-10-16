# Skill Quality CI Guide

## Pull Request

Recommended checks:

```text
Static Validation
Changed-Skill Eval
Critical Behavior Eval
Regression Smoke
```

## Release

Recommended checks:

```text
PR Gate
Full relevant Eval
Critical Regression
Selected Benchmark
Selected Compatibility
Evidence Report
Known Gaps declaration
```

## Scheduled Evaluation

Use scheduled runs for higher-cost validation such as:

- cross-model sampling;
- cross-agent sampling;
- extended benchmarks;
- longitudinal regression.

## Change-based Validation

| Change | Likely impact | Recommended validation |
|---|---|---|
| description / trigger metadata | Discovery, trigger, selection | Positive, Negative, Boundary |
| workflow instructions | Behavior, trajectory | Behavior, Regression, Runtime |
| references | Evidence use, output | Behavior, Regression |
| scripts/tools | Runtime, side effects | Runtime, side_effect, Regression |
| Eval definition | Evidence validity | Eval review / calibration |

## Gate Principle

```text
Quality Claim <= Available Evidence
```

CI success must not be presented as broader runtime or real-world evidence than
the executed checks actually support.
