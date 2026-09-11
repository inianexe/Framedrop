"""Local public-video extraction. No cookies, credentials, or DRM bypass."""
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit


def validate_url(value):
    value = value.strip()
    u = urlsplit(value)
    if u.scheme not in ('http', 'https') or not u.hostname or u.username or u.password:
        raise ValueError('Paste a public HTTP or HTTPS video page or media link.')
    return value


def guard(info, *, incomplete=False):
    if info.get('age_limit', 0) >= 18:
        return 'Age-restricted content is not supported.'
    if info.get('has_drm'):
        return 'Protected content is not supported.'
    if info.get('is_live') or info.get('live_status') in ('is_live', 'is_upcoming'):
        return 'Live and upcoming streams are not supported.'
    if info.get('availability') in ('private', 'premium_only', 'subscriber_only', 'needs_auth'):
        return 'This video requires access that FrameDrop does not support.'
    return None


def choices(info):
    result = []
    for f in info.get('formats', []):
        if f.get('has_drm') or f.get('vcodec') in (None, 'none'):
            continue
        result.append({'id': str(f['format_id']), 'label': '{} · {} · {}'.format(
            str(f['height'])+'p' if f.get('height') else 'Source quality',
            f.get('ext', '?').upper(), f.get('vcodec', '?'))})
    return list(reversed(result))


class Engine:
    def __init__(self, progress=lambda data: None):
        self.progress = progress

    def options(self):
        import imageio_ffmpeg
        root = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
        deno = root / 'bin' / ('deno.exe' if os.name == 'nt' else 'deno')
        opts = dict(quiet=True, no_warnings=True, noplaylist=True, age_limit=17,
                    match_filter=guard, socket_timeout=25, retries=3,
                    ffmpeg_location=imageio_ffmpeg.get_ffmpeg_exe(),
                    progress_hooks=[self.progress], windowsfilenames=True)
        if deno.exists():
            opts['js_runtimes'] = {'deno': {'path': str(deno)}}
        return opts

    def inspect(self, url):
        from yt_dlp import YoutubeDL
        with YoutubeDL(self.options()) as ydl:
            info = ydl.extract_info(validate_url(url), download=False)
        if not info:
            raise ValueError('No supported public video was found.')
        if info.get('_type') in ('playlist', 'multi_video') or 'entries' in info:
            raise ValueError('This page contains multiple videos. Paste a single video link.')
        reason = guard(info)
        if reason:
            raise ValueError(reason)
        if not choices(info):
            raise ValueError('No unprotected video formats were found on this page.')
        return info

    def download(self, url, mode, selection, folder):
        from yt_dlp import YoutubeDL
        info = self.inspect(url)
        opts = self.options()
        if mode == 'audio':
            if selection not in ('128', '192', '320'):
                raise ValueError('Choose a supported MP3 bitrate.')
            opts.update(format='bestaudio/best', postprocessors=[dict(
                key='FFmpegExtractAudio', preferredcodec='mp3', preferredquality=selection)])
        else:
            if selection not in {f['id'] for f in choices(info)}:
                raise ValueError('The available formats changed. Analyze this link again.')
            # A callable selects exact IDs without interpreting them as format expressions.
            def select(context):
                video = next(f for f in context['formats'] if str(f['format_id']) == selection)
                if video.get('acodec') not in (None, 'none'):
                    yield video
                    return
                audio = next((f for f in reversed(context['formats'])
                              if f.get('vcodec') == 'none' and f.get('acodec') not in (None, 'none')
                              and not f.get('has_drm')), None)
                if audio:
                    yield dict(format_id=video['format_id']+'+'+audio['format_id'], ext='mkv',
                               requested_formats=[video, audio], protocol=video['protocol']+'+'+audio['protocol'])
                else:
                    yield video
            opts.update(format=select, merge_output_format='mkv')
        target = Path(folder).expanduser().resolve()
        target.mkdir(parents=True, exist_ok=True)
        opts['outtmpl'] = str(target / '%(title).150B [%(id)s].%(ext)s')
        with YoutubeDL(opts) as ydl:
            result = ydl.download([validate_url(url)])
        if result:
            raise ValueError('The download could not be completed.')
