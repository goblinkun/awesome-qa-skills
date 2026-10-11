Conclusion: **fail** — two direct contract conflicts.

| Location | Conflict and impact | Smallest wording correction |
|---|---|---|
| [sample/SKILL.md:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml), [sample/prompts/review.md:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The entry point requires CSV with `invoice_id,total`; the referenced prompt requires Markdown with Summary and Findings. A response cannot satisfy both output contracts. | Make the requirements identical. If CSV is intended, replace prompt line 3 with `Output CSV with invoice_id,total.` |
| [sample/agents/openai.yaml:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml), [sample/SKILL.md:8](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml), [sample/prompts/review.md:4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The default prompt requests automatic editing of invoice totals; both instruction files prohibit editing invoices. The default request directly violates the skill’s constraint. | Replace the default prompt with `Use sample-review to review supplied invoices without editing them.` |

An additional naming inconsistency appears at [sample/agents/openai.yaml:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml): `invoice-editor` suggests an editing role. Consider `invoice-review` if this key is descriptive; its runtime significance is unverified.

Information gaps: the intended output format is unresolved, and the contract does not explain how to report the “missing source” gap from prompt line 2 within the prescribed CSV columns.

Evidence is limited to static reading of all three files in `sample/`. No invoice task, runtime validation, or file edits were performed.
