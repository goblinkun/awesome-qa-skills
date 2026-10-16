<div align="right"><strong>🇨🇳 中文</strong> | <a href="./skill-change-verification_EN.md">🇬🇧 English</a></div>

# skill-change-verification Pilot 档案

用于复核按变更影响选择验证和声明证据边界的行为。身份：canonical `skill-change-verification`，`skills/{zh,en}/skill-engineering/skill-change-verification/`；版本见 [source-manifest.json](../source-manifest.json)，日期 2026-10-03，评审者 Codex，人工业务批准尚无。

## Quality Profile

目标 L3；当前正式等级 `UNASSESSED`，已有核心与部分兼容 E3，无 E4。

| 质量域 | 状态 | 证据与限制 |
| --- | --- | --- |
| Q1 Specification | `PASS` | canonical name、入口、元数据与语言目录一致 |
| Q2 Design | `PASS` | 本次评审保留变更分类、最小足够验证及声明边界 |
| Q3 Package | `PASS` | 本次全仓质量门禁通过；命令与日志见 [verification.json](../verification.json)，不替代行为或业务验收 |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | 中英文 6/6 文本用例 PASS；实际验证执行与自然选择不能从建议反推 |
| Q5 Effectiveness | `NOT_RUN` | 未纳入选定 Benchmark，不声明增益 |
| Q6 Compatibility | `PASS` | 主 Codex 双语、第二模型中文成功采样；Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | case、原生输出/判分、范围和未知项均可追溯 |

支持：已给定变更的验证选择、缺输入处理和证据边界报告。未支持：建议中的命令已执行、版本回归通过、业务或发布批准。Case 见 [results.json](../results.json)。

## Risk Profile

定性判断，不是自动评分。

| 维度 | 等级 | 原因 |
| --- | --- | --- |
| Reasoning complexity | MEDIUM | 变更类型与验证层需准确映射 |
| Trigger ambiguity | MEDIUM | 与评测设计、代码审阅、发布门禁相近 |
| Side effects | LOW | 本 Pilot 只选择/报告验证；真实命令需按作用重新评估 |
| Tool dependency | MEDIUM | 真实验证依赖仓库命令与 runtime |
| Impact | HIGH | 漏验或过度声明可导致错误交付决定 |
| Model sensitivity | MEDIUM | 最小验证集合及证据分层可能变化 |
| Failure detectability | HIGH | 全量绿灯容易隐藏变更相关缺口 |

必要 Eval：变更已知成功、变更/命令未知、scope/risk 边界、静态与运行时证据差异、真实失败回归。运行深度本轮为报告，不是对任意项目执行测试。

## Behavior Contract

依据 `SKILL.md` 与 `prompts/skill-change-verification.md`。

- MUST：分类内容、元数据/目录、脚本、Evals 与运行时影响；选对应验证；记录执行/未执行、结果和原因；输出残余风险及可以/不能声称的结论。
- SHOULD：选择最小但足够检查，并使检查覆盖真实变更；区分静态、结构、评测、runtime 和人工审查。
- MUST NOT：把 skill-up validate 当 runtime 语义通过；猜测未知项目命令；用全量检查掩盖实际影响缺口；把未执行写成已执行。

Trigger expectation：Skill 变更验证/质量门禁/evidence level；自然选择 BLOCKED。Boundary expectation：验证建议不自动授予发布或业务批准。Output expectation：命令与证据分层、未知项、剩余风险和行动。Failure handling：缺 diff、仓库规则或命令时先说明受限验证路径，unknown 不猜测。

Side effects：本轮只读本地 Skill 与文本；真实验证命令产生的文件/外部操作必须在用户范围内。下一步需真实变更 diff 和可运行项目，执行选定检查并由责任人确认声明边界。
