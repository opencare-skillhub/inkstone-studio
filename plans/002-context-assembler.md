# Plan 002: Core SKILL.md & Context Assembler

## Context
The Agent needs to know *how* to use the workspace. The `SKILL.md` provides the behavioral rules, and the Context Assembler script provides the technical ability to inject the right files into the prompt without overflowing the context window.

## Goal
Write the master `SKILL.md` for the Inkstone Studio and build a `scripts/assemble.py` helper that formats workspace files for the LLM.

## Scope
- **In Scope**: 
  - `SKILL.md` with frontmatter and workflow instructions.
  - `scripts/assemble.py` to read and format Markdown files.
- **Out of Scope**: Specific drafting prompts (covered in Plan 003).

## Steps

### 1. Define SKILL.md
Create `SKILL.md` at the root of the skill:
```yaml
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
```
Add sections:
- **Workflows**: Ideation -> Draft -> Polish -> Publish.
- **Workspace Structure**: Brief map of the directory.
- **Context Assembly Rules**: 
  - Always read `style/voice.md` before generating content.
  - Use `python3 scripts/assemble.py <workspace_path> --step draft --topic <topic>` to get context.
- **Anti-AI-Flavor Constraints**: Hard rules against typical LLM phrases.

### 2. Implement Context Assembler (`scripts/assemble.py`)
Create a Python script using `argparse`:
- `python3 scripts/assemble.py <workspace_path> --step <draft|polish|ideate> [--topic <topic_name>]`
- **Logic**:
  - Reads `inkstone.json` to validate workspace.
  - Always loads `style/voice.md` and `profile.md`.
  - If `--step draft`: loads `style/templates.md`. If `--topic` is provided, loads `memory/topics/<topic>.md`.
  - If `--step polish`: expects a target file path as an extra argument, loads that file.
  - Searches `memory/archive/` for files containing the topic keyword (simple string match for v1) and loads the top 2.
- **Output**: Prints a structured Markdown block to STDOUT:
  ```markdown
  ## [Inkstone Context]
  ### Profile
  <content of profile.md>
  ### Voice Fingerprint
  <content of voice.md>
  ### Relevant History
  <content of matched archive files>
  ```

### 3. Error Handling
- If a required file (like `voice.md`) is missing, print a warning to STDERR but continue with empty content.
- If workspace path is invalid, exit with code 1 and error message.

## Verification
1. Create a test workspace using `scripts/init.py`.
2. Run `python3 scripts/assemble.py /tmp/test_inkstone --step draft --topic "AI"`.
3. Verify STDOUT contains the formatted context block with content from `voice.md` and `profile.md`.
4. Verify missing topic file doesn't crash the script.

## Maintenance Notes
- The assembler should be fast. Avoid heavy dependencies.
- Future version could use embeddings for `memory/archive/` search, but v1 uses simple keyword matching to keep it zero-config.
