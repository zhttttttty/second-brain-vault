---
description: Vault 工作流技能与外部 Obsidian 平台技能的分层和兼容说明
type: system
tags: [知识管理/Obsidian, 技术/Agent]
updated: 2026-08-30
---
# Agent Skills Compatibility

## 两层技能，不重复维护

本 Vault 将技能分成两层：

1. **工作流层**：`.agents/skills/` 中的技能定义“为什么做、何时确认、写到哪里”，随 Vault 一起版本控制。
2. **平台能力层**：[`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) 定义 Markdown、Bases、Canvas、Obsidian CLI 和网页抽取的通用操作，由具体 Agent 在外部安装。

外部技能不复制到 `.agents/skills/`，避免两份上游代码漂移。固定来源、提交版本和依赖级别记录在 `.agents/upstream-skills.yaml`。

## 依赖级别

| 技能 | 级别 | 在本 Vault 中的用途 |
|---|---|---|
| `obsidian-markdown` | 必需 | 写入 Properties、Wikilinks、嵌入、callout 和脚注 |
| `obsidian-bases` | 必需 | 维护 `Bases/*.base` |
| `json-canvas` | 可选 | 维护两个导航 Canvas；Markdown 仍是唯一事实来源 |
| `obsidian-cli` | 可选 | Obsidian 已运行且 CLI 可用时做实时查询、重载和界面验证 |
| `defuddle` | 可选 | 为 `capture-web` 提取网页正文 |

缺少可选技能时，核心 Markdown 知识库仍可使用；相关增强流程应明确报告缺失能力，而不是伪造执行结果。

## 多 Agent 安装原则

- 根目录 `AGENTS.md` 是项目规则的唯一实体文件，也是 Codex 的自动发现入口；不再保留小写副本或符号链接。不能自动识别该名称的 Agent，应在首次接入时显式读取此文件。
- 各 Agent 的技能安装目录和发现协议不同，按上游仓库针对该 Agent 的说明安装。
- 支持 Agent Skills 规范的工具可从 `npx skills add https://github.com/kepano/obsidian-skills` 开始，并在交互中选择目标 Agent；不要默认写入某个未经确认的用户目录。
- Codex 的全局技能通常位于用户级 skills 目录，不会随着 Vault 的 Git 仓库分发。
- Claude 兼容入口 `.claude/skills` 仅指向本 Vault 的工作流层；它不是上游平台技能的副本。
- 升级上游前先更新 `.agents/upstream-skills.yaml` 的 `ref`，再运行本 Vault 校验并在 Obsidian 中抽查 Bases/Canvas。

## Obsidian CLI 安全边界

- 只有在 `obsidian` 命令可用且 Obsidian 桌面端正在运行时才调用 CLI。
- 多 Vault 环境必须显式指定 `vault="<名称>"`，不要依赖当前焦点。
- 批量文件迁移优先在 Obsidian 关闭时通过文件系统完成；不要让 CLI 与另一个进程同时改写同一批文件。
- CLI 不可用时，使用本仓库的确定性校验脚本；不得把“未实时验证”表述为“已在 Obsidian 验证”。

## 单一事实来源

- Markdown 文件保存知识、规则和说明。
- Base 只提供基于 Properties 的数据库视图。
- Canvas 只提供空间导航和关系概览。
- Skills 只定义操作流程，不复制正式知识内容。
