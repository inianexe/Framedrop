# FrameDrop Desktop installation and usage

Desktop builds are available from [this verified-source workflow run](https://github.com/inianexe/Framedrop/actions/runs/34566471892). Sign into GitHub and scroll to **Artifacts**. Choose a **FrameDrop-** download, not a **test-report-** download. These artifacts expire according to the repository's retention policy; rerun Desktop builds to regenerate them.

| Computer | Artifact | Open after extracting the artifact ZIP |
| --- | --- | --- |
| Windows x64 | FrameDrop-windows-latest | `desktop/release/FrameDrop-Windows-x64-Setup.exe` |
| Mac with Apple Silicon | FrameDrop-macos-15 | `desktop/release/FrameDrop-macos-15.dmg` |
| Mac with Intel CPU | FrameDrop-macos-15-intel | `desktop/release/FrameDrop-macos-15-intel.dmg` |
| Linux x64, including compatible Arch desktops | FrameDrop-ubuntu-22.04 | Extract the enclosed tar.gz and run `install-linux.sh` |

Windows: run Setup as your normal user and open FrameDrop from the Start menu. It installs into your user profile and includes an uninstaller.

macOS: open the DMG and drag FrameDrop to Applications. These preview builds are not notarized. If macOS blocks the app, do not disable system protections; a signed/notarized distribution is still pending.

Linux/Arch: extract the tar.gz into a folder and run `sh install-linux.sh` from that folder, without sudo. It installs to `${XDG_DATA_HOME:-$HOME/.local/share}/framedrop` and adds an application-menu entry. It bundles the downloader/runtime tools, but requires a compatible graphical Linux desktop. The build is not yet certified on a clean Arch installation. For a portable run, open `FrameDrop/FrameDrop` directly. To uninstall the user installation, remove the `framedrop` folder and `applications/framedrop.desktop` beneath your user data directory. Your downloads are separate and remain intact.

## Use

1. Copy a public video URL from any browser.
2. Open FrameDrop, paste the link, and choose **Analyze link**.
3. Choose **Video** and an available quality, or **MP3 audio** and a bitrate.
4. Optionally choose a save folder; the default is `~/Downloads/FrameDrop`.
5. Click **Download**, wait for completion, then choose **Open downloads folder**.

No extension ID or separate Python, FFmpeg, or Deno installation is needed for these packaged builds. The existing browser extension is a separate, older YouTube-only interface.

Direct media, supported embedded players, and unprotected HLS/DASH streams are handled through yt-dlp. Unsupported sites, login-required/private/age-restricted/DRM content, browser-local blob URLs, multi-video pages, and live streams may be rejected. This is not a promise to download every link. Only download media you have permission to save.

## Preview status

The source and packaged executable checks exercise generated direct MP4, HTML embedded video, HLS, DASH with separate audio/video, and MP3 conversion. Offscreen GUI startup is checked separately. These automated checks do not establish successful downloads from every live website or compatibility with every OS version.

The downloads are unsigned previews. Automatic app updates are not implemented. GitHub rejected automated release creation with `403 Resource not accessible by integration`, so the installers are currently workflow artifacts rather than a new GitHub Release. The latest extension release therefore remains v0.1.6.

## Developer instructions

Build on each target OS with Python 3.12. Run `python -m pip install -r desktop/requirements.txt`, then `python desktop/build.py`, then `python -m unittest discover -s desktop -p 'test_*.py'`. Build before testing on Linux so tests use the corrected bundled FFmpeg. The workflow installs the required Linux graphics libraries before packaging.
