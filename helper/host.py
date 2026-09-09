#!/usr/bin/env python3
"""One native connection per task; stdout is reserved for framed JSON."""
import json, os, re, shutil, struct, sys, time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

def canonical_url(value):
    u = urlparse(value)
    if u.scheme != 'https' or u.hostname not in ('www.youtube.com', 'youtube.com', 'youtu.be') or u.username or u.port:
        raise ValueError('Use a valid HTTPS YouTube video URL.')
    vid = u.path.strip('/') if u.hostname == 'youtu.be' else (u.path.split('/')[2] if u.path.startswith('/shorts/') else parse_qs(u.query).get('v', [''])[0] if u.path == '/watch' else '')
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', vid):
        raise ValueError('Open a single YouTube video, not a playlist or channel.')
    return 'https://www.youtube.com/watch?v=' + vid

def guard(info):
    if info.get('age_limit', 0) >= 18:
        raise ValueError('Age-restricted videos are not supported.')
    if info.get('is_live') or info.get('live_status') == 'is_upcoming':
        raise ValueError('Live and upcoming streams are not supported.')
    if info.get('has_drm'):
        raise ValueError('Protected videos are not supported.')

def formats(info):
    result = []
    for f in info.get('formats', []):
        if f.get('has_drm') or f.get('vcodec') in (None, 'none') or not f.get('height'):
            continue
        fid = str(f['format_id'])
        if not re.fullmatch(r'[A-Za-z0-9_-]+', fid): continue
        label = f"{f['height']}p · {f.get('fps') or 30:g} fps · {f.get('ext', '?').upper()} · {f.get('vcodec', '').split('.')[0]}"
        if f.get('dynamic_range') not in (None, 'SDR'): label += ' · ' + f['dynamic_range']
        result.append({'id': fid, 'label': label, 'height': f['height'], 'fps': f.get('fps') or 0})
    return sorted(result, key=lambda f: (f['height'], f['fps']), reverse=True)

def emit(data):
    raw = json.dumps(data).encode(); sys.stdout.buffer.write(struct.pack('<I', len(raw)) + raw); sys.stdout.buffer.flush()

class QuietLogger:
    def debug(self, message): pass
    def warning(self, message): pass
    def error(self, message): pass

def run(req):
    if req.get('type') == 'health':
        import importlib.util
        checks = {name: shutil.which(name) or 'MISSING — install and add to PATH' for name in ('ffmpeg','ffprobe','deno')}
        checks['yt-dlp'] = 'installed' if importlib.util.find_spec('yt_dlp') else 'MISSING — rerun setup.py'
        ok = all(not value.startswith('MISSING') for value in checks.values())
        emit({'phase':'health','ok':ok,'checks':checks,'message':'Native helper framing OK. ' + ('Dependencies ready.' if ok else 'Resolve the missing dependencies below, then rerun setup.')}); return
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        emit({'phase':'error','setupRequired':True,'message':'yt-dlp is missing from the helper environment. Run python3 setup.py --browser firefox, or the Windows equivalent in README.'}); return
    url = canonical_url(req.get('url', ''))
    opts = {'quiet': True, 'no_warnings': True, 'logger': QuietLogger(), 'noplaylist': True, 'socket_timeout': 25, 'retries': 3, 'age_limit': 17}
    with YoutubeDL(opts) as ydl: info = ydl.extract_info(url, download=False)
    guard(info)
    choices = formats(info)
    if req['type'] == 'inspect':
        emit({'phase': 'ready', 'message': 'Choose a quality and make it yours.', 'info': {'url': req['url'], 'title': info['title'], 'formats': choices}}); return
    if req['type'] != 'download': raise ValueError('Unknown operation.')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'): raise ValueError('Install FFmpeg and ffprobe, add them to PATH, then restart your browser.')
    mode, fmt = req.get('mode'), req.get('format')
    if mode == 'audio':
        if fmt not in ('128', '192', '320'): raise ValueError('Invalid MP3 bitrate.')
        opts.update(format='bestaudio/best', postprocessors=[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':fmt}])
    elif mode == 'video':
        if fmt not in {f['id'] for f in choices}: raise ValueError('This format is no longer available. Refresh the video.')
        original = next(f for f in info['formats'] if str(f['format_id']) == fmt)
        opts.update(format=fmt + ('+bestaudio' if original.get('acodec') in (None,'none') else ''), merge_output_format='mkv')
    else: raise ValueError('Invalid download type.')
    target = Path.home() / 'Downloads' / 'FrameDrop'; target.mkdir(parents=True, exist_ok=True)
    last = [0.0]
    def progress(d):
        now = time.monotonic()
        if d['status'] == 'finished': emit({'phase':'processing','message':'Merging or converting locally…','percent':None})
        elif d['status'] == 'downloading' and now-last[0] > .25:
            last[0]=now; total=d.get('total_bytes') or d.get('total_bytes_estimate')
            emit({'phase':'downloading','message':'Downloading media stream…','percent': min(100, d.get('downloaded_bytes',0)*100/total) if total else None})
    suffix = ' [' + fmt + 'kbps]' if mode == 'audio' else ''
    opts.update(outtmpl=str(target / ('%(title).150B [%(id)s] [%(format_id)s]' + suffix + '.%(ext)s')), windowsfilenames=True, progress_hooks=[progress])
    with YoutubeDL(opts) as ydl: ydl.download([url])
    emit({'phase':'complete','message':f'Saved to {target}', 'percent':100})

def main():
    if os.name == 'nt':
        import msvcrt
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY); msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    try:
        head=sys.stdin.buffer.read(4)
        if len(head)!=4:return
        length=struct.unpack('<I',head)[0]
        if length>65536:raise ValueError('Request too large.')
        run(json.loads(sys.stdin.buffer.read(length)))
    except Exception as exc: emit({'phase':'error','message':str(exc)[:700]})
if __name__ == '__main__': main()
