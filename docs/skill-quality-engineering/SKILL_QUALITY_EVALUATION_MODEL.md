<div align="right"><strong>🇨🇳 中文</strong> | <a href="./SKILL_QUALITY_EVALUATION_MODEL_EN.md">🇬🇧 English</a></div>

# Skill 质量评测模型（SQEM）

> 版本：1.0<br>
> 状态：Pilot 验证草案<br>
> 适用范围：Agent Skills / Awesome QA Skills

## 1. 目的

Skill Quality Evaluation Model（SQEM）是一套面向 Agent Skills 的**风险驱动、证据驱动**质量评测模型。

它主要回答七个问题：

1. 这是一个规范有效的 Skill 吗？
2. Skill 的设计是否合理，能力边界是否足够清晰？
3. Skill 包是否完整、一致，并能够独立使用？
4. Agent 能否正确发现、选择并执行这个 Skill？
5. 与合理 Baseline 相比，使用 Skill 是否真正改善任务结果？
6. Skill 是否真的能在其声明兼容的 Agent、模型和环境中工作？
7. 当前有哪些证据能够支持这些质量结论？

SQEM 不把 Skill 只看成一份 Prompt，而是把它看成一个运行中的能力单元。

可以用下面的模型理解：

```text
Skill Outcome =
f(
  Skill Package,
  User Task,
  Agent Host,
  Model,
  Tools,
  Environment,
  Context,
  Runtime State
)
```

因此：

```text
SKILL.md 合法 != Skill 可靠
一次 Eval PASS != Skill Quality PASS
```

## 2. 范围与非目标

SQEM 不是：

- Agent Skills Specification 的替代品；
- Skill-Up 等 Eval Runner 的替代品；
- 一个统一 Benchmark；
- 要求所有 Skill 在所有 Agent 和模型上做全量测试的标准；
- 一个 0-100 的单一质量分数。

SQEM 主要定义：**应该评估什么、评估到什么深度、保留什么证据，以及这些证据能够支持什么质量声明。**

## 3. 核心原则

### P1 - Evidence over intuition｜证据优先于感觉
不能因为一次人工运行“看起来不错”，就认为 Skill 已经可靠。优先使用可观察、可重复的证据。

### P2 - Behavior over wording｜行为优先于措辞
验证可观察行为，而不是要求模型输出固定文字。

### P3 - Risk-based over exhaustive｜风险驱动优先于穷举
不要执行 Skill × Language × Agent × Model × Environment × Case 的全排列。测试深度应由风险和质量声明决定。

### P4 - Deterministic before probabilistic｜确定性优先于概率性
使用能够可靠判断结果的最低成本评估方式：

```text
Deterministic assertion
-> Rule-based check
-> Script/domain evaluator
-> Agent/LLM Judge
-> Human review
```

### P5 - Regression from real failures｜真实失败沉淀为回归
有价值的真实 Skill Failure 应成为 Regression Case 候选。

### P6 - Baseline before effectiveness claims｜宣称有效前先有 Baseline
Skill 能成功执行，不代表它真正带来了增量价值。

### P7 - Compatibility must be demonstrated｜兼容性必须验证
符合 Specification 不代表真实 Runtime 一定兼容。

### P8 - Claims must not exceed evidence｜质量声明不能超过证据边界

```text
Quality Claim <= Available Evidence
```

这是 SQEM 最核心的规则。

### 仓库对齐

在本仓库，SQEM 是方法论层：它复用 [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT.md) 的证据状态、失败分类和 Router 选择证据，复用 [Quality Score 与最低 Eval 契约](../governance/QUALITY_SCORE_EVAL_CONTRACT.md) 的评分责任，并遵循 [Skill Evaluation Quality Loop](../governance/SKILL_EVALUATION_DESIGN.md) 的单一 `skill-up` 评测引擎边界。它不新增全局 Eval Engine、Judge、Benchmark 或 Quality Score。

## 4. 七个质量域

### Q1 - Specification Quality｜规范质量

核心问题：它是不是一个结构合法的 Agent Skill？

典型检查：

- `SKILL.md` 是否存在；
- Frontmatter 是否合法；
- Canonical `name` / `description` 是否有效；
- 目录和 Skill 身份是否一致；
- 引用资源是否存在；
- metadata 和仓库约定是否有效。

主要证据：Lint、Schema、静态验证、Repository Tests。

必须明确：

```text
Specification PASS != Behavior PASS
```

### Q2 - Design Quality｜设计质量

核心问题：这个 Skill 是否应该存在，它的能力边界是否清晰？

需要定义：

- Purpose；
- Capability；
- Inputs / Outputs；
- Preconditions；
- Scope / Non-goals；
- Constraints；
- Failure Boundaries；
- Evidence Expectations；
- Adjacent Skills；
- Differentiation。

新增 Skill 前执行 Match Review：

```text
MATCH
MERGE
ENHANCE
NEW
```

治理原则：

> 先匹配，后增强；先合并，后新增。

### Q3 - Package Quality｜Skill 包质量

核心问题：Skill 包是否完整、一致并可以独立使用？

可能包含：

```text
SKILL.md
references/
scripts/
assets/
examples/
templates/
evals/
metadata
```

不是每个 Skill 都必须包含全部资产。

重点关注：

- Integrity；
- Independence；
- Progressive Disclosure；
- Dependency Clarity；
- Localization Parity。

中英文版本应该表示同一个逻辑 Skill，重点保持能力、边界、行为和 Eval 意图一致，而不是逐字翻译。

### Q4 - Behavioral Quality｜行为质量

核心问题：Agent 能不能正确使用 Skill？

典型行为链：

```text
Available
-> Discovered
-> Matched
-> Triggered
-> Loaded
-> Followed
-> Executed
-> Output Produced
```

根据需要评估：

- Discovery；
- Trigger；
- Selection；
- Instruction Adherence；
- Workflow Adherence；
- Constraint Adherence；
- Output Behavior；
- Failure Handling。

#### Trigger Testing

核心 Case：

- Positive：应该触发；
- Negative：不应该触发；
- Boundary：与相邻 Skill 接近，用于验证能力边界。

扩展 Case：

- Paraphrase；
- Adversarial；
- Ambiguous Request。

数据量足够时可以计算：

- Trigger Precision；
- Trigger Recall；
- False Activation Rate；
- Missed Activation Rate。

#### Contrastive Skill Evaluation

存在路由歧义的相邻 Skill 应一起测试。

例如：

```text
requirements-analysis
requirement-quality-review
testability-analysis
```

不仅要分别测试，还要验证代表任务和边界任务能否路由到预期能力。

#### Behavior Contract

Skill 应定义可观察的行为契约：

```yaml
behavior:
  must:
    - identify_requirement_gaps
    - distinguish_fact_from_assumption
    - identify_missing_evidence

  should:
    - prioritize_high_risk_gaps

  must_not:
    - invent_business_rules
    - make_unsupported_claims
    - give_release_approval
```

Eval 应验证 Behavior Contract，而不是文字相似度。

#### Outcome 与 Trajectory

很多 Skill 只需要 Outcome Evaluation。

如果执行过程本身会影响正确性或安全性，再增加 Trajectory Evaluation，例如：

- Tool Usage；
- Reference Usage；
- File Operations；
- Commands；
- Retries；
- Generated Artifacts。

#### Side Effects

能够修改状态的 Skill 应定义：

```text
Expected Side Effects
Allowed Side Effects
Forbidden Side Effects
```

### Q5 - Effectiveness Quality｜有效性质量

核心问题：Skill 是否真的提供了增量价值？

如果要宣称 Skill 有效，应尽可能进行：

```text
Same Task
Same Model
Same Agent
Same Environment

Without Skill
vs
With Skill
```

可比较：

- Task Success；
- Critical Behavior Coverage；
- Finding Recall；
- Error Rate；
- Unsupported Claim Rate；
- Completeness；
- Token Usage；
- Latency；
- Tool Calls。

概念上：

```text
Skill Uplift =
Outcome(with_skill) - Outcome(without_skill)
```

不要强行压缩成单一分数。应该同时报告质量提升、成本增加、无明显变化和负向结果。

### Q6 - Compatibility Quality｜兼容性质量

核心问题：Skill 已经在哪些环境中被真实证明可以工作？

可能包括：

- Agent Host；
- Model；
- Tools；
- Environment；
- Language。

原则：

```text
Specification Compatibility != Runtime Compatibility
```

不要推断未测试的兼容性。采用代表性、风险驱动的抽样，而不是全排列。

### Q7 - Evidence & Evolution Quality｜证据与演进质量

核心问题：Skill 持续变化后，质量证据是否仍然可追溯？

更准确的表达是：

```text
Skill Quality at Version V under Evidence Set E
```

质量循环：

```text
Design
-> Implement
-> Validate
-> Evaluate
-> Release
-> Observe
-> Failure
-> Regression
-> Improve
-> 下一轮
```

Failure-to-Regression：

```text
Observed Failure
-> Capture Evidence
-> Reproduce
-> Classify
-> Root Cause
-> Fix
-> Regression Case
-> Existing Suite
-> Release Evidence
```

## 5. Skill Test Levels

### L1 - Valid｜有效

包括：

- Specification；
- Static Validation；
- Package Validation。

回答：这是一个结构合法、工程上健康的 Skill 吗？

所有维护中的 Skill 都应该达到。

### L2 - Verified｜已验证

增加：

- Positive Eval；
- Negative Eval；
- 必要时 Boundary Eval；
- Behavior Contract；
- Basic Regression。

回答：Skill 的关键行为是否已经被验证？

建议作为 Awesome QA Skills 正式 Skill 的最低目标。

### L3 - Evaluated｜已评测

根据风险增加：

- 更完整的 Eval Suite；
- Agent/LLM Judge；
- Repeated Runs；
- Benchmark；
- Regression Suite；
- Runtime Validation；
- Compatibility Sampling。

回答：Skill 是否足够稳定，并且现有证据是否能够支持其预期价值？

### L4 - Proven｜已有较强实践证据

进一步增加：

- 多 Runtime Environment；
- Cross-model / Cross-agent Evidence；
- Real-project Evidence；
- Historical Regression Evidence；
- Longitudinal Evidence。

L4 表示证据成熟度更高，不表示 Skill 完美。

## 6. Evidence Levels

Test Level 表示测试深度；Evidence Level 表示当前最强证据来源。

### E1 - Static
Lint、Schema、Structure、Metadata、Reference Validation。

### E2 - Eval
Deterministic Assertions、Behavior Eval、Judge、Regression。

### E3 - Runtime
Real Agent Harness、Benchmark、Cross-model、Cross-agent。

### E4 - Real-world
真实项目使用、真实失败、用户反馈、长期证据。

## 7. Risk Profile

评估：

| 维度 | Low | Medium | High |
|---|---|---|---|
| Reasoning Complexity | 简单 | 多步骤 | 复杂判断 |
| Trigger Ambiguity | 独特 | 部分重叠 | 高度重叠 |
| Side Effects | 无 | 创建产物 | 修改状态 |
| Tool Dependency | 无 | 单工具 | 多工具 |
| Impact | 低 | 中 | 高 |
| Model Sensitivity | 低 | 未知 | 已知敏感 |
| Failure Detectability | 明显 | 一般 | 隐蔽 |

Risk Profile 用于决定 Required Eval Types、Target Test Level、Compatibility Scope 和 Runtime Depth。

## 8. Eval 类型

核心：

```text
Positive
Negative
Boundary
Behavior
Regression
```

扩展：

```text
Paraphrase
Adversarial
Benchmark
Compatibility
Trajectory
Side-effect
```

选择规则：

| Eval | 使用条件 |
|---|---|
| Positive | 总是需要 |
| Negative | 总是需要 |
| Boundary | 存在相邻能力 |
| Behavior | 总是需要 |
| Regression | 存在已知 Failure |
| Paraphrase | Trigger 对表达敏感 |
| Adversarial | 高风险行为 |
| Benchmark | 要宣称 Effectiveness |
| Compatibility | 要宣称兼容性 |
| Trajectory | 过程影响正确性 |
| Side-effect | Skill 会修改状态 |

## 9. Evaluation Pyramid

```text
                 Real-world
                     ^
              Compatibility
                     ^
                 Benchmark
                     ^
              Agent Runtime
                     ^
             Behavioral Eval
                     ^
          Deterministic Checks
                     ^
             Static Validation
```

越往下通常越快、越便宜、越确定、越适合 CI；越往上通常越真实，但成本和波动性更高。

Higher 不等于 Always Better。测试深度应与风险和质量声明匹配。

## 10. Evaluation Methods

优先使用能够可靠判断结果的最低成本方法：

1. Deterministic Assertion
2. Rule-based Evaluator
3. Script / Domain Evaluator
4. Agent / LLM Judge
5. Human Review

例如：

```text
文件是否存在？ -> Deterministic
JSON 是否合法？ -> Script
是否覆盖必要风险类别？ -> Rule/Judge
建议是否真正有项目价值？ -> Judge/Human
```

## 11. Repeated Evaluation

LLM 输出具有非确定性。对于重要的 L3/L4 行为，可以执行多次并记录：

- n；
- Pass Rate；
- pass@k；
- Mean / Median；
- Variance；
- Confidence Interval。

样本不足时不要制造虚假的统计精度。

## 12. Eval Quality

重要 Eval 本身也需要评估：

- Coverage；
- Realism；
- Discriminative Power；
- Repeatability；
- Independence；
- Bias；
- Judge Reliability；
- Overfitting。

如果 Baseline 和 Skill 都是 100%，可能说明 Skill 没有 Uplift，也可能说明 Eval 太简单。

## 13. 状态模型

使用：

```text
PASS
FAIL
NOT_RUN
BLOCKED
NOT_SCORED
UNASSESSED
INSUFFICIENT_EVIDENCE
```

本仓库不把 `PARTIAL` 作为独立的 canonical Evidence State：已执行但只能支持限制性结论时使用 `INSUFFICIENT_EVIDENCE`；尚未评估的维度使用 `UNASSESSED`；没有合法 Quality Score 时使用 `NOT_SCORED`。没有观察到失败，不等于已经 PASS。

## 14. Quality Profile

SQEM 不要求一个总质量分数。

推荐：

```text
Skill Quality Profile
────────────────────────────────────

Skill:
functional-testing

Version:
x.y.z

Target Test Level:
L3 Evaluated

Current Test Level:
L2 Verified

Q1 Specification       PASS
Q2 Design              PASS
Q3 Package             PASS
Q4 Behavior            PASS
Q5 Effectiveness       NOT_RUN
Q6 Compatibility       INSUFFICIENT_EVIDENCE
Q7 Evidence/Evolution  PASS

Evidence Level:
E2 Eval

Known Gaps:
- 尚未执行 Benchmark
- Cross-model 证据不完整
- Real-project Evidence 有限

`INSUFFICIENT_EVIDENCE` 表示已有部分运行或审阅痕迹，但不足以支持完整兼容性声明；它不是通过状态。

Next Validation:
- 执行 with/without Skill Benchmark
- 增加代表性 Runtime Compatibility
```

## 15. Quality Gates

### Merge Gate

```text
Specification PASS
Static PASS
Required Eval PASS
No unexplained regression
```

### Release Gate

```text
Merge Gate
+
Critical Regression PASS
+
Evidence updated
+
Known gaps declared
```

### Quality Claim Gate

质量声明必须有对应证据：

```text
"Supports Codex"
-> Codex Runtime Evidence

"Improves test design quality"
-> Comparative Benchmark Evidence

"Works across models"
-> Cross-model Evidence

"Production proven"
-> Real-world Evidence
```

## 16. CI 与 Change-based Validation

Pull Request：

- Static Validation；
- Critical Eval；
- Changed-Skill Eval；
- Regression Smoke。

Release：

- Full Relevant Eval；
- Regression Suite；
- Selected Benchmark；
- Selected Compatibility；
- Evidence Report。

Scheduled：

- Cross-model；
- Cross-agent；
- Extended Benchmark；
- Longitudinal Regression。

Change-based 示例：

```text
Change: description
Potential Impact: Discovery / Trigger / Selection
Required: Trigger Suite / Boundary Suite
```

```text
Change: workflow instructions
Potential Impact: Behavior / Output / Trajectory
Required: Behavior Eval / Regression / Selected Runtime
```

## 17. Anti-patterns

避免：

1. Static PASS 就认为 Skill PASS。
2. 用一次成功的人工运行支持广泛质量结论。
3. 把 Exact Text 当成主要 Oracle。
4. 所有检查都使用 LLM Judge。
5. 做完整 Cross-product Testing。
6. 没有 Runtime Evidence 就宣称兼容。
7. Benchmark 只展示 Skill 赢的 Case。
8. 修复 Failure 后不补 Regression。
9. 没有证据支撑却给出精确 Quality Score。
10. 默认 Eval Suite 本身一定正确。

## 18. Awesome QA Skills 落地

在全仓库深度推广前，先通过代表性 Pilot Skills 验证 SQEM：

```text
functional-testing
testability-analysis
performance-testing
skill-evaluation-design
skill-change-verification
```

Pilot 不仅测试 Skill，也测试 SQEM 本身是否实用、成本是否可接受。Pilot 结果进入 SQEM v1.1。

这些五个候选是 SQEM 方法论 Pilot，不替换仓库已有的 `requirements-analysis`、`ui-test-playwright` 和 `discover-testing` Pilot 记录；它们的运行状态仍须服从 [既有 Pilot 契约](../governance/SKILL_EVALUATION_PILOTS.md)。

## 19. 参考体系

SQEM 主要参考：

- Agent Skills Specification；
- OpenAI - Testing Agent Skills Systematically with Evals；
- Alibaba Skill-Up；
- Vercel skills / skills.sh；
- Codex Skills；
- Claude Code Skills；
- GitHub Copilot Agent Skills；
- Gemini CLI Skills；
- Cursor、Cline 等 Agent Skills 实现。

这些资料分别提供 Specification、Eval、Distribution、Runtime 等方面的实践。SQEM 在此基础上进一步把规范、行为、有效性、兼容性、回归和证据统一成一个 Skill Quality Engineering 模型。
