**主推荐：`authorization-testing`（授权测试）**。属于 Core QA，目标是判断 userA 更改 `objectID` 后读取 userB 记录是否符合对象级授权规则。辅助 skill：无。

推荐理由：

- 登录已有效，主要问题是访问权限。
- 跨用户替换对象 ID 涉及水平越权风险，但当前材料不能证明存在漏洞。
- 授权专项匹配明确，无需套用通用 API Composition 路线；未指定工具链，也无需 plus。

来源：[主 Prompt](../../../skills/zh/testing-workflows/discover-testing/prompts/discover-testing.md)要求优先匹配认证／授权专项；[能力清单](../../../skills/zh/testing-workflows/discover-testing/references/skill-capability-inventory.json)确认 canonical ID 为 `authorization-testing`。

**可用性缺口：`UNAVAILABLE`**。用户明确目标未安装；清单中的 `UNKNOWN` 仅表示目录快照缺少安装证据。后续交接前需安装该 skill 并确认 Host 可调用，本次不执行安装或调用。

**信息缺口与最小验证：**缺少对象归属、共享权限规则，以及脱敏请求／响应。最少补充同一 userA 会话访问自身记录和 userB 记录的材料，仅改变 `objectID`，对照权限规则比较状态码与响应内容。若规则禁止读取 B 的记录，应检查是否拒绝访问且未泄露 B 的数据。交接目标是形成授权检查项与证据缺口；本次没有真实测试结果。

| ID | DECISION | Evidence |
|---|---|---|
| ROUTE | authorization-testing | 用户明确目标未安装，因此 availability=UNAVAILABLE；能力清单确认 canonical ID，但快照中的 UNKNOWN 不证明 Host 已安装或可调用。 |
