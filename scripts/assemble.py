#!/usr/bin/env python3
"""Assemble context for Inkstone LLM calls.

Outputs an XML-tagged context block so prompt templates can reference
discrete sections (<voice>, <templates>, <topic>, <archive>, ...).
"""
import argparse
import sys
from pathlib import Path

ARCHIVE_SNIPPET_CHARS = 500   # truncate each archive match
ARCHIVE_MAX_MATCHES = 2       # keep top-N archive matches


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return f"[Warning: {path.name} not found]"


def tag(name: str, content: str) -> str:
    """Wrap content in an XML-style tag for clean prompt separation."""
    return f"<{name}>\n{content}\n</{name}>"


def resolve_topic(ws: Path, topic: str):
    """Resolve a topic to its file, tolerating the YYYY-MM-DD- prefix.

    Tries, in order:
      1. exact: memory/topics/<topic>.md
      2. fuzzy: memory/topics/*<topic>*.md (case-insensitive substring)
    Returns (matched_name, content). Falls back to a warning string.
    """
    topics_dir = ws / "memory" / "topics"
    exact = topics_dir / f"{topic}.md"
    if exact.exists():
        return topic, read_file(exact)

    if topics_dir.exists():
        needle = topic.lower()
        for f in sorted(topics_dir.glob("*.md")):
            if needle in f.stem.lower():
                return f.stem, read_file(f)

    return topic, f"[Warning: no topic file matching '{topic}' in memory/topics/]"


def search_archive(ws: Path, topic: str) -> str:
    """Simple case-insensitive keyword match over memory/archive/*.md."""
    archive_dir = ws / "memory" / "archive"
    if not archive_dir.exists():
        return ""
    matches = []
    needle = topic.lower()
    for f in sorted(archive_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        if needle in content.lower():
            snippet = content[:ARCHIVE_SNIPPET_CHARS].strip()
            matches.append(f"#### From {f.name}\n{snippet}...")
        if len(matches) >= ARCHIVE_MAX_MATCHES:
            break
    return "\n\n".join(matches)


def list_topic_pool(ws: Path) -> str:
    topics_dir = ws / "memory" / "topics"
    if not topics_dir.exists():
        return "[empty]"
    names = [f.name for f in sorted(topics_dir.glob("*.md"))]
    return "\n".join(f"- {n}" for n in names) if names else "[empty]"


def resolve_target(ws: Path, target: str) -> Path:
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = ws / target_path
    return target_path


def main():
    parser = argparse.ArgumentParser(description="Assemble context for Inkstone LLM calls.")
    parser.add_argument("workspace_path", help="Path to the Inkstone workspace")
    parser.add_argument(
        "--step",
        required=True,
        choices=["ideate", "draft", "polish", "rewrite", "publish"],
        help="Workflow step",
    )
    parser.add_argument("--topic", help="Topic name (for draft step; prefix-tolerant)")
    parser.add_argument("--target", help="Target draft path (for polish/rewrite/publish steps)")
    args = parser.parse_args()

    ws = Path(args.workspace_path)
    if not ws.exists() or not (ws / "inkstone.json").exists():
        print(f"Error: Invalid Inkstone workspace at {ws}", file=sys.stderr)
        sys.exit(1)

    sections = []

    # Core identity is loaded for every step.
    sections.append(tag("profile", read_file(ws / "profile.md")))
    sections.append(tag("voice", read_file(ws / "style" / "voice.md")))

    if args.step == "ideate":
        sections.append(tag("audience", read_file(ws / "audience.md")))
        sections.append(tag("topic_pool", list_topic_pool(ws)))

    elif args.step == "draft":
        sections.append(tag("templates", read_file(ws / "style" / "templates.md")))
        if args.topic:
            name, content = resolve_topic(ws, args.topic)
            sections.append(tag("topic", f"# {name}\n{content}"))
            archive = search_archive(ws, args.topic)
            if archive:
                sections.append(tag("archive", archive))

    elif args.step in ("polish", "rewrite", "publish"):
        if not args.target:
            print(f"Error: --target is required for {args.step} step", file=sys.stderr)
            sys.exit(1)
        sections.append(tag("target_draft", read_file(resolve_target(ws, args.target))))

    output = "<inkstone_context>\n\n" + "\n\n".join(sections) + "\n\n</inkstone_context>"
    print(output)


if __name__ == "__main__":
    sys.exit(main() or 0)
