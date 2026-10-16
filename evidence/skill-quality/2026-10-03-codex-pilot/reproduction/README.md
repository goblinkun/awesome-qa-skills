<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# 复核与复现

用于复核本次已运行的 Codex 文本 Pilot。`packages/` 是当前测试快照，不是新产品 Skill 目录。入口报告见 [README](../README.md)。模型再次运行会消耗账户额度，并可能产生不同回答，不应为了追求同一绿灯无限重跑。

## 先离线复核

检查 [results.json](../results.json)、[source-manifest.json](../source-manifest.json)、[artifact-manifest.json](../artifact-manifest.json) 和各 case 的原生 result/grading/events。源版本由指定基线加工作区 patch 及每文件 SHA256 构成；历史 Eval 的完整字节哈希和每次适配器哈希未捕获，不能补写成已知。

初始可移植适配器与实际调用收集版只有 Codex binary 定位差异：由本机安装路径变为 PATH 中的 `codex`；两版哈希分别记录，不声称字节相同。初始可移植版现冻结在 [snapshots/adapter-20261005.mjs](./snapshots/adapter-20261005.mjs)，SHA256 为 `c193c5037be7c7986ff1823bed5e5972731fb209534664b25a115d920a23fedf`。后续报告的采集哈希继续指向这些原始字节，不追认修正版曾用于历史运行。`native-evals/` 保留仓库原本的 Claude 配置；`packages/*/evals/eval.yaml` 仅覆盖本次 Codex 的传输、安装目标、模型与 timeout。安全边界的 judge-model override 单独记录，实际未执行 judge。

2026-10-16 交付前修正：当前 `adapter.mjs` 在未来调用前用 `codex --version` 实际探测版本，失败时写 `null` / `unknown`；calibration 委派和测试 fixture 使用 `fileURLToPath` 处理空格/中文路径。历史 metadata 中的 `0.159.2` 是硬编码值，不能作为逐调用实测。2026-10-05 的 `source-identity.json` 只证明采集时 CLI 为 `0.160.0`；历史逐调用版本仍未知。修正版仅经过离线回归，未执行新的真实模型 smoke。

两批归档目录内的 `.gitattributes` 仅对捕获输出、源快照、历史 patch 和终端日志保留原始空白/行尾，不以格式化改变哈希。手写报告、当前适配器与测试不在该豁免范围内。

可移植配置已实际运行一次 skill-evaluation 中文不完整输入 smoke，结果 PASS；原生证据在 [portable-smoke](../artifacts/portable-smoke/iteration-1/result.json)。离线复核见 [verification.json](../verification.json)。首次 smoke 在调用模型前因 event-log 父目录缺失退出，复现步骤已补创建目录；这个配置错误不计作 Skill 失败。

## 前置条件

原运行使用 `skill-up 0.12.0`、Node.js v26.10.0；逐调用 Codex CLI 版本未独立采集。重跑前核对实际 CLI 是否支持本配置的参数、记录真实版本并确认可用登录。不要把 token 写入文件或复制用户认证文件。

**安全提示：适配器调用 `--dangerously-bypass-approvals-and-sandbox`，本次仅获授权在临时工作区做文本评测。复现前审查目标 Skill/用例并确认同等授权；提示词中的只读约束不是操作系统隔离。** 不得把该开关推广到未审查内容或生产操作。

在仓库根目录先验证（不调用模型）：

```bash
SQET_EVIDENCE="$PWD/evidence/skill-quality/2026-10-03-codex-pilot"
export SQET_ADAPTER="$SQET_EVIDENCE/reproduction/adapter.mjs"
export SQET_CALIBRATION_ADAPTER="$SQET_EVIDENCE/reproduction/calibration/fixture-agent.mjs"
node --test "$SQET_EVIDENCE/reproduction/adapter.test.mjs" \
  "$SQET_EVIDENCE/reproduction/portability.test.mjs" \
  "$SQET_EVIDENCE/reproduction/sanitization.test.mjs"
skill-up validate "$SQET_EVIDENCE/reproduction/packages/functional-testing-zh/evals/eval.yaml"
```

`SQET_*` 是本任务专用变量，不改 HOME、CODEX_HOME 或 Git 配置。

六条适配器测试、四条可移植性/版本回归与两条证据脱敏回归均不调用模型。脱敏回归覆盖已捕获的祖先目录探测及全包常见本机路径/凭据模式，但不是对所有凭据格式的完整安全审计。

## 经授权重跑

复制快照到新建临时目录，避免改动归档或混入旧输出：

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

对其余 slug 使用同一命令，先创建对应 output/event-log 父目录。两个 testability-analysis 核心组必须额外使用 `--exclude-case-name architecture-unsafe-seam-boundary`：原请求受服务端安全限制，不在本次授权下重试/换模型绕过。被排除 case 保持 BLOCKED/NOT_RUN，不算通过。

选定 Benchmark 使用 functional-testing-zh、testability-analysis-zh 或 skill-evaluation-zh 的 `evals/benchmark.yaml`；不加 `--include-case-name basic-success`。每组同时运行 with/without，baseline FAIL 可能是有效结果。第二模型采样则使用核心配置并加：

```bash
--provider openai --model gpt-6-sol --include-case-name basic-success
```

Judge 校准配置在 `calibration/evals/eval.yaml`，主体是明确标记的合成回答，judge 才调用 Codex；负向与 near-miss 应 FAIL，命令非零不能直接理解为校准失败。当前复现 fixtures 是修订后版本；历史旧 golden 可从对应原生 result 的 response 复核，不追认旧样例版本相同。

## 不可从复现推断的事项

即便文本组再次通过，也没有 canonical selection event、Claude 验收、业务实测或 release approval。当前适配器用真实 CLI/model/usage 作为传输证据，仍由 skill-up 负责所有原生判分与 Benchmark。适配器不提供额外语义评分，也不自动修复 Skill。
