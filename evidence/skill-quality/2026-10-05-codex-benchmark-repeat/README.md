<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# SQET Codex Benchmark 重复采样

用于复核 [2026-10-03 Pilot](../2026-10-03-codex-pilot/README.md) 的三个既有中文 Benchmark。2026-10-05 每组补两轮完整 with/without 对比，加上原单轮，每侧共三个样本。没有新增任务、修改 Skill、放宽断言或替换 Judge。

## 结果与可支持的结论

| Skill | with Skill | without Skill | 解释 |
| --- | --- | --- | --- |
| functional-testing | 3/3 `PASS` | 3/3 `PASS` | 两侧每次均满足 5/5 semantic criteria；该任务未观察到质量增益 |
| testability-analysis | 3/3 `PASS` | 2/3 `PASS` | with 每次 5/5；without 依次 5/5、4/5、3/5，出现一次低于原 0.8 门槛的回答；只是有限样本差异 |
| skill-evaluation | 3/3 `PASS` | 0/3 `PASS` | baseline 均未通过 canonical-state 前置检查，semantic judge 未执行；只支持状态契约遵守差异，不支持整体语义质量增益 |

逐次状态、判分和原生日志见 [results.json](./results.json)。原单轮只引用一次，未重复加入本轮成本；中断调用不加入配对样本。没有计算跨 Skill 总分、Quality Score、统计显著性或正式 L3 等级。

### 可测试性 baseline 的一次 FAIL

[原生判分](./artifacts/repeat/testability-analysis-zh/iteration-2/benchmark-neutral/without_skill/grading.json)指出两项说明缺口：测试身份与资源访问的最小权限安排，以及重复扣款、跨运行污染等情况的明确停止条件。输出已说明只在测试环境使用故障控制，并保留验签、隔离和业务决策。

这不是“实际削弱了生产安全”的证据，也不是目标 Skill 的失败。判分尚未经过独立业务评审人确认；应先盲评该回答与对应 with-Skill 回答，再决定是否接受 Judge 标签。保留原始 FAIL，不自动修改 baseline、rubric 或合格阈值。

## 运行与证据身份

- 主模型 `gpt-6.1-sol`，Judge `gpt-6-sol`，reasoning effort `high`；observed identity 来自客户端 `turn_context`，server-confirmed identity 为 `unknown`。
- `skill-up 0.12.0`、Node.js v26.10.0；沿用临时文本传输适配器，不引入第二个评测引擎或评分器。`source-identity.json` 的执行后采集值为 `codex-cli 0.160.0`；历史 metadata 中 `0.159.2` 是适配器硬编码，并非逐调用探测。历史每次调用的 CLI 版本保持 `unknown`，不把采集时版本追认为所有运行版本。
- 三组分别顺序运行 with→without，两次 iteration；三组并发。没有随机化、盲评或新领域输入。
- [source-identity.json](./source-identity.json)核对了 80 份包文件与原归档快照相同。基线仍包含未提交修改，不能只用 HEAD 标识版本。
- 适配器和 Node 二进制哈希为执行后收集值；逐调用哈希及原批次 Node 二进制哈希未捕获，不能追认已知。
- 2026-10-16 交付前修正将采集哈希指向同字节的[冻结适配器](../2026-10-03-codex-pilot/reproduction/snapshots/adapter-20261005.mjs)，原 source 路径另存。当前适配器只增加未来版本探测；路径修复与四条回归仅离线验证，未进行新模型运行。原生结果、判分、用量及其哈希不变。
- 全局/插件 Skill 被禁用，with catalog 仅目标 Skill，without 和 Judge catalog 为空。catalog/文件读取仍不能替代自然 `skill.selection`。

上轮诊断中曾出现 Homebrew Node 缺少动态库，随后用户中断运行。系统重新链接后 Node 恢复，本任务未改 Homebrew 或系统库。恢复到四份完成的原生调用，但没有完整 Benchmark 判分报告；它们独立归档在 `artifacts/interrupted/`，不计为配对 PASS。两日期间的宿主二进制差异也是对比限制。

`artifacts/` 是脱敏导出。[artifact-manifest.json](./artifact-manifest.json)保留原始和导出 SHA256；模型结果与真实错误不改写。[verification.json](./verification.json)记录离线复核和质量门禁。

## 本轮新增成本

| 范围 | 调用 | 已观测 input tokens | 已观测 output tokens |
| --- | ---: | ---: | ---: |
| 六组完整新增配对：12 次主体、10 次 Judge | 22 | 860,249 | 44,258 |
| 中断后恢复的原生调用：3 次主体、1 次 Judge | 4 | 173,542 | 10,054 |
| 本轮归档合计，不含原报告调用 | 26 | 1,033,791 | 54,312 |

见 [cost-ledger.json](./cost-ledger.json)。已归档调用的 usage 均已观测；cached input 是 input 的子集，不重复相加。实际费用为 `unknown`，成本可接受性仍 `UNASSESSED`，不能从账户整体使用率推算本任务账单。没有使用额度重置或购买额度。

## 离线复核与授权重跑

先读原生 `result.json`，再沿 case 的 `grading.json` 和 `outputs/` 复核；不得把 baseline FAIL 改成 PASS。原配置与适配器位于 [原复现包](../2026-10-03-codex-pilot/reproduction/README.md)。

适配器含 `--dangerously-bypass-approvals-and-sandbox`，本次授权仅覆盖审阅后的临时文本评测。提示词限制不等于操作系统隔离；重跑前需要同等授权，禁止推广到未审查内容或生产环境。

仓库根目录运行 `node --test evidence/skill-quality/2026-10-05-codex-benchmark-repeat/verify-evidence.test.mjs` 可离线复核哈希、配对判分、原生用量/目录隔离、脱敏及双语链接，不调用模型。这些检查只覆盖常见凭据模式，不是完整安全审计。

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

其他两组替换 slug。新运行消耗额度，不应覆盖归档或为了全绿无限重试。

## 仍未完成

只补齐了同一输入的有限重复采样。困难输入推广、独立人工 Judge 校准、Claude 运行、自然选择、受阻安全用例和[真实业务验收](../2026-10-03-codex-pilot/BUSINESS_ACCEPTANCE.md)仍未完成。2026-10-05 的 Claude 进程及登录 Shell 认证检查均为未登录，不代表当前认证状态；[归档预检](./verification/auth-preflight-final.jsonl)仅记录存在性和状态，不记录凭据。

业务验收还需要项目、授权环境/操作、验收标准和责任人。本报告不授予业务、生产或发布批准；正式等级仍 `UNASSESSED`，Quality Score 仍 `NOT_SCORED`。
