#!/usr/bin/env python3
"""
Silence the non-fatal "_r_debug not found in ld.so" loader log line.

This message is useful on desktop debugging setups, but in the Android /
Winlator environment it is just noisy and expected. We remove only the print,
keeping the surrounding logic intact.
"""
from __future__ import annotations

import os
import sys


TARGET = '    else wld_printf( "_r_debug not found in ld.so\\n" );\n'


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fix_preloader_r_debug_noise.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "loader", "preloader.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()

    if TARGET not in text:
        print("OK: _r_debug log noise line already absent")
        return 0

    text = text.replace(TARGET, "", 1)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print("FIXED: silenced missing ld.so _r_debug log line")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())