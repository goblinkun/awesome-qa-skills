# Skill Benchmark: performance-testing

**Date**: 2026-10-03T11:22:48Z
**Evals**: Performance testing: choose types and thresholds by risk, Performance testing: draft without SLA/traffic, Performance testing: not a security penetration list (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Performance testing: choose types and thresholds by risk (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)Task Understanding (?i)Performance Risk (?i)(metric|measurement) (?i)(load model|traffic model|scenario plan|workload)]} | ✅ | output satisfies all regex checks (all:[(?i)Task Understanding (?i)Performance Risk (?i)(metric|measurement) (?i)(load model|traffic model|scenario plan|workload)]) |

### Performance testing: draft without SLA/traffic (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)(assumption|working assumptions) (?i)(gap|gaps|open questions|missing|what I need)]} | ✅ | output satisfies all regex checks (all:[(?i)(assumption|working assumptions) (?i)(gap|gaps|open questions|missing|what I need)]) |

### Performance testing: not a security penetration list (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[scenario scope baseline]} | ✅ | output satisfies all contains checks (all:[scenario scope baseline]) |

