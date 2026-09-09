# ✦ FrameDrop

<img src="extension/icons/logo.png" alt="FrameDrop logo" width="128">

Created by **iniexe**.

A quiet, ink-and-paper YouTube downloader for Chrome, Edge, Chromium and Firefox.
Choose an available video format or save MP3 audio through a local Python helper.

**Status: 0.1.5 developer preview.** Core code and validation tests are included.
Live YouTube downloading and browser installation have not been verified in this build environment.

## What it does

- Adds a FrameDrop button on YouTube watch pages and Shorts.
- Lists exposed video formats with resolution, frame rate, container and codec.
- Combines video-only formats with the best available audio using FFmpeg.
- Converts audio to MP3 at 128, 192 or 320 kbps.
- Shows task progress and errors; the background connection keeps running when the popup closes.
- Saves under your account's `Downloads/FrameDrop` folder.

Only formats yt-dlp can access are offered. This does not promise every quality visible in the YouTube player. Video streams keep their original codecs; separate streams are merged into MKV for compatibility. A combined source may retain MP4 or WebM. MP3 bitrate does not increase source fidelity.

Use for videos you own or have permission to download. No browser-cookie import, login bypass, DRM bypass, age-restricted downloads, playlists, live streams or cloud upload service is included.

## Install — Firefox (v0.1.5 fix)

The service_worker error means the Chromium package was loaded in Firefox. Use the separate Firefox build:

1. Extract the complete ZIP to a permanent folder.
2. Open `about:debugging#/runtime/this-firefox`.
3. Remove an earlier FrameDrop temporary add-on if present.
4. Choose **Load Temporary Add-on**, then select `extension-firefox/manifest.json`.
5. Install Python, FFmpeg/ffprobe and Deno as described below. From the project root:

Linux / macOS:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -U -r helper/requirements.txt
.venv/bin/python helper/install.py framedrop@inianexe --browser firefox
```

Windows:
```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -U -r helper\requirements.txt
.venv\Scripts\python helper\install.py framedrop@inianexe --browser firefox
```

Use the fixed add-on ID above, not Firefox's internal extension UUID. The installer uses Firefox's native-host directory and `allowed_extensions` permission. Firefox 128+ is required. Temporary add-ons disappear when Firefox restarts; load the same manifest again. Permanent installation requires a Mozilla-signed package; this ZIP is a development build. Use the toolbar icon to open FrameDrop if the page button cannot open it.

The Firefox manifest and installer paths were checked locally; actual installation and downloading still require browser validation.

## Install — Chrome / Edge / Chromium

1. Extract the complete ZIP to a permanent folder. Do not run from inside the ZIP.
2. Open `chrome://extensions` or `edge://extensions` and enable **Developer mode**.
3. Choose **Load unpacked**, then select the **extension** folder. It directly contains `manifest.json`. Do not select the project root or `helper` folder.
4. Copy the extension's 32-letter ID from that page.
5. Install Python 3.10+, FFmpeg (including ffprobe), and a JavaScript runtime supported by yt-dlp, preferably Deno. Make `ffmpeg`, `ffprobe` and `deno` available on PATH. See the official dependency instructions below.
6. In a terminal opened in the extracted project root, run:

Windows:
```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -U -r helper\requirements.txt
.venv\Scripts\python helper\install.py YOUR_EXTENSION_ID --browser chrome
```

Linux / macOS:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -U -r helper/requirements.txt
.venv/bin/python helper/install.py YOUR_EXTENSION_ID --browser chrome
```

For Edge, replace `chrome` with `edge`. For Chromium use `chromium`. Run the installer separately for each browser's extension ID. Restart the browser after installation. Keep the project and virtual environment in their installed location.

Requires a recent Chromium-based browser (Chrome 127+). Firefox uses the separate `extension-firefox` folder. Mobile is not packaged in this release. Sandboxed Snap/Flatpak browsers may not be able to launch the host; use a system-installed browser.

## Use

Open a YouTube video, then click **FrameDrop** at the bottom right or the pinned toolbar icon. Wait for format discovery, choose Video or MP3, select quality, then download. Use the refresh arrow after changing videos if needed. Cancellation can leave `.part` files; downloading the same format again may resume them. Progress is per stream, so it can restart when audio begins. Merging and MP3 conversion display an indeterminate status.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Manifest missing or unreadable | Extract ZIP; select `extension`, the folder directly containing `manifest.json`. |
| Native host not found | Run installer with the exact ID and browser. Restart browser. |
| Native host exited | Check the Python virtual environment still exists and yt-dlp is installed in it. |
| FFmpeg not found | Put both FFmpeg and ffprobe on PATH; restart browser. |
| Extraction error or missing formats | Update yt-dlp using the same environment; check Deno installation. YouTube access can differ by network/video. |
| Download button unavailable | Open a single public video and refresh. Read the status message. |
| Page button does not open | Use the pinned toolbar icon and update the browser. |

## Architecture and design

`YouTube button → extension popup → background native port → Python / yt-dlp → FFmpeg → Downloads`

Native messaging grants access only to the installed extension ID. No HTTP listener, shell command execution from page inputs, telemetry or broad browsing permissions are used. The helper validates YouTube URLs and format IDs independently. Metadata is extracted again before downloading to avoid trusting stale options.

The supplied reference informed the warm cream background, thin black outlines, outlined iconography, rounded containers, centered bold headline, serif supporting text and four-point star accents. The original character artwork is not copied. The visual order is identity → illustration → current video → output type → quality → primary action → status. Setup instructions stay collapsed.

## Development and checks

```sh
python3 -m unittest discover -s tests
node --check extension/background.js
node --check extension/popup.js
node --check extension/content.js
```

Optional UI smoke test (mock metadata, no real downloads):
```sh
npm install
npx playwright install chromium
npm run test:ui
```

The UI test creates `docs/interface.png`. At delivery, the four Python validation tests and JS syntax checks passed. UI execution was blocked because this environment has no browser binary. Native messaging, all OS installers, cancellation during conversion and real YouTube downloads still require manual validation. Do not describe this developer preview as production-tested.

## GitHub

Prepared as a standalone project. The connected GitHub tools could inspect repositories but offered no repository-creation action, so this project was not pushed into an unrelated existing repository. Create an empty `FrameDrop` repository, then from this folder:

```sh
git init -b main
git add .
git commit -m "Build FrameDrop developer preview"
git remote add origin https://github.com/inianexe/FrameDrop.git
git push -u origin main
```

## References

- [yt-dlp installation, formats and dependencies](https://github.com/yt-dlp/yt-dlp#readme)
- [Chrome native messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging)
- [FFmpeg](https://ffmpeg.org/download.html)
- [Deno installation](https://docs.deno.com/runtime/getting_started/installation/)

License: MIT for FrameDrop code. Dependencies retain their own licenses.

## Motion and interaction (0.1.5)

Explored three directions: floating paper cards, an audio-reactive illustration, and restrained action feedback. The final design combines short paper entrances, a sliding segmented switch, a Video/MP3 illustration swap, press feedback, an inspecting spinner, a download-arrow bounce, processing rotation, MP3 equalizer bars and a one-shot success sparkle burst. Hover tilt and quality-selection feedback add tactile detail. Idle content does not loop.

Motion is CSS-based, uses no remote library, respects system reduced-motion settings and can be switched off inside the popup. The preference persists. Success celebration occurs only after an observed active download completes, not when reopening an old success state. Quality choices now survive progress updates and switching modes.

Validation: JavaScript syntax checked. Browser rendering and live downloading are still unverified in this environment.

## Helper disconnection fix (0.1.5)

The recording showed a native-helper disconnect before formats arrived. This build reads Firefox's Port.error, handles synchronous launch failures, expands setup instructions on connection failure, shows the tab title before extraction and avoids restoring stale busy state from a dead background process. The popup is more compact so status is easier to see.

**Loading the extension alone cannot download videos.** Install Python 3.10+, FFmpeg/ffprobe and Deno on PATH. From the extracted `framedrop` folder, Firefox users can run:

```sh
python3 setup.py --browser firefox
```

Windows: `py setup.py --browser firefox`. Chrome/Edge: append `--browser chrome --id YOUR_EXTENSION_ID` (or `edge`) instead. Setup creates a virtual environment, updates yt-dlp, checks helper framing and dependencies, then registers the native host. It stops with actionable missing-dependency output instead of silently registering a broken environment. It does not install FFmpeg or Deno.

For an existing environment, run `.venv/bin/python helper/doctor.py` (Windows: `.venv\Scripts\python helper\doctor.py`). This tests the helper subprocess, not the browser registration. On Unix the installer preserves the setup terminal's PATH in the launcher to make dependencies visible to GUI browsers. Keep the installed folder in place; rerun setup after moving it.

The regression tests cover Firefox and Chrome disconnection errors, synchronous launch failure, successful helper replies and cancelling. Actual browser registration and YouTube download still need verification on the user's machine.
