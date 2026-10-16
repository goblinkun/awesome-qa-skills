# Skill Benchmark: skill-evaluation

**Date**: 2026-10-03T11:39:34Z
**Evals**: 受控任务对比（不以 Skill 专用标题作为质量标准） (1 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|-----------|--------------|-------|
| Pass Rate | 100% ± 0% | 83% ± 0% | +0.17 |

## Per-Case Results

### 受控任务对比（不以 Skill 专用标题作为质量标准） (with_skill)

- **Pass Rate**: 100% (6/6)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.exit_code | ✅ | all checks passed |
| 仅把 skill-up validate 成功视为配置或静态证据，明确不支持行为、触发或业务通过。 | ✅ | final_message 将 `skill-up validate` 成功限定为用户报告的静态校验结果，并明确表示不能据此证明运行行为、触发、Benchmark 或业务效果通过。 |
| 给缺少运行、触发与评分的项目适用的 canonical evidence state，并明确未知的 Skill/模型/目标等元数据。 | ✅ | final_message 的 Summary 为未运行、受阻、未评分和证据不足的项目分别使用 `NOT_RUN`、`BLOCKED`、`NOT_SCORED`、`INSUFFICIENT_EVIDENCE` 等状态，并解释其含义。; final_message 将目标 Skill 契约及 run_id、版本、engine/provider/model、judge、环境和时间戳明确标为 `unknown`。 |
| 提出覆盖成功、不完整输入和范围/风险边界的最小评测，评分优先确定性，需要语义时明确 rubric 与校准。 | ✅ | final_message 的 Case Results 提出 HAPPY、INCOMPLETE、BOUNDARY 三类最小候选用例，分别覆盖成功、缺少必要信息和范围或风险边界。; final_message 要求优先使用确定性断言；仅在需要语义判断时使用 `agent_judge`，先定义可观察 rubric，并用人工标注样本校准。 |
| 区分 with/without Skill Benchmark 和 previous/current Version Regression，说明比较需控制可比条件。 | ✅ | final_message 明确将 Benchmark 定义为 with Skill / without Skill 比较，将 Version Regression 定义为 previous / current Skill 比较，且指出回归的两组均使用 Skill。; final_message 要求控制任务、fixtures、模型、runtime、工具权限、生成参数和预算等可比条件，并分别报告两类比较。 |
| 保留 skill-up 为主引擎，输出证据限制和可执行下一步，不发明 trace、分数或发布审批。 | ✅ | final_message 明确沿用 `skill-up` 主评测引擎及已有 `evals/`，并列出补齐契约、实例化用例、运行评测、保存证据和开展对照的步骤。; final_message 明确声明没有 runtime trace、真实输出或评分证据，不能给出行为通过率、触发率、Benchmark 分数、业务效果或发布结论。 |

### 受控任务对比（不以 Skill 专用标题作为质量标准） (without_skill)

- **Pass Rate**: 83% (5/6)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.exit_code | ✅ | all checks passed |
| 仅把 skill-up validate 成功视为配置或静态证据，明确不支持行为、触发或业务通过。 | ✅ | final_message 明确写道，已知结果只有 `skill-up validate` 成功，不能据此认定行为、触发、Benchmark 或业务效果通过。 |
| 给缺少运行、触发与评分的项目适用的 canonical evidence state，并明确未知的 Skill/模型/目标等元数据。 | ✅ | final_message 的状态表将行为、触发和 Benchmark 标为“未运行，受阻”，业务效果标为“未测量”，并说明未运行不等于通过、零分或不适用。; final_message 明确列出缺少 Skill 内容及版本、运行目标、模型和运行配置等元数据。 |
| 提出覆盖成功、不完整输入和范围/风险边界的最小评测，评分优先确定性，需要语义时明确 rubric 与校准。 | ❌ | final_message 提出代表性行为任务、应触发与不应触发场景，以及缺失输入或异常边界场景。; final_message 优先采用可执行断言，并为主观判断给出 0、1、2 分量表。 | Failures: 需要语义评分时，未明确提出评分校准方法，例如用锚定样例试评、核对评分一致性或解决分歧。 |
| 区分 with/without Skill Benchmark 和 previous/current Version Regression，说明比较需控制可比条件。 | ✅ | final_message 的对比表分别定义 with/without Skill 和 previous/current，并要求固定用例、模型或运行配置及评分规则。; final_message 明确指出 previous/current 的两组都使用 Skill，且不能把 without Skill 当作 previous。 |
| 保留 skill-up 为主引擎，输出证据限制和可执行下一步，不发明 trace、分数或发布审批。 | ✅ | final_message 要求沿用现有评测流程、不另建引擎，也不猜测 `skill-up` 的其他命令。; final_message 列出补齐材料和开展对比、触发检查、版本回归的下一步，并明确没有行为通过证据；未编造 trace、分数或发布审批。 |

