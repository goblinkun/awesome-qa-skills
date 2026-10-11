主推荐：`rag-retrieval-testing`，用于 AI Native QA 的检索评估。可选辅助：无。

推荐理由：

- query→document 相关性标签用于判断检索结果是否相关。
- top-k recall 证据直接对应检索召回评估。
- 未提供回答文本，无法判断回答正确性或忠实度。
- 目标是单一专项产出，按主 Prompt 优先选择检索专项，无需套用通用 AI 功能路线。

来源：[主 Prompt](../../../skills/zh/testing-workflows/discover-testing/prompts/discover-testing.md)规定专项优先；[能力清单](../../../skills/zh/testing-workflows/discover-testing/references/skill-capability-inventory.json)确认精确 canonical ID。

信息缺口：材料未列出具体标签、排序列表、k 值、召回数值、标注口径及验收阈值；目标安装状态未知，availability=`UNKNOWN`。

下一步与最小验证：将上述静态证据交接给目标 skill。建议核对一个 query 的标签与 top-k 文档 ID，按 `Recall@k = top-k 中相关文档数 / 全部标注相关文档数` 复核所给证据；分母为零时记为未定义。当前仅完成路由，未执行评测、安装或外部操作。

| ID | DECISION | Evidence |
|---|---|---|
| ROUTE | rag-retrieval-testing | 目录快照包含该精确 ID；`installation_evidence=UNKNOWN`，该项 `availability=UNKNOWN`；未提供当前 Host 安装或可调用证据。 |
