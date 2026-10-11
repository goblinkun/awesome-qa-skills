[运行记录](../../../skills/zh/skill-engineering/skill-evaluation/evals/cases/review-incomparable-runs.yaml) 中，current 已是 `model=model-other`、`input_hash=cases-B`，无需修改。JSON 和计数检查通过。

**数值观察**

| 运行 | Skill 版本 | 模型 | 输入集 | 汇总通过率 |
|---|---|---|---|---|
| `run-prev` | v1 | model-fixture | cases-A | 8/10，80% |
| `run-current` | v2 | model-other | cases-B | 6/10，60% |

通过数减少 2，通过率下降 **20 个百分点**，相对下降 25%。这些是文件中的汇总差异；不能称为“同两例发生退化”，因为输入集不同。

两次记录的 `eval_version=e1`、`skill_up=0.12.0`、`engine=codex`、`temperature=0`、`seed=7`、`judge=rubric-A`、`environment=sandbox-A` 相同；时间分别为 10 月 1 日、2 日 09:00 UTC。配置标签相同尚不能证明实际内容和环境完全相同，provider 为 `unknown`。

**版本退化结论：`INSUFFICIENT_EVIDENCE`。** Skill 版本、模型、输入集同时变化，无法将下降归因于 v2，也无法排除模型、用例难度或交互影响。

| 证据项 | 状态与限制 |
|---|---|
| 逐用例、输出工件、语义判定 | `UNASSESSED`：未评估；缺少断言、逐例结果及 judge 依据 |
| 触发与过程 | `BLOCKED`：缺少 `skill.selection` 和 trace，无法判断触发情况 |
| with/without Skill 基准 | `NOT_RUN`：没有此类比较 |
| 偶发性、基础设施问题 | `UNASSESSED`；失败根因为 `UNKNOWN`，不能定为 Skill Defect |
| Quality Score | `NOT_SCORED`：未评分 |

`PASS`/`FAIL` 应对应具体用例的断言判定；现有汇总计数不足以核验逐例判定。

**最小受控重跑：两次运行，每次执行同一组 10 例。**

1. 补齐 v1、v2 的准确 Skill 快照，以及 cases-A 原始用例、e1 和 rubric-A 配置。验证目标配置；语义 judge 如未经校准，先校准。
2. 在同一冻结环境下，用 **model-fixture + cases-A** 分别运行 v1、v2。固定其余上述条件、provider、调用方式和工具权限；唯一实验变量为 Skill 版本。通过 `skill-up validate` 后执行 `skill-up run`。
3. 保存真实内容哈希、实际模型身份、逐例结果、输出、trace 和 judge 依据；按 `case_id` 配对检查 **v1 PASS → v2 FAIL**，再排查 Eval/Infrastructure 问题。若存在波动，再对相关用例重复配对。

该重跑目前为 `NOT_RUN`：当前目录缺少被测 Skill 两版、原始用例和 judge 配置。一次受控配对可支持这组固定条件下的观察；广泛或稳定的版本退化仍需重复证据。
