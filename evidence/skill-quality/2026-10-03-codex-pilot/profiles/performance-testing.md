<div align="right"><strong>🇨🇳 中文</strong> | <a href="./performance-testing_EN.md">🇬🇧 English</a></div>

# performance-testing Pilot 档案

用于复核性能测试计划而非真实压测结果。身份：canonical `performance-testing`，`skills/{zh,en}/testing-types/performance-testing/`；版本见 [source-manifest.json](../source-manifest.json)，日期 2026-10-03，评审者 Codex，人工业务批准尚无。

## Quality Profile

目标 L2 + 部分 L3；当前正式等级 `UNASSESSED`。本轮获得 L2 方向文本用例与 Codex 采样 E3，不含真实负载实验/E4。

| 质量域 | 状态 | 证据与限制 |
| --- | --- | --- |
| Q1 Specification | `PASS` | 入口、目录、元数据一致，快照可复核 |
| Q2 Design | `PASS` | 本次评审明确性能目标/负载/指标与其他专项边界 |
| Q3 Package | `PASS` | 本次全仓质量门禁通过；命令与日志见 [verification.json](../verification.json)，不替代行为或业务验收 |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | 中英文 6/6 文本用例 PASS；真实负载和自然选择未证明 |
| Q5 Effectiveness | `NOT_RUN` | 不在本轮三个选定 Benchmark 中，没有增益声明 |
| Q6 Compatibility | `PASS` | 主 Codex 双语、第二模型中文成功用例；不是领域正确性完整矩阵 |
| Q7 Evidence/Evolution | `PASS` | 信息缺口断言修复与实际复测可追溯 |

支持：范围/目标、负载假设、测试类型、阈值与环境需求的文本计划。未支持：任何 QPS、p95、容量或优化效果已测得；真实压测、稳定性、业务验收。Case 见 [results.json](../results.json)。

## Risk Profile

定性判断，真实目标风险应重新评估。

| 维度 | 等级 | 原因 |
| --- | --- | --- |
| Reasoning complexity | HIGH | 负载模型、指标、瓶颈与环境差异相互影响 |
| Trigger ambiguity | MEDIUM | 与容量规划、性能诊断等相近 |
| Side effects | LOW | 本轮只有计划；真实压测可能 HIGH，须另行授权 |
| Tool dependency | LOW | 本轮文本；真实压测依赖工具、监控和目标 |
| Impact | HIGH | 错误阈值或负载假设可导致错误容量/发布决定 |
| Model sensitivity | HIGH | 领域建议及未经证实的数字容易变化 |
| Failure detectability | HIGH | 好看的计划需真实数据与性能专家才能检验 |

必要 Eval：成功、缺目标/环境、领域边界、负载/单位/阈值判断、模型敏感性；真实压测应另设输入、预算、停止阈值与回滚。当前没有替代真实工具验证。

## Behavior Contract

依据 `SKILL.md` 与 `prompts/performance-testing.md`。

- MUST：读取主提示词；明确范围、目标、关键交易、流量/并发假设、类型、成功标准、数据、环境、监控指标和风险；区分事实与假设。
- SHOULD：优先高风险交易；给可执行计划和验证方法；未知阈值明确待确认，不把建议数字写成产品要求。
- MUST NOT：编造接口、环境、容量、性能结果或根因；用功能/安全用例替代负载目标；把未运行压测写成通过。

Trigger expectation：性能测试/performance testing 及 load/stress/spike/endurance/capacity 目标；自然选择 BLOCKED。Boundary expectation：文本计划不等于压测执行或优化验收。Output expectation：负载/指标/环境/数据与限制对应，不以“待确认”某一固定短语判定全部质量。Failure handling：缺输入时给带假设初版并列出阻塞实测的缺口。

Side effects：本轮未向目标发流量。下一步需真实 SLO、脱敏交易与授权压测环境、流量预算、停止条件和监控证据，不能直接对生产系统施压。
