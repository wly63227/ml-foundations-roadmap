# 土木工程转机器学习 · 16 周学习路线

数学学过但有些遗忘？从自测恢复记忆，把主要时间用在编程、模型理解和实验上。每周 8–10 小时，数学集中复习 3 周。

- [在线阅读](https://wly63227.github.io/ml-foundations-roadmap/)
- [从这里开始](教材/docs/index.md) · [前置知识清单](教材/docs/checklist.md) · [45 分钟自测](教材/docs/diagnostic.md)
- [16 周总表](教材/docs/roadmap.md) · [第 1 周](教材/docs/weeks/01.md) · [学习记录模板](教材/docs/tracker.md)
- [环境与代码说明](教材/docs/setup.md) · [验收与发布状态](教材/docs/audit.md) · [恢复点](教材/进度.md)

## 本地阅读与验证

网站构建需要 Node.js 22 与 pnpm 10。仅阅读仓库 Markdown 无需安装。

```powershell
pnpm install --frozen-lockfile
pnpm build
pnpm check
```

学习代码使用 Python 3.12。先建立独立虚拟环境，避免影响已有课程环境：

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-ml.txt
.venv/Scripts/python.exe -m pip install -r requirements-torch.txt
.venv/Scripts/python.exe 教材/scripts/verify_math.py
.venv/Scripts/python.exe 教材/scripts/examples.py all
.venv/Scripts/python.exe -m http.server 8766 --bind 127.0.0.1 --directory 教材/site
```

macOS/Linux 把 `.venv/Scripts/python.exe` 换为 `.venv/bin/python`。浏览器打开 `http://127.0.0.1:8766/`。前两周的示例只需 Python 标准库；第 3 周安装科学计算依赖，第 11 周再装 CPU 版 PyTorch。

## 内容与维护

`教材/docs/` 是唯一正文；`教材/scripts/` 保存构建、检查及自编实验；`教材/site/`、`教材/reports/` 为生成目录，不提交。所有周计划和打卡均从未完成开始。网页上的复选框用于呈现记录，不会自动保存或同步 GitHub；请修改 Markdown 后提交。

`main` 更新后，Actions 执行数学、实验、链接与构建检查，再发布 Pages；`version.json` 标识线上提交。本仓库只发布原创学习组织、说明、自编练习及代码，不包含原始课件和参考书。不将本计划解释为教师教学范围或算法岗就业保证。

部署成功后，可用 `python 教材/scripts/check_public.py --expected-commit COMMIT_SHA --external` 核对线上版本、全部正文页面和资源外链；将 `COMMIT_SHA` 替换为该次提交的完整 SHA。检查结果保存在 `教材/reports/public.json`。
