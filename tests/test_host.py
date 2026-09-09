import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'helper'))
from host import canonical_url, formats, guard
class HostTests(unittest.TestCase):
 def test_urls(self):
  for u in ['https://youtu.be/abcdefghijk','https://www.youtube.com/shorts/abcdefghijk','https://www.youtube.com/watch?v=abcdefghijk&list=123']:
   self.assertEqual(canonical_url(u),'https://www.youtube.com/watch?v=abcdefghijk')
 def test_reject_urls(self):
  for u in ['http://youtube.com/watch?v=abcdefghijk','https://youtube.com.evil.com/watch?v=abcdefghijk','https://www.youtube.com/playlist?list=123','https://user@youtube.com/watch?v=abcdefghijk','file:///tmp/a']:
   with self.assertRaises(ValueError):canonical_url(u)
 def test_guard(self):
  for x in [{'age_limit':18},{'is_live':True},{'has_drm':True}]:
   with self.assertRaises(ValueError):guard(x)
 def test_formats(self):
  data={'formats':[{'format_id':'137','height':1080,'vcodec':'avc1','ext':'mp4','fps':30},{'format_id':'140','vcodec':'none'},{'format_id':'x','height':2160,'vcodec':'av1','has_drm':True}]}
  self.assertEqual([f['id'] for f in formats(data)],['137'])
if __name__=='__main__':unittest.main()
