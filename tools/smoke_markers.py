#!/usr/bin/env python3
"""Summarize observed boot evidence in an existing private runtime log.

Markers describe log observations, not game correctness or visual validation.
"""
import argparse
import json
from pathlib import Path

MARKERS = {
    "ENTRY_REACHED": ("BOOT_EVENT phase=guest_start",),
    "FIRST_HLE_CALL": ("HLE: calling ",),
    "FIRST_THREAD_CREATE_CALLED": ("HLE: calling sceKernelCreateThread",),
    "PACKFILE_OPEN_ATTEMPTED": ("HLE_IoOpen: opening 'disc0:/PSP_GAME/USRDIR/PACKFILE.DAT'",),
    "INTRO_VIDEO_OPEN_ATTEMPTED": ("HLE_IoOpen: opening 'disc0:/PSP_GAME/USRDIR/MOVIES/activisn.pmf'",),
    "FIRST_AVC_DECODE_REPORTED": ("MpegAvcDecode #1 ",),
    "FIRST_GE_ENQUEUED": ("HLE: calling sceGeListEnQueue",),
    "FIRST_FRAME_DUMPED": ("[FIRST_FRAME] dumped BGRA",),
}


def classify(lines):
    found = {}
    for number, line in enumerate(lines, 1):
        for marker, terms in MARKERS.items():
            if marker not in found and all(term in line for term in terms):
                found[marker] = number
    return {name: {"observed": name in found, "line": found.get(name)} for name in MARKERS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    args = parser.parse_args()
    with args.log.open(encoding="utf-8", errors="replace") as f:
        print(json.dumps(classify(f), indent=2))


if __name__ == "__main__":
    main()
