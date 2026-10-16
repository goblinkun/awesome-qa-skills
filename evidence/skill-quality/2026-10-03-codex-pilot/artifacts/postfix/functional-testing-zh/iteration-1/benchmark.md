# Skill Benchmark: functional-testing

**Date**: 2026-10-03T11:30:47Z
**Evals**: 功能测试：完整上下文产出可执行方案, 功能测试：信息不全仍给初版, 功能测试：发版窗口短必须砍范围 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### 功能测试：完整上下文产出可执行方案 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[任务理解 (风险|优先级) (边界|极值|限制) (异常|负向|失败)]} | ✅ | output satisfies all regex checks (all:[任务理解 (风险|优先级) (边界|极值|限制) (异常|负向|失败)]) |

### 功能测试：信息不全仍给初版 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[假设 待确认 (信息缺口|必须补齐的信息|待补充信息|信息不足|需要补齐)]} | ✅ | output satisfies all regex checks (all:[假设 待确认 (信息缺口|必须补齐的信息|待补充信息|信息不足|需要补齐)]) |

### 功能测试：发版窗口短必须砍范围 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[P0 降级 (关键路径|核心路径|主链路|闭环|登录[^\n]*下单[^\n]*支付)]} | ✅ | output satisfies all regex checks (all:[P0 降级 (关键路径|核心路径|主链路|闭环|登录[^\n]*下单[^\n]*支付)]) |

