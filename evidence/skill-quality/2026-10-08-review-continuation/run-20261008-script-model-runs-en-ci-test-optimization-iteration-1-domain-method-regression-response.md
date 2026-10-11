### 任务范围与证据边界

目标是对这个静态 fixture 比较流水线时间和质量保护；表中决策只代表 fixture 比较，不代表真实测试执行或发布批准。未执行 CI、调用外部服务或修改项目。

### 输入审计与领域分析

- **已知：** 同一 commit、test set、runner；给出了 queue、install、并行测试和 report 时长，并说明没有重试。来源是本轮提供的 sanitized fixture；证据仅为静态描述，没有运行记录。
- **缺失：** 实际 DAG 和日志、checkout/setup 耗时、runner 分配、缓存键与命中记录、历史 flaky 数据、各测试的分片归属、资源用量和回滚门槛。
- **冲突：** fixture 内未见冲突。**时效：** 未提供运行日期；这是静态 fixture，不是有时间窗口的实测记录。
- **假设：** 只计算列出的阶段，测试在 install 后并行开始，report 等待两个测试 job 完成；未列出的阶段不计入。实际 DAG 可通过检查 job 依赖和时间戳验证。

关键路径是 queue → install → 60 秒测试 job → report；40 秒 job 与其并行，不能把两个测试时长相加。已知测试工作量为 100 job-seconds，但 runner 分配及 install/report 占用情况未给出，因此总 runner 忙碌时间未知。没有重试说明此 fixture 不含重试耗时，不能据此判断历史 flaky 率。60 秒与 40 秒的时长差显示关键路径尾部，但缺少测试归属和资源数据，无法判断如何重分片。缓存键应覆盖 lockfile、toolchain 和配置；fixture 没有提供这些键的实际记录。

### Fixture 决策

| ID | DECISION | Evidence |
|---|---|---|
| CI-1 | ACCEPT | 来源：用户提供的 fixture 及 Skill 的静态决策 oracle。Oracle：有效缓存将 install 从 30 秒降至 10 秒，其余阶段和故障检测相同，保护未降低。证据状态：静态比较。优先级/责任角色：P2，CI 维护者。关闭条件：确认缓存键覆盖 lockfile、toolchain、配置，且测试清单与故障检测保持一致；不匹配时停用缓存。最小验证：同配置冷/热缓存运行，对照缓存键、阶段日志和测试清单；本次未运行。 |
| CI-2 | REJECT | 来源：用户提供的 fixture 及 Skill 的静态决策 oracle。Oracle：移除 money regression job 会漏掉该故障，质量保护下降。证据状态：静态比较。优先级/责任角色：P0，测试与业务质量负责人。关闭条件：恢复该 job，并证明故障能使流水线失败；在此之前不得将此方案视为绿色。最小验证：注入该回归，检查对应 job 与流水线结果；本次未运行。 |
| CI-3 | REJECT | 来源：用户提供的 fixture 及 Skill 的静态决策 oracle。Oracle：job 失败后使用 `|| true` 会掩盖失败并报告绿色。证据状态：静态比较。优先级/责任角色：P0，CI 维护者。关闭条件：失败状态能传递到流水线结果；若仍报告绿色则停止该方案。最小验证：让目标 job 失败，核对退出状态及最终报告；本次未运行。 |
| CI-4 | UNKNOWN | 来源：用户提供的 fixture 及 Skill 的静态决策 oracle。Oracle：lockfile 变化后复用旧缓存且没有验证；缺少缓存键、依赖解析和失效记录，无法确认实际影响。证据状态：静态材料不足。优先级/责任角色：P1，依赖与 CI 维护者。关闭条件：证明 lockfile 变化会使缓存失效，或运行依赖验证后确认结果一致；验证失败时停止复用旧缓存。最小验证：改变 lockfile，对比旧缓存路径与干净解析的缓存键和依赖结果；本次未运行。 |

### 指标与计算

| METRIC | VALUE | Unit/evidence |
|---|---:|---|
| baseline_seconds | 115 | 秒；queue 20 + install 30 + max(并行测试 60, 40) + report 5。关键路径为 queue → install → 60 秒 job → report。 |
| candidate_seconds | 95 | 秒；queue 20 + install 10 + max(并行测试 60, 40) + report 5。关键路径为 queue → install → 60 秒 job → report。 |

### 最小后续验证与剩余风险

最小后续检查是核对阶段依赖、缓存键及失效记录、job 退出状态、测试清单和故障检测；比较同配置的冷/热缓存运行，并查看各并行 job 的时长与资源归属。异常缓存或被掩盖的 job 失败应触发停止优化并交由流水线负责人处理。当前没有真实执行证据、flakiness 数据或 runner 资源证据；fixture 的 ACCEPT/REJECT/UNKNOWN 不构成发布决定。
