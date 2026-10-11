<div align="right"><strong>🇨🇳 中文</strong> | <a href="./SKILL_QUALITY_PILOT_EN.md">🇬🇧 English</a></div>

# Awesome QA Skills 的 SQEM Pilot 计划

> 版本：1.0<br>
> 目的：在全仓库推广前验证 SQEM 的可行性和实用性。

## 1. Pilot 目标

Pilot 用于判断 SQEM 是否：

- 容易理解；
- 可以实际执行；
- 成本可接受；
- 能发现真实 Skill 缺陷；
- 能够在 Awesome QA Skills 当前规模下长期维护。

Pilot 不假设 SQEM v1.0 已经正确。**SQEM 自己也是被测试对象。**

本文件列出的五个 Skill 是 SQEM 方法论 Pilot 候选，不替换仓库已有的 `requirements-analysis` 分析 Pilot、`ui-test-playwright` 可执行 Pilot 或 `discover-testing` Router Composition Pilot。现有 Pilot 的配置、证据状态和执行边界以[既有 Pilot 契约](../governance/SKILL_EVALUATION_PILOTS.md)为准；本文件只补充 SQEM 的质量域、风险和方法验证。

## 2. Pilot Skills

### P1 - functional-testing
类型：通用 QA Skill<br>
目标：L3 Evaluated<br>
重点：Trigger、Behavior、Benchmark、双语一致性。

### P2 - testability-analysis
类型：分析型 QA Skill<br>
目标：L3 Evaluated<br>
重点：Boundary、Contrastive Selection、Unsupported Assumptions、Evidence Handling。

### P3 - performance-testing
类型：专业领域 QA Skill<br>
目标：L2 Verified + 部分 L3<br>
重点：Behavior、领域正确性、Model Sensitivity。

### P4 - skill-evaluation-design
类型：Skill Engineering<br>
目标：L3 Evaluated<br>
重点：Behavior Contract、Eval Design、Judge Usage、Risk-based Selection。

### P5 - skill-change-verification
类型：Skill Engineering / Regression<br>
目标：L3 Evaluated<br>
重点：Change Impact、Regression Selection、Evidence Comparison、Failure Handling。

## 3. Pilot 阶段

### Stage 1 - Inventory

每个 Skill 收集：

```text
Canonical Name
Current Structure
English Variant
Chinese Variant
References
Scripts
Current Evals
Known Issues
Adjacent Skills
```

### Stage 2 - Risk Profile

评估：

```text
Reasoning Complexity
Trigger Ambiguity
Side Effects
Tool Dependency
Impact
Model Sensitivity
Failure Detectability
```

使用 LOW / MEDIUM / HIGH。

### Stage 3 - Q1-Q3 Validation

执行 Specification Validation、Design Review、Package Validation、Localization Consistency。

### Stage 4 - Behavior Contract

为每个 Pilot Skill 定义 MUST、SHOULD、MUST NOT。只约束真正定义能力的行为，避免过度规定输出格式。

### Stage 5 - Core Eval Suite

每个 Pilot 的建议起点：

```text
2-3 Positive
2 Negative
2 Boundary（适用时）
2 Behavior
已有 Regression Cases
```

这是指导值，不是所有 Skill 的强制配额。

### Stage 6 - Runtime Evaluation

至少选择一个真实支持的 Agent Runtime 执行代表性 Eval，并记录 Trigger、Output、必要的 Trajectory、Artifacts、Failures 和 Runtime Metadata。

如果真实 Agent、目标环境、跨模型矩阵或业务验收不可用，保持 `NOT_RUN`、`BLOCKED`、`NOT_SCORED` 或 `INSUFFICIENT_EVIDENCE`，不得用静态检查或 `skill-up validate` 替代运行时结论。

### Stage 7 - Benchmark

优先对：

```text
functional-testing
testability-analysis
skill-evaluation-design
```

执行受控的 Without Skill vs With Skill 对比。

### Stage 8 - Compatibility Sampling

不做所有组合的全量测试，采用代表性环境：

| Skill | Codex | Claude Code | 其他代表 Agent |
|---|---|---|---|
| functional-testing | Required | Recommended | Optional |
| testability-analysis | Required | Recommended | Optional |
| performance-testing | Required | Optional | Optional |
| skill-evaluation-design | Required | Recommended | Optional |
| skill-change-verification | Required | Recommended | Optional |

实际环境取决于可用 Runtime。

### Stage 9 - Bilingual Parity

验证中英文：

- Capability Parity；
- Trigger Parity；
- Behavior Parity；
- Boundary Parity；
- Output Language。

不默认复制完整 Eval Suite，优先使用代表性双语 Case。

## 4. Pilot 指标

### Quality Findings

记录：

- Specification Defects；
- Package Defects；
- Trigger Defects；
- Boundary Defects；
- Behavior Defects；
- Regression Defects；
- Compatibility Differences。

### Engineering Cost

记录：

- Eval 编写时间；
- Eval 维护时间；
- Runtime Cost；
- Token Cost；
- CI Duration；
- Failure Triage Time。

### Framework Usefulness

判断 SQEM 是否：

- 发现 Static Check 无法发现的问题；
- 改善 Skill 能力边界；
- 提高 Regression Confidence；
- 提供有价值的 Benchmark Evidence；
- 引入了过高的维护成本。

## 5. Pilot Exit Criteria

满足以下条件时，Pilot 可以认为达到了验证目的：

1. 五个 Pilot Skill 都能一致应用 SQEM。
2. Skill 作者能够理解七个 Quality Domains。
3. Core Eval Cases 的维护成本可接受。
4. Behavioral Evaluation 能发现 Static Check 无法提供的信息。
5. Benchmark 能产生可行动的证据。
6. Compatibility 可以通过 Sampling 控制成本。
7. 双语验证不要求完整重复维护。
8. Regression Case 能追溯到真实 Failure。
9. Runtime Cost 可以被测量。
10. 能在 SQEM v1.1 前识别并删除冗余复杂度。

## 6. 预期输出

```text
5 个 Skill Quality Profiles
5 个 Risk Profiles
5 个 Behavior Contracts
Core Eval Suites
Selected Benchmarks
Compatibility Evidence
Pilot Cost Report
SQEM v1.1 Change Proposal
```

## 7. Pilot 后决策

可能的结论：

```text
ADOPT
ADOPT_WITH_CHANGES
LIMITED_ADOPTION
REWORK
```
