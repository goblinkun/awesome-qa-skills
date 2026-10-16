# Skill Benchmark: performance-testing

**Date**: 2026-10-03T11:24:54Z
**Evals**: 性能测试：按风险选测试类型与阈值, 性能测试：无 SLA/流量仍给初版, 性能测试：不要做成安全渗透清单 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 89% ± 16% |

## Per-Case Results

### 性能测试：按风险选测试类型与阈值 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[任务理解 性能风险 指标 (负载模型|流量模型|目标负载)]} | ✅ | output satisfies all regex checks (all:[任务理解 性能风险 指标 (负载模型|流量模型|目标负载)]) |

### 性能测试：无 SLA/流量仍给初版 (with_skill)

- **Pass Rate**: 67% (2/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "待确认" |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |

### 性能测试：不要做成安全渗透清单 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[场景 范围 基线]} | ✅ | output satisfies all contains checks (all:[场景 范围 基线]) |

