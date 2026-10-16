无法报告“评测已通过”：目前没有可核验的运行结果，不能标记为 `PASS`。

| 报告项 | 状态 | 含义 |
|---|---|---|
| 评测执行 | `NOT_RUN` | 本次未运行评测 |
| 通过结论 | `INSUFFICIENT_EVIDENCE` | 缺少 Skill、用例、模型、目标和运行 trace |
| 触发验证 | `BLOCKED` | 缺少 `skill.selection` 证据 |
| Benchmark / Regression | `UNASSESSED` | 未评估 |

运行元数据：`unknown`。需提供可核验的评测工件后，才能判断是否通过。
