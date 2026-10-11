静态结论：**A1 PASS；A2、A3 FAIL；A4 INCOMPLETE；A5 BLOCKED。** PASS/FAIL 仅表示所给材料与契约的比较，不代表真实测试执行。本轮未生成文件、发送请求或运行测试。

**1. 任务理解**

唯一已确认接口为 API-v1：`POST /orders`，请求头 `Content-Type: application/json`，请求体 `{"qty":1}`；预期状态为 `[201]`，预期 JSON 为 `{"qty":1}`。

事实来源是用户提供的契约、A1–A5 和决策定义；组织方式依据 [主 Prompt](../../../skills/zh/testing-types/api-test-pytest/prompts/api-test-pytest.md)，生成边界依据 [生成契约](../../../skills/zh/testing-types/api-test-pytest/references/generator-contract.md)。A4 明确缺失的数据不能静默回填为已确认输入。

**2. Pytest 方案或结构**

以下只是建议骨架：

- `tests/conftest.py`：`base_url`（session，从显式配置的 `BASE_URL` 读取）、`api_client`（session，使用 `requests.Session`）。
- `tests/test_orders.py`：`test_create_order_contract`，建议使用 `smoke`、`contract` marker。
- `tests/test_contract_input.py`：检查缺少必要数据和空端点集合。

未提供现有套件，因此无法确认已有目录、fixture 或 marker 约定。

**3. 高优先级覆盖**

优先级为本次建议，并非材料确认的业务等级。

- **P0：契约一致性。** A1–A3 分别核对状态码和 JSON；A2 的状态不符，A3 的响应值不符。不能因为其中一项相符就判 PASS。
- **P1：输入完整性。** A4 已有端点但缺必要请求体和预期状态，判 INCOMPLETE；A5 端点集合为空，判 BLOCKED。二者均不能显示为绿色通过。
- 异常与边界方面，目前仅能分析上述差异和输入缺口；没有依据新增 `qty=0`、401、错误体字段等场景。

**4. fixture 和数据说明**

请求必须保留 `POST /orders`、给定 Content-Type，以及 JSON 对象 `{"qty":1}`：`1` 保持数值类型，不改为字符串，不补字段、不增加包装层，也不根据 A3 的响应改写请求。材料没有原始 HTTP 字节，因此只能确认所给内容与 JSON 类型，不能声称字节级复现。

鉴权方式未提供，不能添加 Bearer、登录流程或通用 token。数据隔离、重复创建和清理方式也未提供，不能虚构清理接口。没有来源化时延要求，不能添加固定 3 秒阈值。

**5. 最小验证与执行建议**

本轮最小验证仅为静态复核：

- A1–A3：检查观察状态是否属于 `[201]`，并比较观察 JSON 与 `{"qty":1}`。
- A4：从明确来源补齐必要请求体与 `expected_statuses`，记录来源后重新校验。
- A5：先提供非空端点集合，再检查各端点完整性。

后续真实执行时，才使用如 `pytest -m smoke` 或 `pytest tests/test_orders.py`；CI 应先校验输入和目标配置，再执行相应范围。生成骨架成功与实际测试通过必须分别报告。

若迁移到其他工具，Bruno 地址必须使用 **`{{baseUrl}}/orders`** 并配置 `baseUrl`；Supertest 必须明确选择远程 URL 模式（`API_BASE_URL`）或本地应用模式（`SUPERTEST_APP` 显式绝对路径），不能自动猜测目标。[配置依据](../../../skills/zh/testing-types/api-test-pytest/references/generator-contract.md)

**6. 信息缺口与假设**

真实目标、鉴权要求、依赖版本、业务边界、数据清理规则、时延契约及实际运行证据均未提供。这些缺口限制后续执行与验收，但不改变本轮静态判断；A4、A5 按用户明确给定的决策契约分类。

| ID | DECISION | Evidence |
|---|---|---|
| A1 | PASS | 用户材料：观察状态 201 属于 `[201]`，观察 JSON `{"qty":1}` 与预期相符。 |
| A2 | FAIL | 用户材料：观察状态 404 不属于 `[201]`；JSON 相符不能抵消状态差异。 |
| A3 | FAIL | 用户材料：观察状态 201 相符，但观察 JSON 为 `{"qty":2}`，预期为 `{"qty":1}`。 |
| A4 | INCOMPLETE | 用户材料：已有端点缺少 `expected_statuses` 和必要请求体；属于输入不完整，无执行结论。 |
| A5 | BLOCKED | 用户材料：端点集合为空，没有可生成的范围；无执行结论。 |
