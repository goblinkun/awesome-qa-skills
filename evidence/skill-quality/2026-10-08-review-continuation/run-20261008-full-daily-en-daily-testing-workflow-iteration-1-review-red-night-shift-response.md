Plan based on [day.json](../../../skills/en/testing-workflows/daily-testing-workflow/evals/cases/review-red-night-shift.yaml). All times are **Asia/Shanghai**; midnight crosses into the following day. This is a plan, with no execution results claimed.

1. **Goals and scope:** Use the four-hour **22:00–02:00** shift for B17 environment recovery, offline P0 preparation, and conditional P0-payment execution. Defer P2-copy and exclude broader regression.

2. **Stage and gate status:** Focus on environment readiness and offline preparation.

   | Milestone | Current status | Decision criteria |
   |---|---|---|
   | Start — 22:00 | **RED** | Environment is RED and smoke unavailable. Clear only with observed recovery **and passing B17 smoke**. Lin’s ownership alone does not clear readiness. |
   | Checkpoint — 00:00 | **PENDING** | Check readiness and whether P0 execution has started. If either is unresolved, keep P2 deferred and replan the remaining time. |
   | Close — 02:00 | **PENDING** | Account for every scoped P0 check, register or escalate any observed P0 failure, and record evidence gaps, risks, and carryover. |

3. **Priority queue:**
   **P0-payment:** input status `NOT_RUN`; first execution priority after readiness clears.
   **P2-copy:** input status `NOT_RUN`; deferred for this shift.

4. **Bounded shift plan:**

   | Window | Planned work |
   |---|---|
   | 22:00–22:15 | Confirm B17 baseline; request recovery ETA and smoke evidence from Lin; record the blocker and escalation recipient. |
   | 22:15–00:00 | Track recovery; prepare the scoped P0 checks, data needs, and expected outcomes offline. Execute only after the start gate clears. |
   | 00:00–01:40 | Apply the checkpoint decision. If ready, prioritize P0 within remaining capacity. Otherwise continue offline preparation and blocker handoff. |
   | 01:40–02:00 | Stop execution; reconcile evidence, failures, blockers, and carryover. Close at 02:00 without extending the shift. |

5. **Handoff:** Next: invoke **`test-strategy`** with B17, the four-hour shift, RED environment, unavailable smoke, recovery owner Lin, P0-payment priority, and deferred P2-copy. Request a bounded recovery/offline plan with explicit P0 scope and the evidence required before execution.

6. **Risks, blockers, assumptions:** Recovery timing, payment acceptance criteria, smoke procedure, data readiness, and escalation recipient are unspecified. The 00:00 checkpoint and 20-minute close window are proposed allocations. Late recovery may leave P0 incomplete.

7. **Close notes:** Not at wrap-up. No failure evidence or defect-sync records were supplied. At close, preserve `NOT_RUN` for unexecuted work and document its blocker; record supported outcomes only. Reporting may close while environment readiness remains **RED**.
