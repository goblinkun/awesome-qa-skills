A1 为 PASS，A2/A3 为 FAIL；A4 为 INCOMPLETE，A5 为 BLOCKED。以下仅比较静态材料，未生成文件、运行测试或发送请求；PASS/FAIL 不代表真实测试执行结果。

1. 任务理解与来源

   范围为 `POST /orders`。API-v1 提供请求与预期，A1–A5 提供比较材料；观测差异不能反过来修改预期。输出遵循本地[主 Prompt](../../../skills/zh/testing-types/api-test-bruno/prompts/api-test-bruno.md)与[生成契约](../../../skills/zh/testing-types/api-test-bruno/references/generator-contract.md)。

2. Bruno 结构方案

   建议结构如下，仅为脚手架方案：

   ```text
   order-api/
     bruno.json
     environments/
       local.bru
       staging.bru
     orders/
       create-order.bru
   ```

   请求 URL 必须使用 `{{baseUrl}}/orders`；环境名是模板约定，真实地址尚未提供。鉴权未知，不能据此认定无需鉴权，也不能擅自添加 `Authorization`、token 或登录接口。

3. 高优先级请求覆盖

   将唯一已确认请求暂列 P0：`meta.name=create-order`，归入 `orders`，重点检查创建响应的状态及数据是否符合契约；此优先级是本轮建议。

   必须保留 `POST /orders`、`Content-Type: application/json`、请求 JSON `{"qty":1}`，保持字段、值和数字类型，不改成字符串、不添加示例字段。材料未提供原始报文字节，无法核对字节级保真。

   断言依据为状态属于 `[201]`，响应完整 JSON 与 `{"qty":1}` 深比较一致。A2 的 `404` 不是已声明的合法负向预期；A3 的 `qty:2` 不能替换契约值。其他错误路径与边界预期缺少来源，暂不生成。

4. 执行备注与最小验证

   本轮最小验证是静态检查：端点集合非空、必需请求体存在、预期状态明确，再逐项比较状态与 JSON。A4 已明确缺失的字段不能用默认值掩盖；A5 没有端点，无法生成请求范围。

   将来真实执行的最小范围是这一个请求，并核对实际发出的请求、响应、状态断言和 JSON 断言。鉴权、前置请求及清理流程均未明确，不能编造。冒烟范围仅包含该请求；回归扩展需要新增来源化契约。当前材料不足以作发布判断。

5. 自动化和 CI 建议

   后续流程可为：安装约定版本的 Bruno CLI → 配置 `baseUrl`及已确认的鉴权 → 运行该请求 → 检查报告。真实通过需有响应、断言实际执行且通过、无跳过，退出码 `0` 本身不足。

   材料没有性能要求，不添加固定三秒或其他延迟阈值。若生成 Supertest，必须显式选择目标模式：HTTP 地址模式配置 `API_BASE_URL`；应用模式配置绝对路径 `SUPERTEST_APP`，不能默认猜测目标。

   生成脚手架、生成成功、真实运行通过是不同结论；本轮只提供静态分析。

6. 信息缺口与假设

   缺少真实目标地址、鉴权要求、原始请求/响应、执行报告、数据隔离与清理规则，以及其他负向和边界契约。A4 另缺明确预期状态及必需请求体；A5 缺整个端点集合。

   本轮按题设用 API-v1 比较 A1–A3，但无法据观测摘要证明实际请求曾保留指定 payload、header，或确实执行过测试。

| ID | DECISION | Evidence |
|---|---|---|
| A1 | PASS | API-v1 预期 `[201]`、`{"qty":1}`；A1 记录 `201`、`{"qty":1}`，两项静态一致。 |
| A2 | FAIL | API-v1 预期 `[201]`；A2 记录 `404`，状态不符；JSON 一致不抵消状态差异。 |
| A3 | FAIL | 状态 `201` 符合；API-v1 预期 `qty:1`，A3 记录 `qty:2`，JSON 不符。 |
| A4 | INCOMPLETE | 已有端点缺明确预期状态及必需请求体，属于请求或预期信息不完整。 |
| A5 | BLOCKED | 端点集合为空，没有可生成的范围；不表示真实请求失败。 |
