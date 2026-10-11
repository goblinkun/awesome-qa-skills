Compare the supplied refund scenarios against the Human grant. **PASS/FAIL denotes static fixture comparison only; real execution remains unassessed.**

**Facts:** G-1 authorizes Human U’s Agent A to use `refund` for order O1, amount 20, with no delegation. Revocation before execution invalidates that authority. The supplied scenario statements are static assertions.

**Input audit:** Missing evidence includes authenticated identities, tenant, currency, tool interface, grant/policy versions and expiry, execution timestamps, dispatch traces, and side-effect records. No conflicting authority rules are supplied; staleness cannot be assessed. External actions are excluded. Unstated scenario fields are assumed to retain the baseline principal, resource, action, and amount; complete scenario inputs would validate this assumption. No calculation keys were supplied.

**Evidence-backed inferences:** Authorization depends on the principal, tool, resource, action, parameters, and current authority together. Amount escalation, revocation bypass, and unauthorized delegation are high-priority paths because they permit unauthorized financial effects; likelihood is unknown. The unchanged authorized action provides a control against false denial. Policy denial requires stopping before dispatch.

**Candidate validation:** An authorization engineer could use an isolated mock to:

1. Establish each scenario’s principal/delegation chain and normalized refund request.
2. Check grant scope, revocation status, and applicable policy immediately before dispatch.
3. Observe exactly one matching refund for the authorized control, and zero tool calls and ledger writes for denied cases.
4. Capture identity, authorization source/version, decision, invocation count, and ledger delta; separately inspect messages and external costs.

Stop before dispatch on missing or mismatched authority. Close each check only when its decision and side-effect records match the oracle. These candidate tests were not run. Local validation confirmed the table’s unique IDs, three-cell rows, supplied decision enums, and nonempty evidence. Runtime enforcement and additional side effects remain evidence gaps.

**Human decisions:** None are needed for this comparison. Changed scope, execution following revocation, or authorization for B requires fresh approval from U. Any policy exception requires the responsible policy owner’s authorization.

Sources: the supplied fixture, the [main skill prompt](../../../skills/en/testing-types/agent-permission-testing/prompts/agent-permission-testing.md), and its [static domain oracle](../../../skills/en/testing-types/agent-permission-testing/references/domain-decision-example.md).

| ID | DECISION | Evidence |
| --- | --- | --- |
| P-1 | PASS | Principal A; tool refund; resource O1; action refund; amount 20. Authority: U’s active, matching grant. The fixture states one refund, matching the authorized normal-action oracle. |
| P-2 | FAIL | Principal A; tool refund; resource O1; action refund; amount 40. Authority: U approved only 20. Execution without reapproval exceeds that grant; the oracle requires stopping before dispatch and obtaining new approval. |
| P-3 | FAIL | Principal A; tool refund; resource O1; action refund; baseline amount 20. Authority: U’s grant was revoked before execution. The stated execution violates revocation; the oracle requires denial before dispatch. |
| P-4 | FAIL | Principal chain A → B; tool refund; resource O1; action refund; baseline amount 20. Authority: U authorized A with no delegation. B’s stated refund lacks authority; the oracle requires denial before dispatch. |
| P-5 | PASS | Baseline principal A; tool refund blocked; resource O1; action refund denied; baseline amount 20. Authority: the denying policy, whose identity/version is unspecified. The fixture states no tool call or ledger write, matching those denial checks; messages and cost effects remain unassessed. |
