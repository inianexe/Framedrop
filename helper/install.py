"""Register this Python environment as the FrameDrop native host."""
import argparse, json, os, re, shlex, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('extension_id');p.add_argument('--browser',choices=['chrome','edge','chromium','firefox'],default='chrome');a=p.parse_args()
if a.browser == 'firefox' and a.extension_id != 'framedrop@inianexe': p.error('Firefox ID must be framedrop@inianexe.')
if a.browser != 'firefox' and not re.fullmatch('[a-p]{32}',a.extension_id):p.error('Copy the 32-letter ID from the browser extensions page.')
base=Path(__file__).resolve().parent; host=base/'host.py'; name='com.framedrop.helper'
if sys.platform=='win32':
    import winreg
    launcher=base/'launch.cmd';launcher.write_text('@echo off\r\n"'+sys.executable+'" "'+str(host)+'"\r\n')
    manifest=base/(name+'.'+a.browser+'.json')
    key={'chrome':'Google\\Chrome','edge':'Microsoft\\Edge','chromium':'Chromium','firefox':'Mozilla'}[a.browser]
    registry=winreg.CreateKey(winreg.HKEY_CURRENT_USER,'Software\\'+key+'\\NativeMessagingHosts\\'+name)
    winreg.SetValueEx(registry,'',0,winreg.REG_SZ,str(manifest));winreg.CloseKey(registry)
else:
    launcher=base/'launch.sh';launcher.write_text('#!/bin/sh\nexport PATH='+shlex.quote(os.environ.get('PATH','/usr/bin:/bin'))+'\nexec '+shlex.quote(sys.executable)+' '+shlex.quote(str(host))+'\n');launcher.chmod(0o700)
    if a.browser == 'firefox':
        manifest=Path.home()/('Library/Application Support/Mozilla/NativeMessagingHosts' if sys.platform=='darwin' else '.mozilla/native-messaging-hosts')/(name+'.json')
    elif sys.platform=='darwin': root=Path.home()/'Library/Application Support'/ {'chrome':'Google/Chrome','edge':'Microsoft Edge','chromium':'Chromium'}[a.browser]
    else: root=Path(os.environ.get('XDG_CONFIG_HOME',str(Path.home()/'.config')))/{'chrome':'google-chrome','edge':'microsoft-edge','chromium':'chromium'}[a.browser]
    if a.browser != 'firefox': manifest=root/'NativeMessagingHosts'/(name+'.json')
    manifest.parent.mkdir(parents=True,exist_ok=True)
manifest.write_text(json.dumps({'name':name,'description':'FrameDrop local media helper','path':str(launcher),'type':'stdio',**({'allowed_extensions':[a.extension_id]} if a.browser=='firefox' else {'allowed_origins':['chrome-extension://'+a.extension_id+'/']})},indent=2))
print('Installed for '+a.browser+'. Keep this folder in place and restart the browser.')
