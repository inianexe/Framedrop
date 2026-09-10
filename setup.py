"""Create the helper environment, check dependencies, then register the browser."""
import argparse
import os
import re
import subprocess
import sys
import venv
from pathlib import Path

FIREFOX_ID = 'framedrop@inianexe'
BROWSER_PAGES = {'chrome': 'chrome://extensions', 'edge': 'edge://extensions', 'chromium': 'chrome://extensions'}

def resolve_id(args, parser):
    """Resolve user input before creating files or installing dependencies."""
    if args.browser == 'firefox':
        if args.id is not None and args.id.strip() != FIREFOX_ID:
            parser.error('Firefox uses the fixed ID framedrop@inianexe. Omit --id for Firefox.')
        return FIREFOX_ID
    value = args.id
    if value is None:
        page = BROWSER_PAGES[args.browser]
        instructions = (
            f'Open {page}, enable Developer mode, and load the extension folder. '
            'Copy the 32-letter ID shown on the FrameDrop card. '
            f'You can also run: python3 setup.py --browser {args.browser} --id YOUR_EXTENSION_ID'
        )
        if not sys.stdin.isatty():
            parser.error('An extension ID is required in non-interactive mode. ' + instructions)
        print(instructions)
        try:
            value = input('Paste the FrameDrop extension ID: ')
        except (EOFError, KeyboardInterrupt):
            parser.error('Setup cancelled before making changes. Run setup again when you have the extension ID.')
    value = value.strip()
    if not re.fullmatch(r'[a-p]{32}', value):
        parser.error('Invalid extension ID: paste exactly 32 lowercase letters a–p from the FrameDrop card. Do not paste a URL or the placeholder YOUR_EXTENSION_ID.')
    return value

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=['firefox', 'chrome', 'edge', 'chromium'], default='firefox')
    parser.add_argument('--id', help='Chrome/Edge/Chromium extension ID; prompts if omitted in an interactive terminal.')
    args = parser.parse_args(argv)
    extension_id = resolve_id(args, parser)
    root = Path(__file__).resolve().parent
    environment = root / '.venv'
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    try:
        if not python.exists():
            venv.EnvBuilder(with_pip=True).create(environment)
        subprocess.run([str(python), '-m', 'pip', 'install', '-U', '-r', str(root / 'helper/requirements.txt')], check=True)
        subprocess.run([str(python), str(root / 'helper/doctor.py')], check=True)
        subprocess.run([str(python), str(root / 'helper/install.py'), extension_id, '--browser', args.browser], check=True)
        print('Setup complete. Reload FrameDrop and refresh the video. Keep this folder in place.')
    except (subprocess.CalledProcessError, OSError):
        print('Setup did not finish. Resolve the error above and run this command again.')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
