<div align="right"><a href="./2026-10-06-all-skills-review.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Review and recommendations for every Skill

Use this review to plan the next optimization round: start with reproduced defects, then read the 164 pair-by-pair recommendations. This is a review and proposal; fixes have not been implemented.

## Scope and conclusion

- Date: 2026-10-06. Reviewed the current working tree at Git HEAD `c61f507f61711c3c0f0d1777136a5a4ff0e211b3`. Existing uncommitted changes are part of the reviewed state; HEAD alone does not identify all reviewed content.
- Scope: **164 canonical Skills and 328 language directories** under `skills/zh/` and `skills/en/`: 5 Skill Engineering pairs, 10 workflow pairs, and 149 testing-type pairs. Evidence packages, fixtures, and `legacy-prompts/` are not active Skills in this count.
- Inspected each pair's entry, main prompt, agent metadata, evaluation configuration and cases, and checked bilingual structure and key constraints. Supplementary scripts were grouped by repeated implementation and risky paths reproduced offline; long examples and other resources were sampled as needed.
- Entries and prompts total 45,974 lines. This review did not execute every example, target framework, or model evaluation.
- Maintenance priorities: **71 P1 pairs and 93 P2 pairs**. P1 includes reproduced script defects, contract/routing issues, and clear domain-procedure gaps. These are not 71 proven runtime failures or a release-gate decision. Shared Excel defects raise affected-package priority; other recommendations retain their original level.

Structural governance is strong: language pairing, canonical names, metadata, standalone resource links, and evaluation configuration passed the static checks. The main opportunities concern input fidelity, generated-output correctness, domain procedures, and behavior evaluation.

## Reproduced defects to address first

### A. Lossy input parsing (P1)

| Component | Minimal input | Actual offline result | Repair validation |
| --- | --- | --- | --- |
| `parse_api_sources.py` in four API tool Skills | `curl 'https://example.test/orders' --data '{"qty":1}'` | GET `/orders` | Preserve implicit POST, explicit methods, bodies and parameters; report missing dependencies instead of silently returning no endpoints. |
| Same parsers | Postman URL `{{baseUrl}}/orders` | path `/`; Bruno becomes `/{{baseUrl}}/orders` | Separate base URL and resource path while preserving variables and unknowns. |
| `requirements-analysis-plus/common_parser.py` | `user_id >= -1; retry-count > 3; REQ-001` | `user id = 1; retry count 3; REQ 001` | Preserve identifiers, signs, operators, and rule IDs. |
| Excel parsers in 24 pairs | inlineStr A1=`REQ-1`, empty B1, C1=`42` | All lose `REQ-1`; the basic parser also produces `["", "42"]`, losing column position | Test inlineStr/sharedStrings, sparse columns, empty cells, multiple worksheets, and declared limitations. |

Without another method option, that curl input uses POST, as documented in the [official curl manual](https://curl.se/docs/manpage.html#-d). Destructive Markdown stripping was confirmed only in this `requirements-analysis-plus` implementation; the other three Plus Markdown parsers already preserve these characters.

The four API Skills are `api-test-bruno`, `api-test-pytest`, `api-test-restassure`, and `api-test-supertest`. The WSDL parser also invents `/soap/CreateOrder` from an operation name. Preserve the service address and SOAP operation/action instead of converting the operation into a REST path. These checks exercised conversion logic without calling an API.

Affected Excel pairs:

`accessibility-testing`, `ai-assisted-testing`, `api-testing`, `automation-testing`, `bug-reporting`, `code-review`, `daily-testing-workflow`, `discover-testing`, `functional-testing`, `manual-testing`, `mobile-testing`, `performance-testing`, `release-testing-workflow`, `requirements-analysis`, `requirements-analysis-plus`, `security-testing`, `sprint-testing-workflow`, `test-case-reviewer`, `test-case-reviewer-plus`, `test-case-writing`, `test-reporting`, `test-strategy`, `test-strategy-plus`, `testcase-writer-plus`.

Each of these 24 Chinese implementations was called separately; each English counterpart is byte-identical. Keep standalone installation: maintain a development-side canonical helper and generate local copies, or check copy consistency. Do not introduce cross-Skill resource dependencies or installation-time script execution.

### B. API artifacts lack meaningful failure detection (P1)

The pytest and REST Assured generators use a nonempty check equivalent to `0 >= 0`, so empty inputs pass. All four generators accept successful responses and several 4xx statuses in one broad allowlist and use fixed empty/sample bodies; some also invent a three-second limit. Missing expectations should yield an explicitly incomplete scaffold, not apparently protective business tests.

The Bruno generator additionally renders `{{baseUrl}}` as `{baseUrl}`, confirmed by an offline `_to_bru` call. The expected interpolation syntax is documented in [Bruno's official documentation](https://docs.usebruno.com/variables/interpolation). After repair, golden-check the generated files and use a minimal service with correct/incorrect responses to verify failure sensitivity. Compilation or successful request transmission is insufficient.

### C. Plus runners invent domain facts (P1)

| Skill | Input | Actual runner result | Recommendation |
| --- | --- | --- | --- |
| `testcase-writer-plus` | Password minimum length of 12 | Promotion/gift/inventory prerequisites, positional P0/P1, vague expectations | Generate sourced scenarios, risk priorities, and observable assertions; preserve unknown data. |
| `test-case-reviewer-plus` | Calculator 1+1=2 | Fixed inventory P0, payment compensation, and T+1/T+2 plans | Produce case-linked findings, allow no findings for correct input, and preserve the pending-human-decision contract. |
| `test-strategy-plus` | Calculator-only requirement | Promotion/inventory scope, gateway/cache/queue topology, and a 95% P1 gate | Use supplied facts only and retain unknown scope, topology, and gates. |

The prompts have stronger provenance/conflict/authority contracts than the runners. Decide whether each runner is an actual capability or a demonstration, then align invocation guidance and output labels. Demonstrations must not present fixed templates as semantic analysis. `requirements-analysis-plus/run_analysis.py` should also distinguish keyword extraction from full multi-source analysis.

See the [offline reproduction evidence](./2026-10-06-all-skills-review-evidence.json). These are local helper reproductions, not model, target-tool, or production acceptance results.

## Cross-Skill improvements

1. **Add concrete domain procedures.** Forty-two specialty pairs have stronger generic input/evidence auditing than domain algorithms, decision rules, and oracles. The individual recommendations identify useful matrices, state machines, or boundaries. Add one minimal procedure and a correct/incorrect example pair before expanding references.
2. **Evaluate task results.** There are 1,128 case configurations: 904 rule-based judges, 210 agent judges, and 14 script judges. Of 164 pairs, 138 have only three cases per language. Counts and judge types are not defects by themselves, but several success cases lack actual review material or only check headings/keywords. Add concrete fixtures, sound controls, and seeded faults; check structure deterministically and calibrate semantic judges. Keep `skill-up` as the execution engine.
3. **Test neighboring routing boundaries.** Use adjacent requests for authentication/authorization, retrieval/answer quality, regression scope/selection, and generation/review. Preserve canonical names and clarify boundaries before considering consolidation. Routing conclusions require observed `skill.selection` or trace-adapter events.
4. **Separate provenance from decisions.** Extend the newer fact/inference/candidate/Human boundaries to validate classification and release Go/No-Go recommendations. Retain unknown, blocked, and unexecuted states.
5. **Improve tooling descriptions and copy maintenance.** Twenty-nine Chinese packages still use English `Use this skill when...` short descriptions; localized, domain-specific wording would improve presentation and selection, without implying a format violation. Select framework versions from project context and provide minimal runnable artifacts and explicit dependency errors. Maintain helper copies through generation or consistency checks while keeping installed packages self-contained.

Keep entries concise, teach concrete procedures with a working example, and load deeper references conditionally, consistent with [official Agent Skills authoring practices](https://agentskills.io/skill-creation/best-practices). Short files are acceptable; the concern is missing procedures that distinguish correct from incorrect results.

## Individual recommendations

Each pair lists both entries, configured case counts, a source location, and targeted recommendations. Shared Excel issues are noted when they raise priority. Configured cases are not model-evaluation passes. Source line numbers refer to the reviewed working-tree snapshot.

## Skill Engineering (5 pairs)

### 001. skill-change-verification

[中文入口](../../skills/zh/skill-engineering/skill-change-verification/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-change-verification/SKILL.md) · **P1 / Contract clarification** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/skill-change-verification.md:9](../../skills/en/skill-engineering/skill-change-verification/prompts/skill-change-verification.md#L9).
- Recommendation and validation: The prompt labels skill-up validate as Evaluation although the entry separates it from runtime evidence. Classify validation as structural/configuration evidence, reserve Evaluation for executed runs and judges, and add a change-to-check decision table. Test a validate-only log versus a real run.

### 002. skill-evaluation

[中文入口](../../skills/zh/skill-engineering/skill-evaluation/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-evaluation/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:5](../../skills/en/skill-engineering/skill-evaluation/evals/cases/basic-success.yaml#L5).
- Recommendation and validation: Evidence and judge boundaries are clear, but the three cases mainly check report shape and missing input. Add comparable/non-comparable run fixtures, missing selection events, and infrastructure timeouts; verify classifications and comparison conclusions.

### 003. skill-prose-review

[中文入口](../../skills/zh/skill-engineering/skill-prose-review/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-prose-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/skill-engineering/skill-prose-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: The success case requests a review without supplying a Skill body. Add a small conflicting package and a correct control, and require concrete locations, impacts, and recommendations instead of checklist repetition.

### 004. skill-prose-trim

[中文入口](../../skills/zh/skill-engineering/skill-prose-trim/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-prose-trim/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:4](../../skills/en/skill-engineering/skill-prose-trim/evals/cases/basic-success.yaml#L4).
- Recommendation and validation: The preservation boundaries are useful, but the success case has no source passage and only checks a word. Add before/after fixtures containing process narration, durable contracts, formal history, and measurement limits; distinguish review from authorized editing.

### 005. skill-quality-review

[中文入口](../../skills/zh/skill-engineering/skill-quality-review/SKILL.md) · [English entry](../../skills/en/skill-engineering/skill-quality-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:5](../../skills/en/skill-engineering/skill-quality-review/evals/cases/basic-success.yaml#L5).
- Recommendation and validation: The package contract is clear, but the success case supplies no actual package. Add valid, missing-prompt, missing bare-path resource, and bilingual-schema fixtures; clarify when package review versus prose review applies.

## Testing types (149 pairs)

### 006. acceptance-criteria-review

[中文入口](../../skills/zh/testing-types/acceptance-criteria-review/SKILL.md) · [English entry](../../skills/en/testing-types/acceptance-criteria-review/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/acceptance-criteria-review.md:3](../../skills/en/testing-types/acceptance-criteria-review/prompts/acceptance-criteria-review.md#L3).
- Recommendation and validation: Distinguish review, proposed rewrites, and missing rules. Test original AC IDs, threshold equality, and duplicate refunds.

### 007. accessibility-testing

[中文入口](../../skills/zh/testing-types/accessibility-testing/SKILL.md) · [English entry](../../skills/en/testing-types/accessibility-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/accessibility-testing.md:24](../../skills/en/testing-types/accessibility-testing/prompts/accessibility-testing.md#L24).
- Recommendation and validation: Record the target WCAG version/level, criterion IDs, and manual versus automated evidence. Test scan success with keyboard failure.
- Shared P1: [Excel parser](../../skills/en/testing-types/accessibility-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 008. agent-failure-recovery-testing

[中文入口](../../skills/zh/testing-types/agent-failure-recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-failure-recovery-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/agent-failure-recovery-testing.md:34](../../skills/en/testing-types/agent-failure-recovery-testing/prompts/agent-failure-recovery-testing.md#L34).
- Recommendation and validation: Add failure-to-recovery state transitions and fixtures for timeout-after-write, partial results, and permanent errors.

### 009. agent-long-running-testing

[中文入口](../../skills/zh/testing-types/agent-long-running-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-long-running-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/agent-long-running-testing.md:34](../../skills/en/testing-types/agent-long-running-testing/prompts/agent-long-running-testing.md#L34).
- Recommendation and validation: Add checkpoint/version and cancellation-race procedures; test resumed work, duplicate submissions, and resource release using traces.

### 010. agent-loop-testing

[中文入口](../../skills/zh/testing-types/agent-loop-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-loop-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/agent-loop-testing.md:34](../../skills/en/testing-types/agent-loop-testing/prompts/agent-loop-testing.md#L34).
- Recommendation and validation: Define progress detection, repeated action/observation handling, and budget precedence; verify stop/escalation decisions from traces.

### 011. agent-memory-testing

[中文入口](../../skills/zh/testing-types/agent-memory-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-memory-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/agent-memory-testing.md:34](../../skills/en/testing-types/agent-memory-testing/prompts/agent-memory-testing.md#L34).
- Recommendation and validation: Test tenant isolation, conflicting preference versions, expiration, and deletion with explicit provenance and retrieval expectations.

### 012. agent-permission-testing

[中文入口](../../skills/zh/testing-types/agent-permission-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-permission-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/agent-permission-testing.md:34](../../skills/en/testing-types/agent-permission-testing/prompts/agent-permission-testing.md#L34).
- Recommendation and validation: Add a principal/tool/resource/action matrix and test revocation, delegation, changed parameters, and zero side effects after denial.

### 013. agent-tool-testing

[中文入口](../../skills/zh/testing-types/agent-tool-testing/SKILL.md) · [English entry](../../skills/en/testing-types/agent-tool-testing/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/agent-tool-testing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use concrete tool schemas and traces to verify argument validity, tool selection, and exactly-once side effects after timeouts.

### 014. ai-agent-testing

[中文入口](../../skills/zh/testing-types/ai-agent-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-agent-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ai-agent-testing.md:42](../../skills/en/testing-types/ai-agent-testing/prompts/ai-agent-testing.md#L42).
- Recommendation and validation: Specify task oracles, trace invariants, repeated-run sampling, and termination classes; test correct answers produced through unauthorized actions.

### 015. ai-assisted-testing

[中文入口](../../skills/zh/testing-types/ai-assisted-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-assisted-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ai-assisted-testing.md:28](../../skills/en/testing-types/ai-assisted-testing/prompts/ai-assisted-testing.md#L28).
- Recommendation and validation: Add sanitized-input and draft/adoption provenance, baseline time/rework measures, and assertions for review responsibilities and acceptance.
- Shared P1: [Excel parser](../../skills/en/testing-types/ai-assisted-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 016. ai-feature-testing

[中文入口](../../skills/zh/testing-types/ai-feature-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-feature-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ai-feature-testing.md:42](../../skills/en/testing-types/ai-feature-testing/prompts/ai-feature-testing.md#L42).
- Recommendation and validation: Add product/language/user slices, labeled rubrics, separate refusal/fallback gates, and model/prompt/data identities; thresholds remain project-supplied.

### 017. ai-generated-test-review

[中文入口](../../skills/zh/testing-types/ai-generated-test-review/SKILL.md) · [English entry](../../skills/en/testing-types/ai-generated-test-review/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 6 / EN 6.

- Source: [prompts/review-test.md:3](../../skills/en/testing-types/ai-generated-test-review/prompts/review-test.md#L3).
- Recommendation and validation: Calibrate false positives using legitimate boundary mocks, meaningful snapshots, and valid status-only checks; align bilingual classifications.

### 018. ai-safety-testing

[中文入口](../../skills/zh/testing-types/ai-safety-testing/SKILL.md) · [English entry](../../skills/en/testing-types/ai-safety-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ai-safety-testing.md:34](../../skills/en/testing-types/ai-safety-testing/prompts/ai-safety-testing.md#L34).
- Recommendation and validation: Map versioned policies to allow/restrict/refuse/escalate decisions and test harmful cases alongside benign controls and over-refusal.

### 019. api-contract-testing

[中文入口](../../skills/zh/testing-types/api-contract-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-contract-testing/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/api-contract-testing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test old/new schemas and old consumers; distinguish schema compatibility, semantic incompatibility, and unknown migration behavior.

### 020. api-design-quality-review

[中文入口](../../skills/zh/testing-types/api-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/api-design-quality-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/api-design-quality-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use OpenAPI diffs and a complete-design control; separate verified design conflicts from missing evidence and consumer migration questions.

### 021. api-error-contract-testing

[中文入口](../../skills/zh/testing-types/api-error-contract-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-error-contract-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-error-contract-testing.md:32](../../skills/en/testing-types/api-error-contract-testing/prompts/api-error-contract-testing.md#L32).
- Recommendation and validation: Add error-specific checks for statuses, codes, fields, correlation IDs, retry semantics, and redaction; test cross-operation inconsistencies.

### 022. api-idempotency-testing

[中文入口](../../skills/zh/testing-types/api-idempotency-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-idempotency-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-idempotency-testing.md:32](../../skills/en/testing-types/api-idempotency-testing/prompts/api-idempotency-testing.md#L32).
- Recommendation and validation: Define same-key payload, concurrency, expiry, and timeout-retry cases; distinguish response reuse from exactly-once business effects.

### 023. api-negative-testing

[中文入口](../../skills/zh/testing-types/api-negative-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-negative-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-negative-testing.md:32](../../skills/en/testing-types/api-negative-testing/prompts/api-negative-testing.md#L32).
- Recommendation and validation: Add source-backed invalid-input classes and valid controls; verify rejection contracts and absence of business side effects without invented statuses.

### 024. api-pagination-testing

[中文入口](../../skills/zh/testing-types/api-pagination-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-pagination-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-pagination-testing.md:32](../../skills/en/testing-types/api-pagination-testing/prompts/api-pagination-testing.md#L32).
- Recommendation and validation: Specify stable ordering, tie-breakers, page edges, cursor behavior, and duplicate/gap oracles using ordered-ID fixtures.

### 025. api-rate-limit-testing

[中文入口](../../skills/zh/testing-types/api-rate-limit-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-rate-limit-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-rate-limit-testing.md:32](../../skills/en/testing-types/api-rate-limit-testing/prompts/api-rate-limit-testing.md#L32).
- Recommendation and validation: Add quota-edge, burst, window-transition, isolation, and recovery procedures; test time-series results and 429/Retry-After behavior.

### 026. api-schema-validation

[中文入口](../../skills/zh/testing-types/api-schema-validation/SKILL.md) · [English entry](../../skills/en/testing-types/api-schema-validation/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-schema-validation.md:32](../../skills/en/testing-types/api-schema-validation/prompts/api-schema-validation.md#L32).
- Recommendation and validation: Identify schema dialect/version and verify required/null, extra properties, composition, and references using valid/invalid sample pairs.

### 027. api-security-testing

[中文入口](../../skills/zh/testing-types/api-security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-security-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-security-testing.md:31](../../skills/en/testing-types/api-security-testing/prompts/api-security-testing.md#L31).
- Recommendation and validation: Add API-specific asset, object/property/function permission, resource-use, and trust-boundary procedures while retaining static review limits.

### 028. api-test-bruno

[中文入口](../../skills/zh/testing-types/api-test-bruno/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-bruno/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/generate_bruno_requests.py:26](../../skills/en/testing-types/api-test-bruno/scripts/generate_bruno_requests.py#L26).
- Recommendation and validation: Fix single-brace baseUrl rendering, invented bodies, permissive status assertions, and lossy parsing; verify generated artifacts against golden fixtures.

### 029. api-test-postman

[中文入口](../../skills/zh/testing-types/api-test-postman/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-postman/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/api-test-postman/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Validate collection artifacts, variable scopes, token extraction, and cleanup; test missing expectations rather than checking report words alone.

### 030. api-test-pytest

[中文入口](../../skills/zh/testing-types/api-test-pytest/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-pytest/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/generate_pytest_tests.py:19](../../skills/en/testing-types/api-test-pytest/scripts/generate_pytest_tests.py#L19).
- Recommendation and validation: Replace always-true empty checks and broad status allowlists with contract-derived or explicitly incomplete assertions; test empty and invalid responses.

### 031. api-test-restassure

[中文入口](../../skills/zh/testing-types/api-test-restassure/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-restassure/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/generate_restassured_tests.py:24](../../skills/en/testing-types/api-test-restassure/scripts/generate_restassured_tests.py#L24).
- Recommendation and validation: Use contract-derived status/body assertions, supplied latency limits, and meaningful nonempty checks; validate compilation and failure sensitivity.

### 032. api-test-supertest

[中文入口](../../skills/zh/testing-types/api-test-supertest/SKILL.md) · [English entry](../../skills/en/testing-types/api-test-supertest/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/generate_supertest_tests.py:22](../../skills/en/testing-types/api-test-supertest/scripts/generate_supertest_tests.py#L22).
- Recommendation and validation: Preserve request bodies and expected outcomes, replace broad status acceptance, distinguish app/baseUrl modes, and test failure-sensitive artifacts.

### 033. api-testing

[中文入口](../../skills/zh/testing-types/api-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-testing.md:33](../../skills/en/testing-types/api-testing/prompts/api-testing.md#L33).
- Recommendation and validation: Add protocol-specific branches and cross-request business postconditions/cleanup; test correct statuses with incorrect persisted business state.
- Shared P1: [Excel parser](../../skills/en/testing-types/api-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 034. api-version-compatibility-testing

[中文入口](../../skills/zh/testing-types/api-version-compatibility-testing/SKILL.md) · [English entry](../../skills/en/testing-types/api-version-compatibility-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/api-version-compatibility-testing.md:32](../../skills/en/testing-types/api-version-compatibility-testing/prompts/api-version-compatibility-testing.md#L32).
- Recommendation and validation: Add wire/schema/semantic compatibility and deprecation procedures; test old/new client and server combinations with explicit consumer tolerance.

### 035. authentication-testing

[中文入口](../../skills/zh/testing-types/authentication-testing/SKILL.md) · [English entry](../../skills/en/testing-types/authentication-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/authentication-testing.md:31](../../skills/en/testing-types/authentication-testing/prompts/authentication-testing.md#L31).
- Recommendation and validation: Add credential lifecycle, MFA, recovery, replay, enumeration, and lockout state procedures; distinguish identity authentication from authorization.

### 036. authorization-testing

[中文入口](../../skills/zh/testing-types/authorization-testing/SKILL.md) · [English entry](../../skills/en/testing-types/authorization-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/authorization-testing.md:31](../../skills/en/testing-types/authorization-testing/prompts/authorization-testing.md#L31).
- Recommendation and validation: Add ownership/tenant/delegation permission matrices, horizontal/vertical escalation, revocation, and deny-default checks using paired allow/deny fixtures.

### 037. automation-roi-analysis

[中文入口](../../skills/zh/testing-types/automation-roi-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/automation-roi-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/automation-roi-analysis.md:34](../../skills/en/testing-types/automation-roi-analysis/prompts/automation-roi-analysis.md#L34).
- Recommendation and validation: Add unit/time-window definitions, break-even calculations, and frequency/change-rate sensitivity using reproducible numeric fixtures.

### 038. automation-testing

[中文入口](../../skills/zh/testing-types/automation-testing/SKILL.md) · [English entry](../../skills/en/testing-types/automation-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/automation-testing.md:28](../../skills/en/testing-types/automation-testing/prompts/automation-testing.md#L28).
- Recommendation and validation: Make selection gates, isolation/cleanup, failure signals, and business postconditions explicit; verify evidence-based reasons to defer automation.
- Shared P1: [Excel parser](../../skills/en/testing-types/automation-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 039. boundary-value-testing

[中文入口](../../skills/zh/testing-types/boundary-value-testing/SKILL.md) · [English entry](../../skills/en/testing-types/boundary-value-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/boundary-value-testing.md:32](../../skills/en/testing-types/boundary-value-testing/prompts/boundary-value-testing.md#L32).
- Recommendation and validation: Define inclusive/exclusive boundaries, representable steps, encoding, precision, and time units; test expected neighbors and unknown precision.

### 040. bug-reporting

[中文入口](../../skills/zh/testing-types/bug-reporting/SKILL.md) · [English entry](../../skills/en/testing-types/bug-reporting/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/bug-reporting/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Check expectation sources, minimal reproduction, sanitized evidence, severity versus priority, and preservation of observed frequency.
- Shared P1: [Excel parser](../../skills/en/testing-types/bug-reporting/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 041. business-rule-extraction

[中文入口](../../skills/zh/testing-types/business-rule-extraction/SKILL.md) · [English entry](../../skills/en/testing-types/business-rule-extraction/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/business-rule-extraction/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test tables, exception precedence, and contradictory documents; preserve conditions, actions, scope, and unknown business rules.

### 042. capacity-planning-analysis

[中文入口](../../skills/zh/testing-types/capacity-planning-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/capacity-planning-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 4 / EN 4.

- Source: [prompts/capacity-planning-analysis.md:43](../../skills/en/testing-types/capacity-planning-analysis/prompts/capacity-planning-analysis.md#L43).
- Recommendation and validation: Use reproducible throughput/latency/resource scenarios and scaling-delay/failure headroom; reject capacity extrapolation from CPU percentage alone.

### 043. change-impact-analysis

[中文入口](../../skills/zh/testing-types/change-impact-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/change-impact-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 4 / EN 4.

- Source: [prompts/change-impact-analysis.md:42](../../skills/en/testing-types/change-impact-analysis/prompts/change-impact-analysis.md#L42).
- Recommendation and validation: Add change/dependency/obligation evidence graphs and traversal limits; test unknown dynamic dependencies and conservative validation scope.

### 044. chaos-testing

[中文入口](../../skills/zh/testing-types/chaos-testing/SKILL.md) · [English entry](../../skills/en/testing-types/chaos-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/chaos-testing.md:31](../../skills/en/testing-types/chaos-testing/prompts/chaos-testing.md#L31).
- Recommendation and validation: Add steady-state hypotheses, controls, injection scope, blast radius, measurable abort criteria, and recovery evidence; block incomplete experiment designs.

### 045. ci-test-optimization

[中文入口](../../skills/zh/testing-types/ci-test-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/ci-test-optimization/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ci-test-optimization.md:34](../../skills/en/testing-types/ci-test-optimization/prompts/ci-test-optimization.md#L34).
- Recommendation and validation: Decompose queue/setup/run/retry time, critical paths, and cache validity; test improvements without dropping protection or hiding failures.

### 046. circuit-breaker-testing

[中文入口](../../skills/zh/testing-types/circuit-breaker-testing/SKILL.md) · [English entry](../../skills/en/testing-types/circuit-breaker-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/circuit-breaker-testing.md:31](../../skills/en/testing-types/circuit-breaker-testing/prompts/circuit-breaker-testing.md#L31).
- Recommendation and validation: Define breaker transition windows, thresholds, probe budgets, failed recovery, and concurrent probes; verify event-sequence outcomes.

### 047. code-review

[中文入口](../../skills/zh/testing-types/code-review/SKILL.md) · [English entry](../../skills/en/testing-types/code-review/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 4 / EN 4.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/code-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Add correct patches and apparent-risk cases with visible upstream safeguards to calibrate false positives and valid no-finding outcomes.
- Shared P1: [Excel parser](../../skills/en/testing-types/code-review/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 048. combinatorial-testing

[中文入口](../../skills/zh/testing-types/combinatorial-testing/SKILL.md) · [English entry](../../skills/en/testing-types/combinatorial-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/combinatorial-testing.md:26](../../skills/en/testing-types/combinatorial-testing/prompts/combinatorial-testing.md#L26).
- Recommendation and validation: Add factor/value/constraint modeling, interaction-strength selection, valid-combination generation, and coverage verification on enumerable fixtures.

### 049. cross-browser-testing

[中文入口](../../skills/zh/testing-types/cross-browser-testing/SKILL.md) · [English entry](../../skills/en/testing-types/cross-browser-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/cross-browser-testing.md:32](../../skills/en/testing-types/cross-browser-testing/prompts/cross-browser-testing.md#L32).
- Recommendation and validation: Add risk-selected engine/platform/version matrices and real-device versus emulation evidence; test WebKit-specific support differences.

### 050. database-design-quality-review

[中文入口](../../skills/zh/testing-types/database-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/database-design-quality-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/database-design-quality-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test staged online migrations and mixed-version deployment, including locks, defaults, rollback, and access patterns, with correct-schema controls.

### 051. decision-table-testing

[中文入口](../../skills/zh/testing-types/decision-table-testing/SKILL.md) · [English entry](../../skills/en/testing-types/decision-table-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/decision-table-testing.md:32](../../skills/en/testing-types/decision-table-testing/prompts/decision-table-testing.md#L32).
- Recommendation and validation: Specify condition partitioning, overlap/gap detection, don't-care handling, and precedence; verify an explicit four-combination table.

### 052. dependency-failure-testing

[中文入口](../../skills/zh/testing-types/dependency-failure-testing/SKILL.md) · [English entry](../../skills/en/testing-types/dependency-failure-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/dependency-failure-testing.md:31](../../skills/en/testing-types/dependency-failure-testing/prompts/dependency-failure-testing.md#L31).
- Recommendation and validation: Add synchronous/asynchronous dependency failure matrices for timeout, slowness, errors, and partial success; verify caller state and recovery.

### 053. disaster-recovery-testing

[中文入口](../../skills/zh/testing-types/disaster-recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/disaster-recovery-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/disaster-recovery-testing.md:31](../../skills/en/testing-types/disaster-recovery-testing/prompts/disaster-recovery-testing.md#L31).
- Recommendation and validation: Define RTO/RPO measurements, backup points, dependency restore order, and post-restore consistency using timestamped recovery fixtures.

### 054. distributed-trace-analysis

[中文入口](../../skills/zh/testing-types/distributed-trace-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/distributed-trace-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/distributed-trace-analysis.md:42](../../skills/en/testing-types/distributed-trace-analysis/prompts/distributed-trace-analysis.md#L42).
- Recommendation and validation: Check parent/link relationships, overlapping spans, exclusive time, and queues; test incomplete traces without summing overlaps or inventing root causes.

### 055. edge-case-discovery

[中文入口](../../skills/zh/testing-types/edge-case-discovery/SKILL.md) · [English entry](../../skills/en/testing-types/edge-case-discovery/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/edge-case-discovery/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use deterministic encoding, timezone, and concurrency fixtures with source-linked candidates and controls against unsupported edge-case expansion.

### 056. equivalence-partitioning

[中文入口](../../skills/zh/testing-types/equivalence-partitioning/SKILL.md) · [English entry](../../skills/en/testing-types/equivalence-partitioning/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/equivalence-partitioning.md:32](../../skills/en/testing-types/equivalence-partitioning/prompts/equivalence-partitioning.md#L32).
- Recommendation and validation: Define behavioral equivalence, disjointness/completeness, dependent classes, and representative selection using region/postcode fixtures.

### 057. error-handling-design-review

[中文入口](../../skills/zh/testing-types/error-handling-design-review/SKILL.md) · [English entry](../../skills/en/testing-types/error-handling-design-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/error-handling-design-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test retryable versus permanent failures and timeout-after-commit designs, preserving consumer contracts, compensation, and propagation evidence.

### 058. failover-testing

[中文入口](../../skills/zh/testing-types/failover-testing/SKILL.md) · [English entry](../../skills/en/testing-types/failover-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/failover-testing.md:31](../../skills/en/testing-types/failover-testing/prompts/failover-testing.md#L31).
- Recommendation and validation: Add trigger/detection, routing, fencing, split-brain, timing, and failback procedures; test partition-induced dual writes.

### 059. flaky-test-analysis

[中文入口](../../skills/zh/testing-types/flaky-test-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/flaky-test-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/flaky-test-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use seeded worker/run fixtures, frequency denominators, and controlled experiments; verify accountable, time-bounded quarantine remains visible.

### 060. functional-testing

[中文入口](../../skills/zh/testing-types/functional-testing/SKILL.md) · [English entry](../../skills/en/testing-types/functional-testing/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/parse_formats.py:83](../../skills/en/testing-types/functional-testing/scripts/parse_formats.py#L83).
- Recommendation and validation: Fix inline-string and sparse-column loss in the bundled Excel parser, then test action-to-business-postcondition coverage.
- Shared P1: [Excel parser](../../skills/en/testing-types/functional-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 061. llm-consistency-testing

[中文入口](../../skills/zh/testing-types/llm-consistency-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-consistency-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/llm-consistency-testing.md:34](../../skills/en/testing-types/llm-consistency-testing/prompts/llm-consistency-testing.md#L34).
- Recommendation and validation: Separate structural invariants from allowed semantic variation; control run identity/parameters and test multi-run variance and intermittent failure.

### 062. llm-evaluation-design

[中文入口](../../skills/zh/testing-types/llm-evaluation-design/SKILL.md) · [English entry](../../skills/en/testing-types/llm-evaluation-design/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/llm-evaluation-design/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Add rubric anchors, human disagreement, blinded ordering, contamination controls, dataset slices, and observable judge-calibration steps.

### 063. llm-hallucination-testing

[中文入口](../../skills/zh/testing-types/llm-hallucination-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-hallucination-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/llm-hallucination-testing.md:34](../../skills/en/testing-types/llm-hallucination-testing/prompts/llm-hallucination-testing.md#L34).
- Recommendation and validation: Define supported/contradicted/missing-source/unassessable labels and test claim-level mappings for numbers, entities, and citations.

### 064. llm-testing

[中文入口](../../skills/zh/testing-types/llm-testing/SKILL.md) · [English entry](../../skills/en/testing-types/llm-testing/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/llm-testing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Replace heading-only evaluation with real samples, structural parsers, calibrated semantic rubrics, and repeated robustness/long-context checks.

### 065. log-analysis

[中文入口](../../skills/zh/testing-types/log-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/log-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/log-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Supply actual sanitized logs and deployment times; verify ordering, request correlation, clusters, gaps, and hypothesis-specific validation actions.

### 066. manual-testing

[中文入口](../../skills/zh/testing-types/manual-testing/SKILL.md) · [English entry](../../skills/en/testing-types/manual-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/manual-testing.md:28](../../skills/en/testing-types/manual-testing/prompts/manual-testing.md#L28).
- Recommendation and validation: Add time-boxed charters, data restoration, evidence notes, and unfinished states; test concrete limited-window execution plans.
- Shared P1: [Excel parser](../../skills/en/testing-types/manual-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 067. metamorphic-testing

[中文入口](../../skills/zh/testing-types/metamorphic-testing/SKILL.md) · [English entry](../../skills/en/testing-types/metamorphic-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/metamorphic-testing.md:26](../../skills/en/testing-types/metamorphic-testing/prompts/metamorphic-testing.md#L26).
- Recommendation and validation: Define source input, transformation, output relation, preconditions, and counterexamples; verify justified metamorphic relations on concrete fixtures.

### 068. metrics-anomaly-analysis

[中文入口](../../skills/zh/testing-types/metrics-anomaly-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/metrics-anomaly-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/metrics-anomaly-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use unit-aware seasonal series with missing samples and explicit baseline windows; test dimensions and causal restraint without a baseline.

### 069. mobile-testing

[中文入口](../../skills/zh/testing-types/mobile-testing/SKILL.md) · [English entry](../../skills/en/testing-types/mobile-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/mobile-testing.md:28](../../skills/en/testing-types/mobile-testing/prompts/mobile-testing.md#L28).
- Recommendation and validation: Add risk-selected OS/device/upgrade/network/lifecycle matrices and restoration oracles for deeplink parameters and interrupted payments.
- Shared P1: [Excel parser](../../skills/en/testing-types/mobile-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 070. mock-quality-review

[中文入口](../../skills/zh/testing-types/mock-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/mock-quality-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/mock-quality-review.md:32](../../skills/en/testing-types/mock-quality-review/prompts/mock-quality-review.md#L32).
- Recommendation and validation: Compare contract/stub fields, statuses, timing, error paths, drift, and mocked subject boundaries using legitimate and invalid mock controls.

### 071. model-based-testing

[中文入口](../../skills/zh/testing-types/model-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/model-based-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/model-based-testing.md:26](../../skills/en/testing-types/model-based-testing/prompts/model-based-testing.md#L26).
- Recommendation and validation: Specify states, guards, events, actions, reachability, and coverage objectives; verify derived paths from a small explicit model.

### 072. multi-agent-testing

[中文入口](../../skills/zh/testing-types/multi-agent-testing/SKILL.md) · [English entry](../../skills/en/testing-types/multi-agent-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/multi-agent-testing.md:34](../../skills/en/testing-types/multi-agent-testing/prompts/multi-agent-testing.md#L34).
- Recommendation and validation: Add delegation IDs, ownership, state versions, acknowledgments, and termination rules; test partial failure, duplicate ownership, and stale messages.

### 073. mutation-testing-analysis

[中文入口](../../skills/zh/testing-types/mutation-testing-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/mutation-testing-analysis/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/mutation-testing-analysis.md:32](../../skills/en/testing-types/mutation-testing-analysis/prompts/mutation-testing-analysis.md#L32).
- Recommendation and validation: Classify mutation outcomes and denominators explicitly; preserve operator/test mappings and verify scores without silently excluding unproven equivalents.

### 074. negative-scenario-discovery

[中文入口](../../skills/zh/testing-types/negative-scenario-discovery/SKILL.md) · [English entry](../../skills/en/testing-types/negative-scenario-discovery/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/negative-scenario-discovery/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test timeout-after-success, compound failures, and failed recovery with explicit rejection/restoration/data-consistency expectations.

### 075. observability-design-review

[中文入口](../../skills/zh/testing-types/observability-design-review/SKILL.md) · [English entry](../../skills/en/testing-types/observability-design-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/observability-design-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test high-cardinality labels and sampled trace breaks; require budget, correlation, and actionable alerts rather than keywords.

### 076. pairwise-testing

[中文入口](../../skills/zh/testing-types/pairwise-testing/SKILL.md) · [English entry](../../skills/en/testing-types/pairwise-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/pairwise-testing.md:32](../../skills/en/testing-types/pairwise-testing/prompts/pairwise-testing.md#L32).
- Recommendation and validation: Generate and verify the valid pair universe under constraints, report gaps, and explicitly separate pairwise from higher-order protection.

### 077. performance-bottleneck-analysis

[中文入口](../../skills/zh/testing-types/performance-bottleneck-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-bottleneck-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/performance-bottleneck-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use staged load/resource fixtures and discriminating experiments; verify evidence-backed hypotheses rather than equating utilization with root cause.

### 078. performance-regression-analysis

[中文入口](../../skills/zh/testing-types/performance-regression-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-regression-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/performance-regression-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Assert comparability limits directly and use paired repeated runs for absolute/relative change, noise, and stable degradation.

### 079. performance-result-analysis

[中文入口](../../skills/zh/testing-types/performance-result-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/performance-result-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/performance-result-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Provide actual stage reports and goals; validate achieved load, samples, error denominators, steady state, and bounded conclusions.

### 080. performance-test-gatling

[中文入口](../../skills/zh/testing-types/performance-test-gatling/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-gatling/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/performance-test-gatling.md:106](../../skills/en/testing-types/performance-test-gatling/prompts/performance-test-gatling.md#L106).
- Recommendation and validation: Validate open/closed injection models, achieved arrival rates, DSL/version compatibility, feeder exhaustion, and missing thresholds with offline compilation.

### 081. performance-test-jmeter

[中文入口](../../skills/zh/testing-types/performance-test-jmeter/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-jmeter/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/performance-test-jmeter.md:27](../../skills/en/testing-types/performance-test-jmeter/prompts/performance-test-jmeter.md#L27).
- Recommendation and validation: Explain thread versus arrival-rate models; validate sanitized JMX, timers, distributed constraints, CSV lifecycle, and latency/error gates.

### 082. performance-test-k6

[中文入口](../../skills/zh/testing-types/performance-test-k6/SKILL.md) · [English entry](../../skills/en/testing-types/performance-test-k6/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:16](../../skills/en/testing-types/performance-test-k6/evals/cases/basic-success.yaml#L16).
- Recommendation and validation: Test executor choice, dropped iterations, checks versus thresholds, request-body fidelity, and business postconditions in generated scripts.

### 083. performance-testing

[中文入口](../../skills/zh/testing-types/performance-testing/SKILL.md) · [English entry](../../skills/en/testing-types/performance-testing/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/parse_formats.py:83](../../skills/en/testing-types/performance-testing/scripts/parse_formats.py#L83).
- Recommendation and validation: Fix the shared Excel parsing defect, then test achieved rather than requested load, resource evidence, and error denominators.
- Shared P1: [Excel parser](../../skills/en/testing-types/performance-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 084. performance-workload-modeling

[中文入口](../../skills/zh/testing-types/performance-workload-modeling/SKILL.md) · [English entry](../../skills/en/testing-types/performance-workload-modeling/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 4 / EN 4.

- Source: [prompts/performance-workload-modeling.md:43](../../skills/en/testing-types/performance-workload-modeling/prompts/performance-workload-modeling.md#L43).
- Recommendation and validation: Add reproducible unit/window/mix/session conversions; do not infer peak RPS from daily totals without a peak-window duration.

### 085. pr-test-impact-analysis

[中文入口](../../skills/zh/testing-types/pr-test-impact-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/pr-test-impact-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/pr-test-impact-analysis.md:43](../../skills/en/testing-types/pr-test-impact-analysis/prompts/pr-test-impact-analysis.md#L43).
- Recommendation and validation: Record base/head and symbol/dependency/test mappings, removed-test impact, and conservative fallbacks for unknown mappings.

### 086. production-incident-analysis

[中文入口](../../skills/zh/testing-types/production-incident-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/production-incident-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/production-incident-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use timestamped incident/change/mitigation fixtures and distinguish symptoms, associations, root causes, proposed actions, and executed actions.

### 087. production-verification

[中文入口](../../skills/zh/testing-types/production-verification/SKILL.md) · [English entry](../../skills/en/testing-types/production-verification/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/production-verification/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test read-only mode, approved writes, canary thresholds, cleanup failures, and per-step side effects; distinguish plans from observed outcomes.

### 088. prompt-injection-testing

[中文入口](../../skills/zh/testing-types/prompt-injection-testing/SKILL.md) · [English entry](../../skills/en/testing-types/prompt-injection-testing/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/prompt-injection-testing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use benign-canary untrusted documents, tool traces, and normal-document controls to verify trust boundaries and unauthorized-call absence.

### 089. prompt-testing

[中文入口](../../skills/zh/testing-types/prompt-testing/SKILL.md) · [English entry](../../skills/en/testing-types/prompt-testing/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 6 / EN 6.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/prompt-testing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use paired before/after outputs with identities, structural parsers, calibrated semantics, and valid paraphrase controls for regression decisions.

### 090. property-based-testing

[中文入口](../../skills/zh/testing-types/property-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/property-based-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/property-based-testing.md:26](../../skills/en/testing-types/property-based-testing/prompts/property-based-testing.md#L26).
- Recommendation and validation: Specify generators, justified invariants, preconditions, seeds, shrinking, and minimal counterexamples; verify sorting and multiset preservation.

### 091. quality-dashboard-design

[中文入口](../../skills/zh/testing-types/quality-dashboard-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-dashboard-design/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-dashboard-design.md:34](../../skills/en/testing-types/quality-dashboard-design/prompts/quality-dashboard-design.md#L34).
- Recommendation and validation: Map decisions to metric/source/action panels and distinguish stale/missing/unexecuted data from zero; test misleading green summaries and minority P0 risks.

### 092. quality-debt-analysis

[中文入口](../../skills/zh/testing-types/quality-debt-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/quality-debt-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-debt-analysis.md:34](../../skills/en/testing-types/quality-debt-analysis/prompts/quality-debt-analysis.md#L34).
- Recommendation and validation: Separate debt from live product defects, document risk accumulation and repayment evidence, and test age versus impact prioritization.

### 093. quality-gate-design

[中文入口](../../skills/zh/testing-types/quality-gate-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-gate-design/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-gate-design.md:34](../../skills/en/testing-types/quality-gate-design/prompts/quality-gate-design.md#L34).
- Recommendation and validation: Define gate state tables, evidence freshness, authorized expiring exceptions, and fail-closed rules; test missing execution evidence.

### 094. quality-maturity-assessment

[中文入口](../../skills/zh/testing-types/quality-maturity-assessment/SKILL.md) · [English entry](../../skills/en/testing-types/quality-maturity-assessment/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-maturity-assessment.md:34](../../skills/en/testing-types/quality-maturity-assessment/prompts/quality-maturity-assessment.md#L34).
- Recommendation and validation: Add observable maturity anchors and unknown/not-applicable handling using evidence-paired fixtures; keep repository Quality Score separate.

### 095. quality-metrics-design

[中文入口](../../skills/zh/testing-types/quality-metrics-design/SKILL.md) · [English entry](../../skills/en/testing-types/quality-metrics-design/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-metrics-design.md:34](../../skills/en/testing-types/quality-metrics-design/prompts/quality-metrics-design.md#L34).
- Recommendation and validation: Provide metric dictionaries, windows, deduplication, exclusions, missingness, and lineage; recalculate reopened-defect and repeated-run fixtures.

### 096. quality-productivity-metrics

[中文入口](../../skills/zh/testing-types/quality-productivity-metrics/SKILL.md) · [English entry](../../skills/en/testing-types/quality-productivity-metrics/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/quality-productivity-metrics.md:34](../../skills/en/testing-types/quality-productivity-metrics/prompts/quality-productivity-metrics.md#L34).
- Recommendation and validation: Use balanced effort/output/quality/process measures with complexity and unit controls; test rising test counts alongside increased escapes.

### 097. quality-risk-analysis

[中文入口](../../skills/zh/testing-types/quality-risk-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/quality-risk-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 4 / EN 4.

- Source: [prompts/quality-risk-analysis.md:43](../../skills/en/testing-types/quality-risk-analysis/prompts/quality-risk-analysis.md#L43).
- Recommendation and validation: Add qualitative risk anchors and uncertainty handling; test rare financial loss versus frequent minor issues without unjustified score products.

### 098. rag-quality-testing

[中文入口](../../skills/zh/testing-types/rag-quality-testing/SKILL.md) · [English entry](../../skills/en/testing-types/rag-quality-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/rag-quality-testing.md:34](../../skills/en/testing-types/rag-quality-testing/prompts/rag-quality-testing.md#L34).
- Recommendation and validation: Map queries/chunks/claims/citations and score completeness/refusal separately; test citations that exist but do not support the answer.

### 099. rag-retrieval-testing

[中文入口](../../skills/zh/testing-types/rag-retrieval-testing/SKILL.md) · [English entry](../../skills/en/testing-types/rag-retrieval-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/rag-retrieval-testing.md:34](../../skills/en/testing-types/rag-retrieval-testing/prompts/rag-retrieval-testing.md#L34).
- Recommendation and validation: Define relevance labels, top-k/denominators, filters, permissions, freshness, and ranking controls; distinguish retrieval from generation failures.

### 100. recovery-testing

[中文入口](../../skills/zh/testing-types/recovery-testing/SKILL.md) · [English entry](../../skills/en/testing-types/recovery-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/recovery-testing.md:31](../../skills/en/testing-types/recovery-testing/prompts/recovery-testing.md#L31).
- Recommendation and validation: Distinguish service/data recovery and define timing, recovery points, consistency, and compensation; verify timeline and snapshot evidence.

### 101. regression-optimization

[中文入口](../../skills/zh/testing-types/regression-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/regression-optimization/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/regression-optimization.md:34](../../skills/en/testing-types/regression-optimization/prompts/regression-optimization.md#L34).
- Recommendation and validation: Define risk-preservation constraints and comparable time/miss-risk measures; reject speed gains obtained by removing critical protection.

### 102. regression-scope-analysis

[中文入口](../../skills/zh/testing-types/regression-scope-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/regression-scope-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/regression-scope-analysis.md:43](../../skills/en/testing-types/regression-scope-analysis/prompts/regression-scope-analysis.md#L43).
- Recommendation and validation: Add change-to-obligation, layer/platform, and inclusion/exclusion mappings. Test indirect dependencies and insufficient budgets without treating unknown impact as excluded.

### 103. regression-test-selection

[中文入口](../../skills/zh/testing-types/regression-test-selection/SKILL.md) · [English entry](../../skills/en/testing-types/regression-test-selection/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/regression-test-selection/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Provide actual test IDs, durations, dependencies, and risk mappings. Verify the selected set, mandatory coverage, and the infeasible-budget branch rather than selection principles alone.

### 104. reliability-testing

[中文入口](../../skills/zh/testing-types/reliability-testing/SKILL.md) · [English entry](../../skills/en/testing-types/reliability-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/reliability-testing.md:31](../../skills/en/testing-types/reliability-testing/prompts/reliability-testing.md#L31).
- Recommendation and validation: Add concrete reliability procedures: SLI definitions, observation windows, failure denominators, repeated failures, and recovery criteria. Test incompatible denominators and short failure-free windows.

### 105. requirement-ambiguity-analysis

[中文入口](../../skills/zh/testing-types/requirement-ambiguity-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-ambiguity-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/requirement-ambiguity-analysis.md:75](../../skills/en/testing-types/requirement-ambiguity-analysis/prompts/requirement-ambiguity-analysis.md#L75).
- Recommendation and validation: Show competing plausible interpretations, their consequences, and a discriminating question. Add a clear-requirement control and distinguish ambiguity from missing rules or contradictions.

### 106. requirement-conflict-detection

[中文入口](../../skills/zh/testing-types/requirement-conflict-detection/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-conflict-detection/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/requirement-conflict-detection/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test similarly worded rules with different scopes or versions and conflicts involving several rules. Require participating rule IDs and a minimal conflicting set, with uncertainty retained.

### 107. requirement-consistency-analysis

[中文入口](../../skills/zh/testing-types/requirement-consistency-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-consistency-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 6 / EN 6.

- Source: [prompts/requirement-consistency-analysis.md:79](../../skills/en/testing-types/requirement-consistency-analysis/prompts/requirement-consistency-analysis.md#L79).
- Recommendation and validation: Add entity/term, unit, and state mappings. Test equivalent aliases, differing versions, and incompatible units to distinguish aligned, contradicted, and non-comparable statements.

### 108. requirement-gap-analysis

[中文入口](../../skills/zh/testing-types/requirement-gap-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-gap-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/requirement-gap-analysis.md:43](../../skills/en/testing-types/requirement-gap-analysis/prompts/requirement-gap-analysis.md#L43).
- Recommendation and validation: Separate undefined rules, unavailable material, conflicts, and non-applicability. Test a complete requirement and a missing closure condition, requiring sourced gaps and observable closure evidence.

### 109. requirement-quality-review

[中文入口](../../skills/zh/testing-types/requirement-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-quality-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/requirement-quality-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Add a sound requirement control and a fixture with a specific high-risk defect. Verify severity, source passages, and targeted rewrites without requiring findings for every input.

### 110. requirement-traceability-analysis

[中文入口](../../skills/zh/testing-types/requirement-traceability-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirement-traceability-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 6 / EN 6.

- Source: [prompts/requirement-traceability-analysis.md:76](../../skills/en/testing-types/requirement-traceability-analysis/prompts/requirement-traceability-analysis.md#L76).
- Recommendation and validation: Use typed traceability edges and distinguish mapped, executed, and satisfied obligations. Test many-to-many links, outdated mappings, duplicate IDs, and coverage calculations on a small graph.

### 111. requirements-analysis

[中文入口](../../skills/zh/testing-types/requirements-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/requirements-analysis/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 4 / EN 4.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/requirements-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Add concrete rule/state fixtures and verify source-linked test points, unknown rules, and useful questions. Include a complete-input control that must not gain invented gaps.
- Shared P1: [Excel parser](../../skills/en/testing-types/requirements-analysis/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 112. requirements-analysis-plus

[中文入口](../../skills/zh/testing-types/requirements-analysis-plus/SKILL.md) · [English entry](../../skills/en/testing-types/requirements-analysis-plus/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 4 / EN 4.

- Source: [scripts/common_parser.py:66](../../skills/en/testing-types/requirements-analysis-plus/scripts/common_parser.py#L66).
- Recommendation and validation: Repair destructive Markdown parsing and distinguish keyword extraction from semantic multi-source analysis. Test numeric rules, conflicting roles, and unrelated domains without invented requirements.
- Shared P1: [Excel parser](../../skills/en/testing-types/requirements-analysis-plus/scripts/common_parser.py#L89) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 113. resilience-testing

[中文入口](../../skills/zh/testing-types/resilience-testing/SKILL.md) · [English entry](../../skills/en/testing-types/resilience-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/resilience-testing.md:31](../../skills/en/testing-types/resilience-testing/prompts/resilience-testing.md#L31).
- Recommendation and validation: Add pre/during/post-disruption invariants, degraded states, and recovery criteria. Test partial dependency failures and failed recovery, clarifying handoffs to reliability and chaos testing.

### 114. retry-testing

[中文入口](../../skills/zh/testing-types/retry-testing/SKILL.md) · [English entry](../../skills/en/testing-types/retry-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/retry-testing.md:31](../../skills/en/testing-types/retry-testing/prompts/retry-testing.md#L31).
- Recommendation and validation: Add retryability, attempt/deadline budgets, backoff, server hints, and side-effect checks. Test timeout-after-write and nested retries using concrete traces.

### 115. risk-based-testing

[中文入口](../../skills/zh/testing-types/risk-based-testing/SKILL.md) · [English entry](../../skills/en/testing-types/risk-based-testing/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/risk-based-testing.md:70](../../skills/en/testing-types/risk-based-testing/prompts/risk-based-testing.md#L70).
- Recommendation and validation: Map each risk to test objectives, depth, minimum evidence, and residual exposure. Use qualitative anchors and a constrained-budget fixture to verify justified priorities and unresolved tradeoffs.

### 116. root-cause-analysis

[中文入口](../../skills/zh/testing-types/root-cause-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/root-cause-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/root-cause-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Add competing hypotheses, counter-evidence, and discriminating experiments. Compare correlation-only and causal-chain fixtures so the final error message is not automatically treated as the root cause.

### 117. secrets-exposure-review

[中文入口](../../skills/zh/testing-types/secrets-exposure-review/SKILL.md) · [English entry](../../skills/en/testing-types/secrets-exposure-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/secrets-exposure-review.md:31](../../skills/en/testing-types/secrets-exposure-review/prompts/secrets-exposure-review.md#L31).
- Recommendation and validation: Add location and credential-lifecycle checks across code, CI, logs, artifacts, and history. Test placeholders and redacted candidates; avoid exposing values or inferring credential validity from a pattern.

### 118. security-requirement-review

[中文入口](../../skills/zh/testing-types/security-requirement-review/SKILL.md) · [English entry](../../skills/en/testing-types/security-requirement-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/security-requirement-review.md:31](../../skills/en/testing-types/security-requirement-review/prompts/security-requirement-review.md#L31).
- Recommendation and validation: Add asset-to-threat, security-obligation, control, and verifiable-acceptance mappings. Test vague and concrete requirements using supplied standards without inventing compliance conclusions.

### 119. security-testing

[中文入口](../../skills/zh/testing-types/security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/security-testing/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/security-testing.md:28](../../skills/en/testing-types/security-testing/prompts/security-testing.md#L28).
- Recommendation and validation: Map threats and controls to tests and evidence, including legitimate-use controls. Distinguish design, execution, and confirmed vulnerabilities; test clean scans with unverified business authorization.
- Shared P1: [Excel parser](../../skills/en/testing-types/security-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 120. session-security-testing

[中文入口](../../skills/zh/testing-types/session-security-testing/SKILL.md) · [English entry](../../skills/en/testing-types/session-security-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/session-security-testing.md:31](../../skills/en/testing-types/session-security-testing/prompts/session-security-testing.md#L31).
- Recommendation and validation: Select lifecycle checks for the supplied cookie/token mechanism: creation, rotation, fixation, expiry, revocation, logout, and concurrent sessions. Test old credentials after logout and permission changes.

### 121. state-transition-testing

[中文入口](../../skills/zh/testing-types/state-transition-testing/SKILL.md) · [English entry](../../skills/en/testing-types/state-transition-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/state-transition-testing.md:32](../../skills/en/testing-types/state-transition-testing/prompts/state-transition-testing.md#L32).
- Recommendation and validation: Add a transition matrix, reachability checks, invalid transitions, guard boundaries, and partial-failure handling. Verify valid and invalid coverage against a small state graph.

### 122. technical-design-quality-review

[中文入口](../../skills/zh/testing-types/technical-design-quality-review/SKILL.md) · [English entry](../../skills/en/testing-types/technical-design-quality-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/technical-design-quality-review/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use concrete component and sequence fixtures to review boundaries, invariants, failure, and recovery. Include a sound design control and partial-commit failure, requiring specific evidence locations.

### 123. test-case-reviewer

[中文入口](../../skills/zh/testing-types/test-case-reviewer/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-reviewer/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/test-case-reviewer/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Provide actual cases and requirements with seeded defects in expectations or prerequisites. Require case-level findings and rewrites, plus a correct control that limits unsupported missing-coverage claims.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-case-reviewer/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 124. test-case-reviewer-plus

[中文入口](../../skills/zh/testing-types/test-case-reviewer-plus/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-reviewer-plus/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 4 / EN 4.

- Source: [scripts/run_review.py:59](../../skills/en/testing-types/test-case-reviewer-plus/scripts/run_review.py#L59).
- Recommendation and validation: The runner invents inventory/payment findings for unrelated inputs and omits the pending-human-decision contract. Replace fixed findings with sourced review or label the runner as a demonstration; test correct and unrelated-domain cases.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-case-reviewer-plus/scripts/common_parser.py#L86) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 125. test-case-writing

[中文入口](../../skills/zh/testing-types/test-case-writing/SKILL.md) · [English entry](../../skills/en/testing-types/test-case-writing/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 4 / EN 4.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/test-case-writing/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Check merge/split rules, ordering, and trace fields structurally. Test conflicting expectations, repeated inputs from four roles, and missing source versions, requiring preserved provenance.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-case-writing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 126. test-code-review

[中文入口](../../skills/zh/testing-types/test-code-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-code-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-code-review.md:32](../../skills/en/testing-types/test-code-review/prompts/test-code-review.md#L32).
- Recommendation and validation: Add assertion failure-sensitivity, subject isolation, mock boundaries, data/concurrency isolation, and cleanup checks. Test swallowed errors, tautological assertions, and sound tests with concrete code findings.

### 127. test-data-generation

[中文入口](../../skills/zh/testing-types/test-data-generation/SKILL.md) · [English entry](../../skills/en/testing-types/test-data-generation/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-data-generation.md:43](../../skills/en/testing-types/test-data-generation/prompts/test-data-generation.md#L43).
- Recommendation and validation: Add schema/relationship-based generation of labeled valid and invalid datasets. Verify uniqueness, foreign keys, state relations, and reproducibility, with artifacts when requested.

### 128. test-data-requirement-analysis

[中文入口](../../skills/zh/testing-types/test-data-requirement-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-data-requirement-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-data-requirement-analysis.md:69](../../skills/en/testing-types/test-data-requirement-analysis/prompts/test-data-requirement-analysis.md#L69).
- Recommendation and validation: Map scenarios to entities, states, relationships, quantity rationale, and acquisition/cleanup conditions. Test missing schemas, cross-entity dependencies, and restricted personal data while preserving unknowns.

### 129. test-effectiveness-analysis

[中文入口](../../skills/zh/testing-types/test-effectiveness-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-effectiveness-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-effectiveness-analysis.md:34](../../skills/en/testing-types/test-effectiveness-analysis/prompts/test-effectiveness-analysis.md#L34).
- Recommendation and validation: Trace faults or obligations through tests and assertions to missed detection. Distinguish historical escapes from controlled fault seeding, and test high pass rates with known misses and explicit denominators.

### 130. test-gap-analysis

[中文入口](../../skills/zh/testing-types/test-gap-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-gap-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/test-gap-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Test mapped-but-unexecuted, executed-but-unsatisfied, unavailable mapping evidence, and non-applicability. Verify gap classifications and closure evidence rather than deriving coverage from item counts.

### 131. test-maintenance-cost-analysis

[中文入口](../../skills/zh/testing-types/test-maintenance-cost-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-maintenance-cost-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-maintenance-cost-analysis.md:34](../../skills/en/testing-types/test-maintenance-cost-analysis/prompts/test-maintenance-cost-analysis.md#L34).
- Recommendation and validation: Break down maintenance by product change, test defects, infrastructure, data, and duplication. Include sample windows and uncertainty; test equal totals with different causes and avoid individual-performance inferences.

### 132. test-report-review

[中文入口](../../skills/zh/testing-types/test-report-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-report-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 5 / EN 5.

- Source: [evals/cases/basic-conditional-pass.yaml:6](../../skills/en/testing-types/test-report-review/evals/cases/basic-conditional-pass.yaml#L6).
- Recommendation and validation: Add case-level statistics with skipped, blocked, and rerun outcomes, build mismatches, and controlled conditions. Verify denominators and recommendation states with a fully consistent report control.

### 133. test-reporting

[中文入口](../../skills/zh/testing-types/test-reporting/SKILL.md) · [English entry](../../skills/en/testing-types/test-reporting/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 4 / EN 4.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/test-reporting/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use raw execution and defect rows to verify planned/executed/outcome totals and rerun rules. Preserve unknown counts instead of deriving them from a summary alone.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-reporting/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 134. test-runtime-optimization

[中文入口](../../skills/zh/testing-types/test-runtime-optimization/SKILL.md) · [English entry](../../skills/en/testing-types/test-runtime-optimization/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-runtime-optimization.md:34](../../skills/en/testing-types/test-runtime-optimization/prompts/test-runtime-optimization.md#L34).
- Recommendation and validation: Add critical-path, setup/teardown, resource-limit, and cold/warm-cache analysis. Compare equivalent baseline/candidate runs and verify retained fault detection as well as duration.

### 135. test-scope-analysis

[中文入口](../../skills/zh/testing-types/test-scope-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-scope-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-scope-analysis.md:58](../../skills/en/testing-types/test-scope-analysis/prompts/test-scope-analysis.md#L58).
- Recommendation and validation: Define scope units across version, layer, platform, and data states with inclusion/exclusion rationale and change triggers. Test undefined boundaries and new requirements; clarify the regression-specific handoff.

### 136. test-strategy

[中文入口](../../skills/zh/testing-types/test-strategy/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy/SKILL.md) · **P1 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-strategy.md:28](../../skills/en/testing-types/test-strategy/prompts/test-strategy.md#L28).
- Recommendation and validation: Connect objectives, scope, depth, capacity, gates, evidence, and owners in an executable plan. Test differing capacity constraints and unresolved risks without imposing arbitrary pass-rate thresholds.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-strategy/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 137. test-strategy-plus

[中文入口](../../skills/zh/testing-types/test-strategy-plus/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy-plus/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 4 / EN 4.

- Source: [scripts/run_strategy.py:56](../../skills/en/testing-types/test-strategy-plus/scripts/run_strategy.py#L56).
- Recommendation and validation: The runner invents promotion scope, infrastructure, and a 95% P1 gate for a calculator requirement. Generate only from supplied facts or label demonstration output; test three unrelated domains and retained unknowns.
- Shared P1: [Excel parser](../../skills/en/testing-types/test-strategy-plus/scripts/common_parser.py#L86) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 138. test-strategy-review

[中文入口](../../skills/zh/testing-types/test-strategy-review/SKILL.md) · [English entry](../../skills/en/testing-types/test-strategy-review/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 5 / EN 5.

- Source: [evals/cases/basic-conditional-pass.yaml:6](../../skills/en/testing-types/test-strategy-review/evals/cases/basic-conditional-pass.yaml#L6).
- Recommendation and validation: Add an acceptable strategy control and fixtures with dependency, responsibility, and gate conflicts. Verify blocker/condition classification and closure evidence without turning every improvement into rejection.

### 139. test-suite-health-analysis

[中文入口](../../skills/zh/testing-types/test-suite-health-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/test-suite-health-analysis/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/test-suite-health-analysis.md:32](../../skills/en/testing-types/test-suite-health-analysis/prompts/test-suite-health-analysis.md#L32).
- Recommendation and validation: Add test/run identities, failure taxonomy, retry/quarantine behavior, redundant coverage, duration trends, and protected obligations. Test retry-heavy green runs without inventing an ungrounded health score.

### 140. testability-analysis

[中文入口](../../skills/zh/testing-types/testability-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/testability-analysis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 6 / EN 6.

- Source: [evals/cases/basic-success.yaml:6](../../skills/en/testing-types/testability-analysis/evals/cases/basic-success.yaml#L6).
- Recommendation and validation: Use actual design/interface fixtures to verify minimal safe observability seams, time/randomness control, and dependency substitutes. Include an existing-seam control to avoid blanket debug-backdoor recommendations.

### 141. testcase-writer-plus

[中文入口](../../skills/zh/testing-types/testcase-writer-plus/SKILL.md) · [English entry](../../skills/en/testing-types/testcase-writer-plus/SKILL.md) · **P1 / Code correctness** · Configured cases: ZH 3 / EN 3.

- Source: [scripts/run_writer.py:48](../../skills/en/testing-types/testcase-writer-plus/scripts/run_writer.py#L48).
- Recommendation and validation: The runner turns password rules into promotion/gift cases, assigns priority by position, and uses vague expectations. Produce sourced scenarios and observable assertions or label the demonstration; test password boundaries and empty input.
- Shared P1: [Excel parser](../../skills/en/testing-types/testcase-writer-plus/scripts/common_parser.py#L86) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 142. testing-bottleneck-analysis

[中文入口](../../skills/zh/testing-types/testing-bottleneck-analysis/SKILL.md) · [English entry](../../skills/en/testing-types/testing-bottleneck-analysis/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/testing-bottleneck-analysis.md:34](../../skills/en/testing-types/testing-bottleneck-analysis/prompts/testing-bottleneck-analysis.md#L34).
- Recommendation and validation: Add event timelines, queue/execution/rework decomposition, WIP, and throughput definitions. Test dependency-blocked idle capacity and harmful concurrency, requiring measurable recommendations rather than automatic staffing conclusions.

### 143. threat-modeling

[中文入口](../../skills/zh/testing-types/threat-modeling/SKILL.md) · [English entry](../../skills/en/testing-types/threat-modeling/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/threat-modeling.md:31](../../skills/en/testing-types/threat-modeling/prompts/threat-modeling.md#L31).
- Recommendation and validation: Add data-flow and trust-boundary modeling with actors, preconditions, controls, and residual risks. Provide an optional lightweight taxonomy and verify threats against supplied architecture without invented components.

### 144. timeout-testing

[中文入口](../../skills/zh/testing-types/timeout-testing/SKILL.md) · [English entry](../../skills/en/testing-types/timeout-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/timeout-testing.md:31](../../skills/en/testing-types/timeout-testing/prompts/timeout-testing.md#L31).
- Recommendation and validation: Add end-to-end deadlines, connect/read/queue budgets, cancellation propagation, and late results. Test over-budget call chains and timeout-after-commit for state, side effects, and recovery.

### 145. ui-test-cypress

[中文入口](../../skills/zh/testing-types/ui-test-cypress/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-cypress/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-cypress.md:28](../../skills/en/testing-types/ui-test-cypress/prompts/ui-test-cypress.md#L28).
- Recommendation and validation: Add version-selected configuration, command/stub boundaries, retry semantics, session/data isolation, and business assertions. Verify that an incorrect product outcome fails in a minimal application fixture.

### 146. ui-test-playwright

[中文入口](../../skills/zh/testing-types/ui-test-playwright/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-playwright/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 4 / EN 4.

- Source: [prompts/ui-test-playwright.md:27](../../skills/en/testing-types/ui-test-playwright/prompts/ui-test-playwright.md#L27).
- Recommendation and validation: Require business postconditions, stable semantic locators, identity/data isolation, and failure artifacts. Test incorrect outcomes and parallel users rather than treating a correct page title as business success.

### 147. ui-test-puppeteer

[中文入口](../../skills/zh/testing-types/ui-test-puppeteer/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-puppeteer/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-puppeteer.md:27](../../skills/en/testing-types/ui-test-puppeteer/prompts/ui-test-puppeteer.md#L27).
- Recommendation and validation: Record version/browser configuration and supported scope; add lifecycle, business-readiness waits, and failure artifacts. Test new windows, loading failures, and timeouts with cleanup and observable postconditions.

### 148. ui-test-selector-review

[中文入口](../../skills/zh/testing-types/ui-test-selector-review/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-selector-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-selector-review.md:32](../../skills/en/testing-types/ui-test-selector-review/prompts/ui-test-selector-review.md#L32).
- Recommendation and validation: Add checks for roles/names, test IDs, scoping, uniqueness, dynamic text, and localization. Test duplicate buttons and stable CSS controls; require reasons rather than blanket CSS/XPath bans.

### 149. ui-test-selenium

[中文入口](../../skills/zh/testing-types/ui-test-selenium/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-selenium/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-selenium.md:27](../../skills/en/testing-types/ui-test-selenium/prompts/ui-test-selenium.md#L27).
- Recommendation and validation: Add version-selected setup, observable waits, stale-element handling, parallel data, and driver cleanup. Test rerendering and exceptional exits, avoiding fixed sleeps as a universal repair.

### 150. ui-test-strategy

[中文入口](../../skills/zh/testing-types/ui-test-strategy/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-strategy/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-strategy.md:32](../../skills/en/testing-types/ui-test-strategy/prompts/ui-test-strategy.md#L32).
- Recommendation and validation: Add journey/state/platform coverage and risk-based allocation across component, integration, E2E, visual, and accessibility evidence. Test minimum effective combinations and explicit residual risk.

### 151. ui-test-testcafe

[中文入口](../../skills/zh/testing-types/ui-test-testcafe/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-testcafe/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-testcafe.md:27](../../skills/en/testing-types/ui-test-testcafe/prompts/ui-test-testcafe.md#L27).
- Recommendation and validation: Add version/browser and CI setup, role isolation, asynchronous waits, and reporter failure propagation. Verify generated artifacts and nonzero failure outcomes with a minimal application fixture.

### 152. ui-test-wait-strategy-review

[中文入口](../../skills/zh/testing-types/ui-test-wait-strategy-review/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-wait-strategy-review/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-wait-strategy-review.md:32](../../skills/en/testing-types/ui-test-wait-strategy-review/prompts/ui-test-wait-strategy-review.md#L32).
- Recommendation and validation: Add a readiness-signal decision table for DOM, business state, network, and events with timeout/retry checks. Test long-lived connections and late results without universally equating network idle with readiness.

### 153. ui-test-webdriverio

[中文入口](../../skills/zh/testing-types/ui-test-webdriverio/SKILL.md) · [English entry](../../skills/en/testing-types/ui-test-webdriverio/SKILL.md) · **P2 / Procedure improvements** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/ui-test-webdriverio.md:28](../../skills/en/testing-types/ui-test-webdriverio/prompts/ui-test-webdriverio.md#L28).
- Recommendation and validation: Add capability/service/version combinations, asynchronous commands, parallel-session isolation, and failure-trace fields. Test incompatible setup and failed commands for actionable diagnostics.

### 154. visual-regression-testing

[中文入口](../../skills/zh/testing-types/visual-regression-testing/SKILL.md) · [English entry](../../skills/en/testing-types/visual-regression-testing/SKILL.md) · **P1 / Domain procedure gap** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/visual-regression-testing.md:32](../../skills/en/testing-types/visual-regression-testing/prompts/visual-regression-testing.md#L32).
- Recommendation and validation: Add baseline keys, environment/data/font controls, animation stabilization, justified masks, and threshold definitions. Test defects versus approved design changes, preserving authorized baseline-update decisions.

## Testing workflows (10 pairs)

### 155. daily-testing-workflow

[中文入口](../../skills/zh/testing-workflows/daily-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/daily-testing-workflow/SKILL.md) · **P1 / Evaluation improvements** · Configured cases: ZH 3 / EN 3.

- Source: [evals/cases/basic-success.yaml:20](../../skills/en/testing-workflows/daily-testing-workflow/evals/cases/basic-success.yaml#L20).
- Recommendation and validation: The workflow has concrete gates, while the success judge mainly checks morning/afternoon words. Test red environments, unstarted P0 work, and unregistered failures; require replanning, escalation, and one next handoff, with milestone-based schedules for nonstandard shifts.
- Shared P1: [Excel parser](../../skills/en/testing-workflows/daily-testing-workflow/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 156. discover-testing

[中文入口](../../skills/zh/testing-workflows/discover-testing/SKILL.md) · [English entry](../../skills/en/testing-workflows/discover-testing/SKILL.md) · **P1 / Routing** · Configured cases: ZH 9 / EN 9.

- Source: [prompts/discover-testing.md:19](../../skills/en/testing-workflows/discover-testing/prompts/discover-testing.md#L19).
- Recommendation and validation: The standalone composition reference has five routes and the fallback enumeration covers fewer than 164 Skills. Bundle a compact, versioned capability/ID inventory and test adjacent specialties while preserving one primary and at most one optional Skill. Verify IDs and availability after copying only the router directory.
- Shared P1: [Excel parser](../../skills/en/testing-workflows/discover-testing/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 157. multi-role-quality-synthesis

[中文入口](../../skills/zh/testing-workflows/multi-role-quality-synthesis/SKILL.md) · [English entry](../../skills/en/testing-workflows/multi-role-quality-synthesis/SKILL.md) · **P2 / Evaluation improvements** · Configured cases: ZH 5 / EN 5.

- Source: [prompts/multi-role-quality-synthesis.md:69](../../skills/en/testing-workflows/multi-role-quality-synthesis/prompts/multi-role-quality-synthesis.md#L69).
- Recommendation and validation: Source preservation and minority-risk rules are strong. Add mixed-stage reports, conflicting versions sharing a source ID, and similarly named but non-equivalent findings; check source-set preservation deterministically and calibrate semantic merging.

### 158. product-quality-perspective

[中文入口](../../skills/zh/testing-workflows/product-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/product-quality-perspective/SKILL.md) · **P2 / Stage coverage** · Configured cases: ZH 11 / EN 11.

- Source: [evals/eval.yaml:1](../../skills/en/testing-workflows/product-quality-perspective/evals/eval.yaml#L1).
- Recommendation and validation: The eight-stage contract is clear. Add direct success cases for test-strategy and test-report-review, and standardize source/version, finding IDs, and action evidence for downstream synthesis without adding installation dependencies.

### 159. project-delivery-perspective

[中文入口](../../skills/zh/testing-workflows/project-delivery-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/project-delivery-perspective/SKILL.md) · **P2 / Stage coverage** · Configured cases: ZH 4 / EN 4.

- Source: [SKILL.md:3](../../skills/en/testing-workflows/project-delivery-perspective/SKILL.md#L3).
- Recommendation and validation: Three supported stages and delivery/quality separation are explicit. Add a success fixture for each stage and separate delivery requests, authorized decisions, and quality evidence; handle time zones, dependency delays, and unassigned actions explicitly.

### 160. qa-quality-perspective

[中文入口](../../skills/zh/testing-workflows/qa-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/qa-quality-perspective/SKILL.md) · **P2 / Stage coverage** · Configured cases: ZH 11 / EN 11.

- Source: [prompts/test-strategy.md:14](../../skills/en/testing-workflows/qa-quality-perspective/prompts/test-strategy.md#L14).
- Recommendation and validation: The evidence-missing reporting case is strong. Add evidence-rich success cases for both reporting stages and a small qualitative risk-anchor table so impact, likelihood, and uncertainty do not become an unexplained numerical score.

### 161. release-testing-workflow

[中文入口](../../skills/zh/testing-workflows/release-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/release-testing-workflow/SKILL.md) · **P1 / Contract clarification** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/release-testing-workflow.md:3](../../skills/en/testing-workflows/release-testing-workflow/prompts/release-testing-workflow.md#L3).
- Recommendation and validation: The evidence gates are concrete, but ownership of the ship decision should explicitly distinguish AI recommendations from authorized approval. Name the decision owner and evidence source, treat T-14 as an adaptable example, and test hotfix/canary windows.
- Shared P1: [Excel parser](../../skills/en/testing-workflows/release-testing-workflow/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 162. sprint-testing-workflow

[中文入口](../../skills/zh/testing-workflows/sprint-testing-workflow/SKILL.md) · [English entry](../../skills/en/testing-workflows/sprint-testing-workflow/SKILL.md) · **P1 / Adaptability** · Configured cases: ZH 3 / EN 3.

- Source: [prompts/sprint-testing-workflow.md:19](../../skills/en/testing-workflows/sprint-testing-workflow/prompts/sprint-testing-workflow.md#L19).
- Recommendation and validation: The DoD and handoffs are useful, while the schedule uses a 12-day example and shallow success assertions. Map phases to supplied length/capacity or milestones and test one-week, continuous-flow, spillover, and unaccepted-P0 scenarios.
- Shared P1: [Excel parser](../../skills/en/testing-workflows/sprint-testing-workflow/scripts/convert_formats.py#L63) loses inlineStr text; repair input fidelity and sparse-column handling as described in finding A.

### 163. technical-quality-perspective

[中文入口](../../skills/zh/testing-workflows/technical-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/technical-quality-perspective/SKILL.md) · **P2 / Stage coverage** · Configured cases: ZH 11 / EN 11.

- Source: [prompts/code-review.md:5](../../skills/en/testing-workflows/technical-quality-perspective/prompts/code-review.md#L5).
- Recommendation and validation: Code identity and reviewable-change gates are concrete. Add success cases for requirements-analysis and test-strategy, standardize file/line/version evidence, and clarify handoff to code-review or specialized design reviews.

### 164. ux-quality-perspective

[中文入口](../../skills/zh/testing-workflows/ux-quality-perspective/SKILL.md) · [English entry](../../skills/en/testing-workflows/ux-quality-perspective/SKILL.md) · **P2 / Stage coverage** · Configured cases: ZH 11 / EN 11.

- Source: [prompts/test-report-review.md:24](../../skills/en/testing-workflows/ux-quality-perspective/prompts/test-report-review.md#L24).
- Recommendation and validation: Applicability and screenshot evidence limits are clear. Add evidence-rich success cases for both reporting stages and an optional, source-selected matrix of input modes, devices, assistive technology, and states.

## Executed checks and remaining evidence gaps

| Check | Result | Evidence limit |
| --- | --- | --- |
| `organize_project_dirs.py --check` | issues=0 | Read-only validation, not directory organization. |
| Metadata / static CLI contract / integrity / independence | 328 directories, findings=0 | Valid structure, identities, and resource links, not correct task behavior. |
| Governance inventory / matrix / v1.4 closeout / Composition | Generated views current; 5 relations, 5 routes, 10 targets | Configuration consistency, not observed routing. |
| External snapshots | 0; over-limit=0, bad names=0 | Snapshot hygiene only. |
| `bash scripts/validate_skill_evals.sh` | `skill-up validate: ok=328 fail=0` | Evaluation YAML validation only. |
| Evaluation contract / eval rules / bilingual docs | findings=0; 20 valid rules | Contract, rule, and documentation checks. |
| `python3 -m unittest discover -s scripts/tests` | 191 tests, OK | Existing repository script tests, not all Skill behavior evaluations. |
| Python AST | 791 files, no syntax errors | Syntax only. |
| Offline helper reproductions | Evidence JSON; separate Excel calls in 24 pairs lose inline text | Limited synthetic inputs, not target-tool execution. |

Used non-writing checks from the quality script; did not directly run the full `check_skills_quality.sh`, which organizes directories and regenerates inventory. The discovery/install smoke in `check_skills_cli_compatibility.sh` was not run; static CLI checks cannot substitute for that smoke.

No full model `skill-up run`, benchmark/regression across all 328 directories, all UI/API framework executions, Host/production checks, or business acceptance was performed. No Quality Score or universal semantic pass is claimed. Behavior fixes should synchronize both languages, maintain evaluations, and run the full project quality gate, relevant executed evaluations, and distribution smoke.

## Suggested implementation order

1. **Parser and generator correctness:** repair A/B/C with minimal offline regression fixtures and failure-sensitive artifacts, maintaining local copies and standalone installation.
2. **Minimal domain procedures:** improve the 42 procedure-gap pairs individually, pilot frequently used capabilities, then expand after calibration.
3. **Evaluations and routing:** add real small inputs, correct controls, and adjacent negative cases; record semantic and selection evidence separately.
4. **Wording and applicability:** fill stage coverage, schedule/window adaptation, localized metadata, framework versions, and dependency guidance.

Only review reports and redacted reproduction evidence were added. Skills were not modified, committed, or pushed; existing working-tree content was preserved.
