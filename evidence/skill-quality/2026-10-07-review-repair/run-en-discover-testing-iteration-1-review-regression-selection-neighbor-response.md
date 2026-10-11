`change-regression` is the Composition context; the current stage is Engineering QA / regression planning. ([Reference](../../../skills/en/testing-workflows/discover-testing/reference.md))

**Primary recommendation:** `regression-test-selection` — choose the smallest regression set covering affected obligations, considering test costs.

**Optional supporting skill:** None.

**Why this fits:**

- Change impact is already confirmed.
- Obligation coverage and test costs identify regression selection as the specific goal.
- One selection deliverable needs one primary; explicit specialties take precedence over broad Composition routing. ([Routing prompt](../../../skills/en/testing-workflows/discover-testing/prompts/discover-testing.md))

**Next step and evidence gaps:** Hand off affected obligations, obligation-to-test mappings, candidate costs, mandatory coverage, and the optimization objective. These details are absent; “smallest” needs clarification as test count versus total cost. Expected output is a justified selection with coverage, costs, and uncovered obligations.

**Minimal validation:** PASS — static fixture comparison only. The canonical ID appears exactly once in the catalog and matches the supplied DECISION enum. Installation is user-supplied evidence; live callability remains unverified. No target invocation, test execution, or external action occurred.

| ID | DECISION | Evidence |
|---|---|---|
| ROUTE | regression-test-selection | Supplied fixture states “Target is installed”; exact canonical ID verified in the [local inventory](../../../skills/en/testing-workflows/discover-testing/references/skill-capability-inventory.json), whose standalone availability is UNKNOWN. |
