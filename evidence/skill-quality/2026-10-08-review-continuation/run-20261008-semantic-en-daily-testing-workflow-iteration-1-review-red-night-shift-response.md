**1. Goals and scope.** Plan for **22:00–02:00 Asia/Shanghai**, crossing midnight, with a **4-hour limit**. Build: **B17**. Prioritize environment recovery and **P0-payment** readiness. Defer **P2-copy**; exclude broader regression and work beyond 02:00. This is a plan, with no execution results claimed.

| Milestone / time | Planned work | Exit criterion |
|---|---|---|
| **Start: 22:00–22:15** | Confirm recovery scope and ETA with Lin; record the RED environment and unavailable smoke. | Recovery owner and next update agreed, or blocker escalation recorded. |
| 22:15–00:00 | Support recovery within scope; prepare P0 checks offline. Execute only after readiness is established. | Environment usable and B17 smoke passes, or recovery blocker documented. |
| **Checkpoint: 00:00–00:15** | Review readiness and whether P0 has started. | If P0 has not started, replan remaining time around recovery/P0 preparation; keep P2 deferred. |
| 00:15–01:45 | If ready, run P0-payment checks and capture evidence. Otherwise continue bounded offline preparation and blocker follow-up. | Available outcomes and unresolved blockers recorded. Stop starting checks at 01:45. |
| **Close: 01:45–02:00** | Record outcomes, defects/escalations, carryover, and next-shift priorities. | Handoff complete by 02:00. |

**2. Stage and gate status.** Focus: **Stage B — environment and data**.

| Gate | Current status | Checkable requirement |
|---|---|---|
| Start | **AMBER** — Lin is named; execution readiness is **RED**. | Recovery ownership is established. Execution requires a usable environment and passing smoke for B17. |
| Checkpoint | **Pending / AMBER risk** — P0 is currently `NOT_RUN`. | Check whether P0 has started; if not, cut P2 and replan. |
| Close | **Pending / unassessed** | Every planned P0 check has a supported pass/fail/blocked outcome; every P0 failure has a bug or escalation; close notes expose carryover risks. |

A documented blocked outcome can satisfy reporting completeness; it does not establish test success.

**3. Priority queue.** Environment recovery, owned by **Lin**, is the dependency. **P0-payment: `NOT_RUN`**, first testing priority. **P2-copy: `NOT_RUN`**, deferred.

**4. Focus-stage notes.** While the environment remains RED, limit work to recovery coordination and offline P0 preparation. Neither item’s recorded status changes without evidence. Defect/failure synchronization is **unknown**; no failure evidence or bug references were supplied.

**5. Handoff.** Next: invoke **`test-strategy`** with B17, the four-hour shift, RED environment, unavailable smoke, recovery owner Lin, P0-payment priority, and P2-copy deferral. Require readiness evidence, executable P0 coverage, and explicit recovery/escalation checkpoints.

**6. Risks and gaps.** Recovery ETA, test data readiness, P0 coverage size, test executor, and escalation destination are unknown. The midpoint checkpoint and 01:45 execution cutoff are proposed planning choices.

**7. EOD notes.** Not at wrap-up. At close, record actual environment/smoke state, supported P0 outcomes or blockers, defect/escalation references, and carryover with owners and next checkpoints.
