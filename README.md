# DailyUp Second Brain Starter

> 一套面向长期人机协作的中文 Obsidian 第二大脑模板。
> 用 Markdown 保存知识，用明确的规则约束 AI，用 Git 记录系统演化。

[快速开始](QUICK_START.md) · [技能手册](Skills_Manual.md) · [库地图](System/Vault_Map.md) · [结构规范](System/Vault_Schema.md) · [贡献指南](CONTRIBUTING.md)

## 项目概览

这个仓库不是一套“漂亮文件夹”，而是一套可直接复制、逐步裁剪的知识工作系统。它把日常记录、项目推进、知识沉淀、外部资料、任务管理和 AI Agent 协作放在同一套可验证的规则中。

当前示例库包括：

- **23 种标准化卡片模板**，覆盖观点、模型、概念、人物、工具、书籍、论文等常见知识对象
- **18 个 Vault 工作流 Skills**，覆盖初始化、计划、阅读、提炼、思考、复习与系统维护
- **9 张示例知识卡片**，用于展示属性、标签、链接、溯源和质量信号
- **5 个 Obsidian Bases 视图**，用于查看卡片、书籍、人物、资源与复习队列
- **2 个 Canvas**，用于说明库架构和知识体系工作流
- Daily、Project 与 Card 模板，以及可重复执行的迁移和校验脚本

核心内容全部使用 Markdown、YAML、Wikilinks、Bases 和 Canvas 等 Obsidian 原生格式；不依赖 Dataview 或 Tasks 才能运行。

## 核心设计

### 1. 内容区与支撑区分离

| 区域 | 目录特征 | 用途 | 变更频率 |
| --- | --- | --- | --- |
| 内容区 | 数字编号 | 日记、项目、知识、资料、任务和归档 | 高频 |
| 支撑区 | 无编号 | 个人上下文、系统规则、视图、模板和附件 | 低频或按需 |
| Agent 层 | 点目录与根文件 | AI 行为契约、Skills 与平台兼容入口 | 随系统演化 |

`Context/` 与 `System/` 刻意分开：前者回答“我是谁、现在关注什么”，后者回答“这个库按什么规则运行”。这样既保留隐私边界，也便于升级模板时分别处理个人数据和系统规则。

### 2. 四种组织机制各司其职

| 机制 | 负责表达 | 不负责表达 |
| --- | --- | --- |
| 文件夹 | 工作流阶段与物理位置 | 主题分类 |
| Tags | 1～3 个受控中文主题 | 类型、状态、来源 |
| Properties | `type`、`card_type`、`status`、`source` 等结构化属性 | 自由主题关联 |
| Wikilinks | 笔记之间的语义关系 | 工作流状态 |

完整约定见 [`System/Vault_Schema.md`](System/Vault_Schema.md)。

### 3. 规则、上下文与内容解耦

- `AGENTS.md`：AI 协作规则的单一来源
- `Context/`：个人背景、偏好和当前 1～3 个月重点
- `System/`：Schema、命名、写作、任务与工作流规则
- 内容目录：只保存实际工作和知识资产
- `03_Knowledge/CHANGELOG.md`：记录知识系统的重要演化

## 目录结构

```text
second-brain-vault/
├── 01_Daily/                       # 每日记录
├── 02_Projects/                    # 有目标、期限或完成标准的项目
├── 03_Knowledge/
│   ├── 00_Cards/                   # 正式卡片区；模板库附带 9 张示例
│   ├── 01_Topics/                  # 主题地图、MOC 与综合理解
│   └── CHANGELOG.md                # 知识系统演化记录
├── 04_References/
│   ├── 01_Inbox/                   # 尚未消化的外部资料
│   └── 02_Library/                 # 已消化且值得保留的原文
├── 05_Tasks/                       # 非项目任务与任务收件箱
├── 06_Archive/                     # 已结束或不再活跃的内容
├── Context/                        # About_Me 与 Current_Priorities
├── System/                         # 规则、地图、说明与架构 Canvas
├── Bases/                          # Obsidian 数据库视图
├── Templates/
│   ├── Cards/                      # 23 种卡片模板
│   ├── Daily_Note.md
│   └── Project.md
├── Attachments/                    # 图片、PDF 等附件
├── .agents/skills/                 # Vault 工作流 Skills
├── .claude/skills                  # 指向 .agents/skills 的兼容入口
├── .obsidian/                      # Obsidian 配置
└── AGENTS.md                       # AI 协作规则与自动发现入口
```

更完整的文件级导航见 [`System/Vault_Map.md`](System/Vault_Map.md)。

## 默认工作流

### 日常闭环

```text
外部资料或临时输入
        ↓
04_References/01_Inbox
        ↓  capture-web / digest
判断价值与去向
        ├─ 长期知识 → 03_Knowledge/00_Cards 或 01_Topics
        ├─ 有完成标准 → 02_Projects
        ├─ 独立行动项 → 05_Tasks
        ├─ 值得保留的原文 → 04_References/02_Library
        └─ 无长期价值 → 明确丢弃
```

每天可用 `today` 聚焦，用 `closeday` 收尾；每周用 `weekly-review` 汇总项目、任务与 Daily Notes。结束的内容进入 `06_Archive/`，而不是继续占据活跃工作区。

### 知识沉淀

单一、可复用的概念或观点进入原子卡片；跨多张卡片的长期综合理解进入 Topic/MOC；有目标和完成标准的学习进入 Project。`knowledge-system` Skill 提供从零散材料到模型、关系、体系和可追溯卡片的六步流程。

建卡门槛、质量信号、来源规范和卡片类型映射分别见：

- [`System/Vault_Schema.md`](System/Vault_Schema.md)
- [`System/Knowledge_Workflow.md`](System/Knowledge_Workflow.md)
- [`System/Card_Type_Map.md`](System/Card_Type_Map.md)

## 5 分钟开始使用

1. **复制或克隆仓库**

   ```bash
   git clone https://github.com/zhttttttty/second-brain-vault.git
   ```

2. **在 Obsidian 中打开仓库根目录**，确认 Daily Notes 的目录为 `01_Daily`、模板目录为 `Templates`。
3. **填写个人上下文**：编辑 `Context/About_Me.md` 和 `Context/Current_Priorities.md`。
4. **初始化模板**：让兼容的 Agent 执行 `onboard`，按需清理 `_EXAMPLE_*` 示例并完成首次检查。
5. **开始工作**：创建当天 Daily Note，或从 `today`、`capture-web`、`digest`、`card-creator` 中选择一个真实流程。

完整说明见 [`QUICK_START.md`](QUICK_START.md)。首次接入 AI 工具时，请先确认它能读取 `AGENTS.md`，并支持所需的 Skills 协议。

## 模板、视图与 Canvas

| 组件 | 位置 | 用途 |
| --- | --- | --- |
| Daily 模板 | `Templates/Daily_Note.md` | 今日重点、执行记录与收尾 |
| Project 模板 | `Templates/Project.md` | 目标、完成标准、下一步、里程碑与决策 |
| Card 模板 | `Templates/Cards/` | 23 种知识对象的统一属性和正文结构 |
| Bases | `Bases/` | 卡片、书籍、人物、资源与复习队列视图 |
| 架构 Canvas | `System/Vault_Architecture.canvas` | 浏览库的分层与信息流 |
| 知识体系 Canvas | `03_Knowledge/01_Topics/Knowledge_System_Workflow.canvas` | 浏览知识提炼六步法 |

`.base` 和 `.canvas` 在其他 Markdown 编辑器中可能无法直接渲染，但底层笔记仍是普通 Markdown 文件。

## AI Skills

Vault 内置的 18 个 Skills 按工作阶段分组如下：

| 阶段 | Skills | 主要用途 |
| --- | --- | --- |
| 初始化与定向 | `onboard`、`session-brief` | 初始化模板、恢复当前工作上下文 |
| 计划与回顾 | `today`、`closeday`、`weekly-review` | 今日计划、每日收尾、每周复盘 |
| 输入与阅读 | `capture-web`、`digest`、`reading-coach` | 网页剪藏、Inbox 消化、主动阅读 |
| 知识创建 | `card-creator`、`knowledge-system` | 创建原子卡片、搭建可追溯知识体系 |
| 思考与连接 | `brain-storming`、`random-thinking`、`connect`、`trace`、`critical-check` | 发散、随机探索、连接、追踪与批判性校验 |
| 复习与维护 | `spaced-review`、`check-health`、`system-sync` | 间隔复习、健康检查、文档和结构同步 |

每个 Skill 的触发条件、输入、输出和写回边界见 [`Skills_Manual.md`](Skills_Manual.md)。Skills 是工作流契约，不代表所有 Agent 平台都会自动发现或执行；平台兼容方式见 [`System/Agent_Skills_Compatibility.md`](System/Agent_Skills_Compatibility.md)。

## 依赖与兼容性

### 必需

- [Obsidian](https://obsidian.md/)：打开和使用 Vault
- Git：建议用于版本记录、回滚与多设备同步

### 可选

- 支持读取项目规则和执行本地 Skills 的 AI Agent
- [Defuddle](https://github.com/kepano/defuddle)：仅 `capture-web` 网页正文提取流程需要
- Obsidian 第三方插件：可以按个人需求安装，但不是本库核心工作流的前提

本库以 `.agents/skills/` 作为跨 Agent 的技能源，并通过兼容入口适配特定工具。外部通用 Obsidian Skills 不复制进 Vault，以避免与仓库自身工作流混在一起；推荐参考 [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)。

> `AGENTS.md` 是普通文件，不依赖符号链接。Windows 若未启用开发者模式或没有创建符号链接的权限，Git 可能无法正确还原 `.claude/skills`；遇到问题时请参考兼容文档或使用实体目录副本。

## 系统规则与质量控制

| 文件 | 作用 |
| --- | --- |
| `AGENTS.md` | AI 角色、导航、读取顺序与写回边界 |
| `System/Vault_Schema.md` | 文件夹、标签、属性、链接、质量信号与建卡门槛 |
| `System/Vault_Map.md` | 当前目录和关键文件地图 |
| `System/Writing_Rules.md` | 默认写作要求 |
| `System/Naming_Conventions.md` | 文件和目录命名规范 |
| `System/Task_Management_Rules.md` | 项目任务、独立任务和 Daily 的边界 |
| `03_Knowledge/CHANGELOG.md` | 知识结构和方法论的重要变更 |

未经整理的聊天原文不应直接进入正式知识区。外部事实、时效信息和高风险判断仍需核对可靠来源；AI 行为契约不能替代事实验证、文件权限、备份和版本控制。

## 校验与维护

结构发生变化后，先执行 `system-sync`，再运行确定性校验：

```bash
python .agents/skills/system-sync/scripts/validate_vault.py --vault . --strict
```

校验范围包括目录结构、模板与技能数量、README 统计、Frontmatter、路径引用、Obsidian 配置、Bases、Canvas、符号链接和生成物清洁度。仓库的 GitHub Actions 会执行同一套严格校验。

如需将旧版编号目录迁移到当前结构，可先预览再执行：

```powershell
powershell -ExecutionPolicy Bypass -File .agents/scripts/migrate-vault-layout.ps1 -Vault "D:\YourVault"
powershell -ExecutionPolicy Bypass -File .agents/scripts/migrate-vault-layout.ps1 -Vault "D:\YourVault" -Apply
```

脚本会改写已知路径引用；执行前仍应备份，并在执行后运行严格校验。

## 隐私与发布边界

- `Context/` 可能包含身份、目标、受众和工作偏好，不应直接发布个人副本
- `Attachments/` 和外部剪藏可能包含版权或隐私材料，提交前需要检查
- API Key、Token、账号信息和私密日志不得写入仓库
- 批量修改前先确认范围，并保留 Git 提交或独立备份

## 如何裁剪与扩展

建议先使用最小组合：Daily、Project，以及 `insight`、`model`、`book`、`tool` 四类卡片。确认真实需求后，再启用其他卡片类型、Bases 或 Skills。

扩展时遵循三个原则：

1. 新增内容前先搜索，避免创建同主题的平行结构
2. 新增标签、模板、Skill 或目录后，同步 Schema、Map、手册和统计
3. 优先删除无用机制，而不是为“以后可能需要”继续堆叠复杂度

## 贡献

欢迎提交 Issue 和 Pull Request。修改目录、模板、Skills 或系统文档时，请先阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)，并确保严格校验通过。

## License

本项目采用 [MIT License](LICENSE)。
