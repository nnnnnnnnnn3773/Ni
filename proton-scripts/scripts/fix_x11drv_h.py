#!/usr/bin/env python3
"""
Apply the Android-specific XATOM__NET_WM_HWND addition directly when the
original x11drv.h patch drifts against newer Wine sources.
"""
import os
import re
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_x11drv_h.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "winex11.drv", "x11drv.h")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, errors="replace") as f:
        src = f.read()

    marker = "    XATOM__NET_WM_HWND,\n"
    if marker in src:
        print("fix_x11drv_h: already applied")
        return 0

    patterns = [
        (
            re.compile(
                r"(    XATOM_text_uri_list,\n)(    XATOM_GAMESCOPE_XALIA_OVERLAY,\n)"
            ),
            r'\1#ifdef __ANDROID__' "\n"
            r"    XATOM__NET_WM_HWND," "\n"
            r"#endif" "\n"
            r"\2",
        ),
        (
            re.compile(r"(    XATOM_text_uri_list,\n)"),
            r'\1#ifdef __ANDROID__' "\n"
            r"    XATOM__NET_WM_HWND," "\n"
            r"#endif" "\n",
        ),
        (
            re.compile(r"(    XATOM_COUNT,\n)"),
            r'#ifdef __ANDROID__' "\n"
            r"    XATOM__NET_WM_HWND," "\n"
            r"#endif" "\n"
            r"\1",
        ),
    ]

    updated = None
    for pattern, replacement in patterns:
        updated, count = pattern.subn(replacement, src, count=1)
        if count:
            break

    if updated is None:
        print("fix_x11drv_h: anchor not found")
        return 3

    with open(path, "w") as f:
        f.write(updated)

    print("fix_x11drv_h: applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())