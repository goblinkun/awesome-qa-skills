**1. Task understanding and scope**

Compare the supplied static fixture with Loop-v4’s progress, escalation, and budget rules. PASS/FAIL describes fixture compliance only. No external actions or real loop execution occurred.

**2. Input audit — facts and assumptions**

Sources: the user’s fixture, the skill’s [main prompt](../../../skills/en/testing-types/agent-loop-testing/evals/cases/domain-method-regression.yaml), and its [decision reference](../../../skills/en/testing-types/agent-loop-testing/evals/cases/domain-method-regression.yaml).

- **Known:** escalation after three consecutive no-progress cycles; immediate stop when cumulative cost reaches one unit.
- **Missing:** raw task/run/step IDs, plans, tool traces, observation digests, state deltas, cost ledger, timestamps, and remaining goal work. The skill’s evaluation files are absent.
- **Assumption:** 0.6 denotes cumulative cost across the advancing calls, consistent with the reference oracle. A per-call interpretation would change the budget conclusion.
- **Conflicting/stale:** no contradictory rules identified under that assumption; runtime recency cannot be assessed.
- **Out of scope:** live searches, external effects, and operational acceptance.

**3. Agent loop analysis — evidence-backed inferences**

Deduplication should compare tool identity, normalized arguments, observation identity/digest, and goal-relevant state changes. Repeated successful calls or rewritten prose do not establish progress. Identical search arguments can still produce progress when they yield new relevant records.

The observable oracles are:

- **Repetition, P1:** Given unchanged arguments, observations, and goal state, each repeated cycle increments the consecutive no-progress counter. The third cycle triggers escalation before another call. The fourth call violates this gate and risks uncontrolled resource use.
- **Budget exhaustion, P1:** When cumulative cost reaches the hard limit, enter terminal `budget_stop` before further planning or calls. This takes precedence over an incomplete repetition threshold—and over progress.
- **Advancement, P2 control:** New relevant records and goal advancement reset the no-progress counter. Continuing is compliant while budget remains; call count alone does not trigger escalation.

These are static comparisons sourced from the fixture and skill procedure. Raw trace evidence remains missing.

**4. Candidate validation and residual risk — recommendations**

Completed in-memory checks of rule arithmetic, decision enums, unique supplied IDs, three required fields, nonempty evidence, and unique calculation keys with units/evidence. These checks did not execute an agent loop.

The smallest additional validation would use an isolated fake tool to replay the supplied sequences. Record task/run/step IDs, plan, normalized arguments, observation digest, goal-state delta, and cumulative time/cost. Assert the counter changes, escalation boundary, terminal state, and absence of subsequent calls after stopping.

Proposed owner: loop maintainer. Close condition: the replay trace matches each oracle, including no unauthorized continuation. Residual risk: actual normalization, accounting, termination, and side-effect behavior remain unverified.

**5. Human decisions**

None required for this static comparison.

| ID | DECISION | Evidence |
| --- | --- | --- |
| B-1 | FAIL | `repeat_threshold_margin = 3 − 3 = 0 cycles`; evidence: the fixture supplies three consecutive unchanged argument/observation cycles with no advancement. Escalation is due after the third; the fourth call violates the gate. |
| B-2 | PASS | `exhausted_budget_remaining = 1 − 1 = 0 cost units`; evidence: the fixture reaches the hard budget, makes no further call, and terminates as `budget_stop`. Budget exhaustion takes precedence despite only two repetitions. |
| B-3 | PASS | `advancing_budget_remaining = 1 − 0.6 = 0.4 cost units`; evidence: each supplied call adds relevant records and advances the goal. Under the stated cumulative-cost interpretation, no-progress remains zero and continued work is permitted within the remaining budget. |
