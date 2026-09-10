# Validation record

Repository edition: **0.1.6**. Prepared: **2026-09-10**.

## Checks run locally

- Python URL validation, unsupported-content guard, and format filtering: four unit tests.
- Installer ID prompting and validation: seven tests, including non-interactive input, Firefox ID and cancellation.
- JavaScript background messaging: five regressions for Firefox `Port.error`, Chrome `runtime.lastError`, synchronous launch failure, normal completion/disconnection, and cancellation.
- Both browser manifests, version consistency, icon and script references, and shared-source parity.
- JavaScript syntax and Python parsing.
- Relative documentation/image links and inclusion of all three supplied screenshots.
- ZIP structure, CRC integrity, and exclusion of environments/caches/generated registrations.

The screenshot evidence shows an identified video, exposed quality choices and MP3 mode. It is not a completed-download or installer test.

## Not independently verified in this environment

- A completed live YouTube video download and MP3 conversion through the browser.
- Full native-messaging installation on Windows, macOS and every browser variant.
- Rendered UI animations: the optional Playwright test is provided, but the build environment has no browser binary.
- The GitHub Actions run, which can only occur after repository upload.

## Manual check before declaring a stable release

Install the dependencies on the target computer, load the correct browser manifest, run setup, and confirm the diagnostic succeeds. Use a short public video you own or have permission to save. Verify the discovered title and quality list, download video and MP3, then open the actual files and confirm audio/video playback. Check cancellation, popup reopening, helper errors, and reduced-motion behavior. Record the tested OS, browser, dependency versions and result in a follow-up validation entry.
