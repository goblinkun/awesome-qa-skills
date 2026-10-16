# Skill Benchmark: skill-evaluation

**Date**: 2026-10-03T11:51:40Z
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
| 仅把 skill-up validate 成功视为配置或静态证据，明确不支持行为、触发或业务通过。 | ✅ | final_message 开头明确说现有证据只支持 skill-up validate 成功，不能据此宣布行为、触发、Benchmark 或业务效果通过。; Summary 将行为标为 NOT_RUN、触发标为 BLOCKED、业务效果标为 INSUFFICIENT_EVIDENCE。 |
| 给缺少运行、触发与评分的项目适用的 canonical evidence state，并明确未知的 Skill/模型/目标等元数据。 | ✅ | final_message 的 Run Metadata 将 Skill/Eval 版本、engine/provider/model、judge 和运行环境等列为 unknown。; Summary 和状态含义区分 PASS、NOT_RUN、BLOCKED、NOT_SCORED、UNASSESSED 与 INSUFFICIENT_EVIDENCE，并说明各状态的证据边界。 |
| 提出覆盖成功、不完整输入和范围/风险边界的最小评测，评分优先确定性，需要语义时明确 rubric 与校准。 | ✅ | final_message 的最小候选集包含完整有效输入、缺少必要输入、范围或风险边界，以及正向和负向触发用例。; 评分部分优先逐断言的确定性判断；使用 agent_judge 时要求先定义可观察 rubric，并用人工确认样例校准。 |
| 区分 with/without Skill Benchmark 和 previous/current Version Regression，说明比较需控制可比条件。 | ✅ | final_message 将 Benchmark 定义为 with Skill / without Skill 比较，并要求控制任务集、模型、运行参数、环境、工具、预算和 judge。; Regression Findings 将版本回归定义为 previous / current Skill 比较，说明两组都使用 Skill、条件须可比，且两种比较不能互相证明结论。 |
| 保留 skill-up 为主引擎，输出证据限制和可执行下一步，不发明 trace、分数或发布审批。 | ✅ | final_message 的 Recommended Actions 要求使用既有 skill-up 引擎运行用例并保存证据。; 全文明确没有运行评测、runtime trace、评分或业务测量数据，并将 Quality Score 标为 NOT_SCORED；没有声称发布获批。 |

### 受控任务对比（不以 Skill 专用标题作为质量标准） (without_skill)

- **Pass Rate**: 50% (1/2)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ❌ | output does not contain "NOT_RUN"; output does not contain "BLOCKED" |
| expect.exit_code | ✅ | all checks passed |

