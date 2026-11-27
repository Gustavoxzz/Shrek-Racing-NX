#!/usr/bin/env python3
"""Conservative tracked-file check. A clean result is not a security audit."""
import re
import subprocess
import sys
from pathlib import Path

DENIED_SUFFIXES = {".iso", ".cso", ".zso", ".chd", ".elf", ".prx", ".nro", ".nacp", ".exe", ".pmf", ".at3", ".wav", ".mp3"}
DENIED_ROOTS = {"original", "extracted", "generated", "build", "dist", "logs", "work"}
PATTERNS = {
    "private key marker": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token pattern": re.compile(rb"\b(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
    "local Windows user path": re.compile(rb"[A-Za-z]:\\Users\\[^\\\r\n]+\\", re.I),
}


def main():
    result = subprocess.run(["git", "ls-files", "-z"], check=True, stdout=subprocess.PIPE)
    problems = []
    for raw in result.stdout.split(b"\0"):
        if not raw:
            continue
        path = Path(raw.decode("utf-8", "surrogateescape"))
        if path.parts[0].lower() in DENIED_ROOTS or path.suffix.lower() in DENIED_SUFFIXES:
            problems.append((str(path), "private path or file extension"))
            continue
        if path.is_symlink() or not path.is_file():
            problems.append((str(path), "symlink or missing file; inspect manually"))
            continue
        data = path.read_bytes()
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                problems.append((str(path), label))
    for path, label in problems:
        print(f"CHECK {path}: {label}")
    print(f"Checked tracked working-tree files: {len(problems)} flagged. History and staged blobs require separate review.")
    return bool(problems)


if __name__ == "__main__":
    sys.exit(main())
