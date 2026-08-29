# DailyUp Second Brain Starter · 知识体系增强版

> An opinionated **Obsidian second-brain template**, built from day one for long-term human–AI collaboration.
>
> 一个为**人机长期协作**而生的 Obsidian 第二大脑模板 — 开箱即用，内置规则、模板和 AI 技能。
>
> 本版本在原始模板基础上，额外整合了 **「1 小时构建知识体系」六步法**（`.agents/skills/knowledge-system/`），让「知识怎么提炼、怎么连接」也有了一套可执行的方法论。

---

## 这是什么

一套可以直接用的 Obsidian Vault 框架，包含：

- **8 个主目录的信息架构** — 系统规则 / 上下文 / 日记 / 项目 / 知识 / 参考 / 任务 / Bases
- **23 种标准化卡片模板** — 原子知识、实体资料、资源工具与导航卡片各有明确用途
- **17 个开箱即用的 AI 技能（Skills）** — `/today`、`/digest`、`/weekly-review`、`/reading-coach`、`/card-creator`、`knowledge-system` 等
- **内置知识体系方法论** — 六步法、5 步模型提炼、4 要素存储、6 种关系工具箱、密度分层
- **完整的 AI 协作规则** — `agent.md` 保存单一规则源，`AGENTS.md` 作为兼容入口指向它
- **可控的中文层级标签体系** — 标签只表达主题，类型 / 来源 / 状态交给 Properties，避免标签蔓延
- **Obsidian Bases 数据库视图** — Books、Persons、Resources、Opensource、Subscriptions
- **清晰的写作规范、命名规范和任务管理规则**

核心设计理念：**让知识能长期积累、让 AI 能长期协作**。

### 本版新增（知识体系方法论层）

| 新增 | 位置 | 作用 |
|------|------|------|
| `knowledge-system` 技能 | `.agents/skills/knowledge-system/` | 六步法 AI 技能 + 12 份方法论文档 |
| `model` 卡片模板 | `04_Knowledge/00_Cards/.templates/Model_Card.md` | 存储 4-5 字认知模型（四要素 + 溯源） |
| 3 张示例模型卡 | `04_Knowledge/00_Cards/_EXAMPLE_model_*.md` | 演示提炼、存储、溯源、关联 |
| 知识体系主题地图 | `04_Knowledge/01_Topics/Knowledge_System_Building.md` | 「元主题」：本 Vault 该怎么用 |
| 方法论落点映射 | `00_System/Knowledge_Workflow.md` | 六步法每一步该落到哪个位置 |

### 本版新增（吸收 Karpathy LLM Wiki 模式）

让知识库「编译一次、持续更新」，靠一致性契约而非每次重新发现：

| 新增 | 位置 | 作用 |
|------|------|------|
| `Vault_Schema.md` | `00_System/Vault_Schema.md` | 领域范围 + 标签分类法 + 建卡门槛 + 质量信号 |
| 变更日志 | `04_Knowledge/CHANGELOG.md` | 每次写入知识库追加一条，演化可追踪 |
| 质量信号 frontmatter | 卡片模板 `confidence`/`contested`/`contradictions` | 弱结论不静默固化成事实 |
| 逐段溯源脚注 | `Writing_Rules.md` | 多来源卡片用 `^[来源]` 逐句追溯 |
| 会话定向协议 | `agent.md` | 新会话先读 Schema → 主题地图 → 变更日志 |
| 批量处理 | `knowledge-system` 技能 | 多来源一次性去重、建卡、更新索引 |

---

## 配套视频课程

如果你希望跟着作者**系统化地、从零搭建**这套 AI × Obsidian 第二大脑，作者推出了一份完全基于本开源模板构建的视频课程：

[**《从零构建 AI × Obsidian 第二大脑》**（付费课程）](https://dailyup.xyz/courses/cmqhhefjl0000ps1ynw5gxpto)

模板本身**永远开源免费**，本文档就是你的上手指南（见下方「5 分钟快速上手」）。课程面向想深入理解设计思路、完整工作流与 AI 协作实战的读者，按需选择即可。

---

## 为什么做这个

市面上的 PKM 模板大多有三个问题：

1. **结构混乱** — 随手一分类，越用越乱
2. **没考虑 AI** — 模板为人类读写设计，AI 无从下手
3. **没法长期维护** — 缺少规则，一年后回看全是"遗迹"

本模板的回答：

| 痛点 | 本模板的做法 |
|---|---|
| 信息该放哪里？| `00_System/Vault_Map.md` 给出明确路由规则 |
| AI 怎么理解我？| `agent.md` + `01_Context/` 的稳定背景与当前重点 |
| 怎么避免重复？| `.templates/` 提供统一模板，所有卡片/项目走同一个骨架 |
| 标签越用越乱？| `Vault_Schema.md` 登记中文层级主题；类型、来源和状态不再重复打标签 |
| 知识怎么沉淀？| 标准化卡片模板 + 双向链接构成知识网络；不要求每种类型都使用 |
| 每天怎么推进？| 内置 `/today`、`/closeday`、`/weekly-review` 三个常用 AI 技能 |

---

## 5 分钟快速上手

详见 [`QUICK_START.md`](./QUICK_START.md)。简要流程：

```bash
# 1. 用这个 repo 作为模板，在 GitHub 上创建你自己的 Vault
#    (点击 "Use this template" 按钮)

# 2. 克隆到本地
git clone https://github.com/<your-user>/<your-vault>.git my-brain
cd my-brain

# 3. 用 Obsidian 打开这个文件夹
#    Obsidian → Open folder as vault → 选择 my-brain/

# 4. 填写你的个人上下文（2 个文件）
#    编辑 01_Context/ 下的 About_Me / Current_Priorities

# 5. 安装 AI 编码工具（推荐 Codex / ZCode），跑第一个 Skill
#    /session-brief   → 让 AI 读懂你的 Vault
#    /today           → 生成今日计划
#    /card-creator    → 创建你的第一张知识卡片
```

---

## 目录结构

```
.
├── 00_System/         # 结构、任务、写作与命名规则
├── 01_Context/        # 全局上下文（你是谁、想做什么、写给谁看）
├── 02_Daily/          # 每日记录（含 Daily Note 模板）
├── 03_Projects/       # 轻量项目管理（单页模板 + 按需产出目录）
├── 04_Knowledge/      # 长期知识沉淀
│   ├── 00_Cards/      # 23 种标准化卡片模板 + 9 张示例
│   └── 01_Topics/     # 长期主题地图（含示例主题 + 知识体系构建元主题）
├── 05_References/     # 剪藏消化（Inbox → 卡片/项目/行动 → 精选 Library）
├── 06_Tasks/          # Inbox 捕获 + 非项目任务管理
├── 07_Bases/          # Obsidian 数据库视图
├── Attachments/       # 根目录笔记的附件；其他笔记使用同目录 Attachments/
├── .obsidian/         # Obsidian 配置（已精简）
├── .agents/skills/    # 通用 Agent 技能
├── agent.md           # AI 协作规则的单一来源
└── AGENTS.md          # 通用 Agent 入口（软链到 agent.md）
```

---

## 内置 AI 技能

> 技能说明见 [`Skills_Manual.md`](./Skills_Manual.md)。当前通用 Agent 技能位于 `.agents/skills/` 下。

| 技能 | 用途 | 触发方式 |
|---|---|---|
| `onboard` | 欢迎新用户、导览模板并清理示例 | `/onboard` |
| `session-brief` | 读懂当前 Vault 状态 | 开新会话时 |
| `today` | 根据任务和优先级生成今日计划 | "今日计划怎么安排" |
| `closeday` | 日终复盘 | "帮我结束今天" |
| `weekly-review` | 周度回顾与下周规划 | "做个周报" |
| `digest` | 把一篇 Inbox 剪藏转化为知识或行动 | `/digest` |
| `reading-coach` | 用 ACTOR 框架主动阅读与学习 | "帮我真正学懂这篇内容" |
| `card-creator` | 根据输入自动创建对应类型的卡片 | "帮我建一张卡" |
| `brain-storming` | 围绕一个主题多维度发散 | "头脑风暴 X" |
| `random-thinking` | 跨主题随机抽卡做关联思考 | "给点灵感" |
| `connect` | 连接两个主题，找出桥梁概念 | "连接 X 和 Y" |
| `trace` | 追踪一个主题在 Vault 中的演化 | "追踪 X 的演化" |
| `critical-check` | 对观点/证据/推理做建设性质疑与校验 | "质疑一下这个观点" |
| `check-health` | 检查孤立卡片、失效链接、矛盾观点 | "检查知识库健康" |
| `spaced-review` | 管理知识卡片间隔复习 | "今天该复习什么" |
| `system-sync` | 同步系统说明、README、统计和技能手册 | "同步系统信息" |

---

## Topics 长期主题地图

`04_Knowledge/01_Topics/` 用于维护**长期关注领域的知识地图与阶段性理解**。

- 单个概念、观点、模型 → 放入 `04_Knowledge/00_Cards/`
- 长期领域的综合理解与知识连接 → 放入 `04_Knowledge/01_Topics/`
- 有目标和完成标准的学习 → 放入 `03_Projects/`
- AI 可执行的方法 → 转化为 `.agents/skills/`

主题默认从一个文件开始，不预建复杂子目录。模板保留 `_EXAMPLE_Learning_Science.md` 展示主题地图的写法；初始化个人 Vault 时可通过 `/onboard` 清理。

---

## 你需要什么

**必备**：
- [Obsidian](https://obsidian.md)（免费）
- Git（用于版本控制和同步）

**强烈推荐** — 才能发挥 Skills 的价值（作者常用的组合）：

| 地区 | 编码工具 | 驱动模型 |
|---|---|---|
| 国外 | [Codex](https://developers.openai.com/codex/cli/) | GPT-5.5 |
| 国内 | [ZCode](https://zcode.z.ai) | [GLM-5.2](https://z.ai/blog/glm-5.2) |

> 本模板以 `agent.md` 为规则单一来源，并通过 `AGENTS.md` 和 `.claude/skills` 提供兼容入口。不同 AI 工具识别的文件名和 Skill 协议可能不同，首次使用时应确认入口是否被正确加载。

**兼容性与能力边界**：

- `agent.md` 和 Skills 是行为契约，可以减少错误路由和无依据猜测，但不是权限系统，也不能保证外部事实正确；重要结论仍需核对来源。
- 核心内容以 Markdown 保存，普通正文具有较好的可迁移性；Wikilinks、`.obsidian/` 配置和 `.base` 视图在其他编辑器中无法获得完全等价的体验。
- 17 个 Skills 是可组合的工作流组件，不是自动运行的中央编排器；是否能触发以及如何调用取决于具体 AI 工具。

克隆后可运行确定性校验，检查 Frontmatter 类型、卡片模板映射、技能手册计数和跨平台入口：

```bash
python -m pip install -r requirements-dev.txt
python .agents/skills/system-sync/scripts/validate_vault.py --vault .
```

**Obsidian 插件**（Core 插件够用，可选增强）：
- Templater — 可选；当前 Daily Note 使用 Obsidian 核心 Templates，卡片默认由 AI Skill 创建或手工复制后填写
- Dataview — 数据库式查询
- Tasks — 任务管理

---

## 它适合谁

- 想认真搭建**长期使用**的第二大脑，而不是玩票
- 已经在用 / 准备用 **AI 编码工具**（Codex / ZCode 等）
- 愿意花 10 分钟填写稳定背景和当前重点，换来更准确的 AI 协作
- 喜欢**文件优先、本地可控**的知识管理方式

它**不**适合谁：

- 只想要一个能用一周的"漂亮模板"
- 完全不打算用 AI 协作（那本模板的一半价值都用不上）
- 只用手机做笔记 —— Obsidian 桌面端体验更好

---

## 如何定制

- **结构**：可以改目录名和编号，但请同步更新 `00_System/Vault_Map.md` 和 `agent.md`
- **卡片类型**：直接在 `04_Knowledge/00_Cards/.templates/` 添加新类型
- **AI 技能**：在 `.agents/skills/` 下新建目录，写一个 `SKILL.md` 即可
- **规则**：`00_System/` 下的规则都是你的，改即可。改完告诉 AI"请读一下新规则"
- **验证**：批量修改后运行 `validate_vault.py`；公开仓库中的 GitHub Actions 会执行同一套检查

---

## 贡献

欢迎提 PR！特别欢迎：

- 新的卡片模板（记得附示例）
- 新的 AI Skills（尤其是跨工具都能用的）
- 翻译（目前以中文为主）
- 使用场景分享

详见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

---

## License

本项目采用**双许可**：

- **代码部分**（Skills、脚本、配置） — [MIT License](./LICENSE)
- **内容部分**（文档、模板、示例卡片和主题地图） — [CC BY 4.0](./LICENSE)

简单说：**自由使用、修改、商用，保留出处就行**。

---

## 相关资源

- **概念来源**：[How to Take Smart Notes](https://book.douban.com/subject/35503571/) — Sönke Ahrens
- **Obsidian 官网**：https://obsidian.md
- **Zettelkasten 方法**：https://zettelkasten.de

---

_Built for people who take knowledge seriously._
