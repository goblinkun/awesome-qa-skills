# Skill Quality Engineering Toolkit v1.0 集成实施计划

<div align="right"><strong>🇨🇳 中文</strong> | <a href="./2026-09-28-skill-quality-engineering-toolkit-integration_EN.md">🇬🇧 English</a></div>

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将已审阅的 SQET v1.0 Toolkit 以符合仓库双语、证据和治理约定的方式集成到 `awesome-qa-skills`，不新增可安装 Skill 或未经执行的质量声明。

**Architecture:** 新增 `docs/skill-quality-engineering/` 作为 SQEM、Eval Contract、Pilot 和模板的文档入口；根级 `evals/` 与 `evidence/skill-quality/` 只提供导航和证据边界说明。现有 Quality Score、Evidence Contract、Quality Loop、Skill-local Eval 和既有 Pilot 保持事实来源，不做迁移或覆盖。

**Tech Stack:** Markdown、Python 3 项目校验脚本、Bash 质量门禁、Git Conventional Commits。

**Spec:** `docs/superpowers/specs/2026-09-28-skill-quality-engineering-toolkit-integration-design.md`（英文镜像：`docs/superpowers/specs/2026-09-28-skill-quality-engineering-toolkit-integration-design_EN.md`）

## Global Constraints

- SQET 不是 `skills/` 下可安装的 Agent Skill。
- 项目级文档使用 `NAME.md`（中文）和 `NAME_EN.md`（英文）；核心入口和三组核心文档必须双向切换。
- 现有 `NOT_RUN`、`NOT_SCORED`、`UNASSESSED`、`INSUFFICIENT_EVIDENCE` 语义保持不变；`PARTIAL` 不新增为仓库级状态。
- `docs/governance/QUALITY_SCORE_EVAL_CONTRACT*` 继续独占 Quality Score；不新增评分维度。
- Skill-local `skills/{zh,en}/.../evals/` 继续是 Eval case 的默认事实来源；根级 `evals/` 不复制用例。
- 五个 SQEM Pilot 仅作为方法论 Pilot 候选集，不替换 `requirements-analysis`、`ui-test-playwright` 和 `discover-testing` 的既有 Pilot 记录。
- 本阶段不添加真实模型输出、目标环境结果、benchmark、compatibility、production 或 release approval 证据。
- 不修改、不删除、不重命名现有治理文档；不提交生成报告、缓存、密钥或无关文件。
- 文档类任务以确定性结构、链接、状态和质量脚本作为测试周期；不为静态文档引入运行时依赖。

## Review Focus

- **Status drift:** 导入附件示例时不能把 `PARTIAL` 变成新的 gate 状态；用状态映射和 `rg` 检查绑定到 Task 1。
- **Duplicate Eval source:** 根级 `evals/README.md` 必须声明 Skill-local Eval 是事实来源；用内容断言绑定到 Task 2。
- **Pilot replacement:** 新 Pilot 文档不能覆盖现有 analysis/executable/router Pilot；用精确文件清单和 `git diff --name-only` 绑定到 Task 1/4。
- **Bilingual discoverability:** 每个新项目级文档必须有双向切换，且被 `check_docs_bilingual.py` 注册；用单元测试和完整校验绑定到 Task 3/4。
- **Evidence overclaim:** 入口和 Pilot 不能把静态校验写成 runtime 或生产证明；用关键词审查与人工 diff review 绑定到 Task 1/2/4。

---

### Task 1: 导入并适配 SQET 核心文档与模板

**Files:**
- Create: `docs/skill-quality-engineering/README.md`
- Create: `docs/skill-quality-engineering/README_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_EVAL_CONTRACT.md`
- Create: `docs/skill-quality-engineering/SKILL_EVAL_CONTRACT_EN.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_PILOT.md`
- Create: `docs/skill-quality-engineering/SKILL_QUALITY_PILOT_EN.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_BEHAVIOR_CONTRACT_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_EVIDENCE_REPORT_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_QUALITY_CI_GUIDE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_QUALITY_PROFILE_TEMPLATE.md`
- Create: `docs/skill-quality-engineering/templates/SKILL_RISK_PROFILE_TEMPLATE.md`
- Source: `awesome-qa-skills-skill-quality-engineering-toolkit-v1.0/docs/skill-quality-engineering/{en,zh}/`（附件仅作内容来源，不把其路径写入仓库）

**Interfaces:**
- Consumes: 已审阅的 SQET spec、附件的三组中英文核心文档和五个模板、现有治理状态与 Pilot 契约。
- Produces: 可独立阅读的双语 SQET 入口、三组核心文档和五个不含凭据的模板；后续 Task 2/3 只依赖这些稳定路径。

- [ ] **Step 1: 创建项目级双语入口**

创建中文默认 `README.md` 和英文 `README_EN.md`，列出 SQEM、Eval Contract、Pilot、五个模板，并明确 SQET 与 `skills/skill-engineering/` 的区别。入口必须写明现有 Quality Score、Evidence Contract、Quality Loop、Skill-local Eval 和既有 Pilot 的事实来源；说明当前状态为 Pilot validation，不是全仓库 runtime quality 或 release approval。

- [ ] **Step 2: 导入三组核心文档并应用最小适配**

将附件 `en/` 与 `zh/` 的三组核心文档分别落为仓库的 `NAME.md` / `NAME_EN.md` 文件。保留 SQEM 七个质量域、L1-L4、E1-E4、Risk Profile、Quality Profile、Quality Claim Gate、Eval Case 类型和五个 Pilot 候选；补充仓库现有 Router `skill.selection` / `selected_skills` 证据规则和现有 Evidence Contract 的引用边界。

- [ ] **Step 3: 修正状态和 Pilot 语义**

将附件质量档案中的 `PARTIAL` 处理为 `INSUFFICIENT_EVIDENCE`、`UNASSESSED` 或逐项说明；保留并解释 `NOT_SCORED`。在 Pilot 文档中明确五个 SQEM 候选只是方法论 Pilot，不替换 `requirements-analysis`、`ui-test-playwright` 和 `discover-testing` 的既有记录；无真实 Agent/目标环境/跨模型/业务证据时保持 `NOT_RUN`、`BLOCKED` 或 `INSUFFICIENT_EVIDENCE`。

- [ ] **Step 4: 复制五个语言中性模板**

导入 Behavior Contract、Evidence Report、Quality CI、Quality Profile、Risk Profile 五个模板，保留空字段和示例结构，不填入真实 Skill 结果、模型、凭据、路径或运行结论。

- [ ] **Step 5: 运行文档静态检查**

Run: `git diff --check`

Expected: exit 0，且 `rg -n 'TODO|TBD|Bearer|/Users/|/home/' docs/skill-quality-engineering` 无输出。人工检查新增文档只声明方法论和边界，不把配置有效性写成 runtime 证明。

- [ ] **Step 6: Commit**

```bash
git add docs/skill-quality-engineering
git commit -m "docs(sqet): add toolkit methodology docs"
```

### Task 2: 添加根级 Eval 与 Evidence 导航边界

**Files:**
- Create: `evals/README.md`
- Create: `evals/README_EN.md`
- Create: `evidence/skill-quality/README.md`
- Create: `evidence/skill-quality/README_EN.md`

**Interfaces:**
- Consumes: Task 1 的 SQET 入口和 spec 中的事实来源映射。
- Produces: 根级目录说明，供 Task 3 注册双语检查并由最终门禁验证；不产生 Eval case 或 Evidence Report。

- [ ] **Step 1: 创建 Eval 双语 README**

写明 Skill-local `eval.yaml` / cases 是默认事实来源；根级目录未来只能承载经过单独设计的 runner-adapted、跨 Skill 或汇总资产；不移动或复制现有用例。

- [ ] **Step 2: 创建 Evidence 双语 README**

写明证据至少应记录 Skill commit/version、Eval version、engine/model、judge、environment、timestamp、result、limitations，以及证据支持和不支持的质量声明。本阶段只创建说明，不创建报告。

- [ ] **Step 3: 绑定根目录边界检查**

Run: `rg -n 'Skill-local|事实来源|source of truth|NOT_RUN|limitations|支持|不支持' evals/README.md evals/README_EN.md evidence/skill-quality/README.md evidence/skill-quality/README_EN.md`

Expected: 双语 README 都包含“本地 Skill Eval 为事实来源”和“未执行内容不能升级为质量结论”的语义；目录中不存在 `eval.yaml`、case 或 Evidence Report 实例。

- [ ] **Step 4: Commit**

```bash
git add evals/README.md evals/README_EN.md evidence/skill-quality/README.md evidence/skill-quality/README_EN.md
git commit -m "docs(sqet): add eval and evidence entrypoints"
```

### Task 3: 注册双语校验并更新仓库入口

**Files:**
- Modify: `scripts/check_docs_bilingual.py` (`PROJECT_PAIRS`)
- Modify: `scripts/tests/test_check_docs_bilingual.py`
- Modify: `README.md:16`
- Modify: `README_EN.md:16`

**Interfaces:**
- Consumes: Task 1/2 创建的路径和双向切换链接。
- Produces: `check_docs_bilingual.py` 对 6 组新增项目文档进行存在性、双向切换和相对链接校验；根 README 提供 SQET 入口但不把它列为可安装 Skill。

- [ ] **Step 1: 添加双语项目文档配对回归测试**

在 `scripts/tests/test_check_docs_bilingual.py` 添加一个测试，断言以下 6 个 tuple 都存在于 `PROJECT_PAIRS`：

```text
("docs/skill-quality-engineering/README.md", "docs/skill-quality-engineering/README_EN.md")
("docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL.md", "docs/skill-quality-engineering/SKILL_QUALITY_EVALUATION_MODEL_EN.md")
("docs/skill-quality-engineering/SKILL_EVAL_CONTRACT.md", "docs/skill-quality-engineering/SKILL_EVAL_CONTRACT_EN.md")
("docs/skill-quality-engineering/SKILL_QUALITY_PILOT.md", "docs/skill-quality-engineering/SKILL_QUALITY_PILOT_EN.md")
("evals/README.md", "evals/README_EN.md")
("evidence/skill-quality/README.md", "evidence/skill-quality/README_EN.md")
```

- [ ] **Step 2: 注册 6 组项目文档配对**

将上述 tuple 加入 `PROJECT_PAIRS`，保持唯一，不把五个语言中性模板加入项目级双语配对。

- [ ] **Step 3: 更新根 README 快速入口**

在 `README.md` 的中文快速入口加入 `docs/skill-quality-engineering/README.md`，在 `README_EN.md` 的英文 Quick links 加入对应 `_EN.md`；不要修改 Skill 数量、安装命令或 Skill catalog 计数。

- [ ] **Step 4: 运行定向测试**

Run: `python3 -m unittest discover -s scripts/tests -p 'test_check_docs_bilingual.py' -v`

Expected: 所有测试 PASS，新增配对测试能阻止未来移除 SQET 文档注册。

- [ ] **Step 5: 运行双语校验**

Run: `python3 scripts/check_docs_bilingual.py --repo-root .`

Expected: `bilingual_docs_findings=0`，同时新增文档的所有相对 Markdown 链接可解析。

- [ ] **Step 6: Commit**

```bash
git add README.md README_EN.md scripts/check_docs_bilingual.py scripts/tests/test_check_docs_bilingual.py
git commit -m "docs(sqet): register bilingual toolkit entrypoints"
```

### Task 4: 全量质量门禁与交付前审查

**Files:**
- Test only: all Task 1-3 changed files
- Review only: `git status`, `git diff --stat`, and the committed file list

**Interfaces:**
- Consumes: Task 1-3 的提交和验证结果。
- Produces: 可复核的最终静态质量证据；不 push、不创建 runtime evidence、不修改无关生成文件。

- [ ] **Step 1: 检查提交范围**

Run: `git status --short --branch` and `git diff origin/develop...HEAD --name-status`

Expected: 只有 SQET spec/plan（已存在）与本次 Toolkit 文档、根入口、双语校验脚本/测试相关文件；没有 Skill 内容、现有治理 Pilot、缓存、密钥或生成报告的无关变更。

- [ ] **Step 2: 运行仓库全量质量门禁**

Run: `bash scripts/check_skills_quality.sh`

Expected: exit 0；Skill CLI compatibility、Skill integrity、Evaluation Quality Loop contract、bilingual docs、local rule catalog 和脚本单测均通过。Toolkit 不应改变 Skill 数量或安装兼容性。

- [ ] **Step 3: 运行最终格式和边界检查**

Run: `git diff --check`

Expected: exit 0；再人工检查新入口没有未经执行的 `PASS`、benchmark、runtime、compatibility、production 或 release approval 声明。

- [ ] **Step 4: 记录交付状态**

Run: `git status --short --branch` and `git log -4 --oneline --decorate`

Expected: 工作区干净；实现提交已存在于当前分支；不执行 `git push`，除非用户另行明确要求。

## Plan self-review

- **Spec coverage:** Spec 的目录结构由 Task 1/2 覆盖；事实来源、状态映射和 Pilot 共存由 Task 1 覆盖；双语守护和根入口由 Task 3 覆盖；验收标准和风险由 Task 4 的定向/全量检查覆盖。
- **Step scan:** 每个步骤只有一个可检查结果；文档复制、语义适配、测试注册、入口更新和质量门禁没有混成不可审查的大步骤。
- **Type consistency:** 所有路径使用最终 `NAME.md` / `NAME_EN.md` 命名；`PROJECT_PAIRS` 的 6 组路径与 Task 1/2 创建的文件完全一致。
- **Review focus coverage:** 五类风险分别绑定到 Task 1、Task 2、Task 3 和 Task 4 的状态、内容、单元、全量和人工审查。
- **Proportion:** 计划只决定文件、适配规则、验证命令和提交边界，不重写附件文档正文或预先实现未来 Pilot。
