"""Create a clean, complete repository ZIP. Includes both extensions and helper."""
import json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','.venv','node_modules','__pycache__','dist','artifacts','.pytest_cache'}
def main():
    version=json.loads((ROOT/'package.json').read_text())['version']
    output=ROOT/'dist'/f'FrameDrop-{version}-repository.zip';output.parent.mkdir(exist_ok=True)
    count=0
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(ROOT.rglob('*')):
            rel=file.relative_to(ROOT)
            if not file.is_file() or any(p in EXCLUDED for p in rel.parts):continue
            if file.suffix in ('.pyc','.zip') or file.name.startswith('.env') or file.name in ('.DS_Store','Thumbs.db'):continue
            if rel.parts[0]=='helper' and (file.name.startswith('launch.') or file.name.startswith('com.framedrop.helper')):continue
            archive.write(file,Path('FrameDrop')/rel);count+=1
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        for item in ('README.md','setup.py','extension/manifest.json','extension-firefox/manifest.json','helper/host.py','.github/workflows/checks.yml'):
            assert 'FrameDrop/'+item in archive.namelist()
    print(f'{count} files packaged: {output}')
if __name__=='__main__':main()
