**Primary recommendation:** `authorization-testing` — check object-level permissions when authenticated userA changes `objectID` to userB’s record. Capability stage: Core QA. The exact ID is listed in the [local inventory](../../../skills/en/testing-workflows/discover-testing/references/skill-capability-inventory.json).

**Optional supporting skill:** none.

**Why this fits:**

- Changing `objectID` tests permission to access another user’s record.
- Valid login establishes the supplied authentication context; the remaining question concerns authorization.
- The [routing prompt](../../../skills/en/testing-workflows/discover-testing/prompts/discover-testing.md) prioritizes this explicit specialty.
- This is one focused testing goal; no Composition route, Plus variant, or tool-specific helper is needed.

**Next step plan:** The target is **UNAVAILABLE**, because the supplied request explicitly states it is not installed. For a future handoff, make `authorization-testing` available and provide sanitized request details, record ownership/sharing rules, and expected access behavior. Expected output: focused authorization cases and evidence requirements. No installation or invocation was performed.

**Evidence gaps:** The access policy and response evidence are missing. Whether userA should be denied—and whether unauthorized access occurs—cannot be established.

**Minimal validation:** Parsed the static inventory and confirmed one exact canonical-ID match against the supplied enum. This is fixture comparison only; real execution is **NOT_RUN**.

| ID | DECISION | Evidence |
| --- | --- | --- |
| ROUTE | authorization-testing | Inventory lists the canonical ID with availability UNKNOWN; explicit input “target is not installed” establishes UNAVAILABLE. |
