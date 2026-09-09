"""Check real native framing without contacting YouTube."""
import json, struct, subprocess, sys
from pathlib import Path
payload=json.dumps({'type':'health'}).encode()
try:
 p=subprocess.run([sys.executable,str(Path(__file__).with_name('host.py'))],input=struct.pack('<I',len(payload))+payload,capture_output=True,timeout=20)
 if len(p.stdout)<4:raise RuntimeError('Helper failed to start: '+p.stderr.decode(errors='replace')[:500])
 size=struct.unpack('<I',p.stdout[:4])[0];result=json.loads(p.stdout[4:4+size]);print(result['message'])
 if result.get('phase')!='health':sys.exit(1)
 for name,value in result['checks'].items():print(name+': '+str(value))
 sys.exit(0 if result['ok'] else 1)
except Exception as e:print('Helper check failed: '+str(e));sys.exit(1)
