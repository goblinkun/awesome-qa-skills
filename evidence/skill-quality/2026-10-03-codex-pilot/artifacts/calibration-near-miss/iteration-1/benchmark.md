# Skill Benchmark: sqet-judge-calibration

**Date**: 2026-10-03T11:48:04Z
**Evals**: 原始无 Skill 输出：缺少 canonical 状态，必须 FAIL (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 50% ± 0% |

## Per-Case Results

### 原始无 Skill 输出：缺少 canonical 状态，必须 FAIL (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "NOT_RUN"; output does not contain "BLOCKED" |
| expect.exit_code | ✅ | all checks passed |

