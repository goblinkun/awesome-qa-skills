Compare the supplied fixture against L-v1 for recovery, writes, lease validity, cancellation, and resource release. All decisions below describe **static fixture comparison**, not real test execution. No external actions were taken.

**Facts and input audit.** The user-supplied protocol and fixture are the evidence sources. The skill’s [main prompt](../../../skills/en/testing-types/agent-long-running-testing/evals/cases/domain-method-regression.yaml) supplies the procedure; its [reference oracle](../../../skills/en/testing-types/agent-long-running-testing/evals/cases/domain-method-regression.yaml) agrees with the comparisons below.

Known rules: checkpoint v2 records committed steps; expired leases cannot commit; each task_id has one execution; cancellation after commit returns completed. Missing evidence includes actual task IDs, checkpoint payloads and integrity, write ledgers, heartbeat and expiry timelines, cancellation acknowledgments, and resource release records. Recency is unspecified; no stale evidence is established. The failing observations contradict protocol rules, without establishing conflicting source definitions. Assume the statements describe independent cases faithfully; trace records would validate that assumption. Runtime recovery and external operations are outside scope.

**Domain steps and evidence-backed inferences.** Proposed priorities reflect potential impact, not measured likelihood.

- **Checkpoint and resume — P1; persistence owner.** Given A’s commit, crash, and recovery, inspect checkpoint version, committed step IDs, provenance, integrity, and subsequent writes. The observable oracle is v2 recovery running only B while preserving A’s effect. Close with a matching checkpoint and write ledger; stop proposed recovery if version or integrity validation fails.
- **Lease and heartbeat — P1; scheduler owner.** Given an expired lease attempting a commit, compare ownership and expiry with the commit event. The oracle is rejection of the expired owner’s commit. The supplied successful commit violates this rule. Heartbeat renewal evidence is absent. Close with an expiry timeline and rejection record; stop on an expired-owner commit.
- **Duplicate execution — P1; task and persistence owners.** Given repeated recovery or duplicate submissions for one task_id, inspect execution identities and writes. The oracles are one execution per task_id and no replay of committed effects. The second write establishes replay failure; missing task IDs prevent assessing duplicate-submission handling. Close with execution and effect records; stop on duplicate execution or repeated committed writes.
- **Cancellation — P1; task owner.** Given commit before cancellation, preserve the committed result and return completed. The supplied terminal state matches that oracle. Cancellation acknowledgment remains missing. Close with ordered commit/cancel events, acknowledgment, and preserved effects; stop if cancellation reverses committed work.
- **Timeouts — P1; protocol owner.** Examine timeout-triggered interruption, ownership expiry, and attempted recovery. Lease expiry prohibits committing, but other timeout transitions and deadlines are undefined. Close only after those rules and their observable events are supplied; do not infer timeout behavior.
- **Resource lifecycle — P2; executor owner.** At terminal state, compare active resources with allocations and releases. The supplied zero counters support release within the fixture; they do not prove actual teardown. Close with reconciled resource records; stop closure if resources remain active or unreconciled.

Only the supplied event orders are established. Other transitions, including cancellation before commit, remain open.

**Candidate validation and residual risk.** The smallest further validation is a read-only review of recorded checkpoints, writes, lease events, cancellation results, and resource records against these oracles. It was not performed. Locally checked the decision output for unique supplied IDs, allowed enums, three cells per row, and nonempty evidence. No calculation keys were supplied or added. Runtime behavior remains unverified.

**Human decisions.** None are needed for these fixture comparisons. The protocol owner must define missing heartbeat, timeout, and precommit cancellation behavior before runtime validation.

| ID | DECISION | Evidence |
| --- | --- | --- |
| L-1 | PASS | A commits before the crash; checkpoint v2 recovery runs only B, avoiding another A write; active resources = 0 supports release in the fixture. |
| L-2 | FAIL | Recovery repeats A with a second write, violating committed-step recovery. Recovery version and release evidence are unspecified. |
| L-3 | FAIL | Expired lease 4 still commits, violating the lease rule. Checkpoint version, write count, and release evidence are unspecified. |
| L-4 | PASS | Commit precedes cancellation; completed and active resources = 0 match the protocol. Checkpoint version and write ledger are unspecified. |
