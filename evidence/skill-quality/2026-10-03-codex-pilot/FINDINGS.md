<div align="right"><strong>🇨🇳 中文</strong> | <a href="./FINDINGS_EN.md">🇬🇧 English</a></div>

# 缺陷分类与修复记录

用于解释为什么改 Eval、哪些结果已被后续运行替代，以及仍不能得出的结论。原生 FAIL 不删除，重新判分与重新调用 Agent 分开记录。

| 问题 | 分类 | 处理与复核 |
| --- | --- | --- |
| 旧临时传输只返回文本，丢失 JSONL/usage；安装目标和插件隔离不明确 | Infrastructure Defect | 改为 SessionResult、明确 `.agents/skills/<name>`、禁用全局/插件 Skill、关闭 stdin；6 个单元测试，实际 catalog 核对 |
| 输出覆盖了异常、假设、证据或推荐行动，但未匹配某个固定词/英文大小写/中文标题 | Eval Defect | 只移除重复字面要求或匹配正式模板的等义写法；保留业务风险、边界、缺口和可执行输出要求 |
| 合法 `NOT_RUN` 未匹配只接受 `not run` 的正则 | Eval Defect | 接受空格和下划线两种形式；规范标签仍保持有效 |
| functional-testing 风险用例输出登录→下单→支付链路，但没写“关键路径”标题 | Eval Defect | 接受明确、按顺序的核心业务链，不改其优先级/降级/残余风险断言 |
| scope 用例让用户直接要求换引擎，却把“提到 skill-up”当成拒绝替换证据 | Eval Defect | 改为当前 Skill 范围内的提案评审，明确不实施；同时检查边界表达和保留现有流程；中英文各完整重跑 3/3 |
| skill-evaluation 极少输入时曾仅使用自然语言代替规范状态 | Skill Defect，已有修复 | 两种语言的 Skill/prompt 已要求最小报告保留适用 canonical state；本次完整组复测通过，不追认旧证据为业务 PASS |
| semantic judge 把自然语言“未运行”算成 canonical-state 满足 | Eval Defect | 增加两边相同的确定性前置检查；保留近似错误样例，重新运行该 Benchmark；不降低 rubric |
| 初版 functional positive golden 缺少充分预期结果与残余风险 | Eval Defect（校准样例） | 补全 golden 后复测，原 FAIL 和修订版 PASS 均保留，不修改合格阈值 |
| 服务端在 unsafe seam 请求产生回答前安全拦截 | Infrastructure Defect / provider_safety_filter | 保留 native ERROR；证据状态 BLOCKED，停止英文等价请求，不评价拒绝质量、不绕过过滤 |
| 缺少 canonical selection event | 缺少观测能力，不是已确认 Trigger Defect | `BLOCKED`；不能用输出相似度、Skill catalog 或文件读取替代 |
| 脱敏规则只覆盖完整工作目录，遗漏祖先 AGENTS 探测中的 macOS 临时父目录 | Infrastructure Defect（证据导出） | 2026-10-04 补充父目录脱敏；两条回归先失败后通过，完整证据包扫描通过；保留原始哈希，只更新一份 trace 的导出哈希，不重跑模型或改写结果 |

## 如何追溯

`artifacts/core/` 保留第一轮核心结果；`postfix/` 保留相关 Eval 修复后的组；`final/` 是范围用例修复后两种语言的最终 skill-evaluation 完整组。`cross-model/` 与 `cross-model-postfix/` 同样分开。最新组选择列表在 [results.json](./results.json)，不是把所有历史样本都计成通过。

`diagnostics/grade-*-red.json` 与 `grade-*-green.json` 是**同一已捕获回答的确定性重新判分**，证明对应断言问题得到修复；它们不是新的模型生成或 previous/current Skill 版本回归。其未带 red/green 后缀的文件保存对应输入与判分配置。

`artifacts/benchmark/` 保留首次对比，`benchmark-postfix/` 保存 canonical-state 前置检查修正后对比。`calibration/` 保留最初合成样例，`calibration-postfix/` 保存完善后的 functional positive，`calibration-near-miss/` 保存必须判为 FAIL 的状态契约近似错误样例。合成主体没有消耗生成模型，judge 调用单独记录。

## 判定限制

本次没有因单次红灯而自动修改 Skill。核心组以显式文本断言为主，不足以证明所有领域建议都正确。校准只有少量人工编写标签、未获业务评审人独立确认；现有正则和 semantic judge 都不能替代高风险领域验收。最终为 `FAIL` 的 without-Skill Benchmark 是有效观察，不是应“修到绿灯”的错误。
