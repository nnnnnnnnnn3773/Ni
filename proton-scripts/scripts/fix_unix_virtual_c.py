#!/usr/bin/env python3
"""
Apply the Android-specific dlls/ntdll/unix/virtual.c changes directly for
Proton 11 layouts, avoiding fuzzy patch application that can corrupt the file.
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
        print("Usage: fix_unix_virtual_c.py <wine-source-dir>")
        return 1

    path = os.path.join(sys.argv[1], "dlls", "ntdll", "unix", "virtual.c")
    if not os.path.exists(path):
        print(f"ERROR: missing file {path}")
        return 2

    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()

    total = 0

    src, n = apply(
        src,
        "android _WIN64 address-space limits",
        "#ifdef _WIN64\n"
        "static void *address_space_limit = (void *)0x7fffffff0000;  /* top of the total available address space */\n"
        "static void *user_space_limit    = (void *)0x7fffffff0000;  /* top of the user address space */\n"
        "static void *working_set_limit   = (void *)0x7fffffff0000;  /* top of the current working set */\n"
        "#else\n",
        "#ifdef _WIN64\n"
        "#ifdef __ANDROID__\n"
        "static void *address_space_limit = (void *)0x7fffff0000;  /* top of the total available address space */\n"
        "static void *user_space_limit    = (void *)0x7fffff0000;  /* top of the user address space */\n"
        "static void *working_set_limit   = (void *)0x7fffff0000;  /* top of the current working set */\n"
        "#else\n"
        "static void *address_space_limit = (void *)0x7fffffff0000;  /* top of the total available address space */\n"
        "static void *user_space_limit    = (void *)0x7fffffff0000;  /* top of the user address space */\n"
        "static void *working_set_limit   = (void *)0x7fffffff0000;  /* top of the current working set */\n"
        "#endif\n"
        "#else\n",
    )
    total += n

    src, n = apply(
        src,
        "android kernel_writewatch guard",
        "static void kernel_writewatch_init(void)\n"
        "{\n"
        "    struct uffdio_api uffdio_api;\n"
        "\n"
        "    uffd_fd = syscall( __NR_userfaultfd, O_CLOEXEC | O_NONBLOCK | UFFD_USER_MODE_ONLY );\n"
        "    if (uffd_fd == -1) return;\n"
        "\n"
        "    uffdio_api.api = UFFD_API;\n"
        "    uffdio_api.features = UFFD_FEATURE_WP_ASYNC | UFFD_FEATURE_WP_UNPOPULATED;\n"
        "    if (ioctl( uffd_fd, UFFDIO_API, &uffdio_api ) || uffdio_api.api != UFFD_API)\n"
        "    {\n"
        "        close( uffd_fd );\n"
        "        return;\n"
        "    }\n"
        "    pagemap_fd = open( \"/proc/self/pagemap\", O_CLOEXEC | O_RDONLY );\n"
        "    if (pagemap_fd == -1)\n"
        "    {\n"
        "        ERR( \"Error opening /proc/self/pagemap.\\n\" );\n"
        "        close( uffd_fd );\n"
        "        return;\n"
        "    }\n"
        "    use_kernel_writewatch = 1;\n"
        "    TRACE( \"Using kernel write watches.\\n\" );\n"
        "}\n",
        "static void kernel_writewatch_init(void)\n"
        "{\n"
        "#ifndef __ANDROID__\n"
        "    struct uffdio_api uffdio_api;\n"
        "\n"
        "    uffd_fd = syscall( __NR_userfaultfd, O_CLOEXEC | O_NONBLOCK | UFFD_USER_MODE_ONLY );\n"
        "    if (uffd_fd == -1) return;\n"
        "\n"
        "    uffdio_api.api = UFFD_API;\n"
        "    uffdio_api.features = UFFD_FEATURE_WP_ASYNC | UFFD_FEATURE_WP_UNPOPULATED;\n"
        "    if (ioctl( uffd_fd, UFFDIO_API, &uffdio_api ) || uffdio_api.api != UFFD_API)\n"
        "    {\n"
        "        close( uffd_fd );\n"
        "        return;\n"
        "    }\n"
        "    pagemap_fd = open( \"/proc/self/pagemap\", O_CLOEXEC | O_RDONLY );\n"
        "    if (pagemap_fd == -1)\n"
        "    {\n"
        "        ERR( \"Error opening /proc/self/pagemap.\\n\" );\n"
        "        close( uffd_fd );\n"
        "        return;\n"
        "    }\n"
        "    use_kernel_writewatch = 1;\n"
        "    TRACE( \"Using kernel write watches.\\n\" );\n"
        "#else\n"
        '    TRACE( "Kernel writewatches are not supported on Android\\n" );\n'
        "    use_kernel_writewatch = 0;\n"
        "#endif\n"
        "}\n",
    )
    total += n

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

    print(f"\nDone. Applied {total} fix(es) to virtual.c")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())