```json
{"execution_status":"NOT_RUN"}
```

Created [perf/options.json](../../../skills/en/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml) and [perf/scripts/order.js](../../../skills/en/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml). JSON and JavaScript syntax checks passed; no load was run. `API_TOKEN` is sent as a Bearer <redacted>

The script’s `check()` calls record the status and response assertions; the `checks` threshold makes any failed assertion fail the run. The arrival-rate setting schedules 100 iterations per second, but that alone does not prove the target was achieved. Confirm actual request rate and dropped iterations from a run’s results.
