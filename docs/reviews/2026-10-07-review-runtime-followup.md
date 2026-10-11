# Skill Review 实际运行续审（2026-10-07）

> 本页保留 2026-10-07 的历史结果和阻塞原因。持续外部运行授权已补齐，后续修复与最新状态见 [真实运行续评](./2026-10-08-review-runtime-continuation.md)。

[English](./2026-10-07-review-runtime-followup_EN.md) · [164 项修复报告](./2026-10-07-all-skills-repair-review.md) · [逐用例证据](../../evidence/skill-quality/2026-10-07-review-repair/runtime-followup.json)

本轮继续实际执行新用例，修复两类评分误判并同步中英文。新增的 530 个用例中，累计 **13 个不同用例报告实际 PASS、1 个历史评分 FAIL 已修复但待实际重跑、1 个 judge ERROR、515 个 NOT_RUN**。PASS 均是指定 fixture 的脚本判分，不能推断完整 Skill 套件或全库语义质量已通过。

## 已执行结果

| Skill / 用例 | EN | ZH | 结论范围 |
| --- | --- | --- | --- |
| `skill-change-verification` / `review-repair-regression` | iteration-4 PASS | iteration-2 PASS | 先前授权的两个用例；配置证据与实际行为结果分开。 |
| `skill-prose-trim` / `review-authorized-trim` | iteration-1 FAIL；修复后 iteration-2 PASS | iteration-1 PASS | 清除过程残留，保留持久契约、测量限制及历史 fixture。 |
| `discover-testing` / 4 个近邻用例 | 4 PASS | 4 PASS | 区分认证、授权、RAG 检索与回归选择；目录身份不等于 Host 已安装。 |
| `multi-role-quality-synthesis` / `review-source-union` | iteration-1 PASS | iteration-1 FAIL；修复后原输出离线重判 PASS，实际重跑阻塞 | 保留所有来源与版本、原始严重度、证据、少数 P0 和分歧。 |
| `skill-evaluation` / `review-comparable-runs` | iteration-1 ERROR | NOT_RUN | runner 已产生输出，但 judge 未完成；不计为语义通过或 Skill 失败。 |

共记录 15 个不同用例的最新结果及 16 次用例尝试；其中 11 个 PASS 来自本轮，2 个来自先前授权运行。更早的历史迭代另保留在 [model-pilot-summary.json](../../evidence/skill-quality/2026-10-07-review-repair/model-pilot-summary.json)。Codex CLI 实际观察版本为 `0.160.1`；报告未提供可靠模型身份，记为 `UNKNOWN`。响应、用例哈希、运行中采集的来源哈希（如有）及运行后来源哈希均分别记录，避免把后采集的哈希冒充运行快照。

## 发现与修复

### 1. 清理文档的末尾换行误判

`review-authorized-trim` 的 YAML 使用 `|-`，原始文件不含末尾换行。旧 grader 却要求可编辑文档与禁止修改的 JSON 都多一个换行，使正确清理被判失败。

中英文 grader 现按保留的行核对可编辑文档；禁止修改的 `fixtures/recorded.json` 仍按原始字节精确核对。回归检查同时覆盖文档有／无末尾换行、历史 fixture 被追加换行、持久禁止条款被删除。原用例输入未修改，中英文实际复测均 PASS。

定位：[EN grader](../../skills/en/skill-engineering/skill-prose-trim/evals/graders/review-authorized-trim.py) · [ZH grader](../../skills/zh/skill-engineering/skill-prose-trim/evals/graders/review-authorized-trim.py) · [RED](../../evidence/skill-quality/2026-10-07-review-repair/prose-trim-grader-red.txt) · [GREEN](../../evidence/skill-quality/2026-10-07-review-repair/prose-trim-grader-green.txt)。

### 2. 来源版本字段的合法表示被拒绝

来源联合用例要求保留来源版本、原始严重度及证据，但没有规定这两个字段只能使用扁平值。中文输出用 `{version, severity}` 和 `{version, evidence}` 明确保留版本；旧 grader 只接受字符串与数组，因表示形式不同误判失败。

中英文 grader 现兼容扁平值和显式版本对象。嵌套版本必须与来源登记一致；原始严重度、证据与来源集合仍严格核对。回归检查接受两种正确表示，并拒绝错误版本、改写严重度、伪造证据及缺少来源。中英文原输出用新 grader 离线重判 PASS；中文实际重跑受审批阻塞，历史 FAIL 保留。

定位：[EN grader](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/graders/review-source-union.py) · [ZH grader](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/graders/review-source-union.py) · [RED](../../evidence/skill-quality/2026-10-07-review-repair/source-union-grader-red.txt) · [GREEN](../../evidence/skill-quality/2026-10-07-review-repair/source-union-grader-green.txt)。

## 尚未完成的运行与原因

**脚本判分队列：**172 个新增脚本用例中，13 个已实际 PASS，1 个 grader FAIL 已修复待实际重跑，158 个尚未尝试。继续这 159 个用例的队列被自动审批拒绝：审批认为原先两个用例的明确授权未明确覆盖新批次将仓库 Skill、Prompt 与用例内容发送至 OpenAI Codex 服务的操作。该队列原设计在临时目录隔离执行、每项固定输入并记录哈希、遇到首个失败或错误停止；拒绝后未尝试绕过。

**语义 judge：**358 个新增 `agent_judge` 用例均配置 `openai/gpt-5`。一次实际尝试中，当前 Codex ChatGPT 登录的后端返回 HTTP 400，明确表示该模型不受支持。skill-up 随后的 judge 输出解析错误只是后续现象；根因记为 `JUDGE_MODEL_UNSUPPORTED_WITH_CURRENT_LOGIN`。已尝试的用例为 ERROR，余下 357 个仍为 NOT_RUN，并标记共享的兼容性前提。

skill-up v0.12.0 的 judge 配置会继承选定 runner 的引擎；API 模型 ID 合法不能证明它可通过该登录或引擎执行。参见 [官方评测文档](https://alibaba.github.io/skill-up/guide/writing-evals)和 [v0.12.0 judge 初始化源码](https://github.com/alibaba/skill-up/blob/v0.12.0/internal/credential/agent_init.go)。当前检查的独立 API 凭证环境变量及 skill-up 凭证文件均未配置。后续需兼容 provider 凭证或明确选定的兼容 judge 配置；本轮保留原 rubric 与模型配置。

## 验证与后续优化建议

- 全量质量门禁 PASS：227 个脚本测试、328 份配置合法；[检查摘要](../../evidence/skill-quality/2026-10-07-review-repair/summary.json)。
- 固定 `skills@1.7.0` 对本地 checkout 的分发 gate PASS：164 项发现及英文 functional-testing 隔离安装；[CLI 记录](../../evidence/skill-quality/2026-10-07-review-repair/cli-summary.json)。
- 两类评分误判均以真实输入复现，并有中英文 RED → GREEN 回归及恶意修改对照；[回归检查](../../scripts/tests/test_review_eval_graders.py)。
- 优化 grader 时，把必须保持的内容／证据与可接受的序列化形式分开；仅对明确不可变的 fixture 要求字节一致。
- 在批量语义评测前，先用一个真实用例验证 judge 的引擎、登录和模型兼容性，再按固定清单执行并保留观测身份。

未提交或推送。完整模型评测仍未完成；本地检查、离线重判和定向 PASS 分别保留其证据范围。
