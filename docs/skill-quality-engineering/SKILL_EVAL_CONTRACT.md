<div align="right"><strong>🇨🇳 中文</strong> | <a href="./SKILL_EVAL_CONTRACT_EN.md">🇬🇧 English</a></div>

# Skill Eval 契约

> 版本：1.0  
> 关联规范：Skill Quality Evaluation Model（SQEM）

## 1. 目的

Skill Eval Contract 用于定义一个 Agent Skill 应该如何被评测的可移植概念结构。

它不绑定具体 Runner，可以映射到 Skill-Up、OpenAI Eval 工作流、仓库脚本、自定义 Agent Harness 或 CI Pipeline。

## 仓库对齐边界

本契约在仓库内复用 [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT.md) 的 Evidence State、Failure Classification 和报告结构；Quality Score 继续由 [Quality Score 与最低 Eval 契约](../governance/QUALITY_SCORE_EVAL_CONTRACT.md) 负责。本契约不新增评分体系，也不替换现有 `skill-up` 评测引擎。

Router case 的 observed selection 必须由结构化的 `skill.selection` trace 或明确的 trace adapter 提供 `route`、`primary`、`optional` 和 `selected_skills`。`selected_skills` 必须严格等于唯一主 Skill 加至多一个辅助 Skill；缺少或非法字段为 `BLOCKED`，值不匹配或多选为 `FAIL`。普通文本推荐、Composition Recipe 或静态配置不能单独证明真实选择。

## 2. Eval Case 模型

一个 Skill Eval Case 建议包含：

```yaml
id: unique-case-id
skill: canonical-skill-name
type: positive

task:
  input: |
    User task goes here.

context:
  files: []
  environment: {}

expected:
  trigger: true

behavior:
  must: []
  should: []
  must_not: []

artifacts:
  required: []
  forbidden: []

side_effects:
  allowed: []
  forbidden: []

evaluation:
  methods: []

evidence:
  capture:
    - output
    - trajectory
    - artifacts
```

不是每个 Case 都必须填写全部字段。

## 3. Case 类型

```text
positive
negative
boundary
behavior
regression
paraphrase
adversarial
benchmark
compatibility
trajectory
side_effect
```

## 4. Positive Case

目的：验证代表性目标任务能够正确触发 Skill，并产生符合预期的行为。

```yaml
id: functional-testing-positive-001
skill: functional-testing
type: positive

task:
  input: |
    为一个电商结账流程设计功能测试。

expected:
  trigger: true

behavior:
  must:
    - identify_primary_business_flow
    - cover_positive_path
    - cover_negative_paths
    - identify_test_data

  must_not:
    - invent_missing_business_rules
```

## 5. Negative Case

目的：验证与 Skill 无关的任务不会误触发。

```yaml
id: functional-testing-negative-001
skill: functional-testing
type: negative

task:
  input: |
    修复这个 Playwright locator。

expected:
  trigger: false
```

## 6. Boundary Case

目的：验证相邻 Skill 之间的能力边界。

```yaml
id: functional-testing-boundary-001
skill: functional-testing
type: boundary

task:
  input: |
    在开始功能测试设计前，评审这个需求是否已经具备可测试条件。

expected:
  preferred_skill:
    - testability-analysis

  unexpected_skill:
    - functional-testing
```

## 7. Behavior Case

目的：验证可观察的 Skill 行为。

```yaml
id: requirement-quality-behavior-001
skill: requirement-quality-review
type: behavior

behavior:
  must:
    - identify_requirement_gaps
    - separate_fact_from_assumption
    - identify_missing_evidence

  should:
    - prioritize_findings

  must_not:
    - invent_business_rules
    - provide_unsupported_release_approval
```

## 8. Regression Case

每个 Regression Case 建议保留来源信息：

```yaml
id: functional-testing-regression-017
skill: functional-testing
type: regression

provenance:
  source: real_failure
  reference: issue-17
  first_observed_version: 1.5.2

failure:
  description: >
    当需求中的支付规则不完整时，Skill 漏掉了支付失败路径。

expected:
  behavior:
    must:
      - identify_missing_payment_rule
      - preserve_unknown_business_boundary
```

Regression Case 应解释它为什么存在。

## 9. Benchmark Case

Benchmark 用于比较受控配置：

```yaml
id: functional-testing-benchmark-001
skill: functional-testing
type: benchmark

variants:
  - without_skill
  - with_skill

controls:
  same_task: true
  same_model: true
  same_agent: true
  same_environment: true

metrics:
  - task_success
  - critical_coverage
  - unsupported_claims
  - tokens
  - latency
```

不要同时改变多个独立变量。

## 10. Compatibility Case

```yaml
id: functional-testing-compatibility-001
skill: functional-testing
type: compatibility

matrix:
  agents:
    - codex
    - claude-code

  models:
    - configured-model-a
    - configured-model-b

behavior:
  must:
    - preserve_core_behavior_contract
```

只报告真实执行过的环境。

## 11. Behavior Contract

使用 MUST、SHOULD、MUST NOT，并聚焦可观察行为。

不推荐：

```yaml
must:
  - provide_a_good_answer
```

推荐：

```yaml
must:
  - identify_missing_acceptance_criteria
  - distinguish_fact_from_assumption
```

## 12. Evaluation Methods

### Deterministic
文件存在、Exit Code、Schema Valid、必需字段、禁止文件不存在等。

### Rule-based
必需章节、已知风险类别、禁止模式等。

### Script / Domain Evaluator
用于领域特定的程序化判断。

### Agent Judge
需要语义判断时使用，Judge Criteria 必须明确。

不推荐：`这个回答好吗？`

推荐：`输出是否区分了文档中的事实和模型自行引入的假设？`

### Human Review
适用于歧义 Case、高影响评测、Judge Calibration 和真实项目有效性复核。

## 13. Evidence Capture

可记录：

```text
Input
Skill Version
Agent
Model
Environment
Output
Trajectory
Tool Calls
Artifacts
Token Usage
Latency
Judge Result
Failure Reason
```

只保留对复现和诊断有价值的证据。

## 14. Repeated Runs

非确定性行为可以多次执行，例如：

```yaml
runs:
  count: 3
```

重要 Case 可以增加样本。一次运行不能证明稳定性。

## 15. Eval Result

推荐概念结构：

```yaml
result:
  status: PASS
  evidence_level: E2

  checks:
    trigger: PASS
    behavior: PASS
    artifacts: PASS

  observations: []
  limitations: []
```

允许状态：

```text
PASS
FAIL
NOT_RUN
BLOCKED
NOT_SCORED
UNASSESSED
INSUFFICIENT_EVIDENCE
```

`NOT_SCORED` 仅表示没有合法 Quality Score，`UNASSESSED` 表示当前范围未评估该维度，`INSUFFICIENT_EVIDENCE` 表示已有痕迹但不足以支持强结论；它们都不是通过状态。

## 16. Eval Quality

重要 Eval Case 也需要复核：

- Realism；
- Coverage；
- Discriminative Power；
- Repeatability；
- Independence；
- Judge Reliability。

如果 Eval 无法区分 Baseline 和真正有价值的 Skill，它本身可能需要改进。

## 17. Contract Portability

Contract 定义的是语义意图：

```text
Skill Eval Contract
       |
       +-- Skill-Up Adapter
       +-- OpenAI Eval Adapter
       +-- Custom Harness Adapter
       +-- CI Adapter
```

这样可以避免质量模型被单一 Eval Framework 锁定。
