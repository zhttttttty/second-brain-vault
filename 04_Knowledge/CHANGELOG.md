---
description: 知识库变更日志 — 每次写入知识库都追加一条
type: system
tags: [知识管理/Obsidian]
updated: 2026-08-29
---
# CHANGELOG · 知识库变更日志

> 记录知识库的每次实质变更：新增了什么卡片、更新了哪个主题、归档了什么、消化了哪篇剪藏。
> 目的：让「知识从哪来、何时改的」可追踪，AI 开会话时先读这里快速定向。
> 格式：`日期 | 类型 | 内容 | 关联`，按时间倒序（最新在上）。

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
