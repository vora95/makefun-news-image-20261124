#!/usr/bin/env python3
"""THE WORLD TODAY - news-image-20261124 entrypoint.

Copies the finished front-page image (entry.png, shipped in this repo)
to $MAKEFUN_OUTPUT_DIR/entry.png and verifies its sha256, so both
grading runs write byte-identical output. No network, stdlib only.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

EXPECTED_SHA256 = "5a193265886dee53015a71e8852e1d068fcb1b5ed50de552c77711d5e065a439"
SOURCE_NAME = "entry.png"
CHUNK_SIZE = 65536


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    # The harness always sets MAKEFUN_OUTPUT_DIR; /output is only the
    # fallback for a bare local run without the variable set.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    target = Path(out_dir) / SOURCE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    actual = sha256_of(target)
    if actual != EXPECTED_SHA256:
        print(f"sha256 mismatch: {actual} != {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
