<div align="right"><a href="./2026-09-28-skill-quality-engineering-toolkit-integration-design.md">🇨🇳 Chinese</a> | <strong>🇬🇧 English</strong></div>

# Skill Quality Engineering Toolkit v1.0 Integration Design

> Date: 2026-09-28<br>
> Status: Plan B approved in chat; awaiting written spec review<br>
> Scope: Integrate the supplied SQET v1.0 Toolkit as engineering documentation assets in `awesome-qa-skills`<br>
> Non-goals: No installable Skill, real model/Agent Pilot, or fabricated runtime evidence in this phase

## 1. Design conclusion

Use a compatibility integration. Do not copy the attachment verbatim, and do not migrate the existing governance documents immediately.

The supplied Toolkit is adopted as a candidate methodology for SQEM, the Eval Case Contract, the Pilot plan, and templates. The repository's existing Quality Score, Evidence State, Skill Evaluation Quality Loop, and Skill-local Eval structures remain the current engineering sources of truth. The new entry point will explain their relationship without creating a second quality-score system, Eval Engine, or global case repository.

The attachment's root `README.md` is packaging guidance and will not replace the repository root README. Its `en/` / `zh/` layout will be normalized to this repository's project-document convention: `NAME.md` / `NAME_EN.md`.

## 2. Review findings

### 2.1 Attachment review

- The package contains a packaging README, a Toolkit README, bilingual versions of three core documents, five templates, an Eval README, and an Evidence README.
- The three core document pairs have matching section numbering and counts. Static scanning found no `TODO`, `TBD`, obvious secrets, absolute local paths, or package-internal Markdown link issues.
- The material consistently emphasizes `Quality Claim <= Available Evidence`, treats the Pilot as a system under test, and keeps static validation separate from runtime evidence. These principles align with the repository's evidence boundaries.
- The attachment uses `PARTIAL` in status examples but does not include the repository's existing `NOT_SCORED` / `UNASSESSED` semantics. A verbatim copy would split status meaning.
- The attachment's five SQEM Pilot Skills differ from the repository's existing analysis / executable / router Pilots. Replacing the current record would lose established Pilot context.

### 2.2 Repository compatibility review

- The repository already has `docs/SKILL_QUALITY_GATE*`, `docs/governance/SKILL_EVALUATION_CONTRACT*`, `QUALITY_SCORE_EVAL_CONTRACT*`, `SKILL_EVALUATION_DESIGN*`, and `SKILL_EVALUATION_PILOTS*`.
- Repository Eval cases are primarily owned by `skills/{zh,en}/.../evals/`; the Toolkit root `evals/README.md` must not create a second source of truth.
- `scripts/check_docs_bilingual.py` uses an explicit project-document pair registry. The new Toolkit documents must be registered or bilingual parity will not be guarded.
- The baseline `bash scripts/check_skills_quality.sh` passed, and this review produced no working-tree changes.

## 3. Goals

1. Provide a stable `docs/skill-quality-engineering/` entry point explaining SQET, SQEM, the Eval Contract, the Pilot, templates, and evidence directories.
2. Preserve SQEM's seven quality domains, L1-L4 Test Levels, E1-E4 Evidence Levels, Risk Profile, Quality Profile, and Quality Claim Gate.
3. Connect the attachment's Eval Contract to the existing evidence-state, judge, trace, regression, and failure-classification boundaries instead of creating new runtime rules.
4. Make the Chinese default entry, English mirror, and root Eval/Evidence entries pass the repository's bilingual documentation checks.
5. Allow incremental future Pilot work while preserving the current `NOT_RUN`, `NOT_SCORED`, `UNASSESSED`, and `INSUFFICIENT_EVIDENCE` boundaries.

## 4. Non-goals

- Turn SQET into an installable Agent Skill under `skills/`.
- Delete, rename, or overwrite existing governance documents.
- Represent the attachment's five Pilot Skills as completed runtime evaluations.
- Copy existing Skill-local Eval cases into a root-level directory.
- Add Quality Score dimensions, a second Eval Engine, a second Judge framework, or an automatic optimization loop.
- Present `skill-up validate`, static checks, project state, or configuration validity as runtime, production, or business-acceptance evidence.
- Commit real model outputs, target-environment results, or unauthorized Evidence Reports in this phase.

## 5. Target directory structure

The new or adjusted scope will be:

```text
docs/skill-quality-engineering/
├── README.md
├── README_EN.md
├── SKILL_QUALITY_EVALUATION_MODEL.md
├── SKILL_QUALITY_EVALUATION_MODEL_EN.md
├── SKILL_EVAL_CONTRACT.md
├── SKILL_EVAL_CONTRACT_EN.md
├── SKILL_QUALITY_PILOT.md
├── SKILL_QUALITY_PILOT_EN.md
└── templates/
    ├── SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md
    ├── SKILL_EVIDENCE_REPORT_TEMPLATE.md
    ├── SKILL_QUALITY_CI_GUIDE.md
    ├── SKILL_QUALITY_PROFILE_TEMPLATE.md
    └── SKILL_RISK_PROFILE_TEMPLATE.md

evals/
├── README.md
└── README_EN.md

evidence/skill-quality/
├── README.md
└── README_EN.md
```

The attachment's packaging README will not be copied to the repository root. The five templates remain English/language-neutral output structures; they do not replace Chinese/English mirrors of the core methodology documents.

## 6. Sources of truth and compatibility boundaries

| Topic | Current source of truth | SQET responsibility | Integration decision |
| --- | --- | --- | --- |
| Quality model | New SQEM documents | Define seven domains, validation depth, and claim boundaries | Methodology entry; no overall score |
| Quality Score | `docs/governance/QUALITY_SCORE_EVAL_CONTRACT*` | SQEM explains when score evidence is needed | Existing contract remains exclusive owner |
| Evidence State | `docs/governance/SKILL_EVALUATION_CONTRACT*` | Eval Contract describes case intent and evidence capture | Runtime states follow the existing contract |
| Quality Loop | `docs/governance/SKILL_EVALUATION_DESIGN*` | SQEM Pilot supplies a higher-level methodology probe | No second Engine / Judge |
| Pilot records | `docs/governance/SKILL_EVALUATION_PILOTS*` | SQEM Pilot tests whether the methodology is useful | Both remain, with different purposes |
| Skill cases | Each Skill's `evals/` | Root README supplies navigation and adapter guidance | No duplicated global case repository |
| Runtime evidence | Runner trace, metadata, judge, and report | Evidence README defines recording boundaries | Unexecuted work remains unrun |

### 6.1 Status mapping

The integrated core documents create no new repository-level status and do not redefine status semantics; runtime results directly reference the [Skill Evaluation Contract](../../governance/SKILL_EVALUATION_CONTRACT_EN.md). This section records only how attachment wording is adapted to that primary contract:

| Attachment wording | Integrated handling |
| --- | --- |
| Existing Evidence States | Reference the primary contract as-is; do not redefine them in this spec |
| `PARTIAL` | Do not import it as a repository-level status; report item by item according to the primary contract and actual evidence |

This preserves the attachment's risk and evidence model without creating a second repository state machine.

### 6.2 Pilot mapping

The attachment names these five SQEM Pilot candidates:

```text
functional-testing
testability-analysis
performance-testing
skill-evaluation-design
skill-change-verification
```

The attachment method name `skill-evaluation-design` maps to the existing canonical repository Skill `skill-evaluation` (`skills/{zh,en}/skill-engineering/skill-evaluation/`); this integration creates no alias directory. In this integration they are the “SQEM methodology Pilot candidate set,” used to test whether the quality model is understandable, executable, and maintainable. They do not replace the repository's existing:

- `requirements-analysis` analysis Pilot;
- `ui-test-playwright` executable Pilot;
- `discover-testing` Router Composition Pilot.

If future work adds or changes Evals for the five candidates, it must reuse the existing Skill-local `eval.yaml`, case, trace, and evidence structures, with authorization, environment, version, judge, and limitations recorded separately.

## 7. Content adaptation

### 7.1 Toolkit README

The Chinese `README.md` is the default entry and `README_EN.md` is its mirror. The entry must list:

- SQEM, the Eval Contract, the Pilot, and the five templates;
- the responsibility split between the Toolkit and `skills/skill-engineering/`;
- the relationship to the existing Quality Score, Evidence Contract, Quality Loop, and Pilot records;
- the fact that root `evals/` and `evidence/skill-quality/` are navigation/evidence locations, not a second execution framework;
- the current Pilot-validation status, which is not repository-wide runtime quality or release approval.

### 7.2 SQEM and Eval Contract

Preserve the attachment's main structure, with repository-specific notes that:

- quality claims are bounded by available evidence;
- Quality Score is not redefined inside SQEM;
- Router behavior and evidence handling remain governed solely by the existing Evaluation Contract; this spec does not restate its fields or verdict rules;
- the attachment's `PARTIAL` is not imported as a repository-level status;
- benchmark, compatibility, runtime, and real-world claims require real, reviewable evidence.

### 7.3 Pilot

Preserve the five candidates, stages, metrics, exit criteria, and four possible decisions, while adding that:

- this is a SQEM methodology Pilot, not a replacement for the existing executable or router Pilots;
- Pilot stages 6-8 must follow the existing Evaluation Contract's evidence boundaries without real Agents, target environments, cross-model evidence, or business-acceptance evidence;
- the candidate list must not be written as completed profiles, benchmarks, or compatibility conclusions.

### 7.4 Root Eval / Evidence READMEs

`evals/README.md` will state that Skill-local Evals are the default source of truth. The root directory may later hold runner-adapted, cross-Skill, or aggregate assets only after a separate design.

`evidence/skill-quality/README.md` will require Skill commit/version, Eval version, engine/model, judge, environment, time, result, limitations, and supported/unsupported claims. This phase creates directory guidance only and adds no report.

## 8. Change scope and execution order

After written approval of this spec, implementation will proceed as follows:

1. Import the core documents and five templates from the attachment, applying the repository naming and status contract with minimal edits.
2. Create bilingual Toolkit, Eval, and Evidence entries, including source-of-truth mapping and Pilot boundaries.
3. Update the root `README.md` / `README_EN.md` quality-engineering quick links; do not add Toolkit to the installable Skill catalog.
4. Register the new project-document pairs in `scripts/check_docs_bilingual.py`.
5. Check all new Markdown links, status terms, directory structure, and `git diff --check`.
6. Run repository quality and bilingual gates; if an existing governance contract conflicts, stop and fix the documentation rather than bypassing it with aliases.

## 9. Acceptance criteria

- The directory structure matches this spec and does not copy the attachment packaging README or blog content.
- Chinese/English core entries and all three core document pairs have bidirectional switch links.
- The five templates are independently usable and contain no credentials or local machine paths.
- The Toolkit entry makes the boundaries between SQEM, the Eval Contract, the existing Evidence Contract, Quality Score, and Quality Loop traceable.
- The attachment's `PARTIAL` is not imported; status semantics and verdict rules remain exclusively owned by the existing Evaluation Contract.
- The five SQEM candidates and the existing three Pilot categories are explicitly distinguished; no existing Pilot is deleted or overwritten.
- No unexecuted PASS, benchmark, runtime, compatibility, production, or release claim is added.
- `bash scripts/check_skills_quality.sh`, `python3 scripts/check_docs_bilingual.py --repo-root .`, and `git diff --check` pass.
- Only Toolkit-related files are committed; generated reports, caches, secrets, and unrelated changes are excluded.

## 10. Risks and handling

| Risk | Handling |
| --- | --- |
| New and existing documents redefine statuses or scores | Add source-of-truth mapping; SQET does not copy score or runtime-state contracts |
| Root `evals/` is mistaken for a second case repository | State that Skill-local Evals remain canonical and root content is navigation/adapter guidance |
| Pilot names imply existing runtime evidence | Distinguish the methodology candidate set from the existing executable/router Pilots |
| New bilingual files are not guarded | Register the new project-document pairs in `check_docs_bilingual.py` |
| External reference families are mistaken for compatibility proof | Keep them non-normative and do not turn the list into compatibility evidence |
| Future runtime work needs high cost or external permissions | Follow the existing Evaluation Contract's evidence boundaries until separately authorized and recorded with run metadata |

## 11. Follow-up work outside this integration

- Add or review real Skill-local Eval suites for the five SQEM candidates.
- Create Quality Profile, Risk Profile, Behavior Contract, and Evidence Report instances.
- Run representative evaluations, benchmarks, and compatibility sampling in authorized Agent/runtime environments.
- Use Pilot findings to propose SQEM v1.1 changes rather than announcing adoption during the v1.0 documentation integration.
