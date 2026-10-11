# 审查结论

结论：**不通过**。`sample/` 的四个文件存在三处直接契约冲突。

## 阻塞问题

| 位置 | 问题与证据 | 可能影响 | 最小文字修订建议 |
|---|---|---|---|
| [sample/agents/openai.yaml:3](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | `metadata.key` 为 `invoice-editor`，但 [SKILL.md:2](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) 声明 `sample-review`；[包契约:3](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) 明确要求二者一致。 | 按 canonical ID 校验或查找的消费者可能拒绝该包或无法定位 Skill。 | 改为 `key: sample-review`，保留已声明的 canonical ID。 |
| [sample/prompts/review.md:3](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | 要求输出包含 Summary、Findings 的 Markdown；[SKILL.md:7](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) 要求 CSV，字段为 `invoice_id,total`。 | 输出格式不确定，期待 CSV 的消费者可能无法解析结果。 | 建议沿用入口声明，将该行改为 `Output CSV with invoice_id,total.` |
| [sample/agents/openai.yaml:7](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | 默认提示要求自动修改发票金额；[SKILL.md:8](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) 和 [review.md:4](../../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) 均明确禁止编辑发票。 | 可能诱导 Agent 超出审阅权限，修改本应只读的发票。 | 改为 `default_prompt: Use sample-review to review invoices without editing them.` |

## 重要建议

无额外建议；本次只报告实际契约冲突。

## 信息缺口

未提供消费者、Host 的实现或运行记录，无法确认上述风险是否已造成实际故障。

## 证据边界

已静态核对 `sample/` 全部四个文件；未验证加载、查找或输出解析行为。未执行发票任务，未编辑文件。
