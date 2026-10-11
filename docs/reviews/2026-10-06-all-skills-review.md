<div align="right"><strong>🇨🇳 中文</strong> | <a href="./2026-10-06-all-skills-review_EN.md">🇬🇧 English</a></div>

# 全部 Skill 逐项审查与优化建议

用于安排下一轮 Skill 优化：先看已复现问题，再按类别逐项阅读 164 组建议。本文是审查结果与建议，尚未实施修复。

## 审查范围与结论

- 日期：2026-10-06；审查当前工作区，Git HEAD 为 `c61f507f61711c3c0f0d1777136a5a4ff0e211b3`。工作区已有未提交改动，本文包含对这些现状的审查，HEAD 不代表全部被审内容。
- 范围：`skills/zh/` 与 `skills/en/` 下 **164 个 canonical Skill、328 个语言目录**：Skill Engineering 5 组、工作流 10 组、测试类型 149 组。`evidence/`、fixture、`legacy-prompts/` 不计为活跃 Skill。
- 逐组核对入口、主 Prompt、agent metadata、Eval 配置及用例；对双语结构和关键约束复核。附属脚本按重复实现归并阅读，对高风险点离线复现；长示例和其它附属资料按需抽查。
- 核心入口与 Prompt 合计 45,974 行；本次没有全面实跑所有示例、目标框架或模型评测。
- 优先级为维护建议：**P1 71 组、P2 93 组**。P1 包含已复现脚本问题、契约/路由问题与明显的专项方法缺口；不等同于 71 个已证实运行故障，也不是发布门禁判定。共享 Excel 缺陷按受影响包提高优先级，其它建议保留原级别。

结构治理较扎实：语言配对、canonical name、metadata、独立安装引用与 Eval 配置均通过本次静态检查。主要改进空间在业务输入保真、生成结果正确性、专项方法和行为评测。

## 优先处理的已复现问题

### A. 输入解析失真（P1）

| 对象 | 最小输入 | 当前离线结果 | 应验证的修复方向 |
| --- | --- | --- | --- |
| 四个 API 工具包的 `parse_api_sources.py` | `curl 'https://example.test/orders' --data '{"qty":1}'` | 解析为 GET `/orders` | 保留隐式 POST、显式方法、请求体和参数；缺依赖须显式报错，不静默返回空端点。 |
| 同上 | Postman URL `{{baseUrl}}/orders` | path 为 `/`；Bruno 输入则变成 `/{{baseUrl}}/orders` | 分开 base URL 与资源路径，保留变量；未知部分明确标记。 |
| `requirements-analysis-plus/common_parser.py` | `user_id >= -1; retry-count > 3; REQ-001` | `user id = 1; retry count 3; REQ 001` | 保留标识符、负号、运算符和规则 ID，不能把 Markdown 清理变成语义改写。 |
| 24 组包内 Excel 解析器 | A1 为 inlineStr `REQ-1`，B1 空，C1 为 `42` | 所有 24 组丢失 `REQ-1`；基础解析器还输出 `["", "42"]`，丢失列位置 | 覆盖 inlineStr/sharedStrings、稀疏列、空单元格、多工作表与格式限制，保留坐标和原文。 |

上述 curl 行在未指定其它方法选项时应为 POST，依据 [curl 官方手册](https://curl.se/docs/manpage.html#-d)。Markdown 破坏仅在 `requirements-analysis-plus` 的该实现中确认，另外三个 Plus 的 Markdown 解析已保留这些字符，不应把修复扩散到已正确的实现。

四个 API 工具包为 `api-test-bruno`、`api-test-pytest`、`api-test-restassure`、`api-test-supertest`。WSDL 的 operation 也被拼成不存在依据的 `/soap/CreateOrder`；建议保留实际 service address 与 SOAP operation/action，而不是把 operation 当 REST 路径。这里验证了转换逻辑，没有访问任何 API。

24 组 Excel 影响清单：

`accessibility-testing`, `ai-assisted-testing`, `api-testing`, `automation-testing`, `bug-reporting`, `code-review`, `daily-testing-workflow`, `discover-testing`, `functional-testing`, `manual-testing`, `mobile-testing`, `performance-testing`, `release-testing-workflow`, `requirements-analysis`, `requirements-analysis-plus`, `security-testing`, `sprint-testing-workflow`, `test-case-reviewer`, `test-case-reviewer-plus`, `test-case-writing`, `test-reporting`, `test-strategy`, `test-strategy-plus`, `testcase-writer-plus`.

本次逐个调用了这 24 组的中文解析实现；对应英文代码逐个字节相同。保留 leaf Skill 独立安装：可以在开发侧维护 canonical helper 再生成包内副本，或维护副本一致性检查；不要改成跨 Skill 相对引用或新增安装时脚本执行。

### B. API 生成工件缺乏失败敏感性（P1）

`api-test-pytest`、`api-test-restassure` 的“非空集合”检查实际为 `0 >= 0`，空输入同样通过。四个生成器普遍把正常成功码和多种 4xx 放进同一允许集合，并使用固定空/样例请求体；部分脚本还写死 3 秒门槛。没有来源化预期时，这些输出应标为待补 scaffold，不应作为已有效的业务测试。

`api-test-bruno` 还把 `{{baseUrl}}` 渲染为 `{baseUrl}`，离线调用 `_to_bru` 已确认。变量插值语法依据 [Bruno 官方文档](https://docs.usebruno.com/variables/interpolation)。修复后应对生成文件做 golden 检查，再用正确/错误响应的最小服务验证能发现错误；编译成功和请求发出均不能替代断言有效性。

### C. Plus runner 固定编造业务内容（P1）

| Skill | 输入领域 | runner 当前结果 | 建议 |
| --- | --- | --- | --- |
| `testcase-writer-plus` | 密码至少 12 字符 | 固定活动页、礼品、库存前置条件；按序号赋 P0/P1；预期为“与规则一致” | 来源化场景、风险优先级、具体可观察断言；未知数据留空或待补。 |
| `test-case-reviewer-plus` | 计算器 1+1=2 | 固定库存 P0、支付补偿和 T+1/T+2 计划 | 基于实际用例产生可定位发现；正确输入允许无发现；保留待人工决策合同。 |
| `test-strategy-plus` | 仅计算器需求 | 固定活动/库存范围、网关/缓存/队列拓扑、P1≥95% 门槛 | 仅用已提供事实生成；未提供的范围、拓扑和门槛保持未知。 |

主 Prompt 的来源、冲突和权限边界比这些 runner 更完善。建议决定 runner 是实际能力还是演示模板，再对齐名称、调用说明与产物标识；若保留为演示，必须明确不能代表语义分析结果。`requirements-analysis-plus/run_analysis.py` 也应说明关键词提取与完整多来源分析的差距。

脱敏离线输入与实际输出见 [复现证据 JSON](./2026-10-06-all-skills-review-evidence.json)。这些是局部 helper 复现，不是模型行为、目标工具或生产验收证据。

## 跨 Skill 的优化方向

1. **补专项操作方法。** 42 组专项 Skill 的当前流程更偏通用输入审计与证据报告，领域算法/检查决策/判定依据较弱。逐项建议已给出应补的矩阵、状态机、边界或 oracle；每个 Skill 先补一个最小方法与一组正确/错误示例，深入资料按需加载。
2. **让 Eval 检查实际任务结果。** 当前共 1,128 份用例配置：904 个 rule-based judge、210 个 agent judge、14 个 script judge；138/164 组每语言只有 3 个用例。judge 类型或数量本身不是缺陷，但不少成功用例未给实际被审材料，或只检查章节/关键词。应加入真实小型 fixture、正确反例和故意植入的错误；结构字段用规则/脚本，语义判断用有锚点并校准的 judge。运行仍统一使用 `skill-up`。
3. **对近邻能力做路由负例。** 认证/授权、检索/回答质量、回归范围/用例选择、生成/评审等应以同一组邻近请求验证选用边界；保留 canonical name，优先澄清边界，不直接合并或改名。实际 routing 结论需要 `skill.selection` 或 trace adapter 事件。
4. **分开来源与决策。** 延续新 Skill 的事实/推断/候选与 Human 决策分离；将 `skill-change-verification` 的 validate 分类、发布工作流的 Go/No-Go 建议统一到相同证据边界。保留未知、受阻和未执行状态。
5. **检查工具说明与重复副本。** 29 个中文包的 short description 仍使用英文 `Use this skill when...` 文案，建议改为自然中文且突出专门用途；这属于展示/选择优化，不是格式违规。框架版本按项目输入选取，提供最小可运行工件与依赖缺失说明；共享 helper 用生成/一致性检查维护，安装产物继续自洽。

保留轻量入口与独立能力单位，补充明确的操作步骤、一个工作示例，并将深资料放到按条件加载的附件；该建议符合 [Agent Skills 官方编写实践](https://agentskills.io/skill-creation/best-practices)。短文件本身不是问题，缺少能区分正确/错误结果的操作方法才是这里的关注点。

## 逐项建议

每组都列出双语入口、Eval 配置用例数、主要定位、建议及验证方向。P1 若由共享 Excel 缺陷升高，会额外说明；“Eval 配置数”不表示这些用例已在模型上通过。源码行号对应本次工作区快照。

## Skill Engineering（5 组）

### 001. skill-change-verification

[中文入口](../../skills/zh/skill-engineering/skill-change-verification/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-change-verification/SKILL.md) · **P1 / 契约澄清** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/skill-change-verification.md:9](../../skills/zh/skill-engineering/skill-change-verification/prompts/skill-change-verification.md#L9)。入口明确 validate 不等于运行时验证，但主 Prompt 将 skill-up validate 列入 Evaluation 证据等级，容易把配置校验与实际评测混淆。
- 建议与验证：将 validate 归入结构/配置验证；Evaluation 单列实际 run 与 judge 结果。补一个变更类型→必需检查→可支持结论的最小决策表。 给出只有 validate 日志的输入，必须判运行评测 NOT_RUN；再给出真实 run 元数据，分别列出证据。

### 002. skill-evaluation

[中文入口](../../skills/zh/skill-engineering/skill-evaluation/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-evaluation/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:5](../../skills/zh/skill-engineering/skill-evaluation/evals/cases/basic-success.yaml#L5)。judge、触发证据、benchmark 与 regression 边界已齐全；当前三个用例主要验证报告骨架、缺失输入和不引入第二引擎。
- 建议与验证：补可比/不可比运行对、缺少 selection 事件、基础设施超时三个真实工件 fixture；验证失败分类与比较结论，而不只检查章节。 同一模型参数的 previous/current 可比较；模型/输入改变必须标限制；无 selection 事件必须 BLOCKED。

### 003. skill-prose-review

[中文入口](../../skills/zh/skill-engineering/skill-prose-review/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-prose-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/skill-engineering/skill-prose-review/evals/cases/basic-success.yaml#L6)。契约链检查清楚，但成功用例要求审查一个 Skill，却没有给出被审查的实际文本。
- 建议与验证：提供一个带真实冲突的小型 Skill fixture，以及一份正确反例；要求定位具体行、影响和修订建议，减少仅复述审查清单的通过。 漏掉输出约束或 metadata 冲突时必须产生对应发现；正确文本不能产生相同发现。

### 004. skill-prose-trim

[中文入口](../../skills/zh/skill-engineering/skill-prose-trim/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-prose-trim/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:4](../../skills/zh/skill-engineering/skill-prose-trim/evals/cases/basic-success.yaml#L4)。保留契约、归档和 fixture 边界明确；成功用例没有提供待清理文本，断言只检查“保留”。
- 建议与验证：用 before/expected-after 文本 fixture 验证实际清理；新增正式历史记录、测量限制与过程残留混排的用例，并说明纯审查与授权编辑两种输出。 清理过程叙述后，安全约束、正式引用、历史日期和 fixture 内容必须保持。

### 005. skill-quality-review

[中文入口](../../skills/zh/skill-engineering/skill-quality-review/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-quality-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:5](../../skills/zh/skill-engineering/skill-quality-review/evals/cases/basic-success.yaml#L5)。包级审查维度完整，但成功用例仅口头声明“完整包”，没有实际包结构与内容供核对。
- 建议与验证：添加最小完整包、缺主提示词、裸文本引用缺文件、双语输出字段不一致四个 fixture；明确与 skill-prose-review 的选用边界。 必须识别植入缺陷并定位文件；正确包允许无阻塞发现；不能由目录存在推断 runtime。

## 测试类型（149 组）

### 006. acceptance-criteria-review

[中文入口](../../skills/zh/testing-types/acceptance-criteria-review/SKILL.md) · [English entry](../../skills/en/testing-types/acceptance-criteria-review/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/acceptance-criteria-review.md:3](../../skills/zh/testing-types/acceptance-criteria-review/prompts/acceptance-criteria-review.md#L3)。定位是“评审”，主提示词开头却偏向从头生成。
- 建议与验证：区分核对现有标准、建议改写、缺规则三种模式；补带 AC ID 的原标准与修改对照 fixture，验证等于阈值和重复退款的可观察预期。

### 007. accessibility-testing

[中文入口](../../skills/zh/testing-types/accessibility-testing/SKILL.md) · [English entry](../../skills/en/testing-types/accessibility-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/accessibility-testing.md:24](../../skills/zh/testing-types/accessibility-testing/prompts/accessibility-testing.md#L24)。用户影响与人工验证边界清楚。
- 建议与验证：显式记录目标 WCAG 版本/等级、成功标准 ID、键盘/读屏/自动扫描的证据类型；补自动扫描通过但键盘仍阻断的用例，避免把扫描等同合规。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/accessibility-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 008. agent-failure-recovery-testing

[中文入口](../../skills/zh/testing-types/agent-failure-recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-failure-recovery-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/agent-failure-recovery-testing.md:34](../../skills/zh/testing-types/agent-failure-recovery-testing/prompts/agent-failure-recovery-testing.md#L34)。列出了恢复维度，具体判断流程仍较概括。
- 建议与验证：补“故障→重试/补偿/升级→恢复后状态”表；用超时但已写入、部分结果和永久错误 fixture 验证重复副作用与恢复证据。

### 009. agent-long-running-testing

[中文入口](../../skills/zh/testing-types/agent-long-running-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-long-running-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/agent-long-running-testing.md:34](../../skills/zh/testing-types/agent-long-running-testing/prompts/agent-long-running-testing.md#L34)。检查点、心跳与取消维度齐全。
- 建议与验证：补中断/恢复状态机、checkpoint 版本、租约和取消竞争的判定；用崩溃后恢复与重复提交 trace 验证已完成步骤不重做、资源释放可见。

### 010. agent-loop-testing

[中文入口](../../skills/zh/testing-types/agent-loop-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-loop-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/agent-loop-testing.md:34](../../skills/zh/testing-types/agent-loop-testing/prompts/agent-loop-testing.md#L34)。已要求停止条件和预算，但缺少具体进展判断。
- 建议与验证：补动作/观察去重、无进展周期、时间/费用预算优先级；用重复调用 trace 验证进入停止或升级分支，而不只出现“循环”关键词。

### 011. agent-memory-testing

[中文入口](../../skills/zh/testing-types/agent-memory-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-memory-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/agent-memory-testing.md:34](../../skills/zh/testing-types/agent-memory-testing/prompts/agent-memory-testing.md#L34)。记忆生命周期与隔离维度明确。
- 建议与验证：补版本/来源/租户标识、过期和删除后检索判据；用两个租户、旧新偏好冲突及删除 fixture 检查污染和遗忘，未知保留策略不能自定。

### 012. agent-permission-testing

[中文入口](../../skills/zh/testing-types/agent-permission-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-permission-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/agent-permission-testing.md:34](../../skills/zh/testing-types/agent-permission-testing/prompts/agent-permission-testing.md#L34)。已涵盖批准/拒绝，需将其转成主体×工具×资源×动作矩阵。
- 建议与验证：补授权撤销、委派和参数变更后重审批用例，检查拒绝时无副作用并保留实际授权来源。

### 013. agent-tool-testing

[中文入口](../../skills/zh/testing-types/agent-tool-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-tool-testing/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/agent-tool-testing/evals/cases/basic-success.yaml#L6)。工具契约维度具体，成功评测只检查通用章节。
- 建议与验证：提供真实工具 schema 与调用 trace，断言参数合法性、工具选择、超时后一次副作用；避免只凭标题认定契约已验证。

### 014. ai-agent-testing

[中文入口](../../skills/zh/testing-types/ai-agent-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-agent-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ai-agent-testing.md:42](../../skills/zh/testing-types/ai-agent-testing/prompts/ai-agent-testing.md#L42)。同时看结果与过程的原则合理。
- 建议与验证：补任务成功判据、轨迹不变量、重复试验次数/样本及终止分类；用“最终答案对但工具越权”的反例验证过程与结果分别结论。

### 015. ai-assisted-testing

[中文入口](../../skills/zh/testing-types/ai-assisted-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-assisted-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ai-assisted-testing.md:28](../../skills/zh/testing-types/ai-assisted-testing/prompts/ai-assisted-testing.md#L28)。人机分工边界清楚。
- 建议与验证：补输入脱敏、AI 草稿与采纳版本的来源链，以及耗时/返工量的基线测量；成功用例应检查人工复核点与产物验收，而非只检查高风险词。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/ai-assisted-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 016. ai-feature-testing

[中文入口](../../skills/zh/testing-types/ai-feature-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-feature-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ai-feature-testing.md:42](../../skills/zh/testing-types/ai-feature-testing/prompts/ai-feature-testing.md#L42)。质量维度完整但评分/上线门槛仍概括。
- 建议与验证：补产品任务×语言×用户群数据切片、人工标注 rubric 与拒答/降级的独立门槛；阈值来自项目并记录模型/Prompt/数据版本。

### 017. ai-generated-test-review

[中文入口](../../skills/zh/testing-types/ai-generated-test-review/SKILL.md) · [English entry](../../skills/en/testing-types/ai-generated-test-review/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 6 / EN 6。

- 定位：[prompts/review-test.md:3](../../skills/zh/testing-types/ai-generated-test-review/prompts/review-test.md#L3)。真实行为、可逃逸缺陷与 STRONG/WEAK/FAKE 契约较成熟。
- 建议与验证：补 mock 有边界但未替代被测对象、合理快照及合理状态码断言的近邻反例，校准分类误报；保持跨语言分级一致。

### 018. ai-safety-testing

[中文入口](../../skills/zh/testing-types/ai-safety-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-safety-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ai-safety-testing.md:34](../../skills/zh/testing-types/ai-safety-testing/prompts/ai-safety-testing.md#L34)。安全政策与 Human 边界明确，领域流程还较泛。
- 建议与验证：补政策版本→允许/限制/拒答/升级矩阵及合理请求对照；分别验证危险请求的处理和正常任务不过度拒绝，避免以拒答率代替安全性。

### 019. api-contract-testing

[中文入口](../../skills/zh/testing-types/api-contract-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-contract-testing/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/api-contract-testing/evals/cases/basic-success.yaml#L6)。明确契约含语义和错误，但成功断言未检查 amount 变更的实际消费者影响。
- 建议与验证：补 old/new schema 与旧客户端 fixture，区分语法可兼容、语义不兼容和迁移未知。

### 020. api-design-quality-review

[中文入口](../../skills/zh/testing-types/api-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/api-design-quality-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/api-design-quality-review/evals/cases/basic-success.yaml#L6)。operation 覆盖矩阵具体。
- 建议与验证：用真实 OpenAPI diff 校验问题定位及消费者迁移；补设计已完整的反例，要求缺证据项与证实的设计冲突分开，避免每次机械生成所有领域问题。

### 021. api-error-contract-testing

[中文入口](../../skills/zh/testing-types/api-error-contract-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-error-contract-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-error-contract-testing.md:32](../../skills/zh/testing-types/api-error-contract-testing/prompts/api-error-contract-testing.md#L32)。主 Prompt 的最低清单只有共享证据字段，没有错误契约专项判断。
- 建议与验证：补状态/错误码/字段、关联 ID、重试含义与脱敏的一致性表；用同一错误不同 operation 的响应 fixture 验证具体冲突。

### 022. api-idempotency-testing

[中文入口](../../skills/zh/testing-types/api-idempotency-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-idempotency-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-idempotency-testing.md:32](../../skills/zh/testing-types/api-idempotency-testing/prompts/api-idempotency-testing.md#L32)。主 Prompt 列输入与通用发现合同，未指导如何形成幂等判据。
- 建议与验证：补同键同载荷/异载荷、并发、有效期、超时后重试矩阵，逐项区分响应复用与业务副作用；用订单写入记录断言。

### 023. api-negative-testing

[中文入口](../../skills/zh/testing-types/api-negative-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-negative-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-negative-testing.md:32](../../skills/zh/testing-types/api-negative-testing/prompts/api-negative-testing.md#L32)。最低清单缺少负向测试分类与合法对照。
- 建议与验证：补缺失/null/空串/越界/类型/权限/大小的来源化候选；用真实约束判定拒绝、错误响应与无业务副作用，不自定状态码。

### 024. api-pagination-testing

[中文入口](../../skills/zh/testing-types/api-pagination-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-pagination-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-pagination-testing.md:32](../../skills/zh/testing-types/api-pagination-testing/prompts/api-pagination-testing.md#L32)。主 Prompt 缺分页连续性的具体判据。
- 建议与验证：补稳定排序与唯一 tie-breaker、首末空页、无重无漏、cursor 失效/篡改及变更语义；用有序 ID fixture 检查跨页集合和 next cursor。

### 025. api-rate-limit-testing

[中文入口](../../skills/zh/testing-types/api-rate-limit-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-rate-limit-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-rate-limit-testing.md:32](../../skills/zh/testing-types/api-rate-limit-testing/prompts/api-rate-limit-testing.md#L32)。配额输入明确，最低清单没有窗口/隔离的专项步骤。
- 建议与验证：补 N-1/N/N+1、突发、窗口切换、用户/租户隔离和恢复；用时间序列 fixture 验证 429/Retry-After 及成功请求不误伤。

### 026. api-schema-validation

[中文入口](../../skills/zh/testing-types/api-schema-validation/SKILL.md) · [English entry](../../skills/en/testing-types/api-schema-validation/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-schema-validation.md:32](../../skills/zh/testing-types/api-schema-validation/prompts/api-schema-validation.md#L32)。宣称支持多种 schema，主 Prompt 未区分 dialect 与关键验证规则。
- 建议与验证：先识别规范版本，检查 required/null、additionalProperties、组合 schema 和引用解析；用合法/非法样例做判定且不由样例反推完整契约。

### 027. api-security-testing

[中文入口](../../skills/zh/testing-types/api-security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-security-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-security-testing.md:31](../../skills/zh/testing-types/api-security-testing/prompts/api-security-testing.md#L31)。主 Prompt 最低清单仍是“主要风险”共享模板。
- 建议与验证：补 API 资产与主体-资源-动作关系、对象/字段/功能权限、资源消耗和服务端信任边界；用脱敏契约验证设计风险，保持静态边界。

### 028. api-test-bruno

[中文入口](../../skills/zh/testing-types/api-test-bruno/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-bruno/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/generate_bruno_requests.py:26](../../skills/zh/testing-types/api-test-bruno/scripts/generate_bruno_requests.py#L26)。生成器把 baseUrl 输出为单花括号，虚构 sample 请求体并允许大量 4xx 通过；解析器也损失变量 URL/隐式 POST。
- 建议与验证：修正变量渲染、保留契约字段、未知断言显式待补；对生成工件做离线 golden 检查。

### 029. api-test-postman

[中文入口](../../skills/zh/testing-types/api-test-postman/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-postman/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/api-test-postman/evals/cases/basic-success.yaml#L6)。结构/变量/CI 清单合理，但 eval 只检查文本。
- 建议与验证：补 Collection schema、变量作用域、登录 token 提取与 cleanup 工件 fixture；验证缺少预期时不会生成可误判为通过的断言。

### 030. api-test-pytest

[中文入口](../../skills/zh/testing-types/api-test-pytest/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-pytest/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/generate_pytest_tests.py:19](../../skills/zh/testing-types/api-test-pytest/scripts/generate_pytest_tests.py#L19)。生成器空集合断言为 len>=0，且把 401/403/404 等与成功共同接受。
- 建议与验证：按真实响应契约生成断言、缺预期时阻断或标 scaffold；补空输入失败、错误响应和请求体保真用例。

### 031. api-test-restassure

[中文入口](../../skills/zh/testing-types/api-test-restassure/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-restassure/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/generate_restassured_tests.py:24](../../skills/zh/testing-types/api-test-restassure/scripts/generate_restassured_tests.py#L24)。生成代码同样允许广泛 2xx/4xx、空集合永远成立，并写死 3 秒。
- 建议与验证：改用来源化 status/body、项目性能阈值和非空检查；补生成类编译与错误响应应失败的本地验证。

### 032. api-test-supertest

[中文入口](../../skills/zh/testing-types/api-test-supertest/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-supertest/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/generate_supertest_tests.py:22](../../skills/zh/testing-types/api-test-supertest/scripts/generate_supertest_tests.py#L22)。生成器任意 2xx/常见 4xx 均通过且写操作 body 固定为空，不能形成业务保护。
- 建议与验证：区分 app/baseUrl 运行模式、传递已知请求体与预期，增加实际失败能被捕获的工件 fixture。

### 033. api-testing

[中文入口](../../skills/zh/testing-types/api-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-testing.md:33](../../skills/zh/testing-types/api-testing/prompts/api-testing.md#L33)。多协议范围已明确，通用输出容易遗漏协议差异。
- 建议与验证：补 REST/GraphQL/gRPC/WebSocket/SOAP 的按需分支、跨请求业务后置条件与数据清理；用状态码正确但业务状态错误的例子验证设计质量。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/api-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 034. api-version-compatibility-testing

[中文入口](../../skills/zh/testing-types/api-version-compatibility-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-version-compatibility-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/api-version-compatibility-testing.md:32](../../skills/zh/testing-types/api-version-compatibility-testing/prompts/api-version-compatibility-testing.md#L32)。主 Prompt 没有版本兼容性专项清单。
- 建议与验证：补 wire/schema/语义兼容、旧客户端读取容忍、默认值、错误码与弃用路径矩阵；用旧新客户端×旧新服务端 fixture 验证迁移风险。

### 035. authentication-testing

[中文入口](../../skills/zh/testing-types/authentication-testing/SKILL.md) · [English entry](../../skills/en/testing-types/authentication-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/authentication-testing.md:31](../../skills/zh/testing-types/authentication-testing/prompts/authentication-testing.md#L31)。最低覆盖仍是通用安全模板。
- 建议与验证：补凭证生命周期、MFA、账户枚举、锁定、恢复、重放和认证状态转移，明确与授权审查分界；用脱敏登录/恢复合同验证行为候选。

### 036. authorization-testing

[中文入口](../../skills/zh/testing-types/authorization-testing/SKILL.md) · [English entry](../../skills/en/testing-types/authorization-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/authorization-testing.md:31](../../skills/zh/testing-types/authorization-testing/prompts/authorization-testing.md#L31)。主体-资源-动作只出现在输入描述，最低清单无具体权限路径。
- 建议与验证：补角色/所有权/租户/委派矩阵、横纵越权、撤权和默认拒绝；用许可/拒绝成对 fixture 检查具体边界。

### 037. automation-roi-analysis

[中文入口](../../skills/zh/testing-types/automation-roi-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/automation-roi-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/automation-roi-analysis.md:34](../../skills/zh/testing-types/automation-roi-analysis/prompts/automation-roi-analysis.md#L34)。成本和收益维度齐全，缺少可复算示例。
- 建议与验证：补建设/执行/维护成本的单位与时间窗、break-even、频率和变更率敏感性；用数值 fixture 验证结论方向，数据缺失不能给伪精确回报。

### 038. automation-testing

[中文入口](../../skills/zh/testing-types/automation-testing/SKILL.md) · [English entry](../../skills/en/testing-types/automation-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/automation-testing.md:28](../../skills/zh/testing-types/automation-testing/prompts/automation-testing.md#L28)。自动化范围取舍清楚。
- 建议与验证：将选型/执行风险与 ROI 分开，增加投入门槛、隔离/清理、失败信号和回归后置条件；用已有 Playwright 项目的候选评分 fixture 验证“暂不自动化”理由。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/automation-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 039. boundary-value-testing

[中文入口](../../skills/zh/testing-types/boundary-value-testing/SKILL.md) · [English entry](../../skills/en/testing-types/boundary-value-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/boundary-value-testing.md:32](../../skills/zh/testing-types/boundary-value-testing/prompts/boundary-value-testing.md#L32)。发现字段含边界值，却缺边界推导步骤。
- 建议与验证：补包含/排除、最小可表示步长、长度编码、货币精度和时间单位规则；用已知 [0,100] fixture 验证边界与邻近值，未知精度保留缺口。

### 040. bug-reporting

[中文入口](../../skills/zh/testing-types/bug-reporting/SKILL.md) · [English entry](../../skills/en/testing-types/bug-reporting/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/bug-reporting/evals/cases/basic-success.yaml#L6)。缺陷骨架和事实/猜测分开合理，judge 只检查“实际/严重”。
- 建议与验证：补期望来源、最小复现、脱敏证据与 severity/priority 分离断言；验证 1/3 频率不被改写成必现。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/bug-reporting/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 041. business-rule-extraction

[中文入口](../../skills/zh/testing-types/business-rule-extraction/SKILL.md) · [English entry](../../skills/en/testing-types/business-rule-extraction/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/business-rule-extraction/evals/cases/basic-success.yaml#L6)。来源与输入指令隔离写得具体。
- 建议与验证：补带表格、例外优先级与互相矛盾文档的 fixture，验证规则条件/动作/作用域是否保真；用正确规则对照防止把缺失信息写成既定业务规则。

### 042. capacity-planning-analysis

[中文入口](../../skills/zh/testing-types/capacity-planning-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/capacity-planning-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[prompts/capacity-planning-analysis.md:43](../../skills/zh/testing-types/capacity-planning-analysis/prompts/capacity-planning-analysis.md#L43)。容量与 SLO/峰值关联合理。
- 建议与验证：补吞吐-延迟-资源的来源链、扩容等待窗口与故障余量的可复算场景；明确不能用 CPU 55% 直接线性推算三倍容量，加入反例断言。

### 043. change-impact-analysis

[中文入口](../../skills/zh/testing-types/change-impact-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/change-impact-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[prompts/change-impact-analysis.md:42](../../skills/zh/testing-types/change-impact-analysis/prompts/change-impact-analysis.md#L42)。已有直接/传递影响及未追踪依赖规则。
- 建议与验证：补 changed→dependent→obligation/test 的证据图与边界停止规则；用未知动态依赖 fixture 检查扩大验证范围，保持与 PR 专项的区分。

### 044. chaos-testing

[中文入口](../../skills/zh/testing-types/chaos-testing/SKILL.md) · [English entry](../../skills/en/testing-types/chaos-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/chaos-testing.md:31](../../skills/zh/testing-types/chaos-testing/prompts/chaos-testing.md#L31)。隔离环境与不执行边界清楚，主清单缺少实验设计要素。
- 建议与验证：补稳态假设、控制组、注入点、爆炸半径、可量测停止条件和恢复证据；用未给停止条件的 fixture 强制保留阻塞。

### 045. ci-test-optimization

[中文入口](../../skills/zh/testing-types/ci-test-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/ci-test-optimization/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ci-test-optimization.md:34](../../skills/zh/testing-types/ci-test-optimization/prompts/ci-test-optimization.md#L34)。列出缓存/分片等维度，但缺测量步骤。
- 建议与验证：补队列/安装/执行/重试时间分解、关键路径与缓存有效性；用 runner 时间序列 fixture 验证优化收益不由削弱测试或隐藏失败取得。

### 046. circuit-breaker-testing

[中文入口](../../skills/zh/testing-types/circuit-breaker-testing/SKILL.md) · [English entry](../../skills/en/testing-types/circuit-breaker-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/circuit-breaker-testing.md:31](../../skills/zh/testing-types/circuit-breaker-testing/prompts/circuit-breaker-testing.md#L31)。closed/open/half-open 只在输入缺口里提示。
- 建议与验证：补计数窗口、触发阈值、探测额度、恢复失败回退和并发探测状态表；以事件序列 fixture 校验转换与兜底，而不只检查 CBR 编号。

### 047. code-review

[中文入口](../../skills/zh/testing-types/code-review/SKILL.md) · [English entry](../../skills/en/testing-types/code-review/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/code-review/evals/cases/basic-success.yaml#L6)。双门槛、分级与证据定位成熟，成功案例有真实 Patch。
- 建议与验证：补正确 Patch 的无发现对照，以及语法看似危险但已有上游保护的反例；检验合规输入不会被机械报成缺陷。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/code-review/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 048. combinatorial-testing

[中文入口](../../skills/zh/testing-types/combinatorial-testing/SKILL.md) · [English entry](../../skills/en/testing-types/combinatorial-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/combinatorial-testing.md:26](../../skills/zh/testing-types/combinatorial-testing/prompts/combinatorial-testing.md#L26)。44 行主 Prompt 主要规定证据合同，未给多因素组合生成步骤。
- 建议与验证：补 factor/value/约束建模、t-way 强度选择、合法组合过滤与覆盖核对；用小型可枚举 fixture 验证三因素交互。

### 049. cross-browser-testing

[中文入口](../../skills/zh/testing-types/cross-browser-testing/SKILL.md) · [English entry](../../skills/en/testing-types/cross-browser-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/cross-browser-testing.md:32](../../skills/zh/testing-types/cross-browser-testing/prompts/cross-browser-testing.md#L32)。缺浏览器专项最低清单。
- 建议与验证：补引擎×平台×版本矩阵与基于用户/风险的取样、真实设备和模拟证据区分；用 WebKit 专有差异 fixture 验证候选与支持声明的对应。

### 050. database-design-quality-review

[中文入口](../../skills/zh/testing-types/database-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/database-design-quality-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/database-design-quality-review/evals/cases/basic-success.yaml#L6)。对象/迁移/恢复矩阵完整。
- 建议与验证：补在线迁移分阶段与混合版本共存 fixture，断言锁表、默认值、回滚和访问模式的证据链；正确 schema 不应被机械列满所有缺陷。

### 051. decision-table-testing

[中文入口](../../skills/zh/testing-types/decision-table-testing/SKILL.md) · [English entry](../../skills/en/testing-types/decision-table-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/decision-table-testing.md:32](../../skills/zh/testing-types/decision-table-testing/prompts/decision-table-testing.md#L32)。字段要求明确，但缺决策表构造/冲突判断流程。
- 建议与验证：补条件离散化、互斥/重叠/缺规则检查、don't-care 与规则优先级；用完整四组合 fixture 验证动作对应，未知优先级不能填造。

### 052. dependency-failure-testing

[中文入口](../../skills/zh/testing-types/dependency-failure-testing/SKILL.md) · [English entry](../../skills/en/testing-types/dependency-failure-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/dependency-failure-testing.md:31](../../skills/zh/testing-types/dependency-failure-testing/prompts/dependency-failure-testing.md#L31)。主清单只列共享失败维度。
- 建议与验证：补不可达/超时/慢响应/错误/部分成功的依赖故障矩阵，区分同步与异步；用调用方状态和副作用 fixture 验证隔离、降级与恢复。

### 053. disaster-recovery-testing

[中文入口](../../skills/zh/testing-types/disaster-recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/disaster-recovery-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/disaster-recovery-testing.md:31](../../skills/zh/testing-types/disaster-recovery-testing/prompts/disaster-recovery-testing.md#L31)。灾备范围明确，但缺 RTO/RPO 的测量口径和恢复顺序。
- 建议与验证：补跨区故障、备份可用性/时间点、依赖恢复顺序及恢复后业务一致性；用时间线 fixture 判断目标而非只写灾备建议。

### 054. distributed-trace-analysis

[中文入口](../../skills/zh/testing-types/distributed-trace-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/distributed-trace-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/distributed-trace-analysis.md:42](../../skills/zh/testing-types/distributed-trace-analysis/prompts/distributed-trace-analysis.md#L42)。采样/时钟偏差边界合理。
- 建议与验证：补 parent-child、异步 span/link、独占时间与排队时间核对步骤；用重叠 span 和缺 span fixture 防止相加总耗时或将最慢 span 直接写成根因。

### 055. edge-case-discovery

[中文入口](../../skills/zh/testing-types/edge-case-discovery/SKILL.md) · [English entry](../../skills/en/testing-types/edge-case-discovery/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/edge-case-discovery/evals/cases/basic-success.yaml#L6)。来源化边界输入和风险合同齐全。
- 建议与验证：补字符/字节长度、时区切换、并发顺序的确定性 fixture，并要求候选回链到规则；正常例对照应避免无证据生成无限边界。

### 056. equivalence-partitioning

[中文入口](../../skills/zh/testing-types/equivalence-partitioning/SKILL.md) · [English entry](../../skills/en/testing-types/equivalence-partitioning/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/equivalence-partitioning.md:32](../../skills/zh/testing-types/equivalence-partitioning/prompts/equivalence-partitioning.md#L32)。要求等价类字段，但未指导如何证明“同类”。
- 建议与验证：补按相同行为划分、互斥/完备检查、条件依赖与代表值选择；用地区×邮编 fixture 验证依赖类，不把所有无效输入混成一类。

### 057. error-handling-design-review

[中文入口](../../skills/zh/testing-types/error-handling-design-review/SKILL.md) · [English entry](../../skills/en/testing-types/error-handling-design-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/error-handling-design-review/evals/cases/basic-success.yaml#L6)。失败/一致性/恢复设计覆盖较具体。
- 建议与验证：补可重试与不可重试错误、超时但副作用已提交的设计 fixture，验证消费者合同与补偿动作；同一失败不同层级要保留传播来源。

### 058. failover-testing

[中文入口](../../skills/zh/testing-types/failover-testing/SKILL.md) · [English entry](../../skills/en/testing-types/failover-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/failover-testing.md:31](../../skills/zh/testing-types/failover-testing/prompts/failover-testing.md#L31)。主备输入明确，缺切换判定流程。
- 建议与验证：补自动/手动触发、健康探测、流量转移、fencing、split-brain、RTO 和切回；用分区期间双写 fixture 验证一致性风险与恢复证据。

### 059. flaky-test-analysis

[中文入口](../../skills/zh/testing-types/flaky-test-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/flaky-test-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/flaky-test-analysis/evals/cases/basic-success.yaml#L6)。重试不可掩盖、隔离有退出条件的规则清楚。
- 建议与验证：补带 seed/worker/运行数的失败记录 fixture，按比例和相关变量设计最小复现实验；断言 quarantine 有 owner/期限且不消失于质量报告。

### 060. functional-testing

[中文入口](../../skills/zh/testing-types/functional-testing/SKILL.md) · [English entry](../../skills/en/testing-types/functional-testing/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/parse_formats.py:83](../../skills/zh/testing-types/functional-testing/scripts/parse_formats.py#L83)。核心功能方案已清楚，附带 Excel 解析器却忽略 inlineStr 并压缩稀疏列，可能损失输入。
- 建议与验证：优先修格式保真；内容再补“动作→业务后置条件”fixture，验证支付状态而不只验证页面提示。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/functional-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 061. llm-consistency-testing

[中文入口](../../skills/zh/testing-types/llm-consistency-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-consistency-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/llm-consistency-testing.md:34](../../skills/zh/testing-types/llm-consistency-testing/prompts/llm-consistency-testing.md#L34)。重复输入与版本因素已列出。
- 建议与验证：补 seed/temperature/版本控制、结构不变量与语义允许差异的分层比较；用多次输出 fixture 验证方差与偶发失败，明确无重复数据时不能证明稳定性。

### 062. llm-evaluation-design

[中文入口](../../skills/zh/testing-types/llm-evaluation-design/SKILL.md) · [English entry](../../skills/en/testing-types/llm-evaluation-design/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/llm-evaluation-design/evals/cases/basic-success.yaml#L6)。代表性、校准与统计置信均有原则。
- 建议与验证：补 rubric 锚点、人工分歧、盲评顺序和 train/test 污染的 fixture；要求输出可执行数据分层和 judge 校准步骤，非通用章节即通过。

### 063. llm-hallucination-testing

[中文入口](../../skills/zh/testing-types/llm-hallucination-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-hallucination-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/llm-hallucination-testing.md:34](../../skills/zh/testing-types/llm-hallucination-testing/prompts/llm-hallucination-testing.md#L34)。声明级证据方向准确。
- 建议与验证：补支持/矛盾/来源缺失/不可判的标签定义，拆解数值、实体与引用；用一个混合支持和虚构条款的答案 fixture 校验逐声明映射。

### 064. llm-testing

[中文入口](../../skills/zh/testing-types/llm-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-testing/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/llm-testing/evals/cases/basic-success.yaml#L6)。Prompt 主张避免精确字符串断言，但自身 eval 仍仅测通用章节。
- 建议与验证：补真实输入/输出样本与结构 parser、校准语义 rubric；以多运行重复试验检查鲁棒性和长上下文遗失。

### 065. log-analysis

[中文入口](../../skills/zh/testing-types/log-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/log-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/log-analysis/evals/cases/basic-success.yaml#L6)。时间、采样和因果边界合理。
- 建议与验证：成功案例没有实际日志。补脱敏原始日志与已知部署时间，验证排序、请求关联、异常聚类和缺失段；要求假设对应最小验证动作。

### 066. manual-testing

[中文入口](../../skills/zh/testing-types/manual-testing/SKILL.md) · [English entry](../../skills/en/testing-types/manual-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/manual-testing.md:28](../../skills/zh/testing-types/manual-testing/prompts/manual-testing.md#L28)。执行/探索并行思路合理。
- 建议与验证：补时间盒 charter、数据恢复、记录模板和未完成项状态；用短窗口 fixture 检查执行路径具体且有证据，不把检查清单写成执行完成。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/manual-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 067. metamorphic-testing

[中文入口](../../skills/zh/testing-types/metamorphic-testing/SKILL.md) · [English entry](../../skills/en/testing-types/metamorphic-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/metamorphic-testing.md:26](../../skills/zh/testing-types/metamorphic-testing/prompts/metamorphic-testing.md#L26)。主 Prompt 未定义变换关系的构造与成立前提。
- 建议与验证：补源输入/变换/输出关系/适用前提/反例，明确不能自行假设等价性；用排序置换与重复元素 fixture 检验关系。

### 068. metrics-anomaly-analysis

[中文入口](../../skills/zh/testing-types/metrics-anomaly-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/metrics-anomaly-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/metrics-anomaly-analysis/evals/cases/basic-success.yaml#L6)。统计异常与业务异常边界清楚。
- 建议与验证：成功案例未提供原始序列。补单位/采样/缺失值/季节性序列，验证基线窗口、维度拆分与相关性不冒充因果；没有基线保持不可判。

### 069. mobile-testing

[中文入口](../../skills/zh/testing-types/mobile-testing/SKILL.md) · [English entry](../../skills/en/testing-types/mobile-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/mobile-testing.md:28](../../skills/zh/testing-types/mobile-testing/prompts/mobile-testing.md#L28)。已有现实设备矩阵和平台差异。
- 建议与验证：补 OS×设备×升级路径×网络/前后台的风险选取和状态恢复判据；用 deeplink 丢参、支付中断 fixture 验证持久化状态与原始参数保真。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/mobile-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 070. mock-quality-review

[中文入口](../../skills/zh/testing-types/mock-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/mock-quality-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/mock-quality-review.md:32](../../skills/zh/testing-types/mock-quality-review/prompts/mock-quality-review.md#L32)。主 Prompt 缺 mock 专项判断步骤。
- 建议与验证：补真实契约与 stub 的字段/状态/时序差异、被测对象是否被替换、错误路径及漂移检查；用正确边界 mock 与 mock 掉被测对象的对照验证误报。

### 071. model-based-testing

[中文入口](../../skills/zh/testing-types/model-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/model-based-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/model-based-testing.md:26](../../skills/zh/testing-types/model-based-testing/prompts/model-based-testing.md#L26)。宣称从模型导路径，主 Prompt 只有通用候选步骤。
- 建议与验证：补初始/终止状态、guard、事件、动作、可达性和状态/边覆盖目标；用小型状态图 fixture 验证实际路径和不可达分支。

### 072. multi-agent-testing

[中文入口](../../skills/zh/testing-types/multi-agent-testing/SKILL.md) · [English entry](../../skills/en/testing-types/multi-agent-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/multi-agent-testing.md:34](../../skills/zh/testing-types/multi-agent-testing/prompts/multi-agent-testing.md#L34)。协作维度已列出。
- 建议与验证：补委派消息 ID、任务所有权、共享状态版本、交接确认与故障终止协议；用部分失败、双重认领和陈旧消息 trace 验证无丢任务/重复副作用。

### 073. mutation-testing-analysis

[中文入口](../../skills/zh/testing-types/mutation-testing-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/mutation-testing-analysis/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/mutation-testing-analysis.md:32](../../skills/zh/testing-types/mutation-testing-analysis/prompts/mutation-testing-analysis.md#L32)。输入要求有报告，但主 Prompt 没有变异状态分类/分母规则。
- 建议与验证：补 killed/survived/no-coverage/timeout/error/等价待判，保留算子与测试映射；用小型结果 fixture 复算分母，不能把等价待判自动排除。

### 074. negative-scenario-discovery

[中文入口](../../skills/zh/testing-types/negative-scenario-discovery/SKILL.md) · [English entry](../../skills/en/testing-types/negative-scenario-discovery/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/negative-scenario-discovery/evals/cases/basic-success.yaml#L6)。失败输入来源与副作用边界已具体。
- 建议与验证：补超时但已成功、双重失败和恢复失败 fixture，要求每个候选有拒绝/恢复/数据一致性预期，不把未知合同补成固定错误码。

### 075. observability-design-review

[中文入口](../../skills/zh/testing-types/observability-design-review/SKILL.md) · [English entry](../../skills/en/testing-types/observability-design-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/observability-design-review/evals/cases/basic-success.yaml#L6)。信号矩阵包含单位/基数/采样/成本。
- 建议与验证：补高基数标签与采样后断链的设计 fixture；断言记录预算/关联方式与告警动作，不能仅出现“采样”就通过。

### 076. pairwise-testing

[中文入口](../../skills/zh/testing-types/pairwise-testing/SKILL.md) · [English entry](../../skills/en/testing-types/pairwise-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/pairwise-testing.md:32](../../skills/zh/testing-types/pairwise-testing/prompts/pairwise-testing.md#L32)。候选字段清楚，缺成对集生成与核对过程。
- 建议与验证：补合法 pair universe、约束过滤与覆盖缺口表，明示 pairwise 不能保护高阶交互；用可枚举因素 fixture 复核所有合法 pairs。

### 077. performance-bottleneck-analysis

[中文入口](../../skills/zh/testing-types/performance-bottleneck-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-bottleneck-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/performance-bottleneck-analysis/evals/cases/basic-success.yaml#L6)。多信号交叉验证原则正确。
- 建议与验证：补阶段化 RPS/排队/CPU/连接池 fixture，让 judge 检查瓶颈假设及最小区分实验；高 CPU 或单一慢 span 不能直接作为根因。

### 078. performance-regression-analysis

[中文入口](../../skills/zh/testing-types/performance-regression-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-regression-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/performance-regression-analysis/evals/cases/basic-success.yaml#L6)。不可比环境不得下结论已明确，成功例已含机型变化但断言没有检查该限制。
- 建议与验证：补配对多运行数据，验证绝对/相对变化与不可比状态，分别报告噪声和稳定退化。

### 079. performance-result-analysis

[中文入口](../../skills/zh/testing-types/performance-result-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-result-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/performance-result-analysis/evals/cases/basic-success.yaml#L6)。有效性与分位数分析齐全，但成功用例只是说“提供指标”。
- 建议与验证：补实际阶段报告及目标，验证达到负载、样本、错误分母与阶段稳态；结果只能支持给定环境负载。

### 080. performance-test-gatling

[中文入口](../../skills/zh/testing-types/performance-test-gatling/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-gatling/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/performance-test-gatling.md:106](../../skills/zh/testing-types/performance-test-gatling/prompts/performance-test-gatling.md#L106)。场景选择和材料优先级具体。
- 建议与验证：补开放/封闭注入模型与目标 RPS 的验证、断言 API 与 DSL/版本基线；离线编译生成 Simulation，测试数据 feeder 耗尽和缺阈值路径。

### 081. performance-test-jmeter

[中文入口](../../skills/zh/testing-types/performance-test-jmeter/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-jmeter/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/performance-test-jmeter.md:27](../../skills/zh/testing-types/performance-test-jmeter/prompts/performance-test-jmeter.md#L27)。线程组/采样器清单可起步，需说明闭环线程数不等于目标 RPS、定时器/吞吐与分布式能力。
- 建议与验证：补脱敏 JMX fixture 和非 GUI 结构校验，验证 CSV 生命周期和错误/时延门槛。

### 082. performance-test-k6

[中文入口](../../skills/zh/testing-types/performance-test-k6/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-k6/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:16](../../skills/zh/testing-types/performance-test-k6/evals/cases/basic-success.yaml#L16)。场景与阈值默认较成熟。
- 建议与验证：补 arrival-rate/closed-model 的选择、dropped_iterations 与 check/threshold 区分；对脚本做离线结构核对，补契约 body 和业务 postcondition 而非仅 HTTP 成功。

### 083. performance-testing

[中文入口](../../skills/zh/testing-types/performance-testing/SKILL.md) · [English entry](../../skills/en/testing-types/performance-testing/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/parse_formats.py:83](../../skills/zh/testing-types/performance-testing/scripts/parse_formats.py#L83)。性能方案本身有风险边界，随包格式解析存在 inlineStr 丢失的共性缺陷。
- 建议与验证：先修解析；再用实际 achieved RPS、资源和错误分母 fixture 验证负载有效性，不把目标 RPS 当已达到。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/performance-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 084. performance-workload-modeling

[中文入口](../../skills/zh/testing-types/performance-workload-modeling/SKILL.md) · [English entry](../../skills/en/testing-types/performance-workload-modeling/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[prompts/performance-workload-modeling.md:43](../../skills/zh/testing-types/performance-workload-modeling/prompts/performance-workload-modeling.md#L43)。开放/封闭、在线/并发区分合理。
- 建议与验证：补输入单位、时窗、交易 mix 和会话转换的可复算例；60 万日请求不能直接推出峰值 RPS，缺峰时宽度时给条件化区间而非自定。

### 085. pr-test-impact-analysis

[中文入口](../../skills/zh/testing-types/pr-test-impact-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/pr-test-impact-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/pr-test-impact-analysis.md:43](../../skills/zh/testing-types/pr-test-impact-analysis/prompts/pr-test-impact-analysis.md#L43)。要求证据链而非文件名选测试。
- 建议与验证：补 base/head、文件/符号/依赖与 test ID 的映射表、删除测试影响、未知映射保守回退；用共享金额类型 diff 验证传递范围。

### 086. production-incident-analysis

[中文入口](../../skills/zh/testing-types/production-incident-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/production-incident-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/production-incident-analysis/evals/cases/basic-success.yaml#L6)。恢复优先与不归责原则合理。
- 建议与验证：补有时间戳的事故记录、并发变更与缓解结果 fixture，分开症状/关联/根因/验证；明确建议动作、实际动作和已批准动作的状态。

### 087. production-verification

[中文入口](../../skills/zh/testing-types/production-verification/SKILL.md) · [English entry](../../skills/en/testing-types/production-verification/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/production-verification/evals/cases/basic-success.yaml#L6)。已有限制账户、数据清理和停止条件。
- 建议与验证：补只读模式、批准写操作清单、canary 阈值与清理失败 fixture；没有原始运行结果时报告计划/待验证，保持每步副作用可追踪。

### 088. prompt-injection-testing

[中文入口](../../skills/zh/testing-types/prompt-injection-testing/SKILL.md) · [English entry](../../skills/en/testing-types/prompt-injection-testing/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/prompt-injection-testing/evals/cases/basic-success.yaml#L6)。覆盖直接/间接注入与拒绝后副作用，但三个 case 只验章节。
- 建议与验证：补含安全 canary 的不可信文档、工具调用 trace 和正常文档对照，分别验证信任边界与零未授权调用。

### 089. prompt-testing

[中文入口](../../skills/zh/testing-types/prompt-testing/SKILL.md) · [English entry](../../skills/en/testing-types/prompt-testing/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 6 / EN 6。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/prompt-testing/evals/cases/basic-success.yaml#L6)。版本回归合同已专项化。
- 建议与验证：补配对 before/after 输出、Prompt/模型/数据身份与等价改写正例；结构用 parser，语义 rubric 校准，验证不能以表面词差或单次结果认定退化。

### 090. property-based-testing

[中文入口](../../skills/zh/testing-types/property-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/property-based-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/property-based-testing.md:26](../../skills/zh/testing-types/property-based-testing/prompts/property-based-testing.md#L26)。宣称性质测试设计，主 Prompt 缺生成器与性质验证步骤。
- 建议与验证：补输入域、来源化不变量、前置限制、随机 seed、shrinking 和最小反例；用排序 fixture 校验输出有序且保持元素多重集。

### 091. quality-dashboard-design

[中文入口](../../skills/zh/testing-types/quality-dashboard-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-dashboard-design/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-dashboard-design.md:34](../../skills/zh/testing-types/quality-dashboard-design/prompts/quality-dashboard-design.md#L34)。受众/钻取/刷新维度已列出。
- 建议与验证：补决策问题→指标→口径→来源→行动的面板映射，空值/过期/未执行与零值分开；用过期绿灯和少数 P0 fixture 检验仪表盘不会掩盖阻塞。

### 092. quality-debt-analysis

[中文入口](../../skills/zh/testing-types/quality-debt-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/quality-debt-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-debt-analysis.md:34](../../skills/zh/testing-types/quality-debt-analysis/prompts/quality-debt-analysis.md#L34)。债务年龄/影响/偿还权衡齐全。
- 建议与验证：补债务与未修产品缺陷的分类、风险利息和偿还完成证据；用高龄低风险和新生高风险对照校验排序不由年龄单项决定。

### 093. quality-gate-design

[中文入口](../../skills/zh/testing-types/quality-gate-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-gate-design/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-gate-design.md:34](../../skills/zh/testing-types/quality-gate-design/prompts/quality-gate-design.md#L34)。准入/例外/回滚维度合理。
- 建议与验证：补 PASS/FAIL/BLOCKED/UNKNOWN 真值表、证据过期、例外授权人/期限与 fail-closed 条件；用缺失测试记录 fixture 验证不能默认为通过。

### 094. quality-maturity-assessment

[中文入口](../../skills/zh/testing-types/quality-maturity-assessment/SKILL.md) · [English entry](../../skills/en/testing-types/quality-maturity-assessment/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-maturity-assessment.md:34](../../skills/zh/testing-types/quality-maturity-assessment/prompts/quality-maturity-assessment.md#L34)。提到评分锚点，但没有可直接使用的锚点例。
- 建议与验证：补每维度可观察实践/工件/成熟等级示例与不适用、未知处理；不另造仓库 Quality Score，用成对团队证据 fixture 校准。

### 095. quality-metrics-design

[中文入口](../../skills/zh/testing-types/quality-metrics-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-metrics-design/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-metrics-design.md:34](../../skills/zh/testing-types/quality-metrics-design/prompts/quality-metrics-design.md#L34)。指标分子分母和解释限制已列出。
- 建议与验证：补口径字典、时窗、样本排除、去重、缺失与 lineage；用重开缺陷/重复运行 fixture 复算，区分测量问题与质量问题。

### 096. quality-productivity-metrics

[中文入口](../../skills/zh/testing-types/quality-productivity-metrics/SKILL.md) · [English entry](../../skills/en/testing-types/quality-productivity-metrics/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/quality-productivity-metrics.md:34](../../skills/zh/testing-types/quality-productivity-metrics/prompts/quality-productivity-metrics.md#L34)。反操纵和非个人绩效边界已明确。
- 建议与验证：补投入/产出/质量/流程的平衡视图、工作复杂度与统计单位，验证跨团队不可直接排名；用例数量上升但逃逸增加的反例检验结论。

### 097. quality-risk-analysis

[中文入口](../../skills/zh/testing-types/quality-risk-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/quality-risk-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[prompts/quality-risk-analysis.md:43](../../skills/zh/testing-types/quality-risk-analysis/prompts/quality-risk-analysis.md#L43)。证据评分和残余风险原则清楚。
- 建议与验证：补可观察的影响/可能性/可探测性锚点及不确定性传播；用资损低频风险与高频轻微问题对照，验证排序不被无依据数值乘积支配。

### 098. rag-quality-testing

[中文入口](../../skills/zh/testing-types/rag-quality-testing/SKILL.md) · [English entry](../../skills/en/testing-types/rag-quality-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/rag-quality-testing.md:34](../../skills/zh/testing-types/rag-quality-testing/prompts/rag-quality-testing.md#L34)。答案级 grounding/citation 与拒答方向明确。
- 建议与验证：补 query→retrieved chunks→claims→citations 对齐表、完整性与拒答 separate rubric；用有引用却不支持答案的 fixture 验证逐声明证据。

### 099. rag-retrieval-testing

[中文入口](../../skills/zh/testing-types/rag-retrieval-testing/SKILL.md) · [English entry](../../skills/en/testing-types/rag-retrieval-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/rag-retrieval-testing.md:34](../../skills/zh/testing-types/rag-retrieval-testing/prompts/rag-retrieval-testing.md#L34)。检索因素齐全，需可计算 relevance 标注与召回分母。
- 建议与验证：补 top-k、过滤/租户权限、新鲜度和排序对照；用已知相关文档集 fixture 区分检索失败、生成失败及代理指标限制。

### 100. recovery-testing

[中文入口](../../skills/zh/testing-types/recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/recovery-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/recovery-testing.md:31](../../skills/zh/testing-types/recovery-testing/prompts/recovery-testing.md#L31)。恢复目标输入明确，主清单缺量化恢复核对。
- 建议与验证：补服务恢复/数据恢复区别、RTO/RPO 起止、恢复点、一致性和业务补偿；用恢复时间线/数据快照 fixture 验证目标。

### 101. regression-optimization

[中文入口](../../skills/zh/testing-types/regression-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/regression-optimization/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/regression-optimization.md:34](../../skills/zh/testing-types/regression-optimization/prompts/regression-optimization.md#L34)。选择/排序/并行/缓存范围明确。
- 建议与验证：补风险保护约束、耗时收益与漏检风险的 before/after 可比口径；用删高风险用例可变快的反例验证优化不能以丢保护换收益。

### 102. regression-scope-analysis

[中文入口](../../skills/zh/testing-types/regression-scope-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/regression-scope-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/regression-scope-analysis.md:43](../../skills/zh/testing-types/regression-scope-analysis/prompts/regression-scope-analysis.md#L43)。范围裁剪与残余风险规则清楚。
- 建议与验证：补“变更→受影响义务→测试层/平台→包含或排除理由”的矩阵，并保留未知依赖；用间接依赖和预算不足 fixture 验证补充范围与升级条件。

### 103. regression-test-selection

[中文入口](../../skills/zh/testing-types/regression-test-selection/SKILL.md) · [English entry](../../skills/en/testing-types/regression-test-selection/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/regression-test-selection/evals/cases/basic-success.yaml#L6)。当前成功输入只有用例总量和预算，没有可选择的实际清单。
- 建议与验证：提供带 ID、时长、依赖与风险映射的用例 fixture；核对选择集合、强制项和预算不可满足分支，不能只输出选择原则。

### 104. reliability-testing

[中文入口](../../skills/zh/testing-types/reliability-testing/SKILL.md) · [English entry](../../skills/en/testing-types/reliability-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/reliability-testing.md:31](../../skills/zh/testing-types/reliability-testing/prompts/reliability-testing.md#L31)。输入已提到可用性与故障窗口，执行与最小覆盖仍主要是通用审计规则。
- 建议与验证：补 SLI 定义、观测窗口、失败计数口径、重复故障和恢复判据；用分母不同及短窗口无故障的 fixture 防止外推可靠性。

### 105. requirement-ambiguity-analysis

[中文入口](../../skills/zh/testing-types/requirement-ambiguity-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-ambiguity-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/requirement-ambiguity-analysis.md:75](../../skills/zh/testing-types/requirement-ambiguity-analysis/prompts/requirement-ambiguity-analysis.md#L75)。已有来源与澄清问题约束。
- 建议与验证：为每个歧义并列至少两种合理解释、各自后果及最小判别问题；补定义充分的正确反例，验证不会把缺规则、冲突和正常简写都归为歧义。

### 106. requirement-conflict-detection

[中文入口](../../skills/zh/testing-types/requirement-conflict-detection/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-conflict-detection/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/requirement-conflict-detection/evals/cases/basic-success.yaml#L6)。同范围互斥才算冲突的规则具体。
- 建议与验证：补同词不同角色/版本的非冲突反例，以及多条规则共同构成冲突的 fixture；输出参与规则 ID 和最小冲突集合，无法判定时保留限制。

### 107. requirement-consistency-analysis

[中文入口](../../skills/zh/testing-types/requirement-consistency-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-consistency-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 6 / EN 6。

- 定位：[prompts/requirement-consistency-analysis.md:79](../../skills/zh/testing-types/requirement-consistency-analysis/prompts/requirement-consistency-analysis.md#L79)。跨来源一致性和单来源限制已有约束。
- 建议与验证：补术语/实体映射、数值单位与状态映射规则；用别名等价、同名不同版本、同一阈值单位不同的 fixture 验证一致、矛盾和不可比较三类结论。

### 108. requirement-gap-analysis

[中文入口](../../skills/zh/testing-types/requirement-gap-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-gap-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/requirement-gap-analysis.md:43](../../skills/zh/testing-types/requirement-gap-analysis/prompts/requirement-gap-analysis.md#L43)。已有角色、规则、状态和异常维度。
- 建议与验证：把未定义规则、材料缺失、冲突与不适用分开；以一个完整需求和一个缺关键关闭条件的 fixture 检查缺口来源、影响、澄清优先级与关闭证据。

### 109. requirement-quality-review

[中文入口](../../skills/zh/testing-types/requirement-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-quality-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/requirement-quality-review/evals/cases/basic-success.yaml#L6)。六类审计与问题来源清楚。
- 建议与验证：补一份无需阻塞的正确需求和一份可定位的高风险缺陷需求；验证问题严重度、原句引用和修订建议，避免评审总要产生问题或只复述审查维度。

### 110. requirement-traceability-analysis

[中文入口](../../skills/zh/testing-types/requirement-traceability-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-traceability-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 6 / EN 6。

- 定位：[prompts/requirement-traceability-analysis.md:76](../../skills/zh/testing-types/requirement-traceability-analysis/prompts/requirement-traceability-analysis.md#L76)。双向链路和“文件存在不等于覆盖”边界清楚。
- 建议与验证：补带类型的边、同一义务多用例、旧版本映射与重复 ID 的处理；把已映射、已执行、已满足分列，并以小型追踪图验证覆盖计算。

### 111. requirements-analysis

[中文入口](../../skills/zh/testing-types/requirements-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirements-analysis/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/requirements-analysis/evals/cases/basic-success.yaml#L6)。基础需求分析契约可用，成功评测主要检查需求理解和澄清章节。
- 建议与验证：提供实际状态/规则 fixture，要求从原文导出可追踪测试点、未知规则和高价值问题，并验证完整需求不会被补上虚构缺口。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/requirements-analysis/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 112. requirements-analysis-plus

[中文入口](../../skills/zh/testing-types/requirements-analysis-plus/SKILL.md) · [English entry](../../skills/en/testing-types/requirements-analysis-plus/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 4 / EN 4。

- 定位：[scripts/common_parser.py:66](../../skills/zh/testing-types/requirements-analysis-plus/scripts/common_parser.py#L66)。多来源 Prompt 要求保真，但 common_parser 会删负号、比较符、字段名下划线；run_analysis 主要按关键词抽取并写固定问题。
- 建议与验证：先修输入保真，再标明提取器能力边界；用数值规则、角色冲突与非活动业务验证不损坏原文、不造规则。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/requirements-analysis-plus/scripts/common_parser.py#L89) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 113. resilience-testing

[中文入口](../../skills/zh/testing-types/resilience-testing/SKILL.md) · [English entry](../../skills/en/testing-types/resilience-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/resilience-testing.md:31](../../skills/zh/testing-types/resilience-testing/prompts/resilience-testing.md#L31)。专项入口有韧性目标，核心方法仍偏通用审计。
- 建议与验证：补扰动前/中/后的功能与数据不变量、降级状态和恢复判据；以部分依赖失效、恢复失败 fixture 区分韧性、可靠性和混沌实验的责任边界。

### 114. retry-testing

[中文入口](../../skills/zh/testing-types/retry-testing/SKILL.md) · [English entry](../../skills/en/testing-types/retry-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/retry-testing.md:31](../../skills/zh/testing-types/retry-testing/prompts/retry-testing.md#L31)。已列重试触发与幂等输入，缺具体判定方法。
- 建议与验证：补可重试/永久错误、次数与总时限、退避抖动、服务端提示和重复副作用矩阵；用“超时但写入成功”及多层重试 trace 验证预算与幂等。

### 115. risk-based-testing

[中文入口](../../skills/zh/testing-types/risk-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/risk-based-testing/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/risk-based-testing.md:70](../../skills/zh/testing-types/risk-based-testing/prompts/risk-based-testing.md#L70)。风险驱动且不直接替代执行已有边界。
- 建议与验证：把每项风险关联到测试目标、深度、最低证据与残余风险，并给定性判断锚点；用时间不足 fixture 检查高风险优先和需授权的取舍，避免无依据量化。

### 116. root-cause-analysis

[中文入口](../../skills/zh/testing-types/root-cause-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/root-cause-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/root-cause-analysis/evals/cases/basic-success.yaml#L6)。触发因素、根因和贡献因素区分明确。
- 建议与验证：加入两个竞争假设、反证和最小判别实验；用只有时间相关性与有因果链的成对 fixture，验证不把最后一个错误日志当作已证实根因。

### 117. secrets-exposure-review

[中文入口](../../skills/zh/testing-types/secrets-exposure-review/SKILL.md) · [English entry](../../skills/en/testing-types/secrets-exposure-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/secrets-exposure-review.md:31](../../skills/zh/testing-types/secrets-exposure-review/prompts/secrets-exposure-review.md#L31)。安全边界已有说明，秘密专项检查方法不足。
- 建议与验证：补代码/配置/CI/日志/产物/历史位置及凭据生命周期核对；用占位符、测试样例和真实格式但有效性未知的脱敏 fixture，验证脱敏引用与风险分级，不凭模式声称凭据有效。

### 118. security-requirement-review

[中文入口](../../skills/zh/testing-types/security-requirement-review/SKILL.md) · [English entry](../../skills/en/testing-types/security-requirement-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/security-requirement-review.md:31](../../skills/zh/testing-types/security-requirement-review/prompts/security-requirement-review.md#L31)。输入包含安全目标，主流程仍主要套通用审计。
- 建议与验证：补“资产→威胁→安全义务→控制→可验证验收”链路及项目给定标准版本；用不可测的“系统安全”与明确义务成对 fixture 验证建议可执行、无虚构合规结论。

### 119. security-testing

[中文入口](../../skills/zh/testing-types/security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/security-testing/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/security-testing.md:28](../../skills/zh/testing-types/security-testing/prompts/security-testing.md#L28)。资产、认证、授权与防御性验证边界清楚。
- 建议与验证：补威胁/控制/测试/证据矩阵和正常授权反例；明确设计、实际执行和漏洞确认三种状态，用“扫描无发现但未验证业务权限” fixture 防止外推安全通过。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/security-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 120. session-security-testing

[中文入口](../../skills/zh/testing-types/session-security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/session-security-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/session-security-testing.md:31](../../skills/zh/testing-types/session-security-testing/prompts/session-security-testing.md#L31)。会话专项输入齐全，但缺会话生命周期的具体覆盖。
- 建议与验证：按 Cookie/token 机制选择创建、轮换、固定、闲置/绝对过期、撤销、退出与多端状态；用退出后旧凭据和权限变化 fixture 验证预期，不自设有效期。

### 121. state-transition-testing

[中文入口](../../skills/zh/testing-types/state-transition-testing/SKILL.md) · [English entry](../../skills/en/testing-types/state-transition-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/state-transition-testing.md:32](../../skills/zh/testing-types/state-transition-testing/prompts/state-transition-testing.md#L32)。已提状态、事件与守卫，缺生成测试的具体过程。
- 建议与验证：补状态/事件/守卫/动作/目标矩阵、不可达与非法迁移、守卫边界及部分失败；用小状态图核对有效与无效迁移覆盖，而不只输出状态名。

### 122. technical-design-quality-review

[中文入口](../../skills/zh/testing-types/technical-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/technical-design-quality-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/technical-design-quality-review/evals/cases/basic-success.yaml#L6)。设计审查范围较明确。
- 建议与验证：加入实际组件/时序材料，核对接口边界、数据不变量、失败与恢复路径；用已有可靠控制的正确设计和分布式部分提交 fixture，检查定位和风险解释而非泛化建议。

### 123. test-case-reviewer

[中文入口](../../skills/zh/testing-types/test-case-reviewer/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-reviewer/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/test-case-reviewer/evals/cases/basic-success.yaml#L6)。用例审查步骤可用，评测对具体缺陷识别较弱。
- 建议与验证：补原始用例、需求和故意植入的不可观察预期/前置缺失；验证逐条定位与修订建议，并用正确用例约束误报，不从行业常识推断必有漏测。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-case-reviewer/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 124. test-case-reviewer-plus

[中文入口](../../skills/zh/testing-types/test-case-reviewer-plus/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-reviewer-plus/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 4 / EN 4。

- 定位：[scripts/run_review.py:59](../../skills/zh/testing-types/test-case-reviewer-plus/scripts/run_review.py#L59)。run_review 对计算器输入仍固定输出库存 P0、支付补偿等发现，且未实现 Prompt 的待人工决策字段。
- 建议与验证：改成基于输入的可追踪审查或明确仅为示例；用完整正确用例与非促销缺陷用例验证可无发现、不伪造覆盖结论。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-case-reviewer-plus/scripts/common_parser.py#L86) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 125. test-case-writing

[中文入口](../../skills/zh/testing-types/test-case-writing/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-writing/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/test-case-writing/evals/cases/basic-success.yaml#L6)。单一统一用例集及来源角色合并规则具体。
- 建议与验证：把合并/拆分条件、顺序与 Trace 字段做结构化检查；用同意图不同预期、四角色重复输入和来源缺版本 fixture 验证正确拆分与来源完整，而不只检查“测试用例”。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-case-writing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 126. test-code-review

[中文入口](../../skills/zh/testing-types/test-code-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-code-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-code-review.md:32](../../skills/zh/testing-types/test-code-review/prompts/test-code-review.md#L32)。“测试代码审查”主 Prompt 仍以通用审计为主，缺断言质量方法。
- 建议与验证：补失败敏感性、被测对象隔离、mock 边界、数据/并行隔离与清理；用吞异常、恒真断言和正常测试 fixture 验证实际缺陷定位。

### 127. test-data-generation

[中文入口](../../skills/zh/testing-types/test-data-generation/SKILL.md) · [English entry](../../skills/en/testing-types/test-data-generation/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-data-generation.md:43](../../skills/zh/testing-types/test-data-generation/prompts/test-data-generation.md#L43)。隐私、种子与清理规则已有约束。
- 建议与验证：补按 schema/实体关系生成有效与无效数据的过程，显式标注各组预期用途；用唯一性、外键、状态关联 fixture 校验生成数据及重现性，不只交付数据策略表。

### 128. test-data-requirement-analysis

[中文入口](../../skills/zh/testing-types/test-data-requirement-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-data-requirement-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-data-requirement-analysis.md:69](../../skills/zh/testing-types/test-data-requirement-analysis/prompts/test-data-requirement-analysis.md#L69)。限定数据需求分析而非生成，边界清楚。
- 建议与验证：补场景→实体/状态/关系→数量依据→获取与清理条件的矩阵；用缺 schema、跨实体关联和受限个人数据 fixture 验证未知量与来源可见。

### 129. test-effectiveness-analysis

[中文入口](../../skills/zh/testing-types/test-effectiveness-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-effectiveness-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-effectiveness-analysis.md:34](../../skills/zh/testing-types/test-effectiveness-analysis/prompts/test-effectiveness-analysis.md#L34)。已区分信号与结论，仍需更具体的有效性证据。
- 建议与验证：补故障/义务→测试→断言→漏检映射，分开历史逃逸与可控故障注入；用高通过率但已知漏检 fixture 检查分母、观察窗口与因果限制。

### 130. test-gap-analysis

[中文入口](../../skills/zh/testing-types/test-gap-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-gap-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/test-gap-analysis/evals/cases/basic-success.yaml#L6)。发现 ID 与来源规则具体。
- 建议与验证：补已映射未执行、已执行未满足、未映射但材料不足、不适用的成对 fixture；核对缺口分类和补测关闭证据，不能把清单项数直接算成有效覆盖率。

### 131. test-maintenance-cost-analysis

[中文入口](../../skills/zh/testing-types/test-maintenance-cost-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-maintenance-cost-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-maintenance-cost-analysis.md:34](../../skills/zh/testing-types/test-maintenance-cost-analysis/prompts/test-maintenance-cost-analysis.md#L34)。输入包含修改频率和维护时长，执行方法较概括。
- 建议与验证：按产品变化、测试缺陷、基础设施、数据与重复实现拆分成本；补样本窗口和区间估计，用相同总时长不同成因 fixture 验证建议，不据此评价个人绩效。

### 132. test-report-review

[中文入口](../../skills/zh/testing-types/test-report-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-report-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 5 / EN 5。

- 定位：[evals/cases/basic-conditional-pass.yaml:6](../../skills/zh/testing-types/test-report-review/evals/cases/basic-conditional-pass.yaml#L6)。报告、结果、缺陷和授权边界较扎实。
- 建议与验证：增加含跳过/阻塞/重跑的用例级统计 fixture，以及构建版本错配与受控条件项；核对分母、分类和建议状态，用完整一致报告约束误拒绝。

### 133. test-reporting

[中文入口](../../skills/zh/testing-types/test-reporting/SKILL.md) · [English entry](../../skills/en/testing-types/test-reporting/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/test-reporting/evals/cases/basic-success.yaml#L6)。缺证据仍完整报告且不确认通过的规则清楚。
- 建议与验证：补原始执行行与缺陷行，核对计划/执行/通过/失败/跳过/阻塞统计和重跑口径；成功样例不应只给总数，未知统计保留未知。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-reporting/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 134. test-runtime-optimization

[中文入口](../../skills/zh/testing-types/test-runtime-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/test-runtime-optimization/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-runtime-optimization.md:34](../../skills/zh/testing-types/test-runtime-optimization/prompts/test-runtime-optimization.md#L34)。已有 profiling、并行和隔离维度。
- 建议与验证：补实际关键路径与 setup/teardown 占比、资源上限、冷暖缓存口径；以同一保护义务的基线/候选运行对验证耗时改善及故障检出保留，不能只比较不同规模总时长。

### 135. test-scope-analysis

[中文入口](../../skills/zh/testing-types/test-scope-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-scope-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-scope-analysis.md:58](../../skills/zh/testing-types/test-scope-analysis/prompts/test-scope-analysis.md#L58)。分析范围与排除规则已有边界。
- 建议与验证：补版本×层级×平台×数据状态的范围单元、包含/排除依据及变更触发；用未定义边界和新需求 fixture 验证未知项，不与回归范围分析混为同一入口。

### 136. test-strategy

[中文入口](../../skills/zh/testing-types/test-strategy/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy/SKILL.md) · **P1 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-strategy.md:28](../../skills/zh/testing-types/test-strategy/prompts/test-strategy.md#L28)。风险驱动的基础策略可用。
- 建议与验证：把目标、范围、深度、资源、准入准出与证据/负责人连接成最小可执行表；用不同容量 fixture 检查取舍和未决风险，不能自动套固定通过率门槛。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-strategy/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 137. test-strategy-plus

[中文入口](../../skills/zh/testing-types/test-strategy-plus/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy-plus/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 4 / EN 4。

- 定位：[scripts/run_strategy.py:56](../../skills/zh/testing-types/test-strategy-plus/scripts/run_strategy.py#L56)。run_strategy 对仅含计算器需求仍生成库存/活动范围、网关拓扑与 P1≥95% 门槛，违背来源约束。
- 建议与验证：先停止把固定模板当作分析结果；按已提供事实生成或明确示例，并用三个非活动领域 fixture 验证未知值不被补全。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/test-strategy-plus/scripts/common_parser.py#L86) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 138. test-strategy-review

[中文入口](../../skills/zh/testing-types/test-strategy-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy-review/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 5 / EN 5。

- 定位：[evals/cases/basic-conditional-pass.yaml:6](../../skills/zh/testing-types/test-strategy-review/evals/cases/basic-conditional-pass.yaml#L6)。评审对象与阻塞边界清楚。
- 建议与验证：补完整可接受策略和带依赖/RACI/门禁冲突的策略 fixture；核对阻塞与条件项分级、关闭证据和正确输入可通过，避免把所有改进建议都当阻塞项。

### 139. test-suite-health-analysis

[中文入口](../../skills/zh/testing-types/test-suite-health-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-suite-health-analysis/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/test-suite-health-analysis.md:32](../../skills/zh/testing-types/test-suite-health-analysis/prompts/test-suite-health-analysis.md#L32)。专项名称清楚，核心仍是通用审计模板。
- 建议与验证：补用例/运行身份、失败类型、重试与隔离、重复覆盖、耗时趋势和被保护义务；用高通过率但大量重试的 fixture 验证健康结论，不自创无依据总分。

### 140. testability-analysis

[中文入口](../../skills/zh/testing-types/testability-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/testability-analysis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 6 / EN 6。

- 定位：[evals/cases/basic-success.yaml:6](../../skills/zh/testing-types/testability-analysis/evals/cases/basic-success.yaml#L6)。架构模式、可观测性与安全边界覆盖较完整。
- 建议与验证：补实际设计图/接口 fixture，验证最小安全观测点、时间/随机性控制与依赖替身建议；用已有测试缝的正确反例，避免一律建议增加调试后门。

### 141. testcase-writer-plus

[中文入口](../../skills/zh/testing-types/testcase-writer-plus/SKILL.md) · [English entry](../../skills/en/testing-types/testcase-writer-plus/SKILL.md) · **P1 / 代码正确性** · Eval 配置：ZH 3 / EN 3。

- 定位：[scripts/run_writer.py:48](../../skills/zh/testing-types/testcase-writer-plus/scripts/run_writer.py#L48)。run_writer 把密码长度需求生成为活动页/礼品/库存用例，优先级按序号赋值，预期仅写“与规则一致”。
- 建议与验证：改为来源驱动的场景、可观察断言和风险优先级或明确示例；用密码边界和空输入 fixture 验证无虚构业务数据。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-types/testcase-writer-plus/scripts/common_parser.py#L86) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 142. testing-bottleneck-analysis

[中文入口](../../skills/zh/testing-types/testing-bottleneck-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/testing-bottleneck-analysis/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/testing-bottleneck-analysis.md:34](../../skills/zh/testing-types/testing-bottleneck-analysis/prompts/testing-bottleneck-analysis.md#L34)。已列等待、依赖与交接信号。
- 建议与验证：补事件时间线、排队/执行/返工拆分、WIP 与吞吐口径；用资源闲置但依赖阻塞及高并发反降吞吐 fixture，验证瓶颈位置与可测改进，不直接归因为人力不足。

### 143. threat-modeling

[中文入口](../../skills/zh/testing-types/threat-modeling/SKILL.md) · [English entry](../../skills/en/testing-types/threat-modeling/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/threat-modeling.md:31](../../skills/zh/testing-types/threat-modeling/prompts/threat-modeling.md#L31)。输入有资产与信任边界，但具体建模方法不足。
- 建议与验证：补数据流/边界识别、威胁主体、前置条件、控制与残余风险链路；给一个可选轻量分类示例，用实际架构 fixture 验证只引用已提供组件与路径。

### 144. timeout-testing

[中文入口](../../skills/zh/testing-types/timeout-testing/SKILL.md) · [English entry](../../skills/en/testing-types/timeout-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/timeout-testing.md:31](../../skills/zh/testing-types/timeout-testing/prompts/timeout-testing.md#L31)。已列超时配置输入，缺预算与状态判定流程。
- 建议与验证：补端到端 deadline、连接/读取/排队预算、取消传播及迟到结果；用调用链预算超限和超时后已提交 fixture 检查状态、副作用与恢复证据。

### 145. ui-test-cypress

[中文入口](../../skills/zh/testing-types/ui-test-cypress/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-cypress/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-cypress.md:28](../../skills/zh/testing-types/ui-test-cypress/prompts/ui-test-cypress.md#L28)。框架入口与组件/E2E 范围明确。
- 建议与验证：补依项目版本选择配置、命令与 stub 边界，以及重试语义、会话/数据隔离和业务断言；用真实最小应用 fixture 验证错误业务结果会失败，不能仅检查测试文件存在。

### 146. ui-test-playwright

[中文入口](../../skills/zh/testing-types/ui-test-playwright/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-playwright/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 4 / EN 4。

- 定位：[prompts/ui-test-playwright.md:27](../../skills/zh/testing-types/ui-test-playwright/prompts/ui-test-playwright.md#L27)。项目、fixture 与 trace 入口已有覆盖。
- 建议与验证：生成测试应明确业务后置条件、稳定语义定位、身份/数据隔离和失败产物；用错误业务结果与并行用户 fixture 检查断言敏感性，页面标题正常不应代表业务成功。

### 147. ui-test-puppeteer

[中文入口](../../skills/zh/testing-types/ui-test-puppeteer/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-puppeteer/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-puppeteer.md:27](../../skills/zh/testing-types/ui-test-puppeteer/prompts/ui-test-puppeteer.md#L27)。浏览器自动化定位明确，执行细节可补强。
- 建议与验证：记录实际版本/浏览器配置与兼容范围，补页面/浏览器生命周期、业务就绪等待和失败产物；用新窗口、加载失败与超时 fixture 检查清理和可观察后置条件。

### 148. ui-test-selector-review

[中文入口](../../skills/zh/testing-types/ui-test-selector-review/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-selector-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-selector-review.md:32](../../skills/zh/testing-types/ui-test-selector-review/prompts/ui-test-selector-review.md#L32)。定位器审查输入已有说明，缺具体选择与验证规则。
- 建议与验证：补语义角色/名称、test ID、作用域、唯一性、动态文案与多语言稳定性比较；用重复按钮和合法稳定 CSS fixture 验证理由，避免机械禁止所有 CSS/XPath。

### 149. ui-test-selenium

[中文入口](../../skills/zh/testing-types/ui-test-selenium/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-selenium/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-selenium.md:27](../../skills/zh/testing-types/ui-test-selenium/prompts/ui-test-selenium.md#L27)。POM、Grid 与显式等待维度齐全。
- 建议与验证：补依项目版本选配置、可观察等待条件、陈旧元素处理、并行数据与 driver 清理；用重新渲染和异常退出 fixture 验证定位/等待与资源释放，不把固定 sleep 当通用修复。

### 150. ui-test-strategy

[中文入口](../../skills/zh/testing-types/ui-test-strategy/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-strategy/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-strategy.md:32](../../skills/zh/testing-types/ui-test-strategy/prompts/ui-test-strategy.md#L32)。UI 策略仍主要是通用审计，缺测试层选择方法。
- 建议与验证：补用户旅程×状态×平台矩阵，按风险分配组件/集成/E2E 与视觉/可访问性证据；用同一需求不同层可覆盖 fixture 验证最小有效组合和保留风险。

### 151. ui-test-testcafe

[中文入口](../../skills/zh/testing-types/ui-test-testcafe/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-testcafe/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-testcafe.md:27](../../skills/zh/testing-types/ui-test-testcafe/prompts/ui-test-testcafe.md#L27)。框架范围可辨，成功评测仍主要检查通用章节。
- 建议与验证：补版本/浏览器与 CI 配置、角色隔离、异步动作/等待及 reporter 失败传播；用最小应用和失败 fixture 验证生成工件可运行、业务失败返回失败状态。

### 152. ui-test-wait-strategy-review

[中文入口](../../skills/zh/testing-types/ui-test-wait-strategy-review/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-wait-strategy-review/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-wait-strategy-review.md:32](../../skills/zh/testing-types/ui-test-wait-strategy-review/prompts/ui-test-wait-strategy-review.md#L32)。等待策略专项缺少具体决策表。
- 建议与验证：按 DOM/业务状态/网络/事件选择就绪信号，核对超时预算、轮询与重试副作用；用长连接、后台请求和迟到结果 fixture 验证不会把网络空闲一律当业务就绪。

### 153. ui-test-webdriverio

[中文入口](../../skills/zh/testing-types/ui-test-webdriverio/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-webdriverio/SKILL.md) · **P2 / 方法增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/ui-test-webdriverio.md:28](../../skills/zh/testing-types/ui-test-webdriverio/prompts/ui-test-webdriverio.md#L28)。配置、服务与 BDD/TDD 维度已有说明。
- 建议与验证：补 capabilities/service/版本组合、异步命令、并行会话隔离和失败 trace 的证据字段；用配置不兼容与命令失败 fixture 验证可诊断错误，而不只输出自动化计划。

### 154. visual-regression-testing

[中文入口](../../skills/zh/testing-types/visual-regression-testing/SKILL.md) · [English entry](../../skills/en/testing-types/visual-regression-testing/SKILL.md) · **P1 / 专项方法缺口** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/visual-regression-testing.md:32](../../skills/zh/testing-types/visual-regression-testing/prompts/visual-regression-testing.md#L32)。基线与差异输入已有要求，核心比较方法不足。
- 建议与验证：补基线版本键、视口/浏览器/字体/数据、动画稳定、遮罩依据与阈值口径；用真实缺陷和已批准设计变化成对 fixture，验证差异归因及基线更新审批边界。

## 测试工作流（10 组）

### 155. daily-testing-workflow

[中文入口](../../skills/zh/testing-workflows/daily-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/daily-testing-workflow/SKILL.md) · **P1 / 评测增强** · Eval 配置：ZH 3 / EN 3。

- 定位：[evals/cases/basic-success.yaml:20](../../skills/zh/testing-workflows/daily-testing-workflow/evals/cases/basic-success.yaml#L20)。阶段、门禁、交接和日终证据定义具体；成功断言主要检查“早晨/下午”。
- 建议与验证：以红环境、P0 尚未启动和日终失败未登记作为评测输入，断言工作队列被重排、P0 失败升级且下一跳唯一；允许非标准班次按里程碑表达节奏。 环境全红时必须安排恢复/离线设计；不能仍给出已完成执行结果。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-workflows/daily-testing-workflow/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 156. discover-testing

[中文入口](../../skills/zh/testing-workflows/discover-testing/SKILL.md) · [English entry](../../skills/en/testing-workflows/discover-testing/SKILL.md) · **P1 / 路由完善** · Eval 配置：ZH 9 / EN 9。

- 定位：[prompts/discover-testing.md:19](../../skills/zh/testing-workflows/discover-testing/prompts/discover-testing.md#L19)。独立包中的 Composition 参考只覆盖五条路线，主 Prompt 的兜底路由枚举少于完整 164 个 Skill；存在“选择当前可用 Skill”与独立安装时可见清单不足的张力。
- 建议与验证：在包内提供轻量的可用能力/精确 ID 清单，并标明目录快照；扩展专项近邻负例，如认证/授权、RAG 检索/质量、回归范围/选择。保持一主至多一辅。 只复制 router 目录后，专项请求仍能给出有效 canonical ID；不存在或未安装目标应报告可用性缺口。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-workflows/discover-testing/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 157. multi-role-quality-synthesis

[中文入口](../../skills/zh/testing-workflows/multi-role-quality-synthesis/SKILL.md) · [English entry](../../skills/en/testing-workflows/multi-role-quality-synthesis/SKILL.md) · **P2 / 评测增强** · Eval 配置：ZH 5 / EN 5。

- 定位：[prompts/multi-role-quality-synthesis.md:69](../../skills/zh/testing-workflows/multi-role-quality-synthesis/prompts/multi-role-quality-synthesis.md#L69)。合并发现、来源保留、少数高风险与项目约束隔离规则很具体。
- 建议与验证：补跨 stage 报告混入、同一 source_id 不同版本、同名但非等价发现三个对抗 fixture；将来源集合完整性加成确定性检查，语义合并继续由校准 judge 负责。 不同 stage 不应静默合并；重复身份冲突可见；合并前后来源集合和少数 P0 不丢失。

### 158. product-quality-perspective

[中文入口](../../skills/zh/testing-workflows/product-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/product-quality-perspective/SKILL.md) · **P2 / 阶段覆盖** · Eval 配置：ZH 11 / EN 11。

- 定位：[evals/eval.yaml:1](../../skills/zh/testing-workflows/product-quality-perspective/evals/eval.yaml#L1)。八阶段 Prompt 和角色边界较完整，当前成功用例未逐一覆盖所有阶段。
- 建议与验证：补 test-strategy 和 test-report-review 的独立成功用例；统一 role report 的 source_id/version、发现 ID、行动证据字段，便于汇总而不硬依赖其它 Skill。 八个合法阶段各有成功行为；unsupported stage 和无产品影响均不能生成填充发现。

### 159. project-delivery-perspective

[中文入口](../../skills/zh/testing-workflows/project-delivery-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/project-delivery-perspective/SKILL.md) · **P2 / 阶段覆盖** · Eval 配置：ZH 4 / EN 4。

- 定位：[SKILL.md:3](../../skills/zh/testing-workflows/project-delivery-perspective/SKILL.md#L3)。限定三个阶段且将项目约束与质量事实分开；目前四个用例对三阶段覆盖不均。
- 建议与验证：每个支持阶段补一个成功 fixture；把交付要求、已授权决策、质量证据分列，并增加时区、依赖延期和未指派行动的表达规则。 排期压力不能改写质量状态；未知负责人/日期保持未知；报告评审约束不成为发布批准。

### 160. qa-quality-perspective

[中文入口](../../skills/zh/testing-workflows/qa-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/qa-quality-perspective/SKILL.md) · **P2 / 阶段覆盖** · Eval 配置：ZH 11 / EN 11。

- 定位：[prompts/test-strategy.md:14](../../skills/zh/testing-workflows/qa-quality-perspective/prompts/test-strategy.md#L14)。缺证据时仍输出 test-reporting 报告的规则有专门用例，角色边界较扎实。
- 建议与验证：补 test-reporting 和 test-report-review 的有证据成功路径；将高/中/低风险的影响、可能性与不确定性判断锚点写成一个小表，避免乘积表述被误作数值评分。 相同结果与缺陷输入须保持统计事实；无运行证据仍有完整受限报告；不外推质量通过。

### 161. release-testing-workflow

[中文入口](../../skills/zh/testing-workflows/release-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/release-testing-workflow/SKILL.md) · **P1 / 契约澄清** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/release-testing-workflow.md:3](../../skills/zh/testing-workflows/release-testing-workflow/prompts/release-testing-workflow.md#L3)。时间线和证据门禁清楚，但“管放行决策”和输出 Go/No-Go 的表述未像较新 Skill 那样明确区分 AI 建议与授权批准。
- 建议与验证：统一写为 Go/No-Go 建议及待授权决策，明确决策者和证据来源；将 T-14 等设为可压缩示例，并补紧急热修/灰度窗口。 只有部分回归或未完成专项时，不得输出已批准发布；热修仍保留必要门禁。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-workflows/release-testing-workflow/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 162. sprint-testing-workflow

[中文入口](../../skills/zh/testing-workflows/sprint-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/sprint-testing-workflow/SKILL.md) · **P1 / 适用性** · Eval 配置：ZH 3 / EN 3。

- 定位：[prompts/sprint-testing-workflow.md:19](../../skills/zh/testing-workflows/sprint-testing-workflow/prompts/sprint-testing-workflow.md#L19)。已有可检查 DoD 与交接；阶段表以 12 天节奏为例，成功断言只检查执行和评审词。
- 建议与验证：以用户迭代长度、容量和事件驱动里程碑映射阶段；补一周迭代、持续流、延期故事与未接受 P0 的行为用例。 压缩日历不能删除门禁；未完成故事和证据缺口必须进入遗留项。
- 共享 P1：[Excel 解析器](../../skills/zh/testing-workflows/sprint-testing-workflow/scripts/convert_formats.py#L63) 已复现 inlineStr 文本丢失；按问题 A 同步修复输入保真并检查稀疏列。

### 163. technical-quality-perspective

[中文入口](../../skills/zh/testing-workflows/technical-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/technical-quality-perspective/SKILL.md) · **P2 / 阶段覆盖** · Eval 配置：ZH 11 / EN 11。

- 定位：[prompts/code-review.md:5](../../skills/zh/testing-workflows/technical-quality-perspective/prompts/code-review.md#L5)。代码身份与可审查变更双门槛具体，八阶段边界完整。
- 建议与验证：补 requirements-analysis 和 test-strategy 的独立成功路径；固定静态发现的文件/行/版本定位格式，避免与 code-review、专项设计审查重复输出。 只有 PR 名无 diff 必须阻断；有 diff 时发现必须指向已提供代码；需求/策略阶段不能宣称实现已验证。

### 164. ux-quality-perspective

[中文入口](../../skills/zh/testing-workflows/ux-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/ux-quality-perspective/SKILL.md) · **P2 / 阶段覆盖** · Eval 配置：ZH 11 / EN 11。

- 定位：[prompts/test-report-review.md:24](../../skills/zh/testing-workflows/ux-quality-perspective/prompts/test-report-review.md#L24)。八阶段、适用性和截图证据边界较完整。
- 建议与验证：补 test-reporting/test-report-review 的独立成功用例；增加输入方式×设备×辅助技术×状态的可选证据矩阵，并标明它由项目材料选择。 单桌面截图不能外推键盘/读屏/移动体验；提供的可观察 UX 结果必须逐项保持。

## 已运行的验证与未验证部分

| 验证 | 当前结果 | 证据边界 |
| --- | --- | --- |
| 目录检查 `organize_project_dirs.py --check` | issues=0 | 只读检查，没有执行目录整理。 |
| metadata / CLI 静态契约 / integrity / independence | 328 目录，findings=0 | 结构、标识、资源链接成立，不代表任务行为正确。 |
| governance inventory / matrix / v1.4 closeout / Composition | 生成视图最新；5 relations、5 routes、10 targets | 配置与生成物一致，不代表真实路由已触发。 |
| external snapshots | 0；超限=0，坏命名=0 | 镜像卫生检查。 |
| `bash scripts/validate_skill_evals.sh` | `skill-up validate: ok=328 fail=0` | 仅 Eval YAML 配置校验。 |
| evaluation contract / eval rules / bilingual docs | findings=0；20 条规则有效 | 契约/规则/文档检查。 |
| `python3 -m unittest discover -s scripts/tests` | 191 tests，OK | 仓库现有本地脚本测试，不是全部 Skill 行为评测。 |
| Python AST | 791 文件，语法错误=0 | 仅语法。 |
| 高风险 helper 离线复现 | 见证据 JSON；24 组 Excel 实现分别复现文本丢失 | 有限合成输入，不代表目标工具已执行。 |

本次采用质量脚本的非写入检查项，未直接执行会整理目录/重生 inventory 的整套 `check_skills_quality.sh`；也未运行 `check_skills_cli_compatibility.sh` 的真实 discovery/install smoke。CLI 静态契约检查不能替代该 smoke。

未对 328 个目录运行全量模型 `skill-up run`、benchmark/regression、所有 UI/API 框架、Host/生产或业务验收。因此不提供 Quality Score，也不宣称所有 Skill 的语义效果已经通过。下一轮修复行为时，应同步中英文、维护 Eval，并按项目要求运行整套质量 gate、相关实际行为评测与分发 smoke。

## 建议实施顺序

1. **解析器与生成器正确性**：修 A/B/C，先加入离线最小回归 fixture，再验证生成工件的失败敏感性；共有副本同步且保持独立安装。
2. **专项能力最小方法**：按 42 个方法缺口逐个补核心步骤与判定依据，先选项目使用最多的能力试点，校准后扩展。
3. **Eval 与路由**：以真实小型输入、正确反例和相邻负例替代浅层关键词成功；语义与选择证据分开记录。
4. **文案与适用性**：处理角色阶段覆盖、班次/发布窗口适配、中文 metadata 展示、框架版本及依赖说明。

本次仅新增审查报告和脱敏复现证据，未修改 Skill、未提交或推送；原工作区内容保留。
