# Contributing

Keep FrameDrop's local-helper workflow straightforward and preserve the cream-and-black interface.

1. Create a feature branch for a focused change.
2. Keep shared code in `extension/` and `extension-firefox/` synchronized; their manifests intentionally differ.
3. Preserve the Firefox add-on ID because native-host registrations use it.
4. Run the commands below and describe any manual checks in your pull request.

```sh
python3 -m unittest discover -s tests
node --test tests/background.cjs
python3 tools/check_repo.py
```

Optional UI testing uses Playwright and mocked metadata. It does not verify native messaging or live downloads:

```sh
npm install
npx playwright install chromium
npm run test:ui
```

For installation changes, check the relevant OS/browser registration with an isolated test environment before changing a real host registration. For media changes, validate with content you own or have permission to download. Do not add cookie import or access-control bypasses.

Do not commit `.venv`, generated helper launchers, host registration files, downloaded media, credentials, or build artifacts. Update the README when setup commands or behavior change. Keep versions consistent in both manifests and `package.json`.
