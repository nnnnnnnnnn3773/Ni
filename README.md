<p align="center">
  <img src="/img.png" width="500" title="The412Banner Nightly Repo">
</p>

<h1 align="center">The412Banner Nightly Repo for Winlator & Emulation</h1>

<p align="center">
  <a href="https://github.com/The412Banner/Nightlies/actions/workflows/new-All-in-one-nightly+zips-latest-stable.yml"><img src="https://github.com/The412Banner/Nightlies/actions/workflows/new-All-in-one-nightly+zips-latest-stable.yml/badge.svg" alt="All-in-One Nightly"></a>
  <a href="https://github.com/The412Banner/Nightlies/actions/workflows/proton-bleeding-edge-nightly.yml"><img src="https://github.com/The412Banner/Nightlies/actions/workflows/proton-bleeding-edge-nightly.yml/badge.svg" alt="Proton Bleeding Edge"></a>
</p>

Welcome to my nightly repository for Windows-emulation components on Android. This repository automatically builds and packages the latest upstream commits from projects like DXVK, VKD3D-Proton, Box64, and FEXCore into ready-to-use `.wcp` (Winlator Component Package) files.

> **Note:** Nightly workflows run automatically and update every hour, and a full daily build is processed at **03:30 AM EST / 08:30 AM UTC**.

A special thanks to [Arihany](https://github.com/Arihany/WinlatorWCPHub), StevenMXZ, Pypetto-Crypto, Max, and Nick417. Much of the structure here was inspired by their fantastic work in the emulation community. 

---

## 🌙 Latest Nightly Releases

> ⚠️ Nightly builds are not always stable. Use at your own risk.

### 📦 All-in-One Emulation Nightly (Box64 · FEX · VKD3D-Proton · DXVK)

<!-- NIGHTLY-LATEST-START -->
| | |
| :--- | :--- |
| **Release** | [🔗 nightly-20260417-082739](https://github.com/The412Banner/Nightlies/releases/tag/nightly-20260417-082739) |
| **FEXCore** | [`441116e1e`](https://github.com/FEX-Emu/FEX/commit/441116e1e) — FEX-2604-Nightly-441116e1e |
| **VKD3D-Proton (Std)** | [`9efd756a`](https://github.com/HansKristian-Work/vkd3d-proton/commit/9efd756a) |
| **VKD3D-Proton (ARM64EC)** | [`9efd756a`](https://github.com/HansKristian-Work/vkd3d-proton/commit/9efd756a) |
| **DXVK (GPLAsync)** | [`a1abc9c4`](https://github.com/doitsujin/dxvk/commit/a1abc9c4) |
| **DXVK (ARM64EC)** | [`a1abc9c4`](https://github.com/doitsujin/dxvk/commit/a1abc9c4) |
| **Box64** | [ptitSeb/box64](https://github.com/ptitSeb/box64/commits/main) + [Pipetto/box64](https://github.com/Pipetto-crypto/box64/commits/main) |
| **Turnip** | [v26.2.0-20260417](https://github.com/The412Banner/Banners-Turnip/releases/tag/v26.2.0-20260417) — Turnip 26.2.0 — 20260417 |
| **Files** | [`.wcp` and `.zip` — scroll to Assets](https://github.com/The412Banner/Nightlies/releases/tag/nightly-20260417-082739) |
<!-- NIGHTLY-LATEST-END -->

### 🍷 Proton Bleeding-Edge ARM64EC

<!-- PROTON-LATEST-START -->
| | |
| :--- | :--- |
| **Release** | [🔗 proton-bleeding-edge-20260414-5edc831-run180](https://github.com/The412Banner/Nightlies/releases/tag/proton-bleeding-edge-20260414-5edc831-run180) |
| **Wine Commit** | [`5edc831`](https://github.com/ValveSoftware/wine/commit/5edc831e88430b5e71efae03d86b908070f05e0f) — atiadlxx: Add ADL2_Graphics_Versions_Get(). |
| **Date** | 2026-04-14 |
| **Files** | [`.wcp` and `.wcp.xz` — scroll to Assets](https://github.com/The412Banner/Nightlies/releases/tag/proton-bleeding-edge-20260414-5edc831-run180) |
<!-- PROTON-LATEST-END -->

---

## 📱 My Other Projects

- [**BannerHub**](https://github.com/The412Banner/bannerhub) — A fully patched GameHub 5.3.5 ReVanced build with a built-in Component Manager, BCI launcher button, online component downloader, performance toggles, and more.
- [**Banners Component Injector**](https://github.com/The412Banner/BannersComponentInjector) — A no-root Android app to browse, download, and seamlessly inject these WCP components directly into GameHub Lite and other Winlator variants.
- [**Banners No-PC Retroid Overclock**](https://github.com/The412Banner/Banners-No-PC-Retroid-Overclock) — Rooting and overclocking tools for Retroid Snapdragon 865 devices.
- [**Ayaneo PocketFit Tools**](https://github.com/The412Banner/Ayaneo-PocketFit-tools) — A helper repository for rooting your Ayaneo Pocket Fit.

---

## 🎮 Recommended Emulators & Builds

*For a comprehensive and up-to-date ranking of emulators, check out [this emulation guide](https://t3st31.github.io/Ranking-Emulators-Download/).*

### Bionic Builds

| Build | Description |
|:---:|---|
| [**Winlator-CMod**](https://github.com/coffincolors/winlator/releases) | Baseline Bionic build with excellent controller support. |
| [**Winlator-Ludashi**](https://github.com/StevenMXZ/Winlator-Ludashi/releases) | Keeps up with the latest upstream code while remaining close to vanilla. Great performance. |
| [**GameNative**](https://github.com/utkarshdalal/GameNative/releases) | Supports both glibc and bionic, featuring a sleek UI and Steam, Epic, GOG, and Amazon Games integration. |
| [**Unofficial GameNative Performance**](https://github.com/maxjivi05/GameNative-Performance/releases) | MaxesTechReview fork supporting glibc/bionic, reworked UI with storefront integrations, and additional performance improvements. |
| [**Winlator-REF4IK**](https://github.com/REF4IK/winlator-ref4ik-/releases) | Enhanced performance monitoring and reworked input controls with numerous QoL improvements. |

### GameHub Builds

| Build | Description |
|:---:|---|
| [**Official GameHub**](https://gamehub.xiaoji.com/) | The original GameHub released by Gamesir. |
| [**Official GameHub Lite**](https://github.com/Producdevity/gamehub-lite/releases) | A community-maintained modified version of GameHub for educational purposes. |
| [**Unofficial GameHub Lite**](https://github.com/ItzDFPlayer/gamehub-lite) | A fork of the Official GameHub Lite updated to run on the GameHub v5.3.5 build with v5.3.3 features. |
| [**GameHub Brasil**](https://github.com/winlatorbrasil/gamehub-brasil/releases) | A Brazilian fork of GameHub, adapted and maintained with a focus on performance, compatibility, and accessibility. |
| [**BannerHub**](https://github.com/The412Banner/bannerhub/releases) | A patched GameHub 5.3.5 ReVanced build featuring a Component Manager, online component downloader, BCI launcher, and performance toggles. |

---

## ⚙️ Additional Packages & Drivers

### 🔥 Adreno GPU Drivers

| Source | Description |
|:---:|---|
| [**StevenMXZ**](https://github.com/StevenMXZ/freedreno_turnip-CI/releases) | Mesa Turnip drivers (ELITE) |
| [**whitebelyash**](https://github.com/whitebelyash/freedreno_turnip-CI/releases) | Mesa Turnip drivers (ELITE) |
| [**K11MCH1**](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | Qualcomm proprietary drivers + Mesa Turnip drivers |
| [**GameNative**](https://gamenative.app/drivers/) | Qualcomm proprietary drivers + Mesa Turnip drivers |
| [**zoerakk**](https://github.com/zoerakk/qualcomm-adreno-driver/releases) | Qualcomm proprietary drivers (ELITE) |
| [**Mr. Purple**](https://github.com/MrPurple666/purple-turnip/releases) | Turnip Drivers - Secret Console |

<details>
  <summary>💡 <b>Quick Info: Driver Types</b></summary>
  <br> 
  <ul>
    <li><b>Qualcomm Proprietary:</b> Extracted from the official Adreno driver of a recent device. Emulation may show reduced performance or rendering glitches.</li>
    <li><b>Mesa Turnip:</b> Open-source Mesa driver with broader Vulkan support and emulator-friendly behavior. Often much more stable across devices.</li>
  </ul>
</details>

### 📦 Windows Runtime Packages

| Type | Link |
|---|---|
| **Visual C++ 2015–2022** | [x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) \| [x86](https://aka.ms/vs/17/release/vc_redist.x86.exe) \| [ARM64](https://aka.ms/vs/17/release/vc_redist.arm64.exe) |
| **Wine-Mono** | [.NET runtime for Wine](https://dl.winehq.org/wine/wine-mono/) *(Install only if the built-in tool fails)* |
| **Wine-Gecko** | [HTML engine for Wine](https://dl.winehq.org/wine/wine-gecko/) *(Install only if the built-in tool fails)* |
| **DirectX (June 2010)** | [Legacy DirectX Runtime](https://download.microsoft.com/download/8/4/a/84a35bf1-dafe-4ae8-82af-ad2ae20b6b14/directx_Jun2010_redist.exe) *(Install only if missing Legacy DLLs)* |
| **PhysX Legacy** | [Nvidia PhysX Legacy](https://www.nvidia.com/content/DriverDownload-March2009/confirmation.php?url=/Windows/9.13.0604/PhysX-9.13.0604-SystemSoftware-Legacy.msi&lang=us&type=Other) *(Install only if an old game requests it)* |

> **Tip:** Install only the minimum necessary runtimes. If you need older VC++ redistributables, try an [AIO package here](https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/).

---

## 💬 Community & Support (Discord)

Join the community to discuss emulation, get support, and share findings:

- [**The412Banner's Discord**](https://discord.gg/n8S4G2WZQ4) *(My personal channel)*
- [**Official GameHub Lite (Emuready)**](https://discord.gg/emuready-1380826875961540648)
- [**MaxesTechReview**](https://discord.gg/9ySMdArY4s)
- [**Emugear International**](https://discord.gg/94PzWBsHHh)
- [**Emucore (Kimchi's Discord)**](https://discord.gg/ZmXUZybNpU)
- [**Ryan Retro**](https://discord.gg/9n6VUzv424)

---

## 🏆 Credits & Licenses

Third-party components used for packaging retain their original upstream licenses. WCP packages redistribute unmodified (or minimally patched) binaries. All copyrights and credits belong to the original authors:

- **FEX:** [FEX-Emu](https://github.com/FEX-Emu)
- **Box64:** [ptitSeb](https://github.com/ptitSeb)
- **DXVK:** [Philip Rebohle (doitsujin)](https://github.com/doitsujin)
- **DXVK-Sarek:** [pythonlover02](https://github.com/pythonlover02)
- **DXVK-GPLAsync Patch:** [Ph42oN](https://gitlab.com/Ph42oN)
- **VKD3D-Proton:** [Hans-Kristian Arntzen](https://github.com/HansKristian-Work)
- **Freedreno Turnip Driver:** [Mesa3D](https://mesa3d.org/)

*Thank you to Max and Nick for their help with GitHub Actions workflows!*

---
<sub>☕ [Support on Ko-fi](https://ko-fi.com/the412banner)</sub>
