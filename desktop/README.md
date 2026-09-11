# FrameDrop Desktop — preview

A local desktop app for public video links. Paste a link from any browser, choose **Analyze link**, select video quality or MP3, choose a save folder, and download.

## Platform builds

The Desktop builds workflow builds Windows x64, Linux x64 (Ubuntu 22.04 baseline, including compatible Arch systems), macOS Apple Silicon, and macOS Intel concurrently. This does not cover Android, iOS, Windows ARM, or every Linux distribution.

Download your platform artifact from GitHub Actions, extract the outer ZIP and enclosed tar.gz, and keep the extracted folder intact. Windows: open `FrameDrop/FrameDrop.exe`. Linux: open `FrameDrop/FrameDrop`. macOS: open `FrameDrop.app`.

These are unsigned developer previews. Windows also has a per-user setup executable, macOS a drag-to-Applications DMG, and Linux an install-linux.sh script that adds FrameDrop to the application menu without sudo. macOS notarization, Windows signing, and automatic updates remain release work. Do not disable operating-system protections to run a build. The app bundles Python, Qt, yt-dlp, its EJS package, FFmpeg, and Deno. FFmpeg is supplied through imageio-ffmpeg; the desktop engine does not require a separate ffprobe executable. This differs from the legacy extension helper.

No browser extension, extension ID, Python installation, or manual pip commands are required for packaged builds. Downloads still need internet access. Desktop and extension are separate interfaces; the extension is currently YouTube-only.

## Supported links and limits

- Public video pages recognized by yt-dlp extractors.
- Direct HTTP(S) media files and supported unprotected HLS/DASH manifests.
- Generic embedded players when yt-dlp can discover the media.
- Unknown resolution formats are labeled Source quality.

Not every link works. Browser-local blob URLs, DRM, restricted/private content, age-restricted videos, live streams and multi-video pages are not supported. No browser cookies or credentials are imported. Site changes may require a new app build. A listed extractor does not guarantee that every video on a site works. Download only content you are permitted to save.

Separate video and audio tracks merge into MKV without codec conversion. MP3 offers 128, 192, and 320 kbps; this cannot improve the source. Operations run off the UI thread. Finish the current operation before closing the preview app.

## Developer build

On each target OS with Python 3.12:

```sh
python -m pip install -r desktop/requirements.txt
python -m unittest discover -s desktop -p 'test_*.py'
python desktop/build.py
```

Deno comes from its official GitHub release, verified against the release asset SHA-256 digest. Builds fail if that digest is unavailable or mismatched. Runtime dependencies currently resolve within the declared ranges; a fully reproducible release needs a reviewed dependency lock and redistribution/license audit. Build metadata records Deno's version and digest.

## How video links work

A URL may return a complete media file, HTML referencing a player, or a manifest listing tracks and segments. HLS uses playlists (often `.m3u8`); DASH uses MPD manifests. Players may request expiring media URLs through site-specific APIs. A `blob:` URL is only a browser-local reference, not a public download URL.

FrameDrop delegates page discovery and manifest interpretation to yt-dlp, then FFmpeg handles merging/conversion locally. It does not execute arbitrary page JavaScript as a browser, intercept traffic, or decrypt protected streams. The optional Deno runtime supports yt-dlp's YouTube extraction requirements.

Research: [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp), [MDN media delivery](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Audio_and_video_delivery), [PyInstaller packaging](https://pyinstaller.org/en/stable/).
