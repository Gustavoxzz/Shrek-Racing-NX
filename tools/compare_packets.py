#!/usr/bin/env python3
"""Compare two local packet captures without printing their contents."""
import argparse
import hashlib
import json
from pathlib import Path

MAX_PACKET = 1024 * 1024


def compare(first: bytes, second: bytes, offset_a: int, offset_b: int) -> dict:
    if min(offset_a, offset_b) < 0:
        raise ValueError("Offsets must be non-negative")
    if max(len(first), len(second)) > MAX_PACKET:
        raise ValueError("Packet exceeds 1 MiB limit")
    mismatch = next((i for i, (a, b) in enumerate(zip(first, second)) if a != b), None)
    if mismatch is None and len(first) != len(second):
        mismatch = min(len(first), len(second))
    return {
        "a": {"size": len(first), "sha256": hashlib.sha256(first).hexdigest(), "offset": offset_a, "offset_mod_16": offset_a % 16},
        "b": {"size": len(second), "sha256": hashlib.sha256(second).hexdigest(), "offset": offset_b, "offset_mod_16": offset_b % 16},
        "equal": first == second,
        "first_difference": mismatch,
    }


def read_bounded(path: Path) -> bytes:
    with path.open("rb") as source:
        data = source.read(MAX_PACKET + 1)
    if len(data) > MAX_PACKET:
        raise ValueError("Packet exceeds 1 MiB limit")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("a", type=Path)
    parser.add_argument("b", type=Path)
    parser.add_argument("--offset-a", type=lambda s: int(s, 0), required=True)
    parser.add_argument("--offset-b", type=lambda s: int(s, 0), required=True)
    args = parser.parse_args()
    print(json.dumps(compare(read_bounded(args.a), read_bounded(args.b), args.offset_a, args.offset_b), indent=2))


if __name__ == "__main__":
    main()
