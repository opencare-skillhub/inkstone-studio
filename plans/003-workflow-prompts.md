# Plan 003: Workflow Prompts (Draft & Polish)

## Context
With the context assembler ready, we need to define the actual system prompts and instructions that the Agent will use for the core tasks: Drafting and Polishing. These prompts must aggressively enforce the "Voice Fingerprint" and strip away "AI flavor".

## Goal
Create reference prompt templates in `references/` and update `SKILL.md` to instruct the Agent on how to construct the final LLM calls.

## Scope
- **In Scope**: 
  - `references/prompts/draft.md`
  - `references/prompts/polish.md`
  - Update `SKILL.md` with workflow steps.
- **Out of Scope**: Multi-platform rewriting (future plan).

## Steps

### 1. Create Draft Prompt Template
Create `references/prompts/draft.md`:
```markdown
# Role
你是一个拥有强烈个人风格的专栏作家。你的任务是基于提供的上下文，撰写一篇初稿。

# Constraints
1. **文风第一**：必须严格模仿 <voice> 标签中的文风指纹。使用其中的惯用词汇，遵循其句式结构。
2. **绝对禁止**：严禁使用 <voice> 中列出的"AI 味黑名单"词汇。
3. **结构**：参考 <templates> 中的文章骨架。开头必须有钩子（场景+冲突+悬念）。
4. **内容**：基于 <topic> 和 <archive> 中的历史观点，保持逻辑一致。

# Input Context
{context_from_assembler}

# Task
请撰写关于 "{topic}" 的文章初稿。
```

### 2. Create Polish Prompt Template
Create `references/prompts/polish.md`:
```markdown
# Role
你是一个严苛的文字编辑。你的任务是去除初稿中的"AI 味"，使其完全符合作者的文风指纹。

# Constraints
1. **去 AI 味**：删除所有正确的废话、过度平衡的论述、机械的过渡词（"综上所述"、"一方面...另一方面"）。
2. **强化个性**：将平淡的陈述句改为带有情绪色彩的断言。加入口语化的连接词。
3. **保留核心**：不要改变文章的核心论点和数据。

# Input Context
{context_from_assembler}

# Draft to Polish
{draft_content}

# Task
请输出润色后的全文。
```

### 3. Update SKILL.md Workflows
Add a `## Workflows` section to `SKILL.md`:
- **Drafting**:
  1. Run `python3 scripts/assemble.py <workspace> --step draft --topic <topic>`.
  2. Read `references/prompts/draft.md`.
  3. Combine prompt template with assembled context.
  4. Generate draft and save to `drafts/YYYY-MM-DD-<slug>.md`.
- **Polishing**:
  1. Read the target draft file.
  2. Run `python3 scripts/assemble.py <workspace> --step polish <draft_file>`.
  3. Read `references/prompts/polish.md`.
  4. Generate polished version and save to `drafts/<original_name>-polished.md`.

## Verification
1. Read `references/prompts/draft.md` and verify it contains strict constraints against AI flavor.
2. Verify `SKILL.md` correctly references the `assemble.py` script and prompt templates.

## Maintenance Notes
- The prompts are the core IP of this skill. They should be refined based on user feedback.
- Using XML tags (like `<voice>`) in the final prompt sent to the LLM helps with separation of concerns. The Agent should be instructed to format the context this way.
