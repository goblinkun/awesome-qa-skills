主推荐：`regression-test-selection`。目标是在受影响义务已确认的前提下，根据覆盖关系和测试成本选择最小回归集。阶段为 Engineering QA / 回归规划；辅助 skill：无。

推荐理由与来源：

- 请求需要单一的回归选择产物，适用专项技能。
- 影响分析已完成，依据[主 Prompt 的专项优先规则](../../../skills/zh/testing-workflows/discover-testing/prompts/discover-testing.md)，直接选择回归测试选择技能；[通用路线参考](../../../skills/zh/testing-workflows/discover-testing/reference.md)中的影响分析阶段无需重复。
- [能力清单](../../../skills/zh/testing-workflows/discover-testing/references/skill-capability-inventory.json)确认精确 canonical ID；用户材料明确目标已安装。没有 plus 或特定工具链需求。

信息缺口与交接：需提供义务 ID、测试与义务的覆盖矩阵、各测试成本、必选项及约束，并明确“最小”指测试数量还是总成本。目标产出应包含入选集、覆盖证据、成本合计和排除理由。目前材料足以路由，尚不足以确定实际集合。

最小验证：仅静态核对必需义务全部覆盖、必选项保留、成本汇总正确；对小规模候选枚举可行子集，比较数量或总成本以验证最优性。未完成最优性比较时，只能称为候选精简集。以上是交接建议，未调用目标或执行真实测试。

| ID | DECISION | Evidence |
| --- | --- | --- |
| ROUTE | regression-test-selection | AVAILABLE（依据用户声明）：材料明确“Target is installed”；能力清单确认精确 ID。清单自身标记 UNKNOWN，未独立验证 Host 可调用性。 |
