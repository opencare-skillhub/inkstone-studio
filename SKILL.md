---
name: inkstone-studio
description: >
  本地优先的模块化 AI 内容创作工作流。包含文风沉淀、上下文组装、去 AI 味润色等工序。
  当用户提到"写稿"、"润色"、"文风"、"inkstone"或"砚台"时触发。
triggers:
  - 写稿
  - 润色
  - 文风
  - inkstone
  - 砚台
---

# Inkstone Studio (砚台)

一个基于纯 Markdown 文件系统的多 Agent 协作流水线。核心目标：去 AI 味、沉淀个人文风。

## 核心规则
1. **文风第一**：任何生成任务前，必须先读取工作区的 `style/voice.md`。
2. **上下文组装**：使用 `python3 <skill_dir>/scripts/assemble.py <workspace_path> --step <step>` 获取上下文，不要自己乱读文件导致 Token 爆炸。组装器输出的是 XML 标签块（`<voice>`、`<templates>`、`<topic>`、`<archive>`、`<target_draft>` 等），提示词里引用的标签即来自于此。
3. **数据主权**：所有产出必须落盘到工作区的 `drafts/` 或 `published/` 目录，严禁只在对话中输出。

## 组装器步骤速查
| step | 必填参数 | 注入的标签 |
|------|----------|------------|
| `ideate` | 无 | `<profile> <voice> <audience> <topic_pool>` |
| `draft` | `--topic` | `<profile> <voice> <templates> <topic> <archive>` |
| `polish` | `--target` | `<profile> <voice> <target_draft>` |
| `rewrite` | `--target` | `<profile> <voice> <target_draft>` |
| `publish` | `--target` | `<profile> <voice> <target_draft>` |

> `--topic` 支持前缀容错：传 `PTSD` 也能匹配到 `2026-06-20-认识丧亲后PTSD.md`。

## 目录结构
- `profile.md` / `audience.md`：账号定位与读者画像
- `style/voice.md`：文风指纹（核心资产）
- `memory/`：历史文章与选题库
- `drafts/`：草稿区

## 工作流 (Workflows)

### 1. 选题 (Ideation)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step ideate`（注入 `<profile> <audience> <topic_pool>`）。
2. 结合外部工具 (Exa/Firecrawl) 调研热点，参见 `<skill_dir>/references/mcp-guide.md`；未配置 MCP 时按指南优雅降级，不要编造结果。
3. 产出 3 个差异化角度，挑选一个存入 `memory/topics/YYYY-MM-DD-<topic>.md`。

### 2. 起草 (Drafting)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step draft --topic <topic>`。
2. 读取 `<skill_dir>/references/prompts/draft.md` 作为系统提示词模板。
3. 将组装的上下文（XML 标签块）替换进模板的 `{context_from_assembler}`，生成初稿。
4. 保存到 `drafts/YYYY-MM-DD-<slug>.md`。

### 3. 润色 (Polishing)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step polish --target <draft_file>`。
2. 读取 `<skill_dir>/references/prompts/polish.md`。
3. 执行去 AI 味审查，强化个性。
4. 保存到 `drafts/<original_name>-polished.md`。

### 4. 改写 (Rewrite)
将定稿改编为其它平台格式（如小红书图文）。
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step rewrite --target <draft_file>`。
2. 读取 `<skill_dir>/references/prompts/rewrite.md`。
3. 按目标平台拆解文案。
4. 保存到 `drafts/<original_name>-<platform>.md`。

### 5. 发布 (Publishing)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step publish --target <final_draft>`。
2. 读取 `<skill_dir>/references/prompts/publish.md`。
3. 若已配置微信/平台 MCP（见 `references/mcp-guide.md`）则直接调用；否则生成带内联样式的 HTML 作为降级方案。
4. 定稿与产物存入 `published/`。
5. 发布后可将历史数据回填到 `memory/analytics/`，并把成稿归档进 `memory/archive/` 供后续 RAG 检索。
