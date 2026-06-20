# Plan 004: MCP Integrations (Research & Publish)

## Context
A true content workflow needs external data (for ideation) and external distribution (for publishing). Inkstone Studio will leverage existing MCPs (Exa, Firecrawl) rather than building custom scrapers.

## Goal
Define how the Agent uses MCPs within the Inkstone workflow for Topic Radar (research) and Multi-platform Publishing.

## Scope
- **In Scope**: 
  - `references/mcp-guide.md` documenting how to use Exa/Firecrawl for research.
  - Workflow instructions in `SKILL.md` for Ideation and Publishing.
- **Out of Scope**: Building custom MCP servers.

## Steps

### 1. Document MCP Usage for Research
Create `references/mcp-guide.md`:
- **Ideation / Topic Radar**:
  - Use `exa.web_search_exa` to find trending topics in the user's niche.
  - Use `firecrawl.scrape` or `curl -s https://r.jina.ai/URL` to read competitor articles.
  - Save research notes to `memory/topics/YYYY-MM-DD-<topic>.md`.
- **Publishing**:
  - Use existing platform MCPs (e.g., `baoyu-post-to-wechat`, `youmind-wechat-article`) if available.
  - If no MCP exists, provide instructions for manual copy-paste or browser automation via `playwright` skill.

### 2. Update SKILL.md with Ideation Workflow
Add to `## Workflows` in `SKILL.md`:
- **Ideation (Topic Radar)**:
  1. Read `profile.md` and `audience.md` to understand the niche.
  2. Use Exa MCP to search for recent high-engagement content in this niche.
  3. Synthesize 3 differentiated angles.
  4. Save selected angle to `memory/topics/`.

### 3. Update SKILL.md with Publishing Workflow
Add to `## Workflows` in `SKILL.md`:
- **Publishing**:
  1. Read `drafts/<final_draft>.md`.
  2. If WeChat MCP is available, invoke it.
  3. Otherwise, format the article with HTML/CSS suitable for WeChat editor (using inline styles).
  4. Save final HTML to `published/`.

### 4. Create Rewrite Prompt (Bonus)
Create `references/prompts/rewrite.md` for multi-platform adaptation:
```markdown
# Task
将这篇公众号长文改编为小红书图文脚本。
# Constraints
- 拆解为 5 张图的文案。
- 标题要情绪化、带 emoji。
- 正文口语化，多用短句。
- 提取 5 个核心标签。
```

## Verification
1. Verify `references/mcp-guide.md` lists correct MCP tool names.
2. Verify `SKILL.md` includes the Ideation and Publishing workflows.

## Maintenance Notes
- MCP availability varies by user environment. The Skill should gracefully degrade (e.g., "If Exa MCP is not available, ask the user for a URL to analyze").
- Publishing is the hardest part to automate due to platform auth. Manual fallback is critical.
