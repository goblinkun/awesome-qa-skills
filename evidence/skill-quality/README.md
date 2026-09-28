<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# Skill Quality Evidence

本目录用于存放经过审阅或由 runner 生成的 Skill 质量证据说明和报告资产。本阶段只建立目录边界，不创建任何 Evidence Report 实例，也不声称已有 runtime 结果。

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
