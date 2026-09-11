"""Build on the target OS. Download Deno from its official release with digest validation."""
import hashlib, json, os, platform, subprocess, sys, urllib.request, zipfile, io
from pathlib import Path
root = Path(__file__).resolve().parent
os.chdir(root)
arch = 'aarch64' if platform.machine().lower() in ('arm64', 'aarch64') else 'x86_64'
suffix = {'win32':'pc-windows-msvc','darwin':'apple-darwin','linux':'unknown-linux-gnu'}[sys.platform]
name = f'deno-{arch}-{suffix}.zip'
headers = {'User-Agent':'FrameDrop-build'}
if os.environ.get('GH_TOKEN'):
    headers['Authorization'] = 'Bearer '+os.environ['GH_TOKEN']
request = urllib.request.Request('https://api.github.com/repos/denoland/deno/releases/latest', headers=headers)
release = json.load(urllib.request.urlopen(request))
asset = next(a for a in release['assets'] if a['name'] == name)
raw = urllib.request.urlopen(asset['browser_download_url']).read()
digest = asset.get('digest', '')
if digest != 'sha256:'+hashlib.sha256(raw).hexdigest():
    raise RuntimeError('Deno release digest missing or mismatched; refusing build.')
(root/'bin').mkdir(exist_ok=True)
exe = 'deno.exe' if os.name == 'nt' else 'deno'
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    (root/'bin'/exe).write_bytes(archive.read(exe))
(root/'bin'/exe).chmod(0o755)
subprocess.run([str(root/'bin'/exe), '--version'], check=True)
import imageio_ffmpeg
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-version'], check=True)
subprocess.run([sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--windowed',
    '--name', 'FrameDrop', '--add-data', str(root.parent/'extension/icons/icon-128.png')+os.pathsep+'.', '--collect-all', 'yt_dlp', '--collect-all', 'yt_dlp_ejs',
    '--collect-all', 'imageio_ffmpeg', '--add-binary', str(root/'bin'/exe)+os.pathsep+'bin', 'app.py'], check=True)
(root/'dist'/'BUILD-INFO.json').write_text(json.dumps({'deno':release['tag_name'],'deno_sha256':digest,'platform':platform.platform()}, indent=2))
