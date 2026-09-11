# FrameDrop v0.2.0 — Desktop preview

Publication status: prepared, not published. The GitHub connector has no release-write operation, and the prior API publication attempt returned 403 Resource not accessible by integration.

## Publisher checklist

Create a prerelease with tag `v0.2.0` targeting tested application commit `7227f4be7cad3f77f3fc4c36496926c5222754f5`. Do not replace the older extension's tag. Download all four FrameDrop artifacts from [successful build run 34566471892](https://github.com/inianexe/Framedrop/actions/runs/34566471892), extract the outer artifact ZIPs and attach these files:

| Platform | Release attachment |
| --- | --- |
| Windows x64 | FrameDrop-Windows-x64-Setup.exe |
| macOS Apple Silicon | FrameDrop-macos-15.dmg |
| macOS Intel | FrameDrop-macos-15-intel.dmg |
| Linux x64 | FrameDrop-ubuntu-22.04.tar.gz |

The Windows EXE and Mac DMGs are under `desktop/release/` inside their artifacts. Attach actual installers, not test-report files. Retain all bundled dependency notices. Verify all four assets appear on the release before updating the README download links from artifact URLs to release asset URLs.

## Release body

FrameDrop Desktop lets you paste a supported public video link, select video quality or MP3, and save it on your computer. By **iniexe**.

### Included
- Standalone desktop interface for Windows x64, macOS Apple Silicon, macOS Intel and Linux x64.
- Bundled downloader/runtime tools: no Python, FFmpeg, Deno installation or extension ID required.
- Public pages supported by yt-dlp, direct media, supported embeds and unprotected HLS/DASH.
- Source quality selection, MP3 conversion, progress and a save-folder picker.

### Installation
- Windows: run FrameDrop-Windows-x64-Setup.exe, then open FrameDrop from the Start menu.
- macOS: choose the DMG matching your chip, then drag FrameDrop to Applications.
- Linux: extract FrameDrop-ubuntu-22.04.tar.gz and run `sh install-linux.sh` as your normal user. Compatible Arch desktops use the same package; clean Arch testing is pending.

[Complete installation and usage guide](https://github.com/inianexe/Framedrop/blob/main/README.md)

### Usage
Paste the public URL → Analyze link → select Video/MP3 and quality → optionally choose a save folder → Download → wait for Saved → Open downloads folder.

### Validation
All four platform jobs passed packaged tests for generated direct MP4, HTML embedded video, HLS, separate-stream DASH and MP3 conversion, plus offscreen GUI startup. [Build evidence](https://github.com/inianexe/Framedrop/actions/runs/34566471892).

### Preview limitations
Unsigned builds; macOS notarization and automatic updates are not implemented. Device protections can block launch. Clean-machine installation and every live website are not verified. Not all links are supported; private, age-restricted and DRM-protected content are outside scope. Download only material you own or have permission to save.

The v0.1.6 extension remains a separate legacy interface.
