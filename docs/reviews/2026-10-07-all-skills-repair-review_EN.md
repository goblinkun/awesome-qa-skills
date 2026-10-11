# All-Skill Repairs and Second Review (2026-10-07)

> This page retains the 2026-10-07 results and blockers. Continuous external-run authorization was subsequently provided; see the [live continuation](./2026-10-08-review-runtime-continuation_EN.md) for later repairs and current states.

[简体中文](./2026-10-07-all-skills-repair-review.md)

All first-review recommendations were addressed across 164 Skills and 328 language packages, followed by a second review of the changes. The original review remains a snapshot. This report records concrete repairs, additional findings, and evidence scope. **Static/script repairs are verified; full model behavior evaluation is incomplete.**

Original review: [2026-10-06 review](./2026-10-06-all-skills-review_EN.md).
Per-Skill machine record: [evidence JSON](./2026-10-07-all-skills-repair-review-evidence.json); verification evidence: [summary.json](../../evidence/skill-quality/2026-10-07-review-repair/summary.json)

Runtime continuation and blockers: [2026-10-07-review-runtime-followup_EN.md](./2026-10-07-review-runtime-followup_EN.md).

## Repair scope

42 domain-method repairs, 59 method/tool enhancements, 50 evaluation/workflow-coverage repairs, and 13 shared-script/contract repairs. Added 530 cases (265 per language), bringing the total to 1,658; existing cases and canonical names were retained. Affected Excel helpers and Chinese metadata were synchronized.

## Verification and limits

| Check | Result and supported scope |
| --- | --- |
| `bash scripts/check_skills_quality.sh` | PASS; 328 valid eval configurations, 227 passing script tests; structure/independence/bilingual/governance checks pass. |
| `SKILLS_CLI_PACKAGE="$PWD" bash scripts/check_skills_cli_compatibility.sh` | PASS; pinned skills@1.7.0 discovers 164 items; English functional-testing installs into an isolated target. No Skill execution claim. |
| Real framework / local requests | 8 EN/ZH projects, 24 outcome runs: good responses pass; wrong status and wrong business body fail. Synthetic loopback service only. |
| Standalone helpers / graders | 74 resource copies match; 118 isolated graders pass both table forms and reject mutants; 26 Plus CLI export checks pass. |
| JMeter / Gatling / UI | Local synthetic JMeter good passes; wrong business state and early CSV exhaustion fail gates. Gatling Java DSL compiles. UI browser runtime and actual load/SLO acceptance are NOT_RUN. |
| Model evaluation | Among 530 new cases: 13 unique reported live PASS, one repaired grader FAIL awaiting a live rerun, one judge ERROR, and 515 NOT_RUN. The remaining script queue is approval-blocked; semantic judges require a compatible account/model setup. |

The two previously authorized bilingual cases and their history remain in [model-pilot-summary.json](../../evidence/skill-quality/2026-10-07-review-repair/model-pilot-summary.json). Per-case continuation records are in [runtime-followup.json](../../evidence/skill-quality/2026-10-07-review-repair/runtime-followup.json). Observed Codex CLI version is 0.160.1; model identity is UNKNOWN. Targeted results do not establish library-wide improvement.

Deterministic generators do not automatically complete complex OpenAPI schemas or WSDL SOAP envelopes; missing sourced requests/assertions produce explicitly incomplete scaffolds. The main prompt can complete them, but generator success does not establish production acceptance. New judge model IDs follow [OpenAI GPT-5 documentation](https://developers.openai.com/api/docs/models/gpt-5); no API-provider execution is claimed.

## Additional findings and repairs

| Finding | Repair | Location |
| --- | --- | --- |
| XLSX and Markdown fidelity | Read inlineStr/rich text, sparse columns, multiple worksheets, and cached formulas with sheet/row identity; unreliable input fails explicitly. Plus row serialization preserves field boundaries and punctuation. | [test_review_parser_fidelity.py](../../scripts/tests/test_review_parser_fidelity.py) |
| API sources and generators | Fixed implicit curl POST, variable URLs, bodies, and distinct scenarios. Numeric OpenAPI response keys and unresolved references are explicit; WSDL operations follow port bindings. Normalized endpoints JSON enters the generator pipeline. | [test_review_api_generators.py](../../scripts/tests/test_review_api_generators.py) |
| False-green scaffolds | Missing expectations/request values/schema assertions produce nonzero incomplete scaffolds. Credentials are environmental; templates no longer universally accept 404. | [api_case_contract.py](../../scripts/skill_resources/api_case_contract.py) |
| Actual Bruno execution | Fixed JSON body indentation. A zero CLI exit with skipped requests fails the report gate unless actual HTTP responses, counts, and assertions support completion. | [test_review_bruno_reports.py](../../scripts/tests/test_review_bruno_reports.py) |
| Fixed Plus answers | Removed invented promotion/payment/inventory scope, priorities, and metrics from all four helpers. Full sources/hashes/unknown states are retained; empty source fails. Evidence preparation remains distinct from semantic work. | [test_review_plus_scaffolds.py](../../scripts/tests/test_review_plus_scaffolds.py) |
| Isolated graders | 118 domain graders are standalone Python files. Valid Markdown with or without outer pipes passes; missing/duplicate/incorrect decisions and wrong calculations fail. | [test_review_eval_graders.py](../../scripts/tests/test_review_eval_graders.py) |
| Grader data and controls | 32 root repair graders have per-ID controls; 22 structured-result graders reject duplicate JSON keys and boolean counts. Missing-rule controls carry their own explicit contracts. | [test_review_eval_graders.py](../../scripts/tests/test_review_eval_graders.py) |
| Existing output contracts | New decision views retain existing RA/RC/RT enums and evidence states; proposed rewrites do not replace original criteria, and Go/No-Go recommendations do not imply authorized approval. | [requirement-traceability-analysis.md](../../skills/zh/testing-types/requirement-traceability-analysis/prompts/requirement-traceability-analysis.md) |
| Thresholds and judge configuration | Retry-After retains protocol units; performance gates come from input; new agent_judge cases use a documented public API model ID. Valid configuration is not provider execution. | [api-rate-limit-testing.md](../../skills/zh/testing-types/api-rate-limit-testing/prompts/api-rate-limit-testing.md) |
| Live grader false rejections | Repaired prose-trim terminal-newline checks and versioned source-union fields. Original FAIL, repairs, offline regrades and live reruns remain separate. | [runtime follow-up](./2026-10-07-review-runtime-followup_EN.md) |

## Per-Skill repairs and second review (164 items)

Each item covers both languages. Static review covers entry/main prompt, fixtures/oracles, standalone resources, and existing contracts. NOT_RUN does not become model PASS because YAML, grader controls, or catalog visibility pass.

### 001. `skill-change-verification` (P1)

Location: [ZH](../../skills/zh/skill-engineering/skill-change-verification/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-change-verification/SKILL.md)

- First-review recommendation: The prompt labels skill-up validate as Evaluation although the entry separates it from runtime evidence. Classify validation as structural/configuration evidence, reserve Evaluation for executed runs and judges, and add a change-to-check decision table. Test a validate-only log versus a real run.
- Changed: Classified validate as configuration evidence, reserved Evaluation for actual runs/judges, and added a change/check/claim decision table and per-ID grader.
- New cases: [review-repair-regression](../../skills/en/skill-engineering/skill-change-verification/evals/cases/review-repair-regression.yaml) — skill-change-verification: sourced repair regression.
- Second review/verification: Contract/routing fixture and grader controls pass; both configurations valid (configuration only).
- Model verification: Current EN/ZH targeted cases both PASS; V1 is NOT_RUN and V2 is FAIL, with sourced explanations and unrun boundaries. Other model cases remain unrun.

### 002. `skill-evaluation` (P2)

Location: [ZH](../../skills/zh/skill-engineering/skill-evaluation/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-evaluation/SKILL.md)

- First-review recommendation: Evidence and judge boundaries are clear, but the three cases mainly check report shape and missing input. Add comparable/non-comparable run fixtures, missing selection events, and infrastructure timeouts; verify classifications and comparison conclusions.
- Changed: Reviewed current evidence-state and attribution contract, preserving pre-existing user edits. Artifact cases test comparison identity and observed selection rather than headings.
- New cases: [review-comparable-runs](../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-comparable-runs.yaml) — Compare pinned previous/current artifacts; [review-incomparable-runs](../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-incomparable-runs.yaml) — Changed input and model prevent attribution; [review-trace-and-timeout](../../skills/en/skill-engineering/skill-evaluation/evals/cases/review-trace-and-timeout.yaml) — Missing selection and infrastructure timeout are distinct.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Model evidence: EN `review-comparable-runs` ran but the judge returned ERROR because the current login does not support the configured `gpt-5`. Reviewing the runner response is not automated semantic acceptance. Other new cases remain NOT_RUN.

### 003. `skill-prose-review` (P2)

Location: [ZH](../../skills/zh/skill-engineering/skill-prose-review/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-prose-review/SKILL.md)

- First-review recommendation: The success case requests a review without supplying a Skill body. Add a small conflicting package and a correct control, and require concrete locations, impacts, and recommendations instead of checklist repetition.
- Changed: Read the prose-review contract and supplied exact line-counted conflicting/control texts; no package-level inventory or business execution is required.
- New cases: [review-conflicting-source](../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) — Locate actual output and metadata conflicts; [review-consistent-control](../../skills/en/skill-engineering/skill-prose-review/evals/cases/review-consistent-control.yaml) — Accept a coherent prose contract.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 004. `skill-prose-trim` (P2)

Location: [ZH](../../skills/zh/skill-engineering/skill-prose-trim/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-prose-trim/SKILL.md)

- First-review recommendation: The preservation boundaries are useful, but the success case has no source passage and only checks a word. Add before/after fixtures containing process narration, durable contracts, formal history, and measurement limits; distinguish review from authorized editing.
- Changed: Before/after fixture separates durable measurements/history from process narration; edit case checks exact bytes and sealed-payload preservation. Review mode is separately graded.
- New cases: [review-authorized-trim](../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-authorized-trim.yaml) — Remove process residue while preserving exact durable facts; [review-only-trim](../../skills/en/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) — Review-only mode distinguishes proposals from edits.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Model evidence: EN/ZH `review-authorized-trim` live reruns PASS. The initial English newline false rejection remains a historic FAIL; both `review-only-trim` cases remain NOT_RUN.

### 005. `skill-quality-review` (P2)

Location: [ZH](../../skills/zh/skill-engineering/skill-quality-review/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-quality-review/SKILL.md)

- First-review recommendation: The package contract is clear, but the success case supplies no actual package. Add valid, missing-prompt, missing bare-path resource, and bilingual-schema fixtures; clarify when package review versus prose review applies.
- Changed: Read full package-review contract; complete fixture resolves independent resources. Four cases isolate correct package, absent prompt, missing bare resource and bilingual schema mismatch.
- New cases: [review-bilingual-schema](../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) — Bilingual output schema mismatch is concrete; [review-missing-bare-resource](../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-missing-bare-resource.yaml) — Bare resource paths must resolve too; [review-missing-prompt](../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-missing-prompt.yaml) — Entry points to an absent primary prompt; [review-valid-package](../../skills/en/skill-engineering/skill-quality-review/evals/cases/review-valid-package.yaml) — Complete package allows no blocking static findings.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 006. `daily-testing-workflow` (P2)

Location: [ZH](../../skills/zh/testing-workflows/daily-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/daily-testing-workflow/SKILL.md)

- First-review recommendation: The workflow has concrete gates, while the success judge mainly checks morning/afternoon words. Test red environments, unstarted P0 work, and unregistered failures; require replanning, escalation, and one next handoff, with milestone-based schedules for nonstandard shifts.
- Changed: Reviewed environment/start, P0 checkpoint and failure-registration gates. New cases assert actual queue changes, escalation and a single handoff.
- New cases: [review-red-night-shift](../../skills/en/testing-workflows/daily-testing-workflow/evals/cases/review-red-night-shift.yaml) — Red environment changes the night-shift queue; [review-unregistered-close-failure](../../skills/en/testing-workflows/daily-testing-workflow/evals/cases/review-unregistered-close-failure.yaml) — Unregistered P0 failure blocks close; [review-unstarted-p0](../../skills/en/testing-workflows/daily-testing-workflow/evals/cases/review-unstarted-p0.yaml) — Priority checkpoint cuts P2 before unstarted P0.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 007. `discover-testing` (P1)

Location: [ZH](../../skills/zh/testing-workflows/discover-testing/SKILL.md) · [EN](../../skills/en/testing-workflows/discover-testing/SKILL.md)

- First-review recommendation: The standalone composition reference has five routes and the fallback enumeration covers fewer than 164 Skills. Bundle a compact, versioned capability/ID inventory and test adjacent specialties while preserving one primary and at most one optional Skill. Verify IDs and availability after copying only the router directory.
- Changed: Added a standalone 164-item catalog snapshot with UNKNOWN installation availability; routing separates authentication, authorization, retrieval, and regression selection and bounds primary/helper composition.
- New cases: [review-authn-neighbor](../../skills/en/testing-workflows/discover-testing/evals/cases/review-authn-neighbor.yaml) — discover-testing: sourced repair regression; [review-authz-neighbor](../../skills/en/testing-workflows/discover-testing/evals/cases/review-authz-neighbor.yaml) — discover-testing: sourced repair regression; [review-rag-retrieval-neighbor](../../skills/en/testing-workflows/discover-testing/evals/cases/review-rag-retrieval-neighbor.yaml) — discover-testing: sourced repair regression; [review-regression-selection-neighbor](../../skills/en/testing-workflows/discover-testing/evals/cases/review-regression-selection-neighbor.yaml) — discover-testing: sourced repair regression.
- Second review/verification: Contract/routing fixture and grader controls pass; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Model evidence: All four new authentication, authorization, RAG retrieval and regression-selection fixtures pass in both languages (eight live PASS). These verdicts do not cover the full Skill suite.

### 008. `multi-role-quality-synthesis` (P2)

Location: [ZH](../../skills/zh/testing-workflows/multi-role-quality-synthesis/SKILL.md) · [EN](../../skills/en/testing-workflows/multi-role-quality-synthesis/SKILL.md)

- First-review recommendation: Source preservation and minority-risk rules are strong. Add mixed-stage reports, conflicting versions sharing a source ID, and similarly named but non-equivalent findings; check source-set preservation deterministically and calibrate semantic merging.
- Changed: Reviewed input validation, semantic equivalence, source-union and minority-severity rules. Structural judge asserts identity, source/evidence conservation and P0; semantic cases isolate stage and equivalence decisions.
- New cases: [review-duplicate-source-version](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/cases/review-duplicate-source-version.yaml) — Conflicting versions cannot share an unqualified identity; [review-mixed-stage](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/cases/review-mixed-stage.yaml) — Mixed stages must not silently synthesize; [review-similar-name-distinct-conditions](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/cases/review-similar-name-distinct-conditions.yaml) — Same finding title does not prove equivalence; [review-source-union](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/cases/review-source-union.yaml) — Merged findings preserve all sources and minority P0.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Model evidence: EN source-union reports live PASS. ZH reports FAIL from a versioned-field false rejection; after repair its stored response regrades PASS offline, while the live rerun is approval-blocked. Other new cases remain NOT_RUN.

### 009. `product-quality-perspective` (P2)

Location: [ZH](../../skills/zh/testing-workflows/product-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/product-quality-perspective/SKILL.md)

- First-review recommendation: The eight-stage contract is clear. Add direct success cases for test-strategy and test-report-review, and standardize source/version, finding IDs, and action evidence for downstream synthesis without adding installation dependencies.
- Changed: Checked existing six supported-stage success cases and added direct strategy and report-review evidence fixtures plus no-product-impact control. Source fields are report-local and version values come from input.
- New cases: [review-no-product-impact-control](../../skills/en/testing-workflows/product-quality-perspective/evals/cases/review-no-product-impact-control.yaml) — Backend-only code without product impact is not filler review; [review-test-report-evidence](../../skills/en/testing-workflows/product-quality-perspective/evals/cases/review-test-report-evidence.yaml) — Product review rejects unsupported full-scope conclusion; [review-test-strategy-evidence](../../skills/en/testing-workflows/product-quality-perspective/evals/cases/review-test-strategy-evidence.yaml) — Product strategy prioritizes irreversible user loss.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 010. `project-delivery-perspective` (P2)

Location: [ZH](../../skills/zh/testing-workflows/project-delivery-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/project-delivery-perspective/SKILL.md)

- First-review recommendation: Three supported stages and delivery/quality separation are explicit. Add a success fixture for each stage and separate delivery requests, authorized decisions, and quality evidence; handle time zones, dependency delays, and unassigned actions explicitly.
- Changed: Read exactly three supported-stage prompts. Each fixture distinguishes requested changes, actual authorized scope and preserved quality status; timezone arithmetic and unknown action fields have explicit oracles.
- New cases: [review-test-report-review-sources](../../skills/en/testing-workflows/project-delivery-perspective/evals/cases/review-test-report-review-sources.yaml) — Delivery sources at test-report-review; [review-test-strategy-review-sources](../../skills/en/testing-workflows/project-delivery-perspective/evals/cases/review-test-strategy-review-sources.yaml) — Delivery sources at test-strategy-review; [review-test-strategy-sources](../../skills/en/testing-workflows/project-delivery-perspective/evals/cases/review-test-strategy-sources.yaml) — Delivery sources at test-strategy.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 011. `qa-quality-perspective` (P2)

Location: [ZH](../../skills/zh/testing-workflows/qa-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/qa-quality-perspective/SKILL.md)

- First-review recommendation: The evidence-missing reporting case is strong. Add evidence-rich success cases for both reporting stages and a small qualitative risk-anchor table so impact, likelihood, and uncertainty do not become an unexplained numerical score.
- Changed: Existing six success stages are retained. Raw six-ID fixture checks status preservation and explicit execution denominator for both reporting stages; anchor table makes qualitative judgment non-numeric.
- New cases: [review-test-report-review-raw-results](../../skills/en/testing-workflows/qa-quality-perspective/evals/cases/review-test-report-review-raw-results.yaml) — QA evidence-rich test-report-review; [review-test-reporting-raw-results](../../skills/en/testing-workflows/qa-quality-perspective/evals/cases/review-test-reporting-raw-results.yaml) — QA evidence-rich test-reporting.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 012. `release-testing-workflow` (P1)

Location: [ZH](../../skills/zh/testing-workflows/release-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/release-testing-workflow/SKILL.md)

- First-review recommendation: The evidence gates are concrete, but ownership of the ship decision should explicitly distinguish AI recommendations from authorized approval. Name the decision owner and evidence source, treat T-14 as an adaptable example, and test hotfix/canary windows.
- Changed: Separated Go/No-Go recommendations from authorized approval records; release paths and exit gates adapt to normal, hotfix, and canary material without inferring approval from test results.
- New cases: [review-repair-regression](../../skills/en/testing-workflows/release-testing-workflow/evals/cases/review-repair-regression.yaml) — release-testing-workflow: sourced repair regression.
- Second review/verification: Contract/routing fixture and grader controls pass; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 013. `sprint-testing-workflow` (P2)

Location: [ZH](../../skills/zh/testing-workflows/sprint-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/sprint-testing-workflow/SKILL.md)

- First-review recommendation: The DoD and handoffs are useful, while the schedule uses a 12-day example and shallow success assertions. Map phases to supplied length/capacity or milestones and test one-week, continuous-flow, spillover, and unaccepted-P0 scenarios.
- Changed: Read all six phase gates and DoD. Cadence adaptation preserves gate semantics for five-day iterations and continuous flow; final scenario checks spillover and written-acceptance boundary.
- New cases: [review-continuous-flow](../../skills/en/testing-workflows/sprint-testing-workflow/evals/cases/review-continuous-flow.yaml) — Continuous flow uses events rather than invented dates; [review-one-week-capacity](../../skills/en/testing-workflows/sprint-testing-workflow/evals/cases/review-one-week-capacity.yaml) — One-week iteration preserves all phase gates; [review-spillover-unaccepted-p0](../../skills/en/testing-workflows/sprint-testing-workflow/evals/cases/review-spillover-unaccepted-p0.yaml) — Unaccepted P0 and delayed story remain exit blockers.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 014. `technical-quality-perspective` (P2)

Location: [ZH](../../skills/zh/testing-workflows/technical-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/technical-quality-perspective/SKILL.md)

- First-review recommendation: Code identity and reviewable-change gates are concrete. Add success cases for requirements-analysis and test-strategy, standardize file/line/version evidence, and clarify handoff to code-review or specialized design reviews.
- Changed: Added the three missing success stages to the five existing stage cases. Source locators are limited to provided design text/version, and code identity gates remain unchanged.
- New cases: [review-requirements-analysis-design](../../skills/en/testing-workflows/technical-quality-perspective/evals/cases/review-requirements-analysis-design.yaml) — Technical source evidence at requirements-analysis; [review-test-report-review-version](../../skills/en/testing-workflows/technical-quality-perspective/evals/cases/review-test-report-review-version.yaml) — Technical report review preserves version mismatch; [review-test-strategy-design](../../skills/en/testing-workflows/technical-quality-perspective/evals/cases/review-test-strategy-design.yaml) — Technical source evidence at test-strategy.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 015. `ux-quality-perspective` (P2)

Location: [ZH](../../skills/zh/testing-workflows/ux-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/ux-quality-perspective/SKILL.md)

- First-review recommendation: Applicability and screenshot evidence limits are clear. Add evidence-rich success cases for both reporting stages and an optional, source-selected matrix of input modes, devices, assistive technology, and states.
- Changed: Added evidence-rich reporting/report-review successes to six existing stage cases. Fixture isolates input/device/AT/state scope and forbids extrapolating one desktop observation.
- New cases: [review-test-report-review-experience](../../skills/en/testing-workflows/ux-quality-perspective/evals/cases/review-test-report-review-experience.yaml) — UX observed results at test-report-review; [review-test-reporting-experience](../../skills/en/testing-workflows/ux-quality-perspective/evals/cases/review-test-reporting-experience.yaml) — UX observed results at test-reporting.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 016. `acceptance-criteria-review` (P2)

Location: [ZH](../../skills/zh/testing-types/acceptance-criteria-review/SKILL.md) · [EN](../../skills/en/testing-types/acceptance-criteria-review/SKILL.md)

- First-review recommendation: Distinguish review, proposed rewrites, and missing rules. Test original AC IDs, threshold equality, and duplicate refunds.
- Changed: Select `review` (check existing criteria), `proposed-rewrite` (suggest a rewrite), or `missing-rule` (undefined policy). Retain each original AC ID, version, text, and source; a proposal never replaces the source rule. Produce: AC ID | original criterion | mode | observable oracle | proposed wording | reason for change | product confirmation. Leave undefined rules open.
- New cases: [domain-method-regression](../../skills/en/testing-types/acceptance-criteria-review/evals/cases/domain-method-regression.yaml) — acceptance-criteria-review: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 017. `accessibility-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/accessibility-testing/SKILL.md) · [EN](../../skills/en/testing-types/accessibility-testing/SKILL.md)

- First-review recommendation: Record the target WCAG version/level, criterion IDs, and manual versus automated evidence. Test scan success with keyboard failure.
- Changed: Record the project-supplied WCAG version/level, scope, and success criterion IDs. Missing targets stay open; never choose a level or claim conformance by default. Build criterion ID | user task/state | input/assistive technology/version | steps | evidence type | outcome. Keep automated scan, keyboard, screen-reader, and manual visual evidence separate.
- New cases: [domain-method-regression](../../skills/en/testing-types/accessibility-testing/evals/cases/domain-method-regression.yaml) — accessibility-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 018. `agent-failure-recovery-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-failure-recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-failure-recovery-testing/SKILL.md)

- First-review recommendation: Add failure-to-recovery state transitions and fixtures for timeout-after-write, partial results, and permanent errors.
- Changed: Build failure | confirmed write state | retryability | retry/compensate/escalate | recovered state | evidence from the project protocol. Separate transient, permanent, and indeterminate outcomes. A timeout does not mean no execution: query committed effects by operation_id/idempotency key before replay. Read back an existing result or retry safely; the same key must not produce a second business write.
- New cases: [domain-method-regression](../../skills/en/testing-types/agent-failure-recovery-testing/evals/cases/domain-method-regression.yaml) — agent-failure-recovery-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 019. `agent-long-running-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-long-running-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-long-running-testing/SKILL.md)

- First-review recommendation: Add checkpoint/version and cancellation-race procedures; test resumed work, duplicate submissions, and resource release using traces.
- Changed: Derive queued→running→checkpointed→interrupted→resuming→completed and running→cancelling→cancelled from the actual protocol; undefined transitions remain open. Capture task_id, checkpoint schema/state version, committed step IDs, provenance, and integrity. Validate versions and committed effects before resuming; incompatible checkpoints cannot be blindly replayed.
- New cases: [domain-method-regression](../../skills/en/testing-types/agent-long-running-testing/evals/cases/domain-method-regression.yaml) — agent-long-running-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 020. `agent-loop-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-loop-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-loop-testing/SKILL.md)

- First-review recommendation: Define progress detection, repeated action/observation handling, and budget precedence; verify stop/escalation decisions from traces.
- Changed: Record task/run/step IDs, plan, tool and normalized arguments, observation identity/digest, business state delta, and cumulative time/cost; redact sensitive values while preserving deduplication evidence. Progress requires new goal-relevant evidence or state advancement. Repeated action/observation with no advancement counts as a no-progress cycle; successful calls or repeated prose do not establish progress.
- New cases: [domain-method-regression](../../skills/en/testing-types/agent-loop-testing/evals/cases/domain-method-regression.yaml) — agent-loop-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 021. `agent-memory-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-memory-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-memory-testing/SKILL.md)

- First-review recommendation: Test tenant isolation, conflicting preference versions, expiration, and deletion with explicit provenance and retrieval expectations.
- Changed: Capture tenant/user IDs, memory ID, content version, source, write time, expiry, and withdrawal/deletion status. Retain retrieved provenance/version, not only the final answer. Resolve old/new preferences using supplied precedence rules. Undefined conflicts remain open; never assume last-write-wins or invent retention periods.
- New cases: [domain-method-regression](../../skills/en/testing-types/agent-memory-testing/evals/cases/domain-method-regression.yaml) — agent-memory-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 022. `agent-permission-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-permission-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-permission-testing/SKILL.md)

- First-review recommendation: Add a principal/tool/resource/action matrix and test revocation, delegation, changed parameters, and zero side effects after denial.
- Changed: Build principal/delegation chain | tool | resource/tenant | action | parameter bounds | authority source/version/expiry | allow/deny/reapprove. Tool names alone do not define authorization. Before execution verify actual identity, revocation, resource, and parameters. Delegation cannot expand the grant; expired/revoked authority is invalid.
- New cases: [domain-method-regression](../../skills/en/testing-types/agent-permission-testing/evals/cases/domain-method-regression.yaml) — agent-permission-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 023. `agent-tool-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/agent-tool-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-tool-testing/SKILL.md)

- First-review recommendation: Use concrete tool schemas and traces to verify argument validity, tool selection, and exactly-once side effects after timeouts.
- Changed: Read tool contract for authorization and retry effects. One schema/trace fixture contains valid read, denied wrong tool, type-invalid argument, exactly-once replay and duplicate write; deterministic grader rejects classification/count mutations.
- New cases: [review-tool-schema-trace](../../skills/en/testing-types/agent-tool-testing/evals/cases/review-tool-schema-trace.yaml) — Tool schema and side effects are judged from concrete traces.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 024. `ai-agent-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/ai-agent-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-agent-testing/SKILL.md)

- First-review recommendation: Specify task oracles, trace invariants, repeated-run sampling, and termination classes; test correct answers produced through unauthorized actions.
- Changed: Define input sample ID, task-success oracle, allowed tools/resources, prohibited effects, and stopping conditions. Missing goals remain open. Check run/step order, permission, idempotency, isolation, recovery, and budget invariants. Judge outcome correctness and process compliance separately; either failure prevents an overall pass.
- New cases: [domain-method-regression](../../skills/en/testing-types/ai-agent-testing/evals/cases/domain-method-regression.yaml) — ai-agent-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 025. `ai-assisted-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/ai-assisted-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-assisted-testing/SKILL.md)

- First-review recommendation: Add sanitized-input and draft/adoption provenance, baseline time/rework measures, and assertions for review responsibilities and acceptance.
- Changed: Record input classification, sanitization, and allowed use. Replace identities, tokens, and personal data with non-reversible placeholders while retaining schema/business constraints. Trace input snapshot→model/prompt version→AI draft ID→Human review→adopted version ID→acceptance evidence. Drafts do not automatically become execution assets.
- New cases: [domain-method-regression](../../skills/en/testing-types/ai-assisted-testing/evals/cases/domain-method-regression.yaml) — ai-assisted-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 026. `ai-feature-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/ai-feature-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-feature-testing/SKILL.md)

- First-review recommendation: Add product/language/user slices, labeled rubrics, separate refusal/fallback gates, and model/prompt/data identities; thresholds remain project-supplied.
- Changed: Fix model, prompt, knowledge/evaluation data, product, and environment versions. Slice by product task×language×user group×risk, recording sample provenance/counts; aggregates cannot hide minority groups. Give Human rubric dimensions observable anchors, labelers, disagreement handling, and reference provenance. Calibrate examples before project-defined scores/weights; undefined scoring stays open.
- New cases: [domain-method-regression](../../skills/en/testing-types/ai-feature-testing/evals/cases/domain-method-regression.yaml) — ai-feature-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 027. `ai-generated-test-review` (P2)

Location: [ZH](../../skills/zh/testing-types/ai-generated-test-review/SKILL.md) · [EN](../../skills/en/testing-types/ai-generated-test-review/SKILL.md)

- First-review recommendation: Calibrate false positives using legitimate boundary mocks, meaningful snapshots, and valid status-only checks; align bilingual classifications.
- Changed: Evaluate assertions against the actual contract; mock, snapshot, or status-only syntax alone does not imply WEAK/FAKE. A boundary mock may replace a confirmed external dependency while real production logic executes. Mocking the subject itself and asserting its preset return offers no protection.
- New cases: [domain-method-regression](../../skills/en/testing-types/ai-generated-test-review/evals/cases/domain-method-regression.yaml) — ai-generated-test-review: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 028. `ai-safety-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/ai-safety-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-safety-testing/SKILL.md)

- First-review recommendation: Map versioned policies to allow/restrict/refuse/escalate decisions and test harmful cases alongside benign controls and over-refusal.
- Changed: Fix policy ID/version/audience and map category/conditions→allow/restrict/refuse/escalate→allowed content/prohibited effects→evidence. Missing policy cannot become a safety approval. Pair policy-defined harmful cases with neighboring benign controls. Assess harmful handling, allowed-task completion, and over-refusal independently; refusal rate alone is no safety metric.
- New cases: [domain-method-regression](../../skills/en/testing-types/ai-safety-testing/evals/cases/domain-method-regression.yaml) — ai-safety-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 029. `api-contract-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/api-contract-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-contract-testing/SKILL.md)

- First-review recommendation: Test old/new schemas and old consumers; distinguish schema compatibility, semantic incompatibility, and unknown migration behavior.
- Changed: Read contract semantic/schema and migration boundaries. Fixtures make amount-unit impact calculable and supply a tolerant-consumer positive control.
- New cases: [review-compatible-additive-control](../../skills/en/testing-types/api-contract-testing/evals/cases/review-compatible-additive-control.yaml) — Optional field addition does not break tolerant consumer; [review-schema-versus-semantics](../../skills/en/testing-types/api-contract-testing/evals/cases/review-schema-versus-semantics.yaml) — Unchanged integer schema can break old consumer semantics.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 030. `api-design-quality-review` (P2)

Location: [ZH](../../skills/zh/testing-types/api-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/api-design-quality-review/SKILL.md)

- First-review recommendation: Use OpenAPI diffs and a complete-design control; separate verified design conflicts from missing evidence and consumer migration questions.
- Changed: Read API finding contract. Real old/new OpenAPI models identify field-path conflict, and complete read-operation control prevents unrelated generic-domain blockers.
- New cases: [review-complete-operation-control](../../skills/en/testing-types/api-design-quality-review/evals/cases/review-complete-operation-control.yaml) — A complete scoped operation permits no blocking design findings; [review-openapi-consumer-diff](../../skills/en/testing-types/api-design-quality-review/evals/cases/review-openapi-consumer-diff.yaml) — OpenAPI diff distinguishes confirmed conflict from migration gap.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 031. `api-error-contract-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-error-contract-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-error-contract-testing/SKILL.md)

- First-review recommendation: Add error-specific checks for statuses, codes, fields, correlation IDs, retry semantics, and redaction; test cross-operation inconsistencies.
- Changed: Build an operation/error contract table for HTTP status, business code, required fields/types, correlation ID, retry meaning, and redaction; retain sourced operation exceptions. Match each response to its request, log, and contract version and compare fields; correlate one interaction without requiring different requests to reuse an ID.
- New cases: [domain-method-control](../../skills/en/testing-types/api-error-contract-testing/evals/cases/domain-method-control.yaml) — api-error-contract-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-error-contract-testing/evals/cases/domain-method-success.yaml) — api-error-contract-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 032. `api-idempotency-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-idempotency-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-idempotency-testing/SKILL.md)

- First-review recommendation: Define same-key payload, concurrency, expiry, and timeout-retry cases; distinguish response reuse from exactly-once business effects.
- Changed: Extract key scope, payload equivalence, lifetime/expiry boundary, concurrency, and replay contracts. Separate response replay from order/payment/message side-effect obligations. Build same-key/same-payload, same-key/different-payload, different-key, concurrency, expiry, and timeout-after-commit scenarios with initial state and project expectations.
- New cases: [domain-method-control](../../skills/en/testing-types/api-idempotency-testing/evals/cases/domain-method-control.yaml) — api-idempotency-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-idempotency-testing/evals/cases/domain-method-success.yaml) — api-idempotency-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 033. `api-negative-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-negative-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-negative-testing/SKILL.md)

- First-review recommendation: Add source-backed invalid-input classes and valid controls; verify rejection contracts and absence of business side effects without invented statuses.
- Changed: Extract field types, required/null rules, ranges, length encoding, payload limits, identity/permission rules, and error contracts with sources. Derive missing, null, empty, wrong-type, out-of-range, oversized, and unauthorized candidates. Isolate one violated constraint when possible; label combined violations separately.
- New cases: [domain-method-control](../../skills/en/testing-types/api-negative-testing/evals/cases/domain-method-control.yaml) — api-negative-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-negative-testing/evals/cases/domain-method-success.yaml) — api-negative-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 034. `api-pagination-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-pagination-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-pagination-testing/SKILL.md)

- First-review recommendation: Specify stable ordering, tie-breakers, page edges, cursor behavior, and duplicate/gap oracles using ordered-ID fixtures.
- Changed: Extract page size, offset/cursor, sort direction, unique tie-breaker, snapshot/live-change semantics, and cursor binding/expiry rules. Sort one snapshot into the expected ID sequence and derive first/middle/last/empty pages, resolving equal primary keys using the supplied tie-breaker.
- New cases: [domain-method-control](../../skills/en/testing-types/api-pagination-testing/evals/cases/domain-method-control.yaml) — api-pagination-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-pagination-testing/evals/cases/domain-method-success.yaml) — api-pagination-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 035. `api-rate-limit-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-rate-limit-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-rate-limit-testing/SKILL.md)

- First-review recommendation: Add quota-edge, burst, window-transition, isolation, and recovery procedures; test time-series results and 429/Retry-After behavior.
- Changed: Extract algorithm, quota N, window/time source, burst allowance, counted events, user/tenant/route scope, and reset rules. Build timed N-1/N/N+1, burst, window-boundary, separate-subject, and recovery scenarios. Recalculate sliding windows/token buckets from their own contracts.
- New cases: [domain-method-control](../../skills/en/testing-types/api-rate-limit-testing/evals/cases/domain-method-control.yaml) — api-rate-limit-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-rate-limit-testing/evals/cases/domain-method-success.yaml) — api-rate-limit-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 036. `api-schema-validation` (P1)

Location: [ZH](../../skills/zh/testing-types/api-schema-validation/SKILL.md) · [EN](../../skills/en/testing-types/api-schema-validation/SKILL.md)

- First-review recommendation: Identify schema dialect/version and verify required/null, extra properties, composition, and references using valid/invalid sample pairs.
- Changed: Identify OpenAPI/JSON Schema/GraphQL and its version/dialect, operation/direction, content type, reference root and resolution context. Suspend version-dependent decisions when unknown. For JSON Schema/OpenAPI schemas, separate required from nullability, types/ranges and additionalProperties, interpreting combinations/references under that version without mixing nullable syntax. For GraphQL use its input/output types and non-null rules, not JSON Schema keywords.
- New cases: [domain-method-control](../../skills/en/testing-types/api-schema-validation/evals/cases/domain-method-control.yaml) — api-schema-validation: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-schema-validation/evals/cases/domain-method-success.yaml) — api-schema-validation: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 037. `api-security-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-security-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-security-testing/SKILL.md)

- First-review recommendation: Add API-specific asset, object/property/function permission, resource-use, and trust-boundary procedures while retaining static review limits.
- Changed: Map supplied endpoints, subjects, resources, actions, sensitive fields and trust boundaries, distinguishing server-derived identity from client-controlled input. Expand allow/deny controls for object, field and function permissions, including ownership, tenant and delegation. Authentication does not establish resource permission.
- New cases: [domain-method-control](../../skills/en/testing-types/api-security-testing/evals/cases/domain-method-control.yaml) — api-security-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-security-testing/evals/cases/domain-method-success.yaml) — api-security-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 038. `api-test-bruno` (P1)

Location: [ZH](../../skills/zh/testing-types/api-test-bruno/SKILL.md) · [EN](../../skills/en/testing-types/api-test-bruno/SKILL.md)

- First-review recommendation: Fix single-brace baseUrl rendering, invented bodies, permissive status assertions, and lossy parsing; verify generated artifacts against golden fixtures.
- Changed: Bruno source parsing preserves method, URL, headers/body, and scenarios; generated assertions require sourced expectations, while missing data or complex schemas fail as incomplete scaffolds; permissive status checks and invented samples were removed.
- New cases: [review-repair-regression](../../skills/en/testing-types/api-test-bruno/evals/cases/review-repair-regression.yaml) — api-test-bruno: sourced repair regression.
- Second review/verification: Source → normalized JSON → generated project executed: good passes, wrong-status/wrong-body fail; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 039. `api-test-postman` (P2)

Location: [ZH](../../skills/zh/testing-types/api-test-postman/SKILL.md) · [EN](../../skills/en/testing-types/api-test-postman/SKILL.md)

- First-review recommendation: Validate collection artifacts, variable scopes, token extraction, and cleanup; test missing expectations rather than checking report words alone.
- Changed: Read Postman assets/output contract. Concrete v2.1 Collection and environment expose variable-shadowing and extraction defects; separate no-oracle case constrains false passing tests.
- New cases: [review-collection-auth-cleanup](../../skills/en/testing-types/api-test-postman/evals/cases/review-collection-auth-cleanup.yaml) — Collection auth scope and cleanup have observable contracts; [review-unknown-expectation](../../skills/en/testing-types/api-test-postman/evals/cases/review-unknown-expectation.yaml) — Missing business expectation cannot produce an always-passing assertion.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 040. `api-test-pytest` (P1)

Location: [ZH](../../skills/zh/testing-types/api-test-pytest/SKILL.md) · [EN](../../skills/en/testing-types/api-test-pytest/SKILL.md)

- First-review recommendation: Replace always-true empty checks and broad status allowlists with contract-derived or explicitly incomplete assertions; test empty and invalid responses.
- Changed: Pytest source parsing preserves method, URL, headers/body, and scenarios; generated assertions require sourced expectations, while missing data or complex schemas fail as incomplete scaffolds; permissive status checks and invented samples were removed.
- New cases: [review-repair-regression](../../skills/en/testing-types/api-test-pytest/evals/cases/review-repair-regression.yaml) — api-test-pytest: sourced repair regression.
- Second review/verification: Source → normalized JSON → generated project executed: good passes, wrong-status/wrong-body fail; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 041. `api-test-restassure` (P1)

Location: [ZH](../../skills/zh/testing-types/api-test-restassure/SKILL.md) · [EN](../../skills/en/testing-types/api-test-restassure/SKILL.md)

- First-review recommendation: Use contract-derived status/body assertions, supplied latency limits, and meaningful nonempty checks; validate compilation and failure sensitivity.
- Changed: REST Assured source parsing preserves method, URL, headers/body, and scenarios; generated assertions require sourced expectations, while missing data or complex schemas fail as incomplete scaffolds; permissive status checks and invented samples were removed.
- New cases: [review-repair-regression](../../skills/en/testing-types/api-test-restassure/evals/cases/review-repair-regression.yaml) — api-test-restassure: sourced repair regression.
- Second review/verification: Source → normalized JSON → generated project executed: good passes, wrong-status/wrong-body fail; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 042. `api-test-supertest` (P1)

Location: [ZH](../../skills/zh/testing-types/api-test-supertest/SKILL.md) · [EN](../../skills/en/testing-types/api-test-supertest/SKILL.md)

- First-review recommendation: Preserve request bodies and expected outcomes, replace broad status acceptance, distinguish app/baseUrl modes, and test failure-sensitive artifacts.
- Changed: Supertest source parsing preserves method, URL, headers/body, and scenarios; generated assertions require sourced expectations, while missing data or complex schemas fail as incomplete scaffolds; permissive status checks and invented samples were removed.
- New cases: [review-repair-regression](../../skills/en/testing-types/api-test-supertest/evals/cases/review-repair-regression.yaml) — api-test-supertest: sourced repair regression.
- Second review/verification: Source → normalized JSON → generated project executed: good passes, wrong-status/wrong-body fail; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 043. `api-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/api-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-testing/SKILL.md)

- First-review recommendation: Add protocol-specific branches and cross-request business postconditions/cleanup; test correct statuses with incorrect persisted business state.
- Changed: Branch only for confirmed protocols: REST method/status/schema/idempotency; GraphQL data+errors/null/field permissions; gRPC status/metadata/deadline/stream termination; WebSocket handshake/message IDs/order/reconnect; SOAP WSDL/namespaces/Fault. Do not require unused protocols. Separate contract checks from cross-request business postconditions: create/update→read-back→permission view→repeat/downstream effects. Preserve request IDs, business keys, versions, and evidence.
- New cases: [domain-method-regression](../../skills/en/testing-types/api-testing/evals/cases/domain-method-regression.yaml) — api-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 044. `api-version-compatibility-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/api-version-compatibility-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-version-compatibility-testing/SKILL.md)

- First-review recommendation: Add wire/schema/semantic compatibility and deprecation procedures; test old/new client and server combinations with explicit consumer tolerance.
- Changed: Identify contract/client/server versions, support/deprecation timeline and migration order; build applicable old/new client by old/new server combinations. Compare wire fields/types, requiredness, enums, defaults, errors and semantic units in each direction. Additive compatibility depends on actual client tolerance, not an assumed ignore-unknown policy.
- New cases: [domain-method-control](../../skills/en/testing-types/api-version-compatibility-testing/evals/cases/domain-method-control.yaml) — api-version-compatibility-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/api-version-compatibility-testing/evals/cases/domain-method-success.yaml) — api-version-compatibility-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 045. `authentication-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/authentication-testing/SKILL.md) · [EN](../../skills/en/testing-types/authentication-testing/SKILL.md)

- First-review recommendation: Add credential lifecycle, MFA, recovery, replay, enumeration, and lockout state procedures; distinguish identity authentication from authorization.
- Changed: Model unauthenticated, challenged, authenticated, locked and recovery states for supplied password/MFA/recovery/federation mechanisms, with creation/rotation/expiry/revocation/replay rules. Derive valid/invalid credentials, incomplete challenges, MFA replay, lock boundaries, recovery-token use and expiry scenarios; do not invent attempt limits, lifetimes or mandatory MFA policy.
- New cases: [domain-method-control](../../skills/en/testing-types/authentication-testing/evals/cases/domain-method-control.yaml) — authentication-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/authentication-testing/evals/cases/domain-method-success.yaml) — authentication-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 046. `authorization-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/authorization-testing/SKILL.md) · [EN](../../skills/en/testing-types/authorization-testing/SKILL.md)

- First-review recommendation: Add ownership/tenant/delegation permission matrices, horizontal/vertical escalation, revocation, and deny-default checks using paired allow/deny fixtures.
- Changed: Extract subject roles, ownership, tenant, actions, fields, delegation scope/lifetime and revocation rules; build allow/deny/unknown cells. Derive horizontal/vertical boundaries by changing subject, resource/tenant or privilege-sensitive action, with permitted controls.
- New cases: [domain-method-control](../../skills/en/testing-types/authorization-testing/evals/cases/domain-method-control.yaml) — authorization-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/authorization-testing/evals/cases/domain-method-success.yaml) — authorization-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 047. `automation-roi-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/automation-roi-analysis/SKILL.md) · [EN](../../skills/en/testing-types/automation-roi-analysis/SKILL.md)

- First-review recommendation: Add unit/time-window definitions, break-even calculations, and frequency/change-rate sensitivity using reproducible numeric fixtures.
- Changed: Fix candidate, window, and units. Separate Human time, machine occupancy, review, maintenance, and money; conversions need sourced rates. For one window, net saving = runs×(manual cost/run−automated cost/run)−maintenance−build cost. Define ROI numerator/denominator; absent monetary conversion, report labor only.
- New cases: [domain-method-regression](../../skills/en/testing-types/automation-roi-analysis/evals/cases/domain-method-regression.yaml) — automation-roi-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 048. `automation-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/automation-testing/SKILL.md) · [EN](../../skills/en/testing-types/automation-testing/SKILL.md)

- First-review recommendation: Make selection gates, isolation/cleanup, failure signals, and business postconditions explicit; verify evidence-based reasons to defer automation.
- Changed: Select using candidate flow | protection obligation | repeat-frequency evidence | oracle/observability | isolation/cleanup | stability | maintenance constraint | adopt/defer rationale. Keep ROI cost scenarios separate; returns cannot remedy missing oracles or authority. Reuse the existing framework. First require observable postconditions, independent data, and a CI entry that propagates failure. Defer unmet candidates with unblock conditions.
- New cases: [domain-method-regression](../../skills/en/testing-types/automation-testing/evals/cases/domain-method-regression.yaml) — automation-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 049. `boundary-value-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/boundary-value-testing/SKILL.md) · [EN](../../skills/en/testing-types/boundary-value-testing/SKILL.md)

- First-review recommendation: Define inclusive/exclusive boundaries, representable steps, encoding, precision, and time units; test expected neighbors and unknown precision.
- Changed: Extract bounds, inclusive/exclusive rules, discrete/continuous type, smallest representable step, length encoding, money precision, time unit/timezone and sources. For known discrete boundaries choose inside neighbors, the boundary and outside neighbors. Integer step 1 cannot be applied to decimals, byte lengths or time blindly.
- New cases: [domain-method-control](../../skills/en/testing-types/boundary-value-testing/evals/cases/domain-method-control.yaml) — boundary-value-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/boundary-value-testing/evals/cases/domain-method-success.yaml) — boundary-value-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 050. `bug-reporting` (P2)

Location: [ZH](../../skills/zh/testing-types/bug-reporting/SKILL.md) · [EN](../../skills/en/testing-types/bug-reporting/SKILL.md)

- First-review recommendation: Check expectation sources, minimal reproduction, sanitized evidence, severity versus priority, and preservation of observed frequency.
- Changed: Reviewed bug-report fields and uncertainty rules. Real repro/expectation fixture distinguishes observed duplication from billing loss and preserves non-deterministic frequency.
- New cases: [review-expected-source-missing](../../skills/en/testing-types/bug-reporting/evals/cases/review-expected-source-missing.yaml) — Observed anomaly does not invent an expectation source; [review-frequency-and-priority](../../skills/en/testing-types/bug-reporting/evals/cases/review-frequency-and-priority.yaml) — Bug facts preserve frequency and severity/priority distinction.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 051. `business-rule-extraction` (P2)

Location: [ZH](../../skills/zh/testing-types/business-rule-extraction/SKILL.md) · [EN](../../skills/en/testing-types/business-rule-extraction/SKILL.md)

- First-review recommendation: Test tables, exception precedence, and contradictory documents; preserve conditions, actions, scope, and unknown business rules.
- Changed: Read BR field contract and no-invention rule. Actual table/date/scope and two same-scope sources make rule preservation and conflict attribution observable; control isolates valid shipping rules.
- New cases: [review-complete-rule-control](../../skills/en/testing-types/business-rule-extraction/evals/cases/review-complete-rule-control.yaml) — A complete supplied rule is not rewritten by assumed policy; [review-table-exception-conflict](../../skills/en/testing-types/business-rule-extraction/evals/cases/review-table-exception-conflict.yaml) — Atomic rules preserve table conditions, exception and source conflict.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 052. `capacity-planning-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/capacity-planning-analysis/SKILL.md) · [EN](../../skills/en/testing-types/capacity-planning-analysis/SKILL.md)

- First-review recommendation: Use reproducible throughput/latency/resource scenarios and scaling-delay/failure headroom; reject capacity extrapolation from CPU percentage alone.
- Changed: For each point record environment/config/instances, workload mix, arrival/completion throughput, latency percentiles, errors, CPU/memory/queues, and window. Trace measurement→SLO→candidate capacity. Estimate only within measured SLO-acceptable regions. CPU percentage cannot linearly predict throughput; unmeasured points remain candidates constrained by downstream saturation/scaling delay.
- New cases: [domain-method-regression](../../skills/en/testing-types/capacity-planning-analysis/evals/cases/domain-method-regression.yaml) — capacity-planning-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 053. `change-impact-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/change-impact-analysis/SKILL.md) · [EN](../../skills/en/testing-types/change-impact-analysis/SKILL.md)

- First-review recommendation: Add change/dependency/obligation evidence graphs and traversal limits; test unknown dynamic dependencies and conservative validation scope.
- Changed: Fix change version/scope and build typed changed file/symbol/config→dependent→business obligation→test ID evidence edges with source/version and confirmed/candidate/unknown states. Traverse direct/transitive consumers with cycle deduplication. Stop only at evidenced contract isolation/no-consumer boundaries and record why; directories alone are no boundary.
- New cases: [domain-method-regression](../../skills/en/testing-types/change-impact-analysis/evals/cases/domain-method-regression.yaml) — change-impact-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 054. `chaos-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/chaos-testing/SKILL.md) · [EN](../../skills/en/testing-types/chaos-testing/SKILL.md)

- First-review recommendation: Add steady-state hypotheses, controls, injection scope, blast radius, measurable abort criteria, and recovery evidence; block incomplete experiment designs.
- Changed: Express steady-state hypotheses as metrics, windows, baseline/control groups and business invariants; state the disruption's proposed causal chain. Specify injection point, fault/duration, instance/traffic fraction, isolated environment, dependencies and blast radius, including authorized and excluded targets.
- New cases: [domain-method-control](../../skills/en/testing-types/chaos-testing/evals/cases/domain-method-control.yaml) — chaos-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/chaos-testing/evals/cases/domain-method-success.yaml) — chaos-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 055. `ci-test-optimization` (P2)

Location: [ZH](../../skills/zh/testing-types/ci-test-optimization/SKILL.md) · [EN](../../skills/en/testing-types/ci-test-optimization/SKILL.md)

- First-review recommendation: Decompose queue/setup/run/retry time, critical paths, and cache validity; test improvements without dropping protection or hiding failures.
- Changed: Fix commit/run/runner/config/test-set identities. Decompose events into queue, checkout/install, setup, execute, retry, and report; separate end-to-end waiting from runner busy time. Compute the actual DAG critical path without summing overlapping jobs. Preserve retry counts and original failures; retry green cannot erase first failure.
- New cases: [domain-method-regression](../../skills/en/testing-types/ci-test-optimization/evals/cases/domain-method-regression.yaml) — ci-test-optimization: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 056. `circuit-breaker-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/circuit-breaker-testing/SKILL.md) · [EN](../../skills/en/testing-types/circuit-breaker-testing/SKILL.md)

- First-review recommendation: Define breaker transition windows, thresholds, probe budgets, failed recovery, and concurrent probes; verify event-sequence outcomes.
- Changed: Extract failure-count definitions, rolling/consecutive window, threshold, open duration, half-open probe/concurrency allowance, and success/failure transitions. Build timed request-identified closed→open→half-open→closed/open event tables, updating counts/state per event without inventing thresholds.
- New cases: [domain-method-control](../../skills/en/testing-types/circuit-breaker-testing/evals/cases/domain-method-control.yaml) — circuit-breaker-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/circuit-breaker-testing/evals/cases/domain-method-success.yaml) — circuit-breaker-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 057. `code-review` (P2)

Location: [ZH](../../skills/zh/testing-types/code-review/SKILL.md) · [EN](../../skills/en/testing-types/code-review/SKILL.md)

- First-review recommendation: Add correct patches and apparent-risk cases with visible upstream safeguards to calibrate false positives and valid no-finding outcomes.
- Changed: Read code identity/reviewable-change gates and empty severity-list contract. Correct equivalent patch and guarded helper are controls; reachable removed guard is the positive defect.
- New cases: [review-correct-patch-control](../../skills/en/testing-types/code-review/evals/cases/review-correct-patch-control.yaml) — Equivalent correct patch permits empty finding lists; [review-reachable-null-defect](../../skills/en/testing-types/code-review/evals/cases/review-reachable-null-defect.yaml) — A reachable removed guard still yields a located finding; [review-upstream-guard-control](../../skills/en/testing-types/code-review/evals/cases/review-upstream-guard-control.yaml) — Visible upstream guard prevents a false index finding.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 058. `combinatorial-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/combinatorial-testing/SKILL.md) · [EN](../../skills/en/testing-types/combinatorial-testing/SKILL.md)

- First-review recommendation: Add factor/value/constraint modeling, interaction-strength selection, valid-combination generation, and coverage verification on enumerable fixtures.
- Changed: Build sourced factor/value tables and constraints, distinguishing input, environment and state; do not invent binary domains for unknown values. Choose t-way strength from defect/risk evidence, explaining t>=3 for higher-order obligations. Pairwise coverage cannot replace a known three-factor risk.
- New cases: [domain-method-control](../../skills/en/testing-types/combinatorial-testing/evals/cases/domain-method-control.yaml) — combinatorial-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/combinatorial-testing/evals/cases/domain-method-success.yaml) — combinatorial-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 059. `cross-browser-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/cross-browser-testing/SKILL.md) · [EN](../../skills/en/testing-types/cross-browser-testing/SKILL.md)

- First-review recommendation: Add risk-selected engine/platform/version matrices and real-device versus emulation evidence; test WebKit-specific support differences.
- Changed: Map project support and user distribution to engine/platform/version/device cells, retaining real-browser/device, emulator and automation-engine identities. Sample by risky journeys, known engine differences and user weight. Multiple Chromium browsers do not establish WebKit/Gecko obligations.
- New cases: [domain-method-control](../../skills/en/testing-types/cross-browser-testing/evals/cases/domain-method-control.yaml) — cross-browser-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/cross-browser-testing/evals/cases/domain-method-success.yaml) — cross-browser-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 060. `database-design-quality-review` (P2)

Location: [ZH](../../skills/zh/testing-types/database-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/database-design-quality-review/SKILL.md)

- First-review recommendation: Test staged online migrations and mixed-version deployment, including locks, defaults, rollback, and access patterns, with correct-schema controls.
- Changed: Read DB constraint/access/migration/rollback contract. Mixed-version DDL has explicit old-writer evidence and unmeasured lock budget; valid scoped schema controls false positives.
- New cases: [review-online-mixed-version-migration](../../skills/en/testing-types/database-design-quality-review/evals/cases/review-online-mixed-version-migration.yaml) — Online migration must explain coexistence, lock evidence and rollback; [review-valid-schema-control](../../skills/en/testing-types/database-design-quality-review/evals/cases/review-valid-schema-control.yaml) — Explicit constraints and access paths are not missing defects.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 061. `decision-table-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/decision-table-testing/SKILL.md) · [EN](../../skills/en/testing-types/decision-table-testing/SKILL.md)

- First-review recommendation: Specify condition partitioning, overlap/gap detection, don't-care handling, and precedence; verify an explicit four-combination table.
- Changed: Discretize continuous conditions into sourced mutually exclusive ranges/categories and list domains, actions, exceptions and precedence; do not force vague conditions into booleans. Enumerate legal combinations for small models and match rules, checking no match, conflicting multiple matches, exclusive conditions and unreachable rules.
- New cases: [domain-method-control](../../skills/en/testing-types/decision-table-testing/evals/cases/domain-method-control.yaml) — decision-table-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/decision-table-testing/evals/cases/domain-method-success.yaml) — decision-table-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 062. `dependency-failure-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/dependency-failure-testing/SKILL.md) · [EN](../../skills/en/testing-types/dependency-failure-testing/SKILL.md)

- First-review recommendation: Add synchronous/asynchronous dependency failure matrices for timeout, slowness, errors, and partial success; verify caller state and recovery.
- Changed: Map caller/dependency, synchronous/asynchronous mode, timeout/retry/fallback contracts and required business/data invariants. Build unreachable, timeout, slow, error and partial-success matrices; add delay/duplicate/reordering/acknowledgment for async paths without borrowing synchronous status expectations.
- New cases: [domain-method-control](../../skills/en/testing-types/dependency-failure-testing/evals/cases/domain-method-control.yaml) — dependency-failure-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/dependency-failure-testing/evals/cases/domain-method-success.yaml) — dependency-failure-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 063. `disaster-recovery-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/disaster-recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/disaster-recovery-testing/SKILL.md)

- First-review recommendation: Define RTO/RPO measurements, backup points, dependency restore order, and post-restore consistency using timestamped recovery fixtures.
- Changed: Identify primary/recovery regions, failure scope, RTO/RPO start/end definitions, acceptable loss and business restoration criteria from contracts; do not invent targets. Check backup points and supplied integrity/decryption/restore evidence plus access dependencies; backup existence is not recoverability.
- New cases: [domain-method-control](../../skills/en/testing-types/disaster-recovery-testing/evals/cases/domain-method-control.yaml) — disaster-recovery-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/disaster-recovery-testing/evals/cases/domain-method-success.yaml) — disaster-recovery-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 064. `distributed-trace-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/distributed-trace-analysis/SKILL.md) · [EN](../../skills/en/testing-types/distributed-trace-analysis/SKILL.md)

- First-review recommendation: Check parent/link relationships, overlapping spans, exclusive time, and queues; test incomplete traces without summing overlaps or inventing root causes.
- Changed: Fix trace/span IDs, parent IDs, asynchronous links, service/deployment versions, timestamps, and sampling scope. Check nesting and clock skew; a link is not automatically synchronous parentage. Within one clock domain, subtract the union of synchronous child intervals to obtain observed exclusive time; overlapping children are not additive. Missing spans limit this to observed intervals, not true exclusive work.
- New cases: [domain-method-regression](../../skills/en/testing-types/distributed-trace-analysis/evals/cases/domain-method-regression.yaml) — distributed-trace-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 065. `edge-case-discovery` (P2)

Location: [ZH](../../skills/zh/testing-types/edge-case-discovery/SKILL.md) · [EN](../../skills/en/testing-types/edge-case-discovery/SKILL.md)

- First-review recommendation: Use deterministic encoding, timezone, and concurrency fixtures with source-linked candidates and controls against unsupported edge-case expansion.
- Changed: Read EC dimensions and candidate-only boundaries. Explicit codepoint/UTF-8, offset and order fixtures provide calculable oracles and normal-value control.
- New cases: [review-bytes-time-order-boundaries](../../skills/en/testing-types/edge-case-discovery/evals/cases/review-bytes-time-order-boundaries.yaml) — Boundary candidates retain exact units, timezone and event order; [review-normal-boundary-control](../../skills/en/testing-types/edge-case-discovery/evals/cases/review-normal-boundary-control.yaml) — A normal example is not a proven boundary failure.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 066. `equivalence-partitioning` (P1)

Location: [ZH](../../skills/zh/testing-types/equivalence-partitioning/SKILL.md) · [EN](../../skills/en/testing-types/equivalence-partitioning/SKILL.md)

- First-review recommendation: Define behavioral equivalence, disjointness/completeness, dependent classes, and representative selection using region/postcode fixtures.
- Changed: Partition by sourced equivalent behavior/errors and constraints, not input shape alone; invalid classes with different responses must remain distinct. Check disjointness/completeness within the supplied domain and retain unclassified values; express dependencies as joint region/postcode or role/action classes.
- New cases: [domain-method-control](../../skills/en/testing-types/equivalence-partitioning/evals/cases/domain-method-control.yaml) — equivalence-partitioning: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/equivalence-partitioning/evals/cases/domain-method-success.yaml) — equivalence-partitioning: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 067. `error-handling-design-review` (P2)

Location: [ZH](../../skills/zh/testing-types/error-handling-design-review/SKILL.md) · [EN](../../skills/en/testing-types/error-handling-design-review/SKILL.md)

- First-review recommendation: Test retryable versus permanent failures and timeout-after-commit designs, preserving consumer contracts, compensation, and propagation evidence.
- Changed: Read EH caller-visible/result/evidence contract. Retry modes include committed-after-timeout and a propagated identity chain; complete read-only control prevents blanket write-recovery findings.
- New cases: [review-reliable-error-control](../../skills/en/testing-types/error-handling-design-review/evals/cases/review-reliable-error-control.yaml) — Existing bounded retry controls are not blanket defects; [review-retry-partial-commit](../../skills/en/testing-types/error-handling-design-review/evals/cases/review-retry-partial-commit.yaml) — Retry classes preserve commit and layered propagation.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 068. `failover-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/failover-testing/SKILL.md) · [EN](../../skills/en/testing-types/failover-testing/SKILL.md)

- First-review recommendation: Add trigger/detection, routing, fencing, split-brain, timing, and failback procedures; test partition-induced dual writes.
- Changed: Extract primary/standby roles, automatic/manual triggers, health detection, routing, fencing/write authority, failback and business-RTO definitions. Build partition timelines for detection, election, old-primary isolation, routing and readiness, tracking writers and request destinations per phase.
- New cases: [domain-method-control](../../skills/en/testing-types/failover-testing/evals/cases/domain-method-control.yaml) — failover-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/failover-testing/evals/cases/domain-method-success.yaml) — failover-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 069. `flaky-test-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/flaky-test-analysis/SKILL.md) · [EN](../../skills/en/testing-types/flaky-test-analysis/SKILL.md)

- First-review recommendation: Use seeded worker/run fixtures, frequency denominators, and controlled experiments; verify accountable, time-bounded quarantine remains visible.
- Changed: Read flakiness/reproduction/quarantine contract. Ten actual rows expose seed×worker confounding and provide all ratio denominators; control prevents invented flakiness.
- New cases: [review-seed-worker-experiment](../../skills/en/testing-types/flaky-test-analysis/evals/cases/review-seed-worker-experiment.yaml) — Flaky ratios and minimal experiments keep quarantine visible; [review-stable-control](../../skills/en/testing-types/flaky-test-analysis/evals/cases/review-stable-control.yaml) — A passing small sample is neither flaky proof nor zero-risk proof.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 070. `functional-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/functional-testing/SKILL.md) · [EN](../../skills/en/testing-types/functional-testing/SKILL.md)

- First-review recommendation: Fix inline-string and sparse-column loss in the bundled Excel parser, then test action-to-business-postcondition coverage.
- Changed: Added successful-response/wrong-persisted-state fixtures and valid controls; checks cover business postconditions, execution evidence, and gaps while preserving existing evals.
- New cases: [review-repair-regression](../../skills/en/testing-types/functional-testing/evals/cases/review-repair-regression.yaml) — functional-testing: sourced repair regression.
- Second review/verification: Contract/routing fixture and grader controls pass; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 071. `llm-consistency-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/llm-consistency-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-consistency-testing/SKILL.md)

- First-review recommendation: Separate structural invariants from allowed semantic variation; control run identity/parameters and test multi-run variance and intermittent failure.
- Changed: Fix sample ID, model/prompt/tool/data versions, temperature, seed where supported, and other sampling parameters, with project-supplied repetition counts. Equal seeds do not establish reproducibility across versions. Check structural invariants first: schema, required fields, enums, and policy. Then compare semantic decisions using the project rubric; permitted paraphrases/order changes are not failures.
- New cases: [domain-method-regression](../../skills/en/testing-types/llm-consistency-testing/evals/cases/domain-method-regression.yaml) — llm-consistency-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 072. `llm-evaluation-design` (P2)

Location: [ZH](../../skills/zh/testing-types/llm-evaluation-design/SKILL.md) · [EN](../../skills/en/testing-types/llm-evaluation-design/SKILL.md)

- First-review recommendation: Add rubric anchors, human disagreement, blinded ordering, contamination controls, dataset slices, and observable judge-calibration steps.
- Changed: Read LLM evaluation data/judge/statistical boundaries. Concrete duplicate data and rater disagreement exercise split handling, adjudication and blind ordering; valid protocol control constrains false positives.
- New cases: [review-contamination-and-calibration](../../skills/en/testing-types/llm-evaluation-design/evals/cases/review-contamination-and-calibration.yaml) — Evaluation design resolves contamination and judge disagreement; [review-disjoint-design-control](../../skills/en/testing-types/llm-evaluation-design/evals/cases/review-disjoint-design-control.yaml) — Disjoint splits with calibrated anchors do not invent leakage.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 073. `llm-hallucination-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/llm-hallucination-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-hallucination-testing/SKILL.md)

- First-review recommendation: Define supported/contradicted/missing-source/unassessable labels and test claim-level mappings for numbers, entities, and citations.
- Changed: Split independently checkable claims including numbers/units, entities, conditions, dates, and citations. Assign IDs, retaining original answer text and evidence version/location. SUPPORTED means evidence supports the same scope; CONTRADICTED means explicit opposing evidence; MISSING_SOURCE means no supplied support or direct contradiction; UNASSESSABLE means inaccessible, unclear-scope, or outdated evidence prevents comparison. Missing support alone does not prove fabrication.
- New cases: [domain-method-regression](../../skills/en/testing-types/llm-hallucination-testing/evals/cases/domain-method-regression.yaml) — llm-hallucination-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 074. `llm-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/llm-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-testing/SKILL.md)

- First-review recommendation: Replace heading-only evaluation with real samples, structural parsers, calibrated semantic rubrics, and repeated robustness/long-context checks.
- Changed: Read LLM repetition/settings/no-exact-string contract. Provided output strings expose JSON type failure, true semantic contradiction and paraphrase control; no model execution is claimed.
- New cases: [review-equivalent-safe-control](../../skills/en/testing-types/llm-testing/evals/cases/review-equivalent-safe-control.yaml) — Equivalent factual paraphrases do not count as regressions; [review-repeated-output-samples](../../skills/en/testing-types/llm-testing/evals/cases/review-repeated-output-samples.yaml) — LLM samples separate parser and calibrated semantic failures.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 075. `log-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/log-analysis/SKILL.md) · [EN](../../skills/en/testing-types/log-analysis/SKILL.md)

- First-review recommendation: Supply actual sanitized logs and deployment times; verify ordering, request correlation, clusters, gaps, and hypothesis-specific validation actions.
- Changed: Read log timezone/sampling/root-cause boundary. Deliberately unordered structured raw lines support deterministic order and request/error-count checks plus a normal-event control.
- New cases: [review-normal-log-control](../../skills/en/testing-types/log-analysis/evals/cases/review-normal-log-control.yaml) — Normal log sample does not invent incident or global health; [review-raw-log-timeline](../../skills/en/testing-types/log-analysis/evals/cases/review-raw-log-timeline.yaml) — Raw logs preserve UTC order, request correlation and missing segment.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 076. `manual-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/manual-testing/SKILL.md) · [EN](../../skills/en/testing-types/manual-testing/SKILL.md)

- First-review recommendation: Add time-boxed charters, data restoration, evidence notes, and unfinished states; test concrete limited-window execution plans.
- Changed: Give each time-box a charter: task/risk, environment/build, data, exploration scope, deadline, and evidence. Track scripted execution and exploration separately within authorization. Record precondition→action→expected→actual→evidence ID→state. Not started is NOT_RUN, interrupted is INCOMPLETE, environment prevention is BLOCKED; a checklist is no execution log.
- New cases: [domain-method-regression](../../skills/en/testing-types/manual-testing/evals/cases/domain-method-regression.yaml) — manual-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 077. `metamorphic-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/metamorphic-testing/SKILL.md) · [EN](../../skills/en/testing-types/metamorphic-testing/SKILL.md)

- First-review recommendation: Define source input, transformation, output relation, preconditions, and counterexamples; verify justified metamorphic relations on concrete fixtures.
- Changed: Define source input domain, transformation T, output relation R and sourced preconditions. An absent exact oracle does not permit arbitrary equivalence assumptions. Check both source/transformed constraints and flag semantic-changing transformations; distinguish equality, proportionality and monotonic relations.
- New cases: [domain-method-control](../../skills/en/testing-types/metamorphic-testing/evals/cases/domain-method-control.yaml) — metamorphic-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/metamorphic-testing/evals/cases/domain-method-success.yaml) — metamorphic-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 078. `metrics-anomaly-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/metrics-anomaly-analysis/SKILL.md) · [EN](../../skills/en/testing-types/metrics-anomaly-analysis/SKILL.md)

- First-review recommendation: Use unit-aware seasonal series with missing samples and explicit baseline windows; test dimensions and causal restraint without a baseline.
- Changed: Read metric definition/baseline/seasonality/causality contract. Real minute series makes unit, missing sample, dimension and non-pooled-percentile decisions explicit; seasonal/absent-baseline controls included.
- New cases: [review-seasonal-control-and-no-baseline](../../skills/en/testing-types/metrics-anomaly-analysis/evals/cases/review-seasonal-control-and-no-baseline.yaml) — Seasonal peak is not a deviation and missing baseline stays unknown; [review-unit-seasonal-missing-series](../../skills/en/testing-types/metrics-anomaly-analysis/evals/cases/review-unit-seasonal-missing-series.yaml) — Metric anomaly uses the supplied baseline and missing-value semantics.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 079. `mobile-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/mobile-testing/SKILL.md) · [EN](../../skills/en/testing-types/mobile-testing/SKILL.md)

- First-review recommendation: Add risk-selected OS/device/upgrade/network/lifecycle matrices and restoration oracles for deeplink parameters and interrupted payments.
- Changed: Select OS×device×install/upgrade×network×lifecycle combinations from distribution, changes, and incidents. Record samples and gaps; do not invent supported devices. Preserve raw deeplink URI, decoding policy, route/parameters, and authorization. Compare cold/warm/resume paths; restoration must not drop parameters or double-decode.
- New cases: [domain-method-regression](../../skills/en/testing-types/mobile-testing/evals/cases/domain-method-regression.yaml) — mobile-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 080. `mock-quality-review` (P1)

Location: [ZH](../../skills/zh/testing-types/mock-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/mock-quality-review/SKILL.md)

- First-review recommendation: Compare contract/stub fields, statuses, timing, error paths, drift, and mocked subject boundaries using legitimate and invalid mock controls.
- Changed: Identify the subject and external-collaborator boundary; map mock/stub version, fields, statuses, errors, timing and side effects to the real contract. Check whether the subject itself is replaced and assertions only confirm stub output/fixed interactions; mocks at a sound boundary are not defects merely for being mocks.
- New cases: [domain-method-control](../../skills/en/testing-types/mock-quality-review/evals/cases/domain-method-control.yaml) — mock-quality-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/mock-quality-review/evals/cases/domain-method-success.yaml) — mock-quality-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 081. `model-based-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/model-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/model-based-testing/SKILL.md)

- First-review recommendation: Specify states, guards, events, actions, reachability, and coverage objectives; verify derived paths from a small explicit model.
- Changed: Build sourced initial/terminal states, events, guards, actions, targets and persistence, rather than an arbitrary state list. Traverse from the initial state and list unreachable states/edges, conflicting transitions and undefined events; retain unsatisfied-guard reasons.
- New cases: [domain-method-control](../../skills/en/testing-types/model-based-testing/evals/cases/domain-method-control.yaml) — model-based-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/model-based-testing/evals/cases/domain-method-success.yaml) — model-based-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 082. `multi-agent-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/multi-agent-testing/SKILL.md) · [EN](../../skills/en/testing-types/multi-agent-testing/SKILL.md)

- First-review recommendation: Add delegation IDs, ownership, state versions, acknowledgments, and termination rules; test partial failure, duplicate ownership, and stale messages.
- Changed: Trace task/message/correlation IDs, sender/receiver, parent delegation, scope, owner, shared-state version, and ACK using actual acceptance/rejection/termination rules. Claim/commit follows the project's atomic ownership or fencing protocol. Stale/duplicate messages must not regain ownership or duplicate writes; never assume exactly-once delivery.
- New cases: [domain-method-regression](../../skills/en/testing-types/multi-agent-testing/evals/cases/domain-method-regression.yaml) — multi-agent-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 083. `mutation-testing-analysis` (P1)

Location: [ZH](../../skills/zh/testing-types/mutation-testing-analysis/SKILL.md) · [EN](../../skills/en/testing-types/mutation-testing-analysis/SKILL.md)

- First-review recommendation: Classify mutation outcomes and denominators explicitly; preserve operator/test mappings and verify scores without silently excluding unproven equivalents.
- Changed: Verify subject revision, operators, mutant IDs/locations, test mapping and budgets; distinguish killed, survived, no-coverage, timeout, error and pending equivalence. Read tool/project scoring and exclusion policies before reporting totals, numerator, denominator and exclusions. With no formula report distribution instead of inventing a single score.
- New cases: [domain-method-control](../../skills/en/testing-types/mutation-testing-analysis/evals/cases/domain-method-control.yaml) — mutation-testing-analysis: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/mutation-testing-analysis/evals/cases/domain-method-success.yaml) — mutation-testing-analysis: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 084. `negative-scenario-discovery` (P2)

Location: [ZH](../../skills/zh/testing-types/negative-scenario-discovery/SKILL.md) · [EN](../../skills/en/testing-types/negative-scenario-discovery/SKILL.md)

- First-review recommendation: Test timeout-after-success, compound failures, and failed recovery with explicit rejection/restoration/data-consistency expectations.
- Changed: Read NS trigger/handling/visible-result/consistency contract. Three supplied compound failures retain unknown contracts; safe rejection control prevents default invented defects.
- New cases: [review-partial-double-recovery-failures](../../skills/en/testing-types/negative-scenario-discovery/evals/cases/review-partial-double-recovery-failures.yaml) — Negative paths retain outcome-unknown and recovery consistency expectations; [review-rejected-invalid-control](../../skills/en/testing-types/negative-scenario-discovery/evals/cases/review-rejected-invalid-control.yaml) — Safe rejection is not an invented recovery defect.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 085. `observability-design-review` (P2)

Location: [ZH](../../skills/zh/testing-types/observability-design-review/SKILL.md) · [EN](../../skills/en/testing-types/observability-design-review/SKILL.md)

- First-review recommendation: Test high-cardinality labels and sampled trace breaks; require budget, correlation, and actionable alerts rather than keywords.
- Changed: Read OBS signal semantics/budget/privacy/actionability contract. Fixture includes calculable label bound, explicit missing propagation and action gap; complete control avoids blanket findings.
- New cases: [review-bounded-signal-control](../../skills/en/testing-types/observability-design-review/evals/cases/review-bounded-signal-control.yaml) — Explicit cardinality and propagation controls are recognized; [review-cardinality-and-broken-sampling](../../skills/en/testing-types/observability-design-review/evals/cases/review-cardinality-and-broken-sampling.yaml) — Signal design ties budget, correlation and alert action to evidence.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 086. `pairwise-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/pairwise-testing/SKILL.md) · [EN](../../skills/en/testing-types/pairwise-testing/SKILL.md)

- First-review recommendation: Generate and verify the valid pair universe under constraints, report gaps, and explicitly separate pairwise from higher-order protection.
- Changed: List sourced factors/domains/joint constraints and pairwise applicability, retaining higher-order obligations outside its guarantee. Enumerate/solve legal assignments and project each factor pair into the legal universe; verify extendability to a legal full assignment rather than removing only obvious invalid pairs.
- New cases: [domain-method-control](../../skills/en/testing-types/pairwise-testing/evals/cases/domain-method-control.yaml) — pairwise-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/pairwise-testing/evals/cases/domain-method-success.yaml) — pairwise-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 087. `performance-bottleneck-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-bottleneck-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-bottleneck-analysis/SKILL.md)

- First-review recommendation: Use staged load/resource fixtures and discriminating experiments; verify evidence-backed hypotheses rather than equating utilization with root cause.
- Changed: Read workload-first/multi-signal bottleneck contract. Real stage metrics distinguish offered from completed load and provide a pool-queue hypothesis with competing controls.
- New cases: [review-high-cpu-slow-span-control](../../skills/en/testing-types/performance-bottleneck-analysis/evals/cases/review-high-cpu-slow-span-control.yaml) — High CPU or one slow span is insufficient for bottleneck; [review-stage-pool-hypothesis](../../skills/en/testing-types/performance-bottleneck-analysis/evals/cases/review-stage-pool-hypothesis.yaml) — Throughput knee and queue evidence guide a discriminator.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 088. `performance-regression-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-regression-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-regression-analysis/SKILL.md)

- First-review recommendation: Assert comparability limits directly and use paired repeated runs for absolute/relative change, noise, and stable degradation.
- Changed: Read comparability/absolute-relative/noise contract. Three paired repeats per group support median arithmetic and consistent-direction versus variable observations; separate incompatible environment/workload case blocks attribution.
- New cases: [review-incomparable-load-control](../../skills/en/testing-types/performance-regression-analysis/evals/cases/review-incomparable-load-control.yaml) — Workload and environment differences block regression attribution; [review-paired-deltas](../../skills/en/testing-types/performance-regression-analysis/evals/cases/review-paired-deltas.yaml) — Paired repeats separate consistent shifts from zero-median variation.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 089. `performance-result-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-result-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-result-analysis/SKILL.md)

- First-review recommendation: Provide actual stage reports and goals; validate achieved load, samples, error denominators, steady state, and bounded conclusions.
- Changed: Read run-validity, stage-stability and workload-boundary contract. Actual warmup/steady report supplies target, achieved load and request denominator; passing steady control constrains false rejection.
- New cases: [review-met-target-control](../../skills/en/testing-types/performance-result-analysis/evals/cases/review-met-target-control.yaml) — A valid steady result can pass its explicit local target; [review-stage-targets-and-denominator](../../skills/en/testing-types/performance-result-analysis/evals/cases/review-stage-targets-and-denominator.yaml) — Actual stage result validates attained load and error denominator.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 090. `performance-test-gatling` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-test-gatling/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-gatling/SKILL.md)

- First-review recommendation: Validate open/closed injection models, achieved arrival rates, DSL/version compatibility, feeder exhaustion, and missing thresholds with offline compilation.
- Changed: Read project Gatling/plugin/JDK and Java/Scala/Kotlin DSL versions, retaining its layout. Use compatible injection/assertion APIs in one DSL. Offline test-compile generated assets with the project build; uncached dependencies mean BLOCKED, not a passed compile. Open models control user arrivals; arrivals equal request RPS only for one request per user without additional loops/retries. Closed models control concurrency; verify RPS from actual request counts/windows.
- New cases: [domain-method-regression](../../skills/en/testing-types/performance-test-gatling/evals/cases/domain-method-regression.yaml) — performance-test-gatling: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 091. `performance-test-jmeter` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-test-jmeter/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-jmeter/SKILL.md)

- First-review recommendation: Explain thread versus arrival-rate models; validate sanitized JMX, timers, distributed constraints, CSV lifecycle, and latency/error gates.
- Changed: Confirm project JMeter/JDK/plugins and JMX version. Check TestPlan/ThreadGroup/Sampler and adjacent hashTree structure, variables, and properties. Parseable XML proves structure only, not execution or SLO success. Standard ThreadGroup controls closed-loop threads. Target RPS needs declared think time/timers, throughput control, or an installed arrival-rate plugin; verify achieved throughput/counts rather than inferring RPS from threads.
- New cases: [domain-method-regression](../../skills/en/testing-types/performance-test-jmeter/evals/cases/domain-method-regression.yaml) — performance-test-jmeter: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 092. `performance-test-k6` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-test-k6/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-k6/SKILL.md)

- First-review recommendation: Test executor choice, dropped iterations, checks versus thresholds, request-body fidelity, and business postconditions in generated scripts.
- Changed: Read k6 input precedence/options/init-only and threshold contract. Package-local assertion parses generated options, checks JS syntax offline and rejects missing dropped/business gates; closed-user control protects model choice.
- New cases: [review-closed-model-control](../../skills/en/testing-types/performance-test-k6/evals/cases/review-closed-model-control.yaml) — Fixed-user workload is not forced into arrival-rate model; [review-offline-arrival-artifacts](../../skills/en/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml) — Offline k6 assets retain load delivery and business checks.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 093. `performance-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/performance-testing/SKILL.md) · [EN](../../skills/en/testing-types/performance-testing/SKILL.md)

- First-review recommendation: Fix the shared Excel parsing defect, then test achieved rather than requested load, resource evidence, and error denominators.
- Changed: Added achieved-load and attempts/completions denominator controls; unrun or under-target scenarios cannot become performance acceptance, and gates remain input-sourced.
- New cases: [review-repair-regression](../../skills/en/testing-types/performance-testing/evals/cases/review-repair-regression.yaml) — performance-testing: sourced repair regression.
- Second review/verification: Contract/routing fixture and grader controls pass; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 094. `performance-workload-modeling` (P2)

Location: [ZH](../../skills/zh/testing-types/performance-workload-modeling/SKILL.md) · [EN](../../skills/en/testing-types/performance-workload-modeling/SKILL.md)

- First-review recommendation: Add reproducible unit/window/mix/session conversions; do not infer peak RPS from daily totals without a peak-window duration.
- Changed: Describe each input with value, unit, timezone/window, source, and coverage. Requests/transactions/sessions/users are distinct; convert through transaction mix and requests per transaction with retries/background traffic noted. Daily volume gives an all-day average only. Peak rate requires peak-share volume and window width; missing width yields a conditional formula/range, never invented peak duration/multipliers.
- New cases: [domain-method-regression](../../skills/en/testing-types/performance-workload-modeling/evals/cases/domain-method-regression.yaml) — performance-workload-modeling: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 095. `pr-test-impact-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/pr-test-impact-analysis/SKILL.md) · [EN](../../skills/en/testing-types/pr-test-impact-analysis/SKILL.md)

- First-review recommendation: Record base/head and symbol/dependency/test mappings, removed-test impact, and conservative fallbacks for unknown mappings.
- Changed: Fix repository/base/head SHAs and diff scope. Source file/symbol/schema/config changes; names alone do not prove impact and results from different HEADs cannot be pooled. Map changed symbol→direct/transitive consumer→obligation→test ID/layer/execution version. Label edges confirmed/candidate/unknown and stop only at evidenced isolation boundaries.
- New cases: [domain-method-regression](../../skills/en/testing-types/pr-test-impact-analysis/evals/cases/domain-method-regression.yaml) — pr-test-impact-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 096. `production-incident-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/production-incident-analysis/SKILL.md) · [EN](../../skills/en/testing-types/production-incident-analysis/SKILL.md)

- First-review recommendation: Use timestamped incident/change/mitigation fixtures and distinguish symptoms, associations, root causes, proposed actions, and executed actions.
- Changed: Read incident mitigation-first/evidence/rollback contract. Timestamped actual/approved actions and concurrent load change prevent false mitigation/root-cause claims.
- New cases: [review-concurrent-changes-actions](../../skills/en/testing-types/production-incident-analysis/evals/cases/review-concurrent-changes-actions.yaml) — Incident timeline distinguishes observation, approval and causality; [review-correlation-only-control](../../skills/en/testing-types/production-incident-analysis/evals/cases/review-correlation-only-control.yaml) — A nearby deployment alone is not an incident root cause.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 097. `production-verification` (P2)

Location: [ZH](../../skills/zh/testing-types/production-verification/SKILL.md) · [EN](../../skills/en/testing-types/production-verification/SKILL.md)

- First-review recommendation: Test read-only mode, approved writes, canary thresholds, cleanup failures, and per-step side effects; distinguish plans from observed outcomes.
- Changed: Read read-only-first/approved-account/stop-side-effect contract. Planning case has no run evidence; write fixture isolates explicit approval and observed cleanup failure with residual data.
- New cases: [review-approved-write-cleanup-failure](../../skills/en/testing-types/production-verification/evals/cases/review-approved-write-cleanup-failure.yaml) — Approved synthetic write does not hide cleanup failure; [review-read-only-plan](../../skills/en/testing-types/production-verification/evals/cases/review-read-only-plan.yaml) — Read-only authorization without raw results remains a plan.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 098. `prompt-injection-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/prompt-injection-testing/SKILL.md) · [EN](../../skills/en/testing-types/prompt-injection-testing/SKILL.md)

- First-review recommendation: Use benign-canary untrusted documents, tool traces, and normal-document controls to verify trust boundaries and unauthorized-call absence.
- Changed: Read injection trust/placeholder/no-side-effects contract. Safe canary and reserved example sink are inert fixture data; trace assertion validates both benign control and refusal-with-unauthorized-attempt, without assuming committed exfiltration.
- New cases: [review-canary-tool-traces](../../skills/en/testing-types/prompt-injection-testing/evals/cases/review-canary-tool-traces.yaml) — Refusal text cannot conceal unauthorized canary call.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 099. `prompt-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/prompt-testing/SKILL.md) · [EN](../../skills/en/testing-types/prompt-testing/SKILL.md)

- First-review recommendation: Use paired before/after outputs with identities, structural parsers, calibrated semantics, and valid paraphrase controls for regression decisions.
- Changed: Read prompt-regression identity/PRT fields and semantic-rubric boundary. Concrete output strings give parseable structural versus semantic versus paraphrase categories; changed-model/data control constrains attribution.
- New cases: [review-changed-model-control](../../skills/en/testing-types/prompt-testing/evals/cases/review-changed-model-control.yaml) — Prompt attribution requires unchanged model and data identity; [review-paired-parser-semantic](../../skills/en/testing-types/prompt-testing/evals/cases/review-paired-parser-semantic.yaml) — Paired prompt outputs use parser and calibrated semantic anchors.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 100. `property-based-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/property-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/property-based-testing/SKILL.md)

- First-review recommendation: Specify generators, justified invariants, preconditions, seeds, shrinking, and minimal counterexamples; verify sorting and multiset preservation.
- Changed: Extract the input domain, sourced invariants, preconditions and observable oracles; do not infer properties solely from a function name or preference. Design constrained generators/distributions, including empty/duplicate/extreme cases only if allowed, and retain seed, generator version, samples and failing input for replay.
- New cases: [domain-method-control](../../skills/en/testing-types/property-based-testing/evals/cases/domain-method-control.yaml) — property-based-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/property-based-testing/evals/cases/domain-method-success.yaml) — property-based-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 101. `quality-dashboard-design` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-dashboard-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-dashboard-design/SKILL.md)

- First-review recommendation: Map decisions to metric/source/action panels and distinguish stale/missing/unexecuted data from zero; test misleading green summaries and minority P0 risks.
- Changed: Map audience decisions to metrics, definitions/windows, source versions, actions and owners; available data alone must not decide what matters. Show numerator/denominator, refresh time and source status. Distinguish zero, null, NOT_RUN, BLOCKED and stale data; never fill gaps with zero or reuse stale green.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-dashboard-design/evals/cases/domain-method-regression.yaml) — quality-dashboard-design: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 102. `quality-debt-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-debt-analysis/SKILL.md) · [EN](../../skills/en/testing-types/quality-debt-analysis/SKILL.md)

- First-review recommendation: Separate debt from live product defects, document risk accumulation and repayment evidence, and test age versus impact prioritization.
- Changed: Separate active product defects, test/architecture debt, exceptions and evidence gaps. Record source, impact, cause, age and current controls. Explain accumulated risk through observed maintenance effort, exposure or detection delay. Missing rates yield qualitative or conditional estimates, not invented money.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-debt-analysis/evals/cases/domain-method-regression.yaml) — quality-debt-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 103. `quality-gate-design` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-gate-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-gate-design/SKILL.md)

- First-review recommendation: Define gate state tables, evidence freshness, authorized expiring exceptions, and fail-closed rules; test missing execution evidence.
- Changed: Define each obligation, evidence version/freshness, operator and PASS/FAIL/BLOCKED/UNKNOWN table. Execution prevented is BLOCKED; missing or indeterminate evidence is UNKNOWN; absence never means PASS. Apply project aggregation and fail-closed rules. Preserve unknown/blocked causes and recommend advancement only when all required gates have fresh valid evidence.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-gate-design/evals/cases/domain-method-regression.yaml) — quality-gate-design: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 104. `quality-maturity-assessment` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-maturity-assessment/SKILL.md) · [EN](../../skills/en/testing-types/quality-maturity-assessment/SKILL.md)

- First-review recommendation: Add observable maturity anchors and unknown/not-applicable handling using evidence-paired fixtures; keep repository Quality Score separate.
- Changed: Fix the project's framework, dimensions, anchors and scope. Without a framework provide candidate anchors and evidence, not ratings or a repository Quality Score. Each anchor needs observable practice, artifacts and continuity. Templates prove existence; repeated runs with failure handling prove operating practice. Label example levels as illustrative.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-maturity-assessment/evals/cases/domain-method-regression.yaml) — quality-maturity-assessment: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 105. `quality-metrics-design` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-metrics-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-metrics-design/SKILL.md)

- First-review recommendation: Provide metric dictionaries, windows, deduplication, exclusions, missingness, and lineage; recalculate reopened-defect and repeated-run fixtures.
- Changed: Define purpose, statistical unit, numerator/denominator, window/timezone, filters, deduplication, missing-data handling, version, source and lineage. Separate defect entities from state events, first attempts from reruns, and closure from reopening. Aggregate supplied IDs/event times; duplicates are not new defects and retries cannot inflate first-pass rates.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-metrics-design/evals/cases/domain-method-regression.yaml) — quality-metrics-design: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 106. `quality-productivity-metrics` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-productivity-metrics/SKILL.md) · [EN](../../skills/en/testing-types/quality-productivity-metrics/SKILL.md)

- First-review recommendation: Use balanced effort/output/quality/process measures with complexity and unit controls; test rising test counts alongside increased escapes.
- Changed: Balance effort/cost, accepted output, defects/escapes and waiting/rework with explicit windows, team/task units, complexity and product risk. Deduplicate split or merged cases and verify acceptance. Case/commit counts do not equal value; missing quality/rework evidence prevents productivity claims.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-productivity-metrics/evals/cases/domain-method-regression.yaml) — quality-productivity-metrics: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 107. `quality-risk-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/quality-risk-analysis/SKILL.md) · [EN](../../skills/en/testing-types/quality-risk-analysis/SKILL.md)

- First-review recommendation: Add qualitative risk anchors and uncertainty handling; test rare financial loss versus frequent minor issues without unjustified score products.
- Changed: Register risk events, affected assets/groups, triggers and controls with observable impact, likelihood and detectability anchors and sources. Without project quantitative rules provide justified qualitative ordering. Separate irreversible impact, authority boundaries and known control gaps; low frequency alone is not low risk.
- New cases: [domain-method-regression](../../skills/en/testing-types/quality-risk-analysis/evals/cases/domain-method-regression.yaml) — quality-risk-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 108. `rag-quality-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/rag-quality-testing/SKILL.md) · [EN](../../skills/en/testing-types/rag-quality-testing/SKILL.md)

- First-review recommendation: Map queries/chunks/claims/citations and score completeness/refusal separately; test citations that exist but do not support the answer.
- Changed: Fix query/sample, knowledge/index/retrieval/model/prompt versions. Map queries to retrieved chunks, atomic claims and citations with support/contradiction/gap labels. Judge citation accuracy, claim support and completeness separately. Supported claims may omit required conditions; use the task and project rubric.
- New cases: [domain-method-regression](../../skills/en/testing-types/rag-quality-testing/evals/cases/domain-method-regression.yaml) — rag-quality-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 109. `rag-retrieval-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/rag-retrieval-testing/SKILL.md) · [EN](../../skills/en/testing-types/rag-retrieval-testing/SKILL.md)

- First-review recommendation: Define relevance labels, top-k/denominators, filters, permissions, freshness, and ranking controls; distinguish retrieval from generation failures.
- Changed: Version queries, relevance annotations, document/chunk units, labelers and corpus. Recall@k uses the known relevant set; Precision@k uses actual returns with the supplied duplicate policy. Check rank, relevance, permission/tenant filters, freshness and version for each hit. Relevant but unauthorized hits are failures; high scores cannot cure stale content.
- New cases: [domain-method-regression](../../skills/en/testing-types/rag-retrieval-testing/evals/cases/domain-method-regression.yaml) — rag-retrieval-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 110. `recovery-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/recovery-testing/SKILL.md)

- First-review recommendation: Distinguish service/data recovery and define timing, recovery points, consistency, and compensation; verify timeline and snapshot evidence.
- Changed: Separate service restart/readiness, recovered data point and business consistency; extract RTO/RPO definitions, failure/start and business-recovery/end plus acceptable loss. Join failure, backups/logs, recovery, dependency readiness and business-validation timelines; health probes do not automatically end business RTO.
- New cases: [domain-method-control](../../skills/en/testing-types/recovery-testing/evals/cases/domain-method-control.yaml) — recovery-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/recovery-testing/evals/cases/domain-method-success.yaml) — recovery-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 111. `regression-optimization` (P2)

Location: [ZH](../../skills/zh/testing-types/regression-optimization/SKILL.md) · [EN](../../skills/en/testing-types/regression-optimization/SKILL.md)

- First-review recommendation: Define risk-preservation constraints and comparable time/miss-risk measures; reject speed gains obtained by removing critical protection.
- Changed: Match before/after versions, environment, obligations, data and windows. Source selection/order/parallel/cache inclusions and exclusions; different test volumes cannot support timing comparisons. Preserve critical risks, known escapes and mandatory gates. Reject removal of sole protection; unknown mappings require conservative checks or escalation.
- New cases: [domain-method-regression](../../skills/en/testing-types/regression-optimization/evals/cases/domain-method-regression.yaml) — regression-optimization: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 112. `regression-scope-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/regression-scope-analysis/SKILL.md) · [EN](../../skills/en/testing-types/regression-scope-analysis/SKILL.md)

- First-review recommendation: Add change-to-obligation, layer/platform, and inclusion/exclusion mappings. Test indirect dependencies and insufficient budgets without treating unknown impact as excluded.
- Changed: Map changes and current baseline to affected obligations, layers/platforms/data states, include/exclude decisions and evidence. Regression protects existing behavior; new-feature acceptance is distinct. Check direct, transitive and dynamic dependencies, historical escapes and nonfunctional impact. Unknown mappings are not proof of no impact; exclusion needs an evidenced boundary.
- New cases: [domain-method-regression](../../skills/en/testing-types/regression-scope-analysis/evals/cases/domain-method-regression.yaml) — regression-scope-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 113. `regression-test-selection` (P2)

Location: [ZH](../../skills/zh/testing-types/regression-test-selection/SKILL.md) · [EN](../../skills/en/testing-types/regression-test-selection/SKILL.md)

- First-review recommendation: Provide actual test IDs, durations, dependencies, and risk mappings. Verify the selected set, mandatory coverage, and the infeasible-budget branch rather than selection principles alone.
- Changed: Read mapped change risk/mandatory/runtime/dependency contract. Actual inventory has unique IDs, costs and prerequisite; script checks set/order/summed budget and separate infeasible branch preserves mandatory coverage.
- New cases: [review-mandatory-budget-infeasible](../../skills/en/testing-types/regression-test-selection/evals/cases/review-mandatory-budget-infeasible.yaml) — An impossible mandatory budget is surfaced rather than hidden; [review-risk-mapped-selection](../../skills/en/testing-types/regression-test-selection/evals/cases/review-risk-mapped-selection.yaml) — Selected set preserves mandatory dependencies and budget.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 114. `reliability-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/reliability-testing/SKILL.md) · [EN](../../skills/en/testing-types/reliability-testing/SKILL.md)

- First-review recommendation: Add concrete reliability procedures: SLI definitions, observation windows, failure denominators, repeated failures, and recovery criteria. Test incompatible denominators and short failure-free windows.
- Changed: Define SLI event/time basis, success/failure, denominator, exclusions, observation window and sourced targets; request success and time availability are different metrics. Recalculate success/total or available/eligible time per window, retaining missing observations, retries, duplicate events and denominator conflicts. Merge only compatible definitions.
- New cases: [domain-method-control](../../skills/en/testing-types/reliability-testing/evals/cases/domain-method-control.yaml) — reliability-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/reliability-testing/evals/cases/domain-method-success.yaml) — reliability-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 115. `requirement-ambiguity-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-ambiguity-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-ambiguity-analysis/SKILL.md)

- First-review recommendation: Show competing plausible interpretations, their consequences, and a discriminating question. Add a clear-requirement control and distinguish ambiguity from missing rules or contradictions.
- Changed: Retain requirement ID, source, version, and wording. Separate AMBIGUOUS (multiple meanings), MISSING_RULE (undefined behavior), CONFLICT (opposing sources), and CLEAR (testable wording); do not flag normal shorthand to manufacture findings. For ambiguity show at least two plausible interpretations, conditions, different business/test consequences, and supporting wording. Without a plausible alternative, check whether material is merely missing.
- New cases: [domain-method-regression](../../skills/en/testing-types/requirement-ambiguity-analysis/evals/cases/domain-method-regression.yaml) — requirement-ambiguity-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 116. `requirement-conflict-detection` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-conflict-detection/SKILL.md) · [EN](../../skills/en/testing-types/requirement-conflict-detection/SKILL.md)

- First-review recommendation: Test similarly worded rules with different scopes or versions and conflicts involving several rules. Require participating rule IDs and a minimal conflicting set, with uncertainty retained.
- Changed: Read same-applicability conflict criterion. Added multi-rule satisfiability fixture, actor/version control and unknown-scope case; no precedence chosen.
- New cases: [review-multi-rule-minimal-conflict](../../skills/en/testing-types/requirement-conflict-detection/evals/cases/review-multi-rule-minimal-conflict.yaml) — Three rules can conflict even when every pair is satisfiable; [review-role-version-nonconflict](../../skills/en/testing-types/requirement-conflict-detection/evals/cases/review-role-version-nonconflict.yaml) — Same verb under different actors or versions is not a same-scope conflict; [review-unknown-scope](../../skills/en/testing-types/requirement-conflict-detection/evals/cases/review-unknown-scope.yaml) — Unknown scope does not establish a confirmed conflict.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 117. `requirement-consistency-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-consistency-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-consistency-analysis/SKILL.md)

- First-review recommendation: Add entity/term, unit, and state mappings. Test equivalent aliases, differing versions, and incompatible units to distinguish aligned, contradicted, and non-comparable statements.
- Changed: Fix sources, versions, and effective dates. Build evidenced aliases, entity IDs, units, and state mappings; equal names are not automatically equivalent. Compare rules with matched scope, version, and conditions. Convert units with documented factors and normalize states only through explicit mappings; never silently merge versions or entities.
- New cases: [domain-method-regression](../../skills/en/testing-types/requirement-consistency-analysis/evals/cases/domain-method-regression.yaml) — requirement-consistency-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 118. `requirement-gap-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-gap-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-gap-analysis/SKILL.md)

- First-review recommendation: Separate undefined rules, unavailable material, conflicts, and non-applicability. Test a complete requirement and a missing closure condition, requiring sourced gaps and observable closure evidence.
- Changed: Build a versioned checklist of applicable roles, states, rules, exceptions, and closure conditions, tied to supplied sources. Do not force irrelevant checklist items onto a product. Separate MISSING_RULE (relevant but undefined behavior), MISSING_MATERIAL (referenced evidence absent), CONFLICT, N/A (evidenced scope exclusion), and COMPLETE.
- New cases: [domain-method-regression](../../skills/en/testing-types/requirement-gap-analysis/evals/cases/domain-method-regression.yaml) — requirement-gap-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 119. `requirement-quality-review` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/requirement-quality-review/SKILL.md)

- First-review recommendation: Add a sound requirement control and a fixture with a specific high-risk defect. Verify severity, source passages, and targeted rewrites without requiring findings for every input.
- Changed: Read RQ quality dimensions/status/owner/validation contract. Fully specified quantity scope controls false blockers; line-counted refund text produces observable high-risk oracle gaps.
- New cases: [review-complete-requirement-control](../../skills/en/testing-types/requirement-quality-review/evals/cases/review-complete-requirement-control.yaml) — Complete scoped requirements do not require invented blockers; [review-located-high-risk-gap](../../skills/en/testing-types/requirement-quality-review/evals/cases/review-located-high-risk-gap.yaml) — Unobservable refund acceptance has concrete source and priority.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 120. `requirement-traceability-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/requirement-traceability-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-traceability-analysis/SKILL.md)

- First-review recommendation: Use typed traceability edges and distinguish mapped, executed, and satisfied obligations. Test many-to-many links, outdated mappings, duplicate IDs, and coverage calculations on a small graph.
- Changed: Fix IDs/versions for requirements, obligations, implementation, tests, and runs. Keep relationship types direct/derived/indirect/contradictory/missing; record implements/validates/executed-by/satisfies as a separate edge-purpose column with sources; file existence or name similarity is no evidence edge. Deduplicate obligation denominators when multiple tests protect one obligation, preserving layers/assertions. Same ID with conflicting content is IDENTITY_CONFLICT, not a mergeable duplicate.
- New cases: [domain-method-regression](../../skills/en/testing-types/requirement-traceability-analysis/evals/cases/domain-method-regression.yaml) — requirement-traceability-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 121. `requirements-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/requirements-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirements-analysis/SKILL.md)

- First-review recommendation: Add concrete rule/state fixtures and verify source-linked test points, unknown rules, and useful questions. Include a complete-input control that must not gain invented gaps.
- Changed: Read facts/assumptions and exact Open Questions output contract. State/rule fixture supports traceable intent and truly missing TTL/owner, while complete requirement control constrains invented gaps.
- New cases: [review-complete-analysis-control](../../skills/en/testing-types/requirements-analysis/evals/cases/review-complete-analysis-control.yaml) — Complete rules do not acquire fictional gaps or extra domains; [review-state-rule-trace](../../skills/en/testing-types/requirements-analysis/evals/cases/review-state-rule-trace.yaml) — Analysis derives sourced test points without filling unknown timing.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 122. `requirements-analysis-plus` (P1)

Location: [ZH](../../skills/zh/testing-types/requirements-analysis-plus/SKILL.md) · [EN](../../skills/en/testing-types/requirements-analysis-plus/SKILL.md)

- First-review recommendation: Repair destructive Markdown parsing and distinguish keyword extraction from semantic multi-source analysis. Test numeric rules, conflicting roles, and unrelated domains without invented requirements.
- Changed: Removed fixed business answers, priorities, and invented metrics; helpers prepare complete source text, line identity, hashes, and NOT_ASSESSED scaffolds, reject empty input, and leave semantic work to the main prompt.
- New cases: [review-repair-regression](../../skills/en/testing-types/requirements-analysis-plus/evals/cases/review-repair-regression.yaml) — requirements-analysis-plus: sourced repair regression.
- Second review/verification: Empty/full-source fidelity, unknown states, isolated CLI/export checks pass; deterministic helpers prepare evidence only; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 123. `resilience-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/resilience-testing/SKILL.md) · [EN](../../skills/en/testing-types/resilience-testing/SKILL.md)

- First-review recommendation: Add pre/during/post-disruption invariants, degraded states, and recovery criteria. Test partial dependency failures and failed recovery, clarifying handoffs to reliability and chaos testing.
- Changed: Define pre/during/post-disruption function/data invariants and normal/degraded/unavailable states from business contracts, retaining permitted experience changes. Model partial/slow dependency failure and failed recovery, specifying protected core and suspendable functions in each state.
- New cases: [domain-method-control](../../skills/en/testing-types/resilience-testing/evals/cases/domain-method-control.yaml) — resilience-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/resilience-testing/evals/cases/domain-method-success.yaml) — resilience-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 124. `retry-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/retry-testing/SKILL.md) · [EN](../../skills/en/testing-types/retry-testing/SKILL.md)

- First-review recommendation: Add retryability, attempt/deadline budgets, backoff, server hints, and side-effect checks. Test timeout-after-write and nested retries using concrete traces.
- Changed: Classify retryable, permanent and unknown-outcome errors from contracts; define total attempts versus additional retries and nested call relationships. List end-to-end deadline, per-attempt timeout, backoff/jitter, HTTP Retry-After (delay seconds or HTTP-date) and cancellation; sum attempts/waits on the timeline without inventing backoff values.
- New cases: [domain-method-control](../../skills/en/testing-types/retry-testing/evals/cases/domain-method-control.yaml) — retry-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/retry-testing/evals/cases/domain-method-success.yaml) — retry-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 125. `risk-based-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/risk-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/risk-based-testing/SKILL.md)

- First-review recommendation: Map each risk to test objectives, depth, minimum evidence, and residual exposure. Use qualitative anchors and a constrained-budget fixture to verify justified priorities and unresolved tradeoffs.
- Changed: Anchor qualitative risk in observable impact, exposure/occurrence evidence, detectability, and control gaps. Without a project numeric model do not invent score products; unknown likelihood remains uncertain. Link each risk to objective, layer/platform, depth, data, minimum observable evidence, sourced duration, and residual risk. High risk needs falsifiable business assertions, not merely more cases.
- New cases: [domain-method-regression](../../skills/en/testing-types/risk-based-testing/evals/cases/domain-method-regression.yaml) — risk-based-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 126. `root-cause-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/root-cause-analysis/SKILL.md) · [EN](../../skills/en/testing-types/root-cause-analysis/SKILL.md)

- First-review recommendation: Add competing hypotheses, counter-evidence, and discriminating experiments. Compare correlation-only and causal-chain fixtures so the final error message is not automatically treated as the root cause.
- Changed: Read root-cause versus trigger/contributor and counter-evidence rules. Paired correlation-only versus controlled exception-release reproduction differentiates causal support while limiting production scope.
- New cases: [review-competing-hypotheses](../../skills/en/testing-types/root-cause-analysis/evals/cases/review-competing-hypotheses.yaml) — Competing hypotheses retain counter-evidence and a minimal discriminator; [review-controlled-causal-chain](../../skills/en/testing-types/root-cause-analysis/evals/cases/review-controlled-causal-chain.yaml) — Controlled reproduction supports a bounded causal explanation.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 127. `secrets-exposure-review` (P1)

Location: [ZH](../../skills/zh/testing-types/secrets-exposure-review/SKILL.md) · [EN](../../skills/en/testing-types/secrets-exposure-review/SKILL.md)

- First-review recommendation: Add location and credential-lifecycle checks across code, CI, logs, artifacts, and history. Test placeholders and redacted candidates; avoid exposing values or inferring credential validity from a pattern.
- Changed: Inventory supplied authorized code/config/CI/log/artifact/history, recording candidate locations, categories and redacted fingerprints without copying values or reading real credentials. Distinguish environment placeholders, explicitly synthetic test values and credential-shaped candidates of unknown validity; patterns do not prove a live credential.
- New cases: [domain-method-control](../../skills/en/testing-types/secrets-exposure-review/evals/cases/domain-method-control.yaml) — secrets-exposure-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/secrets-exposure-review/evals/cases/domain-method-success.yaml) — secrets-exposure-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 128. `security-requirement-review` (P1)

Location: [ZH](../../skills/zh/testing-types/security-requirement-review/SKILL.md) · [EN](../../skills/en/testing-types/security-requirement-review/SKILL.md)

- First-review recommendation: Add asset-to-threat, security-obligation, control, and verifiable-acceptance mappings. Test vague and concrete requirements using supplied standards without inventing compliance conclusions.
- Changed: Map asset→threat actor/path→security obligation→control→verifiable acceptance, retaining scope, sources and project-supplied standard/version; do not select an unsupplied compliance baseline. Turn vague secure/encrypted wording into questions about subject/action/boundary/timing/observable outcome; thresholds/algorithms must be sourced or labeled proposals.
- New cases: [domain-method-control](../../skills/en/testing-types/security-requirement-review/evals/cases/domain-method-control.yaml) — security-requirement-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/security-requirement-review/evals/cases/domain-method-success.yaml) — security-requirement-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 129. `security-testing` (P2)

Location: [ZH](../../skills/zh/testing-types/security-testing/SKILL.md) · [EN](../../skills/en/testing-types/security-testing/SKILL.md)

- First-review recommendation: Map threats and controls to tests and evidence, including legitimate-use controls. Distinguish design, execution, and confirmed vulnerabilities; test clean scans with unverified business authorization.
- Changed: Within actual authorization map asset/principal→threat→control→steps→oracle→evidence/state. Record environment, permitted actions, stop conditions, and authority provenance. Pair authorized access with unauthorized-denial controls. Denial requires no data disclosure or tool/write effects; error responses and scans alone are insufficient.
- New cases: [domain-method-regression](../../skills/en/testing-types/security-testing/evals/cases/domain-method-regression.yaml) — security-testing: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 130. `session-security-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/session-security-testing/SKILL.md) · [EN](../../skills/en/testing-types/session-security-testing/SKILL.md)

- First-review recommendation: Select lifecycle checks for the supplied cookie/token mechanism: creation, rotation, fixation, expiry, revocation, logout, and concurrent sessions. Test old credentials after logout and permission changes.
- Changed: Identify Cookie/opaque-session/access+refresh mechanisms and contracts for creation, post-login rotation, fixation, idle/absolute expiry, revocation, logout and concurrent clients. Build before/after states with credential labels, tracking old-credential invalidation, new privilege and server state without real Cookie/token values.
- New cases: [domain-method-control](../../skills/en/testing-types/session-security-testing/evals/cases/domain-method-control.yaml) — session-security-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/session-security-testing/evals/cases/domain-method-success.yaml) — session-security-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 131. `state-transition-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/state-transition-testing/SKILL.md) · [EN](../../skills/en/testing-types/state-transition-testing/SKILL.md)

- First-review recommendation: Add a transition matrix, reachability checks, invalid transitions, guard boundaries, and partial-failure handling. Verify valid and invalid coverage against a small state graph.
- Changed: Build sourced state/event/guard/action/target cells with initial/terminal, persistence and failure-atomicity contracts. Check reachability from the initial state and illegal/undefined events, deriving true/false guard boundaries rather than checking state-name presence.
- New cases: [domain-method-control](../../skills/en/testing-types/state-transition-testing/evals/cases/domain-method-control.yaml) — state-transition-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/state-transition-testing/evals/cases/domain-method-success.yaml) — state-transition-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 132. `technical-design-quality-review` (P2)

Location: [ZH](../../skills/zh/testing-types/technical-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/technical-design-quality-review/SKILL.md)

- First-review recommendation: Use concrete component and sequence fixtures to review boundaries, invariants, failure, and recovery. Include a sound design control and partial-commit failure, requiring specific evidence locations.
- Changed: Read TD source/design-not-runtime finding contract. Actual component/sequence materials expose commit/publish gap and missing stable identity; outbox/dedup/recovery control prevents blanket findings.
- New cases: [review-distributed-partial-commit](../../skills/en/testing-types/technical-design-quality-review/evals/cases/review-distributed-partial-commit.yaml) — Distributed partial commit violates the declared invariant; [review-reliable-controls-design](../../skills/en/testing-types/technical-design-quality-review/evals/cases/review-reliable-controls-design.yaml) — A reliable design control is not mechanically rejected.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 133. `test-case-reviewer` (P2)

Location: [ZH](../../skills/zh/testing-types/test-case-reviewer/SKILL.md) · [EN](../../skills/en/testing-types/test-case-reviewer/SKILL.md)

- First-review recommendation: Provide actual cases and requirements with seeded defects in expectations or prerequisites. Require case-level findings and rewrites, plus a correct control that limits unsupported missing-coverage claims.
- Changed: Read case-review observable expectations and scope/risk contract. Actual numbered cases contain two different defects; complete TC3 control avoids industry-driven filler findings.
- New cases: [review-correct-case-control](../../skills/en/testing-types/test-case-reviewer/evals/cases/review-correct-case-control.yaml) — Executable sourced case is not falsely rejected; [review-located-case-defects](../../skills/en/testing-types/test-case-reviewer/evals/cases/review-located-case-defects.yaml) — Case review locates weak oracle and missing preconditions.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 134. `test-case-reviewer-plus` (P1)

Location: [ZH](../../skills/zh/testing-types/test-case-reviewer-plus/SKILL.md) · [EN](../../skills/en/testing-types/test-case-reviewer-plus/SKILL.md)

- First-review recommendation: The runner invents inventory/payment findings for unrelated inputs and omits the pending-human-decision contract. Replace fixed findings with sourced review or label the runner as a demonstration; test correct and unrelated-domain cases.
- Changed: Removed fixed business answers, priorities, and invented metrics; helpers prepare complete source text, line identity, hashes, and NOT_ASSESSED scaffolds, reject empty input, and leave semantic work to the main prompt.
- New cases: [review-repair-regression](../../skills/en/testing-types/test-case-reviewer-plus/evals/cases/review-repair-regression.yaml) — test-case-reviewer-plus: sourced repair regression.
- Second review/verification: Empty/full-source fidelity, unknown states, isolated CLI/export checks pass; deterministic helpers prepare evidence only; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 135. `test-case-writing` (P2)

Location: [ZH](../../skills/zh/testing-types/test-case-writing/SKILL.md) · [EN](../../skills/en/testing-types/test-case-writing/SKILL.md)

- First-review recommendation: Check merge/split rules, ordering, and trace fields structurally. Test conflicting expectations, repeated inputs from four roles, and missing source versions, requiring preserved provenance.
- Changed: Read deterministic candidate equivalence/splitting and first-appearance union rules. Structured fixture contains all four roles plus valid different-state outcome and unknown source version; grader asserts one suite, split criteria, order and full provenance.
- New cases: [review-role-merge-split-trace](../../skills/en/testing-types/test-case-writing/evals/cases/review-role-merge-split-trace.yaml) — Four-role duplicates merge while distinct outcomes split.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 136. `test-code-review` (P1)

Location: [ZH](../../skills/zh/testing-types/test-code-review/SKILL.md) · [EN](../../skills/en/testing-types/test-code-review/SKILL.md)

- First-review recommendation: Add assertion failure-sensitivity, subject isolation, mock boundaries, data/concurrency isolation, and cleanup checks. Test swallowed errors, tautological assertions, and sound tests with concrete code findings.
- Changed: Identify protected behavior and how failure must fail the test, tracing actual values to the subject; check tautologies, type-only assertions and swallowed errors with no failure exit. Check mock boundaries, error branches, async waits/returns and cleanup so the subject is not replaced and promise results are observed.
- New cases: [domain-method-control](../../skills/en/testing-types/test-code-review/evals/cases/domain-method-control.yaml) — test-code-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/test-code-review/evals/cases/domain-method-success.yaml) — test-code-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 137. `test-data-generation` (P2)

Location: [ZH](../../skills/zh/testing-types/test-data-generation/SKILL.md) · [EN](../../skills/en/testing-types/test-data-generation/SKILL.md)

- First-review recommendation: Add schema/relationship-based generation of labeled valid and invalid datasets. Verify uniqueness, foreign keys, state relations, and reproducibility, with artifacts when requested.
- Changed: Derive groups from supplied schema, foreign keys, uniqueness, state relationships, and scenario oracles. Fix seed/generator version; missing rules remain UNKNOWN without invented fields or real identities. Separate valid happy/boundary data from deliberate invalid groups. Name the violated constraint and expected allow/reject outcome while preserving other relationships; invalid rows cannot silently enter valid groups.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-data-generation/evals/cases/domain-method-regression.yaml) — test-data-generation: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 138. `test-data-requirement-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/test-data-requirement-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-data-requirement-analysis/SKILL.md)

- First-review recommendation: Map scenarios to entities, states, relationships, quantity rationale, and acquisition/cleanup conditions. Test missing schemas, cross-entity dependencies, and restricted personal data while preserving unknowns.
- Changed: Map scenario/risk→entities/states/relationships→values/boundaries→quantity basis→source/authority→setup/cleanup. This Skill analyzes needs, not implicit generation or collection. Quantity derives from concurrency/isolation/repetitions/consumption. Missing counts yield formulas/gaps, not an invented100 rows; session counts are not entity counts.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-data-requirement-analysis/evals/cases/domain-method-regression.yaml) — test-data-requirement-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 139. `test-effectiveness-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/test-effectiveness-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-effectiveness-analysis/SKILL.md)

- First-review recommendation: Trace faults or obligations through tests and assertions to missed detection. Distinguish historical escapes from controlled fault seeding, and test high pass rates with known misses and explicit denominators.
- Changed: Map obligation/fault class→test ID→real production behavior→effective assertion→escaping defect. Pass/coverage rates are signals, not fault-detection proof. Historical escapes retain observation window, exposure, detection/misses, and sources. Controlled fault injections use separate denominators, controls, environment, and mutation identity; do not pool them into production-defect rates.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-effectiveness-analysis/evals/cases/domain-method-regression.yaml) — test-effectiveness-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 140. `test-gap-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/test-gap-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-gap-analysis/SKILL.md)

- First-review recommendation: Test mapped-but-unexecuted, executed-but-unsatisfied, unavailable mapping evidence, and non-applicability. Verify gap classifications and closure evidence rather than deriving coverage from item counts.
- Changed: Read TG supported gap types and evidence boundaries. Five paired obligation states explicitly distinguish mapping, execution, satisfaction, material insufficiency and non-applicability without adding a coverage authority.
- New cases: [review-obligation-evidence-states](../../skills/en/testing-types/test-gap-analysis/evals/cases/review-obligation-evidence-states.yaml) — Mapped, executed, unknown and not-applicable states are distinct.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 141. `test-maintenance-cost-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/test-maintenance-cost-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-maintenance-cost-analysis/SKILL.md)

- First-review recommendation: Break down maintenance by product change, test defects, infrastructure, data, and duplication. Include sample windows and uncertainty; test equal totals with different causes and avoid individual-performance inferences.
- Changed: Fix assets, sample window, unit, and time sources. Separate product change, test defect, infrastructure, data, duplication, and unclassified costs; do not double-count one event across causes. Link trigger, change frequency, time ranges, review/rework, and failure impact. Separate one-time build from recurring maintenance; one sample cannot predict precise long-term costs.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-maintenance-cost-analysis/evals/cases/domain-method-regression.yaml) — test-maintenance-cost-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 142. `test-report-review` (P2)

Location: [ZH](../../skills/zh/testing-types/test-report-review/SKILL.md) · [EN](../../skills/en/testing-types/test-report-review/SKILL.md)

- First-review recommendation: Add case-level statistics with skipped, blocked, and rerun outcomes, build mismatches, and controlled conditions. Verify denominators and recommendation states with a fully consistent report control.
- Changed: Bad summary, complete consistent control, scoped build evidence and formal approval boundary.
- New cases: [review-report-reconciliation](../../skills/en/testing-types/test-report-review/evals/cases/review-report-reconciliation.yaml) — Reject inconsistent report; accept consistent control.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 143. `test-reporting` (P2)

Location: [ZH](../../skills/zh/testing-types/test-reporting/SKILL.md) · [EN](../../skills/en/testing-types/test-reporting/SKILL.md)

- First-review recommendation: Use raw execution and defect rows to verify planned/executed/outcome totals and rerun rules. Preserve unknown counts instead of deriving them from a summary alone.
- Changed: Raw per-case reruns, unique-case denominator, build attribution, unknown-count control and approval boundary.
- New cases: [review-raw-execution-statistics](../../skills/en/testing-types/test-reporting/evals/cases/review-raw-execution-statistics.yaml) — Distinct cases, reruns, denominators, and build evidence; [review-unknown-denominator](../../skills/en/testing-types/test-reporting/evals/cases/review-unknown-denominator.yaml) — Partial logs preserve unknown planned denominator.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 144. `test-runtime-optimization` (P2)

Location: [ZH](../../skills/zh/testing-types/test-runtime-optimization/SKILL.md) · [EN](../../skills/en/testing-types/test-runtime-optimization/SKILL.md)

- First-review recommendation: Add critical-path, setup/teardown, resource-limit, and cold/warm-cache analysis. Compare equivalent baseline/candidate runs and verify retained fault detection as well as duration.
- Changed: Profile setup, execution, teardown, and retries with matched commit, obligations, data, resources, and windows. Derive DAG critical paths without adding overlapping jobs. Separate cold/warm cache, runner limits, concurrency, isolated data, and contention. Record changed factors; different test volumes/environments cannot prove speedups.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-runtime-optimization/evals/cases/domain-method-regression.yaml) — test-runtime-optimization: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 145. `test-scope-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/test-scope-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-scope-analysis/SKILL.md)

- First-review recommendation: Define scope units across version, layer, platform, and data states with inclusion/exclusion rationale and change triggers. Test undefined boundaries and new requirements; clarify the regression-specific handoff.
- Changed: Build scope cells for version×layer×platform×data state from the delivery objective, linked to requirements, include/exclude evidence, owners, and observable acceptance. New-feature scope is broader than change-only regression. Separate INCLUDE, EXCLUDE, and UNKNOWN. Exclusions need a sourced scope or independent-contract reason; unclear platform/data/boundary support cannot mean 'do not test'.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-scope-analysis/evals/cases/domain-method-regression.yaml) — test-scope-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 146. `test-strategy` (P2)

Location: [ZH](../../skills/zh/testing-types/test-strategy/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy/SKILL.md)

- First-review recommendation: Connect objectives, scope, depth, capacity, gates, evidence, and owners in an executable plan. Test differing capacity constraints and unresolved risks without imposing arbitrary pass-rate thresholds.
- Changed: Build a minimum executable table linking objective→obligation/scope→layer/depth→data/environment→resources/owner→entry/exit rule source→evidence/residual risk. Reuse the project stack and actual capacity, protecting critical loss/authority obligations first. Each scenario needs business postconditions/evidence; insufficient resources expose unfinished work and minimal alternatives.
- New cases: [domain-method-regression](../../skills/en/testing-types/test-strategy/evals/cases/domain-method-regression.yaml) — test-strategy: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 147. `test-strategy-plus` (P1)

Location: [ZH](../../skills/zh/testing-types/test-strategy-plus/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy-plus/SKILL.md)

- First-review recommendation: The runner invents promotion scope, infrastructure, and a 95% P1 gate for a calculator requirement. Generate only from supplied facts or label demonstration output; test three unrelated domains and retained unknowns.
- Changed: Removed fixed business answers, priorities, and invented metrics; helpers prepare complete source text, line identity, hashes, and NOT_ASSESSED scaffolds, reject empty input, and leave semantic work to the main prompt.
- New cases: [review-repair-regression](../../skills/en/testing-types/test-strategy-plus/evals/cases/review-repair-regression.yaml) — test-strategy-plus: sourced repair regression.
- Second review/verification: Empty/full-source fidelity, unknown states, isolated CLI/export checks pass; deterministic helpers prepare evidence only; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 148. `test-strategy-review` (P2)

Location: [ZH](../../skills/zh/testing-types/test-strategy-review/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy-review/SKILL.md)

- First-review recommendation: Add an acceptable strategy control and fixtures with dependency, responsibility, and gate conflicts. Verify blocker/condition classification and closure evidence without turning every improvement into rejection.
- Changed: Acceptable standalone strategy; dependency and responsibility blockers; improvement control; closure/authority boundaries.
- New cases: [review-strategy-control-and-conflicts](../../skills/en/testing-types/test-strategy-review/evals/cases/review-strategy-control-and-conflicts.yaml) — Valid strategy versus gate and responsibility conflicts.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 149. `test-suite-health-analysis` (P1)

Location: [ZH](../../skills/zh/testing-types/test-suite-health-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-suite-health-analysis/SKILL.md)

- First-review recommendation: Add test/run identities, failure taxonomy, retry/quarantine behavior, redundant coverage, duration trends, and protected obligations. Test retry-heavy green runs without inventing an ungrounded health score.
- Changed: Normalize stable test IDs, protected obligations, code/data revisions and run IDs, separating first attempts, retries, quarantine, skips and unrun cases. Recalculate final/first-attempt pass, retry proportions and failure categories under sourced definitions; retain product/test/environment/unknown causes. Green retries do not establish resolved causes.
- New cases: [domain-method-control](../../skills/en/testing-types/test-suite-health-analysis/evals/cases/domain-method-control.yaml) — test-suite-health-analysis: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/test-suite-health-analysis/evals/cases/domain-method-success.yaml) — test-suite-health-analysis: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 150. `testability-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/testability-analysis/SKILL.md) · [EN](../../skills/en/testing-types/testability-analysis/SKILL.md)

- First-review recommendation: Use actual design/interface fixtures to verify minimal safe observability seams, time/randomness control, and dependency substitutes. Include an existing-seam control to avoid blanket debug-backdoor recommendations.
- Changed: Read architecture-mode/source/safe-seam contract; retained pre-existing testability case edits. Actual diagram/interface fixtures support minimal safe adapters and an existing-seam control.
- New cases: [review-actual-design-safe-seams](../../skills/en/testing-types/testability-analysis/evals/cases/review-actual-design-safe-seams.yaml) — Architecture and interfaces yield minimal safe seams; [review-existing-seam-control](../../skills/en/testing-types/testability-analysis/evals/cases/review-existing-seam-control.yaml) — Existing safe test seams are reused instead of adding backdoors.
- Second review/verification: New input/oracles and valid/boundary material reviewed; deterministic grader controls run where configured; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 151. `testcase-writer-plus` (P1)

Location: [ZH](../../skills/zh/testing-types/testcase-writer-plus/SKILL.md) · [EN](../../skills/en/testing-types/testcase-writer-plus/SKILL.md)

- First-review recommendation: The runner turns password rules into promotion/gift cases, assigns priority by position, and uses vague expectations. Produce sourced scenarios and observable assertions or label the demonstration; test password boundaries and empty input.
- Changed: Removed fixed business answers, priorities, and invented metrics; helpers prepare complete source text, line identity, hashes, and NOT_ASSESSED scaffolds, reject empty input, and leave semantic work to the main prompt.
- New cases: [review-repair-regression](../../skills/en/testing-types/testcase-writer-plus/evals/cases/review-repair-regression.yaml) — testcase-writer-plus: sourced repair regression.
- Second review/verification: Empty/full-source fidelity, unknown states, isolated CLI/export checks pass; deterministic helpers prepare evidence only; both configurations valid (configuration only); Excel multi-sheet/sparse-column/source-row helper synchronized.
- Unproven: New semantic model execution NOT_RUN.

### 152. `testing-bottleneck-analysis` (P2)

Location: [ZH](../../skills/zh/testing-types/testing-bottleneck-analysis/SKILL.md) · [EN](../../skills/en/testing-types/testing-bottleneck-analysis/SKILL.md)

- First-review recommendation: Add event timelines, queue/execution/rework decomposition, WIP, and throughput definitions. Test dependency-blocked idle capacity and harmful concurrency, requiring measurable recommendations rather than automatic staffing conclusions.
- Changed: Fix window, work IDs/complexity, arrival/completion, and state events. Separate queue/dependency waiting, execution, rework, handoffs, and blockers; total cycle time is not labor. WIP counts unfinished items; throughput counts completed items per matching window. Measure cycle/stage times separately and disclose missing events/sampling; averages alone establish no cause.
- New cases: [domain-method-regression](../../skills/en/testing-types/testing-bottleneck-analysis/evals/cases/domain-method-regression.yaml) — testing-bottleneck-analysis: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 153. `threat-modeling` (P1)

Location: [ZH](../../skills/zh/testing-types/threat-modeling/SKILL.md) · [EN](../../skills/en/testing-types/threat-modeling/SKILL.md)

- First-review recommendation: Add data-flow and trust-boundary modeling with actors, preconditions, controls, and residual risks. Provide an optional lightweight taxonomy and verify threats against supplied architecture without invented components.
- Changed: Map supplied actors, entries, stores/flows and trust boundaries, listing assets, sensitive data and permitted actions; do not add unsupplied components. For each boundary path record actor, capability, preconditions, controlled input, asset impact and obligation. Optional spoofing/tampering/disclosure/disruption/privilege categories may aid checks.
- New cases: [domain-method-control](../../skills/en/testing-types/threat-modeling/evals/cases/domain-method-control.yaml) — threat-modeling: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/threat-modeling/evals/cases/domain-method-success.yaml) — threat-modeling: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 154. `timeout-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/timeout-testing/SKILL.md) · [EN](../../skills/en/testing-types/timeout-testing/SKILL.md)

- First-review recommendation: Add end-to-end deadlines, connect/read/queue budgets, cancellation propagation, and late results. Test over-budget call chains and timeout-after-commit for state, side effects, and recovery.
- Changed: Identify end-to-end absolute deadlines, connect/queue/read/process budgets, time source and start points, distinguishing serial, overlapping and independent timeouts. Sum elapsed time/remaining deadline along the actual chain and check child-budget propagation; individual phases under limits can still exceed the end-to-end limit.
- New cases: [domain-method-control](../../skills/en/testing-types/timeout-testing/evals/cases/domain-method-control.yaml) — timeout-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/timeout-testing/evals/cases/domain-method-success.yaml) — timeout-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 155. `ui-test-cypress` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-cypress/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-cypress/SKILL.md)

- First-review recommendation: Add version-selected configuration, command/stub boundaries, retry semantics, session/data isolation, and business assertions. Verify that an incorrect product outcome fails in a minimal application fixture.
- Changed: Read Cypress, Node, browser, config, and component/E2E scope from project artifacts. Generate compatible config, custom commands, specs, and CI commands without implicit upgrades or mixed legacy formats. Exercise real page/component logic; cy.intercept replaces only confirmed external boundaries. Stub responses alone cannot prove business postconditions. Define isolated fixture data/session cleanup.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-cypress/evals/cases/domain-method-regression.yaml) — ui-test-cypress: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 156. `ui-test-playwright` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-playwright/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-playwright/SKILL.md)

- First-review recommendation: Require business postconditions, stable semantic locators, identity/data isolation, and failure artifacts. Test incorrect outcomes and parallel users rather than treating a correct page title as business success.
- Changed: Fix project Playwright/Node/browser versions, projects, fixtures, and config. Retain entry points with test ID, commit, worker/project, and environment; diagnose incompatible config without switching stacks. Prefer stable role/name/testid locators and auto-retrying business assertions for order/ledger/state/principal. Title/URL checks protect navigation only, not payment success.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-playwright/evals/cases/domain-method-regression.yaml) — ui-test-playwright: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 157. `ui-test-puppeteer` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-puppeteer/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-puppeteer/SKILL.md)

- First-review recommendation: Record version/browser configuration and supported scope; add lifecycle, business-readiness waits, and failure artifacts. Test new windows, loading failures, and timeouts with cleanup and observable postconditions.
- Changed: Read actual Puppeteer/Node/browser and launch config/support scope. Incompatibility is CONFIG_ERROR; successful launch does not prove every feature is compatible. Identify new windows through target creation/opener association and wait for a usable page, verifying URI/authority. Navigation readiness and business readiness are separate; real state is the oracle, not a fixed sleep.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-puppeteer/evals/cases/domain-method-regression.yaml) — ui-test-puppeteer: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 158. `ui-test-selector-review` (P1)

Location: [ZH](../../skills/zh/testing-types/ui-test-selector-review/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-selector-review/SKILL.md)

- First-review recommendation: Add checks for roles/names, test IDs, scoping, uniqueness, dynamic text, and localization. Test duplicate buttons and stable CSS controls; require reasons rather than blanket CSS/XPath bans.
- Changed: Identify the intended user target from DOM/components; compare role+accessible name, stable test IDs, scoping and CSS/XPath against actual semantics/maintenance contracts. Check match count, visibility/interactability and intended instance in supplied states; use business containers/stable identity for duplicate buttons rather than masking ambiguity with first().
- New cases: [domain-method-control](../../skills/en/testing-types/ui-test-selector-review/evals/cases/domain-method-control.yaml) — ui-test-selector-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/ui-test-selector-review/evals/cases/domain-method-success.yaml) — ui-test-selector-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 159. `ui-test-selenium` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-selenium/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-selenium/SKILL.md)

- First-review recommendation: Add version-selected setup, observable waits, stale-element handling, parallel data, and driver cleanup. Test rerendering and exceptional exits, avoiding fixed sleeps as a universal repair.
- Changed: Fix Selenium/binding/browser/driver/Grid versions, capabilities, and runner. Produce compatible config/POM; do not invent Grid topology and diagnose version conflicts first. Explicitly wait on observable interactability, business state, window, or URL conditions. Presence/visibility is not business readiness; avoid mixed implicit/explicit waits and universal fixed sleeps.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-selenium/evals/cases/domain-method-regression.yaml) — ui-test-selenium: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 160. `ui-test-strategy` (P1)

Location: [ZH](../../skills/zh/testing-types/ui-test-strategy/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-strategy/SKILL.md)

- First-review recommendation: Add journey/state/platform coverage and risk-based allocation across component, integration, E2E, visual, and accessibility evidence. Test minimum effective combinations and explicit residual risk.
- Changed: Build journey/business-state/platform cells mapped to risks, acceptance obligations and existing evidence without expanding unsupported platforms. Allocate a minimum effective combination of component, integration, E2E, visual and accessibility evidence: calculations/states, service interactions, cross-layer journeys and appearance/accessibility need suitable oracles.
- New cases: [domain-method-control](../../skills/en/testing-types/ui-test-strategy/evals/cases/domain-method-control.yaml) — ui-test-strategy: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/ui-test-strategy/evals/cases/domain-method-success.yaml) — ui-test-strategy: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 161. `ui-test-testcafe` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-testcafe/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-testcafe/SKILL.md)

- First-review recommendation: Add version/browser and CI setup, role isolation, asynchronous waits, and reporter failure propagation. Verify generated artifacts and nonzero failure outcomes with a minimal application fixture.
- Changed: Confirm TestCafe/Node/browser, native automation mode, CI, and reporter versions. Produce fixtures/tests/config compatible with the existing runner; missing config is open, not an implicit upgrade. Initialize isolated sessions with Roles or independent identities and isolate accounts/business keys too. Await asynchronous t actions and use supported Selector/assertion waits rather than fixed sleeps.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-testcafe/evals/cases/domain-method-regression.yaml) — ui-test-testcafe: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 162. `ui-test-wait-strategy-review` (P1)

Location: [ZH](../../skills/zh/testing-types/ui-test-wait-strategy-review/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-wait-strategy-review/SKILL.md)

- First-review recommendation: Add a readiness-signal decision table for DOM, business state, network, and events with timeout/retry checks. Test long-lived connections and late results without universally equating network idle with readiness.
- Changed: Choose readiness by obligation: DOM presence/actionability establishes element conditions; business state/version/confirmation IDs establish progress; network/events need correlation to the target operation. Record triggering action, observable condition, request/business ID, timeout and end-to-end budget per wait; fixed sleeps delay but do not guarantee readiness.
- New cases: [domain-method-control](../../skills/en/testing-types/ui-test-wait-strategy-review/evals/cases/domain-method-control.yaml) — ui-test-wait-strategy-review: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/ui-test-wait-strategy-review/evals/cases/domain-method-success.yaml) — ui-test-wait-strategy-review: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 163. `ui-test-webdriverio` (P2)

Location: [ZH](../../skills/zh/testing-types/ui-test-webdriverio/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-webdriverio/SKILL.md)

- First-review recommendation: Add capability/service/version combinations, asynchronous commands, parallel-session isolation, and failure-trace fields. Test incompatible setup and failed commands for actionable diagnostics.
- Changed: Fix WebdriverIO/Node, runner/framework, and browser/driver/service combinations. Check capabilities/services against installed packages, config, and remote support; names alone do not prove compatibility. Generate version-compatible async specs/BDD steps and await every async command. Wait on observable business/element conditions; never catch command errors into a pass.
- New cases: [domain-method-regression](../../skills/en/testing-types/ui-test-webdriverio/evals/cases/domain-method-regression.yaml) — ui-test-webdriverio: Domain outcomes, correct controls, and evidence boundaries.
- Second review/verification: Domain fixture/oracle statically reviewed; isolated grader, valid-output, and mutant controls verified; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

### 164. `visual-regression-testing` (P1)

Location: [ZH](../../skills/zh/testing-types/visual-regression-testing/SKILL.md) · [EN](../../skills/en/testing-types/visual-regression-testing/SKILL.md)

- First-review recommendation: Add baseline keys, environment/data/font controls, animation stabilization, justified masks, and threshold definitions. Test defects versus approved design changes, preserving authorized baseline-update decisions.
- Changed: Define baseline keys: page/revision/viewport/browser/OS/font/theme/data; verify matching comparison conditions or mark environment differences/noncomparability first. Check font readiness, animation/time, dynamic data and screenshot readiness; justify mask scope without masking required content.
- New cases: [domain-method-control](../../skills/en/testing-types/visual-regression-testing/evals/cases/domain-method-control.yaml) — visual-regression-testing: Correct control and boundary decisions; [domain-method-success](../../skills/en/testing-types/visual-regression-testing/evals/cases/domain-method-success.yaml) — visual-regression-testing: Domain procedure and result oracle.
- Second review/verification: Contract/rules, task cases, and valid controls reviewed; enumeration/calculation oracles checked where applicable; both configurations valid (configuration only).
- Unproven: New semantic model execution NOT_RUN.

## Workspace and remaining verification

Of 1,292 files already changed at the start, 1,288 retain their original bytes; four task-related EN/ZH eval manifests only append cases. None of the initial 7,089 files was removed. Original review and evidence are retained. Changes to initial non-Skill files are limited to the generated bilingual governance inventory; new tests/reports/evidence are task additions. HEAD remains `c61f507f61711c3c0f0d1777136a5a4ff0e211b3` on `develop`; no commit/push.

The two authorized targeted model cases are complete. Other new semantic cases, plus target-system UI/load acceptance when project targets are supplied, remain unrun and are not recorded as passing.
