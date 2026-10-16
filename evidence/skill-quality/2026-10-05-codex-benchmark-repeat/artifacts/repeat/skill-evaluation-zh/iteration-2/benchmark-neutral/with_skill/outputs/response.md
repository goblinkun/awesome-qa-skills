# Skill Evaluation Report

## 范围

本次仅解释已有证据并制定计划，没有执行运行时评测。唯一已知结果是：**`skill-up validate` 成功**。

这支持“该次静态校验通过”，不能支持“行为、触发、Benchmark、业务效果全部通过”。没有源码和运行证据，也不能反向判定 Skill 存在缺陷。

## Run Metadata

| 项目 | 已知值 |
|---|---|
| validate 结果 | 成功，由题述提供；未独立复跑 |
| run_id、timestamp、原始日志 | `unknown` |
| Skill / Eval 版本、`skill-up` 版本 | `unknown` |
| engine / provider / model、运行环境 | `unknown` |
| runtime judge、运行目标、用例详情 | `unknown` |
| runtime trace、产物、`skill.selection` | 未提供 |

## 配置与覆盖范围

Skill 的触发声明、输入、输出、约束和目标行为均为 `unknown`。因此，下列用例是**待绑定契约的最小设计**，不能当作已配置或已执行的测试。

状态含义：

| 状态 | 含义 |
|---|---|
| `PASS` | 对应检查已执行并通过，仅适用于该检查范围 |
| `FAIL` | 有有效执行证据证明断言不满足 |
| `NOT_RUN` | 未执行 |
| `BLOCKED` | 必要条件或证据缺失，无法完成检查 |
| `NOT_SCORED` | 尚未评分 |
| `UNASSESSED` | 尚未开展相应评估 |
| `INSUFFICIENT_EVIDENCE` | 现有证据不足以支持所述结论 |

## Summary

| 结论 | 状态 | 证据边界 |
|---|---|---|
| 本次 validate 成功 | `PASS` | 仅有题述结果，具体校验范围未知 |
| 目标行为正确 | `NOT_RUN` | 无运行目标、用例和输出 |
| 实际触发正确 | `BLOCKED` | 缺少 `skill.selection` 事件 |
| Benchmark 已通过 | `NOT_RUN` | 无 with/without Skill 配对运行 |
| 版本无回归 | `NOT_RUN` | 无 previous/current 可比运行 |
| 业务效果达标 | `UNASSESSED` | 无业务指标、基线或观测数据 |
| “全部已通过” | `INSUFFICIENT_EVIDENCE` | validate 无法覆盖上述结论 |

## Case Results

先选择能直接证明契约行为的最小用例；触发模式只覆盖 Skill 实际声明的模式。

| 待执行用例 | 最小输入与可观察断言 | 拟用 judge | 当前状态与限制 |
|---|---|---|---|
| HAPPY | 一个完整、典型任务；检查必需输出及可核验结果 | 优先 `rule_based`；可执行产物用 `script` | `NOT_RUN`；目标行为未知 |
| INCOMPLETE | 删除一个关键输入；检查是否按契约澄清或处理缺失，是否编造缺失值 | `rule_based`；必要时语义判定 | `NOT_RUN`；缺失处理契约未知 |
| BOUNDARY | 一个最关键的范围或风险边界；检查是否遵守约束 | `rule_based`，必要时检查 trace | `NOT_RUN`；边界未知 |
| EXPLICIT_TRIGGER | 明确点名 Skill 的有效请求；检查 selection 是否选中目标 Skill | trace 规则检查 | 执行 `NOT_RUN`；触发判定 `BLOCKED` |
| IMPLICIT_TRIGGER | 不点名但符合描述的请求；检查 selection 是否选中 | trace 规则检查 | 同上；仅在声明支持时纳入 |
| CONTEXTUAL_TRIGGER | 依赖上下文才符合范围的请求；检查 selection 是否选中 | trace 规则检查 | 同上；仅在声明支持时纳入 |
| NEGATIVE_TRIGGER | 含相近词但不属于范围的请求；检查完整 selection 记录是否排除目标 Skill | trace 规则检查 | 同上；不能以日志缺失判定未触发 |

上述用例均为 `NOT_SCORED`。没有具体契约和 fixtures，当前不能给出有效的实际分数。

## Trigger / Process / Outcome / Artifact / Semantic Evidence

- **Trigger：`BLOCKED`。** 输出相似或符合 Skill 风格，不等于观测到触发；缺少事件也不等于“未触发”。
- **Process：`BLOCKED`。** 无 runtime trace，无法判断步骤、工具使用和约束遵守。
- **Outcome / Artifact：`NOT_RUN`。** 无实际任务结果或产物可检查。
- **Semantic：`UNASSESSED`，`NOT_SCORED`。** 未定义并校准语义 rubric。
- **Efficiency：`UNASSESSED`。** 缺少耗时、调用次数、token 等记录；仅在目标要求时纳入。

评分采用既有 `skill-up` 能力：确定性断言优先 `rule_based`，可执行产物用 `script`；仅对确定性检查无法覆盖的语义要求使用校准后的 `agent_judge`。语义 rubric 必须写清可观察的完成度、正确性和约束遵守标准，成为 gate 前先校准。

缺证据项不得计作通过或失败，也不得另造综合 Quality Score。

## Benchmark Results

**`NOT_RUN`；执行准备 `BLOCKED`。**

Benchmark 比较 **with Skill / without Skill**。最小起点是同一个 HAPPY 用例的配对运行，固定模型、任务、工具权限、环境和 judge，仅改变 Skill 是否可用，并记录实际 selection。

一对运行只能提供个案观察；要声称稳定增益，需要根据随机性重复运行并扩大代表性覆盖。任务表现增益仍不能自动升级为业务效果结论。

## Regression Findings

**`NOT_RUN`；执行准备 `BLOCKED`。**

Version Regression 比较 **previous / current Skill**。应固定 Eval 版本、输入、模型、工具、环境和 judge，对两个 Skill 版本运行同一用例集。

它回答“版本变化是否造成退化”，与 with/without Benchmark 回答的问题不同。目前没有版本对或历史失败证据，不能声称无回归，也不应新增所谓“已确认失败回归用例”。

## Flaky / Blocked / Infrastructure Errors

阻塞条件包括：缺少目标 Skill 契约、可运行目标、具体用例、模型元数据和 trace。

波动性为 `UNASSESSED`。没有证据证明发生了基础设施错误；“材料缺失”不能直接归类为 Infrastructure Defect。

## Eval Validity Findings

运行时评测有效性为 `UNASSESSED`；“全部通过”的汇报存在证据越界。

没有已证实的运行失败，故无法归因于 Skill Defect、Eval Defect 或 Infrastructure Defect，根因分类保持 **`UNKNOWN`**。

## Limitations

当前只能报告题述的 validate 成功。无法确认校验对象、复现该运行，或判断运行时正确性、触发、增益、回归和业务效果。

## Recommended Actions

1. **先补契约和可复现信息：** Skill 版本、触发声明、目标行为、运行目标及 validate 日志。
2. **绑定最小用例：** HAPPY、INCOMPLETE、关键 BOUNDARY，加上适用的正向触发和一个负向触发；明确断言与 judge。
3. **使用现有 `skill-up` 执行：** 条件具备后运行，记录 run identity、版本、模型、环境、judge、输出与 trace；不另造评测引擎。
4. **分别开展两种比较：** with/without 做 Benchmark；previous/current 做版本回归。真实失败须先确认根因，再保留证据并添加回归用例。
5. **单独验证业务效果：** 明确指标、基线、观测窗口和归因方法后再评估。

可直接采用的结论是：**“`skill-up validate` 成功；运行时行为与对比评测尚未执行，触发证据受阻，业务效果尚未评估。当前不足以宣称全部通过。”**
