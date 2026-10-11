No files were edited. The only proposed change in [contract.md](../../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) is:

| Line | Before | Proposed after | Reason |
|---|---|---|---|
| 3 | This PR fixed the reviewer concern and now we should keep it. | Delete; no replacement. | Review dialogue tied to an unidentified PR and reviewer, with no independently verifiable fact to retain. |

Preserve these lines verbatim:

| Line | Original content | Why preserved |
|---|---|---|
| 1 | `# Safe review` | Current section title. |
| 2 | `Never send production writes.` | Explicit negative guarantee. |
| 4 | `Measured limit: one local fixture; runtime effectiveness is UNASSESSED.` | Preserves the measured bound and **UNASSESSED** status without implying runtime validation. |
| 5 | `History: 2026-09-18, issue #42 recorded the schema change.` | Durable history with the original date **2026-09-18** and issue ID **#42**. |
| 6 | `Formal reference: https://example.test/spec/v1` | Formal URL retained exactly: **https://example.test/spec/v1**. |

[fixtures/recorded.json](../../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) must remain untouched. Its `expected` value is recorded payload; process-like wording there belongs to the fixture’s expected data. Cleaning it would change that expectation and compromise fixture fidelity. The skill explicitly protects recorded fixtures, and your request prohibits all edits.

The fixture was inspected only to explain that protection. No bilingual counterpart was found.
