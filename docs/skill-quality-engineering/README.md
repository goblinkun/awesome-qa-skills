<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# Skill Quality Engineering Toolkit（SQET）

> 版本：1.0  
> 核心模型：Skill Quality Evaluation Model（SQEM）  
> 当前状态：Pilot validation

SQET 是 Awesome QA Skills 的 Skill 质量工程方法层，用于设计、评估、验证、演进和审查 Agent Skill。它定义质量声明、评测契约、风险和证据边界；它不是一个可安装的 Skill，也不是第二套 Eval Engine。

## 文档入口

- [Skill Quality Evaluation Model（SQEM）](./SKILL_QUALITY_EVALUATION_MODEL.md)：七个质量域、L1-L4 验证层级、E1-E4 证据层级和 Quality Claim Gate。
- [Skill Eval Contract](./SKILL_EVAL_CONTRACT.md)：Case 类型、Judge、运行元数据、失败分类和证据状态。
- [SQEM Pilot](./SKILL_QUALITY_PILOT.md)：五个 SQEM 方法论 Pilot 候选及阶段、指标和退出条件。

### 模板

- [Behavior Contract](./templates/SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md)
- [Evidence Report](./templates/SKILL_EVIDENCE_REPORT_TEMPLATE.md)
- [Quality CI Guide](./templates/SKILL_QUALITY_CI_GUIDE.md)
- [Quality Profile](./templates/SKILL_QUALITY_PROFILE_TEMPLATE.md)
- [Risk Profile](./templates/SKILL_RISK_PROFILE_TEMPLATE.md)

## 与仓库其他层的关系

- `skills/{zh,en}/skill-engineering/` 存放可被 Agent 调用的 Skill；SQET 文档只描述质量方法和标准，不替代这些 Skill。
- `evals/` 存放各 Skill 自己的 Eval 配置和用例；SQET 不创建全仓库共享的第二个 Case 仓库。
- `evidence/skill-quality/` 存放经过审阅或由 runner 生成的质量证据；没有运行证据时保持 `NOT_RUN`、`BLOCKED`、`UNASSESSED`、`NOT_SCORED` 或 `INSUFFICIENT_EVIDENCE`。
- 站点文章属于网站内容，不作为本 Toolkit 的方法论入口。

## 现有事实来源

SQET 复用仓库已有治理契约，不重新定义同名规则：

- [Quality Score 与最低 Eval 契约](../governance/QUALITY_SCORE_EVAL_CONTRACT.md) 负责九维 Quality Score 和最低 Eval 要求。
- [Skill Evaluation Contract](../governance/SKILL_EVALUATION_CONTRACT.md) 负责运行证据状态、失败分类和 Router `skill.selection` / `selected_skills` 结构化选择证据。
- [Skill Evaluation Quality Loop](../governance/SKILL_EVALUATION_DESIGN.md) 负责现有 `skill-up`、本地 trace 规则和评测工作流边界。
- [现有 Skill Evaluation Pilots](../governance/SKILL_EVALUATION_PILOTS.md) 记录 `requirements-analysis`、`ui-test-playwright` 和 `discover-testing` 的既有 Pilot。

因此，当前 SQET 结论是 **Pilot validation**，不是全仓库 runtime quality 证明、跨模型兼容性证明、业务验收或 release approval。核心规则是：

```text
Quality Claim <= Available Evidence
```

在没有真实 Agent、目标环境、跨模型或业务验收证据时，文档和报告必须明确限制，不得把静态门禁或 `skill-up validate` 写成运行效果结论。
