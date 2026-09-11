import unittest
from engine import validate_url, guard, choices

class EngineTests(unittest.TestCase):
    def test_public_links(self):
        for url in ['https://example.org/movie.mp4', 'https://vimeo.com/123', 'https://example.org/a.m3u8?token=abc']:
            self.assertEqual(validate_url(url), url)
    def test_invalid_links(self):
        for url in ['file:///etc/passwd', 'javascript:alert(1)', 'https://name:secret@example.org/v', 'blob:https://example.org/id']:
            with self.assertRaises(ValueError): validate_url(url)
    def test_protected_content(self):
        for info in [{'age_limit':18}, {'has_drm':True}, {'is_live':True}, {'availability':'private'}]:
            self.assertTrue(guard(info))
        self.assertIsNone(guard({'age_limit':0}))
    def test_unknown_resolution_and_drm(self):
        info = {'formats':[{'format_id':'http-1','ext':'mp4'}, {'format_id':'drm','vcodec':'h264','has_drm':True}]}
        self.assertEqual([f['id'] for f in choices(info)], ['http-1'])
