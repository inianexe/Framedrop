"""Real extraction and MP3 conversion against a locally generated media fixture."""
import functools, http.server, subprocess, tempfile, threading, unittest
from pathlib import Path
from engine import Engine, choices

class DownloadTests(unittest.TestCase):
    def test_direct_media_and_mp3(self):
        import imageio_ffmpeg
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ff = Engine().options()['ffmpeg_location']
            ff = str(Path(ff)/'ffmpeg') if Path(ff).is_dir() else ff
            subprocess.run([ff, '-y', '-f','lavfi','-i',
                'color=c=black:s=160x90:d=1','-f','lavfi','-i','sine=frequency=440:duration=1',
                '-c:v','libx264','-c:a','aac','-shortest',str(root/'fixture.mp4')],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=tmp)
            server = http.server.ThreadingHTTPServer(('127.0.0.1',0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f'http://127.0.0.1:{server.server_port}/fixture.mp4'
                engine = Engine()
                info = engine.inspect(url)
                engine.download(url, 'video', choices(info)[0]['id'], root/'video')
                engine.download(url, 'audio', '192', root/'audio')
                self.assertTrue(list((root/'video').glob('*.mp4')))
                mp3 = next((root/'audio').glob('*.mp3'))
                self.assertGreater(mp3.stat().st_size, 1000)
                for manifest, output_opts in [('stream.m3u8', ['-f', 'hls']), ('stream.mpd', ['-f', 'dash'])]:
                    subprocess.run([ff, '-y', '-i', str(root/'fixture.mp4'), '-c', 'copy'] + output_opts + [str(root/manifest)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    link = f'http://127.0.0.1:{server.server_port}/{manifest}'
                    media = engine.inspect(link)
                    destination = root/manifest.replace('.', '_')
                    engine.download(link, 'video', choices(media)[0]['id'], destination)
                    self.assertTrue(any(p.suffix in ('.mp4', '.mkv') and p.stat().st_size > 1000 for p in destination.iterdir()))
            finally:
                server.shutdown()
                server.server_close()
