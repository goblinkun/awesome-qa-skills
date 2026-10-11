**1. Today’s goals and scope.** In SIT, prioritize the payment callback retry fix, then coupon display. Use the morning smoke window to establish current-build readiness. Produce a defect wrap-up in the afternoon.

Cover the changed order/payment paths and coupon selection, discount, and order-summary consistency. Defer broad browser, performance, and unrelated order regression unless capacity remains.

**2. Cadence, stage outputs, and gates.** Current focus: morning review. No execution evidence has been supplied.

| Stage | Actions | Stage output | Exit gate |
|---|---|---|---|
| **Morning review → smoke** | Confirm build, acceptance criteria, carryover defects, owners, and test data. Run current-build checkout/order/payment smoke during the available window. | Agreed P0–P2 queue, explicit exclusions, build/data baseline, smoke evidence, blocker owner if needed. | **Currently RED / unverified:** execution opens only after SIT is observed usable and current-build smoke passes. |
| **Execution → midday checkpoint** | Execute payment P0 checks first, then coupon P1 checks. Capture failures immediately. At midday, check whether P0 execution has started. | Results linked to checks, callback/order evidence, registered defects, updated remaining scope. | Every P0 has PASS/FAIL/BLOCKED status by close. If P0s have not started by midday, cut P2 and replan the afternoon. |
| **Afternoon review → defect wrap-up** | Triage failures, retest available fixes, reconcile coverage, and assign carryover. | Defect summary, retest status, unresolved risks, owners, and tomorrow’s Top 3. | **Pending:** every P0 failure has a defect or escalation; every blocked item has an owner and next checkpoint. |

If smoke cannot run or fails because SIT is unusable, keep readiness **RED**. Escalate recovery and continue offline coverage preparation; assigning an owner does not clear the gate.

**3. Risk priority.** These are execution priorities; defect severity follows observed impact.

| Priority | Work | Risk driving the order |
|---|---|---|
| **P0** | Payment callback retries, duplicate delivery, retry exhaustion, and resulting payment/order state consistency. | Lost payment updates, false paid states, or repeated downstream order actions. |
| **P1** | Coupon eligibility/display, apply/remove behavior, and agreement between displayed discount and checkout/order totals. | Misleading discounts or customer-visible inconsistency. Elevate confirmed charged-amount errors to P0. |
| **P2** | Coupon copy, spacing, and additional display variants. | Lower-impact presentation defects; first scope to cut. |

**4. Morning review focus.** Before the smoke window ends, confirm expected retry limits, terminal failure behavior, coupon rules, and available callback evidence. Assign QA, payment-development, and SIT recovery owners. Prepare executable checks for each P0 risk.

**5. Handoff.** Next: invoke `test-strategy` with the two stories, SIT smoke constraint, priority queue, and afternoon wrap-up requirement. Carry the unknown build/readiness evidence, acceptance-criteria gaps, and **owner currently unassigned**. Required output: agreed coverage, owners, exclusions, and checkable gates.

**6. Risks, blockers, and assumptions.** Build ID, SIT health, carryover defects, staffing, and detailed acceptance criteria are unknown. Times therefore use milestones. If callback logs or payment simulation are unavailable, mark the affected checks BLOCKED and escalate access; UI observations alone cannot establish retry correctness.

**7. Afternoon defect wrap-up.** Status now: **not at wrap-up; defect sync UNKNOWN**. Record:

- Coverage by story: planned, passed, failed, blocked, and not run.
- Each defect: impact/severity, reproduction evidence, owner, status, and retest outcome.
- Unresolved P0/P1 risks and the scope deferred.
- Tomorrow’s proposed Top 3: unresolved payment risks, blocked checks/retests, then remaining coupon coverage.

Completed reporting does not clear unresolved execution blockers.
