# Inkstone Studio (砚台) 🖋️

> 一个本地优先、文件驱动的 AI 内容创作工作流。专为 Codex / OpenClaw 设计的 Skill 集合。

Inkstone Studio 不是另一个套壳 AI 写作工具。它的核心理念是：**你的创作资产，应该长在你自己的硬盘上。**

通过严格的 Markdown 文件系统、精准的上下文路由和极度克制的提示词工程，Inkstone 帮助创作者沉淀个人文风，彻底消除大模型生成的"AI 味"。

## 📦 核心特性

- **📂 本地优先 (Local-First)**：零数据库。所有的定位、文风指纹、历史档案全部是纯 Markdown 文件，天然支持 Git 版本控制。
- **🧠 记忆沉淀 (Context Bounded)**：独创的 Context Assembler 机制。每次 LLM 调用只读取最小必要上下文，避免 Token 爆炸，同时确保文风高度一致。
- **🛠️ 工序流水线 (Agentic Workflow)**：将创作拆解为 Ideation (选题) -> Draft (起草) -> Polish (润色) -> Rewrite (改写) -> Publish (发布) 五道独立工序，每道工序都有严格的规则约束。
- **🚫 去 AI 味 (Anti-AI-Flavor)**：内置严苛的文风黑名单与重构提示词，专门对付"正确的废话"和"机械的排比"。
- **📝 引导式模板 (Guided Templates)**：初始化即附带带说明和示例的 `profile / audience / voice / templates`，照着改就能用，无需从空白开始。

## 🚀 快速开始

### 1. 初始化你的工作区
使用内置脚本生成标准的文件结构：

```bash
python3 scripts/init.py my_account ~/workspace
```

### 2. 沉淀你的文风
初始化后的工作区里，`profile.md`、`audience.md`、`style/voice.md`、`style/templates.md` 都是**带说明和示例的引导式模板**，按提示替换成你自己的内容即可。重点打磨 `style/voice.md`：填入惯用词汇、句式偏好、**绝对禁止**的 AI 词汇，以及最有效的"正反示例对照"。把你过去的文章扔进 `memory/archive/` 作为 RAG 语料。

### 3. 开始创作
如果你使用的是 Codex 或 OpenClaw，将 `inkstone-studio` 挂载为 Skill。然后直接对 Agent 说：

> "砚台，帮我基于 'xxx' 话题起草一篇文章。"

Agent 会自动调用 Context Assembler 读取你的文风指纹，并遵循 Draft 工序生成初稿。

## 🔁 工序与组装器

每道工序通过 `scripts/assemble.py` 按需注入最小上下文（输出为 XML 标签块，供提示词精准引用）：

| 工序 | 命令 | 注入上下文 |
|------|------|------------|
| 选题 Ideate | `assemble.py <ws> --step ideate` | profile / voice / audience / topic_pool |
| 起草 Draft | `assemble.py <ws> --step draft --topic <topic>` | + templates / topic / archive |
| 润色 Polish | `assemble.py <ws> --step polish --target <draft>` | + target_draft |
| 改写 Rewrite | `assemble.py <ws> --step rewrite --target <draft>` | + target_draft |
| 发布 Publish | `assemble.py <ws> --step publish --target <draft>` | + target_draft |

> `--topic` 支持前缀容错：传 `PTSD` 也能匹配到 `2026-06-20-认识丧亲后PTSD.md`。

## 📁 工作区结构 (The Inkstone)

```text
my_account/
├── inkstone.json        # 基础配置
├── profile.md           # 账号定位与核心价值观
├── audience.md          # 读者画像
├── style/
│   ├── voice.md         # 🌟 文风指纹 (灵魂所在)
│   └── templates.md     # 常用文章骨架
├── memory/
│   ├── topics/          # 选题池
│   ├── archive/         # 历史文章 (RAG 语料)
│   └── analytics/       # 发布数据复盘
├── drafts/              # 草稿区
└── published/           # 定稿区
```

## 📂 项目结构

```text
inkstone-studio/
├── SKILL.md             # 核心 Skill 规则与路由逻辑
├── scripts/             # 辅助脚本 (初始化、上下文组装)
├── references/          # 提示词模板与 MCP 集成指南
├── templates/           # 工作区初始模板
├── plans/               # 架构设计与实施计划
└── demo/                # 真实工作区示例 (含生成文章)
```

## 📖 Demo 示例
在 `demo/xiaoyibao/` 目录下，我们提供了一个真实的账号工作区示例（小胰宝社区）。
你可以在 `demo/xiaoyibao/drafts/` 中查看使用 Inkstone 工作流生成的文章，体验其高度结构化、克制且务实的文风。

## 🤝 参与贡献
本项目基于 MIT 协议开源。欢迎提交 PR 优化提示词模板或补充新的 MCP 集成方案。

---
*Inkstone Studio: 你的创作资产，该长在你自己的硬盘上。*
