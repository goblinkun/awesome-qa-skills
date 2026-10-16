### 1. Task Understanding

**Draft plan using the performance-testing skill.** Confirmed scope: points redemption. No SLA, traffic history, architecture, or environment details are available.

Objectives: measure redemption latency and throughput, find saturation and recovery behavior, and verify that concurrent requests preserve balances and redemption outcomes.

**All numeric workloads, durations, and thresholds below are assumptions for initial testing, not agreed acceptance criteria.** This plan does not establish production readiness.

### 2. Performance Risks and Priorities

| Priority | Risk | What to verify |
|---|---|---|
| Critical | Concurrent redemptions overspend a balance | Successful redemptions remain consistent with available points |
| Critical | Retries or duplicate submissions deduct points twice | Confirm the retry contract; verify each logical redemption has the intended single effect |
| Critical | Failure leaves inconsistent state | Reconcile balances, deductions, and redemption records after timeouts and partial failures |
| High | Contention on popular rewards or shared accounts | Compare distributed traffic with concentrated traffic; check inventory if supported |
| High | Slow dependencies exhaust resources | Measure timeout handling, resource saturation, and recovery |
| Medium | Sustained traffic causes degradation | Track latency drift, memory growth, connection usage, and backlog |

These are risks to investigate, not confirmed defects or architectural facts.

### 3. Recommended Test Types

| Type | Purpose | Assumed initial profile |
|---|---|---|
| Baseline | Establish low-load behavior and validate measurements | 1 redemption attempt/second for 10 minutes |
| Load | Measure steady-state performance | 10, 25, then 50 attempts/second; 15 minutes per stage |
| Stress | Find the saturation point and failure behavior | Increase offered rate by 25% per stage until a stop condition |
| Spike | Test abrupt demand and recovery | Jump from 10 to 100 attempts/second for 2 minutes, then return to baseline |
| Endurance | Detect accumulated degradation | 4 hours at the highest stable load-test rate |
| Capacity | Identify sustainable throughput under provisional criteria | Refine the boundary between the highest passing and first failing rates |

Run baseline and load first. Use their findings to adjust later profiles.

### 4. Scenario Plan

- **Ordinary redemption:** unique accounts and logical requests, sufficient balances, varied rewards where supported.
- **Concentrated demand:** repeat the workload against a popular reward; separately exercise concurrent requests against shared accounts.
- **Duplicates and retries:** repeat a logical request during concurrent submission and after an ambiguous timeout. Use the system’s documented identity and retry mechanism.
- **Business rejection:** exercise insufficient points and unavailable rewards, where supported. Verify rejection latency and absence of unintended deductions.
- **Dependency degradation:** in an isolated environment, introduce supported delay or failure injection; observe timeouts, backlog, and recovery.

**Assumed starting mix:** 80% ordinary attempts, 10% duplicates/retries, and 10% business rejections. Run contention and dependency scenarios separately so their effects are attributable.

Use an arrival-rate workload: count logical redemption arrivals separately from retries and downstream requests. Measure actual concurrency and generator shortfalls; do not equate users with requests per second.

### 5. Metrics and Exit Criteria

Collect offered and achieved throughput; p50/p95/p99 latency; technical errors; business rejections; timeouts; retries; and redemption completion time. If processing is asynchronous, measure acceptance and final completion separately.

Observe CPU, memory, connections, database waits, and queues where those components exist.

**Provisional numeric targets—assumptions:**

- Synchronous redemption p95 ≤ 1 second and p99 ≤ 2 seconds.
- Unexpected technical failures ≤ 0.1% of attempts; report expected business rejections separately.
- Achieved logical throughput ≥ 95% of offered throughput.
- After a spike, baseline latency and backlog recover within 5 minutes.

Proposed correctness gates: no duplicate deductions, unauthorized overspending, or unreconciled redemption outcomes. Confirm these against the business rules.

Report each profile’s results and the first limiting resource. A threshold breach identifies a boundary for investigation; it does not prove a root cause.

### 6. Execution Notes

Use an isolated test environment with representative configuration and synthetic accounts, balances, and rewards. Prepare enough data to avoid accidental depletion during ordinary-load tests. Record configuration, dataset size, dependency behavior, and generator capacity.

Validate scripts at low load, capture a baseline, execute profiles, and reconcile records after each run. Stop on integrity violations, environment health limits, or failure to recover. Preserve measurements and diagnostic evidence.

**Gaps to resolve:**

- Business SLA and release acceptance criteria.
- Normal and peak arrival rates, bursts, retry patterns, and workload mix.
- Redemption flow, synchronous versus asynchronous completion, and duplicate-request contract.
- Balance, inventory, reservation, rollback, and reconciliation rules.
- Architecture, dependency limits, scaling behavior, and observability.
- Test-environment fidelity, data volume, permitted fault injection, and operational stop limits.

Replace assumptions with agreed inputs before formal acceptance. Deliver per-profile results, integrity findings, bottleneck evidence, and capacity conclusions limited to the tested configuration.
