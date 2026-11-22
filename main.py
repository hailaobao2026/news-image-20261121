#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered front page to the harness output dir.

Standard library only, no network, fully deterministic: the bytes written
are exactly the bytes of assets/entry.png, so every run is identical.
"""
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE, "assets", "entry.png")
TARGET = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def run():
    if not os.path.isfile(IMAGE):
        print(f"missing source image: {IMAGE}", file=sys.stderr)
        return 1
    os.makedirs(TARGET, exist_ok=True)
    dest = os.path.join(TARGET, "entry.png")
    shutil.copyfile(IMAGE, dest)
    print(f"wrote {dest} ({os.path.getsize(dest)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
