# Free QA Skills 借鉴点审阅（2026-10-09）

[English](./2026-10-09-free-qa-skills-learning-review_EN.md)

## 范围与依据

审阅目标仓库 `Quality-Max/free-qa-skills` 当前 `main`，源码树 SHA：`b0f94a6bf1b50a1c124b4735f46e5b8cf6826b89`。核对了 Skill 源文件及本地相邻 Skill；这是静态阅读，不代表已运行上游 Skill 或验证其浏览器检查结果。

## 建议优先学习

| 优先级 | 上游 Skill | 借鉴点 | 与本仓库关系 |
| --- | --- | --- | --- |
| 1 | [evidence-code-audit](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/evidence-code-audit/SKILL.md) 及[审查维度清单](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/evidence-code-audit/references/dimensions.md) | 先选增量、专项或全仓审查范围；沿输入到具体故障后果追证；把严重度、置信度、覆盖度分开记录，并保留 Not assessed。 | 本地 [code-review](../../skills/zh/testing-types/code-review/SKILL.md) 聚焦 PR/diff。可学习其全仓审查模式与覆盖矩阵，不必替换现有 PR 审查契约。 |
| 2 | [script-quality-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/script-quality-review/SKILL.md) | 用“跳过仍绿、泛化 4xx、断言未覆盖用例标题、路由/选择器不存在、写入后未清理”识别假绿测试。 | 本地 [ai-generated-test-review](../../skills/zh/testing-types/ai-generated-test-review/SKILL.md) 与 [test-code-review](../../skills/zh/testing-types/test-code-review/SKILL.md) 已更系统。适合吸收其反例到 Eval，而非新增重复 Skill。 |
| 3 | [flaky-selector-scan](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/flaky-selector-scan/SKILL.md) | 把绝对 XPath、位置选择器、生成类名、深层后代、文案耦合、索引定位映射到稳定替代方案。 | 本地 [ui-test-selector-review](../../skills/zh/testing-types/ui-test-selector-review/SKILL.md) 的语义和证据约束更完整；可借鉴它的短分类表和逐类示例。 |
| 4 | [responsive-screenshots](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/responsive-screenshots/SKILL.md) | 固定 375/768/1280/1920/2560px 视口，逐项截图并报告溢出、字号、触控目标、导航折叠等问题。 | 本地 [visual-regression-testing](../../skills/zh/testing-types/visual-regression-testing/SKILL.md) 主要定义基线与比较条件；这类执行步骤和截图交付可作为补充。 |

## 可作为覆盖扩展候选

- [i18n-rtl-audit](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/i18n-rtl-audit/SKILL.md)：长文案溢出、RTL 布局、硬编码文案、`lang` / `dir` 属性。当前本地文件搜索未发现直接对应的站点端专项 Skill；若要扩展多语言 Web QA，值得做一个小范围试点。它会临时修改页面文案和 `dir`，借鉴时应限定测试环境并恢复状态。
- [cookie-privacy-scan](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/cookie-privacy-scan/SKILL.md)：检查用户同意前的网络请求、第三方追踪器和 Cookie 属性，补充本地偏会话生命周期的 [session-security-testing](../../skills/zh/testing-types/session-security-testing/SKILL.md)。借鉴时应脱敏 Cookie 值，并把法务结论留给已知司法辖区和项目规则，避免固定严重度直接变成合规结论。
- [core-web-vitals](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/core-web-vitals/SKILL.md)：浏览器采集页面性能指标，并明确未交互时 INP 未测。可补充本地以负载模型和性能分析为主的技能。不要把一次浏览器采样或其 A–F 汇总分数当作稳定基线、生产验收或发布结论。

## 不建议重复建设

上游 [test-quality-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/test-quality-review/SKILL.md)、[diff-risk-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/diff-risk-review/SKILL.md)、accessibility-check 和 agentic-app-risk-review 与本地测试代码审查、代码审查、无障碍及 AI 安全能力重叠。它们的价值主要在于短触发语、快速检查路径和紧凑报告示例；本地 Skill 已有更细的证据状态、输入边界和 Eval 契约。

## 结论

优先读 `evidence-code-audit` 和 `script-quality-review`，再把 `flaky-selector-scan` 与 `responsive-screenshots` 的紧凑分类和可见产物做法吸收进相邻 Skill 的示例或 Eval。若目标是扩展 Web 产品巡检，再评估 i18n/RTL、Cookie 隐私和 Core Web Vitals。上游浏览器 Skill 需要 Playwright MCP；本审阅没有执行这些流程。

`evidence-code-audit` 声明其部分审查框架源自 XiNian-dada 仓库并保留 MIT 条款。若复制其具体文字或素材，应保留来源与许可要求；本笔记仅提炼方法。
