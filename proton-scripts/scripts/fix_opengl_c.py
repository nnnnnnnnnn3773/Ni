#!/usr/bin/env python3
"""
Apply the Android-specific opengl.c changes directly when the original
GameNative patch drifts against newer Proton/Wine sources.
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
        print("Usage: fix_opengl_c.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "winex11.drv", "opengl.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, errors="replace") as f:
        src = f.read()

    total = 0

    src, n = apply(
        src,
        "android wine_x11forceglx variable",
        "UINT X11DRV_OpenGLInit( UINT version, const struct opengl_funcs *opengl_funcs, const struct opengl_driver_funcs **driver_funcs )\n{\n    int error_base, event_base;\n",
        "UINT X11DRV_OpenGLInit( UINT version, const struct opengl_funcs *opengl_funcs, const struct opengl_driver_funcs **driver_funcs )\n{\n    int error_base, event_base;\n#ifdef __ANDROID__\n    int wine_x11forceglx = 0;\n#endif\n",
    )
    total += n

    src, n = apply(
        src,
        "android WINE_X11FORCEGLX handling",
        '    if(!X11DRV_WineGL_InitOpenglInfo()) goto failed;\n\n    if (XQueryExtension( gdi_display, "GLX", &glx_opcode, &event_base, &error_base ))\n',
        '    if(!X11DRV_WineGL_InitOpenglInfo()) goto failed;\n\n#ifdef __ANDROID__\n    if (getenv("WINE_X11FORCEGLX"))\n        wine_x11forceglx = atoi(getenv("WINE_X11FORCEGLX"));\n\n    if (XQueryExtension( gdi_display, "GLX", &glx_opcode, &event_base, &error_base ) || wine_x11forceglx)\n#else\n    if (XQueryExtension( gdi_display, "GLX", &glx_opcode, &event_base, &error_base ))\n#endif\n',
    )
    total += n

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"\nDone. Applied {total} fix(es) to opengl.c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())