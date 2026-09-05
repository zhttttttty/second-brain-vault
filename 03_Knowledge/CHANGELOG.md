---
description: 知识库操作与变更日志 — 记录 Ingest、Query 写回、维护和系统演化
type: system
tags: [知识管理/Obsidian]
updated: 2026-09-05
---
# CHANGELOG · 知识库操作与变更日志

> 记录知识库的每次实质变更：Ingest、Query 写回、Lint/维护、卡片与主题变更、归档，以及影响知识行为的系统规则变化。
> 目的：让「知识从哪来、何时改的」可追踪，AI 开会话时先读这里快速定向。
> 格式：在日期标题下使用 ``- `类型` | 内容 | 关联``；类型优先使用 `ingest`、`query`、`lint`、`知识更新`、`系统变更`。日期按倒序排列，同一天只保留一个标题。

## 2026-09-05

- `ingest` | 整合《把 Obsidian 当做知识库，浪费了它 90% 的能力》：强化“面向调用、更新优先、个人增量、语义连接”，新增内容准入清单，并为 6 类模板增加可选 `use_when` | [[01_Topics/Knowledge_System_Building|知识体系构建]]、[[_EXAMPLE_model_知识体系是关系集合]]、[[_EXAMPLE_checklist_内容是否值得进入知识库]]

## 2026-08-31

- `系统变更` | 增加 LLM Wiki 持续积累闭环：统一 Ingest / Query 写回技能、知识内容索引，并将 CHANGELOG 扩展为操作日志 | [[INDEX]]、`.agents/skills/llm-wiki/`

## 2026-08-30

- `入口收敛` | 将 AI 规则入口收敛为单一实体 `AGENTS.md`，移除小写源文件与根目录符号链接，并同步 Skills、脚本、README、快速开始、兼容说明和严格校验 | `AGENTS.md`、`System/Agent_Skills_Compatibility.md`、`.agents/skills/system-sync/`
- `文档重构` | README 改为以当前库内容为准的使用说明，统一架构、工作流、18 个 Skills、23 种模板、兼容性、校验与隐私边界，移除版本堆叠和过时工具推荐 | `README.md`
- `架构迁移` | 将编号目录收敛为 `01_Daily` 至 `06_Archive` 的内容生命周期；`Context`、`System`、`Bases`、`Templates` 改为无编号支撑层，并同步 Agent、Skills、Obsidian 配置、Base、Canvas、脚本和说明文档 | `agent.md`、`System/Vault_Map.md`、`.agents/scripts/migrate-vault-layout.ps1`
- `模板集中` | Daily、Project 与 23 种 Cards 模板迁入根目录 `Templates`，作为唯一模板源；移除各内容目录中的分散 `.templates` | `Templates/`、`.obsidian/templates.json`、`.obsidian/daily-notes.json`
- `平台层增强` | 接入 kepano/obsidian-skills 的分层约定，固定上游提交并明确多 Agent、Claude 兼容入口与 Obsidian CLI 安全边界 | `.agents/upstream-skills.yaml`、`00_System/Agent_Skills_Compatibility.md`
- `网页捕获` | 新增默认只预览、确认后写入的 `capture-web` 技能，将 Defuddle 抽取结果送入 Inbox，再交给 `digest` | `.agents/skills/capture-web/`、`.agents/skills/digest/SKILL.md`
- `Base 现代化` | 5 个 Base 改用 Properties 过滤与当前 `properties` / `views` / `order` Schema，移除旧式 columns、sort 和 Handlebars 字段 | `07_Bases/`
- `Canvas 导航` | 新增 Vault 架构与知识体系工作流两个可选 Canvas；Markdown 保持唯一事实来源 | `00_System/Vault_Architecture.canvas`、`04_Knowledge/01_Topics/Knowledge_System_Workflow.canvas`
- `校验增强` | 盘点加入 Canvas，校验器新增 Base YAML、模板属性、公式引用和 JSON Canvas 完整性检查 | `.agents/skills/system-sync/scripts/`
- `溯源规范` | 多来源卡片改用包含 Wikilink 或 URL 的命名脚注，避免不可点击的模糊来源标记 | `00_System/Writing_Rules.md`、`.agents/skills/knowledge-system/SKILL.md`

## 2026-08-29

- `系统增强` | 增加确定性 Vault 校验脚本与 GitHub Actions，检查 YAML、标签、related 类型、模板映射、文档计数和跨平台 Agent 入口 | `.agents/skills/system-sync/scripts/validate_vault.py`、`.github/workflows/validate-vault.yml`
- `示例修复` | 修正 5 张示例卡中未加引号的 related Wikilink，避免被 YAML 解析为嵌套数组 | `04_Knowledge/00_Cards/_EXAMPLE_*.md`
- `文档澄清` | 将 23 种模板区分为原子知识、实体资源与导航实践类型，并明确 AI 规则、溯源和质量信号的能力边界 | `README.md`、`agent.md`、`00_System/`
- `兼容性增强` | 补充 Windows 软链自检、跨 Agent 协议差异和 Obsidian 专属能力的迁移边界 | `QUICK_START.md`、`README.md`
- `规则优化` | 参考中文个人知识库标签框架，将标签收敛为 1～3 个中文层级主题；类型、来源、状态改由 Properties 表达，并同步模板、示例与 Skills | `00_System/Vault_Schema.md`、`04_Knowledge/00_Cards/.templates/`
- `系统修复` | 对齐 Daily Note 与附件的 Obsidian 配置 | `.obsidian/daily-notes.json`、`.obsidian/app.json`
- `规则修复` | 明确标签分类法适用范围，补充 `task` 形态标签与 CHANGELOG 记录边界 | `00_System/Vault_Schema.md`
- `模板修复` | 23 种卡片模板与 Daily/Project 模板的占位 frontmatter 改为合法 YAML | `04_Knowledge/00_Cards/.templates/`
- `Base 修复` | 对齐 Books、Persons、Resources、Subscriptions 与对应卡片字段 | `07_Bases/`
- `技能修复` | `card-creator` 接入 Schema/CHANGELOG；`onboard` 与 `system-sync` 修复 `agent.md` 路径并增加跨平台 Python 助手 | `.agents/skills/`

## 2026-08-28

- `初始化` | 从 DailyUp Second Brain + 「1小时构建知识体系」方法论创建本模板库
- `新增技能` | knowledge-system（六步法：提炼模型→按关系组体系→存储可追溯知识）
- `新增卡片类型` | `model`（4-5 字认知模型，四要素 + 溯源）
- `新增示例` | 3 张 model 卡片 + 元主题「知识体系构建」+ 方法论落点映射
