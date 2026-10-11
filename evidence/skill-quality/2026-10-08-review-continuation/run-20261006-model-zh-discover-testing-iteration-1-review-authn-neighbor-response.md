**主推荐：`authentication-testing`**，用于检查错误密码、过期 token 和登录会话创建。属于 Core QA 专项测试；未命中 Composition 路线。辅助 skill：无。

推荐理由：

- 错误密码涉及凭证校验，过期 token 涉及认证有效性，登录会话创建涉及认证成功后的状态建立。
- 用户明确排除跨用户读取记录的问题，因此无需路由到授权测试。
- 请求目标明确，优先匹配认证专项；没有工作流、plus 或指定工具链要求。

来源：[主 Prompt](../../../skills/zh/testing-workflows/discover-testing/prompts/discover-testing.md)要求专项优先；[能力清单](../../../skills/zh/testing-workflows/discover-testing/references/skill-capability-inventory.json)确认准确 ID 为 `authentication-testing`。

**信息缺口与下一步：**交接时提供认证协议、token 到期及容差规则、会话创建契约，以及三类场景的脱敏响应或日志。期望产出为认证检查结果及对应证据。

**最小验证：**仅将三类静态记录与已确认契约逐项比较，核对错误密码处理、到期 token 处理和成功登录后的会话状态。当前没有实际记录，无法判断行为是否符合预期。本次未执行外部操作、调用目标 skill 或运行测试。

| ID | DECISION | Evidence |
|---|---|---|
| ROUTE | authentication-testing | 用户明确说明目标已安装，按材料记为 AVAILABLE；清单确认 canonical ID。清单快照的 availability 为 UNKNOWN，本次未独立验证 Host 可调用性。 |
