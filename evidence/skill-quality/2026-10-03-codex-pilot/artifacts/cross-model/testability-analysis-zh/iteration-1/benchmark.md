# Skill Benchmark: testability-analysis

**Date**: 2026-10-03T11:36:37Z
**Evals**: 可测试性分析：领域完整场景 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### 可测试性分析：领域完整场景 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(输入审计|输入证据|证据与边界|证据基础) 风险 P0 (预期|判断标准|验收标准|成功标准)]} | ✅ | output satisfies all regex checks (all:[(输入审计|输入证据|证据与边界|证据基础) 风险 P0 (预期|判断标准|验收标准|成功标准)]) |

