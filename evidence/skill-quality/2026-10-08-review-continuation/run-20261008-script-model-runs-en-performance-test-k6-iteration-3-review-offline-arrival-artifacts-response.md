{"execution_status":"NOT_RUN"}

Created [options.json](../../../skills/en/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml) and [order.js](../../../skills/en/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml). JSON and JavaScript syntax checks passed; no load test was run.

The script records the status and response contract assertions with `check()`. The `checks: ["rate==1"]` threshold makes any failed assertion fail the run. The scenario schedules 100 iterations per second, with one POST per iteration. Zero dropped iterations does not establish the achieved request rate or performance results; those remain unmeasured.
