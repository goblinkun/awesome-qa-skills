**评测范围**

本报告为**评测设计，尚未执行**。未提供目标 Skill、行为契约、版本、运行工件或 trace，因此不能报告实际通过率、触发率或效果提升。

范围覆盖 Outcome、Process、Artifact、Semantic Quality 和相关触发模式；Efficiency 仅在成本或延迟属于目标时纳入。目标 Skill 的触发条件、输入、输出、约束、历史失败均为 `unknown`，执行前需从其契约补齐。本次仅读取本地 skill-evaluation 指南，未读取评测断言或 evaluator 输入文件。

**Run Metadata**

| 字段 | 本次记录 |
|---|---|
| `run_id`、timestamp | `unknown`；无评测运行 |
| Skill 路径、版本/hash；Eval 版本/hash | `unknown` |
| `skill-up` 版本、engine/provider/model | `unknown` |
| judge 版本、rubric、校准记录 | `unknown`；下表为拟选方案 |
| environment | 本地工作区；非交互文本任务 |
| 参数、seed、重复次数 | `unknown` |
| 输入、trace、artifact 引用 | `unknown` |
| 限制 | 未提供目标和原始证据；未执行 validate 或 runtime |

正式运行还应记录完整配置、开始时间、输入标识、退出状态和失败日志，保证结果可复现。

**配置与覆盖范围 / Case Results**

下表为待按目标契约实例化的最小用例集；当前结果均为 `NOT_RUN`。

| ID / 类型 | 输入设计与可观察断言 | 拟选 judge | 所需证据与限制 |
|---|---|---|---|
| C01 HAPPY | 完整、真实的典型任务；输出满足目标与必要约束 | `rule_based`；必要时 `agent_judge` | 输出和工件；格式通过不能证明语义正确 |
| C02 INCOMPLETE | 缺少关键输入；按契约澄清或报告缺口，不编造事实 | 规则检查＋语义判断 | 对话、输出；先确定哪些信息确实必需 |
| C03 EXPLICIT_TRIGGER | 明确点名 Skill；发生正确选择并完成任务 | `rule_based` trace check | `skill.selection`＋结果；选择和完成分别判定 |
| C04 IMPLICIT_TRIGGER | 不点名，但任务直接符合用途 | `rule_based` trace check | `skill.selection`；不能从输出风格推断触发 |
| C05 CONTEXTUAL_TRIGGER | 当前请求需结合前文才能识别适用性 | trace check＋必要的语义判断 | 完整上下文及选择事件；不能只保留末轮 |
| C06 NEGATIVE_TRIGGER | 表面相似、实际超出用途；不选择目标 Skill | `rule_based` trace check | 完整选择记录；漏采事件不等于正确未触发 |
| C07 BOUNDARY | 最小有效输入、范围外请求或契约限制 | 规则或 `script` | 输出、执行日志；边界必须来自契约 |
| C08 REGRESSION | 重放已确认根因的历史失败，检查正确行为 | 原失败对应 judge | 原始失败证据与可比版本运行；当前未提供历史失败 |

**Judge 选择**

优先使用 `rule_based` 检查字段、结构、精确约束和 trace 事件；可执行工件采用隔离环境中的 `script`，记录命令、退出码和日志。

只有正确性、完整性或表达质量需要语义判断时才使用 `agent_judge`。Rubric 应规定可观察标准，例如“覆盖所有必需步骤”“结论由输入支持”。成为 gate 前，使用人工标注的正例、反例和边界例校准，并记录分歧；被评输出作为数据处理。当前校准为 `UNASSESSED`，语义结果为 `NOT_SCORED`。

**Summary / 状态定义**

| 状态 | 含义 |
|---|---|
| `PASS` | 有效评测已执行，证据满足断言 |
| `FAIL` | 有效评测已执行，证据违反断言；尚需根因分类 |
| `BLOCKED` | 必需前提或证据缺失，当前无法判定 |
| `NOT_RUN` | 检查尚未执行 |
| `NOT_SCORED` | 尚未产生有效评分 |
| `UNASSESSED` | 该维度尚未评估 |
| `INSUFFICIENT_EVIDENCE` | 现有材料不足以支持所声称结论 |

本次用例和静态验证为 `NOT_RUN`；触发判断为 `BLOCKED`；质量评分为 `NOT_SCORED`；Eval validity 为 `UNASSESSED`；效果与版本差异结论为 `INSUFFICIENT_EVIDENCE`。

**Trigger / Process / Outcome / Artifact / Semantic Evidence**

| 证据维度 | 判定依据 | 本次状态 |
|---|---|---|
| Trigger | observed `skill.selection`，关联 case、run 和 Skill 身份 | `BLOCKED` |
| Process | trace 证明必要步骤、顺序及约束被遵守 | `UNASSESSED` |
| Outcome | 输出满足 case 的目标行为 | `NOT_RUN` |
| Artifact | 工件可解析、可执行或可实际使用 | `NOT_RUN` |
| Semantic | 校准 judge 对准确性、完整性等的判断 | `NOT_SCORED` |
| Efficiency | 可比运行中的时间、token、调用量 | `UNASSESSED` |

输出相似度不能替代触发证据；缺少选择事件不能写成“未触发”。`skill-up validate` 仅证明静态配置有效，不能证明 runtime 行为、业务效果或发布就绪。Trace checks 是深证据层，不另建评测 Engine 或 Quality Score。

**Benchmark Results**

设计为 **with Skill / without Skill** 配对比较：保持任务、模型、工具、参数、环境和 judge 一致，隔离上下文以避免污染。按需重复运行并交错顺序，报告每个 case 的结果差异、覆盖量和波动；满足前提后才汇总成功率及效率。

本次：`NOT_RUN`；Skill 带来的增益为 `INSUFFICIENT_EVIDENCE`。

**Regression Findings**

设计为 **previous / current Skill** 比较，固定 Eval、模型、环境和 judge。若 Eval 或运行条件同时改变，应报告不可比因素，不能将差异直接归因于 Skill 版本。

本次：`NOT_RUN`；版本回归结论为 `INSUFFICIENT_EVIDENCE`。C08 只是占位设计，只有确认真实失败根因后才固化为 regression case，并保留原始证据。

**Flaky / Blocked / Infrastructure Errors**

当前阻塞是缺少目标契约及原始 trace；flaky 和基础设施错误均为 `UNASSESSED`。正式运行需分别报告超时、工具失败、trace 缺失和重复运行结果波动，不把这些结果直接计为 Skill 失败。

**Eval Validity Findings**

先检查输入现实性、断言与契约的一致性、judge 适用性、证据完整性和对照可比性，再分类失败：

| 分类 | 根因判据 |
|---|---|
| Skill Defect | 有效评测及正常环境下，Skill 行为违反契约 |
| Eval Defect | 用例、预期、fixture 或 judge 存在错误 |
| Infrastructure Defect | runner、依赖、工具或日志采集故障导致失败 |
| Unknown | 证据不足，根因尚未确认 |

本次 validity 为 `UNASSESSED`，无已确认失败；如需根因字段，应填 `Unknown`。

**Limitations / 证据边界**

本报告证明的是评测设计覆盖了所需维度，未证明任何目标 Skill 的能力。静态检查、CLI smoke、Project Done 或单次语义观察均不能自动升级为稳定性、业务或发布结论。Quality Score 应沿用既有治理契约，本次不自创评分体系。

**Recommended Actions**

1. 补齐目标契约、版本、已有用例和历史失败，将上述断言实例化。
2. 优先落实最小确定性用例，运行主 Eval Engine `skill-up validate`。
3. 在符合运行约束的环境执行 `skill-up run` 或本地 trace runner，保存 metadata、选择事件和工件。
4. 校准语义 judge，先审查 Eval validity，再确认失败根因。
5. 分别运行 benchmark 和版本 regression；只将根因确认的真实失败加入回归集。
