# 全量 Skill 修复与二次 Review (2026-10-07)

> 本页保留 2026-10-07 的历史结果和阻塞原因。持续外部运行授权已补齐，后续修复与最新状态见 [真实运行续评](./2026-10-08-review-runtime-continuation.md)。

[English](./2026-10-07-all-skills-repair-review_EN.md)

已逐项处理 164 个 Skill、328 个语言目录的首轮建议，并继续复查修复内容。原始 review 保留为快照；本报告记录实际改动、二次发现与验证范围。**静态/脚本修复已验证，完整模型行为评测尚未完成。**

原始审查：[2026-10-06 review](./2026-10-06-all-skills-review.md)。
逐项机器记录：[evidence JSON](./2026-10-07-all-skills-repair-review-evidence.json)；验证证据：[summary.json](../../evidence/skill-quality/2026-10-07-review-repair/summary.json)

本轮实际运行与阻塞详情：[2026-10-07-review-runtime-followup.md](./2026-10-07-review-runtime-followup.md)。

## 修复范围

42 项领域方法、59 项方法/工具增强、50 项评测或工作流覆盖、13 项共享脚本/契约。新增 530 个案例（EN/ZH 各 265），当前共 1,658 个案例；保留原有案例与 canonical name。另同步受影响的 Excel helper 与中文元数据。

## 验证与限制

| 检查 | 结果与可支持范围 |
| --- | --- |
| `bash scripts/check_skills_quality.sh` | PASS；328 份 eval 配置合法，227 个脚本测试通过；结构/独立性/双语/治理检查通过。 |
| `SKILLS_CLI_PACKAGE="$PWD" bash scripts/check_skills_cli_compatibility.sh` | PASS；固定 skills@1.7.0 发现 164 项，英文 functional-testing 在隔离目标安装通过；不代表 Skill 运行。 |
| 真实框架本地请求 | 8 个 EN/ZH 项目、24 次结果运行：合法响应通过，错误状态和错误业务体分别失败；仅本地合成服务。 |
| 独立 helper 与 grader | 74 份资源副本一致；118 份 grader 独立复制、两种表格形式和变异对照通过；Plus CLI 导出检查 26 项。 |
| JMeter / Gatling / UI | JMeter 本地合成 good 通过、业务错误及 CSV 提前耗尽 gate 失败；Gatling Java DSL 编译通过。UI 浏览器运行与实际负载/SLO 验收 NOT_RUN。 |
| 模型评测 | 新增 530 用例中：13 个不同用例报告实际 PASS，1 个评分误判已修复但待实际重跑，1 个 judge ERROR，515 个 NOT_RUN。剩余脚本队列受审批阻塞；语义 judge 受登录/模型兼容性阻塞。 |

先前获授权的中英文两个用例及其历史记录保留在 [model-pilot-summary.json](../../evidence/skill-quality/2026-10-07-review-repair/model-pilot-summary.json)。继续运行的逐用例记录见 [runtime-followup.json](../../evidence/skill-quality/2026-10-07-review-repair/runtime-followup.json)。Codex CLI 实际观察版本为 0.160.1，模型身份 UNKNOWN；这些定向结果不能证明全库效果提升。

复杂 OpenAPI schema 与 WSDL SOAP envelope 尚不能由确定性生成器自动完成；缺有来源的请求或断言时明确返回未完成脚手架。主 Prompt 可继续补齐，但生成器成功与生产验收不能混为一谈。新增 judge 的公开模型 ID 依据 [OpenAI GPT-5 文档](https://developers.openai.com/api/docs/models/gpt-5)；本轮没有 API provider 运行证据。

## 二次发现与处理

| 问题 | 修复 | 定位 |
| --- | --- | --- |
| XLSX 与 Markdown 保真 | 解析 inlineStr、富文本、稀疏列、多工作表与缓存公式，保留工作表/行号；无法可靠解析时报告错误。Plus 的行序列化保留字段边界与符号。 | [test_review_parser_fidelity.py](../../scripts/tests/test_review_parser_fidelity.py) |
| API 源及生成器 | 修复隐式 curl POST、变量 URL、请求体与多场景；OpenAPI 数字状态键和未解析引用显式处理；WSDL 按端口绑定操作。标准化 endpoints JSON 可直接进入生成链。 | [test_review_api_generators.py](../../scripts/tests/test_review_api_generators.py) |
| 缺规则时的假通过 | 生成器缺预期、请求值或 schema 断言时以非零状态标未完成；认证来自环境变量；模板取消普遍接受 404 的检查。 | [api_case_contract.py](../../scripts/skill_resources/api_case_contract.py) |
| Bruno 实际运行 | 修复 JSON body 缩进；CLI 返回 0 但跳过全部请求时，报告 gate 检查实际 HTTP 响应、执行数和断言并失败。 | [test_review_bruno_reports.py](../../scripts/tests/test_review_bruno_reports.py) |
| Plus 固定结论 | 四种 Plus helper 删除固定促销/支付/库存、优先级和指标；保留完整来源、哈希和未知状态，空源失败；不会把证据准备当语义分析完成。 | [test_review_plus_scaffolds.py](../../scripts/tests/test_review_plus_scaffolds.py) |
| grader 独立执行 | 118 份 domain grader 改成可独立复制的 Python 文件；合法无外框 Markdown 表格可通过，遗漏、重复、错误决策及计算错误会失败。 | [test_review_eval_graders.py](../../scripts/tests/test_review_eval_graders.py) |
| grader 数据与对照 | 32 份根修复 grader 加入逐 ID 正反对照；22 份结构化结果 grader 拒绝重复 JSON 键和布尔计数；缺规则对照显式带入独立合同。 | [test_review_eval_graders.py](../../scripts/tests/test_review_eval_graders.py) |
| 既有输出合同 | 方法附表保留既有 RA/RC/RT 等枚举与证据状态；建议改写不覆盖原标准，Go/No-Go 建议不替代授权批准。 | [requirement-traceability-analysis.md](../../skills/zh/testing-types/requirement-traceability-analysis/prompts/requirement-traceability-analysis.md) |
| 阈值与模型配置 | Retry-After 保留协议单位；性能门槛来自输入；新增 agent_judge 改用文档中的公开 API 模型 ID，配置通过不代表 provider 运行通过。 | [api-rate-limit-testing.md](../../skills/zh/testing-types/api-rate-limit-testing/prompts/api-rate-limit-testing.md) |
| 实际运行中的评分误判 | 修复 prose-trim 的末尾换行误判与来源联合的版本化字段误判；原始 FAIL、修复、离线重判和实际重跑分开记录。 | [runtime follow-up](./2026-10-07-review-runtime-followup.md) |

## 逐项修复与复查（164 项）

每项均对应中文和英文版本；“静态复查”指入口、主 Prompt、fixture、oracle、独立安装和原合同复核。“NOT_RUN”不会因 YAML 合法、grader 正反对照通过或目录可见而变成模型通过。

### 001. `skill-change-verification` (P1)

定位：[ZH](../../skills/zh/skill-engineering/skill-change-verification/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-change-verification/SKILL.md)

- 首轮建议：将 validate 归入结构/配置验证；Evaluation 单列实际 run 与 judge 结果。补一个变更类型→必需检查→可支持结论的最小决策表。
- 已改：将 validate 归为配置证据；实际 run 与 judge 才属于 Evaluation；补变更、检查、可支持结论的决策表及逐 ID 判定 grader。
- 新案例：[review-repair-regression](../../skills/zh/skill-engineering/skill-change-verification/evals/cases/review-repair-regression.yaml) — skill-change-verification: sourced repair regression。
- 二次复查/验证：契约或路由正反 fixture/grader 控制通过；双端配置 合法（仅配置）。
- 模型验证：当前 EN/ZH 定向用例均 PASS；V1 判 NOT_RUN，V2 判 FAIL，并保留来源和未执行边界。其他模型用例未运行。

### 002. `skill-evaluation` (P2)

定位：[ZH](../../skills/zh/skill-engineering/skill-evaluation/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-evaluation/SKILL.md)

- 首轮建议：补可比/不可比运行对、缺少 selection 事件、基础设施超时三个真实工件 fixture；验证失败分类与比较结论，而不只检查章节。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-comparable-runs](../../skills/zh/skill-engineering/skill-evaluation/evals/cases/review-comparable-runs.yaml) — 比较身份固定的 previous/current 工件；[review-incomparable-runs](../../skills/zh/skill-engineering/skill-evaluation/evals/cases/review-incomparable-runs.yaml) — 模型和输入变化不能归因版本退化；[review-trace-and-timeout](../../skills/zh/skill-engineering/skill-evaluation/evals/cases/review-trace-and-timeout.yaml) — 区分 selection 缺失与基础设施超时。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 模型验证：EN `review-comparable-runs` 已执行，judge 因当前登录不支持配置的 `gpt-5` 而 ERROR；模型输出复核不等于自动语义验收。其余新增用例 NOT_RUN。

### 003. `skill-prose-review` (P2)

定位：[ZH](../../skills/zh/skill-engineering/skill-prose-review/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-prose-review/SKILL.md)

- 首轮建议：提供一个带真实冲突的小型 Skill fixture，以及一份正确反例；要求定位具体行、影响和修订建议，减少仅复述审查清单的通过。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-conflicting-source](../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-conflicting-source.yaml) — 定位实际输出和 metadata 冲突；[review-consistent-control](../../skills/zh/skill-engineering/skill-prose-review/evals/cases/review-consistent-control.yaml) — 正确契约不得误报相同冲突。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 004. `skill-prose-trim` (P2)

定位：[ZH](../../skills/zh/skill-engineering/skill-prose-trim/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-prose-trim/SKILL.md)

- 首轮建议：用 before/expected-after 文本 fixture 验证实际清理；新增正式历史记录、测量限制与过程残留混排的用例，并说明纯审查与授权编辑两种输出。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-authorized-trim](../../skills/zh/skill-engineering/skill-prose-trim/evals/cases/review-authorized-trim.yaml) — 授权清理必须保留契约和历史事实；[review-only-trim](../../skills/zh/skill-engineering/skill-prose-trim/evals/cases/review-only-trim.yaml) — 纯审查区分建议和实际编辑。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 模型验证：EN/ZH `review-authorized-trim` 实际复测 PASS；EN 首次换行误判保留为历史 FAIL。`review-only-trim` 两端仍 NOT_RUN。

### 005. `skill-quality-review` (P2)

定位：[ZH](../../skills/zh/skill-engineering/skill-quality-review/SKILL.md) · [EN](../../skills/en/skill-engineering/skill-quality-review/SKILL.md)

- 首轮建议：添加最小完整包、缺主提示词、裸文本引用缺文件、双语输出字段不一致四个 fixture；明确与 skill-prose-review 的选用边界。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-bilingual-schema](../../skills/zh/skill-engineering/skill-quality-review/evals/cases/review-bilingual-schema.yaml) — 双语输出字段不一致需要定位；[review-missing-bare-resource](../../skills/zh/skill-engineering/skill-quality-review/evals/cases/review-missing-bare-resource.yaml) — 裸文本资源路径也必须可解析；[review-missing-prompt](../../skills/zh/skill-engineering/skill-quality-review/evals/cases/review-missing-prompt.yaml) — 入口指向缺失主提示词；[review-valid-package](../../skills/zh/skill-engineering/skill-quality-review/evals/cases/review-valid-package.yaml) — 完整包允许无静态阻塞发现。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 006. `daily-testing-workflow` (P2)

定位：[ZH](../../skills/zh/testing-workflows/daily-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/daily-testing-workflow/SKILL.md)

- 首轮建议：以红环境、P0 尚未启动和日终失败未登记作为评测输入，断言工作队列被重排、P0 失败升级且下一跳唯一；允许非标准班次按里程碑表达节奏。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-red-night-shift](../../skills/zh/testing-workflows/daily-testing-workflow/evals/cases/review-red-night-shift.yaml) — 夜班红环境必须重排工作队列；[review-unregistered-close-failure](../../skills/zh/testing-workflows/daily-testing-workflow/evals/cases/review-unregistered-close-failure.yaml) — 未登记 P0 失败阻止收尾门禁；[review-unstarted-p0](../../skills/zh/testing-workflows/daily-testing-workflow/evals/cases/review-unstarted-p0.yaml) — P0 未启动时检查点压缩 P2。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 007. `discover-testing` (P1)

定位：[ZH](../../skills/zh/testing-workflows/discover-testing/SKILL.md) · [EN](../../skills/en/testing-workflows/discover-testing/SKILL.md)

- 首轮建议：在包内提供轻量的可用能力/精确 ID 清单，并标明目录快照；扩展专项近邻负例，如认证/授权、RAG 检索/质量、回归范围/选择。保持一主至多一辅。
- 已改：补独立可复制的 164 项目录快照及可用性 UNKNOWN；路由区分认证、授权、RAG 检索和回归选择，控制主 Skill 与辅助 Skill 数量。
- 新案例：[review-authn-neighbor](../../skills/zh/testing-workflows/discover-testing/evals/cases/review-authn-neighbor.yaml) — discover-testing: sourced repair regression；[review-authz-neighbor](../../skills/zh/testing-workflows/discover-testing/evals/cases/review-authz-neighbor.yaml) — discover-testing: sourced repair regression；[review-rag-retrieval-neighbor](../../skills/zh/testing-workflows/discover-testing/evals/cases/review-rag-retrieval-neighbor.yaml) — discover-testing: sourced repair regression；[review-regression-selection-neighbor](../../skills/zh/testing-workflows/discover-testing/evals/cases/review-regression-selection-neighbor.yaml) — discover-testing: sourced repair regression。
- 二次复查/验证：契约或路由正反 fixture/grader 控制通过；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 模型验证：认证、授权、RAG 检索和回归选择 4 个新增用例 × EN/ZH 均实际 PASS（共 8）；只支持这些 fixture，不代表完整 Skill 套件。

### 008. `multi-role-quality-synthesis` (P2)

定位：[ZH](../../skills/zh/testing-workflows/multi-role-quality-synthesis/SKILL.md) · [EN](../../skills/en/testing-workflows/multi-role-quality-synthesis/SKILL.md)

- 首轮建议：补跨 stage 报告混入、同一 source_id 不同版本、同名但非等价发现三个对抗 fixture；将来源集合完整性加成确定性检查，语义合并继续由校准 judge 负责。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-duplicate-source-version](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/cases/review-duplicate-source-version.yaml) — 同一 source_id 的不同版本不能混淆身份；[review-mixed-stage](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/cases/review-mixed-stage.yaml) — 混入不同 stage 不得静默汇总；[review-similar-name-distinct-conditions](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/cases/review-similar-name-distinct-conditions.yaml) — 发现同名不能证明语义等价；[review-source-union](../../skills/zh/testing-workflows/multi-role-quality-synthesis/evals/cases/review-source-union.yaml) — 合并保留全部来源与少数 P0。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 模型验证：EN 来源联合用例实际 PASS；ZH 首次因版本化字段被评分器误拒而 FAIL，修复后原输出离线重判 PASS，实际重跑被审批阻止；其他新增用例 NOT_RUN。

### 009. `product-quality-perspective` (P2)

定位：[ZH](../../skills/zh/testing-workflows/product-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/product-quality-perspective/SKILL.md)

- 首轮建议：补 test-strategy 和 test-report-review 的独立成功用例；统一 role report 的 source_id/version、发现 ID、行动证据字段，便于汇总而不硬依赖其它 Skill。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-no-product-impact-control](../../skills/zh/testing-workflows/product-quality-perspective/evals/cases/review-no-product-impact-control.yaml) — 无产品影响的后端变更不生成填充发现；[review-test-report-evidence](../../skills/zh/testing-workflows/product-quality-perspective/evals/cases/review-test-report-evidence.yaml) — 产品报告评审识别无证据全范围结论；[review-test-strategy-evidence](../../skills/zh/testing-workflows/product-quality-perspective/evals/cases/review-test-strategy-evidence.yaml) — 产品策略优先不可逆用户损失。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 010. `project-delivery-perspective` (P2)

定位：[ZH](../../skills/zh/testing-workflows/project-delivery-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/project-delivery-perspective/SKILL.md)

- 首轮建议：每个支持阶段补一个成功 fixture；把交付要求、已授权决策、质量证据分列，并增加时区、依赖延期和未指派行动的表达规则。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-test-report-review-sources](../../skills/zh/testing-workflows/project-delivery-perspective/evals/cases/review-test-report-review-sources.yaml) — test-report-review 的交付来源成功路径；[review-test-strategy-review-sources](../../skills/zh/testing-workflows/project-delivery-perspective/evals/cases/review-test-strategy-review-sources.yaml) — test-strategy-review 的交付来源成功路径；[review-test-strategy-sources](../../skills/zh/testing-workflows/project-delivery-perspective/evals/cases/review-test-strategy-sources.yaml) — test-strategy 的交付来源成功路径。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 011. `qa-quality-perspective` (P2)

定位：[ZH](../../skills/zh/testing-workflows/qa-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/qa-quality-perspective/SKILL.md)

- 首轮建议：补 test-reporting 和 test-report-review 的有证据成功路径；将高/中/低风险的影响、可能性与不确定性判断锚点写成一个小表，避免乘积表述被误作数值评分。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-test-report-review-raw-results](../../skills/zh/testing-workflows/qa-quality-perspective/evals/cases/review-test-report-review-raw-results.yaml) — QA test-report-review 有证据成功路径；[review-test-reporting-raw-results](../../skills/zh/testing-workflows/qa-quality-perspective/evals/cases/review-test-reporting-raw-results.yaml) — QA test-reporting 有证据成功路径。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 012. `release-testing-workflow` (P1)

定位：[ZH](../../skills/zh/testing-workflows/release-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/release-testing-workflow/SKILL.md)

- 首轮建议：统一写为 Go/No-Go 建议及待授权决策，明确决策者和证据来源；将 T-14 等设为可压缩示例，并补紧急热修/灰度窗口。
- 已改：将 Go/No-Go 建议与有权限人员的批准记录分开；发布路径和退出门槛按常规、热修、灰度材料适配，不从测试结果推断批准。
- 新案例：[review-repair-regression](../../skills/zh/testing-workflows/release-testing-workflow/evals/cases/review-repair-regression.yaml) — release-testing-workflow: sourced repair regression。
- 二次复查/验证：契约或路由正反 fixture/grader 控制通过；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 013. `sprint-testing-workflow` (P2)

定位：[ZH](../../skills/zh/testing-workflows/sprint-testing-workflow/SKILL.md) · [EN](../../skills/en/testing-workflows/sprint-testing-workflow/SKILL.md)

- 首轮建议：以用户迭代长度、容量和事件驱动里程碑映射阶段；补一周迭代、持续流、延期故事与未接受 P0 的行为用例。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-continuous-flow](../../skills/zh/testing-workflows/sprint-testing-workflow/evals/cases/review-continuous-flow.yaml) — 持续流使用事件而非编造日期；[review-one-week-capacity](../../skills/zh/testing-workflows/sprint-testing-workflow/evals/cases/review-one-week-capacity.yaml) — 一周迭代保留全部阶段门禁；[review-spillover-unaccepted-p0](../../skills/zh/testing-workflows/sprint-testing-workflow/evals/cases/review-spillover-unaccepted-p0.yaml) — 未接受 P0 与延期故事不能宣告完成。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 014. `technical-quality-perspective` (P2)

定位：[ZH](../../skills/zh/testing-workflows/technical-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/technical-quality-perspective/SKILL.md)

- 首轮建议：补 requirements-analysis 和 test-strategy 的独立成功路径；固定静态发现的文件/行/版本定位格式，避免与 code-review、专项设计审查重复输出。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-requirements-analysis-design](../../skills/zh/testing-workflows/technical-quality-perspective/evals/cases/review-requirements-analysis-design.yaml) — requirements-analysis 的技术证据成功路径；[review-test-report-review-version](../../skills/zh/testing-workflows/technical-quality-perspective/evals/cases/review-test-report-review-version.yaml) — 技术报告评审保留版本错配；[review-test-strategy-design](../../skills/zh/testing-workflows/technical-quality-perspective/evals/cases/review-test-strategy-design.yaml) — test-strategy 的技术证据成功路径。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 015. `ux-quality-perspective` (P2)

定位：[ZH](../../skills/zh/testing-workflows/ux-quality-perspective/SKILL.md) · [EN](../../skills/en/testing-workflows/ux-quality-perspective/SKILL.md)

- 首轮建议：补 test-reporting/test-report-review 的独立成功用例；增加输入方式×设备×辅助技术×状态的可选证据矩阵，并标明它由项目材料选择。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-test-report-review-experience](../../skills/zh/testing-workflows/ux-quality-perspective/evals/cases/review-test-report-review-experience.yaml) — test-report-review 的 UX 观察结果成功路径；[review-test-reporting-experience](../../skills/zh/testing-workflows/ux-quality-perspective/evals/cases/review-test-reporting-experience.yaml) — test-reporting 的 UX 观察结果成功路径。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 016. `acceptance-criteria-review` (P2)

定位：[ZH](../../skills/zh/testing-types/acceptance-criteria-review/SKILL.md) · [EN](../../skills/en/testing-types/acceptance-criteria-review/SKILL.md)

- 首轮建议：区分核对现有标准、建议改写、缺规则三种模式；补带 AC ID 的原标准与修改对照 fixture，验证等于阈值和重复退款的可观察预期。
- 已改：先选择 `review`（核对原标准）、`proposed-rewrite`（建议改写）或 `missing-rule`（规则缺失）；保留原 AC ID、版本、原文和来源，不把建议覆盖成原规则。；逐条输出：AC ID | 原标准 | 模式 | 可观察预期 | 建议文本 | 差异原因 | 待产品确认。无规则的格子保持待确认。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/acceptance-criteria-review/evals/cases/domain-method-regression.yaml) — acceptance-criteria-review: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 017. `accessibility-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/accessibility-testing/SKILL.md) · [EN](../../skills/en/testing-types/accessibility-testing/SKILL.md)

- 首轮建议：显式记录目标 WCAG 版本/等级、成功标准 ID、键盘/读屏/自动扫描的证据类型；补自动扫描通过但键盘仍阻断的用例，避免把扫描等同合规。
- 已改：记录项目指定的 WCAG 版本/等级、范围和成功标准 ID；目标未指定时列为缺口，不能自行选等级或声称合规。；建立 成功标准 ID | 用户任务/状态 | 输入方式/辅助技术/版本 | 检查步骤 | 证据类型 | 结果 表。自动扫描、键盘操作、读屏和人工视觉检查分别记录。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/accessibility-testing/evals/cases/domain-method-regression.yaml) — accessibility-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 018. `agent-failure-recovery-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-failure-recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-failure-recovery-testing/SKILL.md)

- 首轮建议：补“故障→重试/补偿/升级→恢复后状态”表；用超时但已写入、部分结果和永久错误 fixture 验证重复副作用与恢复证据。
- 已改：按项目协议建立 故障 | 写入是否确认 | 可重试性 | 重试/补偿/升级 | 恢复后状态 | 所需证据 表；暂时错误、永久错误和结果不确定分开。；超时不能推出未执行：先以 operation_id/幂等键查已提交副作用，再决定读回结果或安全重试；同键不得产生第二次业务写入。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/agent-failure-recovery-testing/evals/cases/domain-method-regression.yaml) — agent-failure-recovery-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 019. `agent-long-running-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-long-running-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-long-running-testing/SKILL.md)

- 首轮建议：补中断/恢复状态机、checkpoint 版本、租约和取消竞争的判定；用崩溃后恢复与重复提交 trace 验证已完成步骤不重做、资源释放可见。
- 已改：从实际协议写出 queued→running→checkpointed→interrupted→resuming→completed 和 running→cancelling→cancelled；未定义状态或转换标为待确认。；每个 checkpoint 记录 task_id、schema/状态版本、已提交 step ID、来源和完整性；恢复先校验版本与已提交效果，版本不兼容不得盲目重放。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/agent-long-running-testing/evals/cases/domain-method-regression.yaml) — agent-long-running-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 020. `agent-loop-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-loop-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-loop-testing/SKILL.md)

- 首轮建议：补动作/观察去重、无进展周期、时间/费用预算优先级；用重复调用 trace 验证进入停止或升级分支，而不只出现“循环”关键词。
- 已改：按 task/run/step ID 记录计划、工具名与归一化参数、观察身份/摘要、业务状态变化和时间/费用累计；敏感参数脱敏但保留去重依据。；进展以项目目标的新证据或状态前进判断；动作/观察相同且目标未前进记无进展周期。只重复文本或工具成功不算进展。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/agent-loop-testing/evals/cases/domain-method-regression.yaml) — agent-loop-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 021. `agent-memory-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-memory-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-memory-testing/SKILL.md)

- 首轮建议：补版本/来源/租户标识、过期和删除后检索判据；用两个租户、旧新偏好冲突及删除 fixture 检查污染和遗忘，未知保留策略不能自定。
- 已改：为记忆记录 tenant/user ID、memory ID、内容版本、来源、写入时间、有效期、撤回/删除状态；检索结果保留来源版本，不只检查最终回答。；先依据项目优先级规则选择新旧偏好；冲突未定义时标为待确认，不能默认最后写入或自定保留期。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/agent-memory-testing/evals/cases/domain-method-regression.yaml) — agent-memory-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 022. `agent-permission-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-permission-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-permission-testing/SKILL.md)

- 首轮建议：补授权撤销、委派和参数变更后重审批用例，检查拒绝时无副作用并保留实际授权来源。
- 已改：建立 主体/委派链 | 工具 | 资源/租户 | 动作 | 参数范围 | 授权来源/版本/期限 | 允许/拒绝/重审批 矩阵，不用工具名代替具体授权。；执行前核对实际身份、授权是否撤销、资源及参数是否仍匹配；委派不能扩大原主体权限，过期或撤销授权失效。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/agent-permission-testing/evals/cases/domain-method-regression.yaml) — agent-permission-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 023. `agent-tool-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/agent-tool-testing/SKILL.md) · [EN](../../skills/en/testing-types/agent-tool-testing/SKILL.md)

- 首轮建议：提供真实工具 schema 与调用 trace，断言参数合法性、工具选择、超时后一次副作用；避免只凭标题认定契约已验证。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-tool-schema-trace](../../skills/zh/testing-types/agent-tool-testing/evals/cases/review-tool-schema-trace.yaml) — 用实际工具 schema 与 trace 判断副作用。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 024. `ai-agent-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/ai-agent-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-agent-testing/SKILL.md)

- 首轮建议：补任务成功判据、轨迹不变量、重复试验次数/样本及终止分类；用“最终答案对但工具越权”的反例验证过程与结果分别结论。
- 已改：对每个任务定义输入样本 ID、成功 oracle、允许工具/资源、禁止副作用和停止条件；未知目标保持待确认。；轨迹按 run/step ID 核对顺序、权限、幂等、数据隔离、恢复和预算不变量；把结果正确性与过程合规分别判定，任一失败不得整体通过。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ai-agent-testing/evals/cases/domain-method-regression.yaml) — ai-agent-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 025. `ai-assisted-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/ai-assisted-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-assisted-testing/SKILL.md)

- 首轮建议：补输入脱敏、AI 草稿与采纳版本的来源链，以及耗时/返工量的基线测量；成功用例应检查人工复核点与产物验收，而非只检查高风险词。
- 已改：先记录输入分类/脱敏方法与允许使用范围；真实身份、令牌和个人数据替换为不可反推占位符，保留 schema 与业务约束。；建立 输入快照 ID→模型/Prompt 版本→AI 草稿 ID→人工复核意见→采纳版本 ID→验收证据 来源链；草稿不自动成为执行资产。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ai-assisted-testing/evals/cases/domain-method-regression.yaml) — ai-assisted-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 026. `ai-feature-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/ai-feature-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-feature-testing/SKILL.md)

- 首轮建议：补产品任务×语言×用户群数据切片、人工标注 rubric 与拒答/降级的独立门槛；阈值来自项目并记录模型/Prompt/数据版本。
- 已改：固定模型、Prompt、知识/评测数据、产品和环境版本；建立 产品任务×语言×用户群×风险 切片，记录抽样来源及样本量，不以总体平均遮盖小群体。；人工 rubric 为每个维度写可观察锚点、标签者、分歧处理和参考答案来源；先校准样本，再按项目评分与权重汇总，未定规则不自造分数。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ai-feature-testing/evals/cases/domain-method-regression.yaml) — ai-feature-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 027. `ai-generated-test-review` (P2)

定位：[ZH](../../skills/zh/testing-types/ai-generated-test-review/SKILL.md) · [EN](../../skills/en/testing-types/ai-generated-test-review/SKILL.md)

- 首轮建议：补 mock 有边界但未替代被测对象、合理快照及合理状态码断言的近邻反例，校准分类误报；保持跨语言分级一致。
- 已改：按所验证的契约判断断言，不能仅因出现 mock、snapshot 或状态码就标为 WEAK/FAKE。；边界 mock 可替代已确认的外部依赖，但被测生产逻辑必须真实执行；mock 被测对象并断言它返回的预设值才缺乏保护。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ai-generated-test-review/evals/cases/domain-method-regression.yaml) — ai-generated-test-review: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 028. `ai-safety-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/ai-safety-testing/SKILL.md) · [EN](../../skills/en/testing-types/ai-safety-testing/SKILL.md)

- 首轮建议：补政策版本→允许/限制/拒答/升级矩阵及合理请求对照；分别验证危险请求的处理和正常任务不过度拒绝，避免以拒答率代替安全性。
- 已改：固定政策 ID/版本/适用对象，建立 类别/条件→允许/限制/拒答/升级→可提供内容/禁止副作用→证据 矩阵；缺政策不自行认定安全批准。；用政策描述的危险样本与近邻正常请求配对；分别检查危险处理正确性、允许请求完成质量和过度拒答，不能只汇总拒答率。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ai-safety-testing/evals/cases/domain-method-regression.yaml) — ai-safety-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 029. `api-contract-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/api-contract-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-contract-testing/SKILL.md)

- 首轮建议：补 old/new schema 与旧客户端 fixture，区分语法可兼容、语义不兼容和迁移未知。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-compatible-additive-control](../../skills/zh/testing-types/api-contract-testing/evals/cases/review-compatible-additive-control.yaml) — 容忍未知字段的消费者可接受可选新增字段；[review-schema-versus-semantics](../../skills/zh/testing-types/api-contract-testing/evals/cases/review-schema-versus-semantics.yaml) — 整数 schema 不变仍可能破坏消费者语义。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 030. `api-design-quality-review` (P2)

定位：[ZH](../../skills/zh/testing-types/api-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/api-design-quality-review/SKILL.md)

- 首轮建议：用真实 OpenAPI diff 校验问题定位及消费者迁移；补设计已完整的反例，要求缺证据项与证实的设计冲突分开，避免每次机械生成所有领域问题。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-complete-operation-control](../../skills/zh/testing-types/api-design-quality-review/evals/cases/review-complete-operation-control.yaml) — 完整限定操作允许无设计阻塞发现；[review-openapi-consumer-diff](../../skills/zh/testing-types/api-design-quality-review/evals/cases/review-openapi-consumer-diff.yaml) — OpenAPI diff 区分已证实冲突与迁移缺口。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 031. `api-error-contract-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-error-contract-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-error-contract-testing/SKILL.md)

- 首轮建议：补状态/错误码/字段、关联 ID、重试含义与脱敏的一致性表；用同一错误不同 operation 的响应 fixture 验证具体冲突。
- 已改：按 operation 与错误触发建立契约表：HTTP 状态、业务码、必需字段/类型、关联 ID、重试含义和脱敏规则；允许有来源的 operation 例外。；把每份响应与请求、日志和契约版本对应，逐字段比对；关联 ID 检查同一次交互的可追踪性，不要求不同请求复用同一 ID。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-error-contract-testing/evals/cases/domain-method-control.yaml) — api-error-contract-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-error-contract-testing/evals/cases/domain-method-success.yaml) — api-error-contract-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 032. `api-idempotency-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-idempotency-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-idempotency-testing/SKILL.md)

- 首轮建议：补同键同载荷/异载荷、并发、有效期、超时后重试矩阵，逐项区分响应复用与业务副作用；用订单写入记录断言。
- 已改：提取键作用域、载荷等价规则、有效期及到期边界、并发处理和重复响应合同；分别列响应复用与订单/支付/消息等业务副作用义务。；建立同键同载荷、同键异载荷、异键、并发、到期前后、提交后超时重试矩阵；每项标初始业务状态与项目预期。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-idempotency-testing/evals/cases/domain-method-control.yaml) — api-idempotency-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-idempotency-testing/evals/cases/domain-method-success.yaml) — api-idempotency-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 033. `api-negative-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-negative-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-negative-testing/SKILL.md)

- 首轮建议：补缺失/null/空串/越界/类型/权限/大小的来源化候选；用真实约束判定拒绝、错误响应与无业务副作用，不自定状态码。
- 已改：逐字段抽取类型、必填、可空、范围、长度编码和大小约束，再提取身份/权限与错误合同，注明各自来源。；按缺失、null、空串、错误类型、边界外、超大小及无权限构造候选；有独立约束时一次只违背一项，组合错误单列。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-negative-testing/evals/cases/domain-method-control.yaml) — api-negative-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-negative-testing/evals/cases/domain-method-success.yaml) — api-negative-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 034. `api-pagination-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-pagination-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-pagination-testing/SKILL.md)

- 首轮建议：补稳定排序与唯一 tie-breaker、首末空页、无重无漏、cursor 失效/篡改及变更语义；用有序 ID fixture 检查跨页集合和 next cursor。
- 已改：提取页大小、offset/cursor、排序方向、唯一 tie-breaker、快照或实时变更合同、cursor 绑定/失效规则。；用同一数据快照排序出预期 ID 序列，切分首/中/末/空页；相同排序主键必须按给定 tie-breaker 判定。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-pagination-testing/evals/cases/domain-method-control.yaml) — api-pagination-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-pagination-testing/evals/cases/domain-method-success.yaml) — api-pagination-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 035. `api-rate-limit-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-rate-limit-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-rate-limit-testing/SKILL.md)

- 首轮建议：补 N-1/N/N+1、突发、窗口切换、用户/租户隔离和恢复；用时间序列 fixture 验证 429/Retry-After 及成功请求不误伤。
- 已改：提取算法、配额 N、窗口起止/时间源、突发额度、计数对象、用户/租户/路由作用域和重置规则。；按时间线构造 N-1/N/N+1、突发、窗口边界、不同主体及解除限流场景；对滑动窗口或 token bucket 按其合同重算，不套固定窗口。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-rate-limit-testing/evals/cases/domain-method-control.yaml) — api-rate-limit-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-rate-limit-testing/evals/cases/domain-method-success.yaml) — api-rate-limit-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 036. `api-schema-validation` (P1)

定位：[ZH](../../skills/zh/testing-types/api-schema-validation/SKILL.md) · [EN](../../skills/en/testing-types/api-schema-validation/SKILL.md)

- 首轮建议：先识别规范版本，检查 required/null、additionalProperties、组合 schema 和引用解析；用合法/非法样例做判定且不由样例反推完整契约。
- 已改：先确认 OpenAPI/JSON Schema/GraphQL 及具体版本或 dialect、operation/方向、内容类型、引用根与解析上下文；版本未知时暂停依赖版本的判断。；对 JSON Schema/OpenAPI 的 schema，分别核对 required 与 null、类型/范围、additionalProperties；按版本解释组合与引用，不混用 nullable。GraphQL 按其输入/输出类型和非空规则核对，不套用 JSON Schema 关键词。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-schema-validation/evals/cases/domain-method-control.yaml) — api-schema-validation: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-schema-validation/evals/cases/domain-method-success.yaml) — api-schema-validation: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 037. `api-security-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-security-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-security-testing/SKILL.md)

- 首轮建议：补 API 资产与主体-资源-动作关系、对象/字段/功能权限、资源消耗和服务端信任边界；用脱敏契约验证设计风险，保持静态边界。
- 已改：从已给 API 清单建立 endpoint、主体、资源、动作、敏感字段和信任边界表，标身份来自服务端还是可控请求。；按对象/字段/功能权限分别展开允许与拒绝对照，检查所有权、租户与委派；登录成功不代表有资源操作权限。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-security-testing/evals/cases/domain-method-control.yaml) — api-security-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-security-testing/evals/cases/domain-method-success.yaml) — api-security-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 038. `api-test-bruno` (P1)

定位：[ZH](../../skills/zh/testing-types/api-test-bruno/SKILL.md) · [EN](../../skills/en/testing-types/api-test-bruno/SKILL.md)

- 首轮建议：修正变量渲染、保留契约字段、未知断言显式待补；对生成工件做离线 golden 检查。
- 已改：Bruno 的源解析保留方法、URL、请求头/体及场景；生成断言要求有来源的预期，缺数据或复杂 schema 时显式失败为未完成脚手架，移除宽泛状态接受与固定样例。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/api-test-bruno/evals/cases/review-repair-regression.yaml) — api-test-bruno: sourced repair regression。
- 二次复查/验证：源→标准化 JSON→生成项目实际执行：good 通过，wrong-status/wrong-body 失败；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 039. `api-test-postman` (P2)

定位：[ZH](../../skills/zh/testing-types/api-test-postman/SKILL.md) · [EN](../../skills/en/testing-types/api-test-postman/SKILL.md)

- 首轮建议：补 Collection schema、变量作用域、登录 token 提取与 cleanup 工件 fixture；验证缺少预期时不会生成可误判为通过的断言。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-collection-auth-cleanup](../../skills/zh/testing-types/api-test-postman/evals/cases/review-collection-auth-cleanup.yaml) — Collection 授权作用域和清理具有可观察契约；[review-unknown-expectation](../../skills/zh/testing-types/api-test-postman/evals/cases/review-unknown-expectation.yaml) — 业务预期缺失不能生成总通过断言。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 040. `api-test-pytest` (P1)

定位：[ZH](../../skills/zh/testing-types/api-test-pytest/SKILL.md) · [EN](../../skills/en/testing-types/api-test-pytest/SKILL.md)

- 首轮建议：按真实响应契约生成断言、缺预期时阻断或标 scaffold；补空输入失败、错误响应和请求体保真用例。
- 已改：Pytest 的源解析保留方法、URL、请求头/体及场景；生成断言要求有来源的预期，缺数据或复杂 schema 时显式失败为未完成脚手架，移除宽泛状态接受与固定样例。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/api-test-pytest/evals/cases/review-repair-regression.yaml) — api-test-pytest: sourced repair regression。
- 二次复查/验证：源→标准化 JSON→生成项目实际执行：good 通过，wrong-status/wrong-body 失败；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 041. `api-test-restassure` (P1)

定位：[ZH](../../skills/zh/testing-types/api-test-restassure/SKILL.md) · [EN](../../skills/en/testing-types/api-test-restassure/SKILL.md)

- 首轮建议：改用来源化 status/body、项目性能阈值和非空检查；补生成类编译与错误响应应失败的本地验证。
- 已改：REST Assured 的源解析保留方法、URL、请求头/体及场景；生成断言要求有来源的预期，缺数据或复杂 schema 时显式失败为未完成脚手架，移除宽泛状态接受与固定样例。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/api-test-restassure/evals/cases/review-repair-regression.yaml) — api-test-restassure: sourced repair regression。
- 二次复查/验证：源→标准化 JSON→生成项目实际执行：good 通过，wrong-status/wrong-body 失败；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 042. `api-test-supertest` (P1)

定位：[ZH](../../skills/zh/testing-types/api-test-supertest/SKILL.md) · [EN](../../skills/en/testing-types/api-test-supertest/SKILL.md)

- 首轮建议：区分 app/baseUrl 运行模式、传递已知请求体与预期，增加实际失败能被捕获的工件 fixture。
- 已改：Supertest 的源解析保留方法、URL、请求头/体及场景；生成断言要求有来源的预期，缺数据或复杂 schema 时显式失败为未完成脚手架，移除宽泛状态接受与固定样例。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/api-test-supertest/evals/cases/review-repair-regression.yaml) — api-test-supertest: sourced repair regression。
- 二次复查/验证：源→标准化 JSON→生成项目实际执行：good 通过，wrong-status/wrong-body 失败；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 043. `api-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/api-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-testing/SKILL.md)

- 首轮建议：补 REST/GraphQL/gRPC/WebSocket/SOAP 的按需分支、跨请求业务后置条件与数据清理；用状态码正确但业务状态错误的例子验证设计质量。
- 已改：按已确认协议选择分支：REST 校验 method/status/schema/幂等；GraphQL 校验 data 与 errors、null 和字段权限；gRPC 校验 status/metadata/deadline/流终止；WebSocket 校验握手、消息 ID/顺序/重连；SOAP 校验 WSDL、namespace 与 Fault。未使用协议不强行覆盖。；将契约检查与跨请求业务后置条件分开：创建/更新→读回→权限视图→重复请求/下游效果；每步保留请求 ID、业务键、版本与证据。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/api-testing/evals/cases/domain-method-regression.yaml) — api-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 044. `api-version-compatibility-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/api-version-compatibility-testing/SKILL.md) · [EN](../../skills/en/testing-types/api-version-compatibility-testing/SKILL.md)

- 首轮建议：补 wire/schema/语义兼容、旧客户端读取容忍、默认值、错误码与弃用路径矩阵；用旧新客户端×旧新服务端 fixture 验证迁移风险。
- 已改：标出契约与客户端/服务端版本、支持/弃用时间线和迁移顺序，建立旧/新客户端×旧/新服务端的适用矩阵。；逐方向比较 wire 字段/类型、必需性、枚举、默认值、错误与语义单位；新增字段是否兼容取决于真实客户端读取容忍，不假设所有客户端忽略未知字段。
- 新案例：[domain-method-control](../../skills/zh/testing-types/api-version-compatibility-testing/evals/cases/domain-method-control.yaml) — api-version-compatibility-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/api-version-compatibility-testing/evals/cases/domain-method-success.yaml) — api-version-compatibility-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 045. `authentication-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/authentication-testing/SKILL.md) · [EN](../../skills/en/testing-types/authentication-testing/SKILL.md)

- 首轮建议：补凭证生命周期、MFA、账户枚举、锁定、恢复、重放和认证状态转移，明确与授权审查分界；用脱敏登录/恢复合同验证行为候选。
- 已改：根据已给密码、MFA、恢复或联邦机制建未认证/挑战中/已认证/锁定/恢复中的状态图，标创建、轮换、过期、撤销与重放规则。；逐机制构造有效/无效凭证、挑战未完成、MFA 重放、锁定边界和恢复令牌使用/过期候选；不自设尝试次数、有效期或 MFA 强制政策。
- 新案例：[domain-method-control](../../skills/zh/testing-types/authentication-testing/evals/cases/domain-method-control.yaml) — authentication-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/authentication-testing/evals/cases/domain-method-success.yaml) — authentication-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 046. `authorization-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/authorization-testing/SKILL.md) · [EN](../../skills/en/testing-types/authorization-testing/SKILL.md)

- 首轮建议：补角色/所有权/租户/委派矩阵、横纵越权、撤权和默认拒绝；用许可/拒绝成对 fixture 检查具体边界。
- 已改：提取主体角色、资源所有权、租户、动作、字段、委派范围/期限及撤权生效合同，建立允许/拒绝/未知矩阵。；对同资源换主体、同主体换资源/租户、低角色调用高权限动作分别构造横向/纵向边界及合法控制。
- 新案例：[domain-method-control](../../skills/zh/testing-types/authorization-testing/evals/cases/domain-method-control.yaml) — authorization-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/authorization-testing/evals/cases/domain-method-success.yaml) — authorization-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 047. `automation-roi-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/automation-roi-analysis/SKILL.md) · [EN](../../skills/en/testing-types/automation-roi-analysis/SKILL.md)

- 首轮建议：补建设/执行/维护成本的单位与时间窗、break-even、频率和变更率敏感性；用数值 fixture 验证结论方向，数据缺失不能给伪精确回报。
- 已改：固定候选、时间窗和单位；人工工时、自动执行占用、人工复核、维护工时与货币成本分开，换算必须有费率来源。；以同一时间窗计算净节省 = 次数×(人工单次成本−自动单次成本)−维护成本−建设成本；ROI 的分子/分母须明示，未有货币换算只报工时。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/automation-roi-analysis/evals/cases/domain-method-regression.yaml) — automation-roi-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 048. `automation-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/automation-testing/SKILL.md) · [EN](../../skills/en/testing-types/automation-testing/SKILL.md)

- 首轮建议：将选型/执行风险与 ROI 分开，增加投入门槛、隔离/清理、失败信号和回归后置条件；用已有 Playwright 项目的候选评分 fixture 验证“暂不自动化”理由。
- 已改：用 候选流程 | 保护义务 | 重复频率证据 | oracle/可观测性 | 数据隔离/清理 | 稳定性 | 维护约束 | 采用/延期理由 表选型；ROI 另列成本情景，不能抵消缺 oracle 或无授权环境。；优先沿用现有框架；先检查是否有可核对后置条件、可独立数据和可传播失败的 CI 入口，不满足者延期并写解除条件。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/automation-testing/evals/cases/domain-method-regression.yaml) — automation-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 049. `boundary-value-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/boundary-value-testing/SKILL.md) · [EN](../../skills/en/testing-types/boundary-value-testing/SKILL.md)

- 首轮建议：补包含/排除、最小可表示步长、长度编码、货币精度和时间单位规则；用已知 [0,100] fixture 验证边界与邻近值，未知精度保留缺口。
- 已改：抽取上下界、包含/排除、离散/连续类型、最小可表示步长、长度编码、货币精度、时间单位/时区及来源。；对已知离散边界选界内邻值、边界和界外邻值；整数步长 1 不能套到小数、字节长度或时间上。
- 新案例：[domain-method-control](../../skills/zh/testing-types/boundary-value-testing/evals/cases/domain-method-control.yaml) — boundary-value-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/boundary-value-testing/evals/cases/domain-method-success.yaml) — boundary-value-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 050. `bug-reporting` (P2)

定位：[ZH](../../skills/zh/testing-types/bug-reporting/SKILL.md) · [EN](../../skills/en/testing-types/bug-reporting/SKILL.md)

- 首轮建议：补期望来源、最小复现、脱敏证据与 severity/priority 分离断言；验证 1/3 频率不被改写成必现。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-expected-source-missing](../../skills/zh/testing-types/bug-reporting/evals/cases/review-expected-source-missing.yaml) — 缺预期来源不能虚构规则；[review-frequency-and-priority](../../skills/zh/testing-types/bug-reporting/evals/cases/review-frequency-and-priority.yaml) — 缺陷保留频率并区分 severity/priority。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 051. `business-rule-extraction` (P2)

定位：[ZH](../../skills/zh/testing-types/business-rule-extraction/SKILL.md) · [EN](../../skills/en/testing-types/business-rule-extraction/SKILL.md)

- 首轮建议：补带表格、例外优先级与互相矛盾文档的 fixture，验证规则条件/动作/作用域是否保真；用正确规则对照防止把缺失信息写成既定业务规则。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-complete-rule-control](../../skills/zh/testing-types/business-rule-extraction/evals/cases/review-complete-rule-control.yaml) — 完整规则不被默认政策改写；[review-table-exception-conflict](../../skills/zh/testing-types/business-rule-extraction/evals/cases/review-table-exception-conflict.yaml) — 原子规则保留表条件、例外和来源冲突。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 052. `capacity-planning-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/capacity-planning-analysis/SKILL.md) · [EN](../../skills/en/testing-types/capacity-planning-analysis/SKILL.md)

- 首轮建议：补吞吐-延迟-资源的来源链、扩容等待窗口与故障余量的可复算场景；明确不能用 CPU 55% 直接线性推算三倍容量，加入反例断言。
- 已改：对每个观测点记录环境/配置/实例数、负载 mix、到达/完成吞吐、延迟分位数、错误率、CPU/内存/队列和时窗；把测量→SLO→容量候选的来源链列出。；仅使用已测 SLO 可接受区间估计；CPU 百分比不能线性换算吞吐，未测点为候选，受下游、饱和与伸缩时延限制。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/capacity-planning-analysis/evals/cases/domain-method-regression.yaml) — capacity-planning-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 053. `change-impact-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/change-impact-analysis/SKILL.md) · [EN](../../skills/en/testing-types/change-impact-analysis/SKILL.md)

- 首轮建议：补 changed→dependent→obligation/test 的证据图与边界停止规则；用未知动态依赖 fixture 检查扩大验证范围，保持与 PR 专项的区分。
- 已改：固定变更版本及范围，输出 changed 文件/符号/配置→dependent→业务义务→test ID 的带类型证据图；每条边记录来源、版本与 confirmed/candidate/unknown。；遍历直接和传递消费者，去重循环；只有契约隔离或已证明无消费者边才可停止，记录停止依据，不能以目录边界截断。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/change-impact-analysis/evals/cases/domain-method-regression.yaml) — change-impact-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 054. `chaos-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/chaos-testing/SKILL.md) · [EN](../../skills/en/testing-types/chaos-testing/SKILL.md)

- 首轮建议：补稳态假设、控制组、注入点、爆炸半径、可量测停止条件和恢复证据；用未给停止条件的 fixture 强制保留阻塞。
- 已改：先把稳态假设写成指标、时间窗、基线/控制组与业务不变量，明确要验证的扰动因果链，而非仅列故障名称。；指定注入点、故障类型/持续时间、目标实例/流量比例、隔离环境、依赖与爆炸半径；列已授权范围和不触碰对象。
- 新案例：[domain-method-control](../../skills/zh/testing-types/chaos-testing/evals/cases/domain-method-control.yaml) — chaos-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/chaos-testing/evals/cases/domain-method-success.yaml) — chaos-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 055. `ci-test-optimization` (P2)

定位：[ZH](../../skills/zh/testing-types/ci-test-optimization/SKILL.md) · [EN](../../skills/en/testing-types/ci-test-optimization/SKILL.md)

- 首轮建议：补队列/安装/执行/重试时间分解、关键路径与缓存有效性；用 runner 时间序列 fixture 验证优化收益不由削弱测试或隐藏失败取得。
- 已改：以 commit/run/runner/config/test-set ID 固定比较对象；从事件时间线分解 queue、checkout/install、setup、execute、retry、report，区分端到端等待与 runner 忙时。；沿 DAG 计算实际关键路径，重叠 job 不相加；报告重试次数与失败原始结果，不能用重跑绿灯隐藏首失败。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ci-test-optimization/evals/cases/domain-method-regression.yaml) — ci-test-optimization: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 056. `circuit-breaker-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/circuit-breaker-testing/SKILL.md) · [EN](../../skills/en/testing-types/circuit-breaker-testing/SKILL.md)

- 首轮建议：补计数窗口、触发阈值、探测额度、恢复失败回退和并发探测状态表；以事件序列 fixture 校验转换与兜底，而不只检查 CBR 编号。
- 已改：提取失败计数口径、滚动/连续窗口、触发阈值、open 时限、half-open 探测额度/并发和成功/失败回退合同。；按时间和请求身份展开 closed→open→half-open→closed/open 的事件表，逐事件更新窗口与状态；没有阈值不能自行选择。
- 新案例：[domain-method-control](../../skills/zh/testing-types/circuit-breaker-testing/evals/cases/domain-method-control.yaml) — circuit-breaker-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/circuit-breaker-testing/evals/cases/domain-method-success.yaml) — circuit-breaker-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 057. `code-review` (P2)

定位：[ZH](../../skills/zh/testing-types/code-review/SKILL.md) · [EN](../../skills/en/testing-types/code-review/SKILL.md)

- 首轮建议：补正确 Patch 的无发现对照，以及语法看似危险但已有上游保护的反例；检验合规输入不会被机械报成缺陷。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-correct-patch-control](../../skills/zh/testing-types/code-review/evals/cases/review-correct-patch-control.yaml) — 等价正确 Patch 允许无发现；[review-reachable-null-defect](../../skills/zh/testing-types/code-review/evals/cases/review-reachable-null-defect.yaml) — 移除可达保护仍需定位实际缺陷；[review-upstream-guard-control](../../skills/zh/testing-types/code-review/evals/cases/review-upstream-guard-control.yaml) — 可见上游保护防止下标误报。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 058. `combinatorial-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/combinatorial-testing/SKILL.md) · [EN](../../skills/en/testing-types/combinatorial-testing/SKILL.md)

- 首轮建议：补 factor/value/约束建模、t-way 强度选择、合法组合过滤与覆盖核对；用小型可枚举 fixture 验证三因素交互。
- 已改：从材料建 factor/value 表及约束表达式，区分输入、环境与状态；未知值域不能补成任意二元值。；按缺陷或风险证据选择 t-way 强度，并说明高阶风险为何需要 t>=3；成对覆盖不能代替已知三因素义务。
- 新案例：[domain-method-control](../../skills/zh/testing-types/combinatorial-testing/evals/cases/domain-method-control.yaml) — combinatorial-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/combinatorial-testing/evals/cases/domain-method-success.yaml) — combinatorial-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 059. `cross-browser-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/cross-browser-testing/SKILL.md) · [EN](../../skills/en/testing-types/cross-browser-testing/SKILL.md)

- 首轮建议：补引擎×平台×版本矩阵与基于用户/风险的取样、真实设备和模拟证据区分；用 WebKit 专有差异 fixture 验证候选与支持声明的对应。
- 已改：把项目支持声明与用户分布映射为引擎×平台×版本×设备矩阵，记录真实浏览器、真实设备、模拟器和自动化引擎各自身份。；按高风险旅程、已知引擎差异和用户权重取样；同为 Chromium 的多款浏览器不能证明 WebKit/Gecko 的义务。
- 新案例：[domain-method-control](../../skills/zh/testing-types/cross-browser-testing/evals/cases/domain-method-control.yaml) — cross-browser-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/cross-browser-testing/evals/cases/domain-method-success.yaml) — cross-browser-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 060. `database-design-quality-review` (P2)

定位：[ZH](../../skills/zh/testing-types/database-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/database-design-quality-review/SKILL.md)

- 首轮建议：补在线迁移分阶段与混合版本共存 fixture，断言锁表、默认值、回滚和访问模式的证据链；正确 schema 不应被机械列满所有缺陷。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-online-mixed-version-migration](../../skills/zh/testing-types/database-design-quality-review/evals/cases/review-online-mixed-version-migration.yaml) — 在线迁移需说明混合版本、锁证据和回滚；[review-valid-schema-control](../../skills/zh/testing-types/database-design-quality-review/evals/cases/review-valid-schema-control.yaml) — 已有约束与访问路径不能误报缺失。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 061. `decision-table-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/decision-table-testing/SKILL.md) · [EN](../../skills/en/testing-types/decision-table-testing/SKILL.md)

- 首轮建议：补条件离散化、互斥/重叠/缺规则检查、don't-care 与规则优先级；用完整四组合 fixture 验证动作对应，未知优先级不能填造。
- 已改：将连续条件按来源规则离散为互斥区间/类别，列条件域、动作、例外和优先级；不把模糊条件直接填真/假。；枚举小模型的合法条件组合，与每条规则匹配；检查无匹配、多个冲突动作、互斥条件及不可达规则。
- 新案例：[domain-method-control](../../skills/zh/testing-types/decision-table-testing/evals/cases/domain-method-control.yaml) — decision-table-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/decision-table-testing/evals/cases/domain-method-success.yaml) — decision-table-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 062. `dependency-failure-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/dependency-failure-testing/SKILL.md) · [EN](../../skills/en/testing-types/dependency-failure-testing/SKILL.md)

- 首轮建议：补不可达/超时/慢响应/错误/部分成功的依赖故障矩阵，区分同步与异步；用调用方状态和副作用 fixture 验证隔离、降级与恢复。
- 已改：列调用方、依赖、同步/异步、超时/重试/降级合同，以及必须保持的数据和业务不变量。；分别建不可达、超时、慢响应、错误响应、部分成功矩阵；异步另列延迟、重复、乱序与消费确认，不能套同步状态码。
- 新案例：[domain-method-control](../../skills/zh/testing-types/dependency-failure-testing/evals/cases/domain-method-control.yaml) — dependency-failure-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/dependency-failure-testing/evals/cases/domain-method-success.yaml) — dependency-failure-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 063. `disaster-recovery-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/disaster-recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/disaster-recovery-testing/SKILL.md)

- 首轮建议：补跨区故障、备份可用性/时间点、依赖恢复顺序及恢复后业务一致性；用时间线 fixture 判断目标而非只写灾备建议。
- 已改：从灾备合同标主/备用区域、跨区故障范围、RTO/RPO 起止定义、可接受丢失和业务恢复标准，未知目标不得自设。；核对备份时间点、完整性/可解密/可恢复的既有证据及访问依赖；备份文件存在不证明可恢复。
- 新案例：[domain-method-control](../../skills/zh/testing-types/disaster-recovery-testing/evals/cases/domain-method-control.yaml) — disaster-recovery-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/disaster-recovery-testing/evals/cases/domain-method-success.yaml) — disaster-recovery-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 064. `distributed-trace-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/distributed-trace-analysis/SKILL.md) · [EN](../../skills/en/testing-types/distributed-trace-analysis/SKILL.md)

- 首轮建议：补 parent-child、异步 span/link、独占时间与排队时间核对步骤；用重叠 span 和缺 span fixture 防止相加总耗时或将最慢 span 直接写成根因。
- 已改：固定 trace/span ID、parent ID、异步 links、服务/部署版本、起止时刻和采样范围；核对父子包含关系与时钟偏差，link 不自动当同步父子。；同一时钟域内按区间并集扣除同步子 span 得 observed exclusive time；重叠子 span 不能相加。缺 span 时只报可见区间，不能宣称真实独占时间。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/distributed-trace-analysis/evals/cases/domain-method-regression.yaml) — distributed-trace-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 065. `edge-case-discovery` (P2)

定位：[ZH](../../skills/zh/testing-types/edge-case-discovery/SKILL.md) · [EN](../../skills/en/testing-types/edge-case-discovery/SKILL.md)

- 首轮建议：补字符/字节长度、时区切换、并发顺序的确定性 fixture，并要求候选回链到规则；正常例对照应避免无证据生成无限边界。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-bytes-time-order-boundaries](../../skills/zh/testing-types/edge-case-discovery/evals/cases/review-bytes-time-order-boundaries.yaml) — 边界候选保留单位、时区和事件顺序；[review-normal-boundary-control](../../skills/zh/testing-types/edge-case-discovery/evals/cases/review-normal-boundary-control.yaml) — 正常样例不应误判边界失败。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 066. `equivalence-partitioning` (P1)

定位：[ZH](../../skills/zh/testing-types/equivalence-partitioning/SKILL.md) · [EN](../../skills/en/testing-types/equivalence-partitioning/SKILL.md)

- 首轮建议：补按相同行为划分、互斥/完备检查、条件依赖与代表值选择；用地区×邮编 fixture 验证依赖类，不把所有无效输入混成一类。
- 已改：按相同行为/错误与约束来源划有效、无效和未知类，不仅按字段形状；响应不同的无效类不得合并。；检查类在给定域内互斥、完备，记录未分类值；条件依赖以地区×邮编、角色×动作等联合类表达。
- 新案例：[domain-method-control](../../skills/zh/testing-types/equivalence-partitioning/evals/cases/domain-method-control.yaml) — equivalence-partitioning: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/equivalence-partitioning/evals/cases/domain-method-success.yaml) — equivalence-partitioning: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 067. `error-handling-design-review` (P2)

定位：[ZH](../../skills/zh/testing-types/error-handling-design-review/SKILL.md) · [EN](../../skills/en/testing-types/error-handling-design-review/SKILL.md)

- 首轮建议：补可重试与不可重试错误、超时但副作用已提交的设计 fixture，验证消费者合同与补偿动作；同一失败不同层级要保留传播来源。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-reliable-error-control](../../skills/zh/testing-types/error-handling-design-review/evals/cases/review-reliable-error-control.yaml) — 已有受限重试控制不应误报缺失；[review-retry-partial-commit](../../skills/zh/testing-types/error-handling-design-review/evals/cases/review-retry-partial-commit.yaml) — 重试类别保留已提交事实与分层传播。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 068. `failover-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/failover-testing/SKILL.md) · [EN](../../skills/en/testing-types/failover-testing/SKILL.md)

- 首轮建议：补自动/手动触发、健康探测、流量转移、fencing、split-brain、RTO 和切回；用分区期间双写 fixture 验证一致性风险与恢复证据。
- 已改：提取主备角色、自动/手动触发、健康检测、流量转移、fencing/写权与切回合同，以及业务 RTO 定义。；用节点/网络分区时间线建立探测、选主、隔离旧主、路由及就绪阶段，记录每阶段谁可写和请求去向。
- 新案例：[domain-method-control](../../skills/zh/testing-types/failover-testing/evals/cases/domain-method-control.yaml) — failover-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/failover-testing/evals/cases/domain-method-success.yaml) — failover-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 069. `flaky-test-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/flaky-test-analysis/SKILL.md) · [EN](../../skills/en/testing-types/flaky-test-analysis/SKILL.md)

- 首轮建议：补带 seed/worker/运行数的失败记录 fixture，按比例和相关变量设计最小复现实验；断言 quarantine 有 owner/期限且不消失于质量报告。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-seed-worker-experiment](../../skills/zh/testing-types/flaky-test-analysis/evals/cases/review-seed-worker-experiment.yaml) — flaky 比例与最小实验保留隔离风险；[review-stable-control](../../skills/zh/testing-types/flaky-test-analysis/evals/cases/review-stable-control.yaml) — 小样本全通过不是 flaky 或零风险证明。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 070. `functional-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/functional-testing/SKILL.md) · [EN](../../skills/en/testing-types/functional-testing/SKILL.md)

- 首轮建议：优先修格式保真；内容再补“动作→业务后置条件”fixture，验证支付状态而不只验证页面提示。
- 已改：补响应成功但持久化业务状态错误的用例及合法对照；逐项检查业务后置条件、执行证据与信息缺口，追加而不覆盖已有 eval。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/functional-testing/evals/cases/review-repair-regression.yaml) — functional-testing: sourced repair regression。
- 二次复查/验证：契约或路由正反 fixture/grader 控制通过；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 071. `llm-consistency-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/llm-consistency-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-consistency-testing/SKILL.md)

- 首轮建议：补 seed/temperature/版本控制、结构不变量与语义允许差异的分层比较；用多次输出 fixture 验证方差与偶发失败，明确无重复数据时不能证明稳定性。
- 已改：固定样本 ID、模型/Prompt/工具/数据版本、temperature、seed（仅供应商支持时）和其他采样参数，记录项目指定重复次数；seed 相同不代表跨版本可复现。；先比 schema、必需字段、允许枚举和政策等结构不变量，再依据项目 rubric 比语义结论；同义表达或获准顺序变化不应报错。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/llm-consistency-testing/evals/cases/domain-method-regression.yaml) — llm-consistency-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 072. `llm-evaluation-design` (P2)

定位：[ZH](../../skills/zh/testing-types/llm-evaluation-design/SKILL.md) · [EN](../../skills/en/testing-types/llm-evaluation-design/SKILL.md)

- 首轮建议：补 rubric 锚点、人工分歧、盲评顺序和 train/test 污染的 fixture；要求输出可执行数据分层和 judge 校准步骤，非通用章节即通过。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-contamination-and-calibration](../../skills/zh/testing-types/llm-evaluation-design/evals/cases/review-contamination-and-calibration.yaml) — 评测设计处理污染和 judge 分歧；[review-disjoint-design-control](../../skills/zh/testing-types/llm-evaluation-design/evals/cases/review-disjoint-design-control.yaml) — 分层独立且有校准锚点时不编造泄漏。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 073. `llm-hallucination-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/llm-hallucination-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-hallucination-testing/SKILL.md)

- 首轮建议：补支持/矛盾/来源缺失/不可判的标签定义，拆解数值、实体与引用；用一个混合支持和虚构条款的答案 fixture 校验逐声明映射。
- 已改：拆出独立可核对声明，包括数字/单位、实体、条件、时间和引用；为声明编号并保留答案原文、证据库版本和来源位置。；标签定义：SUPPORTED 有相同范围的证据支持；CONTRADICTED 被证据明确反驳；MISSING_SOURCE 提供材料未支持且没有直接反证；UNASSESSABLE 因来源不可访问、范围/时效不明而不能比对。缺来源不等同已证明虚构。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/llm-hallucination-testing/evals/cases/domain-method-regression.yaml) — llm-hallucination-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 074. `llm-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/llm-testing/SKILL.md) · [EN](../../skills/en/testing-types/llm-testing/SKILL.md)

- 首轮建议：补真实输入/输出样本与结构 parser、校准语义 rubric；以多运行重复试验检查鲁棒性和长上下文遗失。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-equivalent-safe-control](../../skills/zh/testing-types/llm-testing/evals/cases/review-equivalent-safe-control.yaml) — 等价事实改写不能当退化；[review-repeated-output-samples](../../skills/zh/testing-types/llm-testing/evals/cases/review-repeated-output-samples.yaml) — LLM 样本区分 parser 与校准语义失败。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 075. `log-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/log-analysis/SKILL.md) · [EN](../../skills/en/testing-types/log-analysis/SKILL.md)

- 首轮建议：成功案例没有实际日志。补脱敏原始日志与已知部署时间，验证排序、请求关联、异常聚类和缺失段；要求假设对应最小验证动作。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-normal-log-control](../../skills/zh/testing-types/log-analysis/evals/cases/review-normal-log-control.yaml) — 正常日志样本不能编造事故或整体健康；[review-raw-log-timeline](../../skills/zh/testing-types/log-analysis/evals/cases/review-raw-log-timeline.yaml) — 原始日志保留 UTC 顺序、请求关联与缺失段。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 076. `manual-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/manual-testing/SKILL.md) · [EN](../../skills/en/testing-types/manual-testing/SKILL.md)

- 首轮建议：补时间盒 charter、数据恢复、记录模板和未完成项状态；用短窗口 fixture 检查执行路径具体且有证据，不把检查清单写成执行完成。
- 已改：为每个时间盒建立 charter：任务/风险、环境/构建、数据、探索范围、截止和证据；执行既定路径与探索新问题分别记账，不自行扩展授权。；步骤记录 前置状态→动作→预期→实际→证据 ID→状态；未启动为 NOT_RUN，中断为 INCOMPLETE，环境阻断为 BLOCKED，不把清单当完成记录。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/manual-testing/evals/cases/domain-method-regression.yaml) — manual-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 077. `metamorphic-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/metamorphic-testing/SKILL.md) · [EN](../../skills/en/testing-types/metamorphic-testing/SKILL.md)

- 首轮建议：补源输入/变换/输出关系/适用前提/反例，明确不能自行假设等价性；用排序置换与重复元素 fixture 检验关系。
- 已改：先确定原始输入域、变换 T、输出关系 R 及其来源/适用前提；没有可靠 oracle 不代表可以自行假设任意等价关系。；对源输入及变换后输入检查约束，标会改变语义的变换；输出相等、比例关系或单调关系需分别说明。
- 新案例：[domain-method-control](../../skills/zh/testing-types/metamorphic-testing/evals/cases/domain-method-control.yaml) — metamorphic-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/metamorphic-testing/evals/cases/domain-method-success.yaml) — metamorphic-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 078. `metrics-anomaly-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/metrics-anomaly-analysis/SKILL.md) · [EN](../../skills/en/testing-types/metrics-anomaly-analysis/SKILL.md)

- 首轮建议：成功案例未提供原始序列。补单位/采样/缺失值/季节性序列，验证基线窗口、维度拆分与相关性不冒充因果；没有基线保持不可判。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-seasonal-control-and-no-baseline](../../skills/zh/testing-types/metrics-anomaly-analysis/evals/cases/review-seasonal-control-and-no-baseline.yaml) — 季节峰值不是偏离且无基线保持未知；[review-unit-seasonal-missing-series](../../skills/zh/testing-types/metrics-anomaly-analysis/evals/cases/review-unit-seasonal-missing-series.yaml) — 指标异常使用给定基线与缺值语义。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 079. `mobile-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/mobile-testing/SKILL.md) · [EN](../../skills/en/testing-types/mobile-testing/SKILL.md)

- 首轮建议：补 OS×设备×升级路径×网络/前后台的风险选取和状态恢复判据；用 deeplink 丢参、支付中断 fixture 验证持久化状态与原始参数保真。
- 已改：用生产分布、变化和事故证据选 OS×设备×安装/升级路径×网络×前后台 的风险矩阵，注明样本与未覆盖组合，不能臆造支持列表。；deeplink 保留原始 URI、解码规则、路由/参数与授权状态；比较冷启动、热启动和恢复，参数不能在恢复后丢失或二次解码。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/mobile-testing/evals/cases/domain-method-regression.yaml) — mobile-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 080. `mock-quality-review` (P1)

定位：[ZH](../../skills/zh/testing-types/mock-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/mock-quality-review/SKILL.md)

- 首轮建议：补真实契约与 stub 的字段/状态/时序差异、被测对象是否被替换、错误路径及漂移检查；用正确边界 mock 与 mock 掉被测对象的对照验证误报。
- 已改：先标被测对象与外部协作者边界，将 mock/stub 的版本、字段、状态码、错误、时序和副作用与真实合同逐项对应。；检查是否替换了被测逻辑本身、断言是否只验证 stub 输出或固定交互；正确边界 mock 不因使用 mock 就成为缺陷。
- 新案例：[domain-method-control](../../skills/zh/testing-types/mock-quality-review/evals/cases/domain-method-control.yaml) — mock-quality-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/mock-quality-review/evals/cases/domain-method-success.yaml) — mock-quality-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 081. `model-based-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/model-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/model-based-testing/SKILL.md)

- 首轮建议：补初始/终止状态、guard、事件、动作、可达性和状态/边覆盖目标；用小型状态图 fixture 验证实际路径和不可达分支。
- 已改：从来源建立初始/终止状态、事件、guard、动作、目标及持久化模型，明确是行为模型而非随意列状态。；从初始状态做可达性遍历，列不可达状态/边、冲突转移和未定义事件；guard 无法满足时保留理由。
- 新案例：[domain-method-control](../../skills/zh/testing-types/model-based-testing/evals/cases/domain-method-control.yaml) — model-based-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/model-based-testing/evals/cases/domain-method-success.yaml) — model-based-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 082. `multi-agent-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/multi-agent-testing/SKILL.md) · [EN](../../skills/en/testing-types/multi-agent-testing/SKILL.md)

- 首轮建议：补委派消息 ID、任务所有权、共享状态版本、交接确认与故障终止协议；用部分失败、双重认领和陈旧消息 trace 验证无丢任务/重复副作用。
- 已改：用 task/message/correlation ID、sender/receiver、父委派、scope、owner、共享状态版本和 ACK 建立交接轨迹；按真实协议指定接收/拒绝/终止条件。；认领/提交须依据项目原子所有权或fencing协议，陈旧消息与重复消息不能重新取得所有权或重复写入；未给 exactly-once 协议不假定存在。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/multi-agent-testing/evals/cases/domain-method-regression.yaml) — multi-agent-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 083. `mutation-testing-analysis` (P1)

定位：[ZH](../../skills/zh/testing-types/mutation-testing-analysis/SKILL.md) · [EN](../../skills/en/testing-types/mutation-testing-analysis/SKILL.md)

- 首轮建议：补 killed/survived/no-coverage/timeout/error/等价待判，保留算子与测试映射；用小型结果 fixture 复算分母，不能把等价待判自动排除。
- 已改：核对被测版本、算子、mutant ID、位置、测试映射和运行预算，将 killed/survived/no-coverage/timeout/error/等价待判分别归类。；先读取工具/项目评分公式和排除政策，列总数、分子、分母及排除理由；公式未给则报告分布而不创造唯一总分。
- 新案例：[domain-method-control](../../skills/zh/testing-types/mutation-testing-analysis/evals/cases/domain-method-control.yaml) — mutation-testing-analysis: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/mutation-testing-analysis/evals/cases/domain-method-success.yaml) — mutation-testing-analysis: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 084. `negative-scenario-discovery` (P2)

定位：[ZH](../../skills/zh/testing-types/negative-scenario-discovery/SKILL.md) · [EN](../../skills/en/testing-types/negative-scenario-discovery/SKILL.md)

- 首轮建议：补超时但已成功、双重失败和恢复失败 fixture，要求每个候选有拒绝/恢复/数据一致性预期，不把未知合同补成固定错误码。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-partial-double-recovery-failures](../../skills/zh/testing-types/negative-scenario-discovery/evals/cases/review-partial-double-recovery-failures.yaml) — 异常路径保留结果未知与恢复一致性预期；[review-rejected-invalid-control](../../skills/zh/testing-types/negative-scenario-discovery/evals/cases/review-rejected-invalid-control.yaml) — 安全拒绝不能编造恢复缺陷。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 085. `observability-design-review` (P2)

定位：[ZH](../../skills/zh/testing-types/observability-design-review/SKILL.md) · [EN](../../skills/en/testing-types/observability-design-review/SKILL.md)

- 首轮建议：补高基数标签与采样后断链的设计 fixture；断言记录预算/关联方式与告警动作，不能仅出现“采样”就通过。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-bounded-signal-control](../../skills/zh/testing-types/observability-design-review/evals/cases/review-bounded-signal-control.yaml) — 明确基数与传播控制需被识别；[review-cardinality-and-broken-sampling](../../skills/zh/testing-types/observability-design-review/evals/cases/review-cardinality-and-broken-sampling.yaml) — 信号设计关联预算、链路与告警行动。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 086. `pairwise-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/pairwise-testing/SKILL.md) · [EN](../../skills/en/testing-types/pairwise-testing/SKILL.md)

- 首轮建议：补合法 pair universe、约束过滤与覆盖缺口表，明示 pairwise 不能保护高阶交互；用可枚举因素 fixture 复核所有合法 pairs。
- 已改：列来源化因素、值域与联合约束，确定 pairwise 适用风险及不覆盖的三阶以上义务。；枚举/求解合法全组合，再投影每两因素的合法 pair universe；不能仅删除显然非法 pairs，需确认可扩展为合法全组合。
- 新案例：[domain-method-control](../../skills/zh/testing-types/pairwise-testing/evals/cases/domain-method-control.yaml) — pairwise-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/pairwise-testing/evals/cases/domain-method-success.yaml) — pairwise-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 087. `performance-bottleneck-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-bottleneck-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-bottleneck-analysis/SKILL.md)

- 首轮建议：补阶段化 RPS/排队/CPU/连接池 fixture，让 judge 检查瓶颈假设及最小区分实验；高 CPU 或单一慢 span 不能直接作为根因。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-high-cpu-slow-span-control](../../skills/zh/testing-types/performance-bottleneck-analysis/evals/cases/review-high-cpu-slow-span-control.yaml) — 高 CPU 或单慢 span 不足以确定瓶颈；[review-stage-pool-hypothesis](../../skills/zh/testing-types/performance-bottleneck-analysis/evals/cases/review-stage-pool-hypothesis.yaml) — 吞吐拐点与排队证据指导区分实验。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 088. `performance-regression-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-regression-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-regression-analysis/SKILL.md)

- 首轮建议：补配对多运行数据，验证绝对/相对变化与不可比状态，分别报告噪声和稳定退化。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-incomparable-load-control](../../skills/zh/testing-types/performance-regression-analysis/evals/cases/review-incomparable-load-control.yaml) — 负载与环境不同阻断版本退化归因；[review-paired-deltas](../../skills/zh/testing-types/performance-regression-analysis/evals/cases/review-paired-deltas.yaml) — 配对重复区分一致变化和零中位数波动。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 089. `performance-result-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-result-analysis/SKILL.md) · [EN](../../skills/en/testing-types/performance-result-analysis/SKILL.md)

- 首轮建议：补实际阶段报告及目标，验证达到负载、样本、错误分母与阶段稳态；结果只能支持给定环境负载。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-met-target-control](../../skills/zh/testing-types/performance-result-analysis/evals/cases/review-met-target-control.yaml) — 有效稳态结果可通过明确局部门槛；[review-stage-targets-and-denominator](../../skills/zh/testing-types/performance-result-analysis/evals/cases/review-stage-targets-and-denominator.yaml) — 实际阶段结果核对达到负载和错误分母。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 090. `performance-test-gatling` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-test-gatling/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-gatling/SKILL.md)

- 首轮建议：补开放/封闭注入模型与目标 RPS 的验证、断言 API 与 DSL/版本基线；离线编译生成 Simulation，测试数据 feeder 耗尽和缺阈值路径。
- 已改：先读取项目 Gatling/插件/JDK 与 Java/Scala/Kotlin DSL 版本，沿用已有布局；选定同一 DSL 的 injection 与 assertion API，不能混用。生成资产先用项目构建的离线 test-compile 验证，依赖未缓存则标 BLOCKED 而非编译通过。；开放模型控制用户到达率，只有每用户单请求且无额外循环/重试时才与目标 RPS 一一对应；封闭模型控制并发，RPS 要从实际请求数/时窗核对。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/performance-test-gatling/evals/cases/domain-method-regression.yaml) — performance-test-gatling: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 091. `performance-test-jmeter` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-test-jmeter/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-jmeter/SKILL.md)

- 首轮建议：补脱敏 JMX fixture 和非 GUI 结构校验，验证 CSV 生命周期和错误/时延门槛。
- 已改：确认项目 JMeter/JDK/插件与 JMX版本，逐个核对 TestPlan/ThreadGroup/Sampler 与相邻 hashTree、变量和属性；XML可解析只证明结构，不等于JMeter可执行或SLO通过。；标准ThreadGroup控制闭环线程数；目标RPS需明确think time/timer、吞吐控制器或已安装到达率插件，记录实际吞吐和请求数，不能从线程数直接推出RPS。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/performance-test-jmeter/evals/cases/domain-method-regression.yaml) — performance-test-jmeter: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 092. `performance-test-k6` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-test-k6/SKILL.md) · [EN](../../skills/en/testing-types/performance-test-k6/SKILL.md)

- 首轮建议：补 arrival-rate/closed-model 的选择、dropped_iterations 与 check/threshold 区分；对脚本做离线结构核对，补契约 body 和业务 postcondition 而非仅 HTTP 成功。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-closed-model-control](../../skills/zh/testing-types/performance-test-k6/evals/cases/review-closed-model-control.yaml) — 固定用户负载不强制改到达速率模型；[review-offline-arrival-artifacts](../../skills/zh/testing-types/performance-test-k6/evals/cases/review-offline-arrival-artifacts.yaml) — 离线 k6 产物保留负载达到与业务断言。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 093. `performance-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/performance-testing/SKILL.md) · [EN](../../skills/en/testing-types/performance-testing/SKILL.md)

- 首轮建议：先修解析；再用实际 achieved RPS、资源和错误分母 fixture 验证负载有效性，不把目标 RPS 当已达到。
- 已改：补实际达成负载、尝试数与完成数分母的对照；未执行和未达目标不能升级为性能通过，项目门槛保持来自输入。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/performance-testing/evals/cases/review-repair-regression.yaml) — performance-testing: sourced repair regression。
- 二次复查/验证：契约或路由正反 fixture/grader 控制通过；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 094. `performance-workload-modeling` (P2)

定位：[ZH](../../skills/zh/testing-types/performance-workload-modeling/SKILL.md) · [EN](../../skills/en/testing-types/performance-workload-modeling/SKILL.md)

- 首轮建议：补输入单位、时窗、交易 mix 和会话转换的可复算例；60 万日请求不能直接推出峰值 RPS，缺峰时宽度时给条件化区间而非自定。
- 已改：将每项输入写为数值、单位、时区/窗口、来源和覆盖：请求/交易/会话/用户不能互换；从交易mix及每交易请求数转换，注明重试与后台流量。；日请求量只能复算全天平均；峰值需峰时流量比例与窗口宽度，缺窗口保持条件公式/区间，不自定峰时长度或峰倍数。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/performance-workload-modeling/evals/cases/domain-method-regression.yaml) — performance-workload-modeling: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 095. `pr-test-impact-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/pr-test-impact-analysis/SKILL.md) · [EN](../../skills/en/testing-types/pr-test-impact-analysis/SKILL.md)

- 首轮建议：补 base/head、文件/符号/依赖与 test ID 的映射表、删除测试影响、未知映射保守回退；用共享金额类型 diff 验证传递范围。
- 已改：固定repo/base/head SHA与diff范围；为文件、符号、schema/config变化列来源，不按文件名猜影响或将不同HEAD的测试结果合并。；输出变化符号→直接/传递消费者→保护义务→test ID/层级/执行版本的映射表，边标confirmed/candidate/unknown；只在有证据的隔离边界停止。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/pr-test-impact-analysis/evals/cases/domain-method-regression.yaml) — pr-test-impact-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 096. `production-incident-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/production-incident-analysis/SKILL.md) · [EN](../../skills/en/testing-types/production-incident-analysis/SKILL.md)

- 首轮建议：补有时间戳的事故记录、并发变更与缓解结果 fixture，分开症状/关联/根因/验证；明确建议动作、实际动作和已批准动作的状态。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-concurrent-changes-actions](../../skills/zh/testing-types/production-incident-analysis/evals/cases/review-concurrent-changes-actions.yaml) — 事故时间线区分观察、批准与因果；[review-correlation-only-control](../../skills/zh/testing-types/production-incident-analysis/evals/cases/review-correlation-only-control.yaml) — 相邻部署单独不能确定事故根因。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 097. `production-verification` (P2)

定位：[ZH](../../skills/zh/testing-types/production-verification/SKILL.md) · [EN](../../skills/en/testing-types/production-verification/SKILL.md)

- 首轮建议：补只读模式、批准写操作清单、canary 阈值与清理失败 fixture；没有原始运行结果时报告计划/待验证，保持每步副作用可追踪。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-approved-write-cleanup-failure](../../skills/zh/testing-types/production-verification/evals/cases/review-approved-write-cleanup-failure.yaml) — 批准的合成写入不能隐去清理失败；[review-read-only-plan](../../skills/zh/testing-types/production-verification/evals/cases/review-read-only-plan.yaml) — 只读授权且无原结果只能交付计划。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 098. `prompt-injection-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/prompt-injection-testing/SKILL.md) · [EN](../../skills/en/testing-types/prompt-injection-testing/SKILL.md)

- 首轮建议：补含安全 canary 的不可信文档、工具调用 trace 和正常文档对照，分别验证信任边界与零未授权调用。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-canary-tool-traces](../../skills/zh/testing-types/prompt-injection-testing/evals/cases/review-canary-tool-traces.yaml) — 拒绝文本不能掩盖未授权 canary 调用。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 099. `prompt-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/prompt-testing/SKILL.md) · [EN](../../skills/en/testing-types/prompt-testing/SKILL.md)

- 首轮建议：补配对 before/after 输出、Prompt/模型/数据身份与等价改写正例；结构用 parser，语义 rubric 校准，验证不能以表面词差或单次结果认定退化。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-changed-model-control](../../skills/zh/testing-types/prompt-testing/evals/cases/review-changed-model-control.yaml) — Prompt 归因需相同模型和数据身份；[review-paired-parser-semantic](../../skills/zh/testing-types/prompt-testing/evals/cases/review-paired-parser-semantic.yaml) — 配对 Prompt 输出使用 parser 和校准语义锚点。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 100. `property-based-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/property-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/property-based-testing/SKILL.md)

- 首轮建议：补输入域、来源化不变量、前置限制、随机 seed、shrinking 和最小反例；用排序 fixture 校验输出有序且保持元素多重集。
- 已改：从合同列输入域、来源化不变量、前置限制及可观察 oracle；性质不能由函数名或个人常识自行断定。；设计满足约束的生成域和关键分布（空/重复/极值等仅在允许时），记录 seed、生成器版本、样本与失败输入以便重放。
- 新案例：[domain-method-control](../../skills/zh/testing-types/property-based-testing/evals/cases/domain-method-control.yaml) — property-based-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/property-based-testing/evals/cases/domain-method-success.yaml) — property-based-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 101. `quality-dashboard-design` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-dashboard-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-dashboard-design/SKILL.md)

- 首轮建议：补决策问题→指标→口径→来源→行动的面板映射，空值/过期/未执行与零值分开；用过期绿灯和少数 P0 fixture 检验仪表盘不会掩盖阻塞。
- 已改：按受众决策建立 问题→指标→口径/时窗→数据来源/版本→可采取行动→责任人 面板映射，不从易取数据倒推决策。；展示值的分子分母、最后刷新时间与来源状态；0、null、NOT_RUN、BLOCKED、过期值分别呈现，禁止缺值补0或沿用过期绿灯。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-dashboard-design/evals/cases/domain-method-regression.yaml) — quality-dashboard-design: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 102. `quality-debt-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-debt-analysis/SKILL.md) · [EN](../../skills/en/testing-types/quality-debt-analysis/SKILL.md)

- 首轮建议：补债务与未修产品缺陷的分类、风险利息和偿还完成证据；用高龄低风险和新生高风险对照校验排序不由年龄单项决定。
- 已改：将已存在产品缺陷、测试/架构债务、暂时例外与数据缺口分列；每条记录来源、当前影响、形成原因、年龄和已有控制，不把所有未完成项叫债务。；估计风险利息时说明变化路径：后续修改成本、故障暴露、检测延迟等可观察证据；没有费率/频率只给定性或条件范围，不自造金额。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-debt-analysis/evals/cases/domain-method-regression.yaml) — quality-debt-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 103. `quality-gate-design` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-gate-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-gate-design/SKILL.md)

- 首轮建议：补 PASS/FAIL/BLOCKED/UNKNOWN 真值表、证据过期、例外授权人/期限与 fail-closed 条件；用缺失测试记录 fixture 验证不能默认为通过。
- 已改：为每个门槛记录义务、输入/版本/时效、比较符、PASS/FAIL、不可执行BLOCKED、缺证据或无法判断UNKNOWN的真值表；没有记录不得视为PASS。；聚合规则由项目指定：必要门槛FAIL优先，无法验证按fail-closed停止；UNKNOWN/BLOCKED保持原因而不是折算失败率。所有必要门槛有新鲜有效PASS才可推荐通过。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-gate-design/evals/cases/domain-method-regression.yaml) — quality-gate-design: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 104. `quality-maturity-assessment` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-maturity-assessment/SKILL.md) · [EN](../../skills/en/testing-types/quality-maturity-assessment/SKILL.md)

- 首轮建议：补每维度可观察实践/工件/成熟等级示例与不适用、未知处理；不另造仓库 Quality Score，用成对团队证据 fixture 校准。
- 已改：先固定项目成熟度框架、维度、锚点与适用范围；若没有框架，只给证据清单与候选锚点，不能擅自发布组织分级或仓库Quality Score。；每级锚点至少包含可观察实践、工件及持续性证据：例如“有模板”只证明工件存在，“重复执行且有失败处置记录”才能支持执行实践；示例级别必须标为示例。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-maturity-assessment/evals/cases/domain-method-regression.yaml) — quality-maturity-assessment: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 105. `quality-metrics-design` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-metrics-design/SKILL.md) · [EN](../../skills/en/testing-types/quality-metrics-design/SKILL.md)

- 首轮建议：补口径字典、时窗、样本排除、去重、缺失与 lineage；用重开缺陷/重复运行 fixture 复算，区分测量问题与质量问题。
- 已改：建立指标字典：决策目的、统计单位、分子/分母、时窗/时区、筛选/去重、缺失处理、版本、来源与lineage；率的分母不能隐式变化。；区分缺陷实体与状态事件、首次执行与重跑、关闭与重开；按项目唯一键和事件时间聚合，避免把重复ID/重开计成新缺陷或重试冲高通过率。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-metrics-design/evals/cases/domain-method-regression.yaml) — quality-metrics-design: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 106. `quality-productivity-metrics` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-productivity-metrics/SKILL.md) · [EN](../../skills/en/testing-types/quality-productivity-metrics/SKILL.md)

- 首轮建议：补投入/产出/质量/流程的平衡视图、工作复杂度与统计单位，验证跨团队不可直接排名；用例数量上升但逃逸增加的反例检验结论。
- 已改：将投入工时/成本、可验收产出、质量缺陷/逃逸、流程等待/返工放在平衡视图，明确窗口、团队/任务统计单位、复杂度与产品风险。；去重拆分/合并用例并核对验收，不以用例/commit数量代替价值；质量和返工下降证据缺失时不宣称生产率改善。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-productivity-metrics/evals/cases/domain-method-regression.yaml) — quality-productivity-metrics: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 107. `quality-risk-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/quality-risk-analysis/SKILL.md) · [EN](../../skills/en/testing-types/quality-risk-analysis/SKILL.md)

- 首轮建议：补可观察的影响/可能性/可探测性锚点及不确定性传播；用资损低频风险与高频轻微问题对照，验证排序不被无依据数值乘积支配。
- 已改：从风险事件、受影响资产/人群、触发和当前控制建立登记表；影响、可能性、可探测性各给可观察证据锚点与来源，不凭印象填分。；项目未指定量化规则时用有理由的定性排序；重大不可逆影响、授权边界与已知控制缺口单列，低频不自动降为低风险。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/quality-risk-analysis/evals/cases/domain-method-regression.yaml) — quality-risk-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 108. `rag-quality-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/rag-quality-testing/SKILL.md) · [EN](../../skills/en/testing-types/rag-quality-testing/SKILL.md)

- 首轮建议：补 query→retrieved chunks→claims→citations 对齐表、完整性与拒答 separate rubric；用有引用却不支持答案的 fixture 验证逐声明证据。
- 已改：固定query/sample ID、知识库/索引/检索/模型/Prompt版本；建立query→检索chunk ID/版本→原子声明→引用位置→支持/矛盾/缺失映射，不以有引用判断grounding。；引用准确性、声明支持与答案完整性分别评：遗漏必需条件即使已有声明全支持也可能不完整；按用户任务和项目rubric判。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/rag-quality-testing/evals/cases/domain-method-regression.yaml) — rag-quality-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 109. `rag-retrieval-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/rag-retrieval-testing/SKILL.md) · [EN](../../skills/en/testing-types/rag-retrieval-testing/SKILL.md)

- 首轮建议：补 top-k、过滤/租户权限、新鲜度和排序对照；用已知相关文档集 fixture 区分检索失败、生成失败及代理指标限制。
- 已改：给query及相关集合固定标注规则、文档/chunk粒度、标注者与版本；Recall@k分母为已知相关集合，Precision@k按实际返回数和项目对重复chunk规则计算。；逐结果核对top-k/rank、relevance、租户/权限过滤、新鲜度与文档版本；越权结果不能因相关而计成功，过时结果不由分数高抵消。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/rag-retrieval-testing/evals/cases/domain-method-regression.yaml) — rag-retrieval-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 110. `recovery-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/recovery-testing/SKILL.md) · [EN](../../skills/en/testing-types/recovery-testing/SKILL.md)

- 首轮建议：补服务恢复/数据恢复区别、RTO/RPO 起止、恢复点、一致性和业务补偿；用恢复时间线/数据快照 fixture 验证目标。
- 已改：分开服务重启/就绪、数据恢复点和业务一致性，提取 RTO/RPO 定义、故障起点、业务恢复终点及可接受丢失。；连接故障、备份/日志、恢复过程、依赖就绪与业务验证时间线；健康探测成功不自动结束业务 RTO。
- 新案例：[domain-method-control](../../skills/zh/testing-types/recovery-testing/evals/cases/domain-method-control.yaml) — recovery-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/recovery-testing/evals/cases/domain-method-success.yaml) — recovery-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 111. `regression-optimization` (P2)

定位：[ZH](../../skills/zh/testing-types/regression-optimization/SKILL.md) · [EN](../../skills/en/testing-types/regression-optimization/SKILL.md)

- 首轮建议：补风险保护约束、耗时收益与漏检风险的 before/after 可比口径；用删高风险用例可变快的反例验证优化不能以丢保护换收益。
- 已改：固定before/after变更版本、环境、测试义务集合、数据和窗口；列选择/排序/并行/缓存候选的纳入与排除证据，不比较不同规模总时长。；将关键风险/已知逃逸/必须门禁作为保护约束；删去唯一保护的提速不得采纳，未知映射保留保守验证或升级。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/regression-optimization/evals/cases/domain-method-regression.yaml) — regression-optimization: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 112. `regression-scope-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/regression-scope-analysis/SKILL.md) · [EN](../../skills/en/testing-types/regression-scope-analysis/SKILL.md)

- 首轮建议：补“变更→受影响义务→测试层/平台→包含或排除理由”的矩阵，并保留未知依赖；用间接依赖和预算不足 fixture 验证补充范围与升级条件。
- 已改：以变更和当前基线为入口，列变更→受影响义务→测试层/平台/数据状态→纳入/排除及证据的矩阵；回归保护已有行为，不把新特性完整测试混为回归。；检查直接、传递与动态依赖、历史逃逸和非功能影响；未知依赖单列，不以无映射当无影响，排除需契约/证据证明。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/regression-scope-analysis/evals/cases/domain-method-regression.yaml) — regression-scope-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 113. `regression-test-selection` (P2)

定位：[ZH](../../skills/zh/testing-types/regression-test-selection/SKILL.md) · [EN](../../skills/en/testing-types/regression-test-selection/SKILL.md)

- 首轮建议：提供带 ID、时长、依赖与风险映射的用例 fixture；核对选择集合、强制项和预算不可满足分支，不能只输出选择原则。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-mandatory-budget-infeasible](../../skills/zh/testing-types/regression-test-selection/evals/cases/review-mandatory-budget-infeasible.yaml) — 强制集合预算不足必须显式暴露；[review-risk-mapped-selection](../../skills/zh/testing-types/regression-test-selection/evals/cases/review-risk-mapped-selection.yaml) — 选择集合保留强制依赖与预算。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 114. `reliability-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/reliability-testing/SKILL.md) · [EN](../../skills/en/testing-types/reliability-testing/SKILL.md)

- 首轮建议：补 SLI 定义、观测窗口、失败计数口径、重复故障和恢复判据；用分母不同及短窗口无故障的 fixture 防止外推可靠性。
- 已改：明确 SLI 事件/时间口径、成功/失败定义、分母、排除、观测窗口和目标来源；请求成功率与时间可用性不能互换。；逐窗口复算成功/总量或可用/应观测时长，保留缺测、重试、重复事件和分母冲突；只有定义兼容时才合并窗口。
- 新案例：[domain-method-control](../../skills/zh/testing-types/reliability-testing/evals/cases/domain-method-control.yaml) — reliability-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/reliability-testing/evals/cases/domain-method-success.yaml) — reliability-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 115. `requirement-ambiguity-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-ambiguity-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-ambiguity-analysis/SKILL.md)

- 首轮建议：为每个歧义并列至少两种合理解释、各自后果及最小判别问题；补定义充分的正确反例，验证不会把缺规则、冲突和正常简写都归为歧义。
- 已改：保留需求ID、来源、版本和原文；先分清同一句多解AMBIGUOUS、没有规则MISSING_RULE、来源矛盾CONFLICT和明确可测CLEAR，不能为凑发现误报正常简写。；每项歧义并列至少两种合理解释、适用条件、不同业务/测试后果和支持原文；无第二种合理解释时检查是否其实是缺资料。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/requirement-ambiguity-analysis/evals/cases/domain-method-regression.yaml) — requirement-ambiguity-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 116. `requirement-conflict-detection` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-conflict-detection/SKILL.md) · [EN](../../skills/en/testing-types/requirement-conflict-detection/SKILL.md)

- 首轮建议：补同词不同角色/版本的非冲突反例，以及多条规则共同构成冲突的 fixture；输出参与规则 ID 和最小冲突集合，无法判定时保留限制。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-multi-rule-minimal-conflict](../../skills/zh/testing-types/requirement-conflict-detection/evals/cases/review-multi-rule-minimal-conflict.yaml) — 三规则共同冲突即使每一对可满足；[review-role-version-nonconflict](../../skills/zh/testing-types/requirement-conflict-detection/evals/cases/review-role-version-nonconflict.yaml) — 同词不同角色或版本不是同范围冲突；[review-unknown-scope](../../skills/zh/testing-types/requirement-conflict-detection/evals/cases/review-unknown-scope.yaml) — 范围未知不能确认冲突。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 117. `requirement-consistency-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-consistency-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-consistency-analysis/SKILL.md)

- 首轮建议：补术语/实体映射、数值单位与状态映射规则；用别名等价、同名不同版本、同一阈值单位不同的 fixture 验证一致、矛盾和不可比较三类结论。
- 已改：固定比较来源及版本/生效时间，建立术语别名、实体ID、单位和状态映射；映射要有词典/契约证据，名字相同不自动同义。；比较同范围、同版本、同条件下的业务规则；单位按证据换算，状态按明示映射归一，不静默合并跨版本或不同业务实体。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/requirement-consistency-analysis/evals/cases/domain-method-regression.yaml) — requirement-consistency-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 118. `requirement-gap-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-gap-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-gap-analysis/SKILL.md)

- 首轮建议：把未定义规则、材料缺失、冲突与不适用分开；以一个完整需求和一个缺关键关闭条件的 fixture 检查缺口来源、影响、澄清优先级与关闭证据。
- 已改：以范围/版本和适用角色、状态、规则、异常、关闭条件建立需求清单；每项注明来源与已提供材料覆盖，不把通常清单强套到不适用产品。；分列MISSING_RULE（确认相关但规则未定义）、MISSING_MATERIAL（引用资料未提供）、CONFLICT（已提供规则冲突）、N/A（有范围理由不适用）与COMPLETE。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/requirement-gap-analysis/evals/cases/domain-method-regression.yaml) — requirement-gap-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 119. `requirement-quality-review` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/requirement-quality-review/SKILL.md)

- 首轮建议：补一份无需阻塞的正确需求和一份可定位的高风险缺陷需求；验证问题严重度、原句引用和修订建议，避免评审总要产生问题或只复述审查维度。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-complete-requirement-control](../../skills/zh/testing-types/requirement-quality-review/evals/cases/review-complete-requirement-control.yaml) — 完整限定需求不应编造阻塞；[review-located-high-risk-gap](../../skills/zh/testing-types/requirement-quality-review/evals/cases/review-located-high-risk-gap.yaml) — 退款验收不可观察缺口需具体来源和优先级。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 120. `requirement-traceability-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/requirement-traceability-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirement-traceability-analysis/SKILL.md)

- 首轮建议：补带类型的边、同一义务多用例、旧版本映射与重复 ID 的处理；把已映射、已执行、已满足分列，并以小型追踪图验证覆盖计算。
- 已改：固定requirement/obligation及实现/test/run的ID与版本，关系类型保持direct/derived/indirect/contradictory/missing；implements/validates/executed-by/satisfies只作为独立的边用途列，并记录证据来源；文件存在、名字相似不构成边。；同义务多测试按义务唯一ID去重分母，保留测试层和具体断言；重复ID但不同内容先标IDENTITY_CONFLICT，不能合并计覆盖。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/requirement-traceability-analysis/evals/cases/domain-method-regression.yaml) — requirement-traceability-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 121. `requirements-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/requirements-analysis/SKILL.md) · [EN](../../skills/en/testing-types/requirements-analysis/SKILL.md)

- 首轮建议：提供实际状态/规则 fixture，要求从原文导出可追踪测试点、未知规则和高价值问题，并验证完整需求不会被补上虚构缺口。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-complete-analysis-control](../../skills/zh/testing-types/requirements-analysis/evals/cases/review-complete-analysis-control.yaml) — 完整规则不应新增虚构缺口或领域；[review-state-rule-trace](../../skills/zh/testing-types/requirements-analysis/evals/cases/review-state-rule-trace.yaml) — 分析导出有来源测试点但不补未知时间。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 122. `requirements-analysis-plus` (P1)

定位：[ZH](../../skills/zh/testing-types/requirements-analysis-plus/SKILL.md) · [EN](../../skills/en/testing-types/requirements-analysis-plus/SKILL.md)

- 首轮建议：先修输入保真，再标明提取器能力边界；用数值规则、角色冲突与非活动业务验证不损坏原文、不造规则。
- 已改：移除固定业务结论、优先级和虚构指标；脚本仅准备完整源材料、行号、哈希及 NOT_ASSESSED 脚手架，空输入失败；语义任务由主 Prompt 执行。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/requirements-analysis-plus/evals/cases/review-repair-regression.yaml) — requirements-analysis-plus: sourced repair regression。
- 二次复查/验证：空源、完整源保真、未知值及独立 CLI/导出检查通过；确定性脚本只作准备；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 123. `resilience-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/resilience-testing/SKILL.md) · [EN](../../skills/en/testing-types/resilience-testing/SKILL.md)

- 首轮建议：补扰动前/中/后的功能与数据不变量、降级状态和恢复判据；以部分依赖失效、恢复失败 fixture 区分韧性、可靠性和混沌实验的责任边界。
- 已改：用业务合同定义扰动前/中/后功能与数据不变量，列正常、降级、不可用状态及允许的体验变化。；为部分依赖失效、慢依赖和恢复失败建立条件矩阵，逐状态写仍需保护的核心功能及可暂停功能。
- 新案例：[domain-method-control](../../skills/zh/testing-types/resilience-testing/evals/cases/domain-method-control.yaml) — resilience-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/resilience-testing/evals/cases/domain-method-success.yaml) — resilience-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 124. `retry-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/retry-testing/SKILL.md) · [EN](../../skills/en/testing-types/retry-testing/SKILL.md)

- 首轮建议：补可重试/永久错误、次数与总时限、退避抖动、服务端提示和重复副作用矩阵；用“超时但写入成功”及多层重试 trace 验证预算与幂等。
- 已改：按错误合同分类可重试、永久拒绝和结果未知，明确“次数”是总尝试还是追加重试及每层调用关系。；列端到端 deadline、每次超时、退避/抖动、HTTP Retry-After（延迟秒数或 HTTP-date） 与取消规则，按时间线计算尝试与等待的总预算，不自设退避数值。
- 新案例：[domain-method-control](../../skills/zh/testing-types/retry-testing/evals/cases/domain-method-control.yaml) — retry-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/retry-testing/evals/cases/domain-method-success.yaml) — retry-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 125. `risk-based-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/risk-based-testing/SKILL.md) · [EN](../../skills/en/testing-types/risk-based-testing/SKILL.md)

- 首轮建议：把每项风险关联到测试目标、深度、最低证据与残余风险，并给定性判断锚点；用时间不足 fixture 检查高风险优先和需授权的取舍，避免无依据量化。
- 已改：按可观察影响、暴露/发生证据、可探测性与控制缺口建立定性锚点；缺项目数值模型不用自定分数乘积，未知概率保留不确定。；每风险关联测试目标、层/平台、深度、数据、最低可观察证据、时长依据和剩余风险；高风险须有可证伪业务断言，而非仅更多用例。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/risk-based-testing/evals/cases/domain-method-regression.yaml) — risk-based-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 126. `root-cause-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/root-cause-analysis/SKILL.md) · [EN](../../skills/en/testing-types/root-cause-analysis/SKILL.md)

- 首轮建议：加入两个竞争假设、反证和最小判别实验；用只有时间相关性与有因果链的成对 fixture，验证不把最后一个错误日志当作已证实根因。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-competing-hypotheses](../../skills/zh/testing-types/root-cause-analysis/evals/cases/review-competing-hypotheses.yaml) — 竞争假设保留反证和最小区分实验；[review-controlled-causal-chain](../../skills/zh/testing-types/root-cause-analysis/evals/cases/review-controlled-causal-chain.yaml) — 受控复现支持受限因果解释。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 127. `secrets-exposure-review` (P1)

定位：[ZH](../../skills/zh/testing-types/secrets-exposure-review/SKILL.md) · [EN](../../skills/en/testing-types/secrets-exposure-review/SKILL.md)

- 首轮建议：补代码/配置/CI/日志/产物/历史位置及凭据生命周期核对；用占位符、测试样例和真实格式但有效性未知的脱敏 fixture，验证脱敏引用与风险分级，不凭模式声称凭据有效。
- 已改：按已授权材料盘点代码、配置、CI、日志、产物和历史位置，记录候选的路径/行号、类别及脱敏指纹，不复制值或自行读取真实凭据。；区分环境变量占位符、明确合成测试值和真实格式但有效性未知的候选；模式匹配不能证明凭据存在或有效。
- 新案例：[domain-method-control](../../skills/zh/testing-types/secrets-exposure-review/evals/cases/domain-method-control.yaml) — secrets-exposure-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/secrets-exposure-review/evals/cases/domain-method-success.yaml) — secrets-exposure-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 128. `security-requirement-review` (P1)

定位：[ZH](../../skills/zh/testing-types/security-requirement-review/SKILL.md) · [EN](../../skills/en/testing-types/security-requirement-review/SKILL.md)

- 首轮建议：补“资产→威胁→安全义务→控制→可验证验收”链路及项目给定标准版本；用不可测的“系统安全”与明确义务成对 fixture 验证建议可执行、无虚构合规结论。
- 已改：建立资产→威胁主体/路径→安全义务→控制→可验证验收链，标范围、来源与项目指定标准/版本，未给标准不能自选合规基线。；将“安全”“加密好”等模糊需求拆成需要澄清的主体、动作、边界、时机与可观察结果；具体阈值/算法须来自要求或标建议。
- 新案例：[domain-method-control](../../skills/zh/testing-types/security-requirement-review/evals/cases/domain-method-control.yaml) — security-requirement-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/security-requirement-review/evals/cases/domain-method-success.yaml) — security-requirement-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 129. `security-testing` (P2)

定位：[ZH](../../skills/zh/testing-types/security-testing/SKILL.md) · [EN](../../skills/en/testing-types/security-testing/SKILL.md)

- 首轮建议：补威胁/控制/测试/证据矩阵和正常授权反例；明确设计、实际执行和漏洞确认三种状态，用“扫描无发现但未验证业务权限” fixture 防止外推安全通过。
- 已改：在已授权范围内建立资产/主体→威胁→控制→验证步骤→预期→证据/状态矩阵；记录环境、动作范围、停止条件与真实授权来源。；正常授权访问与越权拒绝成对验证；拒绝路径要核对数据未泄露、工具/写入无副作用，不能只看错误响应或扫描结果。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/security-testing/evals/cases/domain-method-regression.yaml) — security-testing: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 130. `session-security-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/session-security-testing/SKILL.md) · [EN](../../skills/en/testing-types/session-security-testing/SKILL.md)

- 首轮建议：按 Cookie/token 机制选择创建、轮换、固定、闲置/绝对过期、撤销、退出与多端状态；用退出后旧凭据和权限变化 fixture 验证预期，不自设有效期。
- 已改：先识别 Cookie/opaque session/access+refresh token 等机制，列创建、认证后轮换、固定、闲置/绝对过期、撤销、退出和多端合同。；用凭据 label 建前后状态表，检查旧凭据何时失效、新凭据权限与服务端状态；不要记录真实 Cookie/token。
- 新案例：[domain-method-control](../../skills/zh/testing-types/session-security-testing/evals/cases/domain-method-control.yaml) — session-security-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/session-security-testing/evals/cases/domain-method-success.yaml) — session-security-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 131. `state-transition-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/state-transition-testing/SKILL.md) · [EN](../../skills/en/testing-types/state-transition-testing/SKILL.md)

- 首轮建议：补状态/事件/守卫/动作/目标矩阵、不可达与非法迁移、守卫边界及部分失败；用小状态图核对有效与无效迁移覆盖，而不只输出状态名。
- 已改：建立来源化状态/事件/guard/动作/目标矩阵，标初始与终止、持久化和失败时的原子性合同。；从初始状态核对可达迁移，并列非法/未定义事件；guard 在边界的真/假分别构造，不仅检查状态名出现。
- 新案例：[domain-method-control](../../skills/zh/testing-types/state-transition-testing/evals/cases/domain-method-control.yaml) — state-transition-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/state-transition-testing/evals/cases/domain-method-success.yaml) — state-transition-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 132. `technical-design-quality-review` (P2)

定位：[ZH](../../skills/zh/testing-types/technical-design-quality-review/SKILL.md) · [EN](../../skills/en/testing-types/technical-design-quality-review/SKILL.md)

- 首轮建议：加入实际组件/时序材料，核对接口边界、数据不变量、失败与恢复路径；用已有可靠控制的正确设计和分布式部分提交 fixture，检查定位和风险解释而非泛化建议。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-distributed-partial-commit](../../skills/zh/testing-types/technical-design-quality-review/evals/cases/review-distributed-partial-commit.yaml) — 分布式部分提交违反给定不变量；[review-reliable-controls-design](../../skills/zh/testing-types/technical-design-quality-review/evals/cases/review-reliable-controls-design.yaml) — 可靠控制设计不能机械拒绝。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 133. `test-case-reviewer` (P2)

定位：[ZH](../../skills/zh/testing-types/test-case-reviewer/SKILL.md) · [EN](../../skills/en/testing-types/test-case-reviewer/SKILL.md)

- 首轮建议：补原始用例、需求和故意植入的不可观察预期/前置缺失；验证逐条定位与修订建议，并用正确用例约束误报，不从行业常识推断必有漏测。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-correct-case-control](../../skills/zh/testing-types/test-case-reviewer/evals/cases/review-correct-case-control.yaml) — 可执行有来源用例不应误拒；[review-located-case-defects](../../skills/zh/testing-types/test-case-reviewer/evals/cases/review-located-case-defects.yaml) — 用例评审定位弱预期和缺前置。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 134. `test-case-reviewer-plus` (P1)

定位：[ZH](../../skills/zh/testing-types/test-case-reviewer-plus/SKILL.md) · [EN](../../skills/en/testing-types/test-case-reviewer-plus/SKILL.md)

- 首轮建议：改成基于输入的可追踪审查或明确仅为示例；用完整正确用例与非促销缺陷用例验证可无发现、不伪造覆盖结论。
- 已改：移除固定业务结论、优先级和虚构指标；脚本仅准备完整源材料、行号、哈希及 NOT_ASSESSED 脚手架，空输入失败；语义任务由主 Prompt 执行。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/test-case-reviewer-plus/evals/cases/review-repair-regression.yaml) — test-case-reviewer-plus: sourced repair regression。
- 二次复查/验证：空源、完整源保真、未知值及独立 CLI/导出检查通过；确定性脚本只作准备；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 135. `test-case-writing` (P2)

定位：[ZH](../../skills/zh/testing-types/test-case-writing/SKILL.md) · [EN](../../skills/en/testing-types/test-case-writing/SKILL.md)

- 首轮建议：把合并/拆分条件、顺序与 Trace 字段做结构化检查；用同意图不同预期、四角色重复输入和来源缺版本 fixture 验证正确拆分与来源完整，而不只检查“测试用例”。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-role-merge-split-trace](../../skills/zh/testing-types/test-case-writing/evals/cases/review-role-merge-split-trace.yaml) — 四角色重复合并但不同预期拆分。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 136. `test-code-review` (P1)

定位：[ZH](../../skills/zh/testing-types/test-code-review/SKILL.md) · [EN](../../skills/en/testing-types/test-code-review/SKILL.md)

- 首轮建议：补失败敏感性、被测对象隔离、mock 边界、数据/并行隔离与清理；用吞异常、恒真断言和正常测试 fixture 验证实际缺陷定位。
- 已改：先标被测行为和失败时测试应如何失败，逐断言追踪实际值是否来自被测对象，检查恒真、只断类型或吞异常后无失败出口。；核对mock边界、异常分支、异步等待/返回和清理，避免把被测对象自身mock掉或遗漏promise结果。
- 新案例：[domain-method-control](../../skills/zh/testing-types/test-code-review/evals/cases/domain-method-control.yaml) — test-code-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/test-code-review/evals/cases/domain-method-success.yaml) — test-code-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 137. `test-data-generation` (P2)

定位：[ZH](../../skills/zh/testing-types/test-data-generation/SKILL.md) · [EN](../../skills/en/testing-types/test-data-generation/SKILL.md)

- 首轮建议：补按 schema/实体关系生成有效与无效数据的过程，显式标注各组预期用途；用唯一性、外键、状态关联 fixture 校验生成数据及重现性，不只交付数据策略表。
- 已改：从已提供schema、实体外键、唯一约束、状态关系与场景预期派生数据组；固定种子/生成器版本，缺规则保留UNKNOWN，不自动发明字段或真实用户。；分开有效happy/boundary数据与定向无效数据，每组注明改变的约束、预期拒绝/允许和不受影响的关系；无效数据不能悄悄进入正常流程组。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-data-generation/evals/cases/domain-method-regression.yaml) — test-data-generation: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 138. `test-data-requirement-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/test-data-requirement-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-data-requirement-analysis/SKILL.md)

- 首轮建议：补场景→实体/状态/关系→数量依据→获取与清理条件的矩阵；用缺 schema、跨实体关联和受限个人数据 fixture 验证未知量与来源可见。
- 已改：从场景/风险列场景→实体/状态/关系→取值/边界→数量依据→获取来源/权限→准备/清理条件矩阵；本Skill分析需求，不默认生成或抓取数据。；数据量依据来自并发/隔离/重复次数/消耗模式，未知次数给公式与缺口；不能自定100行或把会话数等同实体数。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-data-requirement-analysis/evals/cases/domain-method-regression.yaml) — test-data-requirement-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 139. `test-effectiveness-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/test-effectiveness-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-effectiveness-analysis/SKILL.md)

- 首轮建议：补故障/义务→测试→断言→漏检映射，分开历史逃逸与可控故障注入；用高通过率但已知漏检 fixture 检查分母、观察窗口与因果限制。
- 已改：固定义务/故障类别、测试ID、实际生产逻辑、有效断言与可逃逸缺陷的映射；通过率/覆盖率只是信号，不能替代故障检出证据。；历史逃逸记录观察窗口、暴露量、检出/漏检与关联来源；可控故障注入另列独立分母、控制组、环境和变异身份，不能混为生产缺陷率。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-effectiveness-analysis/evals/cases/domain-method-regression.yaml) — test-effectiveness-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 140. `test-gap-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/test-gap-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-gap-analysis/SKILL.md)

- 首轮建议：补已映射未执行、已执行未满足、未映射但材料不足、不适用的成对 fixture；核对缺口分类和补测关闭证据，不能把清单项数直接算成有效覆盖率。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-obligation-evidence-states](../../skills/zh/testing-types/test-gap-analysis/evals/cases/review-obligation-evidence-states.yaml) — 已映射、已执行、未知和不适用状态需区分。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 141. `test-maintenance-cost-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/test-maintenance-cost-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-maintenance-cost-analysis/SKILL.md)

- 首轮建议：按产品变化、测试缺陷、基础设施、数据与重复实现拆分成本；补样本窗口和区间估计，用相同总时长不同成因 fixture 验证建议，不据此评价个人绩效。
- 已改：固定测试资产/样本窗口/统计单位和工时来源，分产品变化、测试缺陷、基础设施、数据、重复实现及无法分类成本；同一工时不得重复计入多个原因。；把触发事件、修改频率、工时范围、复核/返工与故障影响关联，区分一次建设和持续维护，不用单次样本推长期精确费用。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-maintenance-cost-analysis/evals/cases/domain-method-regression.yaml) — test-maintenance-cost-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 142. `test-report-review` (P2)

定位：[ZH](../../skills/zh/testing-types/test-report-review/SKILL.md) · [EN](../../skills/en/testing-types/test-report-review/SKILL.md)

- 首轮建议：增加含跳过/阻塞/重跑的用例级统计 fixture，以及构建版本错配与受控条件项；核对分母、分类和建议状态，用完整一致报告约束误拒绝。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-report-reconciliation](../../skills/zh/testing-types/test-report-review/evals/cases/review-report-reconciliation.yaml) — 拒绝冲突报告并接受一致对照。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 143. `test-reporting` (P2)

定位：[ZH](../../skills/zh/testing-types/test-reporting/SKILL.md) · [EN](../../skills/en/testing-types/test-reporting/SKILL.md)

- 首轮建议：补原始执行行与缺陷行，核对计划/执行/通过/失败/跳过/阻塞统计和重跑口径；成功样例不应只给总数，未知统计保留未知。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-raw-execution-statistics](../../skills/zh/testing-types/test-reporting/evals/cases/review-raw-execution-statistics.yaml) — 用例、重跑、分母与构建证据；[review-unknown-denominator](../../skills/zh/testing-types/test-reporting/evals/cases/review-unknown-denominator.yaml) — 部分日志保留未知计划分母。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 144. `test-runtime-optimization` (P2)

定位：[ZH](../../skills/zh/testing-types/test-runtime-optimization/SKILL.md) · [EN](../../skills/en/testing-types/test-runtime-optimization/SKILL.md)

- 首轮建议：补实际关键路径与 setup/teardown 占比、资源上限、冷暖缓存口径；以同一保护义务的基线/候选运行对验证耗时改善及故障检出保留，不能只比较不同规模总时长。
- 已改：用同commit/测试义务/数据/资源/窗口的事件profile分setup、execute、teardown、重试；沿依赖DAG求关键路径，重叠job不相加。；单列cold/warm缓存、runner上限、并发、独立数据与资源争用；候选改变的因素有记录，不能用不同测试规模或环境推断提速。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-runtime-optimization/evals/cases/domain-method-regression.yaml) — test-runtime-optimization: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 145. `test-scope-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/test-scope-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-scope-analysis/SKILL.md)

- 首轮建议：补版本×层级×平台×数据状态的范围单元、包含/排除依据及变更触发；用未定义边界和新需求 fixture 验证未知项，不与回归范围分析混为同一入口。
- 已改：从当前交付目标与版本建立版本×测试层×平台×数据状态的范围单元，关联需求/义务、纳入/排除证据、负责人和可观察验收；新需求测试不限于回归变更。；分列INCLUDE、EXCLUDE、UNKNOWN，排除必须有范围来源/独立契约理由；不明支持平台、边界或数据规则保持未知，不能默认不测。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-scope-analysis/evals/cases/domain-method-regression.yaml) — test-scope-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 146. `test-strategy` (P2)

定位：[ZH](../../skills/zh/testing-types/test-strategy/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy/SKILL.md)

- 首轮建议：把目标、范围、深度、资源、准入准出与证据/负责人连接成最小可执行表；用不同容量 fixture 检查取舍和未决风险，不能自动套固定通过率门槛。
- 已改：以版本/业务目标与风险建立最小执行表：目标→义务/范围→层与深度→数据/环境→资源/负责人→准入准出来源→证据与剩余风险，避免分散章节无法执行。；沿用项目工具与现实容量，先覆盖关键资损/授权等最低保护；每场景有业务后置条件和证据，资源不足列不可完成项与最小替代验证。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/test-strategy/evals/cases/domain-method-regression.yaml) — test-strategy: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 147. `test-strategy-plus` (P1)

定位：[ZH](../../skills/zh/testing-types/test-strategy-plus/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy-plus/SKILL.md)

- 首轮建议：先停止把固定模板当作分析结果；按已提供事实生成或明确示例，并用三个非活动领域 fixture 验证未知值不被补全。
- 已改：移除固定业务结论、优先级和虚构指标；脚本仅准备完整源材料、行号、哈希及 NOT_ASSESSED 脚手架，空输入失败；语义任务由主 Prompt 执行。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/test-strategy-plus/evals/cases/review-repair-regression.yaml) — test-strategy-plus: sourced repair regression。
- 二次复查/验证：空源、完整源保真、未知值及独立 CLI/导出检查通过；确定性脚本只作准备；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 148. `test-strategy-review` (P2)

定位：[ZH](../../skills/zh/testing-types/test-strategy-review/SKILL.md) · [EN](../../skills/en/testing-types/test-strategy-review/SKILL.md)

- 首轮建议：补完整可接受策略和带依赖/RACI/门禁冲突的策略 fixture；核对阻塞与条件项分级、关闭证据和正确输入可通过，避免把所有改进建议都当阻塞项。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-strategy-control-and-conflicts](../../skills/zh/testing-types/test-strategy-review/evals/cases/review-strategy-control-and-conflicts.yaml) — 合法策略与门禁责任冲突。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 149. `test-suite-health-analysis` (P1)

定位：[ZH](../../skills/zh/testing-types/test-suite-health-analysis/SKILL.md) · [EN](../../skills/en/testing-types/test-suite-health-analysis/SKILL.md)

- 首轮建议：补用例/运行身份、失败类型、重试与隔离、重复覆盖、耗时趋势和被保护义务；用高通过率但大量重试的 fixture 验证健康结论，不自创无依据总分。
- 已改：按稳定test ID、义务、代码/数据版本与run ID归一化运行，分开首尝试、重试、隔离、跳过和未运行。；按给定口径复算最终/首尝试通过、重试比例与失败类别，保留产品/测试/环境/未知原因；重试后绿不证明根因已消失。
- 新案例：[domain-method-control](../../skills/zh/testing-types/test-suite-health-analysis/evals/cases/domain-method-control.yaml) — test-suite-health-analysis: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/test-suite-health-analysis/evals/cases/domain-method-success.yaml) — test-suite-health-analysis: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 150. `testability-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/testability-analysis/SKILL.md) · [EN](../../skills/en/testing-types/testability-analysis/SKILL.md)

- 首轮建议：补实际设计图/接口 fixture，验证最小安全观测点、时间/随机性控制与依赖替身建议；用已有测试缝的正确反例，避免一律建议增加调试后门。
- 已改：补充以下具体任务用例与合法/边界对照，复核输入、判定标准及来源边界；保留原有案例。
- 新案例：[review-actual-design-safe-seams](../../skills/zh/testing-types/testability-analysis/evals/cases/review-actual-design-safe-seams.yaml) — 架构和接口导出最小安全测试缝；[review-existing-seam-control](../../skills/zh/testing-types/testability-analysis/evals/cases/review-existing-seam-control.yaml) — 已有安全测试缝需复用而非新增后门。
- 二次复查/验证：新增输入、预期与合法/边界材料复核；确定性 grader 的正反对照已运行（配置中包含时）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 151. `testcase-writer-plus` (P1)

定位：[ZH](../../skills/zh/testing-types/testcase-writer-plus/SKILL.md) · [EN](../../skills/en/testing-types/testcase-writer-plus/SKILL.md)

- 首轮建议：改为来源驱动的场景、可观察断言和风险优先级或明确示例；用密码边界和空输入 fixture 验证无虚构业务数据。
- 已改：移除固定业务结论、优先级和虚构指标；脚本仅准备完整源材料、行号、哈希及 NOT_ASSESSED 脚手架，空输入失败；语义任务由主 Prompt 执行。
- 新案例：[review-repair-regression](../../skills/zh/testing-types/testcase-writer-plus/evals/cases/review-repair-regression.yaml) — testcase-writer-plus: sourced repair regression。
- 二次复查/验证：空源、完整源保真、未知值及独立 CLI/导出检查通过；确定性脚本只作准备；双端配置 合法（仅配置）；Excel 多表/稀疏列/源行号 helper 同步修复。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 152. `testing-bottleneck-analysis` (P2)

定位：[ZH](../../skills/zh/testing-types/testing-bottleneck-analysis/SKILL.md) · [EN](../../skills/en/testing-types/testing-bottleneck-analysis/SKILL.md)

- 首轮建议：补事件时间线、排队/执行/返工拆分、WIP 与吞吐口径；用资源闲置但依赖阻塞及高并发反降吞吐 fixture，验证瓶颈位置与可测改进，不直接归因为人力不足。
- 已改：固定窗口、工作项ID/复杂度、到达/完成和状态事件；时间线区分queue/等待依赖、实际执行、返工、交接与阻塞，不能把总周期当工时。；WIP用同窗口内未完成项，吞吐用完成项/窗口，交付周期与各状态停留分别统计；样本/缺事件与窗口不一致时给限制，不凭平均推因果。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/testing-bottleneck-analysis/evals/cases/domain-method-regression.yaml) — testing-bottleneck-analysis: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 153. `threat-modeling` (P1)

定位：[ZH](../../skills/zh/testing-types/threat-modeling/SKILL.md) · [EN](../../skills/en/testing-types/threat-modeling/SKILL.md)

- 首轮建议：补数据流/边界识别、威胁主体、前置条件、控制与残余风险链路；给一个可选轻量分类示例，用实际架构 fixture 验证只引用已提供组件与路径。
- 已改：按已给组件画主体、入口、数据存储/流动与信任边界，列资产、敏感数据和允许动作；未给组件不得自行加入。；对每条跨边界路径写威胁主体、能力、前置条件、可控输入、资产影响与适用义务，可选用冒充/篡改/泄露/中断/提权等轻量分类帮助查漏。
- 新案例：[domain-method-control](../../skills/zh/testing-types/threat-modeling/evals/cases/domain-method-control.yaml) — threat-modeling: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/threat-modeling/evals/cases/domain-method-success.yaml) — threat-modeling: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 154. `timeout-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/timeout-testing/SKILL.md) · [EN](../../skills/en/testing-types/timeout-testing/SKILL.md)

- 首轮建议：补端到端 deadline、连接/读取/排队预算、取消传播及迟到结果；用调用链预算超限和超时后已提交 fixture 检查状态、副作用与恢复证据。
- 已改：标端到端absolute deadline与连接/排队/读取/处理预算、时间源和计时起点，区分串行、重叠与每层独立超时。；按实际调用链累计已用时间和剩余deadline，检查子调用是否传播剩余预算；单项均未超时也可能总链超限。
- 新案例：[domain-method-control](../../skills/zh/testing-types/timeout-testing/evals/cases/domain-method-control.yaml) — timeout-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/timeout-testing/evals/cases/domain-method-success.yaml) — timeout-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 155. `ui-test-cypress` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-cypress/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-cypress/SKILL.md)

- 首轮建议：补依项目版本选择配置、命令与 stub 边界，以及重试语义、会话/数据隔离和业务断言；用真实最小应用 fixture 验证错误业务结果会失败，不能仅检查测试文件存在。
- 已改：从项目lockfile/config确认Cypress、Node和浏览器版本及component/E2E边界；按该版本生成配置、custom command、spec与CI命令，不默认升级或混用旧配置。；保留真实页面/组件与业务逻辑，cy.intercept只替换已确认外部边界；仅验证stub回包不足以证明真实后置条件。明确fixture数据与session隔离/注销。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-cypress/evals/cases/domain-method-regression.yaml) — ui-test-cypress: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 156. `ui-test-playwright` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-playwright/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-playwright/SKILL.md)

- 首轮建议：生成测试应明确业务后置条件、稳定语义定位、身份/数据隔离和失败产物；用错误业务结果与并行用户 fixture 检查断言敏感性，页面标题正常不应代表业务成功。
- 已改：固定项目Playwright/Node/browser版本、projects/fixtures与配置；沿用真实入口，记录测试ID、commit、worker/project和环境，未兼容配置先诊断不擅自换框架。；优先role/name/testid等稳定语义定位，执行后以auto-retrying assertion核对订单/账务/状态与主体；页面标题/URL只满足相应导航义务，不能替代付款成功。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-playwright/evals/cases/domain-method-regression.yaml) — ui-test-playwright: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 157. `ui-test-puppeteer` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-puppeteer/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-puppeteer/SKILL.md)

- 首轮建议：记录实际版本/浏览器配置与兼容范围，补页面/浏览器生命周期、业务就绪等待和失败产物；用新窗口、加载失败与超时 fixture 检查清理和可观察后置条件。
- 已改：读取实际Puppeteer/Node/browser与launch配置/支持范围；版本或browser不兼容单列CONFIG_ERROR，不能把launch成功当所有功能兼容。；新窗口从目标创建事件/关联opener定位并等待可用page，检查目标URI与权限；导航等待与业务就绪分开，以页面真实状态作oracle，固定sleep无此证据。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-puppeteer/evals/cases/domain-method-regression.yaml) — ui-test-puppeteer: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 158. `ui-test-selector-review` (P1)

定位：[ZH](../../skills/zh/testing-types/ui-test-selector-review/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-selector-review/SKILL.md)

- 首轮建议：补语义角色/名称、test ID、作用域、唯一性、动态文案与多语言稳定性比较；用重复按钮和合法稳定 CSS fixture 验证理由，避免机械禁止所有 CSS/XPath。
- 已改：从DOM/组件与用户动作明确目标元素，比较role+accessible name、稳定test ID、作用域及CSS/XPath的实际语义和维护合同。；在给定页面状态检查匹配数量、可见/可交互性和正确实例；重复按钮须以业务容器/稳定身份区分，不能用first()掩盖歧义。
- 新案例：[domain-method-control](../../skills/zh/testing-types/ui-test-selector-review/evals/cases/domain-method-control.yaml) — ui-test-selector-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/ui-test-selector-review/evals/cases/domain-method-success.yaml) — ui-test-selector-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 159. `ui-test-selenium` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-selenium/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-selenium/SKILL.md)

- 首轮建议：补依项目版本选配置、可观察等待条件、陈旧元素处理、并行数据与 driver 清理；用重新渲染和异常退出 fixture 验证定位/等待与资源释放，不把固定 sleep 当通用修复。
- 已改：固定项目Selenium/binding/browser/driver/Grid版本、capabilities和runner，生成兼容配置与POM；未提供Grid不自建拓扑，版本冲突先诊断。；显式等待可观察条件（元素可交互、业务状态/窗口/URL达成），区分presence/visibility/业务ready；不混用implicit/explicit或以固定sleep修复所有时序。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-selenium/evals/cases/domain-method-regression.yaml) — ui-test-selenium: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 160. `ui-test-strategy` (P1)

定位：[ZH](../../skills/zh/testing-types/ui-test-strategy/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-strategy/SKILL.md)

- 首轮建议：补用户旅程×状态×平台矩阵，按风险分配组件/集成/E2E 与视觉/可访问性证据；用同一需求不同层可覆盖 fixture 验证最小有效组合和保留风险。
- 已改：建立用户旅程×业务状态×平台矩阵，映射每格的风险、验收义务和现有证据，未支持平台不自扩范围。；按最小有效组合分配component、integration、E2E、visual与accessibility证据：业务计算/状态、服务交互、跨层旅程与外观/可访问性分别需要合适oracle。
- 新案例：[domain-method-control](../../skills/zh/testing-types/ui-test-strategy/evals/cases/domain-method-control.yaml) — ui-test-strategy: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/ui-test-strategy/evals/cases/domain-method-success.yaml) — ui-test-strategy: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 161. `ui-test-testcafe` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-testcafe/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-testcafe/SKILL.md)

- 首轮建议：补版本/浏览器与 CI 配置、角色隔离、异步动作/等待及 reporter 失败传播；用最小应用和失败 fixture 验证生成工件可运行、业务失败返回失败状态。
- 已改：确认项目TestCafe/Node/browser、原生自动化模式与CI/reporter版本；生成fixture/test/config和现有runner兼容，缺配置保持待确认不推荐隐式升级。；用Role或独立身份初始化隔离会话，账号/业务键同样隔离；异步t动作必须await，Selector/断言采用支持的智能等待而非固定sleep。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-testcafe/evals/cases/domain-method-regression.yaml) — ui-test-testcafe: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 162. `ui-test-wait-strategy-review` (P1)

定位：[ZH](../../skills/zh/testing-types/ui-test-wait-strategy-review/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-wait-strategy-review/SKILL.md)

- 首轮建议：按 DOM/业务状态/网络/事件选择就绪信号，核对超时预算、轮询与重试副作用；用长连接、后台请求和迟到结果 fixture 验证不会把网络空闲一律当业务就绪。
- 已改：按动作后义务选择就绪信号：DOM存在/可操作只证明元素条件；业务状态/版本/确认号证明业务进度；网络/事件只有与目标操作关联才可作证据。；逐等待记录开始动作、可观察条件、请求/业务ID、timeout与端到端预算；固定sleep仅能延时，不能保证条件成立。
- 新案例：[domain-method-control](../../skills/zh/testing-types/ui-test-wait-strategy-review/evals/cases/domain-method-control.yaml) — ui-test-wait-strategy-review: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/ui-test-wait-strategy-review/evals/cases/domain-method-success.yaml) — ui-test-wait-strategy-review: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 163. `ui-test-webdriverio` (P2)

定位：[ZH](../../skills/zh/testing-types/ui-test-webdriverio/SKILL.md) · [EN](../../skills/en/testing-types/ui-test-webdriverio/SKILL.md)

- 首轮建议：补 capabilities/service/版本组合、异步命令、并行会话隔离和失败 trace 的证据字段；用配置不兼容与命令失败 fixture 验证可诊断错误，而不只输出自动化计划。
- 已改：固定WebdriverIO/Node、runner/framework、browser/driver/service版本组合；核对capabilities、services与实际安装包、配置及远端支持，不从名称假定兼容。；生成该版本的async spec/BDD步骤，所有异步命令await；等待以可观察业务状态和元素条件，原命令错误不得catch吞成通过。
- 新案例：[domain-method-regression](../../skills/zh/testing-types/ui-test-webdriverio/evals/cases/domain-method-regression.yaml) — ui-test-webdriverio: 领域结果、正确对照与证据边界。
- 二次复查/验证：领域 fixture 与 oracle 静态复核；grader 独立复制、合法输出和错误对照已验证；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

### 164. `visual-regression-testing` (P1)

定位：[ZH](../../skills/zh/testing-types/visual-regression-testing/SKILL.md) · [EN](../../skills/en/testing-types/visual-regression-testing/SKILL.md)

- 首轮建议：补基线版本键、视口/浏览器/字体/数据、动画稳定、遮罩依据与阈值口径；用真实缺陷和已批准设计变化成对 fixture，验证差异归因及基线更新审批边界。
- 已改：定义baseline键：页面/版本/视口/浏览器/OS/字体/主题/数据，并检查比较双方同条件；条件不同先标不可比或环境差异。；核对字体加载、动画/时间、动态数据和截图就绪；遮罩需理由与范围，不能遮住被验收的关键内容。
- 新案例：[domain-method-control](../../skills/zh/testing-types/visual-regression-testing/evals/cases/domain-method-control.yaml) — visual-regression-testing: 正确对照与边界判定；[domain-method-success](../../skills/zh/testing-types/visual-regression-testing/evals/cases/domain-method-success.yaml) — visual-regression-testing: 领域流程与结果判定。
- 二次复查/验证：合同/规则与成功、正确对照逐项复核；枚举或计算 oracle 静态复验（适用项）；双端配置 合法（仅配置）。
- 尚未证明：新增语义模型运行 NOT_RUN。

## 工作区与后续验证

开始时已有 1,292 个改动文件：1,288 个保持原字节，4 个与本任务相关的 EN/ZH eval 清单仅追加案例；初始 7,089 个文件没有删除。原 review 和现有证据保留。初始文件中非 Skill 的改动仅生成治理 inventory 双语文档；其余为本次新增测试、报告与证据。HEAD 保持 `c61f507f61711c3c0f0d1777136a5a4ff0e211b3`，分支 `develop`，没有 commit/push。

本次获授权的两个定向模型用例已完成。其余新增语义用例的模型评测，以及项目提供目标系统后才有意义的 UI/真实负载验收仍未执行；本报告没有将其记为通过。
