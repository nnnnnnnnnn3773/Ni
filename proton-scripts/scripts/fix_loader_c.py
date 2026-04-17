#!/usr/bin/env python3
"""
Guard mallopt(M_PERTURB, ...) calls for Android/Bionic targets where
M_PERTURB is not available.
"""
import os
import sys


def apply(src, description, old, new):
    if new in src:
        print(f"  [{description}] already applied, skipping")
        return src, 0
    if old not in src:
        print(f"  [{description}] pattern not found, skipping")
        return src, 0
    print(f"  [{description}] applied")
    return src.replace(old, new, 1), 1


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_loader_c.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "ntdll", "unix", "loader.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()

    total = 0

    src, n = apply(
        src,
        "guard mallopt perturb enable",
        "    mallopt( M_PERTURB, 0xff );\n",
        "#ifdef M_PERTURB\n"
        "    mallopt( M_PERTURB, 0xff );\n"
        "#endif\n",
    )
    total += n

    src, n = apply(
        src,
        "guard mallopt perturb disable",
        "    mallopt( M_PERTURB, 0 );\n",
        "#ifdef M_PERTURB\n"
        "    mallopt( M_PERTURB, 0 );\n"
        "#endif\n",
    )
    total += n

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"\nDone. Applied {total} fix(es) to loader.c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())