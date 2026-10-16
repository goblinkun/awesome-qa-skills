# Skill Benchmark: skill-evaluation

**Date**: 2026-10-03T11:26:28Z
**Evals**: Design a complete Skill evaluation, Missing evaluation environment, Reject a competing evaluation engine (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Design a complete Skill evaluation (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[Evidence Boundaries Recommended Actions]} | ✅ | output satisfies all contains checks (all:[Evidence Boundaries Recommended Actions]) |

### Missing evaluation environment (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)(information gaps|missing|nothing has been run|no .* provided|insufficient[_ ]evidence|not[_ ]run|blocked) NOT_RUN]} | ✅ | output satisfies all regex checks (all:[(?i)(information gaps|missing|nothing has been run|no .* provided|insufficient[_ ]evidence|not[_ ]run|blocked) NOT_RUN]) |

### Reject a competing evaluation engine (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[skill-up Quality Score]} | ✅ | output satisfies all contains checks (all:[skill-up Quality Score]) |

