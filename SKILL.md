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
2. **上下文组装**：使用 `python3 <skill_dir>/scripts/assemble.py <workspace_path> --step <step>` 获取上下文，不要自己乱读文件导致 Token 爆炸。
3. **数据主权**：所有产出必须落盘到工作区的 `drafts/` 或 `published/` 目录，严禁只在对话中输出。

## 目录结构
- `profile.md` / `audience.md`：账号定位与读者画像
- `style/voice.md`：文风指纹（核心资产）
- `memory/`：历史文章与选题库
- `drafts/`：草稿区

## 工作流 (Workflows)

### 1. 选题 (Ideation)
1. 读取 `profile.md` 和 `audience.md`。
2. 结合外部工具 (Exa/Firecrawl) 调研热点。
3. 产出 3 个差异化角度，存入 `memory/topics/YYYY-MM-DD-<topic>.md`。

### 2. 起草 (Drafting)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step draft --topic <topic>`。
2. 读取 `<skill_dir>/references/prompts/draft.md` 作为系统提示词模板。
3. 将组装的上下文注入模板，生成初稿。
4. 保存到 `drafts/YYYY-MM-DD-<slug>.md`。

### 3. 润色 (Polishing)
1. 运行 `python3 <skill_dir>/scripts/assemble.py <workspace> --step polish --target <draft_file>`。
2. 读取 `<skill_dir>/references/prompts/polish.md`。
3. 执行去 AI 味审查，强化个性。
4. 保存到 `drafts/<original_name>-polished.md`。
