#!/bin/bash -e
# Turnip (Mesa Freedreno Vulkan) build script for Nightlies CI.
#
# Environment variables:
#   NDK_DIR    — path to pre-cached android-ndk-r29 (required)
#   OUTPUT_DIR — where to write the zip + build_info.env (required)

green='\033[0;32m'
red='\033[0;31m'
nocolor='\033[0m'

: "${NDK_DIR:?NDK_DIR must be set}"
: "${OUTPUT_DIR:?OUTPUT_DIR must be set}"

NDK="$NDK_DIR/toolchains/llvm/prebuilt/linux-x86_64/bin"
SDKVER="36"
MESASRC="https://gitlab.freedesktop.org/mesa/mesa"
WORKDIR="$(pwd)/turnip_workdir"

mkdir -p "$WORKDIR" "$OUTPUT_DIR"

echo -e "${green}====== Cloning Mesa main ======${nocolor}"
git clone "$MESASRC" --depth=1 -b main "$WORKDIR/mesa"

cd "$WORKDIR/mesa"

GITHASH=$(git rev-parse --short HEAD)
GITHASH_FULL=$(git rev-parse HEAD)
COMMIT_DATE=$(git log -1 --format="%ci" | cut -d' ' -f1)
COMMIT_TITLE=$(git log -1 --format="%s")
MESA_VERSION=$(cat VERSION 2>/dev/null | sed 's/-devel.*//' | tr -d '[:space:]' || echo "unknown")
BUILD_DATE=$(date +%Y%m%d)

echo -e "${green}Mesa ${MESA_VERSION} @ ${GITHASH} (${COMMIT_DATE})${nocolor}"

# NDK compatibility fixes
sed -i 's/typedef const native_handle_t\* buffer_handle_t;/typedef void* buffer_handle_t;/g' include/android_stub/cutils/native_handle.h || true
sed -i 's/, hnd->handle/, (void *)hnd->handle/g' src/util/u_gralloc/u_gralloc_fallback.c || true
sed -i 's/native_buffer->handle->/((const native_handle_t *)native_buffer->handle)->/g' src/vulkan/runtime/vk_android.c || true

mkdir -p /tmp/turnip-bin
ln -sf "$NDK/clang"   /tmp/turnip-bin/cc
ln -sf "$NDK/clang++" /tmp/turnip-bin/c++
export PATH="/tmp/turnip-bin:$NDK:$PATH"
export CC=clang CXX=clang++ AR=llvm-ar RANLIB=llvm-ranlib STRIP=llvm-strip
export OBJDUMP=llvm-objdump OBJCOPY=llvm-objcopy LDFLAGS="-fuse-ld=lld"
export CFLAGS="-D__ANDROID__ -Wno-error -Wno-deprecated-declarations -Wno-incompatible-pointer-types-discards-qualifiers -Wno-incompatible-pointer-types"
export CXXFLAGS="$CFLAGS"

echo -e "${green}====== Generating Meson cross files ======${nocolor}"

python3 - <<PYEOF
ndk = "$NDK"
sdk = "$SDKVER"
lines_cross = [
    "[binaries]",
    f"ar = '{ndk}/llvm-ar'",
    f"c = ['ccache', '{ndk}/aarch64-linux-android{sdk}-clang']",
    f"cpp = ['ccache', '{ndk}/aarch64-linux-android{sdk}-clang++', '-fno-exceptions', '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '--start-no-unused-arguments', '-static-libstdc++', '--end-no-unused-arguments']",
    f"c_ld = '{ndk}/ld.lld'",
    f"cpp_ld = '{ndk}/ld.lld'",
    f"strip = '{ndk}/llvm-strip'",
    f"pkg-config = ['env', 'PKG_CONFIG_LIBDIR={ndk}/pkg-config', '/usr/bin/pkg-config']",
    "",
    "[host_machine]",
    "system = 'android'",
    "cpu_family = 'aarch64'",
    "cpu = 'armv8'",
    "endian = 'little'",
]
with open("android-aarch64.txt", "w") as f:
    f.write("\n".join(lines_cross) + "\n")

lines_native = [
    "[build_machine]",
    "c = ['ccache', 'clang']",
    "cpp = ['ccache', 'clang++']",
    "ar = 'llvm-ar'",
    "strip = 'llvm-strip'",
    "c_ld = 'ld.lld'",
    "cpp_ld = 'ld.lld'",
    "system = 'linux'",
    "cpu_family = 'x86_64'",
    "cpu = 'x86_64'",
    "endian = 'little'",
]
with open("native.txt", "w") as f:
    f.write("\n".join(lines_native) + "\n")
PYEOF

echo -e "${green}====== Meson setup ======${nocolor}"
meson setup build-android-aarch64 \
    --cross-file "android-aarch64.txt" \
    --native-file "native.txt" \
    --prefix /tmp/turnip-out \
    -Dbuildtype=release \
    -Dstrip=true \
    -Dplatforms=android \
    -Dvideo-codecs= \
    -Dplatform-sdk-version=36 \
    -Dandroid-stub=true \
    -Dgallium-drivers= \
    -Dvulkan-drivers=freedreno \
    -Dvulkan-beta=true \
    -Dfreedreno-kmds=kgsl \
    -Degl=disabled \
    -Dandroid-libbacktrace=disabled

echo -e "${green}====== Compiling ======${nocolor}"
ninja -C build-android-aarch64 install

if ! [ -f /tmp/turnip-out/lib/libvulkan_freedreno.so ]; then
    echo -e "${red}Build failed — libvulkan_freedreno.so not found${nocolor}" && exit 1
fi

echo -e "${green}====== Packaging ======${nocolor}"
cd /tmp/turnip-out/lib

python3 - <<PYEOF
import json, os
meta = {
    "schemaVersion": 1,
    "name": f"Turnip v{os.environ['MESA_VERSION']}-{os.environ['BUILD_DATE']} ({os.environ['GITHASH']})",
    "description": f"A6xx/A7xx/A8xx Turnip driver from Mesa main (git {os.environ['GITHASH']}). KGSL build.",
    "author": "The412Banner",
    "packageVersion": "1",
    "vendor": "Mesa",
    "driverVersion": "Vulkan 1.4",
    "minApi": 28,
    "libraryName": "libvulkan_freedreno.so"
}
with open("meta.json", "w") as f:
    json.dump(meta, f, indent=2)
PYEOF

export MESA_VERSION BUILD_DATE GITHASH GITHASH_FULL COMMIT_DATE COMMIT_TITLE
ZIPNAME="Turnip-v${MESA_VERSION}-${BUILD_DATE}-${GITHASH}.zip"
zip -q "/tmp/${ZIPNAME}" libvulkan_freedreno.so meta.json
cp "/tmp/${ZIPNAME}" "$OUTPUT_DIR/"

echo -e "${green}====== Writing build info ======${nocolor}"
{
    printf 'MESA_VERSION=%q\n' "$MESA_VERSION"
    printf 'BUILD_DATE=%q\n'   "$BUILD_DATE"
    printf 'GITHASH=%q\n'      "$GITHASH"
    printf 'GITHASH_FULL=%q\n' "$GITHASH_FULL"
    printf 'COMMIT_DATE=%q\n'  "$COMMIT_DATE"
    printf 'COMMIT_TITLE=%q\n' "$COMMIT_TITLE"
    printf 'TURNIP_ZIP=%q\n'   "$ZIPNAME"
} > "$OUTPUT_DIR/build_info.env"

echo -e "${green}====== Done: ${ZIPNAME} ======${nocolor}"
