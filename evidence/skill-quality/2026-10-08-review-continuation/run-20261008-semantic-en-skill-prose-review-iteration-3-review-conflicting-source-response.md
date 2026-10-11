# Review conclusion

Conclusion: **fail** — three concrete contract conflicts in `sample/`.

## Blocking findings

| Location | Finding and smallest correction | Impact | Evidence |
|---|---|---|---|
| [agents/openai.yaml:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | `metadata.key` is `invoice-editor`. Change it to `sample-review`. | Consumers using the canonical ID could reject package validation or fail lookup. | [SKILL.md:2](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) declares `sample-review`; [package-contract.md:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) requires exact equality. |
| [SKILL.md:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml), [prompts/review.md:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The root requires CSV; its referenced prompt requires Markdown. Change prompt line 3 to `Output CSV with invoice_id,total.` | The instructions cannot both govern the sole output format. Markdown output could break a consumer expecting CSV. | The two files explicitly require different formats. |
| [agents/openai.yaml:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The default prompt requests automatic invoice editing. Replace it with `Use sample-review to review invoices.` | The entry point could induce unauthorized changes to invoice totals or cause inconsistent refusal behavior. | [SKILL.md:8](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) and [prompts/review.md:4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) both prohibit editing invoices. |

## Important suggestions

The corrections above preserve the declared canonical ID and the root CSV requirement. No broader rewrite is needed to resolve these conflicts.

## Information gaps

- No precedence rule resolves the conflicting output formats.
- CSV handling for missing invoice IDs or totals is unspecified.

## Evidence boundary

- Verified: static prose comparison across all four files in `sample/`.
- Not verified: runtime behavior, consumer parsing, or Host validation and lookup failures.
- No invoice task was executed; no files were edited.
