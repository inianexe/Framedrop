# Upload FrameDrop to GitHub

This ZIP contains the complete **local-helper** project. No cloud backend is required.

## 1. Extract the ZIP

Extract the downloaded archive. Open the `FrameDrop` folder inside it. `README.md`, `setup.py`, `extension`, `extension-firefox`, `helper`, `docs`, and `tests` should appear together.

## 2. Create a repository

On GitHub, select **New repository**.

- **Suggested name:** `FrameDrop`
- **Suggested description:** `A cream-and-black YouTube video and MP3 downloader with source-quality selection, subtle animations, and local processing. By iniexe.`
- **Visibility:** choose Public if you want anyone to browse or download it; otherwise Private.
- Leave automatic README, `.gitignore`, and license creation unchecked: this package already includes them.

## 3. Upload the extracted contents

On the empty repository page, choose **uploading an existing file**. For an existing repository use **Add file → Upload files**.

Drag the **contents inside `FrameDrop`** into the upload area, retaining all subfolders. Do not upload the outer folder as a nested `FrameDrop/` directory, and do not upload only the ZIP.

Check that `README.md` is at the repository root and `docs/screenshots` contains the three PNG files. The repository also includes `.github`, `.gitignore`, and `.gitattributes`; ensure they are included. If your file picker does not expose those project files, use Git as described below to preserve the complete tree.

Commit with a message such as:

```text
Add FrameDrop local-helper extension and installation guide
```

After upload, check:

- The README renders on the main repository page.
- All three screenshot images display.
- Both browser manifests and all helper files are present.
- The Actions tab shows the result of the repository checks. The workflow runs only after upload; a workflow file alone is not evidence of success.

### Alternative: upload with Git

From the extracted project root:

```sh
git init -b main
git add .
git commit -m "Add FrameDrop local-helper extension and installation guide"
git remote add origin https://github.com/YOUR_USERNAME/FrameDrop.git
git push -u origin main
```

Replace `YOUR_USERNAME` with the account that owns the new repository. Authenticate through your normal Git credential manager. Do not paste credentials into source files. If the remote already contains commits, clone it first and copy the project files into that checkout rather than force-pushing over existing work.

## 4. Optional GitHub Release

Once uploaded and checked, create a release with tag `v0.1.6` and title **FrameDrop v0.1.6 — Local Video & MP3 Downloader**. Mark it as a **pre-release** while live-download/cross-platform verification is incomplete.

Suggested release notes:

> FrameDrop brings video-format selection and MP3 conversion to YouTube through a local helper. Includes Chrome/Edge and Firefox builds, an animated cream-and-black interface, a dependency checker, and detailed installation instructions. Install Python, FFmpeg/ffprobe and Deno, load the browser extension, then run setup as shown in the README. This is a developer preview; not all platforms and download paths have been verified.

Attach the complete repository ZIP as a release asset. Users need the helper and setup files, not just a browser-only archive. To rebuild a clean ZIP from source:

```sh
python3 tools/package_repo.py
```

On Windows use `py tools/package_repo.py`. The archive is created in `dist/`. The packaging script excludes environments, caches and machine-specific helper registrations.

The default GitHub source archives also contain the complete committed project. A source ZIP is not a signed Firefox add-on and is not a Chrome Web Store publication.
