以下仅比较脱敏静态材料，未生成文件、执行测试或发起外部请求。**PASS/FAIL 只表示材料与契约的比较结果。**

1. **任务理解**

   范围仅为 `POST /orders`，依据用户提供的 API-v1：请求体 `{"qty":1}`、`Content-Type: application/json`、预期状态 `[201]`、预期 JSON `{"qty":1}`。A1–A3 的观测值用于比较，不能反向覆盖预期；A4 按其明确缺失独立判断，不能静默补齐。

   输出遵循 [主 Prompt](../../../skills/zh/testing-types/api-test-supertest/evals/cases/review-repair-regression.yaml)；目标配置、缺失数据及生成边界依据 [生成契约](../../../skills/zh/testing-types/api-test-supertest/evals/cases/review-repair-regression.yaml)。

2. **Supertest 方案或结构**

   建议结构为 `tests/orders.test.js`、`jest.config.cjs`，执行配置采用 `jest --runInBand`；没有提供现有 Node 测试资产，暂无法确认兼容配置。

   脚手架方案明确采用 **baseUrl 模式**：`request(process.env.API_BASE_URL)`。这是因未提供 app 导出而采用的方案假设，实际地址仍缺失，不设置默认目标。若改为进程内模式，须显式配置绝对路径 `SUPERTEST_APP`。

   请求必须保留原始内容：`.send({qty:1})`，保留数值类型与字段，不包裹、不增删、不替换为 sample body。响应使用完整 JSON 相等断言，例如 `toStrictEqual({qty:1})`。材料没有原始字节串，不能声称字节级一致。

   未提供鉴权要求，不添加 Authorization。确认需要后，才通过 `headers_env` 映射完整头值。Bruno 地址必须使用 **`{{baseUrl}}/orders`**，并显式配置环境变量 `baseUrl`。

3. **高优先级覆盖**

   建议文件 `tests/orders.test.js`，正向标题为 `POST /orders returns 201 with exact JSON {qty:1}`。建议列为 P0，因为状态和响应内容是当前唯一明确的契约。

   A1 覆盖正向一致；A2 覆盖状态不一致；A3 覆盖响应内容不一致。A2/A3 是观测偏差，不能改写成允许 404 或 `qty:2` 的服务端负向契约。A4/A5 覆盖生成输入缺失与空集合边界。其他业务异常、数量边界没有依据，暂不补造。

4. **环境和数据说明**

   本地与 CI 的目标地址、依赖版本、数据隔离及订单清理方式均未提供。未来执行 POST 前需确认这些条件，不编造清理接口。`--runInBand` 可降低并发数据干扰，但不能代替数据隔离。

   没有来源化 `max_response_ms`，因此不增加固定 3 秒等延迟门槛。

5. **最小验证与执行边界**

   本轮最小验证是静态核对：A1–A3 分别比较状态和完整 JSON；A4 核对必要请求体、明确预期状态是否齐备；A5 核对端点集合是否非空。

   后续生成验证应确认 A4/A5 产生明确失败工件并非零退出，不能形成空套件绿色结果。数据补齐、目标显式配置后，才具备执行 `npx jest tests/orders.test.js --runInBand` 的前提；本轮未运行该命令。**生成脚手架、实际运行、业务验收是不同证据层级。**

6. **信息缺口**

   A4 缺必要请求体与预期状态；A5 缺整个端点范围。真实执行还缺目标地址或 app 导出、鉴权要求、环境配置及数据生命周期说明。现有材料不支持判断根因、实际延迟或真实服务是否通过。

| ID | DECISION | Evidence |
|---|---|---|
| A1 | PASS | 用户材料：观测状态 201 属于预期 `[201]`；观测 `{"qty":1}` 与预期 JSON 相等。 |
| A2 | FAIL | 用户材料：观测状态 404 不属于预期 `[201]`；响应 JSON 相等不能抵消状态偏差。 |
| A3 | FAIL | 用户材料：状态 201 符合预期；观测 `{"qty":2}` 与预期 `{"qty":1}` 不相等。 |
| A4 | INCOMPLETE | 已有端点缺明确预期状态及必要请求体；属于输入不完整，不表示真实请求失败。 |
| A5 | BLOCKED | `endpoints` 为空，没有可生成的端点范围；不表示真实请求执行结果。 |
