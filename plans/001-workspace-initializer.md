# Plan 001: Workspace Initializer & Templates

## Context
Inkstone Studio relies on a strict local directory structure to manage context. We need a way for users to quickly scaffold this "Inkstone" workspace and populate it with instructional templates.

## Goal
Create a Python script `scripts/init.py` and a set of default Markdown templates that establish the file-based state machine.

## Scope
- **In Scope**: 
  - `scripts/init.py` (CLI tool to scaffold workspace).
  - `templates/workspace/` directory with default Markdown files.
- **Out of Scope**: Agent logic, LLM integration.

## Steps

### 1. Create Default Templates
In `templates/workspace/`, create the following files with instructional content:

- **`profile.md`**:
  ```markdown
  # 账号定位
  ## 核心赛道
  - 
  ## 人设与价值观
  - 
  ```
- **`audience.md`**:
  ```markdown
  # 读者画像
  ## 他们是谁
  - 
  ## 核心痛点
  - 
  ```
- **`style/voice.md`**:
  ```markdown
  # 文风指纹 (Voice Fingerprint)
  ## 惯用词汇与句式
  - 
  ## 绝对禁止的词汇 (AI 味黑名单)
  - "综上所述"、"总而言之"、"首先...其次..."、"令人深思"
  ## 情绪基调
  - 
  ```
- **`style/templates.md`**:
  ```markdown
  # 文章骨架
  ## 爆款开头公式
  - 场景 + 冲突 + 悬念
  ```
- **`inkstone.json`**:
  ```json
  {
    "version": "1.0",
    "workspace_name": "default",
    "language": "zh-CN"
  }
  ```

### 2. Implement Initializer Script (`scripts/init.py`)
Create a Python script using `argparse`:
- `python3 scripts/init.py <workspace_name> [destination_path]`
- Copies the `templates/workspace/` directory to the destination.
- Creates empty subdirectories: `memory/topics/`, `memory/archive/`, `memory/analytics/`, `drafts/`, `published/`.
- Updates `inkstone.json` with the provided `workspace_name`.
- Prints success message with next steps.

### 3. Make Script Executable
Ensure `scripts/init.py` has a shebang `#!/usr/bin/env python3` and is executable.

## Verification
1. Run `python3 scripts/init.py my_blog /tmp/test_inkstone`.
2. Verify all directories and template files are created in `/tmp/test_inkstone`.
3. Verify `inkstone.json` contains `"workspace_name": "my_blog"`.
4. Verify `style/voice.md` contains the "AI 味黑名单" section.

## Maintenance Notes
- Templates should be written in Chinese as the primary target audience is Chinese creators.
- The initializer should not overwrite existing files if run in an existing directory (add a safety check).
