#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261127.

Copies the pre-rendered entry.png (1024x1024, drawn at build time by
draw_passport.py) to $MAKEFUN_OUTPUT_DIR/entry.png.

Standard library only: no network, no PIL, no fonts at run time.
The run is deterministic: the same input bytes always produce the
same output bytes.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()

    if not data.startswith(PNG_MAGIC):
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(
            f"error: entry.png is {len(data)} bytes, over the "
            f"{MAX_BYTES} byte limit",
            file=sys.stderr,
        )
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    with open(dst, "rb") as f:
        copied = f.read()
    if copied != data:
        print("error: copied file does not match entry.png", file=sys.stderr)
        return 1

    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
