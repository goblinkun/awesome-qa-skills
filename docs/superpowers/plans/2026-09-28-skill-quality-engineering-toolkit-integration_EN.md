# Skill Quality Engineering Toolkit v1.0 Integration Plan

<div align="right"><a href="./2026-09-28-skill-quality-engineering-toolkit-integration.md">🇨🇳 Chinese</a> | <strong>🇬🇧 English</strong></div>

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the approved SQET v1.0 Toolkit into `awesome-qa-skills` under the repository's bilingual, evidence, and governance rules, without adding an installable Skill or unexecuted quality claims.

**Architecture:** Add `docs/skill-quality-engineering/` as the documentation entry point for SQEM, the Eval Contract, the Pilot, and templates; root `evals/` and `evidence/skill-quality/` provide navigation and evidence-boundary guidance only. Existing Quality Score, Evidence Contract, Quality Loop, Skill-local Evals, and Pilot records remain the sources of truth and are not migrated or overwritten.

**Tech Stack:** Markdown, Python 3 repository validators, Bash quality gates, and Git Conventional Commits.

**Spec:** `docs/superpowers/specs/2026-09-28-skill-quality-engineering-toolkit-integration-design_EN.md` (Chinese mirror: `docs/superpowers/specs/2026-09-28-skill-quality-engineering-toolkit-integration-design.md`)

## Global Constraints

- SQET is not an installable Agent Skill under `skills/`.
- Project documents use `NAME.md` for Chinese and `NAME_EN.md` for English; the core entry and three core document pairs must have bidirectional switches.
- Preserve the existing meanings of `NOT_RUN`, `NOT_SCORED`, `UNASSESSED`, and `INSUFFICIENT_EVIDENCE`; do not add `PARTIAL` as a repository-level status.
- `docs/governance/QUALITY_SCORE_EVAL_CONTRACT*` remains the exclusive owner of Quality Score; add no score dimensions.
- Skill-local `skills/{zh,en}/.../evals/` remains the default Eval-case source of truth; root `evals/` must not duplicate cases.
- The five SQEM Pilot candidates are methodology candidates only; they do not replace the existing `requirements-analysis`, `ui-test-playwright`, and `discover-testing` Pilot records.
- Do not add real model outputs, target-environment results, benchmark, compatibility, production, or release-approval evidence in this phase.
- Do not modify, delete, or rename existing governance documents; do not commit generated reports, caches, secrets, or unrelated files.
- Documentation tasks use deterministic structure, link, status, and quality checks as their test cycle; do not introduce runtime dependencies for static documents.

## Review Focus

- **Status drift:** Imported examples must not turn `PARTIAL` into a new gate status; bind this to Task 1 with status mapping and `rg` checks.
- **Duplicate Eval source:** Root `evals/README.md` must state that Skill-local Evals are canonical; bind this to Task 2 with content assertions.
- **Pilot replacement:** New Pilot documentation must not overwrite existing analysis/executable/router Pilots; bind this to Tasks 1 and 4 with the exact file list and `git diff --name-only`.
- **Bilingual discoverability:** Every new project document needs a bidirectional switch and registration in `check_docs_bilingual.py`; bind this to Tasks 3 and 4 with a unit test and the full gate.
- **Evidence overclaim:** The entry points and Pilot must not present static validation as runtime or production proof; bind this to Tasks 1, 2, and 4 with keyword review and manual diff review.

---

### Task 1: Import and adapt SQET core documents and templates

**Files:**
- Create: `docs/skill-quality-engineering/README.md`
- Create: `docs/skill-quality-engineering/README_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_EVAL_CONTRACT.md`
- Create: `docs/skill-quality-engineering/SKILL_EVAL_CONTRACT_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_PILOT.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_PILOT_EN.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_EVIDENCE_REPORT_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_QUALITY_CI_GUIDE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_QUALITY_PROFILE_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_RISK_PROFILE_TEMPLATE.md`
- Source: `awesome-qa-skills-skill-quality-engineering-toolkit-v1.0/docs/skill-quality-engineering/{en,zh}/` (source material only; do not record that absolute path in the repository)

**Interfaces:**
- Consumes: The approved SQET spec, the attachment's three bilingual core-document pairs and five templates, and the existing governance status and Pilot contracts.
- Produces: Self-contained bilingual SQET entry/core documents and five credential-free templates; Tasks 2 and 3 rely on these stable paths.

- [ ] **Step 1: Create the bilingual project entry**

Create Chinese-default `README.md` and English `README_EN.md`. List SQEM, the Eval Contract, the Pilot, and the five templates. Explain the responsibility split between SQET and `skills/skill-engineering/`, and map existing Quality Score, Evidence Contract, Quality Loop, Skill-local Evals, and Pilot records. State that the current status is Pilot validation, not repository-wide runtime quality or release approval.

- [ ] **Step 2: Import the three core-document pairs with minimal adaptation**

Place the attachment's `en/` and `zh/` documents as repository `NAME.md` / `NAME_EN.md` files. Preserve SQEM's seven domains, L1-L4, E1-E4, Risk Profile, Quality Profile, Quality Claim Gate, Eval case types, and five Pilot candidates. Add the repository's existing Router `skill.selection` / `selected_skills` evidence rules and Evidence Contract boundary.

- [ ] **Step 3: Correct status and Pilot semantics**

Rewrite the attachment Quality Profile's `PARTIAL` examples as `INSUFFICIENT_EVIDENCE`, `UNASSESSED`, or itemized evidence; preserve and explain `NOT_SCORED`. State in the Pilot document that the five SQEM candidates are methodology Pilots, not replacements for the existing `requirements-analysis`, `ui-test-playwright`, and `discover-testing` records. Without real Agent, target-environment, cross-model, or business evidence, keep results `NOT_RUN`, `BLOCKED`, or `INSUFFICIENT_EVIDENCE`.

- [ ] **Step 4: Copy the five language-neutral templates**

Import the Behavior Contract, Evidence Report, Quality CI, Quality Profile, and Risk Profile templates. Preserve empty fields and example structure; do not fill in real Skill results, models, credentials, paths, or runtime conclusions.

- [ ] **Step 5: Run the document static check**

Run: `git diff --check`

Expected: exit 0, and `rg -n 'TODO|TBD|Bearer|/Users/|/home/' docs/skill-quality-engineering` produces no output. Manually verify that the new documents make methodology and boundary claims only, not runtime claims from configuration validity.

- [ ] **Step 6: Commit**

```bash
git add docs/skill-quality-engineering
git commit -m "docs(sqet): add toolkit methodology docs"
```

### Task 2: Add root Eval and Evidence navigation boundaries

**Files:**
- Create: `evals/README.md`
- Create: `evals/README_EN.md`
- Create: `evidence/skill-quality/README.md`
- Create: `evidence/skill-quality/README_EN.md`

**Interfaces:**
- Consumes: Task 1's SQET entry and source-of-truth mapping.
- Produces: Root directory guidance for Task 3 registration and final gates; no Eval cases or Evidence Reports.

- [ ] **Step 1: Create the bilingual Eval README**

State that Skill-local `eval.yaml` / cases are the default source of truth. The root directory may later hold runner-adapted, cross-Skill, or aggregate assets only after a separate design; no existing cases are moved or copied.

- [ ] **Step 2: Create the bilingual Evidence README**

State that evidence should record Skill commit/version, Eval version, engine/model, judge, environment, timestamp, result, limitations, and supported/unsupported quality claims. This phase creates guidance only and no report.

- [ ] **Step 3: Bind the root-boundary content check**

Run: `rg -n 'Skill-local|source of truth|NOT_RUN|limitations|supported|unsupported' evals/README.md evals/README_EN.md evidence/skill-quality/README.md evidence/skill-quality/README_EN.md`

Expected: both language entries state that Skill-local Evals are canonical and unexecuted work cannot become a quality conclusion; no `eval.yaml`, case, or Evidence Report instance exists under the new root directories.

- [ ] **Step 4: Commit**

```bash
git add evals/README.md evals/README_EN.md evidence/skill-quality/README.md evidence/skill-quality/README_EN.md
git commit -m "docs(sqet): add eval and evidence entrypoints"
```

### Task 3: Register bilingual checks and update repository entry points

**Files:**
- Modify: `scripts/check_docs_bilingual.py` (`PROJECT_PAIRS`)
- Modify: `scripts/tests/test_check_docs_bilingual.py`
- Modify: `README.md:16`
- Modify: `README_EN.md:16`

**Interfaces:**
- Consumes: The paths and bidirectional switches created in Tasks 1 and 2.
- Produces: `check_docs_bilingual.py` checks existence, switches, and relative links for six new project-document pairs; root README exposes SQET without listing it as an installable Skill.

- [ ] **Step 1: Add a bilingual-pair regression test**

Add a test in `scripts/tests/test_check_docs_bilingual.py` asserting that these six tuples are present in `PROJECT_PAIRS`:

```text
("docs/skill-quality-engineering/README.md", "docs/skill-quality-engineering/README_EN.md")
("docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL.md", "docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL_EN.md")
("docs/skill-quality-engineering/SKILL_EVAL_CONTRACT.md", "docs/skill-quality-engineering/SKILL_EVAL_CONTRACT_EN.md")
("docs/skill-quality-engineering/SKILL_QUALITY_PILOT.md", "docs/skill-quality-engineering/SKILL_QUALITY_PILOT_EN.md")
("evals/README.md", "evals/README_EN.md")
("evidence/skill-quality/README.md", "evidence/skill-quality/README_EN.md")
```

- [ ] **Step 2: Register the six project-document pairs**

Add the tuples to `PROJECT_PAIRS`, keeping them unique. Do not register the five language-neutral templates as project-level bilingual pairs.

- [ ] **Step 3: Update the root README quick links**

Add `docs/skill-quality-engineering/README.md` to the Chinese quick links in `README.md` and the `_EN.md` counterpart to the English Quick links. Do not change Skill counts, installation commands, or the Skill catalog count.

- [ ] **Step 4: Run the focused tests**

Run: `python3 -m unittest discover -s scripts/tests -p 'test_check_docs_bilingual.py' -v`

Expected: all tests PASS, including the new registration test that prevents future removal of the SQET pair registry.

- [ ] **Step 5: Run the bilingual validator**

Run: `python3 scripts/check_docs_bilingual.py --repo-root .`

Expected: `bilingual_docs_findings=0`, with all new relative Markdown links resolving.

- [ ] **Step 6: Commit**

```bash
git add README.md README_EN.md scripts/check_docs_bilingual.py scripts/tests/test_check_docs_bilingual.py
git commit -m "docs(sqet): register bilingual toolkit entrypoints"
```

### Task 4: Run the full quality gate and delivery review

**Files:**
- Test only: all Task 1-3 changed files
- Review only: `git status`, `git diff --stat`, and the committed file list

**Interfaces:**
- Consumes: Task 1-3 commits and verification results.
- Produces: Reviewable final static-quality evidence; no push, runtime evidence, or unrelated generated-file changes.

- [ ] **Step 1: Check the commit scope**

Run: `git status --short --branch` and `git diff origin/develop...HEAD --name-status`

Expected: only the SQET spec/plan already created and the Toolkit documents, root entry points, bilingual validator, and test changes are present; no Skill content, existing governance Pilot, cache, secret, or unrelated generated file appears.

- [ ] **Step 2: Run the repository-wide quality gate**

Run: `bash scripts/check_skills_quality.sh`

Expected: exit 0; Skill CLI compatibility, Skill integrity, the Evaluation Quality Loop contract, bilingual docs, the local rule catalog, and script tests pass. Toolkit integration must not change Skill counts or installation compatibility.

- [ ] **Step 3: Run final format and boundary checks**

Run: `git diff --check`

Expected: exit 0. Then manually review the new entry points for unexecuted `PASS`, benchmark, runtime, compatibility, production, or release-approval claims.

- [ ] **Step 4: Record delivery state**

Run: `git status --short --branch` and `git log -4 --oneline --decorate`

Expected: clean working tree; implementation commits exist on the current branch; do not run `git push` unless the user explicitly requests it.

## Plan self-review

- **Spec coverage:** Task 1 covers the spec directory, source mapping, status mapping, and Pilot coexistence; Task 2 covers root Eval/Evidence boundaries; Task 3 covers bilingual guards and root entry links; Task 4 covers acceptance and risk checks.
- **Step scan:** Each step has one checkable result; document import, semantic adaptation, test registration, entry updates, and quality gates are not hidden inside one unreviewable step.
- **Type consistency:** All paths use the final `NAME.md` / `NAME_EN.md` convention; the six `PROJECT_PAIRS` entries exactly match the files created in Tasks 1 and 2.
- **Review-focus coverage:** All five failure modes are bound to the status, content, unit, full-gate, and manual reviews in Tasks 1-4.
- **Proportion:** The plan decides files, adaptation rules, commands, and commit boundaries without rewriting the attachment body or implementing future Pilot execution.
