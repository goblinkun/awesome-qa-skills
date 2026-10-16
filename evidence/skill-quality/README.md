<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# Skill Quality Evidence

本目录用于存放经过审阅或由 runner 生成的 Skill 质量证据说明和报告资产。每份报告的运行范围、模型、版本、未执行项和可支持声明必须单独明确，不能从一个 Pilot 推断全仓库通过。

## 已有报告

- [2026-10-05 Codex Benchmark 重复采样](./2026-10-05-codex-benchmark-repeat/README.md)：三个既有中文任务各补两轮；连同原单轮每侧三个样本，中断调用及成本独立保留；不代表业务验收或统计增益。
- [2026-10-03 Codex SQET Pilot](./2026-10-03-codex-pilot/README.md)：五个 Skill 的双语文本核心运行、三个选定单次 Benchmark、第二模型代表采样、成本和原生证据。自然触发、受阻安全边界、Claude 与业务验收仍按报告的未验证状态保留。

## 最低记录字段

可复核的证据至少应记录：

- Skill commit 或 version；
- Eval version 与 case id；
- engine、provider、requested/observed model；
- judge 类型与 judge model（如适用）；
- environment 与 timestamp；
- result、failure classification、trace/artifact 位置；
- limitations；
- 证据支持和不支持的质量声明。

未知值写 `unknown`，不得猜测；凭据、Cookie、Bearer token 和不必要的敏感内容不得写入证据。

## 证据状态与声明边界

证据报告应使用仓库已有的 `PASS`、`FAIL`、`BLOCKED`、`NOT_RUN`、`NOT_SCORED`、`UNASSESSED` 和 `INSUFFICIENT_EVIDENCE` 语义。没有真实 Agent、目标环境、跨模型或业务验收证据时，结果保持 `NOT_RUN`、`BLOCKED` 或 `INSUFFICIENT_EVIDENCE`；静态门禁和 `skill-up validate` 不能升级为运行时质量、兼容性、业务效果或 release approval 结论。

证据只能支持与其层级相称的质量声明，遵循：

```text
Quality Claim <= Available Evidence
```

方法论入口见 [SQET](../../docs/skill-quality-engineering/README.md)，状态与报告结构见 [Skill Evaluation Contract](../../docs/governance/SKILL_EVALUATION_CONTRACT.md)。
