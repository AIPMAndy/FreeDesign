"""Static landing integrity tests for a built FreePhoto site."""
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from marketing import HERO, DETAILS

class WebsiteTests(unittest.TestCase):
    def test_semantic_sections_and_accessible_links(self):
        self.assertIn('id="fp-heading"',HERO)
        self.assertIn('href="#tool"',HERO)
        self.assertIn('rel="noopener noreferrer"',HERO)
        self.assertIn('id="privacy"',DETAILS)
        self.assertIn('id="faq-heading"',DETAILS)
        self.assertIn('MAZANOKE',DETAILS)
    def test_expected_static_assets(self):
        base=Path(__file__).resolve().parents[1]
        css=(base/"freephoto-site.css").read_text(encoding="utf-8")
        self.assertIn("@media(max-width:560px)",css)
        self.assertIn(".fp-hero",css)
        self.assertIn(".fp-faq",css)
    def test_landing_build_after_upstream(self):
        from marketing import enhance_website
        import json
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"index.html").write_text('<html><head><link rel="stylesheet" href="./freephoto-theme.css" /></head><body>    <div class="content">upstream tool</div>    <footer>original</footer></body></html>',encoding="utf-8")
            (root/"manifest.json").write_text(json.dumps({"icons":[]}),encoding="utf-8")
            (root/"service-worker.js").write_text('const urlsToCache = ["./freephoto-theme.css",];',encoding="utf-8")
            enhance_website(root)
            text=(root/"index.html").read_text(encoding="utf-8")
            for marker in ('id="fp-heading"','id="tool"','id="privacy"','id="faq-heading"','upstream tool'):
                self.assertIn(marker,text)
            self.assertTrue((root/"freephoto-mark.svg").is_file())
            self.assertTrue((root/"freephoto-site.css").is_file())
            self.assertTrue((root/".nojekyll").exists())
            self.assertIn("freephoto-mark.svg",(root/"manifest.json").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
