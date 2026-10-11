### 1. Task Understanding and Scope

This is a static comparison of the supplied fixture for sample S, model M1, prompt P2, temperature 0, and seed 7 against the required JSON contract. The table classifies the fixture only; it does not report a real model run.

### 2. Input Audit

- **Known:** The contract requires `decision=APPROVE` and `amount=20`; equivalent wording is allowed for `reason`. Source: the sanitized fixture supplied in this turn.
- **Evidence quality and recency:** The fixture is a direct summary supplied now, but raw outputs and run records are absent.
- **Missing:** Concrete model and prompt versions, tool/data versions, timestamps, and raw outputs. These limit verification beyond the stated conditions.
- **Conflicting or stale:** No conflict is apparent; freshness of the underlying model or prompt versions cannot be assessed.
- **Assumption:** The summaries accurately describe the fixture. Raw outputs would be needed to check that assumption.
- **Out of scope:** External calls or actions and claims about real execution.

### 3. LLM Consistency Analysis and Priorities

The supplied conditions define one comparison group. The model and prompt labels are present, but their concrete versions are not; equal seeds do not establish reproducibility across versions.

The observable structural oracle is valid JSON with the required fields and values. The semantic oracle permits equivalent wording for `reason`. A valid structure without a semantic oracle supports structural assessment only. The supportable numeric variance measure is structural failure count divided by trial count, with both counts measured in outputs; this does not measure overall or semantic quality variance.

### 4. Candidate Validation and Residual Risk

Minimal validation, **not performed**: preserve raw outputs and exact configuration/version records, check each output against the schema and required values, then apply the approved semantic oracle to `reason`. Stop structural acceptance on a missing required field; withhold semantic conclusions when no oracle is available. A repeat-consistency claim also needs the project-defined number of observations under fixed conditions. Residual risk remains because only summaries were supplied.

### 5. Human Decisions

A domain or evaluation owner must supply or approve the missing semantic oracle before semantic correctness can be judged. No risk acceptance or exception is established by this fixture.

| ID | DECISION | Evidence |
| --- | --- | --- |
| L-1 | PASS | Source: supplied fixture; calibration: llm-consistency-testing domain oracle. Observable oracle: required JSON contract and paraphrase-permitted `reason`. The summary reports three valid outputs with `amount=20` and equivalent reasons. Static fixture evidence only; raw outputs are unavailable. Priority P3 for this fixture; broader impact is unassessed. Owner: QA/evaluation. Minimal validation: check the three saved outputs against the schema, values, and reason rubric; close when those records confirm the summary. |
| L-2 | FAIL | Source: supplied fixture; calibration: llm-consistency-testing structural-invariant rule. Observable oracle: required `amount` field. The stated third output omits it. `structural_failure_count = 1 output` (basis: the stated omission violates the required-field check); `trial_denominator = 3 outputs` (basis: the fixture states three outputs). Static fixture comparison only; raw outputs are unavailable. Priority P1 for contract validity; a schema check detects this directly, while downstream impact is unknown. Owner: QA/evaluation. Minimal validation: parse the three saved outputs and stop on a missing required field. |
| L-3 | INSUFFICIENT_EVIDENCE | Source: supplied fixture; calibration: llm-consistency-testing repeat-observation rule. Observable oracle: repeated observations under fixed conditions are needed to support consistency. The fixture describes one output as stable, which cannot establish repeat consistency. Static fixture evidence only. Priority P2 for an unsupported stability claim. Owner: QA/evaluation. Minimal validation: collect the project-defined repeat count under recorded conditions and compare outputs; do not claim stability until then. |
| L-4 | UNKNOWN | Source: supplied fixture; calibration: llm-consistency-testing rule for missing semantic rubrics. Observable oracle: the three structures are valid, but no semantic oracle is supplied. Structural validity therefore cannot determine semantic correctness. Static fixture evidence only. Priority P2 because semantic assessment is blocked; business impact is unknown. Owner: domain/evaluation. Minimal validation: approve a semantic rubric and apply it to the saved outputs; withhold a semantic conclusion while the rubric is absent. |
