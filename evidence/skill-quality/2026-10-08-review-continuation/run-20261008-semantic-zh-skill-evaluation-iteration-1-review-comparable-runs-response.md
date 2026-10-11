记录显示，previous → current 的通过率从 **80% 降至 60%，下降 20 个百分点，净少通过 2 个**。这是版本回归信号；发布结论为 `INSUFFICIENT_EVIDENCE`。

**范围**

依据 [artifacts/runs.json](../../../skills/zh/skill-engineering/skill-evaluation/evals/cases/review-comparable-runs.yaml) 解读已有记录。本次仅解析 JSON、核对配置及计算通过率，未运行引擎：`NOT_RUN`。

**运行元数据**

| 项目 | previous | current |
|---|---|---|
| run_id | `run-prev` | `run-current` |
| Skill 版本 | `v1` | `v2` |
| 时间（UTC） | 2026-10-01 09:00 | 2026-10-02 09:00 |
| 通过数 / 总数 | 8 / 10 | 6 / 10 |
| 通过率 | 80% | 60% |

两次记录共同配置：评测版本 `e1`、`skill-up 0.12.0`、引擎 `codex`、模型 `model-fixture`、`temperature=0`、`seed=7`、输入标识 `cases-A`、judge `rubric-A`、环境 `sandbox-A`。provider 为 `unknown`。

**配置与覆盖范围**

这些字段及总数一致，提供了**记录层面的可比依据**。但未提供 Skill/用例快照、实际输入、judge 内容或运行日志，无法独立验证配置及输入实际一致。目标行为、用例类型和覆盖范围均为 `unknown`。

**摘要**

比较类型为 **Version Regression（previous/current 版本回归）**。通过率变化的算术事实成立；该汇总记录尚不足以支持“v2 普遍退化”或将变化归因于 Skill 修改。

**用例结果**

缺少逐例 ID、断言、输出及判定依据，逐例复核为 `UNASSESSED`。净少通过 2 个，不代表已确认具体有 2 个用例从 `PASS` 变为 `FAIL`；新增失败、恢复通过及其他状态的分布为 `unknown`。

**触发 / 过程 / 结果 / 工件 / 语义证据**

| 维度 | 证据状态与解释 |
|---|---|
| 触发 | `BLOCKED`：缺少 observed `skill.selection`，无法判断是否触发 |
| 过程、工件、语义 | `UNASSESSED`：未提供 trace、输出工件或语义判定明细 |
| 结果 | 仅支持记录中的 8/10 → 6/10；未复核原始执行 |
| Quality Score | `NOT_SCORED`：通过率不自动转为质量评分 |

**Benchmark 结果**

with/without Skill 的 Benchmark 为 `NOT_RUN`；本文件不能证明启用 Skill 带来的收益。

**回归发现**

在记录配置一致的条件下，观察到通过率下降。可报告为**待核实的版本回归信号**；失败原因分类保持 `UNKNOWN`，尚不能区分 Skill Defect、Eval Defect 或 Infrastructure Defect。

**波动 / 阻塞 / 基础设施错误**

每个版本仅有一条汇总记录，稳定性为 `UNASSESSED`。缺少错误日志，基础设施是否影响结果为 `unknown`；固定 seed 和 temperature 不能替代重复运行证据。

**评测有效性**

`UNASSESSED`：没有用例定义、可观察断言、judge 实现或 rubric。judge 类型为 `unknown`；若使用语义 judge，还缺少校准证据。

**限制**

每次仅 10 个用例，缺少配对结果和重复运行。无法据此判断统计显著性、覆盖充分性或因果关系。

**推荐行动与发布结论**

当前发布判定为 **`INSUFFICIENT_EVIDENCE`，无法作出发布通过结论**。仍缺：

- 逐例输出、断言、判定理由及原始 trace，用于定位并确认回归。
- Skill、用例、judge 与运行配置的可核验快照，用于确认实际可比性。
- 重复运行及失败复核证据，用于判断稳定性和根因。
- 发布门槛、关键场景与风险覆盖要求，以及相应验收证据。

状态含义：`PASS`＝断言通过；`FAIL`＝断言失败；`BLOCKED`＝必要前提或证据不可得；`NOT_RUN`＝未执行；`NOT_SCORED`＝未评分；`UNASSESSED`＝未评估；`INSUFFICIENT_EVIDENCE`＝证据不足以支持结论。
