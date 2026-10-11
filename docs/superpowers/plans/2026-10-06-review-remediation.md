# All-Skill Review Remediation Implementation Plan

> **For agentic workers:** Use the dispatching-parallel-agents workflow for disjoint content packages. The coordinator owns shared script fixes, integration, and final verification. User authorization is to repair the findings and continue reviewing; the subsequent user instruction authorizes committing and pushing the reviewed changes after continuation; no rename or release is requested.

**Goal:** Address the 164 pair-by-pair review recommendations and reproduce/review the corrected behavior.

**Architecture:** Keep each leaf Skill self-contained and preserve canonical names. Correct shared parser copies together; conservative helpers prepare evidence or incomplete scaffolds instead of inventing semantic results. Add concise domain procedures and concrete, calibrated Eval fixtures without replacing the existing evaluation engine.

**Tech Stack:** Python standard library/unittest, Markdown, YAML, skill-up, skills CLI 1.7.0.

**Spec:** [All-Skill review](../../reviews/2026-10-06-all-skills-review.md).

## Global Constraints

- Synchronize EN/ZH and retain standalone resources, names, installation behavior and existing provenance/authority constraints.
- Preserve pre-existing working-tree modifications. Add to existing user-edited files only where necessary; no reset or wholesale overwrite.
- Treat validate/static tests, local helper behavior, model evaluation, distribution smoke and business acceptance as separate evidence.
- Keep original review reports as snapshots; record closure and new findings in a separate review.

## Review Focus

- Sparse/multi-sheet Excel and punctuation-rich Markdown must retain supplied values and source identity.
- Variable URLs, implicit curl methods, request bodies, unresolved schemas and missing parser dependencies must not silently change intent.
- API scaffolds without supplied expectations/data must not become green protective tests; bad responses must fail concrete assertions.
- Unrelated/empty Plus input must preserve unknowns and never acquire invented business scope, priorities, findings or approval.
- Domain procedures and Eval fixtures must test the task and its correct control, preserve role/version evidence, and stay bilingual and standalone.

## Tasks

- [x] **1. Parser fidelity:** Add failing regressions in `scripts/tests/test_review_parser_fidelity.py`; repair all affected `scripts/{parse_formats,convert_formats,common_parser}.py` copies and API source parsers. Validate original failures, sparse/multi-sheet cells, alternate curl options, variables, bodies, SOAP addresses and dependency errors.
- [x] **2. API generators:** Add failing regressions in `scripts/tests/test_review_api_generators.py`; fix the four tool-specific generators/templates and add bilingual behavioral Eval cases. Validate empty input, missing expectations, escaping, request fidelity and failure-sensitive generated assertions.
- [x] **3. Plus helpers:** Add failing regressions in `scripts/tests/test_review_plus_scaffolds.py`; remove fixed business answers, preserve source material and mark preparatory output unassessed. Align usage docs/Prompts/Evals, validate unrelated and empty inputs and separately review semantic capability limits.
- [x] **4. Skill content:** Process the 42 domain gaps, 59 method enhancements, 44 evaluation recommendations, 5 stage-coverage recommendations and schedule adaptation in disjoint groups. Add operational steps, concrete fixtures and correct controls; preserve existing contracts. Coordinator handles validate evidence, release recommendations and standalone router inventory.
- [x] **5. Integration checks:** Run all new regressions, `bash scripts/check_skills_quality.sh`, local-checkout `check_skills_cli_compatibility.sh` with isolated temporary cache, relevant `skill-up run` cases and a final scoped diff/status audit. Record external/engine blockers precisely.
- [x] **6. Continue review:** Review corrected scripts and all changed packages, challenge the Review Focus inputs, fix new correctness findings, and publish paired remediation/review reports with per-Skill closure and evidence limits.

## Decisions

- Optional deterministic Plus scripts prepare evidence and explicit incomplete scaffolds; semantic analysis remains the agent's main Prompt task. This repairs fabricated results without adding an unrequested model provider/runtime.
- Script regressions use sanitized offline fixtures and local fake clients, not production APIs.
- Review recommendations are maintenance guidance; closure of wording/fixtures does not establish a model quality score or release approval.

## Verification Ledger

Completed repairs and second static/local review for all 164 pairs. Final quality gate: 328 valid configurations and 227 passing tests. Local skills@1.7.0 gate: 164 discovered, isolated English installation passes. Eight generated API projects pass good responses and reject wrong status/body. Stored EN model outputs pass offline regrading. After explicit user authorization on 2026-10-07, current targeted EN and ZH model cases both run PASS (100% each); other semantic cases remain NOT_RUN. See [paired final review](../../reviews/2026-10-07-all-skills-repair-review.md) and [evidence](../../../evidence/skill-quality/2026-10-07-review-repair/summary.json).


Runtime continuation on 2026-10-07: 13 unique selected cases report PASS; a versioned-provenance grader FAIL is repaired and passes offline, with its live rerun blocked by automatic approval review. One semantic judge attempt is ERROR because the current Codex ChatGPT login rejects gpt-5. Of 530 new cases, 515 remain NOT_RUN. Both newline and provenance grader repairs have RED-to-GREEN tests. See [runtime follow-up](../../reviews/2026-10-07-review-runtime-followup.md).


Subsequent continuation: nested configuration and grader controls pass, bilingual review inputs and concrete impact/owner-request behavior are repaired. Account quota events remain distinct from approval rejection. See [current runtime continuation](../../reviews/2026-10-08-review-runtime-continuation.md) for source-bound outcomes and remote-delivery status.
