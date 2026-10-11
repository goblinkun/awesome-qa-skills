Plan only, based on `day.json`; no execution or recovery results are claimed.

1. **Goals and scope**
   Use the four-hour **22:00–02:00 Asia/Shanghai** shift for B17 environment recovery and P0-payment readiness. Run P0-payment only if the execution gate clears. Defer P2-copy, broader regression, and overtime.

2. **Stage and gate status**
   Focus: environment readiness and offline planning.
   - **Start: RED** — environment is RED; B17 smoke is unavailable. Lin is the recovery owner; ownership does not clear the gate.
   - **Checkpoint: pending** — assess at 00:00.
   - **Close: pending** — assess at 02:00.

   Execution requires **observed environment recovery and passing smoke on B17**.

3. **Priority queue**

   | Priority | Item | Recorded status | Shift disposition |
   |---|---|---|---|
   | P0 | P0-payment | NOT_RUN | First executable work after readiness clears |
   | P2 | P2-copy | NOT_RUN | Deferred |

4. **Bounded milestone plan**

   | Milestone | Time budget | Planned work and exit criteria |
   |---|---|---|
   | Start | 22:00–00:00, 2 hours | First 15 minutes: confirm B17 baseline and request recovery evidence/ETA from Lin. Remaining time: offline P0 preparation and recovery tracking. Keep execution blocked until both readiness conditions pass. |
   | Checkpoint | 00:00–01:30, 1.5 hours | Check readiness and whether P0 has started. If ready, prioritize P0 within the remaining window. If still blocked, escalate the blocker with Lin’s latest status; continue offline preparation. Keep P2 deferred. |
   | Close | 01:30–02:00, 0.5 hours | Stop new execution and prepare handoff. At 02:00, stop work; record evidenced outcomes, unfinished P0 work, blocker ownership, and carryover. |

5. **Handoff — exactly one next Skill**
   Next: invoke `test-strategy` with the four-hour shift, B17, RED environment, unavailable smoke, Lin as recovery owner, P0-payment priority, and deferred P2-copy. Request a bounded recovery/offline plan requiring environment recovery evidence and passing B17 smoke before execution.

6. **Risks, blockers, assumptions**
   The readiness blocker may consume the entire shift. Recovery ETA, payment acceptance checks, smoke procedure, QA owner, and escalation recipient are unknown. The 00:00 checkpoint and 01:30 execution cutoff are proposed planning boundaries.

7. **EOD notes**
   Not at wrap-up. At close, every P0 check needs an evidenced result or explicit blocked/unrun disposition; any observed P0 failure needs a defect or escalation. Record remaining risks and next-shift priorities. A completed handoff does not make readiness GREEN.
