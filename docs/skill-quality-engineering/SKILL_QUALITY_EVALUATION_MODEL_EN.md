<div align="right"><a href="./SKILL_QUALITY_EVALUATION_MODEL.md">🇨🇳 中文</a> | <strong>🇬🇧 English</strong></div>

# Skill Quality Evaluation Model (SQEM)

> Version: 1.0  
> Status: Draft for Pilot Validation  
> Scope: Agent Skills / Awesome QA Skills

## 1. Purpose

The Skill Quality Evaluation Model (SQEM) is a risk-driven and evidence-driven quality framework for evaluating Agent Skills.

It answers seven questions:

1. Is this a valid Skill?
2. Is the Skill well designed and sufficiently differentiated?
3. Is the Skill package complete, consistent, and independently usable?
4. Can an agent discover, select, and execute the Skill correctly?
5. Does the Skill improve task outcomes compared with an appropriate baseline?
6. Does the Skill work in the environments for which compatibility is claimed?
7. What evidence supports each quality claim?

SQEM evaluates a Skill as an operational capability rather than only as a prompt artifact.

A useful mental model is:

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

Therefore:

```text
Valid SKILL.md != Reliable Skill
One Eval PASS != Skill Quality PASS
```

## 2. Scope and Non-goals

SQEM is not:

- a replacement for the Agent Skills Specification;
- a replacement for an Eval runner such as Skill-Up;
- a universal benchmark;
- a requirement to test every Skill across every model and agent;
- a single 0-100 quality score.

SQEM defines what to evaluate, how deeply to evaluate it, what evidence to retain, and what claims that evidence can support.

## 3. Core Principles

### P1 - Evidence over intuition
Prefer observable and repeatable evidence over impressions from one successful run.

### P2 - Behavior over wording
Evaluate observable behavior instead of requiring exact generated text.

### P3 - Risk-based over exhaustive
Do not execute the full Cartesian product of Skill x language x agent x model x environment x case. Select depth according to risk and claims.

### P4 - Deterministic before probabilistic
Use the cheapest reliable evaluator:

```text
Deterministic assertion
-> Rule-based check
-> Script/domain evaluator
-> Agent/LLM Judge
-> Human review
```

### P5 - Regression from real failures
Meaningful failures should become regression candidates.

### P6 - Baseline before effectiveness claims
A successful execution does not prove that the Skill adds value. Compare with an appropriate baseline when claiming effectiveness.

### P7 - Compatibility must be demonstrated
Specification conformance does not prove runtime compatibility.

### P8 - Claims must not exceed evidence

```text
Quality Claim <= Available Evidence
```

This is the central SQEM rule.

### Repository alignment

In this repository, SQEM is the methodology layer. It reuses the [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT_EN.md) for evidence states, failure classification, and structured Router-selection evidence; the [Quality Score and minimum Eval contract](../governance/QUALITY_SCORE_EVAL_CONTRACT_EN.md) for score ownership; and the [Skill Evaluation Quality Loop](../governance/SKILL_EVALUATION_DESIGN_EN.md) for the single `skill-up` evaluation-engine boundary. It does not introduce a second repository-wide Eval Engine, Judge, Benchmark, or Quality Score.

## 4. Seven Quality Domains

### Q1 - Specification Quality

Question: Is this a structurally valid Agent Skill?

Typical checks:

- `SKILL.md` exists;
- frontmatter is valid;
- canonical `name` and `description` are valid;
- directory and Skill identity are consistent;
- referenced resources exist;
- metadata and repository conventions are valid.

Primary evidence: lint, schema validation, static validation, repository tests.

Important:

```text
Specification PASS != Behavior PASS
```

### Q2 - Design Quality

Question: Should this Skill exist, and is its capability boundary clear?

Define:

- purpose;
- capability;
- inputs and outputs;
- preconditions;
- scope and non-goals;
- constraints;
- failure boundaries;
- evidence expectations;
- adjacent Skills;
- differentiation.

Before adding a new Skill, perform a Match Review:

```text
MATCH
MERGE
ENHANCE
NEW
```

Governance principle: match before enhance; merge before create.

### Q3 - Package Quality

Question: Is the Skill package complete, consistent, and independently usable?

Potential assets:

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

Not every Skill requires every asset.

Key properties:

- integrity;
- independence;
- progressive disclosure;
- dependency clarity;
- localization parity.

Localized variants should represent the same logical capability, not necessarily literal translations.

### Q4 - Behavioral Quality

Question: Can an agent use the Skill correctly?

Behavioral lifecycle:

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

Evaluate where relevant:

- discovery;
- trigger;
- selection;
- instruction adherence;
- workflow adherence;
- constraint adherence;
- output behavior;
- failure handling.

#### Trigger Testing

Core cases:

- Positive: should trigger.
- Negative: should not trigger.
- Boundary: close to an adjacent Skill.

Extended cases:

- paraphrase;
- adversarial;
- ambiguous request.

Possible metrics, when the dataset supports them:

- Trigger Precision;
- Trigger Recall;
- False Activation Rate;
- Missed Activation Rate.

#### Contrastive Skill Evaluation

Related Skills should be evaluated together where routing ambiguity exists.

Example:

```text
requirements-analysis
requirement-quality-review
testability-analysis
```

Evaluate whether representative and boundary tasks route to the intended capability.

#### Behavior Contract

Define observable expectations:

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

Evaluate behavior against the contract rather than exact wording.

#### Outcome and Trajectory

For many Skills, outcome evaluation is sufficient.

When execution process affects correctness or safety, also evaluate trajectory, such as:

- tool use;
- reference use;
- file operations;
- commands;
- retries;
- generated artifacts.

#### Side Effects

State-changing Skills should define expected, allowed, and forbidden side effects.

### Q5 - Effectiveness Quality

Question: Does the Skill provide meaningful incremental value?

Where an effectiveness claim is made, compare:

```text
Same Task
Same Model
Same Agent
Same Environment

Without Skill
vs
With Skill
```

Potential metrics:

- task success;
- critical behavior coverage;
- finding recall;
- error rate;
- unsupported claim rate;
- completeness;
- token usage;
- latency;
- tool calls.

Conceptually:

```text
Skill Uplift =
Outcome(with_skill) - Outcome(without_skill)
```

Do not force all metrics into one score. Report quality/cost trade-offs and negative or neutral uplift as well as improvements.

### Q6 - Compatibility Quality

Question: Where has the Skill actually been demonstrated to work?

Dimensions may include:

- Agent Host;
- Model;
- Tools;
- Environment;
- Language.

Principle:

```text
Specification compatibility != Runtime compatibility
```

Do not infer untested compatibility. Use representative, risk-based sampling instead of exhaustive matrices.

### Q7 - Evidence & Evolution Quality

Question: How does evidence remain traceable as the Skill changes?

A more accurate representation is:

```text
Skill Quality at Version V under Evidence Set E
```

Quality loop:

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
-> next iteration
```

Failure-to-regression workflow:

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

### L1 - Valid

Includes specification, static validation, and package validation.

Answers: Is this a structurally valid and internally healthy Skill?

Expected for all maintained Skills.

### L2 - Verified

Adds:

- Positive Eval;
- Negative Eval;
- Boundary Eval where applicable;
- Behavior Contract;
- basic regression.

Answers: Have the Skill's critical behaviors been verified?

Recommended minimum target for production-quality Awesome QA Skills.

### L3 - Evaluated

Adds selected:

- broader Eval suite;
- Agent/LLM Judge;
- repeated runs;
- benchmark;
- regression suite;
- runtime validation;
- compatibility sampling.

Answers: Is the Skill sufficiently stable, and does evidence support its expected value?

### L4 - Proven

Adds evidence such as:

- multiple runtime environments;
- cross-model or cross-agent evidence;
- real-project evidence;
- historical regression evidence;
- longitudinal evidence.

L4 means evidence maturity, not perfection.

## 6. Evidence Levels

Test Level describes validation depth. Evidence Level describes the strongest available evidence source.

### E1 - Static
Lint, schema, structure, metadata, reference validation.

### E2 - Eval
Deterministic assertions, behavior Eval, Judge, regression.

### E3 - Runtime
Real Agent harness, benchmark, cross-model, cross-agent.

### E4 - Real-world
Real project usage, observed failures, user feedback, longitudinal evidence.

## 7. Risk Profile

Assess:

| Dimension | Low | Medium | High |
|---|---|---|---|
| Reasoning complexity | Simple | Multi-step | Complex judgment |
| Trigger ambiguity | Unique | Some overlap | Strong overlap |
| Side effects | None | Creates artifacts | Modifies state |
| Tool dependency | None | One tool | Multiple tools |
| Impact | Low | Medium | High |
| Model sensitivity | Low | Unknown | Known sensitivity |
| Failure detectability | Obvious | Moderate | Hidden |

The risk profile determines required Eval types, target Test Level, compatibility scope, and runtime depth.

## 8. Eval Types

Core:

```text
Positive
Negative
Boundary
Behavior
Regression
```

Extended:

```text
Paraphrase
Adversarial
Benchmark
Compatibility
Trajectory
Side-effect
```

Selection:

| Eval | Use |
|---|---|
| Positive | Always |
| Negative | Always |
| Boundary | Adjacent capability exists |
| Behavior | Always |
| Regression | Known failure exists |
| Paraphrase | Trigger sensitivity matters |
| Adversarial | High-risk behavior |
| Benchmark | Effectiveness claim |
| Compatibility | Compatibility claim |
| Trajectory | Process matters |
| Side-effect | State can change |

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

Lower levels are generally faster, cheaper, more deterministic, and CI-friendly. Higher levels are generally more realistic but more expensive and variable.

Higher is not automatically better. Select appropriate depth based on risk and claims.

## 10. Evaluation Methods

Use the lowest-cost evaluator that can reliably verify the requirement:

1. Deterministic assertion
2. Rule-based evaluator
3. Script/domain evaluator
4. Agent/LLM Judge
5. Human review

Examples:

```text
File exists? -> Deterministic
JSON valid? -> Script
Required risk categories identified? -> Rule/Judge
Recommendation useful in project context? -> Judge/Human
```

## 11. Repeated Evaluation

LLM behavior is non-deterministic. For important L3/L4 behavior, consider repeated runs and report appropriate statistics such as:

- n;
- pass rate;
- pass@k;
- mean/median;
- variance;
- confidence interval.

Do not report statistical precision unsupported by the sample size.

## 12. Eval Quality

Important Evals should themselves be reviewed for:

- coverage;
- realism;
- discriminative power;
- repeatability;
- independence;
- bias;
- Judge reliability;
- overfitting.

If baseline and Skill both score 100%, the Skill may provide no uplift or the Eval may be too easy.

## 13. Status Model

Use:

```text
PASS
FAIL
NOT_RUN
BLOCKED
NOT_SCORED
UNASSESSED
INSUFFICIENT_EVIDENCE
```

This repository does not treat `PARTIAL` as a separate canonical Evidence State: use `INSUFFICIENT_EVIDENCE` when some execution or review trace exists but only a limited claim is supported; use `UNASSESSED` for a dimension not evaluated in the current scope; and use `NOT_SCORED` when there is no valid Quality Score. Do not convert "no observed failure" into PASS without sufficient evidence.

## 14. Quality Profile

SQEM does not require an overall numeric quality score.

Recommended format:

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
- Benchmark not executed
- Cross-model evidence incomplete
- Real-project evidence limited

`INSUFFICIENT_EVIDENCE` means that some execution or review trace exists but is not sufficient for a complete compatibility claim; it is not a passing state.

Next Validation:
- Run with/without Skill benchmark
- Add selected runtime compatibility
```

## 15. Quality Gates

### Merge Gate

Recommended:

```text
Specification PASS
Static PASS
Required Eval PASS
No unexplained regression
```

### Release Gate

Recommended:

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

Claims require matching evidence:

```text
"Supports Codex"
-> Codex runtime evidence

"Improves test design quality"
-> comparative benchmark evidence

"Works across models"
-> cross-model evidence

"Production proven"
-> real-world evidence
```

## 16. CI and Change-based Validation

Pull Request:

- static validation;
- critical Eval;
- changed-Skill Eval;
- regression smoke.

Release:

- full relevant Eval;
- regression suite;
- selected benchmark;
- selected compatibility;
- evidence report.

Scheduled:

- cross-model;
- cross-agent;
- extended benchmark;
- longitudinal regression.

Change-based examples:

```text
Change: description
Potential impact: Discovery / Trigger / Selection
Required: Trigger suite / Boundary suite
```

```text
Change: workflow instructions
Potential impact: Behavior / Output / Trajectory
Required: Behavior Eval / Regression / selected runtime
```

## 17. Anti-patterns

Avoid:

1. Static PASS means Skill PASS.
2. One successful manual run as broad evidence.
3. Exact text as the primary oracle.
4. LLM Judge for everything.
5. Full cross-product testing.
6. Compatibility by assumption.
7. Reporting only benchmark wins.
8. Fixing failures without regression cases.
9. Quality scores without supporting evidence.
10. Treating the Eval suite as unquestionable.

## 18. Awesome QA Skills Adoption

Validate SQEM through representative Pilot Skills before repository-wide deep adoption:

```text
functional-testing
testability-analysis
performance-testing
skill-evaluation-design
skill-change-verification
```

The Pilot should measure both Skill quality and SQEM practicality. Pilot results should feed into SQEM v1.1.

These five candidates are SQEM methodology Pilots. They do not replace the repository's existing `requirements-analysis`, `ui-test-playwright`, and `discover-testing` Pilot records; their execution status remains governed by the [existing Pilot contract](../governance/SKILL_EVALUATION_PILOTS_EN.md).

## 19. Reference Families

SQEM is informed by:

- Agent Skills Specification;
- OpenAI - Testing Agent Skills Systematically with Evals;
- Alibaba Skill-Up;
- Vercel skills and skills.sh;
- Codex Skills;
- Claude Code Skills;
- GitHub Copilot Agent Skills;
- Gemini CLI Skills;
- Cursor, Cline, and other compatible Agent Skill implementations.

These sources inform individual parts of the framework. SQEM combines specification, evaluation, runtime, compatibility, regression, and evidence into one quality-engineering model.
