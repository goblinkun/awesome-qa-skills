<div align="right"><strong>🇨🇳 中文</strong> | <a href="./functional-testing_EN.md">🇬🇧 English</a></div>

# functional-testing Pilot 档案

用于复核功能测试 Skill 的范围、行为及证据。身份：canonical `functional-testing`，`skills/{zh,en}/testing-types/functional-testing/`；版本为 [基线加工作区快照](../source-manifest.json)，日期 2026-10-03，评审者 Codex，人工业务批准尚无。

## Quality Profile

下表保留 2026-10-03 原批次状态；[2026-10-05 后续采样](../../2026-10-05-codex-benchmark-repeat/README.md)中同一任务每侧三次均 PASS，不升级等级或统计增益声明。

目标 L3；当前正式等级 `UNASSESSED`。已收集 L2 方向核心用例与部分 L3 证据；证据最高为限定范围的 E3，不含 E4。

| 质量域 | 状态 | 证据与限制 |
| --- | --- | --- |
| Q1 Specification | `PASS` | 入口/frontmatter/元数据对应，当前文件身份有 SHA256；仅规范检查 |
| Q2 Design | `PASS` | 本次范围评审：业务功能覆盖与性能/安全等专项验证不混淆；契约见下文 |
| Q3 Package | `PASS` | 本次全仓质量门禁通过；命令与日志见 [verification.json](../verification.json)，不替代行为或业务验收 |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | 中英文 6/6 显式使用文本用例 PASS；自然选择 BLOCKED，不授予整体可靠性 |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | with/without 单次均 5/5 semantic criteria；未观察到质量增益 |
| Q6 Compatibility | `PASS` | 主 Codex 双语、第二 Codex 模型中文成功用例采样；Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | 原生结果、历史断言失败、重判分、真实复测与限制均可追溯 |

支持：本次风险导向计划、信息不全初版、范围/优先级边界用例成功。未支持：自动触发、真实功能测试已执行、统计增益、生产或发布验收。Case 与路径见 [results.json](../results.json) 中本 Skill 的记录。

## Risk Profile

以下为评审判断，不是自动风险评分；实际目标系统会改变风险。

| 维度 | 等级 | 原因 |
| --- | --- | --- |
| Reasoning complexity | MEDIUM | 业务链路、数据和异常路径需要关联 |
| Trigger ambiguity | MEDIUM | 与日常测试、API、UI、测试策略任务重叠 |
| Side effects | LOW | 本 Pilot 只输出计划；实际执行必须单独授权 |
| Tool dependency | LOW | 文本计划仅依赖本地 Skill 资源 |
| Impact | HIGH | 漏掉支付、履约或权限风险会误导发布判断 |
| Model sensitivity | MEDIUM | 风险排序和信息缺口表达可能变化 |
| Failure detectability | MEDIUM | 文字覆盖可查，业务遗漏仍需领域评审 |

必要 Eval：成功、不完整输入、风险优先级、领域边界、正负触发、困难任务 Benchmark、真实失败回归。兼容范围仅为本报告的 Codex 采样；运行深度仅文本，不包含 UI/API 实际操作。

## Behavior Contract

依据当前 `SKILL.md` 与 `prompts/functional-testing.md`，不新增 Skill 执行权限。

- MUST：读取主提示词；说明范围、关键链路、正向/异常/边界、角色、数据和集成点；按业务风险排优先级；区分确认事实、假设和缺口。
- SHOULD：给可执行场景、预期结果和下一步；输入不全时提供带限制的初版；默认 Markdown，尊重明确格式要求。
- MUST NOT：编造接口、字段、环境或根因；平均摊铺所有优先级；把计划当已执行结果或把未验证项目写成通过。

Trigger expectation：功能测试/functional testing 及功能计划/用例任务；正负自然选择尚未观测。Boundary expectation：专项性能与渗透测试不能由本计划替代。Output expectation：风险与场景具体、缺口明确，不把固定中文短语当作领域质量本身。Failure handling：缺少需求/环境时保留假设和待确认事项，不伪造结果。

Side effects：本轮预期为本地资源读取和文本产物；没有授权生产写操作。下一步是获得领域审阅的真实需求、补自然选择 trace，并用较稀疏/困难输入有限重复 Benchmark。
