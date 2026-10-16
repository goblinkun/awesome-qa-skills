本次按“Prompt 内容与行为变更 + eval.yaml 评测配置变更”选择验证，依据本地 `skill-change-verification` Skill。

| 选择的检查 | 证据等级 | 验证目标 |
|---|---|---|
| 审查 Prompt 差异 | Human review | 指令一致性、适用范围、术语与预期行为 |
| 检查 YAML 语法、项目 schema 和引用路径 | Static / Structural | 配置可解析、必需字段完整、引用有效；具体命令待确认 |
| `skill-up validate` | Evaluation | 检查工具实际覆盖的规则；覆盖范围和调用参数待确认 |
| 实际运行修改后的 Prompt，并执行受影响的评测用例 | Runtime | 验证行为是否符合预期，覆盖正常、边界和回归场景；运行命令待确认 |

**两者的区别：**`skill-up validate` 通过，只能说明其覆盖的检查通过。它不等于运行时语义验证，不能据此声称 Prompt 实际行为正确。运行时验证需要真实执行 Prompt，并检查输出与预期是否一致；仅确认 eval.yaml 能解析或加载也不足以证明行为正确。

本次已执行的检查：

| 命令 | 证据等级 | 结果 |
|---|---|---|
| `cat .agents/skills/skill-change-verification/SKILL.md` | Static | 已读取验证规则 |
| `cat .agents/skills/skill-change-verification/prompts/skill-change-verification.md` | Static | 已读取证据分级与汇报要求 |

本次未提供具体变更差异，也未运行配置检查、`skill-up validate` 或运行时评测。按照你的限制，未读取评测断言或 evaluator 输入文件，未访问外部服务或执行生产写入。

可以声称：已完成验证选型并明确证据边界。不能声称：变更已通过验证或没有回归。残余风险是 Prompt 行为变化及评测覆盖缺口尚未验证。
