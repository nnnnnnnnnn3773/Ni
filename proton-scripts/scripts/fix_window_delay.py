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
        print("Usage: fix_window_delay.py <wine-source-dir>")
        return 1

    window_c = os.path.join(os.path.abspath(sys.argv[1]), 'dlls', 'winex11.drv', 'window.c')
    if not os.path.exists(window_c):
        print(f"ERROR: {window_c} not found")
        return 1

    with open(window_c, encoding='utf-8', errors='replace') as f:
        src = f.read()

    total = 0
    replacements = [
        (
            'disable mwm hints delay on android',
            'static BOOL window_needs_mwm_hints_change_delay( struct x11drv_win_data *data )\n{\n',
            'static BOOL window_needs_mwm_hints_change_delay( struct x11drv_win_data *data )\n{\n#ifdef __ANDROID__\n    return FALSE;\n#endif\n',
        ),
        (
            'disable net wm state delay on android',
            'static BOOL window_needs_net_wm_state_change_delay( struct x11drv_win_data *data )\n{\n',
            'static BOOL window_needs_net_wm_state_change_delay( struct x11drv_win_data *data )\n{\n#ifdef __ANDROID__\n    return FALSE;\n#endif\n',
        ),
        (
            'disable config change delay on android',
            'static BOOL window_needs_config_change_delay( struct x11drv_win_data *data )\n{\n',
            'static BOOL window_needs_config_change_delay( struct x11drv_win_data *data )\n{\n#ifdef __ANDROID__\n    return FALSE;\n#endif\n',
        ),
    ]

    for description, old, new in replacements:
        src, n = replace_once(src, old, new, description)
        total += n

    with open(window_c, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)

    print(f"Done. Applied {total} window delay fix(es)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
