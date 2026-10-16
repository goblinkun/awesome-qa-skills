### 1. Task Understanding

Deliver a **four-hour performance test runbook** for the highest-impact user journeys. SQL injection and weak-password checks belong to **security testing** and require a separate scope.

This is an executable first draft; no tests or scans were run. The system, traffic, tooling, and SLA were not supplied, so the parameters below must be filled before execution.

### 2. Performance Risks and Priorities

| Priority | Focus | Risk to investigate |
|---|---|---|
| P0 | Most business-critical transaction | Failed or slow completion under expected peak traffic |
| P0 | Highest-volume transaction | Queue growth, connection exhaustion, throughput shortfall |
| P1 | Most expensive transaction, if different | Database contention, CPU or memory saturation |
| P1 | Sudden traffic increase | Timeouts and failure to recover |

Select actual transactions from existing usage evidence. Do not invent endpoints or equally weight every journey.

**Security testing boundary:**

- **SQL injection:** assess whether untrusted input can alter database queries, bypass authorization, or expose data.
- **Weak passwords:** assess password policy, default credentials, and resistance to password guessing using separately authorized methods and accounts.
- Normal login throughput and authentication latency are performance concerns. Password guessing and injection payloads are security checks.
- Keep security scans out of performance measurement windows; they change the workload and make results harder to interpret.

The half-day scope includes a security handoff, not a completed security assessment.

### 3. Recommended Test Types

Run **baseline, expected-peak load, and a short spike/recovery test**.

Defer stress-to-failure, sustained endurance, and capacity certification. A half-day run cannot establish long-term stability or maximum sustainable capacity.

### 4. Scenario Plan

Before running, bind these parameters:

| Parameter | Required value |
|---|---|
| `TARGET` | Isolated nonproduction environment |
| `T1–T3` | Selected transactions with business-success assertions |
| `P` | Expected peak arrival rate, requests or journeys/second |
| `MIX` | Transaction proportions totaling 100% |
| `DATA` | Sufficient valid test accounts and representative records |
| `LIMITS` | Latency, error, recovery, and environment stop thresholds |

Use recorded traffic where available. If unavailable, label `P` and `MIX` as exploratory assumptions; results cannot demonstrate production readiness.

| Time | Activity | Execution |
|---|---|---|
| 0–30 min | Scope and security handoff | Fill parameters; identify owners, environment limits, and security backlog |
| 30–75 min | Prepare and validate | Configure the existing load tool; verify each journey with one user, business assertions, telemetry, and data |
| 75–95 min | Baseline | 5-minute warm-up, 10-minute low-load measurement, 5-minute settle |
| 95–140 min | Load | Ramp to `0.5P` for 5 minutes; hold 10; ramp to `P` for 5; hold 20; settle 5 |
| 140–165 min | Spike/recovery | Hold `P` for 5 minutes; spike to `1.5P` for 5; return to `P` for 10; settle 5 |
| 165–200 min | Investigate and repeat | Repeat the most informative failed or uncertain stage with identical workload and data conditions |
| 200–240 min | Report | Summarize evidence, limitations, bottleneck candidates, and security handoff |

`1.5P` is a **provisional spike assumption**, subject to environment limits. Skip the spike if peak load already breaches stop criteria.

Use an arrival-rate workload when supported. For user-based workloads, derive concurrency from journey duration plus realistic think time; record achieved traffic rather than assuming configured users equal throughput.

### 5. Metrics and Exit Criteria

Capture per transaction:

- p50/p95/p99 latency, achieved throughput, errors, timeouts, and business-success rate.
- CPU, memory, restarts, connection pools, queues, database latency, locks, and slow queries.
- Load-generator utilization and dropped or delayed arrivals.

Use existing SLAs first. If none exist, these are **provisional triage thresholds**, not release acceptance:

- Business-success rate ≥99%.
- Peak-load p95 ≤2× low-load baseline for each transaction.
- Achieved throughput ≥95% of requested traffic.
- No continuously growing queue, exhausted pool, or service restart.
- Latency and queues recover within 5 minutes after the spike.

Stop on data corruption or unexpected environment impact. Also provisionally stop if failures exceed 5% for 2 consecutive minutes or an agreed resource limit is breached.

### 6. Execution Notes

Use representative synthetic data, distinct accounts where required, production-like configuration, synchronized timestamps, and existing monitoring. Record build, infrastructure sizing, cache state, workload, and deviations.

Report each scenario as **pass, fail, or inconclusive**. Missing telemetry, generator saturation, or unrepresentative infrastructure makes the affected conclusion inconclusive. Support bottleneck findings with correlated measurements; latency alone does not establish a database root cause.

The final deliverable is the workload configuration, run results, metric exports, prioritized findings, and a separate security-testing scope for SQL injection and weak-password assessment.
