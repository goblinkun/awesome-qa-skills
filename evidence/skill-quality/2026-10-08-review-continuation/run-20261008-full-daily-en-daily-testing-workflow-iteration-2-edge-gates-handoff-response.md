This is a proposed daily QA workflow; no build, environment, owners, or execution results were supplied.

Today’s scope is current-build smoke, critical change coverage, risk-ordered testing, defect tracking, and wrap-up. Defer P2 work when P0 work is blocked or behind schedule. Exploratory testing requires a cleared smoke gate.

| Stage | Entry gate | Exit gate | Handoff point → skill |
|---|---|---|---|
| Morning planning | Candidate changes and carryover defects identified; unknown inputs marked | P0–P2 queue, owners, scope, and explicit deferred work recorded | Risk prioritization → `test-strategy` |
| Environment, data, and smoke | Target build/environment identified; smoke checks and required data available | Environment observed usable **and current-build smoke passes**. Failed or unavailable smoke keeps readiness **RED** | Smoke execution/recovery → `automation-testing` |
| Case preparation | Scope and expected behavior clear; offline preparation allowed during recovery | Every critical change has an executable new or reused check, prerequisites, and expected results | Coverage preparation → `test-case-writing` |
| Functional/regression execution | Readiness **GREEN**; selected checks and data ready | Every in-scope P0 check has a recorded PASS, FAIL, or BLOCKED disposition; failures enter defect logging | Ready checks → `functional-testing` |
| Exploratory testing | Current-build smoke passes; environment usable; P0 execution has started; charter and timebox agreed | Session findings, evidence, coverage gaps, and defects recorded | Approved exploratory session → `manual-testing` |
| Defect logging, throughout the day | A smoke or execution failure is observed | Failure has a defect reference with reproduction evidence, impact, severity, status, and owner or escalation | Immediately upon failure → `bug-reporting` |
| Afternoon review | Available results, defects, and unresolved blockers collected—even if testing remains blocked | **Defect summary produced and reviewed before wrap-up**; priorities and carryover updated | Afternoon consolidation → `test-reporting` |
| End-of-day wrap-up | Afternoon defect summary complete; P0 dispositions accounted for | Done, carryover, risks, owners, and tomorrow’s Top 3 recorded; every P0 failure registered or escalated | Final daily handoff → `test-reporting` |

Gate status is conditional until evidence is available:

- **Start:** RED after failed/unavailable smoke or an unusable environment. Assigning a recovery owner does not clear it. Require observed recovery and passing smoke for the current build.
- **Midday:** If P0 execution has not started, replan the afternoon and cut P2 work.
- **Afternoon:** RED until the defect summary is complete and reviewed.
- **Close:** Clear only when all P0 checks have a documented disposition, all P0 failures are registered or escalated, and EOD notes exist. A blocked day can close administratively while execution readiness remains RED.

The proposed priority queue is **P0:** smoke failure, recovery, and critical checks; **P1:** changed areas and targeted regression; **P2:** lower-risk exploration and broader regression.

For the morning-failure branch, immediately record the failure and keep environment-dependent execution blocked. **Do not start exploratory testing.** Continue offline case preparation while recovery proceeds. A replacement build requires its own passing smoke before execution resumes.

Next on a failed smoke: invoke `bug-reporting` at failure capture. Keep the current build/environment, failed check, observed behavior, evidence, and recovery ownership available for the handoff.

Owners, escalation contacts, exact coverage, and capacity remain unknown. Unexecuted checks retain NOT_RUN or BLOCKED status; no passing result is inferred from recovery activity.

Not at wrap-up yet. The required afternoon defect summary must cover defect IDs, severity/impact, status, owners, blockers, and unresolved risks. Record zero observed defects only when supported, alongside actual coverage. Carry that summary into the EOD report with completed work, deferred work, recovery actions, and tomorrow’s Top 3.
