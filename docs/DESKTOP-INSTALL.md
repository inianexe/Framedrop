# FrameDrop Desktop installation and usage

The [main README](../README.md) is the complete desktop guide:

- [Download the correct OS/CPU package](../README.md#download)
- [Install on Windows, macOS, Linux or Arch-based desktops](../README.md#installation)
- [Download video or MP3 and find saved files](../README.md#usage)
- [Troubleshoot problems](../README.md#troubleshooting)
- [Update or uninstall](../README.md#update-and-uninstall)
- [Preview validation and limitations](../README.md#verification-and-limitations)

Desktop packages bundle the downloader tools. The [legacy extension guide](EXTENSION-INSTALL.md) is a separate manual setup.

Release publication is pending. [Prepared release notes and installer list](RELEASE-v0.2.0.md).

## Developer instructions

Build on each target OS with Python 3.12:

```sh
python -m pip install -r desktop/requirements.txt
python desktop/build.py
python -m unittest discover -s desktop -p 'test_*.py'
```

Build before testing on Linux so tests use the corrected bundled FFmpeg. The desktop workflow installs the required Linux graphics libraries before packaging. See [the successful four-platform run](https://github.com/inianexe/Framedrop/actions/runs/34566471892) and [workflow source](../.github/workflows/desktop.yml).
