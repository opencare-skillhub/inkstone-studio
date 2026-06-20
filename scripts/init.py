#!/usr/bin/env python3
import argparse
import shutil
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Initialize a new Inkstone workspace.")
    parser.add_argument("workspace_name", help="Name of the workspace/account")
    parser.add_argument("destination", nargs="?", default=".", help="Destination path (default: current directory)")
    args = parser.parse_args()

    dest_path = Path(args.destination) / args.workspace_name
    template_path = Path(__file__).parent.parent / "templates" / "workspace"

    if dest_path.exists() and any(dest_path.iterdir()):
        print(f"Error: Directory '{dest_path}' already exists and is not empty.", file=sys.stderr)
        sys.exit(1)

    # Copy templates
    shutil.copytree(template_path, dest_path, dirs_exist_ok=True)

    # Update inkstone.json
    config_path = dest_path / "inkstone.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        config["workspace_name"] = args.workspace_name
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Inkstone workspace '{args.workspace_name}' created successfully at {dest_path}")
    print("Next steps:")
    print(f"  cd {dest_path}")
    print("  Edit profile.md and style/voice.md to define your persona.")

if __name__ == "__main__":
    import sys
    sys.exit(main() or 0)
