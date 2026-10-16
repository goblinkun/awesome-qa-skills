<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# SQET Codex Pilot 证据报告

用于复核五个 SQEM Pilot 的真实文本运行、选定 Benchmark 与跨模型采样。运行日期为 **2026-10-03**；这是工程验证报告，不是业务验收或发布批准。

## 结果

| 验证项 | 结果 | 边界 |
| --- | --- | --- |
| 5 个 Pilot，中英文核心用例 | 34/34 `PASS` | 36 个计划用例中实际可执行的 34 个；修正 Eval 后选取最新完整组，每个用例一次 |
| 可测试性安全边界，中文 | `BLOCKED` | 原生结果为 `ERROR`，服务端安全过滤在产生回答前拦截；不能评价 Skill 拒绝行为 |
| 同一安全边界，英文 | `NOT_RUN` | 中文拦截后主动停止等价请求，没有推断英文结果，也没有换模型绕过过滤 |
| 第二个 Codex 模型 | 5/5 `PASS` | 仅五个中文 `basic-success`，不是完整第二模型矩阵 |
| 选定 Benchmark | 3 组已运行 | 每组 with/without 各一次；详见下文 |
| Judge 烟雾校准 | 7/7 符合预期标签 | 合成正反样例及近似错误样例，不计入真实 Pilot 通过数，不代表统计可靠性 |
| 自然触发/选择 | `BLOCKED` | 没有 canonical `skill.selection` 事件；可用目录和读取文件不能替代该事件 |
| Claude 运行 | `NOT_RUN` | 当前进程没有该 provider 的环境变量凭据；CLI 已安装不等于运行验收 |
| 真实业务验收 | `NOT_RUN` | 缺少真实项目、授权环境/操作、验收标准及责任人决定 |
| Quality Score / 正式测试等级 | `NOT_SCORED` / `UNASSESSED` | 不把断言通过率变成全局评分，不授予完整 L3/L4 或发布结论 |

当前核心组：functional-testing 6/6、testability-analysis 10/10（另有上述两个未验证安全用例）、performance-testing 6/6、skill-evaluation 6/6、skill-change-verification 6/6。中英文均包含成功、不完整输入及范围/风险边界；这里只验证明确要求使用 Skill 的文本行为。

## Run Metadata

- Skill 基线 commit：`c61f507f61711c3c0f0d1777136a5a4ff0e211b3`，**包含尚未提交的修改**。准确身份见 [source-manifest.json](./source-manifest.json) 和 [source-changes.patch](./source-changes.patch)，不能只用 HEAD 代表测试版本。
- 主引擎：`skill-up 0.12.0`。使用其 custom local transport 调用原生 `codex-cli --no-daemon`；传输适配器不实现第二套 Judge、Benchmark 或评分。历史适配器把 `codex_version` 固定写为 `0.159.2`，不是独立版本探测；逐调用 CLI 版本保持 `unknown`，不能据此声称每次运行都使用该版本。
- Provider：`openai`。主运行 requested/observed model 为 `gpt-6.1-sol`，第二模型与 Benchmark semantic judge 为 `gpt-6-sol`；reasoning effort 为 `high`。
- Observed model 来源为 CLI session 的客户端 `turn_context`，**server-confirmed identity 为 `unknown`**。
- 环境：macOS arm64、Node.js v26.10.0、临时工作目录、900 秒 case timeout。生产、浏览器或真实目标环境均不在本次执行范围内。
- 经用户授权使用 Codex sandbox bypass。关闭用户项目说明，禁用全局/插件 Skill，with Skill 只在 `.agents/skills/<canonical-name>` 安装目标 Skill；without Skill 和 judge 不加载目标 Skill。
- 每次调用的起止时间、模型、usage、目录和错误保留在原生日志。历史各次适配器文件哈希未在运行时记录，写为 `unknown`；当前收集版与可移植版哈希分开记录，不能追认历史字节一致。

## Benchmark 的正确解释

主模型、同组输入、reasoning effort、限制和 rubric 均保持一致；基线不提供目标 Skill。输入不使用 Skill 专用输出标题作为质量要求。

| Skill | with Skill | without Skill | 可支持的结论 |
| --- | --- | --- | --- |
| functional-testing | `PASS`，5/5 semantic criteria | `PASS`，5/5 | 这个单次、信息较充分的任务未观察到质量增益 |
| testability-analysis | `PASS`，5/5 | `PASS`，5/5 | 同上，不等于 Skill 对稀疏或困难输入没有价值 |
| skill-evaluation | `PASS`，canonical 状态满足，5/5 semantic criteria | `FAIL`，缺少 `NOT_RUN`、`BLOCKED` | 观察到机器可读状态契约遵守差异，**不是普遍语义质量提升** |

第三组 baseline 使用了自然语言的“未运行/证据不足”，因此不应宣称其整体判断都错。两边应用相同的 canonical-state 前置检查；baseline 前置检查失败后，`skill-up` 没有继续调用 semantic judge。其原生 1/2 与 with Skill 的 7/7 断言比例不是可比较的 semantic 分数。首次 Benchmark 及发现的 judge 误判均保留，复测结果没有覆盖它们。

本报告原始批次均为每个变体一个样本，顺序执行，没有置信区间、稳定性或长期收益结论。此对比不是 previous/current 的版本回归。

2026-10-05 已对同一三个中文任务各补两轮；连同原单轮，每侧现有三个样本。[后续报告](../2026-10-05-codex-benchmark-repeat/README.md)保留逐样本结果、可测试性 baseline 的一次 FAIL 和中断调用成本，不改写本报告原始单轮结果。

## 五份档案

每份档案分开记录 Quality Profile、Risk Profile 和 Behavior Contract，避免重复入口：

- [functional-testing](./profiles/functional-testing.md)
- [testability-analysis](./profiles/testability-analysis.md)
- [performance-testing](./profiles/performance-testing.md)
- [skill-evaluation](./profiles/skill-evaluation.md)
- [skill-change-verification](./profiles/skill-change-verification.md)

## 复核与复现

先看 [results.json](./results.json) 的 case 选择与状态，再沿 `report`、`grading`、`metadata` 路径查看原生证据。历史 FAIL、旧 Eval、Provider ERROR、修复后 PASS 分属不同目录，禁止只挑绿灯而隐藏失败。

- [缺陷分类与修复记录](./FINDINGS.md)：Skill/Eval/Infrastructure/Unknown 分开。
- [成本报告](./COST_REPORT.md)：main/judge 与未知费用分开。
- [复现说明](./reproduction/README.md)：固定参数、完整当前快照、可移植传输适配器及单元测试。
- [业务验收清单](./BUSINESS_ACCEPTANCE.md)：待提供真实项目后执行。
- [SQEM v1.1 改进提案](./SQEM_V1_1_PROPOSAL.md)：尚未发布的新规范建议。
- [artifact-manifest.json](./artifact-manifest.json)：原始与脱敏后 SHA256、路径替换次数。

`artifacts/` 是 runner 产物的**脱敏导出**，并非所有文件都与私有原始字节一致。保留真实 provider 错误与原生状态，只有本机路径被替换为符号。最早未完全隔离的 smoke 和 9 月 30 日旧运行不纳入本报告。复现包只用于证据复核，不是新增可安装 Skill 或默认 CI 模型调用。

2026-10-04 收尾复核修复了一份 trace 中遗漏的 macOS 临时父目录路径。两条离线回归分别检查该 trace 与整个证据包的本机路径/常见凭据模式；修复不改变原生结果或用量。原始 SHA256 保留，导出 SHA256 已更新；完整门禁和复核日志见 [verification.json](./verification.json)。

2026-10-16 交付前 review 修正了 CLI 版本声明及空格/中文路径复现问题。[原可移植适配器](./reproduction/snapshots/adapter-20261005.mjs)按原 SHA256 冻结；当前修正版对未来调用先探测 `--version`，失败时记录未知。新增四条离线回归已完成红绿验证，未执行新的模型 smoke；历史 portable-smoke 只适用于原版。原生结果、判分和用量不变，详见[复现说明](./reproduction/README.md)。

## 剩余验收项

工程核心文本验证与选定对比已有真实证据，但整个 Pilot 尚不能无条件关闭：自然选择证据、受阻安全用例、更广泛的困难输入采样、人工 Judge 校准、Claude 兼容、真实业务验收、成本是否可接受仍未确认。不得将本报告升级为业务或发布批准。
