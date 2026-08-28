---
description: 领域范围、标签分类法、建卡门槛与质量信号约定
tags: [system, schema, taxonomy]
updated: 2026-08-29
---
# Vault Schema

> 这是知识库的「领域契约」：约束 AI 行为、保证长期一致性的单一来源。
> 建卡、写主题、打标签之前先读这里。灵感来自 Karpathy LLM Wiki 的 SCHEMA.md 模式。

## 领域范围（Domain）

> 本库覆盖什么、不覆盖什么。明确范围能帮 AI 判断「什么该收录、什么该忽略」。

- 当前核心领域：尚未设置；完成 `01_Context/About_Me.md` 与 `01_Context/Current_Priorities.md` 后再登记
- 明确不收录：一次性琐事、纯娱乐、与长期方向无关的内容

### 适用范围

本分类法约束 `01_Context/`、`02_Daily/`、`03_Projects/`、`04_Knowledge/`、`05_References/`、`06_Tasks/` 中的**正式内容**。

以下文件不参与领域标签校验：

- `.agents/`、`.github/`、`.obsidian/` 中的工具与配置文件
- `.templates/` 中尚未实例化的模板
- `README.md`、`Skills_Manual.md` 等导航说明
- `_EXAMPLE_*` 与 `_Example_Project/` 示例内容

这样既保持正式内容的标签一致性，也避免用知识分类法约束工具说明和模板占位符。

## 标签分类法（Tag Taxonomy）

> 目的：防止标签蔓延。所有文件的 `tags` 必须来自下表；需要新标签时，**先加到这里，再用**。

### 第一层 · 形态（文件类型，固定）

| 标签 | 含义 |
|------|------|
| `card` | 原子化知识卡片 |
| `daily` | 每日记录 |
| `project` | 项目 |
| `topic` | 长期主题地图 |
| `system` | 系统规则文件 |
| `context` | 个人背景与优先级 |
| `reference` | 外部剪藏 |
| `task` | 全局或独立任务 |

### 第二层 · 知识类型（对应卡片类型，固定）

`model` / `insight` / `mentalmodel` / `term` / `quote` / `book` / `book-note` / `person` / `tool` / `resource` / `opensource` / `course` / `prompt` / `checklist` / `tip` / `counterintuitive` / `paradox` / `question` / `story` / `moc` / `techstack` / `atomic-habit` / `subscription`

> 卡片类型到模板的映射见 `.agents/skills/card-creator/references/card-type-map.md`。

### 第三层 · 领域（自定义，先登记再用）

| 标签 | 含义 |
|------|------|
| `investment` | 投资与资产配置 |
| `knowledge-mgmt` | 知识管理与方法 |
| `learning` | 学习与认知 |
| `ai` | 人工智能 |
| （按需扩展） | |

> 规则：正式卡片的 `tags` 由「`card` + 知识类型 + 0～2 个领域标签」组成；其他正式内容使用对应形态标签，并可附 0～2 个领域标签。新领域标签先登记到这里，避免同义标签分裂（如同时出现 `ai`、`AI` 和 `人工智能`）。

不确定领域时宁可暂不添加，也不要把临时主题词直接升级为领域标签。具体关系优先使用正文链接与 `related`，不要用标签复制文件夹或链接结构。

## 建卡门槛（Create / Update / Don't create）

| 动作 | 触发条件 |
|------|---------|
| **新建卡片** | 一个概念/实体在 2+ 来源出现，或对单一来源至关重要 |
| **更新已有卡片** | 来源提到已覆盖的内容 → 追加知识点，不重复建卡 |
| **不建卡** | 顺带提及、次要细节、领域外内容 |
| **拆分卡片** | 单卡超过约 200 行 → 拆成子主题并交叉链接 |
| **归档卡片** | 内容被完全取代 → 移到 `20_Archive/`，从索引/MOC 移除 |

## 质量信号（可选 frontmatter）

> 让「弱断言不静默固化成事实」。观点密集或快速变化的领域尤其推荐填写。

```yaml
confidence: high | medium | low   # 该卡片主张的证据充分程度
contested: true                    # 存在未解决的矛盾时设 true
contradictions: [other-card-slug]  # 与之冲突的卡片
```

`lint` / `check-health` 会把 `confidence: low` 和 `contested: true` 的卡片列入待审，避免弱结论悄悄变成「公认事实」。

## 内容索引与变更日志

- **全库索引**：主题地图 `04_Knowledge/01_Topics/` + MOC 卡片
- **变更日志**：`04_Knowledge/CHANGELOG.md` — 记录新增/更新/归档知识，以及影响全库行为的系统规则变更；普通 Daily 与任务勾选不逐条记录
- **会话定向**：新会话先读本文件 → 索引/主题地图 → 最近变更日志（见 `agent.md`）
