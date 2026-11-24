#!/usr/bin/env python3
"""news-23 b41 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(HERE)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(SRC):
        fail("entry.png missing next to main.py")
    with open(SRC, "rb") as fh:
        data = fh.read()
    if len(data) > 1024 * 1024:
        fail("entry.png over 1 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("not a PNG (bad signature)")
    if len(data) < 33:
        fail("PNG too short")
    # IHDR chunk: length (4) + type (4) + width (4) + height (4) + bit depth (1) + colour type (1)
    ilen, itype = struct.unpack(">I4s", data[8:16])
    if itype != b"IHDR" or ilen != 13:
        fail("bad IHDR chunk")
    width, height, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        fail("entry.png is not 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or ctype not in (2, 6):
        fail("unexpected PNG bit depth / colour type")
    # IEND trailer: last 12 bytes = length 0 + 'IEND' + crc
    if data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        fail("PNG IEND trailer malformed")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output not byte-identical to source")
    sha = hashlib.sha256(data).hexdigest()
    print("source entry.png: %d bytes, sha256 %s" % (len(data), sha))
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))


if __name__ == "__main__":
    main()
