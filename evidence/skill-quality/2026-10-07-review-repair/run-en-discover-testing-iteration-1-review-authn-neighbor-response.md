Primary recommendation: **`authentication-testing`** — check wrong-password rejection, expired-token handling, and login session creation.

Optional supporting skill: **none**.

Why this fits:

- These checks concern authentication; cross-user record access would concern authorization.
- The [routing prompt](../../../skills/en/testing-workflows/discover-testing/prompts/discover-testing.md) prioritizes explicit specialties.
- The [inventory](../../../skills/en/testing-workflows/discover-testing/references/skill-capability-inventory.json) confirms the exact canonical ID. This is a Core QA request; no structured [Composition route](../../../skills/en/testing-workflows/discover-testing/reference.md) matches.

Next step: hand off the sanitized login contract, token-expiry rules, and expected session behavior to produce a focused authentication checklist. Prioritize wrong-password and expired-token rejection.

Evidence gaps: expected responses and session details are missing. Installation is asserted by the supplied fixture; the inventory records availability as `UNKNOWN` and does not independently establish Host callability.

Minimal validation: **PASS — fixture comparison only**. The selection matches the allowed enum and canonical inventory ID. No authentication tests or external actions were performed.

| ID | DECISION | Evidence |
|---|---|---|
| ROUTE | authentication-testing | Supplied fixture explicitly states the target is installed; inventory confirms the canonical ID. Host callability was not exercised. |
