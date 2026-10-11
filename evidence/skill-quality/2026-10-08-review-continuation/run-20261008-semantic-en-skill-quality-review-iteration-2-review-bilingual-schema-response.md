The paired output contract has a **blocking bilingual inconsistency**, although each entry agrees with its own prompt.

| Language | Entry | Prompt | Output fields |
|---|---|---|---|
| EN | [SKILL.md:6](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) | [review.md:1](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) | `invoice_id, pass_count` |
| ZH | [SKILL.md:6](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) | [review.md:1](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) | `invoice_id, total` |

The shared field is `invoice_id`. The differing fields represent distinct quantities: [`output-contract.md:2–3`](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) defines `total` as the invoice amount **in cents**, and `pass_count` as the number of passed validation checks **in checks**. They are not equivalent translations or interchangeable values. Consumers therefore receive different information depending on the language selected.

The [contract explicitly assigns schema selection to the owner](../../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml), and that decision is not supplied. Neither language can be treated as authoritative. Once the owner specifies the schema, all four declarations should conform to it.

This was a read-only static review of the entries and prompts using the supplied contract. Both prompt references resolve, and both prompts preserve `never edit`. Runtime behavior is `NOT_RUN`; no files were changed.
