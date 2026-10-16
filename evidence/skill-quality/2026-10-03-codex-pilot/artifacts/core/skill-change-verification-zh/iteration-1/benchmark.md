# Skill Benchmark: skill-change-verification

**Date**: 2026-10-03T11:24:11Z
**Evals**: 完整变更验证路由, 缺少验证环境, 静态检查冒充运行时证据 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### 完整变更验证路由 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[运行时]} | ✅ | output satisfies all contains checks (all:[运行时]) |

### 缺少验证环境 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(待确认|需要提供|缺少|需补充) (未执行|NOT_RUN|未验证)]} | ✅ | output satisfies all regex checks (all:[(待确认|需要提供|缺少|需补充) (未执行|NOT_RUN|未验证)]) |

### 静态检查冒充运行时证据 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(不能声称|不能据此报告|不可宣称|不能报告) 运行时]} | ✅ | output satisfies all regex checks (all:[(不能声称|不能据此报告|不可宣称|不能报告) 运行时]) |

