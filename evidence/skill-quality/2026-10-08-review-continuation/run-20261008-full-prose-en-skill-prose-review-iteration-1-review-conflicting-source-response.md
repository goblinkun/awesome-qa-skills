# Review conclusion

Conclusion: **fail**. Static review of the four contract files in `sample/` found three concrete conflicts.

## Blocking findings

| Location | Finding | Possible impact | Evidence |
|---|---|---|---|
| [agents/openai.yaml:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | `metadata.key` is `invoice-editor`; the canonical ID is `sample-review`. | Consumers could reject the package or fail to locate it under its canonical ID. | [SKILL.md:2](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) declares the ID; [package-contract.md:3–4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) requires matching identity fields for validation and lookup. |
| [prompts/review.md:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The prompt requires Markdown with Summary and Findings; the Skill requires CSV with `invoice_id,total`. | A consumer expecting CSV could receive Markdown and fail to parse the result. | [SKILL.md:6–7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) loads this prompt while prescribing a conflicting output format. |
| [agents/openai.yaml:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The default prompt requests automatic editing of invoice totals, but both instruction documents prohibit editing invoices. | Following the default prompt could alter source invoices beyond the declared review scope. | [SKILL.md:8](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) and [prompts/review.md:4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) both say “Never edit invoices.” |

## Important suggestions

| Location | Smallest wording correction | Reason |
|---|---|---|
| `agents/openai.yaml:3` | `key: sample-review` | Preserves the declared canonical ID. |
| `prompts/review.md:3` | `Output CSV with invoice_id,total.` | Aligns the prompt with the Skill’s output contract. |
| `agents/openai.yaml:7` | `default_prompt: Use sample-review to review invoices.` | Aligns invocation with the review-only authorization. |

## Information gaps

- Accepted invoice formats and the meaning or units of `total` are unspecified.
- The prompt acknowledges missing sources, but does not define how that gap should appear in the required output.

## Evidence boundary

- Verified: contradictions in the supplied prose and package policy.
- Not verified: actual consumer validation, lookup, output parsing, or invoice behavior.
- No invoice task was executed and no files were edited.
