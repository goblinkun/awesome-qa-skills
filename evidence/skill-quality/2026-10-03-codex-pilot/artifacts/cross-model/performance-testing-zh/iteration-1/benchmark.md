# Skill Benchmark: performance-testing

**Date**: 2026-10-03T11:36:28Z
**Evals**: 性能测试：按风险选测试类型与阈值 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### 性能测试：按风险选测试类型与阈值 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[任务理解 性能风险 指标 (负载模型|流量模型|目标负载)]} | ✅ | output satisfies all regex checks (all:[任务理解 性能风险 指标 (负载模型|流量模型|目标负载)]) |

