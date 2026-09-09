"""Create the helper environment, check dependencies, then register the browser."""
import argparse, os, subprocess, sys, venv
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--browser',choices=['firefox','chrome','edge','chromium'],default='firefox');p.add_argument('--id');a=p.parse_args()
if a.browser!='firefox' and not a.id:p.error('Supply --id with your extension ID for Chromium browsers.')
root=Path(__file__).resolve().parent;env=root/'.venv';python=env/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
try:
 if not python.exists():venv.EnvBuilder(with_pip=True).create(env)
 subprocess.run([str(python),'-m','pip','install','-U','-r',str(root/'helper/requirements.txt')],check=True)
 subprocess.run([str(python),str(root/'helper/doctor.py')],check=True)
 subprocess.run([str(python),str(root/'helper/install.py'),a.id or 'framedrop@inianexe','--browser',a.browser],check=True)
 print('Setup complete. Reload FrameDrop and refresh the video. Keep this folder in place.')
except (subprocess.CalledProcessError,OSError) as e:
 print('Setup did not finish. Resolve the error above and run this command again.');sys.exit(1)
