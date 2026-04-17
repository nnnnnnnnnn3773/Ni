#!/usr/bin/env python3
"""
Apply the Android-specific x11drv_main.c changes directly when the original
patch drifts against newer Wine sources.
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
        print("Usage: fix_x11drv_main_c.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "winex11.drv", "x11drv_main.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, errors="replace") as f:
        src = f.read()

    total = 0

    src, n = apply(
        src,
        "android _NET_WM_HWND atom",
        '    "text/uri-list",\n'
        '    "GAMESCOPE_XALIA_OVERLAY",\n',
        '    "text/uri-list",\n'
        '#ifdef __ANDROID__\n'
        '    "_NET_WM_HWND",\n'
        '#endif\n'
        '    "GAMESCOPE_XALIA_OVERLAY",\n',
    )
    total += n

    src, n = apply(
        src,
        "guard x11drv_xinput2_load",
        "#ifdef SONAME_LIBXCOMPOSITE\n"
        "    X11DRV_XComposite_Init();\n"
        "#endif\n"
        "    x11drv_xinput2_load();\n"
        "\n"
        "    XkbUseExtension( gdi_display, NULL, NULL );\n",
        "#ifdef SONAME_LIBXCOMPOSITE\n"
        "    X11DRV_XComposite_Init();\n"
        "#endif\n"
        "#ifdef HAVE_X11_EXTENSIONS_XINPUT2_H\n"
        "    x11drv_xinput2_load();\n"
        "#endif\n"
        "\n"
        "    XkbUseExtension( gdi_display, NULL, NULL );\n",
    )
    total += n

    with open(path, "w") as f:
        f.write(src)

    print(f"\nDone. Applied {total} fix(es) to x11drv_main.c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())