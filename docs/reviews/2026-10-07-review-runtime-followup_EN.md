# Skill Review Runtime Follow-up (2026-10-07)

> This page retains the 2026-10-07 results and blockers. Continuous external-run authorization was subsequently provided; see the [live continuation](./2026-10-08-review-runtime-continuation_EN.md) for later repairs and current states.

[简体中文](./2026-10-07-review-runtime-followup.md) · [164-Skill repair report](./2026-10-07-all-skills-repair-review_EN.md) · [Per-case evidence](../../evidence/skill-quality/2026-10-07-review-repair/runtime-followup.json)

This continuation ran new fixtures, repaired two grader false rejections, and synchronized both languages. Among 530 new cases, **13 unique cases report live PASS, one historic grader FAIL is repaired but awaits a live rerun, one judge reports ERROR, and 515 remain NOT_RUN**. PASS refers to script grading of selected fixtures; it does not establish full Skill-suite or library-wide semantic acceptance.

## Executed results

| Skill / case | EN | ZH | Supported scope |
| --- | --- | --- | --- |
| `skill-change-verification` / `review-repair-regression` | iteration-4 PASS | iteration-2 PASS | The two previously authorized cases; configuration evidence stays distinct from behavior outcomes. |
| `skill-prose-trim` / `review-authorized-trim` | iteration-1 FAIL; repaired iteration-2 PASS | iteration-1 PASS | Remove process residue while preserving durable constraints, measurement limits and historic fixtures. |
| `discover-testing` / four neighbor cases | 4 PASS | 4 PASS | Distinguish authentication, authorization, RAG retrieval and regression selection; catalog identity does not establish Host installation. |
| `multi-role-quality-synthesis` / `review-source-union` | iteration-1 PASS | iteration-1 FAIL; stored response regrades PASS after repair, live rerun blocked | Preserve all sources, versions, original severities, evidence, minority P0 findings and disagreements. |
| `skill-evaluation` / `review-comparable-runs` | iteration-1 ERROR | NOT_RUN | The runner produced a response, but judging did not complete; neither semantic PASS nor Skill failure is established. |

The record contains the latest outcomes for 15 unique cases and 16 case attempts: 11 PASS from this continuation and two from the earlier authorized runs. Older iterations remain separately in [model-pilot-summary.json](../../evidence/skill-quality/2026-10-07-review-repair/model-pilot-summary.json). Observed Codex CLI version is `0.160.1`; reliable model identity is absent and recorded as `UNKNOWN`. Responses, case hashes, execution-time source snapshots where available, and source hashes captured afterward are recorded separately.

## Findings and repairs

### 1. Terminal-newline false rejection in prose cleanup

The `review-authorized-trim` fixture uses YAML `|-`; its original files have no terminal newline. The old grader expected an extra newline in both the editable document and protected JSON, rejecting a correct cleanup.

Both language graders now compare preserved document lines, while checking protected `fixtures/recorded.json` against its exact original bytes. Regression checks cover editable text with and without a terminal newline, an added newline in the protected fixture, and deletion of a durable prohibition. The case input is unchanged; live reruns pass in both languages.

Locations: [EN grader](../../skills/en/skill-engineering/skill-prose-trim/evals/graders/review-authorized-trim.py) · [ZH grader](../../skills/zh/skill-engineering/skill-prose-trim/evals/graders/review-authorized-trim.py) · [RED](../../evidence/skill-quality/2026-10-07-review-repair/prose-trim-grader-red.txt) · [GREEN](../../evidence/skill-quality/2026-10-07-review-repair/prose-trim-grader-green.txt).

### 2. Valid versioned provenance rejected by a flat-only grader

The source-union case requires source versions, original severities and evidence without restricting those fields to flat values. The Chinese output explicitly retained versions in `{version, severity}` and `{version, evidence}` objects; the grader accepted only strings and arrays, producing a false rejection.

Both graders now accept flat values and explicit version objects. Nested versions must match the source register; original severities, evidence and source coverage remain exact. Regression checks accept both valid representations and reject altered versions, severities, invented evidence and missing sources. Both stored responses regrade PASS with the repaired grader. The Chinese live rerun is approval-blocked, so its historic FAIL remains recorded.

Locations: [EN grader](../../skills/en/testing-workflows/multi-role-quality-synthesis/evals/graders/review-source-union.py) · [ZH grader](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/graders/review-source-union.py) · [RED](../../evidence/skill-quality/2026-10-07-review-repair/source-union-grader-red.txt) · [GREEN](../../evidence/skill-quality/2026-10-07-review-repair/source-union-grader-green.txt).

## Outstanding execution and blockers

**Script-graded queue:** Of 172 new script cases, 13 report live PASS, one repaired grader FAIL awaits a live rerun, and 158 are unattempted. Automatic approval review rejected the remaining 159-case queue, reasoning that the earlier explicit authorization for two cases did not explicitly cover this batch's transmission of repository Skill, Prompt and case content to the OpenAI Codex service. The proposed queue uses temporary isolated workspaces, fixed inputs, source hashes and a stop at the first failure or execution error. No workaround was attempted after rejection.

**Semantic judge:** All 358 new `agent_judge` cases specify `openai/gpt-5`. One actual attempt received HTTP 400 from the current Codex ChatGPT login because this model is unsupported. The subsequent judge JSON parsing error is secondary; the root classification is `JUDGE_MODEL_UNSUPPORTED_WITH_CURRENT_LOGIN`. The attempted case is ERROR; the other 357 remain NOT_RUN with the shared compatibility prerequisite recorded.

skill-up v0.12.0 resolves the judge through the selected runner engine. A valid API model ID does not establish compatibility with that login or engine. See the [official evaluation guide](https://alibaba.github.io/skill-up/guide/writing-evals) and [v0.12.0 judge initialization source](https://github.com/alibaba/skill-up/blob/v0.12.0/internal/credential/agent_init.go). The checked separate API credential environment variables and skill-up credential file are absent. Further execution needs compatible provider credentials or an explicitly selected compatible judge profile; the rubric and configured model remain unchanged.

## Verification and optimization suggestions

- Full quality gate PASS: 227 script tests and 328 valid configurations; [check summary](../../evidence/skill-quality/2026-10-07-review-repair/summary.json).
- Pinned `skills@1.7.0` distribution gate PASS against the local checkout: 164 discovered Skills and an isolated English functional-testing installation; [CLI record](../../evidence/skill-quality/2026-10-07-review-repair/cli-summary.json).
- Both false rejections were reproduced from actual inputs, followed by bilingual RED → GREEN regression and adversarial mutation checks; [regression tests](../../scripts/tests/test_review_eval_graders.py).
- Graders should distinguish required content and evidence from acceptable serialization. Require byte identity only for explicitly immutable fixtures.
- Before a semantic batch, validate the judge engine, login and model compatibility with one real fixture, then execute a fixed manifest and retain observed identity.

No commit or push was performed. Full model evaluation remains incomplete; local checks, offline regrading and selected live verdicts retain their separate evidence boundaries.
