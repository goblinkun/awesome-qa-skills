# Skill Evaluation Report

## 范围

本报告采用 `skill-evaluation` 的证据规则。唯一已知结果是 **`skill-up validate` 成功**，由题设提供；未提供原始日志，本次未重新运行。

**成立的结论仅是该次 validate 通过。行为、触发、Benchmark 和业务效果全部通过的说法不成立。** validate 不能证明 runtime 语义、实际选择 Skill 或业务收益。

Skill 的触发条件、输入、输出、约束和目标行为均为 `unknown`，无法据此定义具体业务断言。

## Run Metadata

| 字段 | 已知信息 |
|---|---|
| 命令及结果 | `skill-up validate`：成功 |
| run_id、timestamp、日志 | `unknown` |
| Skill 路径、版本；Eval 版本 | `unknown` |
| skill-up 版本、engine/provider/model | `unknown` |
| judge、environment | `unknown` |
| runtime trace、产物、skill.selection | 未提供 |

## 配置与覆盖范围

现有证据仅覆盖 validate。下面的用例是**待落实的评测设计**，尚未执行；取得 Skill 契约及已有 `evals/`、fixtures 后，才能确定真实输入和预期结果。

## Summary

本报告使用以下状态：

| 状态 | 含义 |
|---|---|
| `PASS` | 指定检查有通过证据，仅限该检查范围 |
| `FAIL` | 有有效证据证明违反明确断言 |
| `NOT_RUN` | 尚未执行 |
| `BLOCKED` | 缺少必要前提或证据，无法完成判断 |
| `NOT_SCORED` | 尚未评分，不等于零分 |
| `UNASSESSED` | 尚未开展该维度的评估 |
| `INSUFFICIENT_EVIDENCE` | 现有证据不足以支持所述结论 |

## Case Results

| 检查 | 当前状态 | 证据与边界 |
|---|---|---|
| validate | `PASS` | 依据题设；具体检查范围和日志未知 |
| 行为与产物正确性 | `NOT_RUN` | 无目标、用例、运行输出或产物 |
| 实际触发 | `BLOCKED` | 缺少 `skill.selection` 事件 |
| Benchmark | `NOT_RUN` | 无 with/without 成对运行 |
| 版本回归 | `NOT_RUN` | 无 previous/current 可比运行 |
| 业务效果 | `UNASSESSED` | 无指标、基线、观测窗口或业务数据 |
| 综合质量评分 | `NOT_SCORED` | 不以 validate 换算分数 |
| “全部通过”声明 | `INSUFFICIENT_EVIDENCE` | 超出现有证据范围 |

最小有效用例从一个能证明核心目标行为的确定性成功用例开始，再补必要边界：

| 待运行用例 | 可观察断言 | Judge 与限制 |
|---|---|---|
| HAPPY：一个真实典型任务 | 满足契约规定的输出及关键约束 | 优先 `rule_based`；目标契约缺失，当前 `NOT_RUN` |
| INCOMPLETE：缺少关键输入 | 按契约追问或处理缺失项，不编造事实 | 确定性检查；仅语义部分使用已校准 `agent_judge` |
| BOUNDARY：范围或风险边界 | 遵守契约规定的边界行为 | 优先 `rule_based`；边界定义待取得 |
| 正向触发 | 显式、隐式、上下文模式中，分别覆盖契约声称支持的模式 | 检查 observed `skill.selection`；当前 `BLOCKED` |
| NEGATIVE_TRIGGER：相邻但不适用任务 | 完整 selection 记录显示未选择目标 Skill | trace 检查；日志缺失不能当作未触发 |

以上用例均未运行。回归用例只在确认真实失败及根因后加入，并保留原始证据。

## Trigger / Process / Outcome / Artifact / Semantic Evidence

- **Trigger：`BLOCKED`**。输出相似、提及 Skill 名称或任务成功，都不能替代选择事件。
- **Process：`BLOCKED`**。缺少 runtime trace，不能证明遵守了内部流程。
- **Outcome / Artifact：`NOT_RUN`**。没有可检查的运行结果。
- **Semantic：`NOT_SCORED`**。尚无目标行为、rubric 和 judge 校准证据。

评分按可观察断言进行：确定性要求用 `rule_based`；可执行产物用 `script`；只有需要语义判断时才用 `agent_judge`，明确通过条件，并在成为 gate 前校准。未运行或受阻项不计作通过，也不记为零分。使用既有 `skill-up` 体系，不另造 Engine、Judge、Benchmark 或 Quality Score。

## Benchmark Results

状态：`NOT_RUN`。

**with/without Skill** 衡量引入 Skill 的增量效果。两组需使用相同任务、模型、工具权限、环境和评分标准，仅改变 Skill 是否可用；记录实际选择证据，并对随机性进行重复运行。

先比较任务成功率及必要的质量、耗时、token 等指标。一次输出更好不能证明稳定收益；离线 Benchmark 也不能自动升级为业务效果。

## Regression Findings

状态：`NOT_RUN`。

**previous/current** 衡量版本变化是否引入退化。两版应使用相同 Eval、模型和环境，在两组均启用 Skill 的条件下比较。

它与 with/without 的问题不同，不能互相替代。缺少旧版本或可比运行时，不能写“无回归”；若用例或环境发生变化，必须披露，不能把差异直接归因于 Skill 版本。

## Flaky / Blocked / Infrastructure Errors

运行受阻于源码、契约、运行目标及用例缺失；触发判断另受阻于 selection 证据缺失。

目前没有证据确认 flaky 或 Infrastructure Defect。缺少资料本身不证明基础设施故障。

## Eval Validity Findings

Eval validity：`UNASSESSED`；缺陷归因：`UNKNOWN`。

尚无法确认用例是否有效、judge 是否可靠，也无法区分 Skill Defect、Eval Defect 或 Infrastructure Defect。不能把未知情况写成 Skill 失败或通过。

## Limitations

没有 runtime 和业务证据，不能给出行为通过率、触发率、性能提升、业务收益或发布就绪结论。validate 成功也不能证明 Skill 完整满足其契约。

## Recommended Actions

1. 取得 Skill 契约、源码、已有 `evals/` 与 fixtures、validate 日志和可运行目标，补齐运行元数据。
2. 用既有 `skill-up` 校验配置，先运行一个确定性 HAPPY 用例，再补不完整输入与边界用例。
3. 为契约支持的触发模式补正向和负向用例，采集 `skill.selection` 与 runtime trace；无法采集时继续标记 `BLOCKED`。
4. 分别运行 with/without Benchmark、previous/current 版本回归，保存输入、输出、judge、产物及环境记录。
5. 业务效果单独定义指标、基线和观测窗口后评估。在此之前，报告保留上述证据状态，不改写为“全部通过”。
