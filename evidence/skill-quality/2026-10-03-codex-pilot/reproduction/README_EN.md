<div align="right"><a href="./README.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Review and Reproduction

Use this directory to review the executed Codex text Pilots. `packages/` contains current reproduction exports, including declared sanitization revisions, not new product Skills. Not every export is byte-identical to the historical snapshot. Start with the [report](../README_EN.md). Reruns consume account quota and can differ; do not rerun indefinitely to obtain matching green results.

## Offline Review First

Review [results.json](../results.json), [source-manifest.json](../source-manifest.json), [artifact-manifest.json](../artifact-manifest.json), and native case results/grading/events. Source identity is the base commit plus worktree patch and per-file hashes. Exact historical Eval and per-invocation adapter hashes were not captured and must not be invented.

The initial portable adapter differed from the collected execution version only in finding `codex` through PATH instead of a local binary path. Their hashes are separate, not claimed identical. That initial portable version is now frozen at [snapshots/adapter-20261005.mjs](./snapshots/adapter-20261005.mjs), SHA256 `c193c5037be7c7986ff1823bed5e5972731fb209534664b25a115d920a23fedf`. Historical collection hashes still resolve to those original bytes; they do not prove the corrected adapter ran historically. `native-evals/` preserves original repository Claude configurations; `packages/*/evals/eval.yaml` overrides only Codex transport, installation target, model, and timeout. The safety-boundary judge-model override is recorded separately; that judge never ran.

The 2026-10-16 delivery correction makes the current `adapter.mjs` probe `codex --version` before future calls, recording `null` / `unknown` on failure. Calibration delegation and test fixtures use `fileURLToPath` for spaces/Unicode. Historical metadata hardcoded `0.159.2`, not an independently measured per-call version. The 2026-10-05 `source-identity.json` establishes only the collection-time CLI version `0.160.0`; historical individual-call versions remain unknown. The corrected adapter has offline regression coverage only, not a new real-model smoke.

The 2026-10-16 security-scan revision replaces one illustrative fixed login password in the Chinese performance-testing [tutorial](./packages/performance-testing-zh/tutorial.md) with `__ENV.TEST_PASSWORD`. Future execution requires an authorized dedicated test-account password supplied through the environment. `artifact-manifest.json` retains the original SHA256 and records the previous export hash, revised export hash, and `byte_identical: false`. The `runtime_snapshot_matches` values in `source-manifest.json` describe the collection-time comparison, not byte identity of the current sanitized export. This is a future-reproduction revision, not retrospective evidence of the historical runtime version. Native outputs, grading, usage, and historical verification logs are unchanged; no new model call or business HTTP request ran. The English archived tutorial did not trigger this fixed-password rule and retains its original bytes.

The two archive-local `.gitattributes` files preserve whitespace/EOL bytes only for captured outputs, source snapshots, historical patches, and terminal logs. Formatting must not change their hashes. Curated reports, current adapters, and tests retain normal checks.

The portable configuration actually ran one Chinese skill-evaluation incomplete-input smoke successfully; native evidence is in [portable-smoke](../artifacts/portable-smoke/iteration-1/result.json). Offline checks are in [verification.json](../verification.json). The first smoke exited before model invocation because the event-log parent did not exist; reproduction now creates it. This configuration error is not a Skill failure.

## Prerequisites

The original run used `skill-up 0.12.0` and Node.js v26.10.0; individual Codex CLI versions were not independently captured. Before rerunning, verify the actual CLI supports these flags, record its version, and confirm available authentication. Never write tokens to these files or copy user authentication files.

**Safety: the adapter calls `--dangerously-bypass-approvals-and-sandbox`. This run was authorized only for temporary-workspace text evaluation. Review the target Skill/cases and obtain equivalent authority before reproduction; prompt-level read-only restrictions are not OS isolation.** Do not apply the flag to unreviewed content or production actions.

From the repository root, validate without model calls:

```bash
SQET_EVIDENCE="$PWD/evidence/skill-quality/2026-10-03-codex-pilot"
export SQET_ADAPTER="$SQET_EVIDENCE/reproduction/adapter.mjs"
export SQET_CALIBRATION_ADAPTER="$SQET_EVIDENCE/reproduction/calibration/fixture-agent.mjs"
node --test "$SQET_EVIDENCE/reproduction/adapter.test.mjs" \
  "$SQET_EVIDENCE/reproduction/portability.test.mjs" \
  "$SQET_EVIDENCE/reproduction/sanitization.test.mjs"
skill-up validate "$SQET_EVIDENCE/reproduction/packages/functional-testing-zh/evals/eval.yaml"
```

These task-specific `SQET_*` variables do not repurpose HOME/CODEX_HOME or change Git configuration.

The six adapter tests, four portability/version regressions, and four evidence-redaction/provenance regressions make no model calls. Redaction checks cover the captured ancestor probes, common local-path/credential patterns across the package, the k6 login example above, and export hashes/original provenance; they are not a comprehensive security audit of every credential format.

## Authorized Rerun

Copy snapshots to a new temporary directory, avoiding archive mutation or old output contamination:

```bash
SQET_WORK=$(mktemp -d)
mkdir -p "$SQET_WORK/packages"
cp -R "$SQET_EVIDENCE/reproduction/packages/." "$SQET_WORK/packages/"
mkdir -p "$SQET_WORK/results/functional-testing-zh"

skill-up run "$SQET_WORK/packages/functional-testing-zh/evals/eval.yaml" \
  --format json --format junit --iteration 1 --parallelism 3 \
  --output-dir "$SQET_WORK/results/functional-testing-zh" \
  --event-log "$SQET_WORK/results/functional-testing-zh/events.jsonl"
```

Use the same command for other slugs, creating each output/event-log parent first. Both testability-analysis core suites must additionally use `--exclude-case-name architecture-unsafe-seam-boundary`. The provider-limited request must not be retried or routed around filtering under this authorization. Excluded cases remain BLOCKED/NOT_RUN, not passed.

Selected Benchmarks use `evals/benchmark.yaml` in functional-testing-zh, testability-analysis-zh, or skill-evaluation-zh, without `--include-case-name basic-success`. Each runs both variants; baseline FAIL can be a valid result. For second-model sampling use the core configuration plus:

```bash
--provider openai --model gpt-6-sol --include-case-name basic-success
```

Judge calibration is in `calibration/evals/eval.yaml`. Main answers are explicitly synthetic; only judges call Codex. Negatives/near-misses should FAIL, so a nonzero command exit is not itself failed calibration. Reproduction fixtures are the revised versions; inspect historical native result responses for old goldens rather than claiming version identity.

## Claims Reproduction Cannot Establish

Passing text suites still does not provide canonical selection events, Claude acceptance, real business measurements, or release approval. The adapter supplies actual CLI/model/usage transport evidence, while skill-up owns native grading and Benchmarks. It adds no semantic scorer and does not modify Skills automatically.
