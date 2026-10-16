<div align="right"><strong>🇨🇳 中文</strong> | <a href="./2026-10-16-all-skills-review-update_EN.md">🇬🇧 English</a></div>

# 全量 Skills 逐项 Review 更新（2026-10-16）

## 结论

当前仓库有 **165 个 canonical Skill、330 个中英文 Skill 包**：Skill Engineering 5 个、testing-types 150 个、testing-workflows 10 个。此前 164 个 Skill 已有逐项静态 Review 与修复复查；本次更新补审 2026-10-12 新增的 `one-page-test-strategy`，并修复当前发现的 Playwright JSON 报告缺失。

这份更新不重复复制 164 项历史记录。完整逐项建议、修复、二次 Review 和有限真实运行证据见 [2026-10-06 全量 Review](./2026-10-06-all-skills-review.md)、[2026-10-07 修复与二次 Review](./2026-10-07-all-skills-repair-review.md) 和 [2026-10-08 起真实运行续评](./2026-10-08-review-runtime-continuation.md)。历史的 Skill 运行结果按原日期和配置理解，不代表当前全库模型评测已完成。

## 本轮逐项 Review：`one-page-test-strategy`

定位：[中文 Skill](../../skills/zh/testing-types/one-page-test-strategy/SKILL.md) · [English Skill](../../skills/en/testing-types/one-page-test-strategy/SKILL.md) · [Router 用例](../../skills/zh/testing-workflows/discover-testing/evals/cases/route-one-page-test-strategy.yaml)

| 检查点 | 结论 | 依据与边界 |
| --- | --- | --- |
| QA 工作中的合理性与正确性 | 合适 | 面向团队讨论的一页策略摘要，覆盖目标、风险、测试方式和反馈；不把它当执行计划或测试结论。源文也把“一页纸”定位为关键信息的可视化表达，而不是完整策略本身，并强调目标驱动和随项目演进。[源文](https://www.bylinzi.com/2020/01/10/one-page-test-strategy/) |
| Skill 本身的正确性与合理性 | 合适 | 与 `test-strategy` / `test-strategy-plus` 的完整策略职责有明确边界；facts、建议、假设和待确认项分开；测试象限、测试分层与反馈机制按项目证据选择，不被规定为强制执行顺序或比例。独立安装和中英文配对通过仓库质量门禁。 |
| 定义与输出 | 合适，有一项评测建议 | 输入审计、必需模块和输出结构明确，并要求不得编造门槛、责任人、生产能力或执行结果。三个 Eval 分别覆盖成功、信息不足和范围边界；边界用例以模型 Judge 定性检查摘要是否仍保持一页策略定位。由于没有真实模型运行或版面渲染证据，实际输出是否稳定紧凑仍为 `UNASSESSED`；可在后续定向 Eval 中增加长输入/多风险案例，但这不是已复现缺陷。 |

## 已修复的确定缺陷

中英文 [`ui-test-playwright` runner](../../skills/zh/testing-types/ui-test-playwright/scripts/run-tests.sh) 原先只运行 `list,html` reporter，却打印 JSON 报告路径。现在增加 JSON reporter，并通过 `PLAYWRIGHT_JSON_OUTPUT_FILE` 指向该路径；新增隔离回归测试覆盖两种语言。

## 其余审查范围与证据边界

- 其余 164 个 Skill 的逐项定位、建议、修复记录及二次 Review 保留在上述历史报告中。本轮再次运行仓库质量门禁，覆盖 330 个 Skill 包的结构、元数据、独立性、双语和 Eval 配置；门禁不证明每个专项 QA 方法在真实项目中有效。
- 截至 2026-10-11，历史续评所列 530 个新增用例状态为 PASS 94、FAIL 1、ERROR 4、NOT_RUN 431；这不是全库完整模型评测。`one-page-test-strategy` 的实际模型 Eval 仍为 `NOT_RUN`。
- `discover-testing` 保持“选 Skill 并交接”的职责。`allow_implicit_invocation` 表示宿主可以隐式选择单个 Skill，不等于仓库能保证宿主自动串接多个 Skill；本轮不增加路由或编排功能。
