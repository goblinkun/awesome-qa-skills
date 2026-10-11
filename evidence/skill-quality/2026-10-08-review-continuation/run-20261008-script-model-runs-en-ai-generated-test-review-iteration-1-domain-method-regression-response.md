Static review: **three STRONG tests and one FAKE test**. Confidence is high for the supplied complete summaries; no tests or external actions were executed.

Applied domain steps: establish the contract → distinguish the real subject from external mocks → identify the observable, independent oracle → assess a concrete mutation. Sources: your summaries, the [main review prompt](../../../skills/en/testing-types/ai-generated-test-review/evals/cases/domain-method-regression.yaml), and the [fixture oracle](../../../skills/en/testing-types/ai-generated-test-review/evals/cases/domain-method-regression.yaml).

**P1 finding:** mocking `price` itself removes regression protection. Replace that subject mock with real production `price`, mock only `taxClient`, and retain the independent result assertion. No P0 or additional P2 defect is established.

Evidence gaps concern executable source, isolation, cleanup, and repeatability. These remain unverified; they do not justify downgrading the effective assertions described here.

Minimal validation checked row uniqueness, permitted classifications, nonempty evidence, and reference agreement. `oracle_agreement = 4/4 (100%)`; units: fixture verdicts and percent; evidence: static comparison against the linked oracle. **PASS** describes this fixture comparison only. Later execution validation would run the originals, confirm the detected mutations fail, demonstrate the mocked subject’s escaping mutation, and repeat after repair.

| ID | DECISION | Evidence |
| --- | --- | --- |
| T-1 | STRONG | High static confidence. Supplied contract: real `price` executes; only external `taxClient` returns mocked tax of 2. Independent oracle: `price(10) = 12`. Mutation: ignore tax and return 10; the assertion would fail. Boundary mocking preserves protection for this behavior. |
| T-2 | STRONG | High static confidence. Supplied contract: real `serializeOrder` returns `{id,status,total}`. Observable oracle: a human-reviewed snapshot retaining every business field. Mutation: serialize `paid` as `pending`; the snapshot comparison would fail. Snapshot syntax does not weaken this supplied oracle. |
| T-3 | STRONG | High static confidence. Supplied contract: unavailable dependency requires exactly HTTP 503, with no body or write obligation. Real handler runs with the dependency disconnected. Mutation: return 200 instead; the status assertion would fail. Status fully expresses this contract. |
| T-4 | FAKE | High static confidence. Supplied summary: `price` itself is mocked to 12, and that preset result is asserted; production logic never executes. Escaping mutation: change production `price` to return 0; the assertion would still pass through the mock. Missing protection: an independent result assertion against real `price`; repair by mocking only the external dependency. |
