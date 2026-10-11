1. **Day Goals and Scope**

   **Confirmed:** the request is “test the new feature today.” Feature details, environment, and blockers are unknown.

   **Draft goal:** check the feature’s main user outcome, investigate its highest risks, and finish with an evidence-based status and carryover list.

   **Proposed scope:** the new feature and directly affected existing behavior. **Won’t-do:** full-product regression, unrelated cleanup, or broad automation work unless today’s risks require them.

2. **Stage and Gate Status**

   **Current focus: A—Morning planning, AMBER.** Scope needs clarification. **Execution status: NOT_RUN.**

   | Gate | Current status | Checkable condition |
   |---|---|---|
   | Start/environment | **RED** | Confirm the target build, usable environment, access and data; observe passing smoke on that build. |
   | Midday checkpoint | Pending | Every P0 has started or has a recorded blocker. Otherwise, replan and remove P2 work. |
   | Close | Pending | Every P0 has a PASS/FAIL/BLOCKED result; every P0 failure has a bug or escalation; EOD notes exist. |

   Assigning a recovery owner does **not** clear the RED environment gate.

3. **Priority Queue (P0 → P2)**

   These are provisional testing priorities; confirm them once the feature is identified.

   | Priority | Work |
   |---|---|
   | **P0—first** | Establish test readiness; verify the main user outcome and highest-impact failures, including permissions, sensitive data, or irreversible actions where applicable. |
   | **P1—next** | Important alternate/error paths and regression checks for directly affected behavior. |
   | **P2—if time remains** | Lower-risk edge cases and cosmetic checks. |

4. **Focus-Stage Execution Notes**

   Use milestones because working hours and deadlines are unknown.

   | Milestone | Action and exit |
   |---|---|
   | Start of work | Identify the feature, expected outcome, scope, risks, and owners. Exit with an agreed priority list and exclusions. |
   | Readiness check | Confirm build, environment, accounts, data, and current-build smoke. If RED, continue recovery and offline preparation; execution stays NOT_RUN/BLOCKED. |
   | Before execution | Prepare or reuse executable checks for each P0, with expected results and evidence to capture. |
   | First execution block | Run P0 checks first. Record results against the build; capture failures as they occur. |
   | Midday checkpoint | Review P0 progress and blockers. Cut P2 if P0 work has not started; assign remaining work explicitly. |
   | Remaining work and close | Finish P0, retest available fixes, then address P1. Record unfinished work and tomorrow’s Top 3. |

   Log defects throughout execution with reproduction steps, expected/actual behavior, build, evidence, impact, and owner.

5. **Handoff (Next Skill)**

   **Next: invoke `requirements-analysis`** with the feature description, available requirement links, and the gaps below. Carry forward: scope unresolved; environment readiness RED; requirement and recovery owners unknown.

   Required output: agreed expected behavior, testable P0 scope, explicit exclusions, and identified owners. Evidence needed before execution: target build details and passing current-build smoke.

6. **Risks, Blockers, Assumptions**

   **Assumption:** this is a one-day assessment. Capacity and release expectations still need confirmation. Blockers have not yet been checked.

   Fill in this information:

   | Required information | What to provide |
   |---|---|
   | Feature and expectations | Feature/story/PR link, intended users, acceptance criteria, requirement decision owner. |
   | Build and environment | Build/version, environment URL, deployment status, feature flags, smoke procedure and result. |
   | Access and data | Accounts/roles, representative test data, setup/reset steps, permitted changes. |
   | Risks and dependencies | Affected components, integrations, known defects, carryover work, unavailable services. |
   | Capacity and deadlines | Tester availability, end-of-day deadline, release/freeze time, developer support. |
   | Escalation and evidence | Blocker owner/channel, bug tracker, evidence location, person receiving the final status. |

7. **EOD Notes — Not at Wrap-up Yet**

   Complete this at close:

   > Build/environment: ___
   > Tested, with evidence: ___
   > P0 results: ___ PASS / ___ FAIL / ___ BLOCKED
   > Bugs and escalations: ___
   > Untested scope and remaining risks: ___
   > Carryover owners and tomorrow’s Top 3: ___

   Completing the cadence does not establish feature readiness; that conclusion must follow the recorded results.
