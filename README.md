<p align="center"><img src="extension/icons/logo.png" alt="FrameDrop logo" width="112"></p>

<h1 align="center">FrameDrop</h1>
<p align="center"><strong>Worth keeping.</strong><br>Public video and MP3 downloads, processed on your computer.<br>Created by <strong>iniexe</strong></p>

**Desktop v0.2.0 preview · Windows / macOS / Linux · Local processing**

Paste a supported public video link, choose video quality or MP3, and save it locally. The cream-and-black desktop app bundles its downloader tools and works independently of your browser.

**Start here:** [Download](#download) · [Installation](#installation) · [Usage](#usage) · [Troubleshooting](#troubleshooting) · [Legacy extension guide](docs/EXTENSION-INSTALL.md)

## Download

**Desktop v0.2.0 preview** bundles Python, yt-dlp, FFmpeg and the JavaScript runtime. No extension, extension ID, or separate downloader dependency installation is required. Copy links from whichever browser you use.

The desktop installers are currently **GitHub Actions artifacts**. Release publication is pending; the existing v0.1.6 release is the older extension. Sign into GitHub before downloading these packages. **Code → Download ZIP** and **Source code** downloads contain source, not an installed app.

| Computer | Download | File to open inside the extracted ZIP |
| --- | --- | --- |
| Windows x64 | [Windows package](https://github.com/inianexe/Framedrop/actions/runs/34566471892/artifacts/10186257722) | `desktop/release/FrameDrop-Windows-x64-Setup.exe` |
| macOS Apple Silicon (M-series) | [Apple Silicon package](https://github.com/inianexe/Framedrop/actions/runs/34566471892/artifacts/10186232711) | `desktop/release/FrameDrop-macos-15.dmg` |
| macOS Intel | [Intel Mac package](https://github.com/inianexe/Framedrop/actions/runs/34566471892/artifacts/10186297376) | `desktop/release/FrameDrop-macos-15-intel.dmg` |
| Linux x64, including compatible Arch desktops | [Linux package](https://github.com/inianexe/Framedrop/actions/runs/34566471892/artifacts/10186229669) | `FrameDrop-ubuntu-22.04.tar.gz` |

On a Mac, **Apple menu → About This Mac** identifies the chip/processor. These are desktop packages; Android, iOS and Linux ARM packages are not included. Builds were tested on GitHub's Windows, Ubuntu 22.04 and macOS 15 runners; this does not establish a minimum supported OS version or compatibility with every computer.

Artifacts expire under GitHub's retention policy. If a download expires, report it through [Issues](https://github.com/inianexe/Framedrop/issues).

## Installation

### Windows

1. Download the Windows package above and choose **Extract All**.
2. Open `desktop/release` inside the extracted folder.
3. Run **FrameDrop-Windows-x64-Setup.exe** as your normal user.
4. Follow Setup and launch **FrameDrop** from the Start menu or desktop shortcut.

The installer installs to your user profile and includes an uninstaller. Keep all files together if using the enclosed portable archive instead. The preview is unsigned; if your device blocks it, report the warning rather than disabling device protection.


### Windows Smart App Control warning

A Windows 11 user reported that installation worked after turning off Smart App Control. This is a user-reported result, not a supported installation requirement: disabling this feature reduces protection for other applications too. FrameDrop does not recommend disabling it or adding antivirus exclusions.

The current preview is unsigned. If Windows reports “An application control policy has blocked this file,” record the blocked filename and check Windows Security → App & browser control → Smart App Control settings without changing it. On a managed device, ask the administrator to review the application. Signed distribution and testing with application control enabled remain release requirements. See [Microsoft's Smart App Control guidance](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/overview).

### macOS

1. Download the package matching your Mac's chip and extract the ZIP.
2. Open the matching **.dmg** in `desktop/release`.
3. Drag **FrameDrop** onto **Applications**.
4. Eject the disk image and open FrameDrop from Applications.

These previews are not notarized. If macOS blocks launch, signed/notarized distribution is still pending; do not disable system protections. Choosing the correct architecture does not remove this limitation.

### Linux, including Arch-based desktops

1. Download the Linux package and extract its ZIP.
2. Extract **FrameDrop-ubuntu-22.04.tar.gz** using your archive manager.
3. Open a terminal in the resulting folder containing both **install-linux.sh** and **FrameDrop/**.
4. Run:

```sh
sh install-linux.sh
```

5. Open **FrameDrop** from your application menu.

Run the installer as your normal user, **without sudo**. It installs to `${XDG_DATA_HOME:-$HOME/.local/share}/framedrop` and creates an application-menu entry. For a portable run, launch `./FrameDrop/FrameDrop` from the extracted folder.

Arch, EndeavourOS, CachyOS and Manjaro users use this same Linux package. It is not a pacman/AUR package. Python, FFmpeg and Deno are bundled; the manual dependency commands in the legacy extension guide do not apply. A compatible graphical desktop and system graphics libraries are still required. **Clean Arch installation has not yet been verified.**

## Usage

### Save a video

1. Copy the public video's page URL or direct media URL from your browser.
2. Open FrameDrop, paste it into the link field, and click **Analyze link**.
3. Wait for analysis to finish and the available qualities to appear.
4. Select **Video**, then choose a quality offered by the source.
5. Click **Choose save folder** if you want a different destination.
6. Click **Download**. Keep the app open while it downloads and merges.
7. Wait for **Saved to …**, then click **Open downloads folder**.

After pasting a different link, analyze it again before choosing its format. Quality depends on the source; FrameDrop does not upscale video. Separate video and audio streams are merged into MKV to preserve their codecs; a combined source may retain its original container. Selecting an MP4 source does not guarantee an MP4 final file.

### Save MP3 audio

1. Paste the link and click **Analyze link**.
2. Select **MP3 audio** and choose **128**, **192**, or **320 kbps**.
3. Choose a destination if needed, then click **Download**.
4. Wait for conversion and **Saved to …** before opening the folder.

A higher bitrate cannot restore detail missing from the source audio.

### Find your downloads

The default is **Downloads/FrameDrop beneath your user home**, on all platforms. It is independent of your browser's download directory. Use **Choose save folder** for a redirected or custom Downloads location; **Open downloads folder** opens the current destination.

One job runs at a time. Progress can restart for the next stream, and merging/conversion may take additional time. This desktop preview does not provide the extension's cancellation control. Keep it open until the job finishes.

## Supported links

| Link type | Expected behavior |
| --- | --- |
| Public video page supported by yt-dlp | Extracts metadata and available formats |
| Direct media file, such as MP4 | Downloads the file; quality choices may be limited |
| Supported HTML video embed | Attempts to find the embedded media |
| Unprotected HLS / DASH manifest | Downloads segments and merges streams as needed |
| Unsupported page or browser-local blob URL | May fail; a page containing video is not automatically supported |

Private/login-required, age-restricted and DRM-protected media are outside supported scope. Playlists, multi-video pages and live streams are not guaranteed. Only save media you own or have permission to download.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Download link asks for sign-in | Actions artifacts require a GitHub login. |
| Only source files or setup.py appear | You downloaded repository source. Use your OS package in the table above. |
| Missing helper or extension ID prompt | You are using the legacy extension. Open the desktop app for the bundled workflow. |
| App does not launch | Confirm CPU architecture, fully extract the archive, and retain every bundled file. Record the exact OS warning/error. |
| Linux Qt/graphics error | Launch the portable executable from a terminal and report the missing library/plugin text and distribution version. Bundled downloader tools do not replace system GUI libraries. |
| No formats / unsupported URL | Check that the link is a public page or media URL. Try a different permitted public source; not all sites have an extractor. |
| Site worked before but now fails | Extraction can break when a website changes. Check for a newer desktop build and report the exact error. |
| Download appears finished but app is processing | Wait for merging or MP3 conversion and the Saved message. |
| Cannot find output | Click Open downloads folder; the browser Downloads panel is unrelated. |
| File ends in .mkv | Expected when merging separate streams; use a player that supports the source codecs. |
| Permission denied / disk full | Choose a writable folder with enough room for both temporary streams and final output. |

For a bug report, include the app/build version, OS and CPU architecture, exact error, and a public example URL if appropriate. Remove private paths or sensitive data.

## Update and uninstall

There is no automatic updater in this preview. Close the app, download a newer package for the same architecture, and install it again. Installing the desktop app does not update or connect the old browser extension.

- **Windows:** uninstall through the system's installed-apps settings.
- **macOS:** remove FrameDrop from Applications.
- **Linux:** remove the `framedrop` directory and `applications/framedrop.desktop` under your user data directory (normally `~/.local/share`). Remove only these FrameDrop items.

Downloaded media is separate from the app installation and is not removed by these steps.

## Verification and limitations

[All four platform jobs passed](https://github.com/inianexe/Framedrop/actions/runs/34566471892) for source commit `7227f4be7cad3f77f3fc4c36496926c5222754f5`. Packaged executable tests cover generated MP4, HTML embedded video, HLS, DASH with separate audio/video, and MP3 conversion. Offscreen GUI startup is also checked.

These tests do not establish successful downloads from every live website, interactive installation on clean machines, or universal OS support. Signing, macOS notarization, automatic updates and clean Arch installation testing remain unfinished.


## Earlier extension screenshots

These screenshots show the **v0.1.x browser extension**, not the desktop app. They demonstrate the original design, video detection and quality selection, not a completed download.

![Extension video mode](docs/screenshots/video-mode.png)
![Extension MP3 mode](docs/screenshots/mp3-mode.png)
<details><summary>Extension quality selector</summary>

![Extension available formats](docs/screenshots/quality-selector.png)

</details>

## Development

Desktop source, build scripts and platform installers live in `desktop/`. See [desktop developer instructions](docs/DESKTOP-INSTALL.md#developer-instructions). The legacy extension remains v0.1.6 and has its own helper setup; see [its complete guide](docs/EXTENSION-INSTALL.md).

## Privacy and license

Downloads and conversion run on your computer. FrameDrop has no hosted conversion service; the downloader contacts the source website and media hosts directly. See [privacy notes](PRIVACY.md).

Created by **iniexe**. Powered by yt-dlp, FFmpeg, Deno, Python and PySide6. FrameDrop source is [MIT licensed](LICENSE); bundled dependencies retain their respective licenses. FrameDrop is not affiliated with the supported websites.
