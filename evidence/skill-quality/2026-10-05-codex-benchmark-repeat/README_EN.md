<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# SQET Codex Benchmark Repeated Sampling

Review three existing Chinese Benchmarks from the [2026-10-03 Pilot](../2026-10-03-codex-pilot/README_EN.md). Two complete with/without pairs per Skill were added on 2026-10-05, giving three samples per variant including the original. No tasks, Skills, assertions, thresholds, or Judges were changed.

## Results and Supported Claims

| Skill | With Skill | Without Skill | Interpretation |
| --- | --- | --- | --- |
| functional-testing | 3/3 `PASS` | 3/3 `PASS` | Both variants met 5/5 semantic criteria each time; no quality uplift observed on this task |
| testability-analysis | 3/3 `PASS` | 2/3 `PASS` | With: 5/5 each time; without: 5/5, 4/5, 3/5, with one answer below the unchanged 0.8 threshold; a limited sample difference |
| skill-evaluation | 3/3 `PASS` | 0/3 `PASS` | Baselines failed canonical-state preconditions and skipped semantic judging; a state-contract difference, not generalized semantic uplift |

See [results.json](./results.json) for individual statuses, grading, and native traces. The original pair is referenced once and excluded from this round's cost. Interrupted calls are not paired samples. No cross-Skill total score, Quality Score, statistical significance, or formal L3 level was calculated.

### One Testability Baseline FAIL

[Native grading](./artifacts/repeat/testability-analysis-zh/iteration-2/benchmark-neutral/without_skill/grading.json) identified two missing explanations: least-privilege test identities/resource access, and explicit stop conditions for duplicate charges or cross-run contamination. The answer already limited fault controls to test environments and retained signature validation, isolation, and business decisions.

This does not prove actual weakening of production safety and is not a target-Skill failure. An independent business reviewer has not confirmed the Judge labels. Blind-review this answer and its corresponding Skill variant before accepting the classification. Retain native FAIL without automatically changing the baseline, rubric, or threshold.

## Runtime and Evidence Identity

- Primary: `gpt-6.1-sol`; Judge: `gpt-6-sol`; reasoning effort: `high`. Observed identity comes from client `turn_context`; server-confirmed identity remains `unknown`.
- `skill-up 0.12.0`, Node.js v26.10.0. The temporary text transport was reused, with no second evaluation engine or scorer. Post-execution `source-identity.json` records `codex-cli 0.160.0`; historical metadata hardcoded `0.159.2` rather than probing each call. Individual historical CLI versions remain `unknown`; the collection-time version is not assigned retrospectively to every run.
- Each group ran with→without sequentially for two iterations; three independent groups ran concurrently. No randomization, blinding, or new domain inputs.
- [source-identity.json](./source-identity.json) confirms 80 package files match the original archived snapshot. The baseline includes uncommitted changes; HEAD alone is insufficient identity.
- Adapter and Node hashes were collected after execution. Per-call hashes and the original round's Node binary hash were not captured and must not be invented.
- The 2026-10-16 delivery correction points the collected hash to a byte-identical [frozen adapter](../2026-10-03-codex-pilot/reproduction/snapshots/adapter-20261005.mjs), retaining the original source path separately. The current adapter adds future version probing; path fixes and four regressions were verified offline only, with no new model execution. Native results, grading, usage, and their hashes are unchanged.
- Global/plugin Skills were disabled. With-Skill catalogs contained only the target; without-Skill and Judge catalogs were empty. Catalogs/file reads still do not establish natural `skill.selection`.

An earlier diagnostic encountered a missing Homebrew Node library before the user interrupted execution. Node recovered after external relinking; this task did not modify Homebrew or system libraries. Four completed native calls were recovered, but no complete Benchmark grading report. They are retained under `artifacts/interrupted/`, excluded from paired PASS counts. Host binary differences between dates are also comparison limitations.

`artifacts/` contains sanitized exports. [artifact-manifest.json](./artifact-manifest.json) retains original/exported SHA256; model results and real errors are unchanged. [verification.json](./verification.json) records offline audits and the quality gate.

## Additional Cost

| Scope | Calls | Observed input tokens | Observed output tokens |
| --- | ---: | ---: | ---: |
| Six complete new pairs: 12 main, 10 Judge | 22 | 860,249 | 44,258 |
| Recovered interrupted calls: 3 main, 1 Judge | 4 | 173,542 | 10,054 |
| This archive only, excluding original-report calls | 26 | 1,033,791 | 54,312 |

See [cost-ledger.json](./cost-ledger.json). Usage is observed for archived calls. Cached input is a subset of input, not an extra chargeable-token total. Actual monetary cost is `unknown` and acceptable cost remains `UNASSESSED`; shared account usage cannot establish this task's invoice. No quota resets or credits were purchased or used.

## Offline Review and Authorized Rerun

Start with native `result.json`, then follow case `grading.json` and `outputs/`. Do not rewrite baseline FAIL as PASS. Original configuration and transport are in the [reproduction package](../2026-10-03-codex-pilot/reproduction/README_EN.md).

The adapter contains `--dangerously-bypass-approvals-and-sandbox`. Authority here covered reviewed temporary text evaluation only. Prompt restrictions are not OS isolation. Obtain equivalent authority before rerunning; do not generalize it to unreviewed content or production.

From the repository root, run `node --test evidence/skill-quality/2026-10-05-codex-benchmark-repeat/verify-evidence.test.mjs` to audit hashes, paired grading, native usage/catalog isolation, redaction, and bilingual links offline without model calls. Credential-pattern checks are not a comprehensive security audit.

```bash
SQET_PARENT="$PWD/evidence/skill-quality/2026-10-03-codex-pilot"
export SQET_ADAPTER="$SQET_PARENT/reproduction/adapter.mjs"
skill-up validate "$SQET_PARENT/reproduction/packages/functional-testing-zh/evals/benchmark.yaml"

SQET_WORK=$(mktemp -d)
mkdir -p "$SQET_WORK/packages" "$SQET_WORK/results/functional-testing-zh"
cp -R "$SQET_PARENT/reproduction/packages/functional-testing-zh" "$SQET_WORK/packages/"
skill-up run "$SQET_WORK/packages/functional-testing-zh/evals/benchmark.yaml" \
  --iteration 2 --parallelism 1 --format json --format junit \
  --output-dir "$SQET_WORK/results/functional-testing-zh" \
  --event-log "$SQET_WORK/results/functional-testing-zh/events.jsonl"
```

Replace the slug for the other two groups. Reruns consume quota; never overwrite archives or retry indefinitely for green results.

## Still Unfinished

Only finite repetitions of unchanged inputs were added. Difficult-input generalization, independent human Judge calibration, Claude execution, natural selection, the blocked safety case, and [real business acceptance](../2026-10-03-codex-pilot/BUSINESS_ACCEPTANCE_EN.md) remain unfinished. Archived Claude process/login-shell checks on 2026-10-05 reported not logged in, not the current authentication state; [preflight](./verification/auth-preflight-final.jsonl) records presence/status only, never credentials.

Business acceptance requires a project, approved environment/actions, criteria, and accountable reviewer. This report grants no business, production, or release approval. Formal level remains `UNASSESSED`; Quality Score remains `NOT_SCORED`.
