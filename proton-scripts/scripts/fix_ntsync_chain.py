#!/usr/bin/env python3
"""
Apply the drift-prone 0162 ntsync prerequisite edits directly to
dlls/ntdll/unix/sync.c.

The upstream Valve tree drifts often enough that the raw GE patch can fail on a
single hunk even when the surrounding functions still exist. We patch the
source structurally here, then let later ntsync patches apply on top.
"""
from __future__ import annotations

import os
import sys


STUBS_BLOCK = """static NTSTATUS inproc_release_semaphore( HANDLE handle, ULONG count, ULONG *prev_count )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_query_semaphore( HANDLE handle, SEMAPHORE_BASIC_INFORMATION *info )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_set_event( HANDLE handle, LONG *prev_state )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_reset_event( HANDLE handle, LONG *prev_state )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_pulse_event( HANDLE handle, LONG *prev_state )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_query_event( HANDLE handle, EVENT_BASIC_INFORMATION *info )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_release_mutex( HANDLE handle, LONG *prev_count )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_query_mutex( HANDLE handle, MUTANT_BASIC_INFORMATION *info )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_wait( DWORD count, const HANDLE *handles, BOOLEAN wait_any,
                             BOOLEAN alertable, const LARGE_INTEGER *timeout )
{
    return STATUS_NOT_IMPLEMENTED;
}

static NTSTATUS inproc_signal_and_wait( HANDLE signal, HANDLE wait,
                                        BOOLEAN alertable, const LARGE_INTEGER *timeout )
{
    return STATUS_NOT_IMPLEMENTED;
}


"""


def find_matching_brace(text: str, open_brace: int) -> int:
    depth = 0
    for idx in range(open_brace, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return idx
    return -1


def get_function_body(text: str, signature: str) -> tuple[int, int, int, str] | None:
    start = text.find(signature)
    if start < 0:
        return None
    open_brace = text.find("{", start)
    if open_brace < 0:
        return None
    close_brace = find_matching_brace(text, open_brace)
    if close_brace < 0:
        return None
    return start, open_brace, close_brace, text[open_brace + 1 : close_brace]


def replace_function_body(text: str, signature: str, new_body: str) -> str:
    info = get_function_body(text, signature)
    if info is None:
        raise ValueError(f"function not found: {signature}")
    start, open_brace, close_brace, _ = info
    return text[: open_brace + 1] + new_body + text[close_brace:]


def ensure_stubs_block(text: str) -> tuple[str, bool]:
    marker = "static NTSTATUS inproc_signal_and_wait( HANDLE signal, HANDLE wait,"
    if marker in text:
        print("  [insert 0162 inproc stubs] already applied")
        return text, True

    anchor = "\n\n/******************************************************************************\n *              NtCreateSemaphore"
    pos = text.find(anchor)
    if pos < 0:
        print("  [insert 0162 inproc stubs] anchor not found")
        return text, False

    print("  [insert 0162 inproc stubs] applied")
    return text[:pos] + "\n\n" + STUBS_BLOCK + text[pos:], True


def ensure_before_anchor(body: str, desc: str, marker: str, snippet: str, anchor: str) -> tuple[str, bool]:
    if marker in body:
        print(f"  [{desc}] already applied")
        return body, True

    pos = body.find(anchor)
    if pos < 0:
        print(f"  [{desc}] anchor not found")
        return body, False

    print(f"  [{desc}] applied")
    return body[:pos] + snippet + body[pos:], True


def ensure_in_function_before_anchor(
    text: str,
    signature: str,
    desc: str,
    marker: str,
    snippet: str,
    anchor: str,
) -> tuple[str, bool]:
    info = get_function_body(text, signature)
    if info is None:
        print(f"  [{desc}] function not found")
        return text, False

    _, _, _, body = info
    new_body, ok = ensure_before_anchor(body, desc, marker, snippet, anchor)
    if not ok:
        return text, False
    if new_body == body:
        return text, True
    return replace_function_body(text, signature, new_body), True


def ensure_signal_and_wait(text: str) -> tuple[str, bool]:
    signature = "NTSTATUS WINAPI NtSignalAndWaitForSingleObject( HANDLE signal, HANDLE wait,"
    info = get_function_body(text, signature)
    if info is None:
        print("  [hook NtSignalAndWaitForSingleObject] function not found")
        return text, False

    _, _, _, body = info
    ok = True

    if "\n    NTSTATUS ret;\n" in body:
        print("  [hook NtSignalAndWaitForSingleObject ret] already applied")
    else:
        anchor = "\n    union select_op select_op;\n"
        pos = body.find(anchor)
        if pos < 0:
            print("  [hook NtSignalAndWaitForSingleObject ret] anchor not found")
            ok = False
        else:
            print("  [hook NtSignalAndWaitForSingleObject ret] applied")
            body = body[:pos] + "\n    NTSTATUS ret;" + body[pos:]

    invalid_handle = "    if (!signal) return STATUS_INVALID_HANDLE;\n"
    inproc_call = (
        "    if ((ret = inproc_signal_and_wait( signal, wait, alertable, timeout )) != STATUS_NOT_IMPLEMENTED)\n"
        "        return ret;\n"
        "\n"
    )

    if invalid_handle in body:
        print("  [hook NtSignalAndWaitForSingleObject invalid-handle] already applied")
    else:
        anchor = "    if (do_fsync())\n"
        pos = body.find(anchor)
        if pos < 0:
            print("  [hook NtSignalAndWaitForSingleObject invalid-handle] anchor not found")
            ok = False
        else:
            print("  [hook NtSignalAndWaitForSingleObject invalid-handle] applied")
            body = body[:pos] + invalid_handle + "\n" + body[pos:]

    if "inproc_signal_and_wait( signal, wait, alertable, timeout )" in body:
        print("  [hook NtSignalAndWaitForSingleObject inproc call] already applied")
    else:
        anchor = "    if (do_fsync())\n"
        pos = body.find(anchor)
        if pos < 0:
            print("  [hook NtSignalAndWaitForSingleObject inproc call] anchor not found")
            ok = False
        else:
            print("  [hook NtSignalAndWaitForSingleObject inproc call] applied")
            body = body[:pos] + inproc_call + body[pos:]

    return replace_function_body(text, signature, body), ok


def ensure_wait_for_multiple_objects(text: str) -> tuple[str, bool]:
    signature = "NTSTATUS WINAPI NtWaitForMultipleObjects( DWORD count, const HANDLE *handles, BOOLEAN wait_any,"
    info = get_function_body(text, signature)
    if info is None:
        print("  [hook NtWaitForMultipleObjects ret] function not found")
        return text, False

    _, _, _, body = info

    if "\n    NTSTATUS ret;\n" in body:
        print("  [hook NtWaitForMultipleObjects ret] already applied")
        return text, True

    anchor = "\n    if (!count || count > MAXIMUM_WAIT_OBJECTS) return STATUS_INVALID_PARAMETER_1;\n"
    pos = body.find(anchor)
    if pos < 0:
        print("  [hook NtWaitForMultipleObjects ret] anchor not found")
        return text, False

    print("  [hook NtWaitForMultipleObjects ret] applied")
    body = body[:pos] + "\n    NTSTATUS ret;" + body[pos:]
    return replace_function_body(text, signature, body), True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fix_ntsync_chain.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "ntdll", "unix", "sync.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()

    ok = True

    src, rc = ensure_stubs_block(src)
    ok = ok and rc

    function_ops = [
        (
            "NTSTATUS WINAPI NtQuerySemaphore( HANDLE handle, SEMAPHORE_INFORMATION_CLASS class,",
            "hook NtQuerySemaphore",
            "inproc_query_semaphore( handle, out )",
            "    if ((ret = inproc_query_semaphore( handle, out )) != STATUS_NOT_IMPLEMENTED)\n"
            "    {\n"
            "        if (!ret && ret_len) *ret_len = sizeof(SEMAPHORE_BASIC_INFORMATION);\n"
            "        return ret;\n"
            "    }\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtReleaseSemaphore( HANDLE handle, ULONG count, ULONG *previous )",
            "hook NtReleaseSemaphore",
            "inproc_release_semaphore( handle, count, previous )",
            "    if ((ret = inproc_release_semaphore( handle, count, previous )) != STATUS_NOT_IMPLEMENTED)\n"
            "        return ret;\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtSetEvent( HANDLE handle, LONG *prev_state )",
            "hook NtSetEvent",
            "inproc_set_event( handle, prev_state )",
            "    if ((ret = inproc_set_event( handle, prev_state )) != STATUS_NOT_IMPLEMENTED)\n"
            "        return ret;\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtResetEvent( HANDLE handle, LONG *prev_state )",
            "hook NtResetEvent",
            "inproc_reset_event( handle, prev_state )",
            "    if ((ret = inproc_reset_event( handle, prev_state )) != STATUS_NOT_IMPLEMENTED)\n"
            "        return ret;\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtPulseEvent( HANDLE handle, LONG *prev_state )",
            "hook NtPulseEvent",
            "inproc_pulse_event( handle, prev_state )",
            "    if ((ret = inproc_pulse_event( handle, prev_state )) != STATUS_NOT_IMPLEMENTED)\n"
            "        return ret;\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtQueryEvent( HANDLE handle, EVENT_INFORMATION_CLASS class,",
            "hook NtQueryEvent",
            "inproc_query_event( handle, out )",
            "    if ((ret = inproc_query_event( handle, out )) != STATUS_NOT_IMPLEMENTED)\n"
            "    {\n"
            "        if (!ret && ret_len) *ret_len = sizeof(EVENT_BASIC_INFORMATION);\n"
            "        return ret;\n"
            "    }\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtReleaseMutant( HANDLE handle, LONG *prev_count )",
            "hook NtReleaseMutant",
            "inproc_release_mutex( handle, prev_count )",
            "    if ((ret = inproc_release_mutex( handle, prev_count )) != STATUS_NOT_IMPLEMENTED)\n"
            "        return ret;\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtQueryMutant( HANDLE handle, MUTANT_INFORMATION_CLASS class,",
            "hook NtQueryMutant",
            "inproc_query_mutex( handle, out )",
            "    if ((ret = inproc_query_mutex( handle, out )) != STATUS_NOT_IMPLEMENTED)\n"
            "    {\n"
            "        if (!ret && ret_len) *ret_len = sizeof(MUTANT_BASIC_INFORMATION);\n"
            "        return ret;\n"
            "    }\n"
            "\n",
        ),
        (
            "NTSTATUS WINAPI NtWaitForMultipleObjects( DWORD count, const HANDLE *handles, BOOLEAN wait_any,",
            "hook NtWaitForMultipleObjects",
            "inproc_wait( count, handles, wait_any, alertable, timeout )",
            "    if ((ret = inproc_wait( count, handles, wait_any, alertable, timeout )) != STATUS_NOT_IMPLEMENTED)\n"
            "    {\n"
            "        TRACE( \"-> %#x\\n\", ret );\n"
            "        return ret;\n"
            "    }\n"
            "\n",
        ),
    ]

    src, rc = ensure_wait_for_multiple_objects(src)
    ok = ok and rc

    for signature, desc, marker, snippet in function_ops:
        src, rc = ensure_in_function_before_anchor(
            src,
            signature,
            desc,
            marker,
            snippet,
            "    if (do_fsync())\n",
        )
        ok = ok and rc

    src, rc = ensure_signal_and_wait(src)
    ok = ok and rc

    required_markers = [
        "static NTSTATUS inproc_release_semaphore( HANDLE handle, ULONG count, ULONG *prev_count )",
        "NTSTATUS ret;\n    if (!count || count > MAXIMUM_WAIT_OBJECTS) return STATUS_INVALID_PARAMETER_1;",
        "inproc_query_semaphore( handle, out )",
        "inproc_release_semaphore( handle, count, previous )",
        "inproc_set_event( handle, prev_state )",
        "inproc_reset_event( handle, prev_state )",
        "inproc_pulse_event( handle, prev_state )",
        "inproc_query_event( handle, out )",
        "inproc_release_mutex( handle, prev_count )",
        "inproc_query_mutex( handle, out )",
        "inproc_wait( count, handles, wait_any, alertable, timeout )",
        "inproc_signal_and_wait( signal, wait, alertable, timeout )",
    ]

    missing = [marker for marker in required_markers if marker not in src]

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)

    if missing or not ok:
        if missing:
            print("fix_ntsync_chain: missing required 0162 markers:")
            for marker in missing:
                print(f"  - {marker}")
        else:
            print("fix_ntsync_chain: failed to apply full 0162 drift fix")
        return 2

    print("fix_ntsync_chain: 0162 ntsync prerequisite looks complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())