**Primary recommendation:** `rag-retrieval-testing` — evaluate query→document relevance and top-k recall within AI Native QA.

**Optional supporting skill:** none.

**Why this fits:**

- Labeled query→document relevance provides retrieval ground truth.
- Top-k recall evidence directly concerns retrieval coverage.
- No answer text is supplied, so answer-quality judgment lacks evidence.

The [routing prompt](../../../skills/en/testing-workflows/discover-testing/prompts/discover-testing.md) prioritizes this explicit specialty over broader Composition routes.

**Next step and evidence gaps:** Prepare a handoff containing relevance labels and top-k recall evidence. Clarify k, corpus version, metric definition, aggregation, and acceptance thresholds. Target installation remains unknown; verify availability before any future invocation. Expected output is a retrieval evaluation with evidence limitations.

**Minimal validation:** PASS for static fixture comparison: the selected ID matches the supplied enum and unique catalog entry. Real testing: NOT_RUN. No external actions performed.

| ID | DECISION | Evidence |
| --- | --- | --- |
| ROUTE | rag-retrieval-testing | Availability `UNKNOWN`: the [catalog entry](../../../skills/en/testing-workflows/discover-testing/references/skill-capability-inventory.json) identifies the capability but provides no installation or callability evidence. |
