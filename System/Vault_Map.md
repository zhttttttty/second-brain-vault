---
description: Visual map and overview of the vault structure
type: system
tags: [知识管理/Obsidian]
updated: 2026-08-31
---
# Vault Map

## 分层原则

- `01_Daily/` 至 `06_Archive/`：用户日常浏览和流转的工作内容，编号表达生命周期顺序。
- `Context/`、`System/`、`Bases/`、`Templates/`、`Attachments/`：支撑层，不参与内容流转排序。
- `Context/Current_Priorities.md` 会随阶段更新；无编号不等于永不修改。

## System
系统级规则与导航：

- `Vault_Schema.md` — 领域范围、标签分类法、建卡门槛、质量信号
- `Vault_Map.md` — 目录职责和内容路由
- `Task_Management_Rules.md` — Inbox、独立任务、项目任务与 Daily Note 的边界
- `Writing_Rules.md` — 表达、Markdown、Frontmatter、来源与附件规范
- `Naming_Conventions.md` — 文件、目录、项目和 Base 命名规范
- `Knowledge_Workflow.md` — 「1小时构建知识体系」方法论如何落到卡片/主题/项目
- `Agent_Skills_Compatibility.md` — Vault 工作流层与外部 Obsidian 平台技能的兼容边界
- `Vault_Architecture.canvas` — 系统规则、个人上下文和写回入口的空间导航

### 自动校验

- `.agents/skills/system-sync/scripts/vault_inventory.py` — 以统一口径盘点卡片、模板、技能、README、Base、Canvas、MOC 和附件
- `.agents/skills/system-sync/scripts/validate_vault.py` — 校验 Frontmatter、标签、`related`、模板映射、Base、Canvas、文档计数和 Agent 兼容入口
- `.agents/scripts/migrate-vault-layout.ps1` — 将旧编号结构安全迁移到当前布局；默认 Dry Run，`-Apply` 后执行
- `.github/workflows/validate-vault.yml` — 在 push / pull request 时运行同一套确定性校验

AI 的协作流程和写回原则统一维护在根目录 `AGENTS.md`，不在这里重复维护。

### 附件管理
- 所有附件存放到对应目录下的 `Attachments/` 文件夹
- `.obsidian/app.json` 已设置 `./Attachments`，与该规则保持一致
- 见 `Writing_Rules.md` 中的"附件管理规则"章节

## Context
长期稳定背景与当前动态重点：

- `About_Me.md` — 我是谁、长期方向、AI 协作偏好，以及可选的受众与表达风格
- `Current_Priorities.md` — 当前目标、重点、活跃项目、关键问题和暂时不做

默认只维护这两个文件。受众、品牌或使命内容增长到明显需要独立维护时，再按需拆分。

## 01_Daily
每日记录、会话摘要、临时想法、最近进展

`.obsidian/daily-notes.json` 已将 Daily Note 固定到 `01_Daily/`，并使用 `Templates/Daily_Note.md`。模板只保留三个栏目：
- `今日重点` — 当天选择的 1～3 个关注点
- `今日记录` — 进展、问题、决定、输入和想法的统一记录区
- `一句话总结` — 可选的日终收束

## 02_Projects
具体项目资料，按项目组织

### 项目文件结构
每个项目默认只有一个核心文件：
- `Project.md` — 项目定义、完成标准、状态、下一步、Backlog、里程碑、进展与决策

### 项目产出目录（按需创建）
- `Outputs/` — 文章、方案、课程材料、设计稿等真实产出；出现第一份产出时再创建
- 内容明显增多后，可在 `Outputs/` 下按需拆分 `Docs/`、`Assets/`、`Meetings/` 等目录

### 项目模板
项目模板为 `Templates/Project.md`。新建项目时只复制这一文件，不预建空目录。

## 03_Knowledge
长期知识沉淀与主题连接
- `00_Cards/` — 标准化知识卡片与实体卡片
- `01_Topics/` — 长期关注领域的知识地图与阶段性理解
  - 默认一个主题对应一个文件，内容增长后再按需升级为目录
  - 通过链接连接卡片、项目和来源，不复制保存原始材料
  - `Knowledge_System_Workflow.canvas` — 六步法从输入、提炼到卡片与主题组装的可视导航
- `INDEX.md` — 面向内容的统一入口；知识查询先从这里定位 Topic 和卡片
- `CHANGELOG.md` — Ingest、Query 写回、Lint/维护和系统演化记录

方法论不单设目录：原理进入 `model` 或 `mentalmodel` 卡片，人工步骤进入 `checklist` 卡片，AI 可执行流程进入 `.agents/skills/`。知识体系构建方法已固化为 `.agents/skills/knowledge-system/`；来源整合和知识查询写回由 `.agents/skills/llm-wiki/` 维护。

卡片模板中的 frontmatter 占位值保持为合法 YAML；最终卡片必须由 `card-creator` 或人工完整替换占位符后再进入正式卡片目录。

## 04_References
外部剪藏的收集、消化与精选原文保留

### 目录结构
- `01_Inbox/` — 尚未判断或消化的剪藏
- `02_Library/` — 已消化且原文本身值得长期保留的精选文章

### 工作流程
网页 URL 可先由 `capture-web` 调用 Defuddle 预览，用户确认后写入 Inbox；已有剪藏直接进入 `digest`。需要持续整合进知识层时使用 `llm-wiki`：比较已有页面 → 更新卡片与 Topic → 更新 INDEX → 记录 CHANGELOG。来源正文捕获后不改写；原文进入 Library 或删除仍需单独确认。主题通过标签和链接表达，不建立分类目录。

## 05_Tasks
全局任务入口与非项目任务管理：
- `Inbox.md` — 尚未分类的新任务，定期处理并尽量清空
- `Tasks.md` — 不属于具体项目的下一步、等待事项和以后可能

项目任务保留在对应项目的 `Project.md`；Daily Note 只记录当天的选择和执行结果。

## 06_Archive
已经退出 Daily、Projects、Knowledge、References 或 Tasks 活跃工作流，但因追溯、复用或合规需要仍应保留的历史内容。默认不参与会话定向和日常搜索。

## Templates
模板的单一来源：

- `Daily_Note.md` — Daily Note 模板
- `Project.md` — 单页项目模板
- `Cards/` — 23 种标准化卡片模板：`model`, `insight`, `counterintuitive`, `paradox`, `question`, `story`, `quote`, `term`, `mentalmodel`, `book`, `book-note`, `person`, `resource`, `tool`, `opensource`, `course`, `subscription`, `prompt`, `checklist`, `tip`, `moc`, `techstack`, `atomic-habit`

`.obsidian/templates.json` 指向根目录 `Templates/`。模板只负责生成内容，不作为正式卡片、项目或日记参与统计。

## Bases
Obsidian Base 数据库视图

### 内容型 Base（集中式）
跨目录聚合的知识实体数据库，需要全库视角访问：
- `Resources.base` — 资源合集
- `Persons.base` — 人物卡片
- `Books.base` — 藏书管理
- `Opensource.base` — 开源项目
- `Subscriptions.base` — 订阅追踪

**特点：** 通过 `type` / `card_type` Properties 和卡片目录过滤，Base 与内容分离，不依赖文件名前缀

### 新建 Base 的判断规则
问自己：这个 Base 是"全库视角"还是"领域视角"？
- 全库 → 放在 `Bases/`
- 领域 → 嵌入对应子目录

Base 的列名必须与对应卡片模板 frontmatter 同步；新增或重命名属性时同时检查 `Bases/*.base`。

Base 使用当前 Obsidian Schema 的 `properties`、`views` 和 `order`；不要重新引入旧式 `columns`、`sort` 或 Handlebars 展示字段。Base 仅是视图，卡片 Markdown 与 Properties 才是事实来源。
