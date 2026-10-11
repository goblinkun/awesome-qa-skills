# Review conclusion

**Conclusion: fail.** Static review of the four files in `sample/` found three concrete contract conflicts.

## Blocking findings

| Location | Finding | Impact | Evidence |
|---|---|---|---|
| [SKILL.md:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | Requires CSV, while the loaded prompt requires Markdown. | The required response format is unresolved; neither document specifies precedence. | [prompts/review.md:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) requires Summary and Findings in Markdown. |
| [agents/openai.yaml:7](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | The default prompt requests automatic editing of invoice totals. | The invocation instructs an action explicitly prohibited by the Skill and review prompt. | “Never edit invoices” appears at [SKILL.md:8](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) and [prompts/review.md:4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml). |
| [agents/openai.yaml:3](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) | `metadata.key` is `invoice-editor`, but the canonical ID is `sample-review`. | Violates the package’s documented identity requirement. This does not establish observed Host failure. | [SKILL.md:2](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) defines the name; [package-contract.md:2–4](../../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) requires matching identity fields. |

## Important suggestions

These are the smallest wording corrections:

| Location | Suggestion | Reason |
|---|---|---|
| `sample/prompts/review.md:3` | Replace with `Output CSV with invoice_id,total.` | Aligns the loaded prompt with the Skill’s output contract. |
| `sample/agents/openai.yaml:7` | Replace with `default_prompt: Use sample-review to review invoice totals.` | Removes the prohibited editing instruction. |
| `sample/agents/openai.yaml:3` | Replace with `key: sample-review` | Matches the explicitly defined canonical ID. |

## Information gaps

- Accepted invoice input formats and whether `total` means the supplied or verified amount are unspecified. These are gaps, not demonstrated conflicts.

## Evidence boundary

- **Verified:** prose and metadata in all four files; conflicts traced to explicit lines.
- **Not verified:** invoice execution, runtime behavior, package validation, or Host behavior. No files were edited.
