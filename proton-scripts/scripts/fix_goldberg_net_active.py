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
        print("Usage: fix_goldberg_net_active.py <wine-source-dir>")
        return 1

    event_c = os.path.join(os.path.abspath(sys.argv[1]), 'dlls', 'winex11.drv', 'event.c')
    if not os.path.exists(event_c):
        print(f"ERROR: {event_c} not found")
        return 1

    with open(event_c, encoding='utf-8', errors='replace') as f:
        src = f.read()

    old = (
        'static void handle_net_active_window( XPropertyEvent *event )\n'
        '{\n'
        '    struct x11drv_thread_data *data = x11drv_thread_data();\n'
        '    Window window = 0;\n\n'
        '    if (data->active_window)\n'
        '    {\n'
        '        XFree( data->active_window );\n'
        '        data->active_window = NULL;\n'
        '    }\n\n'
        '    if (event->state == PropertyNewValue) window = get_net_active_window( event->display );\n'
        '    net_active_window_notify( event->serial, window, event->time );\n'
        '}\n'
    )
    new = (
        'static void handle_net_active_window( XPropertyEvent *event )\n'
        '{\n'
        '    struct x11drv_thread_data *data = x11drv_thread_data();\n'
        '    Window window = 0;\n\n'
        '    if (data->active_window)\n'
        '    {\n'
        '        XFree( data->active_window );\n'
        '        data->active_window = NULL;\n'
        '    }\n\n'
        '    if (event->state == PropertyNewValue) window = get_net_active_window( event->display );\n'
        '#ifdef __ANDROID__\n'
        '    if (!window)\n'
        '    {\n'
        '        TRACE( "ignoring _NET_ACTIVE_WINDOW None update on Android\n" );\n'
        '        return;\n'
        '    }\n'
        '#endif\n'
        '    net_active_window_notify( event->serial, window, event->time );\n'
        '}\n'
    )

    src, total = replace_once(src, old, new, 'ignore _NET_ACTIVE_WINDOW None on android')

    with open(event_c, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)

    print(f"Done. Applied {total} Goldberg net-active fix(es)")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
