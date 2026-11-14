# dfVX — Kisatchie Audio

**dfVX** is a Windows x64 VST3 vocal-effects processor developed by **Kisatchie Audio**.

![dfVX vocal effects plugin user interface](images/dfvx-plugin.png)

## Download dfVX for Windows

**Version 1.0 — Windows x64 VST3**

[Download dfVX 1.0 for Windows (VST3 ZIP)](https://github.com/Quiescent18/dfVX-downloads/releases/download/v1.0.0/dfVX-1.0.0-Windows-VST3-x64.zip)

**dfVX 1.0** is available through the files linked in the [GitHub release](https://github.com/Quiescent18/dfVX-downloads/releases/tag/v1.0.0).

Download the **Windows VST3 ZIP** (not the automatically generated GitHub “Source code” archives). The ZIP contains the complete `dfVX.vst3` bundle, installation README, release notes, and the **color illustrated user manual (PDF)**. No standalone app is included.

## Installation

1. Download the ZIP and extract it completely.
2. Close your DAW.
3. Copy the entire `dfVX.vst3` directory to `C:\Program Files\Common Files\VST3`. Administrator permission may be required.
4. Restart your DAW and rescan VST3 plugins if necessary. Find **dfVX** by **Kisatchie Audio**.

For updates, close your DAW before replacing the complete VST3 bundle. User presets are stored separately at `Documents\dfVX\Presets`.

## User manual

[Download color illustrated dfVX user manual (PDF)](https://github.com/Quiescent18/dfVX-downloads/releases/download/v1.0.0/dfVX_User_Manual_1.0.pdf)

## Features

- Two-stage compression: FET and optical processing.
- Telephone and megaphone filtering.
- Rotary, phaser, and tremolo modulation.
- Stereo pitch shifting and vocal thickening.
- Warm, grit, and aggressive saturation character.
- Delay and reverb.
- Factory presets and saved user presets.

## What's new in dfVX 1.0

The Windows 1.0 build passed the GitHub Windows VST3 build and audio DSP regression tests. Key updates include:

- Independent **Phaser** and **Tremolo** selection, or both effects combined.
- Tempo Division syncing for solo Tremolo, with the actual rate shown under **TREM EDIT**.
- Stronger Phaser defaults, wider sweep, and the retuned Floating Phaser factory preset.
- Automatic Modulation activation when selecting Phaser or Tremolo.
- Correct **FREE** tempo behavior when manually changing a synced rate.
- **1/2** tempo division in Manual Delay and updated compression label alignment.
- Updated color illustrated PDF user manual, also included inside the Windows ZIP.

Compatibility across individual DAWs has not been independently validated. Windows binaries are **not digitally signed**.

## Release files and verification

- [Color illustrated user manual (PDF)](https://github.com/Quiescent18/dfVX-downloads/releases/download/v1.0.0/dfVX_User_Manual_1.0.pdf)
- [Version 1.0 release](https://github.com/Quiescent18/dfVX-downloads/releases/tag/v1.0.0)
- [Previous v0.1.0 release](https://github.com/Quiescent18/dfVX-downloads/releases/tag/v0.1.0)
- [All releases and future updates](https://github.com/Quiescent18/dfVX-downloads/releases)
- [SHA-256 checksum file](https://github.com/Quiescent18/dfVX-downloads/releases/download/v1.0.0/SHA256SUMS.txt)

To verify the ZIP, use Windows PowerShell:

```powershell
Get-FileHash .\dfVX-1.0.0-Windows-VST3-x64.zip -Algorithm SHA256
```

Compare the result to `SHA256SUMS.txt` on the release page.

The public download repository contains installation information and release binaries only, **not** the dfVX source code, development libraries, `.exp` files, or the internal test application. Retain any supplied third-party notices. All third-party components remain subject to their respective license terms.

Copyright © 2026 Kisatchie Audio. All rights reserved.
