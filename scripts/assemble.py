#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"[Warning: {path.name} not found]"

def main():
    parser = argparse.ArgumentParser(description="Assemble context for Inkstone LLM calls.")
    parser.add_argument("workspace_path", help="Path to the Inkstone workspace")
    parser.add_argument("--step", required=True, choices=["draft", "polish", "ideate"], help="Workflow step")
    parser.add_argument("--topic", help="Topic name (for draft step)")
    parser.add_argument("--target", help="Target file path (for polish step)")
    args = parser.parse_args()

    ws = Path(args.workspace_path)
    if not ws.exists() or not (ws / "inkstone.json").exists():
        print(f"Error: Invalid Inkstone workspace at {ws}", file=sys.stderr)
        sys.exit(1)

    context = ["## [Inkstone Context]"]
    
    # Always load profile and voice
    context.append("### Profile\n" + read_file(ws / "profile.md"))
    context.append("### Voice Fingerprint\n" + read_file(ws / "style/voice.md"))

    if args.step == "draft":
        context.append("### Templates\n" + read_file(ws / "style/templates.md"))
        if args.topic:
            topic_file = ws / "memory" / "topics" / f"{args.topic}.md"
            context.append(f"### Topic: {args.topic}\n" + read_file(topic_file))
            
            # Simple keyword search in archive
            archive_dir = ws / "memory" / "archive"
            if archive_dir.exists():
                matches = []
                for f in archive_dir.glob("*.md"):
                    content = f.read_text(encoding="utf-8")
                    if args.topic.lower() in content.lower():
                        matches.append(f"#### From {f.name}\n{content[:500]}...")
                if matches:
                    context.append("### Relevant History\n" + "\n".join(matches[:2]))

    elif args.step == "polish":
        if args.target:
            target_path = Path(args.target)
            if not target_path.is_absolute():
                target_path = ws / target_path
            context.append("### Target Draft\n" + read_file(target_path))
        else:
            print("Error: --target is required for polish step", file=sys.stderr)
            sys.exit(1)

    print("\n\n".join(context))

if __name__ == "__main__":
    sys.exit(main() or 0)
