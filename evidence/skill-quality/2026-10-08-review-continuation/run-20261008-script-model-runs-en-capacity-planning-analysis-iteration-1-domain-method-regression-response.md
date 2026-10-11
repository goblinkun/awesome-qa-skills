## 1. Task Understanding and Scope

Assess the supplied sanitized fixture against its p95 SLO, calculate the scaling-wait backlog, and identify what its measurements do and do not support; this is static analysis only, with no external actions or test execution.

## 2. Input Audit

The fixture gives a two-instance setup with fixed workload mix and a p95 target of 200 ms. At 100 RPS, p95 is 150 ms and CPU is 55%; at 150 RPS, p95 is 260 ms. A separate queue scenario gives 130 RPS arrival, 100 RPS validated service, and a 60-second scaling wait.

**Working Assumptions**

- The 100 and 150 RPS measurements refer to the same two-instance configuration and fixed mix.
- The backlog calculation assumes constant arrival and service rates and an initially empty queue; it gives net backlog added during the wait.

**Open Questions**

- Measurement windows, offered versus completed throughput, errors, concurrency, memory, queue depth, and resource readings at 150 RPS are absent.
- The required peak, burst, growth target, safety margin, one-instance-loss target, cost limits, and scaling policy are unspecified.
- No queue drain or recovery measurements are provided.

### evidence

The only source is the user-supplied sanitized fixture. No external sources were used. Evidence quality is suitable for comparing the stated points and calculating the stated queue scenario; it does not establish sustained production capacity or acceptance.

## 3. Risks and Priorities

- **P1 — Capacity overstatement:** extrapolating throughput from 55% CPU is unsupported, and the measured 150 RPS point already exceeds the latency SLO. Verify the SLO boundary under the same workload before relying on a higher capacity claim.
- **P1 — Degraded capacity unknown:** without one-instance-loss measurements, the fixture cannot establish SLO compliance or headroom after losing an instance.
- **P2 — Queue recovery unknown:** 1,800 requests of net backlog accumulate during the stated scaling wait under the assumptions above; drain time and user impact are unmeasured.
- **P2 — Planning inputs incomplete:** peaks and bursts, concurrency, growth, safety margin, resource bottlenecks, and cost are unassessed. The 60-second wait is supplied for the queue scenario, but actual scaling behavior is not evidenced.

## 4. Core Analysis and Execution Items

**Workload and capacity:** 100 RPS is a measured SLO-compliant point (150 ms ≤ 200 ms). The 150 RPS point fails (260 ms > 200 ms). These observations do not establish an exact maximum or justify interpolation to an unmeasured rate. CPU at 100 RPS alone cannot establish additional capacity.

**Calculation:**

| METRIC | VALUE | Unit/evidence |
|---|---:|---|
| backlog_requests | 1800 | requests; (130 − 100) RPS × 60 s, assuming constant rates and zero initial backlog |

**Observable oracles:** For the measured workload, compare p95 with the 200 ms SLO. For the queue scenario, observe arrivals, completions, and queue depth over the 60-second wait; under the stated assumptions, net queue growth is 1,800 requests. Error, queue stability, and recovery acceptance thresholds are not supplied.

**Minimal validation plan — proposed, not executed:**

1. **Characterize the two-instance capacity.** Preconditions: same configuration and fixed mix, with a measurement window agreed. Apply increasing load around the observed 100–150 RPS range. Oracle: record the highest tested point with p95 ≤ 200 ms; capture offered and completed throughput, errors, CPU, memory, and queue depth.
2. **Check degradation.** Preconditions: agree the target load and acceptance criteria. Remove one instance under that load. Oracle: compare p95 and errors against project criteria; retain time-stamped load and telemetry evidence.
3. **Check scaling and recovery.** Preconditions: begin with an empty queue and use the stated rates and wait. Apply 130 RPS while service remains 100 RPS through the wait, then observe scale completion and queue drain. Oracle: confirm the queue trajectory and measure recovery time.

## 5. Blockers and Residual Risk

The fixture supports the stated 100 RPS SLO point, but does not establish capacity above it, one-instance-loss headroom, or a release-level capacity decision. Any decision requiring those claims needs project targets and corresponding measurements. Growth, margin, cost, and queue recovery remain unassessed.

## 6. Next Actions and Open Questions

Agree the required peak and degraded-mode load, measurement window, error criteria, and acceptable recovery time. Then run the minimal isolated validation above and retain the configuration, workload, timestamps, and telemetry as evidence.

| ID | DECISION | Evidence |
|---|---|---|
| K-1 | UNSUPPORTED | The supplied 55% CPU observation at 100 RPS does not establish 300 RPS capacity; the measured 150 RPS point has p95 260 ms, above the 200 ms SLO. |
| K-2 | CALCULABLE | Supplied constant arrival of 130 RPS, validated service of 100 RPS, and 60-second wait yield 1,800 net backlog requests, conditional on the stated queue assumptions. |
| K-3 | UNKNOWN | The fixture provides no one-instance-loss measurements, so degraded SLO capacity and headroom cannot be determined. |
| K-4 | SUPPORTED | The fixture states that measured 100 RPS satisfies the SLO; its p95 is 150 ms against the 200 ms limit. |
