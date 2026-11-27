#!/usr/bin/env python3
"""Clone pinned public references without altering pre-existing checkouts."""
import argparse
import json
import re
import subprocess
from pathlib import Path


def git(*args, cwd=None):
    return subprocess.run(["git", *map(str, args)], cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE).stdout.strip()


def setup(manifest, destination):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema")
    destination.mkdir(parents=True, exist_ok=True)
    for entry in data["repositories"]:
        name, url, commit = entry["name"], entry["url"], entry["commit"]
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", name):
            raise ValueError("Unsafe repository name")
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("Expected full SHA-1")
        target = destination / name
        if target.exists():
            if git("rev-parse", "HEAD", cwd=target) != commit:
                raise RuntimeError(f"{target}: different revision; left unchanged")
            if git("status", "--porcelain", cwd=target):
                raise RuntimeError(f"{target}: local changes; left unchanged")
            print(f"OK existing {name}: {commit}", flush=True)
            continue
        git("clone", "--no-checkout", "--", url, target)
        git("checkout", "--detach", commit, cwd=target)
        if git("rev-parse", "HEAD", cwd=target) != commit:
            raise RuntimeError(f"{name}: revision verification failed")
        print(f"OK cloned {name}: {commit}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("dependencies.json"))
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        setup(args.manifest, args.destination)
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
