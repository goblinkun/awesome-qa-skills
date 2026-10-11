# 独立 Skill 的公共脚本源 / Shared script sources

这些文件是维护副本的 canonical source，不是 leaf Skill 的运行依赖。修改后将对应文件复制到使用它的 `scripts/`，再运行 `python3 scripts/check_review_resource_copies.py` 和相关回归测试。安装 Skill 只复制包内资源，不自动执行脚本。

These files maintain identical copies; leaf Skills import their own local files. After a change, copy the source into each affected package, run `python3 scripts/check_review_resource_copies.py`, and exercise the relevant regressions. Installing a Skill copies resources without executing scripts.
