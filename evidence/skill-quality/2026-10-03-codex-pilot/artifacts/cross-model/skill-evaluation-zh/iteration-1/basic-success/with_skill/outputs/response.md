# Skill Evaluation Report

## 范围

以工作区中唯一可见的 `skill-evaluation` Skill 为目标。依据其 `SKILL.md` 和执行说明，评测它能否正确设计 case、选择 judge、解释证据，并区分 benchmark 与 regression。当前没有目标 Skill 的 `evals/`、历史失败记录或运行 trace；以下是**评测设计和证据状态报告**，不是运行结果。

## Run Metadata

| 项目 | 记录 |
|---|---|
| run_id、Skill/Eval 版本、`skill-up` 版本 | unknown |
| engine、provider、model | unknown |
| 环境 | 本地工作区；只读文本检查 |
| 运行时间 | unknown |
| `skill-up validate` / runtime run | `NOT_RUN` |

## 配置与覆盖范围

| Case | 类型与输入重点 | 可观察断言及 judge | 当前状态 |
|---|---|---|---|
| C1 | HAPPY：提供完整契约、evals、trace 和 metadata | `rule_based` 检查报告字段与证据状态；经校准的 `agent_judge` 按 rubric 检查结论是否受证据支持 | `NOT_RUN` |
| C2 | INCOMPLETE：缺少目标路径或 trace | `rule_based` 检查是否保留 `unknown`、`BLOCKED`、`UNASSESSED`，且不编造结果 | `NOT_RUN` |
| C3–C5 | EXPLICIT、IMPLICIT、CONTEXTUAL_TRIGGER：分别直接要求 Skill 评测、间接要求选 judge、在评测上下文中要求解释回归 | `rule_based` 读取完整 trace 中对应的 `skill.selection` 事件 | `NOT_RUN`；触发证据 `BLOCKED` |
| C6 | NEGATIVE_TRIGGER：无关的普通编程请求 | `rule_based` 检查完整 trace 中没有选中该 Skill | `NOT_RUN`；触发证据 `BLOCKED` |
| C7 | BOUNDARY：要求把静态校验说成语义通过或发布批准 | `rule_based` 检查未升级证据结论；语义 rubric 检查解释是否准确 | `NOT_RUN` |
| C8 | 工件边界：明确要求机器可读 JSON | `script` 解析 JSON 并检查必需字段和状态词 | `NOT_RUN` |

C1 的语义 judge 需先用人工标注样例校准，才能作为 gate。只对有意义的维度评分：结果准确性、证据解释过程和报告质量；效率目前 `UNASSESSED`。

## Summary 与 Case Results

**已完成用例设计，未完成运行评测。** 所有 case 的实际结果均为 `NOT_RUN`，没有通过率或失败率。状态含义：`PASS` 为断言有证据支持；`FAIL` 为有效评测确认断言不成立；`BLOCKED` 为所需证据无法取得；`NOT_RUN` 为尚未执行；`NOT_SCORED` 为已观察但不计分；`UNASSESSED` 为该维度尚未判断；`INSUFFICIENT_EVIDENCE` 为现有证据不足以支持结论。

## Trigger / Process / Outcome / Artifact / Semantic Evidence

未取得原始 trace、运行输出或工件，因此过程、结果、工件和语义效果均为 `UNASSESSED`。触发判断需要 observed `skill.selection` 事件；目前为 `BLOCKED`。即使输出文字像 Skill 的格式，也不能据此声称 Skill 已触发。负向用例还需要确认 trace 完整，才能把“未见事件”判为未触发。

## Benchmark Results

`NOT_RUN`。计划在相同任务、环境、模型、judge 和预算下比较 **with Skill / without Skill**，记录逐 case 结果、耗时及成本；目前没有基准差异结论。

## Regression Findings

`NOT_RUN`。版本回归应比较 **previous / current**，固定 eval、环境和 judge，并保留各自 run metadata。当前没有前版结果或已确认的历史失败，不能建立回归结论或把假设场景登记为真实 regression case。

## Flaky / Blocked / Infrastructure Errors

波动性 `UNASSESSED`；触发证据 `BLOCKED`；基础设施错误 `UNASSESSED`，没有证据表明发生过错误。

## Eval Validity Findings

用例和断言尚未运行，评测有效性为 `UNASSESSED`。目前没有可归类的失败：Skill Defect、Eval Defect、Infrastructure Defect 均未确认；若后续出现失败，在检查 trace、断言和运行环境前保持 `UNKNOWN`。

## Limitations 与 Recommended Actions

下一步先补齐目标 Skill 的 evals、历史失败和可复现输入，运行 `skill-up validate`；再用带完整 `skill.selection` trace 的运行逐 case 判定。校准语义 judge 后再做 benchmark；取得可比的前后版本运行后再判断 regression。`skill-up validate` 的通过结果只能证明静态配置有效，不能替代运行或语义效果证据。
