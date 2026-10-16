# Skill Benchmark: testability-analysis

**Date**: 2026-10-03T11:32:20Z
**Evals**: 可测试性分析：领域完整场景, 可测试性分析：信息不完整时的受限初版, 可测试性分析：高风险边界与取舍, 架构可测试性评审：接缝与环境复现, 架构可测试性评审：架构材料不完整 (1 runs each per configuration)

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

### 可测试性分析：信息不完整时的受限初版 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[当前假设 信息缺口 待确认]} | ✅ | output satisfies all contains checks (all:[当前假设 信息缺口 待确认]) |

### 可测试性分析：高风险边界与取舍 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[P0 P1 剩余风险]} | ✅ | output satisfies all contains checks (all:[P0 P1 剩余风险]) |

### 架构可测试性评审：接缝与环境复现 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(输入审计|输入证据|证据与边界|证据基础) 隔离 验证]} | ✅ | output satisfies all regex checks (all:[(输入审计|输入证据|证据与边界|证据基础) 隔离 验证]) |

### 架构可测试性评审：架构材料不完整 (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[输入审计 (待确认|信息缺口|开放问题) (证据|依据)]} | ✅ | output satisfies all regex checks (all:[输入审计 (待确认|信息缺口|开放问题) (证据|依据)]) |

