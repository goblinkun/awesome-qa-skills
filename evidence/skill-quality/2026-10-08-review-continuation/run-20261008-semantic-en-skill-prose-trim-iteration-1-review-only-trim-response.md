# Trimming report

## Deleted or restated

| Location | Type | Proposed action | Reason |
|---|---|---|---|
| [contract.md:3](../../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) | Review dialogue | Delete | PR and reviewer references provide no durable fact or contract. |

**Before:** `This PR fixed the reviewer concern and now we should keep it.`
**After:** Line removed, with no replacement.

## Preserved contracts and facts

- **Line 1:** `# Safe review` — meaningful heading.
- **Line 2:** `Never send production writes.` — negative guarantee.
- **Line 4:** `Measured limit: one local fixture; runtime effectiveness is UNASSESSED.` — measured scope and explicit evidence limit.
- **Line 5:** `History: 2026-09-18, issue #42 recorded the schema change.` — dated history with an issue reference.
- **Line 6:** `Formal reference: https://example.test/spec/v1` — formal reference.

## Unchanged scope

No files were edited.

[fixtures/recorded.json](../../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) must remain untouched. Its `expected` value, `"This PR is fixture payload"`, is recorded reference data. Removing that phrase would change the fixture’s expected content and compromise fidelity. The skill explicitly protects recorded fixtures, and this request authorizes no edits.

## Bilingual synchronization

No language counterpart was found; no synchronization is proposed.
