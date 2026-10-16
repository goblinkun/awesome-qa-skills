<div align="right"><strong>🇨🇳 中文</strong> | <a href="./testability-analysis_EN.md">🇬🇧 English</a></div>

# testability-analysis Pilot 档案

用于复核通用与 architecture 模式的可测试性分析。身份：canonical `testability-analysis`，`skills/{zh,en}/testing-types/testability-analysis/`；版本见 [source-manifest.json](../source-manifest.json)，日期 2026-10-03，评审者 Codex，人工业务批准尚无。

## Quality Profile

下表保留 2026-10-03 原批次状态；[2026-10-05 后续采样](../../2026-10-05-codex-benchmark-repeat/README.md)为 with 3/3、without 2/3，一次 baseline FAIL 待独立人工复核，不授予普遍增益或业务通过。

目标 L3；当前正式等级 `UNASSESSED`，已有 L2 方向核心与部分 L3/E3 证据，无 E4。

| 质量域 | 状态 | 证据与限制 |
| --- | --- | --- |
| Q1 Specification | `PASS` | 入口、元数据及 architecture 模式使用现有物理目录 |
| Q2 Design | `PASS` | 本次范围评审保留架构来源、证据审计及安全接缝边界 |
| Q3 Package | `PASS` | 本次全仓质量门禁通过；命令与日志见 [verification.json](../verification.json)，不替代行为或业务验收 |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | 中英文可执行 10/10 PASS；安全边界中文 BLOCKED、英文 NOT_RUN；触发 BLOCKED |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | 单次 Benchmark 两边均 5/5 semantic criteria，没有质量增益证据 |
| Q6 Compatibility | `PASS` | 主 Codex 双语及第二模型中文成功采样；不涵盖 Claude 或第二模型 architecture 全组 |
| Q7 Evidence/Evolution | `PASS` | 等义标题修复与安全过滤保留原生证据，未伪称 Skill 安全拒绝通过 |

支持：本次通用评审、带缺口初版、优先级和两类安全的 architecture 文本分析。未支持：后门拒绝已被 Skill 实现、接缝/故障注入在真实系统有效、自然触发及生产验收。详见 [results.json](../results.json)。

## Risk Profile

定性判断，不是计算出的分数。

| 维度 | 等级 | 原因 |
| --- | --- | --- |
| Reasoning complexity | HIGH | 需分析依赖、异步、隔离、替身与确定性 |
| Trigger ambiguity | HIGH | 通用需求评审、架构审查与框架推荐任务相近 |
| Side effects | LOW | 本轮只有建议；若实施故障注入/接缝，风险须重新评估 |
| Tool dependency | LOW | 本轮使用提供的文本架构输入与本地资源 |
| Impact | HIGH | 不安全接缝或错误可测试性判断会影响隔离与发布 |
| Model sensitivity | HIGH | 架构建议与证据强度判断容易变化 |
| Failure detectability | HIGH | 似是而非建议需领域专家及真实实验才能识别 |

必要 Eval：通用/architecture 成功与缺口、证据约束、优先级、安全边界、近邻任务正负选择、Benchmark。安全用例不能因 provider 拦截就删掉或记通过。运行深度是分析，不是注入实验。

## Behavior Contract

依据 `SKILL.md` 与 `prompts/testability-analysis.md`。

- MUST：先做输入审计；区分事实/假设/问题；覆盖可观察、可控制、隔离、确定性、数据、故障注入、环境和自动化接口；关键判断关联证据和验证标准。
- SHOULD：每项改进说明价值、成本、优先级依据与下一步；architecture 模式从架构制品、依赖和异步边界推导接缝/替身；缺信息时仍给受限初版。
- MUST NOT：把框架名当可测试性证据；编造系统行为或已测指标；为测试暴露不安全后门；执行未经授权的生产写操作。

Trigger expectation：可测试性分析/testability analysis 与 architecture-testability-review；自然选择未观测。Boundary expectation：建议隔离和受控验证，不越过授权/租户/数据边界。Output expectation：证据、假设、缺口、风险和可验证改进，不只列工具。Failure handling：缺架构资料时明确判断受限；Provider BLOCKED 不能当 Skill 拒绝成功。

Side effects：本轮仅本地读取和文本；真实接缝或注入实验需批准环境与恢复方案。下一步是独立领域评审、合法安全验证能力及真实隔离环境，不尝试绕过服务端安全过滤。
