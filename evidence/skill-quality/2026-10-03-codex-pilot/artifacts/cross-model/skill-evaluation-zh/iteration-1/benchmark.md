# Skill Benchmark: skill-evaluation

**Date**: 2026-10-03T11:38:16Z
**Evals**: 设计完整 Skill 评测 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 50% ± 0% |

## Per-Case Results

### 设计完整 Skill 评测 (with_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "评测范围"; output does not contain "推荐行动" |
| expect.exit_code | ✅ | all checks passed |

