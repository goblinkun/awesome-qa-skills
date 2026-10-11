**Scope.** Compare the supplied traces with R-v2. All decisions concern this static fixture; no recovery system or external service was executed.

**Input audit — facts.** R-v2 and the trace statements are the primary evidence. The [skill prompt](../../../skills/en/testing-types/agent-failure-recovery-testing/evals/cases/domain-method-regression.yaml) defines the procedure; its [calibration example](../../../skills/en/testing-types/agent-failure-recovery-testing/evals/cases/domain-method-regression.yaml) repeats this fixture and provides no independent execution evidence.

Known: protocol and described writes/retries. Missing: query chronology, inspectable ledger and attempt logs, notices, escalation receipts, amounts, resources, environment and timestamps. The described violations conflict with R-v2; source definitions are consistent. Recency is unknown. External execution and actual remediation are out of scope. Trace statements are accepted as fixture facts only.

**Analysis — evidence-backed inferences and observable oracles.** Priorities describe review urgency, not measured incident severity. Owner roles below are proposed.

- **Committed debit followed by timeout — P1:** duplicate financial writes require attention from the debit/recovery maintainer. The requester’s timeout leaves its outcome uncertain; the fixture establishes commitment. Query by `operation_id` and read back the committed result. Oracle: one debit entry and the existing result returned. Stop replay upon confirmed commitment; conflicting entries require escalation. Closure evidence: ordered query/write logs, ledger entries and user-result notice.
- **Partial completion — P2:** the recovery maintainer must reconcile completed and remaining steps, preserve committed steps and execute only uncommitted work. Oracle: state query precedes retry, completed steps are skipped, and each intended step has one entry. Stop mutation if state remains indeterminate. Closure evidence: step-state records, query/recovery chronology and completion notice. The supplied outcome supports the resume pattern; query ordering remains unverified.
- **Permanent permission denial — P2:** unchanged retries waste resources and delay handoff. Stop and escalate to the access/service owner; notify the user. Oracle: no unchanged retry after permanent classification, with observable notice and escalation events. Closure evidence: attempt history and handoff receipts. R-v2 supplies no permission-bypassing fallback or compensation authority.

**Candidate validation and residual risk.** Proposed minimal validation: replay these histories locally against mocked state and ledger functions, recording queries, writes, attempts, notices and escalations; compare those records with the oracles above. This was not performed. A local static check verified the supplied count/set comparisons and table structure. Runtime recovery, notification delivery, resource effects and missing query ordering remain unverified.

**Human decisions.** None is needed for this fixture comparison. Any remediation of the excess debit requires business-owner authorization; that authority is absent from the fixture.

| ID | DECISION | Evidence |
| --- | --- | --- |
| F-1 | FAIL | R-v2 permits 1 debit entry per operation_id; the supplied trace records 2 committed entries for pay-1 after timeout and replay. Required branch: query pay-1 and return its committed result; stop further debits and escalate the duplicate for authorized remediation. Final supplied state: duplicate debit; amounts unknown. |
| F-2 | PASS | Supplied trace: steps 1/2 committed; recovery executes only step 3, with 1 entry per step. Final supplied state: steps 1–3 committed once each. Required branch: query and reconcile state, then execute only uncommitted step 3. Query chronology is absent; this verdict covers the described partial-resume pattern. |
| F-3 | FAIL | R-v2 requires permanent permission errors to stop and escalate; the supplied trace shows 5 unchanged retries after permanent 403. Required branch: stop, notify, and escalate. Final business state is unknown; notice and escalation evidence are absent. |
