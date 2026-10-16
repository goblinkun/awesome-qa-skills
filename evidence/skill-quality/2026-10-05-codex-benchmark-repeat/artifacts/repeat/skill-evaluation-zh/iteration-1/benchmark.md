# Skill Benchmark: skill-evaluation

**Date**: 2026-10-05T02:39:26Z
**Evals**: 受控任务对比（不以 Skill 专用标题作为质量标准） (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 100% ± 0% | 50% ± 0% | +0.50 |

## Per-Case Results

### 受控任务对比（不以 Skill 专用标题作为质量标准） (with_skill)

- **Pass Rate**: 100% (7/7)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| 仅把 skill-up validate 成功视为配置或静态证据，明确不支持行为、触发或业务通过。 | ✅ | final_message 将 `skill-up validate` 成功限定为该次校验通过，并明确指出它不能证明行为、实际触发、Benchmark 或业务效果。 |
| 给缺少运行、触发与评分的项目适用的 canonical evidence state，并明确未知的 Skill/模型/目标等元数据。 | ✅ | final_message 使用 PASS、NOT_RUN、BLOCKED、NOT_SCORED、UNASSESSED 和 INSUFFICIENT_EVIDENCE 标记各项证据状态。; final_message 将 Skill 路径与版本、模型、目标行为、运行日志和 selection 记录列为未知或未提供。 |
| 提出覆盖成功、不完整输入和范围/风险边界的最小评测，评分优先确定性，需要语义时明确 rubric 与校准。 | ✅ | final_message 提出 HAPPY、INCOMPLETE 和 BOUNDARY 三类待运行用例，并为每类写明可观察断言。; final_message 优先使用 rule_based 和 script；仅在需要语义判断时使用 agent_judge，并要求明确通过条件及校准。 |
| 区分 with/without Skill Benchmark 和 previous/current Version Regression，说明比较需控制可比条件。 | ✅ | final_message 将 with/without Skill 定义为增量效果比较，将 previous/current 定义为版本退化比较。; final_message 要求比较时控制任务、模型、环境和评分标准，并披露用例或环境变化。 |
| 保留 skill-up 为主引擎，输出证据限制和可执行下一步，不发明 trace、分数或发布审批。 | ✅ | final_message 明确要求使用既有 `skill-up` 体系，并给出取得契约与日志、运行用例、采集 selection 证据及开展两类比较的后续步骤。; final_message 将 trace 和评分标为缺失或未评分，且明确不能据此得出业务收益或发布就绪结论。 |

### 受控任务对比（不以 Skill 专用标题作为质量标准） (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "NOT_RUN"; output does not contain "BLOCKED" |
| expect.exit_code | ✅ | all checks passed |

