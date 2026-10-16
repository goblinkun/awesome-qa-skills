# Skill Evaluation Report

## 范围

唯一已知结果是 **`skill-up validate` 成功**，来源为用户提供的信息。本次未重新运行命令，未执行 runtime 评测。

**“行为、触发、Benchmark 和业务效果全部通过”的结论不成立。** Validate 成功只能支持其实际检查范围内的静态校验通过，不能证明运行行为或效果。

目标 Skill 的触发声明、输入、输出、约束和目标行为均为 `unknown`，不能用评测工具 Skill 的契约代替目标契约。

## Run Metadata

以下均为 `unknown`：`run_id`、目标 Skill 版本、Eval 版本、`skill-up` 版本、engine/provider/model、judge、运行环境、timestamp。

缺少源码、运行目标、用例、原始日志、runtime trace 和 `skill.selection` 事件。

## 配置与覆盖范围

沿用 **`skill-up` 主评测引擎及已有 `evals/`**；不另建 Engine、Judge、Benchmark 或 Quality Score。以下只是待目标契约补齐后实例化的最小用例设计。

## Summary

| 项目 | 状态 | 可成立的结论 |
|---|---|---|
| Validate | `PASS`，据用户报告 | 已知该命令成功；具体检查项未知 |
| 行为与产物 | `NOT_RUN` | 没有执行结果 |
| 触发 | `BLOCKED` | 缺少 `skill.selection`，不能判断已触发或未触发 |
| Benchmark | `NOT_RUN` | 没有 with/without 对照 |
| 版本回归 | `NOT_RUN` | 没有 previous/current 对照 |
| 业务效果 | `INSUFFICIENT_EVIDENCE` | 没有业务指标与归因证据 |
| Eval 有效性 | `UNASSESSED` | 无用例和 judge 可供审查 |
| 语义评分 | `NOT_SCORED` | 无输出、rubric 或校准证据 |

状态含义：`PASS`／`FAIL` 表示已执行检查满足／违反明确断言；`NOT_RUN` 表示未执行；`BLOCKED` 表示所需前提或证据缺失；`NOT_SCORED` 表示没有评分；`UNASSESSED` 表示尚未评估；`INSUFFICIENT_EVIDENCE` 表示证据不足以支持结论。**这些状态不能相互替代，也不能全部算作失败。**

## Case Results

| 最小候选用例 | 待契约补齐后的可观察断言 | 评分方法 | 当前状态 |
|---|---|---|---|
| HAPPY，可兼顾显式请求 | 必要输入齐全，输出满足契约且产物可用 | `rule_based`；可执行产物用 `script` | `NOT_RUN`；实例化受阻 |
| INCOMPLETE | 缺少必要信息时，按契约处理且不编造缺失值 | `rule_based`；必要时语义 judge | `NOT_RUN`；实例化受阻 |
| BOUNDARY | 范围或风险边界处，按契约停止、澄清或降级 | `rule_based`；必要时语义 judge | `NOT_RUN`；实例化受阻 |
| EXPLICIT_TRIGGER | 明确请求目标 Skill 后，观察到对应 selection 事件 | trace 规则检查 | `BLOCKED` |
| IMPLICIT／CONTEXTUAL_TRIGGER | 每个实际声明的模式至少一个独立输入，观察对应 selection | trace 规则检查 | `BLOCKED`；适用模式 `UNASSESSED` |
| NEGATIVE_TRIGGER | 在应排除的相邻任务中未选择目标 Skill | 完整且确认启用的 selection trace | `BLOCKED` |

行为与触发可以复用输入，但必须分别判定。不能用输出相似度替代触发事件；负向用例也不能仅凭日志中没看到事件就判定通过。

## Trigger / Process / Outcome / Artifact / Semantic Evidence

- **Trigger：`BLOCKED`**，没有 selection 证据。
- **Process：`BLOCKED`**，没有 runtime trace。
- **Outcome／Artifact：`NOT_RUN`**，没有真实输出或产物。
- **Semantic：`NOT_SCORED`**，不能从 validate 推导语义质量。

确定性断言优先逐项判定通过或失败；缺证据单列状态，不计作零分。只有语义质量确实需要判断时才用 `agent_judge`，先定义可观察 rubric，并经人工标注样本校准后再作为 gate。不临时汇总成新的质量总分。

## Benchmark Results

**`NOT_RUN`。** Benchmark 比较 **with Skill / without Skill**，用于评估 Skill 的增益。

需要相同任务、fixtures、模型、runtime、工具权限、生成参数和预算，仅改变 Skill 可用性，并防止 without 组获得 Skill 内容。记录配对结果；存在随机性时重复运行并报告波动。功能结果不能直接升级为业务收益。

## Regression Findings

**`NOT_RUN`。** Version Regression 比较 **previous / current Skill**，两组均使用 Skill，固定其他运行条件。

当前没有版本、基线或可比运行，不能声称“无回归”。只有真实失败经根因确认后，才新增回归用例并保留原始证据。

## Flaky / Blocked / Infrastructure Errors

运行受源码、契约、用例和目标缺失所阻；触发检查受 selection 证据缺失所阻。Flaky 情况为 `UNASSESSED`。

缺失材料不等于基础设施故障。Skill Defect、Eval Defect、Infrastructure Defect 均无法确认，归因保持 `UNKNOWN`。

## Eval Validity Findings

**`UNASSESSED`。** 尚不能检查用例是否代表真实任务、断言是否匹配契约、judge 是否校准、对照是否公平，以及是否存在信息泄漏。

## Limitations

本报告仅解释已知证据并提出评测设计；没有运行新增评测，不能给出行为通过率、触发率、Benchmark 分数、业务效果或发布结论。

## Recommended Actions

1. 补齐目标 Skill 契约、源码、已有 `evals/`、fixtures 和可运行目标；确认相关 trigger mode。
2. 先实例化 HAPPY、INCOMPLETE、BOUNDARY 三类用例，以确定性检查为主，使用既有 `skill-up` 流程运行并保存 metadata、输出和产物。
3. 补齐 runtime trace 与 `skill.selection`，再运行相关正向及负向触发用例；缺失时保持 `BLOCKED`。
4. 分别建立 with/without Benchmark 和 previous/current 版本回归，独立报告，禁止互相替代。
5. 业务效果另需真实指标、观察窗口和可比对照；在取得这些证据前保持 `INSUFFICIENT_EVIDENCE`。
