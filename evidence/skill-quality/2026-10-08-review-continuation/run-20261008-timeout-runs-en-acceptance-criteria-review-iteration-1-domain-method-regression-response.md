Static comparison of the four v3 originals finds two contradictions, one matching observation, and one missing rule. This review preserves the originals and separates proposed rewrites. FAIL/PASS describes this fixture only; no real system was tested.

All original criteria and observations come from the supplied sanitized v3 fixture. Working assumptions: the supplied order amounts are the amounts compared against the shipping threshold, and monetary values use consistent currency units. The rules and observations are comparable within v3; runtime records, balances, timestamps, permissions, and dependency behavior are absent.

Prioritize AC-8 as P1 because duplicate refunds affect accounting, then AC-7 as P2 because customers are overcharged at the boundary. AC-10 is P2 because its ambiguity prevents timing acceptance. AC-9 provides a matching control. The fixture cannot establish defect frequency or root cause.

The original criteria and observable oracles are:

- **AC-7 — v3, `review`.** Original: “orders >= 100 currency units have free shipping.” Given an order amount of 100, calculate shipping: the expected charge is 0 currency units; the supplied charge is 5. Equality belongs to `>= 100`. Boundary scenarios at 99, 100, and 101 therefore expect shipping charges of 5, 0, and 0 respectively, using AC-9 below the threshold. These scenarios are proposed checks.
- **AC-8 — v3, `review`.** Original: “retries with the same refund_id must not debit twice.” Given the successful 20-unit refund, capture its business key, cumulative refund, remaining refundable balance, and persisted accounting state; then retry the same request. Expected postconditions: cumulative refund remains 20 currency units, the retry adds 0, refundable balance does not decrease again, and persisted records contain only one effective refund debit for that key. The fixture reports cumulative refunds of 40. A successful response alone cannot prove these accounting postconditions; ledger and balance evidence are missing.
- **AC-9 — v3, `review`.** Original: “orders < 100 pay 5 shipping.” Given an order amount of 99, calculate shipping: expected and supplied charges both equal 5 currency units. This criterion is sufficiently defined and testable. Exactly 100 is excluded by `< 100` and covered by AC-7.
- **AC-10 — v3, `missing-rule`.** Original: “refund promptly.” Attempting to construct a timing assertion exposes missing start and end events, a maximum duration, and its unit. No observable timing acceptance condition can be derived from this wording.

The following are **proposed rewrites**, separate from those originals:

- **AC-7:** Given an order amount of at least 100 currency units, when shipping is calculated, then the shipping charge is 0 currency units. This makes the existing inclusive boundary explicit.
- **AC-8:** Given a successful 20-unit refund with a particular `refund_id`, when that request is retried, then cumulative refunds remain 20 currency units, refundable balance remains unchanged from its post-success value, and no additional effective debit is persisted. Apply the same postcondition when the original debit succeeded but its response was lost. This exposes the accounting invariant.
- **AC-9:** Given an order amount below 100 currency units, when shipping is calculated, then the shipping charge is 5 currency units. This makes the observable charge explicit.
- **AC-10:** Given [product-defined refund scope], when [approved start event] occurs, then [approved end event] occurs within [approved limit and unit]; if the deadline is missed, then [approved observable failure or escalation outcome] occurs. Product must resolve every placeholder before this becomes executable.

The first three proposals preserve the supplied policies. Product confirmation remains necessary for monetary amount calculation, invalid inputs, conflicting retry payloads, authorization failures, pending refunds, and provider failures; their outcomes must not be invented.

Calculations:

- `shipping_at_threshold`: expected 0; observed 5; excess = 5 − 0 = **5 currency units**. Evidence: AC-7, amount 100, and supplied shipping charge 5.
- `refund_retry`: expected cumulative refund 20 and retry increment 0; observed cumulative refund 40 and increment = 40 − 20 = **20 currency units**. Evidence: AC-8’s successful refund and same-key retry.
- `shipping_below_threshold`: expected 5; observed 5; difference = 5 − 5 = **0 currency units**. Evidence: AC-9, amount 99, and supplied shipping charge 5.

AC-10 blocks timing acceptance until Product defines its rule. Missing accounting records prevent conclusions about actual money movement or implementation causes. These findings do not establish runtime correctness or release readiness.

Minimal validation performed: arithmetic and output schema checks. The smallest proposed follow-up is for QA to check the three shipping boundaries and compare refund totals, balances, and persisted debits before and after a same-key retry; Product must first define the timing oracle. No external actions were taken.

| ID | DECISION | Evidence |
| --- | --- | --- |
| AC-7 | FAIL | v3: 100 >= 100 requires shipping of 0 currency units; the fixture reports 5. |
| AC-8 | FAIL | v3: the same refund_id retry must add 0 currency units; the fixture reports cumulative refunds rising from 20 to 40. |
| AC-9 | PASS | v3: 99 < 100 requires shipping of 5 currency units; the fixture reports 5. |
| AC-10 | MISSING_RULE | v3: "refund promptly" supplies no time limit or observable start and end events. |
