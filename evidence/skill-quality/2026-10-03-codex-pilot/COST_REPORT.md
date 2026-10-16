<div align="right"><strong>🇨🇳 中文</strong> | <a href="./COST_REPORT_EN.md">🇬🇧 English</a></div>

# Pilot 成本报告

用于复核本次运行的工程开销，**不作为账单或成本可接受的审批**。逐调用数据见 [cost-ledger.json](./cost-ledger.json)。

| 统计范围 | Codex 调用 | 已观测 input tokens | 已观测 output tokens | usage 未知 |
| --- | ---: | ---: | ---: | ---: |
| 选定当前核心组 | 34 | 1,774,125 | 56,687 | 0 |
| 选定第二模型采样 | 5 | 373,842 | 11,321 | 0 |
| 所有归档 judge 调用 | 14 | 262,200 | 11,246 | 0 |
| 所有归档原生调用（包含上述各组） | 85 | 4,113,159 | 139,377 | 1 |

最后一行包含修复前后复测、Benchmark、校准 judge、一次可移植配置 smoke 和一次被拦截请求，不是 85 个独立验收用例；各行不能相加。未完全隔离的最初 smoke、9 月 30 日旧运行及合成校准主体不纳入调用账本。

`input_tokens` 来自 Codex CLI 完成事件，已经包含 cached input；账本另列其已观测缓存子集，**不重复加总**。工具交互可能增加输入量，因此不是提示词字数。被服务端拦截的调用没有 usage，计为 `unknown`，不能把原生报告的 0 当成实际免费。

## 选定 Benchmark 的主体成本

| Skill | 变体 | 主体秒数 | 主体 input + output tokens |
| --- | --- | ---: | ---: |
| functional-testing | with / without | 177.407 / 202.515 | 55,484 / 69,496 |
| testability-analysis | with / without | 157.598 / 123.741 | 55,829 / 85,010 |
| skill-evaluation | with / without | 93.166 / 94.581 | 54,307 / 67,095 |

表格不含 judge 耗时和 usage；后者见逐调用账本。skill-evaluation baseline 的前置检查失败，没有执行 semantic judge，因此其总流水线成本不能直接和另一边比较。每边一次，运行次序和负载可能影响耗时，不推断稳定节省。

## 未测量成本

- 实际美元费用 / 账户账单：`unknown`，未用列表价格推算用户实际付款。
- Eval 编写、维护、失败排查人工时间：`unknown`，没有可靠计时。
- CI 模型执行成本：`NOT_RUN`，没有为 CI 加入自动付费调用。
- 可接受预算 / 长期维护成本：`UNASSESSED`，需要责任人定义上限和重复样本。

建议下一轮先固定有限预算和停止条件，用代表性核心组以及少量困难 Benchmark 做重复采样；修复断言时先重新判分已捕获输出，确认是 Eval Defect 后再进行必要真实复测。该建议不授权自动消耗额度重置或购买费用。
