<div align="right"><strong>🇨🇳 中文</strong> | <a href="./SQEM_V1_1_PROPOSAL_EN.md">🇬🇧 English</a></div>

# SQEM v1.1 改进提案

状态：**提案，未发布的新规范**。用于评审本次 Pilot 暴露的有效性、可观测性与维护成本问题；不新增 Engine、Judge 或 Quality Score。

## 建议保留与删减

| 建议 | 本次依据 | 验收方式 |
| --- | --- | --- |
| 行为优先，减少重复固定措辞检查 | 多次真实回答被标题、大小写或等义表达误判 | 对同一正向回答及一个真实负向样例都判对，而不是只看绿色 |
| 区分正文自然语言与机器 enum | semantic judge 误把“未运行”算成 canonical state | enum 放确定性前置检查，语义 rubric 只评真正需要的判断 |
| 校准需正、反与近似错误样例 | 初版 golden 不充分；状态 near-miss 能揭示 false positive | 业务评审人独立确认 anchors，保存预期/实际/分歧；本次 7 个样例只作为 smoke |
| 真实宿主安装与隔离写入最小元数据 | 旧 transport 只回文本，目标未明确且可能加载插件 | 每次记录 target、catalog、全局隔离、native JSONL、模型与 usage |
| 严格区分 availability/read 与 selection | CLI 缺 canonical selection event | 没有事件保持 BLOCKED，不用输出/读文件证明自然触发 |
| 范围评审与另行授权架构任务分开 | 旧“换引擎”请求不是有效的边界评测 | 输入明确当前流程中的评审范围；需要实现替换则另行授权/设计 |
| 主体/judge/未知 usage 分开 | 一次 provider 拦截没有 usage；缓存不能重复算 | 独立调用账本，unknown 不写 0，费用不凭模型标价推用户账单 |
| 核心、对比、业务证据分层 | 34 个文本 PASS 不能证明真实压测、业务或发布 | 每层声明可支持/不可支持的结论；业务必须有项目与责任人 |

## 下一轮有限实验

先保留已有五个核心组，不做全组合膨胀。对三个选定 Skill 各选少量经过领域评审的稀疏/困难输入，在经确认的预算内重复 with/without，控制参数、顺序与 judge。报告每个 case/variant，而不是只展示平均总分。遇到安全过滤停止等价请求，不以换模型或改写请求绕过。

兼容先补有授权凭据的 Claude 代表采样；trigger 层需要真正提供 selection 事件的宿主。真实业务只从一个获授权项目的最小关键路径开始。上述实验尚未执行，不能加入当前 PASS 数。

## 暂不采用

- 新全局评分、第二个 Eval Engine 或“自动修到通过”循环。
- 把所有 Skill 都扩成同一个大配额 Eval suite。
- 根据单次 Benchmark 给所有 Skill 授 L3 或宣布增益。
- 将 provider filtering 算成 Skill 负向行为 PASS。

正式推进 v1.1 前还需确认维护预算、业务验收、人工 judge 校准及未完成验证项；本提案仅给出可行动的改进方向。
