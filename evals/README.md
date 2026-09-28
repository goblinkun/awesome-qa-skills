<div align="right"><strong>🇨🇳 中文</strong> | <a href="./README_EN.md">🇬🇧 English</a></div>

# 根级 Skill Eval 目录边界

## 默认事实来源

每个 Skill 的本地 `eval.yaml` 和 `cases/` 是 Eval 的默认事实来源，位置为：

```text
skills/{zh,en}/<category>/<skill>/evals/
```

评测设计、配置和用例应随对应 Skill 一起维护，保证 Skill 可以独立安装、复核和演进。根级 `evals/` 不移动、复制或重新声明现有 Skill-local 用例。

## 根级目录允许承载的内容

只有经过单独设计并明确 owner 的资产才适合放在根级目录，例如：

- runner-adapted 的跨 Skill 组合资产；
- 明确服务多个 Skill 的汇总或对比资产；
- 与仓库治理门禁配套的评测说明。

新增根级资产必须说明输入来源、适用范围、执行方式、证据产物和与 Skill-local Eval 的关系；它不能成为第二个 Eval Engine 或隐式的全局 Case 仓库。

## 质量结论边界

Eval 配置可以通过静态或结构检查，不代表模型、Agent、目标环境或业务结果已经验证。未执行的内容必须保持 `NOT_RUN`、`BLOCKED`、`UNASSESSED`、`NOT_SCORED` 或 `INSUFFICIENT_EVIDENCE`，不能升级为质量通过、运行时兼容或发布批准。

质量方法和状态定义见 [SQET 入口](../docs/skill-quality-engineering/README.md) 与 [Skill Evaluation Contract](../docs/governance/SKILL_EVALUATION_CONTRACT.md)。
