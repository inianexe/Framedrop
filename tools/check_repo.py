"""Validate packaged browser builds, versions, documentation links and JS syntax."""
import ast, json, re, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    node=shutil.which('node')
    if not node:raise SystemExit('Install Node.js to run developer syntax checks.')
    version=json.loads((ROOT/'package.json').read_text())['version']
    for folder in ('extension','extension-firefox'):
        base=ROOT/folder;manifest=json.loads((base/'manifest.json').read_text())
        assert manifest['version']==version, 'Version mismatch'
        assert 'nativeMessaging' in manifest['permissions'], 'Local helper permission missing'
        background=manifest['background']
        if folder=='extension':assert background=={'service_worker':'background.js'}
        else:
            assert background=={'scripts':['background.js']}
            assert manifest['browser_specific_settings']['gecko']['id']=='framedrop@inianexe'
        paths=list(manifest['icons'].values())+list(manifest['action']['default_icon'].values())+[manifest['action']['default_popup']]
        paths+=background.get('scripts',[background.get('service_worker')])
        for content in manifest['content_scripts']:paths+=content['js']
        for path in paths:assert path and (base/path).is_file(),f'Missing browser asset: {path}'
        for js in base.glob('*.js'):subprocess.run([node,'--check',str(js)],check=True)
    for name in ('background.js','content.js','popup.js','popup.html','popup.css'):
        assert (ROOT/'extension'/name).read_bytes()==(ROOT/'extension-firefox'/name).read_bytes(),f'Browser files drifted: {name}'
    for folder in ('helper','tools','tests'):
        for path in (ROOT/folder).glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    ast.parse((ROOT/'setup.py').read_text())
    for path in [ROOT/'README.md',ROOT/'PRIVACY.md',ROOT/'CONTRIBUTING.md',*sorted((ROOT/'docs').glob('*.md'))]:
        text=path.read_text()
        links=re.findall(r'\]\(([^)]+)\)',text)+re.findall(r'(?:src|href)="([^"]+)"',text)
        for link in links:
            if link.startswith(('https:','http:','#','mailto:')):continue
            target=link.split('#')[0]
            assert (path.parent/target).exists(),f'Broken local link in {path.name}: {link}'
    assert len(list((ROOT/'docs/screenshots').glob('*.png')))==3
    print('PASS: browser manifests, versions, source parity, JS/Python syntax, local documentation links and three screenshots.')
if __name__=='__main__':main()
