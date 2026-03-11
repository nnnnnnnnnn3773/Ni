#!/usr/bin/env python3
import os
import sys


def replace_once(src, old, new, description):
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
        print("Usage: fix_goldberg_hwnd_mapping.py <wine-source-dir>")
        return 1

    window_c = os.path.join(os.path.abspath(sys.argv[1]), 'dlls', 'winex11.drv', 'window.c')
    if not os.path.exists(window_c):
        print(f"ERROR: {window_c} not found")
        return 1

    with open(window_c, encoding='utf-8', errors='replace') as f:
        src = f.read()

    old = (
        '/* returns the HWND for the X11 window, or the desktop window if it isn\'t a Wine window */\n'
        'static HWND hwnd_from_window( Display *display, Window window )\n'
        '{\n'
        '    HWND hwnd, desktop = NtUserGetDesktopWindow();\n'
        '    HWND *list;\n'
        '    UINT i;\n\n'
        '    if (!window || window == root_window) return desktop;\n'
        '    if (!XFindContext( display, window, winContext, (char **)&hwnd )) return hwnd;\n\n'
        '    if (!(list = build_hwnd_list())) return desktop;\n\n'
        '    for (i = 0; list[i] != HWND_BOTTOM; i++)\n'
        '        if (window == X11DRV_get_whole_window( list[i] ))\n'
        '            break;\n'
        '    hwnd = list[i] == HWND_BOTTOM ? desktop : list[i];\n\n'
        '    free( list );\n\n'
        '    return hwnd;\n'
        '}\n'
    )
    new = (
        '/* returns the HWND for the X11 window, or 0 if it isn\'t a Wine window */\n'
        'static HWND hwnd_from_window( Display *display, Window window )\n'
        '{\n'
        '    HWND hwnd;\n'
        '    HWND *list;\n'
        '    UINT i;\n\n'
        '    if (!window || window == root_window) return 0;\n'
        '    if (!XFindContext( display, window, winContext, (char **)&hwnd )) return hwnd;\n\n'
        '    if (!(list = build_hwnd_list())) return 0;\n\n'
        '    for (i = 0; list[i] != HWND_BOTTOM; i++)\n'
        '        if (window == X11DRV_get_whole_window( list[i] ))\n'
        '            break;\n'
        '    hwnd = list[i] == HWND_BOTTOM ? 0 : list[i];\n\n'
        '    free( list );\n\n'
        '    return hwnd;\n'
        '}\n'
    )

    src, total = replace_once(src, old, new, 'return 0 for unknown foreign windows')

    with open(window_c, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)

    print(f"Done. Applied {total} Goldberg hwnd mapping fix(es)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
