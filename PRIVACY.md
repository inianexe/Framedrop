# Privacy

FrameDrop v0.1.5 uses a local helper, with no FrameDrop-hosted download server, account system, or analytics endpoint.

## What the extension handles

When you open the popup on YouTube, the extension reads the active tab URL and title to identify the video. It sends the selected video URL and requested format to the registered helper. Format discovery can begin when the popup opens, before the Download button is pressed.

The extension stores its current task state, video metadata, status messages, and motion preference in browser-local extension storage. The code uses `storage.local`, not browser sync storage. Stored task state may include a video URL/title and a local output path. There is no dedicated history list or automatic state-expiry policy in this version. Uninstalling the extension removes its browser-managed data according to the browser's behavior; downloaded media remains on disk.

## Network activity and files

The Python helper uses yt-dlp to contact YouTube and media hosts to extract metadata and download streams. FFmpeg processes files locally. Network requests are visible to the contacted services and normal network intermediaries. yt-dlp may maintain its normal local cache. FrameDrop does not import browser cookies or send media to its own cloud service.

Setup uses pip to fetch Python dependencies and writes a native-host registration for the selected browser. It saves machine-specific launcher paths; on Unix the launcher also records the installation terminal's PATH. Keep generated launchers and registrations out of public repositories. Downloaded and partial files are written under the user's `Downloads/FrameDrop` directory.

## Permissions

| Permission or access | Reason |
| --- | --- |
| `activeTab` | Identify the video in the active tab when invoked |
| `nativeMessaging` | Communicate with the installed helper |
| `storage` | Save task status and the motion preference |
| YouTube content-script match | Display the FrameDrop button on YouTube watch pages and Shorts |

The host registration authorizes the selected extension ID. It does not open an HTTP service on your computer.

## Screenshots and reports

Repository screenshots are supplied by the project owner. Bug reports may be public; remove personal paths and unrelated private information before posting. Third-party sites and dependencies have their own policies.
