# Skill Benchmark: skill-change-verification

**Date**: 2026-10-03T11:23:53Z
**Evals**: Complete verification routing, Missing verification environment, Static evidence overstated as runtime proof (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Complete verification routing (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[runtime]} | ✅ | output satisfies all contains checks (all:[runtime]) |

### Missing verification environment (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[confirmation]} | ✅ | output satisfies all contains checks (all:[confirmation]) |

### Static evidence overstated as runtime proof (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)(not supported|unverified|cannot establish|not proven) (?i)runtime]} | ✅ | output satisfies all regex checks (all:[(?i)(not supported|unverified|cannot establish|not proven) (?i)runtime]) |

