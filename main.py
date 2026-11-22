"""Entrypoint: render the 21 November 2026 front page to entry.png.

Usage:
    python3 main.py

Writes assets/entry.png next to this file, or $MAKEFUN_OUTPUT_DIR/entry.png
when that variable is set (the competition harness sets it). Deterministic:
same input, same bytes, every run.
"""

import hashlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import render_page  # noqa: E402


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return Path(out_dir) / "entry.png"
    return Path(__file__).resolve().parent / "assets" / "entry.png"


def main():
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    image = render_page()
    image.save(path, format="PNG")
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {path} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
