---
title: Knowledge Directory
description: 长期知识卡片与主题地图
created: 2026-04-23
updated: 2026-08-31
type: system
tags: [知识管理/Obsidian]
---
# Knowledge

`03_Knowledge/` 保存经过整理、值得长期复用的知识。

## 目录结构

```text
03_Knowledge/
├── 00_Cards/      # 原子化知识卡片
├── 01_Topics/     # 长期主题地图
├── INDEX.md       # 面向内容的统一入口
├── CHANGELOG.md   # Ingest、Query 写回与维护记录
└── README.md
```

## LLM Wiki 闭环

```text
外部来源 → 捕获 / 消化 → Ingest
                         ├─ 更新已有卡片
                         ├─ 更新 Topic 当前理解
                         ├─ 维护交叉链接
                         ├─ 更新 INDEX
                         └─ 记录 CHANGELOG

知识问题 → 先读 INDEX → 聚焦检索 → 带依据回答
                                   └─ 有长期价值且用户确认 → 写回 Wiki
```

`llm-wiki` Skill 负责这个闭环。来源正文保留在 `04_References/`，捕获后不被知识整理流程改写；新的理解和修订进入卡片或 Topic。

## 00_Cards

一张卡片聚焦一个可以独立引用的概念、观点、模型、清单、人物或资源。

`Templates/Cards/` 提供 23 种卡片模板。常见方法论按形态处理：

- 提炼出的 4-5 字认知模型（世界观/方法论）→ `model` 卡片
- 原理或思考模型 → `mentalmodel` 卡片
- 人可直接执行的步骤 → `checklist` 卡片
- 用来指导 AI 执行的完整流程 → `.agents/skills/`

## 01_Topics

Topic 是长期关注领域的知识地图，用于维护主题范围、核心问题、阶段性理解，以及相关卡片、项目和来源之间的连接。

默认从单个主题文件开始，不预建复杂目录。详见 [[01_Topics/README|Topics 使用说明]]。

## 内容路由

| 内容 | 位置 |
|---|---|
| 单个概念、观点、模型或清单 | `00_Cards/` |
| 长期领域的知识地图与综合理解 | `01_Topics/` |
| 有目标、期限或完成标准的工作 | `02_Projects/` |
| 外部文章和原始资料 | `04_References/` |
| AI 可执行的完整流程 | `.agents/skills/` |

网上剪藏先进入 `04_References/01_Inbox/`；消化后形成卡片、Topic 更新、项目决定或行动。原文本身值得长期保留时才进入 `04_References/02_Library/`。

## 相关文档

- [[INDEX|Knowledge Index]] — 内容索引与查询入口
- [[CHANGELOG]] — Ingest、Query 写回和维护记录
- [[../System/Vault_Map|Vault Map]] — 整体仓库结构
- [[../System/Writing_Rules|Writing Rules]] — 写作规范
