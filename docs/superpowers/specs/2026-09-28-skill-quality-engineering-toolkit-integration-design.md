<div align="right"><strong>🇨🇳 中文</strong> | <a href="./2026-09-28-skill-quality-engineering-toolkit-integration-design_EN.md">🇬🇧 English</a></div>

# Skill Quality Engineering Toolkit v1.0 集成设计

> 日期：2026-09-28<br>
> 状态：方案 B 已获聊天确认；等待本 spec 书面审阅<br>
> 范围：将提供的 SQET v1.0 Toolkit 作为 `awesome-qa-skills` 的工程文档资产集成<br>
> 非目标：本阶段不新增可安装 Skill，不执行真实模型/Agent Pilot，不伪造运行证据

## 1. 设计结论

采用“兼容性集成”，不把附件原样复制进仓库，也不立即迁移现有治理文档。

附件中的 Toolkit 作为 SQEM 方法论、Eval Case 契约、Pilot 计划和模板的候选规范；仓库已有的 Quality Score、Evidence State、Skill Evaluation Quality Loop 和 Skill-local Eval 结构继续保留为现行工程事实来源。新增入口负责组织两者关系，避免出现第二个质量分体系、第二个 Eval Engine 或第二个全局用例库。

附件根目录的 `README.md` 是打包说明，不作为仓库根 README 覆盖源。附件中的 `en/` / `zh/` 文档布局也会转换为本仓库项目级文档使用的 `NAME.md` / `NAME_EN.md` 约定。

## 2. 审查结果

### 2.1 附件本身

- 实际包包含入口说明、Toolkit README、三组核心文档的中英文版本、五个模板、Eval README 和 Evidence README。
- 三组核心文档的章节编号和章节数量一致；静态扫描未发现 `TODO`、`TBD`、明显密钥、绝对本机路径或包内 Markdown 相对链接问题。
- 内容明确强调 `Quality Claim <= Available Evidence`、Pilot 仍是验证对象、运行证据不能由静态校验替代，这些原则与本仓库现有证据边界一致。
- 附件的状态示例包含 `PARTIAL`，但没有纳入本仓库已有的 `NOT_SCORED` / `UNASSESSED`；直接复制会造成状态语义分裂。
- 附件的五个 SQEM Pilot Skill 与仓库现有的 analysis / executable / router Pilot 不同；直接替换会丢失当前已验证的 Pilot 记录。

### 2.2 仓库兼容性

- 当前仓库已有 `docs/SKILL_QUALITY_GATE*`、`docs/governance/SKILL_EVALUATION_CONTRACT*`、`QUALITY_SCORE_EVAL_CONTRACT*`、`SKILL_EVALUATION_DESIGN*` 和 `SKILL_EVALUATION_PILOTS*`。
- 当前仓库的 Eval 用例以 Skill 包内 `skills/{zh,en}/.../evals/` 为主；不能因为 Toolkit 的根级 `evals/README.md` 创建第二个事实来源。
- `scripts/check_docs_bilingual.py` 使用显式项目文档配对表；新 Toolkit 文档必须加入该表，否则双语镜像不会被自动守护。
- 基线 `bash scripts/check_skills_quality.sh` 已通过，且本次审查未产生工作区改动。

## 3. 目标

1. 提供一个稳定的 `docs/skill-quality-engineering/` 入口，解释 SQET、SQEM、Eval Contract、Pilot、模板和证据目录的关系。
2. 保留 SQEM 的七个质量域、L1-L4 Test Level、E1-E4 Evidence Level、Risk Profile、Quality Profile 和 Quality Claim Gate。
3. 将附件 Eval Contract 接入现有证据状态、Judge、trace、回归和失败分类边界，而不是另起一套运行规则。
4. 让中文默认入口、英文镜像、根级 Eval/Evidence 入口都能通过项目双语校验。
5. 让后续 Pilot 可以增量落地，同时保持当前 `NOT_RUN`、`NOT_SCORED`、`UNASSESSED` 和 `INSUFFICIENT_EVIDENCE` 的事实边界。

## 4. 非目标

- 不把 SQET 变成 `skills/` 下可安装的 Agent Skill。
- 不删除、重命名或覆盖现有治理文档。
- 不把附件的五个 Pilot Skill 直接写成已经完成的运行评测。
- 不复制已有 Skill-local Eval case 到根级目录。
- 不新增 Quality Score 维度、第二个 Eval Engine、第二个 Judge 框架或自动优化循环。
- 不把 `skill-up validate`、静态检查、项目状态或配置有效性写成 runtime、生产或业务验收证据。
- 不在本阶段提交任何真实模型输出、目标环境结果或未经授权的 Evidence Report。

## 5. 目标目录结构

实施后新增或调整的范围如下：

```text
docs/skill-quality-engineering/
├── README.md
├── README_EN.md
├── SKILL_QUALITY_EVALUATION_MODEL.md
├── SKILL_QUALITY_EVALUATION_MODEL_EN.md
├── SKILL_EVAL_CONTRACT.md
├── SKILL_EVAL_CONTRACT_EN.md
├── SKILL_QUALITY_PILOT.md
├── SKILL_QUALITY_PILOT_EN.md
└── templates/
    ├── SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md
    ├── SKILL_EVIDENCE_REPORT_TEMPLATE.md
    ├── SKILL_QUALITY_CI_GUIDE.md
    ├── SKILL_QUALITY_PROFILE_TEMPLATE.md
    └── SKILL_RISK_PROFILE_TEMPLATE.md

evals/
├── README.md
└── README_EN.md

evidence/skill-quality/
├── README.md
└── README_EN.md
```

附件包的根级打包 README 不复制到仓库根目录。模板作为输出模板保留英文/语言中性结构；它们不替代核心方法论文档的中文/英文镜像。

## 6. 事实来源与兼容边界

| 主题 | 现行事实来源 | SQET 的职责 | 集成决策 |
| --- | --- | --- | --- |
| 质量模型 | 新增 SQEM 文档 | 定义七个质量域、测试深度和质量声明边界 | 作为方法论入口，不生成总分 |
| Quality Score | `docs/governance/QUALITY_SCORE_EVAL_CONTRACT*` | SQEM 只说明何时需要评分证据 | 继续由现有契约独占 |
| Evidence State | `docs/governance/SKILL_EVALUATION_CONTRACT*` | Eval Contract 描述 case 意图和证据采集 | 运行状态以现有契约为准 |
| Quality Loop | `docs/governance/SKILL_EVALUATION_DESIGN*` | SQEM Pilot 提供更高层的验证框架 | 不创建第二套 Engine / Judge |
| Pilot 记录 | `docs/governance/SKILL_EVALUATION_PILOTS*` | SQEM Pilot 验证方法论可用性 | 两者并存，明确不同目标 |
| Skill 用例 | 各 Skill 的 `evals/` | 根级 README 提供导航和适配约定 | 不复制为全局用例库 |
| 运行证据 | runner 生成的 trace、metadata、judge、report | Evidence README 规定记录边界 | 无运行结果时保持未运行状态 |

### 6.1 状态映射

集成后的核心文档不创建新的仓库级状态，也不重复定义状态语义；运行结果直接引用 [Skill Evaluation Contract](../../governance/SKILL_EVALUATION_CONTRACT.md)。本节只记录附件表达如何适配到该主契约：

| 附件表达 | 集成后的处理 |
| --- | --- |
| 现有 Evidence State | 按主契约原样引用，不在本 spec 重定义 |
| `PARTIAL` | 不导入为仓库级状态；按主契约和实际证据逐项报告 |

这样既保留附件的风险和证据思想，也不会让读者误以为仓库存在第二套状态机。

### 6.2 Pilot 映射

附件的五个 Pilot Skill：

```text
functional-testing
testability-analysis
performance-testing
skill-evaluation-design
skill-change-verification
```

其中，附件方法名 `skill-evaluation-design` 映射到仓库现有 canonical Skill `skill-evaluation`（`skills/{zh,en}/skill-engineering/skill-evaluation/`）；本次不创建别名目录。它们在本次集成中被定义为“SQEM 方法论 Pilot 候选集”，用于验证质量模型是否可理解、可执行、可维护；它们不替换仓库现有的：

- `requirements-analysis` analysis Pilot；
- `ui-test-playwright` executable Pilot；
- `discover-testing` Router Composition Pilot。

后续若要为五个候选 Skill 新增或调整 Eval，应沿用现有 Skill-local `eval.yaml`、case、trace 和 evidence 结构，并单独记录授权、环境、版本、judge 与限制。

## 7. 文档内容适配

### 7.1 Toolkit README

中文 `README.md` 作为默认入口，英文 `README_EN.md` 作为镜像。入口必须列出：

- SQEM、Eval Contract、Pilot 和五个模板；
- Toolkit 与 `skills/skill-engineering/` 的职责区别；
- 与现有 Quality Score、Evidence Contract、Quality Loop 和 Pilot 记录的关系；
- 根级 `evals/` 与 `evidence/skill-quality/` 只作为导航/证据落点，不构成第二套执行框架；
- 当前状态为 Pilot validation，不代表全仓库 runtime quality 或 release approval。

### 7.2 SQEM 与 Eval Contract

保留附件的主体结构，但增加仓库适配说明：

- 质量声明必须受可用证据约束；
- Quality Score 不在 SQEM 内重新定义；
- Router 行为和证据处理继续完全服从现有 Evaluation Contract，本 spec 不重复其字段或判定规则；
- 附件的 `PARTIAL` 不导入为仓库级状态；
- benchmark、compatibility、runtime、real-world 仍需真实且可复核的证据。

### 7.3 Pilot

保留五个候选 Skill、阶段、指标、退出条件和四种决策，但补充：

- 它是 SQEM 方法论 Pilot，不是现有 executable Pilot 的替代物；
- Pilot 阶段 6-8 在没有真实 Agent、目标环境、跨模型或业务验收证据时，必须遵循现有 Evaluation Contract 的证据边界；
- 不把候选清单写成已经完成的质量档案、benchmark 或兼容性结论。

### 7.4 根级 Eval / Evidence README

`evals/README.md` 明确 Skill-local Eval 是默认事实来源；根级目录只在未来需要 runner-adapted、跨 Skill 或汇总索引时承载经过单独设计的资产。

`evidence/skill-quality/README.md` 明确运行证据应记录 Skill commit/version、Eval version、engine/model、judge、环境、时间、结果、限制和支持/不支持的质量声明。本阶段只建立目录说明，不新增报告。

## 8. 变更范围与执行顺序

获得本 spec 书面批准后，按以下顺序实施：

1. 从附件导入核心文档与五个模板，并按本仓库命名和状态契约做最小适配。
2. 创建双语 Toolkit、Eval、Evidence 入口，补齐事实来源映射和 Pilot 边界。
3. 更新根 `README.md` / `README_EN.md` 的质量工程快速入口；不把 Toolkit 添加为可安装 Skill。
4. 在 `scripts/check_docs_bilingual.py` 注册新增项目文档配对。
5. 检查所有新增 Markdown 链接、状态词、目录结构和 `git diff --check`。
6. 运行仓库质量门禁与文档双语校验；若发现现有治理契约冲突，停止并修正文档，不通过新增别名绕过。

## 9. 验收标准

- 新目录结构与本 spec 一致，且没有复制附件打包说明或博客内容。
- 中文/英文核心入口和三组核心文档均有双向切换链接。
- `templates/` 五个文件可独立作为模板使用，不含真实凭据或本机路径。
- SQEM、Eval Contract、现有 Evidence Contract、Quality Score 和 Quality Loop 的职责边界在入口文档中可追溯。
- 不导入附件的 `PARTIAL` 状态；状态语义和判定规则继续由现有 Evaluation Contract 独占。
- 五个 SQEM Pilot 候选与现有三类 Pilot 均被明确区分；没有删除或覆盖既有 Pilot。
- 没有新增未经执行的 PASS、benchmark、runtime、compatibility、production 或 release claim。
- 通过 `bash scripts/check_skills_quality.sh`、`python3 scripts/check_docs_bilingual.py --repo-root .` 和 `git diff --check`。
- 只提交本次 Toolkit 集成相关文件，不提交生成报告、缓存、密钥或无关改动。

## 10. 风险与处理

| 风险 | 处理 |
| --- | --- |
| 新旧文档重复定义状态或评分 | 入口增加 Source of Truth 映射，SQET 不复制评分和运行状态契约 |
| 根级 `evals/` 被误解为第二个用例库 | README 明确 Skill-local Eval 优先，根级仅作导航/适配落点 |
| Pilot 名称让读者误以为已有运行证据 | 明确“方法论 Pilot 候选集”与现有 executable/router Pilot 的差异 |
| 双语文档新增后未被守护 | 把新项目级文档加入 `check_docs_bilingual.py` 的显式配对表 |
| 外部参考体系被误读为已验证兼容性 | 保留为非规范性参考族，不把名称列表升级成兼容性证明 |
| 未来真实运行需要高成本或外部权限 | 遵循现有 Evaluation Contract 的证据边界，另行授权和记录 run metadata |

## 11. 后续工作（不属于本次集成）

- 为五个 SQEM Pilot 候选补充或审查真实 Skill-local Eval suite。
- 创建 Quality Profile、Risk Profile、Behavior Contract 和 Evidence Report 实例。
- 在授权的 Agent/runtime 中执行代表性评测、benchmark 和兼容性采样。
- 根据 Pilot 结果提出 SQEM v1.1 变更，而不是在 v1.0 集成时预先宣布采用。
