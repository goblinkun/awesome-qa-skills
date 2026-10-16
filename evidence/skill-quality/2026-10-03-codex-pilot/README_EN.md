<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# SQET Codex Pilot Evidence Report

Use this report to review the five SQEM Pilots' real text runs, selected Benchmarks, and cross-model sampling. The runs occurred on **2026-10-03**. This is engineering evidence, not business acceptance or release approval.

## Results

| Check | Result | Boundary |
| --- | --- | --- |
| Five Pilots, bilingual core cases | 34/34 `PASS` | 34 runnable cases out of 36 planned; latest complete suites after Eval repairs, one selected run per case |
| Testability safety boundary, Chinese | `BLOCKED` | Native `ERROR`: provider safety filtering before an answer; no conclusion about the Skill's refusal behavior |
| Equivalent safety boundary, English | `NOT_RUN` | Withheld after the Chinese request was blocked; no result inferred and no model switch to bypass filtering |
| Second Codex model | 5/5 `PASS` | Five Chinese `basic-success` cases only, not a complete second-model matrix |
| Selected Benchmarks | Three pairs executed | One with/without trial per pair; interpretation below |
| Judge smoke calibration | 7/7 expected labels matched | Synthetic positive/negative and near-miss fixtures; excluded from real Pilot pass counts, not statistical reliability |
| Natural trigger/selection | `BLOCKED` | No canonical `skill.selection` event; catalog availability and file reads are not substitutes |
| Claude runtime | `NOT_RUN` | No provider environment credentials in the current process; an installed CLI is not acceptance evidence |
| Real business acceptance | `NOT_RUN` | Missing project, approved environment/actions, criteria, and accountable acceptance decision |
| Quality Score / formal test level | `NOT_SCORED` / `UNASSESSED` | Assertion rates are not a global score; no full L3/L4 or release conclusion awarded |

Current core: functional-testing 6/6, testability-analysis 10/10 (plus the two unverified safety cases above), performance-testing 6/6, skill-evaluation 6/6, and skill-change-verification 6/6. Both languages cover success, incomplete input, and scope/risk boundaries. These are text behaviors under explicit Skill-use requests.

## Run Metadata

- Base commit: `c61f507f61711c3c0f0d1777136a5a4ff0e211b3`, **with uncommitted changes**. Exact identity is in [source-manifest.json](./source-manifest.json) and [source-changes.patch](./source-changes.patch); HEAD alone does not identify the tested version.
- Main engine: `skill-up 0.12.0`, using its custom local transport to call native `codex-cli --no-daemon`. The transport adapter does not implement another Judge, Benchmark, or scoring engine. The historical adapter hardcoded `codex_version` as `0.159.2` instead of independently probing it; individual CLI versions remain `unknown`, not proof that every call used that version.
- Provider: `openai`. Primary requested/observed model: `gpt-6.1-sol`; second model and Benchmark semantic judge: `gpt-6-sol`; reasoning effort: `high`.
- Observed model comes from the CLI session's client `turn_context`; **server-confirmed identity is `unknown`**.
- Environment: macOS arm64, Node.js v26.10.0, temporary workspaces, 900-second case timeout. Production, browser, and real target environments were out of scope.
- Codex sandbox bypass was authorized by the human. User project instructions and global/plugin Skills were disabled. With Skill installs only the target at `.agents/skills/<canonical-name>`; without Skill and judge calls do not load it.
- Per-call timestamps, models, usage, catalogs, and errors are retained. Historical per-invocation adapter hashes were not captured and remain `unknown`. The collected and portable adapter hashes are separate, not retrospective proof of identical historical bytes.

## Interpreting the Benchmarks

Each pair holds the primary model, input, reasoning effort, restrictions, and rubric constant; the baseline has no target Skill. Skill-specific report headings are not quality requirements.

| Skill | With Skill | Without Skill | Supported conclusion |
| --- | --- | --- | --- |
| functional-testing | `PASS`, 5/5 semantic criteria | `PASS`, 5/5 | No quality uplift observed on this single, well-specified task |
| testability-analysis | `PASS`, 5/5 | `PASS`, 5/5 | Same; this does not establish lack of value on sparse or difficult inputs |
| skill-evaluation | `PASS`, canonical states present, 5/5 semantic criteria | `FAIL`, lacks `NOT_RUN` and `BLOCKED` | An observed machine-readable state-contract difference, **not generalized semantic improvement** |

The third baseline described missing runs/evidence in natural language; its reasoning must not all be labeled incorrect. Both variants used the same canonical-state precondition. After the baseline failed it, `skill-up` did not invoke the semantic judge. Its native 1/2 and the Skill variant's 7/7 assertion rates are not comparable semantic scores. The first Benchmark and the judge's false acceptance remain archived separately from the rerun.

Every variant in this report's original round has one sample, run sequentially, with no confidence interval, stability, or long-term effectiveness claim. This is not previous/current version regression.

Two further pairs per unchanged Chinese task were executed on 2026-10-05, giving three samples per variant including the original. The [follow-up report](../2026-10-05-codex-benchmark-repeat/README_EN.md) retains per-sample results, one testability-baseline FAIL, and interrupted-call costs without rewriting these original single-trial results.

## Five Profiles

Each document keeps Quality Profile, Risk Profile, and Behavior Contract as separate sections under one entry point:

- [functional-testing](./profiles/functional-testing_EN.md)
- [testability-analysis](./profiles/testability-analysis_EN.md)
- [performance-testing](./profiles/performance-testing_EN.md)
- [skill-evaluation](./profiles/skill-evaluation_EN.md)
- [skill-change-verification](./profiles/skill-change-verification_EN.md)

## Review and Reproduction

Start with the case selection and states in [results.json](./results.json), then follow each `report`, `grading`, and `metadata` path. Historical FAIL, old Evals, provider ERROR, and repaired PASS are separate cohorts; do not conceal failures by showing only green results.

- [Findings and repairs](./FINDINGS_EN.md): separate Skill/Eval/Infrastructure/Unknown classifications.
- [Cost report](./COST_REPORT_EN.md): separate main/judge usage and unknown monetary costs.
- [Reproduction](./reproduction/README_EN.md): fixed parameters, complete current snapshots, portable transport adapter, and unit tests.
- [Business acceptance checklist](./BUSINESS_ACCEPTANCE_EN.md): requires a real project.
- [SQEM v1.1 proposal](./SQEM_V1_1_PROPOSAL_EN.md): proposals, not a newly released standard.
- [artifact-manifest.json](./artifact-manifest.json): original/exported SHA256 and path replacements.

`artifacts/` contains **sanitized exports**, not universally byte-identical private raw files. Native states and real provider errors remain; local paths become symbolic markers. The first incompletely isolated smoke and September 30 legacy runs are excluded. Reproduction packages are evidence assets, not newly installable Skills or automatic CI model calls.

The 2026-10-04 closeout repaired missed macOS temporary ancestor paths in one trace. Two offline regressions check that trace and the entire evidence package for local paths and common credential patterns; native results and usage are unchanged. The original SHA256 is retained and the exported SHA256 updated. Full quality-gate and audit logs are linked from [verification.json](./verification.json).

The 2026-10-16 delivery review corrected CLI-version claims and reproduction under paths containing spaces/Unicode. The [original portable adapter](./reproduction/snapshots/adapter-20261005.mjs) is frozen at its original SHA256. The corrected adapter probes `--version` for future calls and records unknown when probing fails. Four added offline regressions passed red/green checks; no new model smoke ran, and the historical portable smoke applies only to the original adapter. Native results, grading, and usage are unchanged; see [reproduction](./reproduction/README_EN.md).

## Remaining Acceptance

Real evidence now supports engineering text checks and selected comparisons, but unconditional Pilot closure is not justified. Natural selection, the blocked safety case, broader difficult-input sampling, human judge calibration, Claude compatibility, real business acceptance, and acceptable cost remain unconfirmed. This report must not be promoted to business or release approval.
