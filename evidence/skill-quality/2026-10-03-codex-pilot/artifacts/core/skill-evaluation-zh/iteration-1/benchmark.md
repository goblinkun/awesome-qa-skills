# Skill Benchmark: skill-evaluation

**Date**: 2026-10-03T11:26:56Z
**Evals**: 设计完整 Skill 评测, 缺少评测环境, 拒绝重复评测引擎 (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### 设计完整 Skill 评测 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[评测范围 (证据边界|证据分别判断|证据约束|证据状态) 推荐行动]} | ✅ | output satisfies all regex checks (all:[评测范围 (证据边界|证据分别判断|证据约束|证据状态) 推荐行动]) |

### 缺少评测环境 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(信息缺口|资料缺失|缺少|没有提供) NOT_RUN]} | ✅ | output satisfies all regex checks (all:[(信息缺口|资料缺失|缺少|没有提供) NOT_RUN]) |

### 拒绝重复评测引擎 (with_skill)

- **Pass Rate**: 100% (3/3)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_contains{all:[skill-up Quality Score]} | ✅ | output satisfies all contains checks (all:[skill-up Quality Score]) |

