<div align="right"><strong>🇨🇳 中文</strong> | <a href="./skill-evaluation_EN.md">🇬🇧 English</a></div>

# skill-evaluation Pilot 档案

用于复核 Skill 评测设计和证据解释。附件名称 `skill-evaluation-design` 映射为已有 canonical `skill-evaluation`，不创建别名。目录 `skills/{zh,en}/skill-engineering/skill-evaluation/`；版本见 [source-manifest.json](../source-manifest.json)，日期 2026-10-03，评审者 Codex，人工业务批准尚无。

## Quality Profile

下表保留 2026-10-03 原批次状态；[2026-10-05 后续采样](../../2026-10-05-codex-benchmark-repeat/README.md)为 with 3/3、without 0/3，仍只证明该任务的规范状态标签差异；baseline semantic judge 未执行。

目标 L3；当前正式等级 `UNASSESSED`，已有核心与部分 L3/E3；没有 E4。

| 质量域 | 状态 | 证据与限制 |
| --- | --- | --- |
| Q1 Specification | `PASS` | canonical name、入口和元数据对应，目录可独立复制 |
| Q2 Design | `PASS` | 本次范围评审维持 skill-up 和既有评分/状态契约，不再造引擎 |
| Q3 Package | `PASS` | 本次全仓质量门禁通过；命令与日志见 [verification.json](../verification.json)，不替代行为或业务验收 |
| Q4 Behavior | `INSUFFICIENT_EVIDENCE` | 中英文最新完整组 6/6 PASS；极少输入保留 canonical state；自然选择 BLOCKED |
| Q5 Effectiveness | `INSUFFICIENT_EVIDENCE` | 单次状态契约遵守差异；baseline semantic judge 未执行，不能算普遍质量增益 |
| Q6 Compatibility | `PASS` | 主 Codex 双语、第二模型中文成功采样；Claude NOT_RUN |
| Q7 Evidence/Evolution | `PASS` | 旧 scope 误判、judge 误判、近似错误样例及真实复测均保留 |

支持：最小评测设计、缺少运行证据时的状态区分、既有引擎范围评审。未支持：自然选择、已完成业务评测、整体评分、发布批准及 previous/current 版本回归。详见 [results.json](../results.json)。

## Risk Profile

定性判断，不计算新分数。

| 维度 | 等级 | 原因 |
| --- | --- | --- |
| Reasoning complexity | HIGH | 需分开 Outcome/Process、validity、judge 与多层证据 |
| Trigger ambiguity | HIGH | 与变更验证、治理及普通测试设计重叠 |
| Side effects | MEDIUM | 获授权运行评测会调用模型并生成文件；本轮主体仅文本 |
| Tool dependency | HIGH | 真正评测依赖 skill-up、runtime、trace 和 judge |
| Impact | HIGH | 错误 PASS/评分可误导全仓质量与发布判断 |
| Model sensitivity | HIGH | 状态语义与 rubric 选择存在模型差异 |
| Failure detectability | HIGH | 表面可信报告可能混淆静态/触发/业务证据 |

必要 Eval：成功、极少输入、状态 enum、范围评审、触发证据缺失、Benchmark vs regression、judge 正反/近似错误校准。目标运行深度按任务授权分层，评测设计本身不是实际评测成功。

## Behavior Contract

依据 `SKILL.md` 与 `prompts/skill-evaluation.md`。

- MUST：读取目标契约与主提示词；使用 skill-up；优先确定性；按需要选择语义 judge 并校准；记录 run metadata、case、judge、限制和失败分类；最小报告保留适用 canonical evidence state。
- SHOULD：选择有意义的行为/触发/边界/回归用例；有真实失败根因时才沉淀 Skill 回归；用最低成本有效验证。
- MUST NOT：在本 Skill 工作流内另造全局 Engine/Judge/Benchmark/Quality Score；伪造 trace/分数；以输出相似代替 observed trigger；把静态/单次观察升级为业务/发布结论；自动无限修改 Skill。

Trigger expectation：Skill 评测/设计/解释和评测回归；选择观测 BLOCKED。Boundary expectation：范围评审明确保留当前流程；**不把 Skill 文案当成可忽略更高优先级、另行授权架构需求的依据**。Output expectation：scope、结果、证据状态、blocked checks、下一步，不强制翻译正式英文模板标题。Failure handling：unknown 保持 unknown，缺 trace 写 BLOCKED，未运行写 NOT_RUN，评分未执行写 NOT_SCORED。

Side effects：设计阶段只读/文本；真实模型或脚本执行须在已授权范围内，不能自动改 Skill。下一步需人工确认 judge anchors、自然选择事件和真实项目的报告使用验收。
