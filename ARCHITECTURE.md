# Inkstone Studio - Architecture Design

## 1. Core Philosophy
- **Skill-Native**: Not a standalone app, but a Codex/OpenClaw Skill that guides the LLM through a structured content creation pipeline.
- **Local-First State**: All user assets (voice, history, drafts) live in a local Markdown folder structure.
- **Context-Bounded**: The LLM only reads what it needs for the current step, orchestrated by the Skill instructions and helper scripts.
- **Composable**: Leverages existing MCPs (Exa for research, Firecrawl for reading) instead of reinventing the wheel.

## 2. Workspace Structure (The Inkstone)
Users initialize a workspace (e.g., `~/inkstone/my-account`) using the skill's templates:
```text
my-account/
├── inkstone.json        # Config (LLM preferences, active MCPs)
├── profile.md           # Account positioning, core themes
├── audience.md          # Target reader personas
├── style/
│   ├── voice.md         # The "Fingerprint": syntax, tone, banned words
│   └── templates.md     # Reusable structural skeletons
├── memory/
│   ├── topics/          # Topic ideas and research notes
│   ├── archive/         # Published historical articles (RAG source)
│   └── analytics/       # Post-publication data
├── drafts/              # Active WIPs
└── published/           # Final versions
```

## 3. System Components

### A. The Orchestrator (SKILL.md)
- Defines the workflow states (Ideation -> Drafting -> Polishing -> Publishing).
- Instructs the Agent on which workspace files to read for each state.
- Contains the "Anti-AI-Flavor" system prompts.

### B. Context Assembler (`scripts/assemble.py`)
- A Python script invoked by the Agent.
- Reads `inkstone.json` to determine workspace root.
- Reads requested files (e.g., `style/voice.md`, specific `archive/` files) and formats them into a single context block for the LLM prompt.
- Prevents context overflow by truncating or summarizing large histories.

### C. Workspace Initializer (`scripts/init.sh` or `init.py`)
- Scaffolds a new Inkstone workspace from `templates/workspace/`.

## 4. Tech Stack
- **Agent Engine**: Codex / OpenClaw
- **Skill Format**: YAML frontmatter + Markdown instructions
- **Helper Scripts**: Python 3.10+ (using standard library + `pydantic` if needed)
- **External Tools**: Exa MCP, Firecrawl MCP, Jina Reader
