import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import build

class PatchTest(unittest.TestCase):
    def test_patch_site(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)
            (p/'assets/js').mkdir(parents=True)
            (p/'assets/js/global.js').write_text('libURL: `${location.origin}/assets/vendor/browser-image-compression.js`,',encoding='utf8')
            from hardening import ORIGINAL_WORKER, ORIGINAL_BAD_FILE, ORIGINAL_PROGRESS
            (p/'assets/js/compression.js').write_text('\n'.join((ORIGINAL_WORKER, ORIGINAL_BAD_FILE, ORIGINAL_PROGRESS)), encoding='utf8')
            (p/'assets/js/helpers.js').write_text('  // Create the output dom for compressed images.\n${outputFileNameText.slice(0, -8)}\n${outputFileNameText.slice(-8)}\ndownload=\"${outputFileNameText}\"', encoding='utf8')
            (p/'assets/js/download.js').write_text('return await response.blob();\\nconst fileSize = parseInt(compressedImages[i].dataset.filesize, 10);\\n      const originalName = compressedImages[i].download;\\ncurrentZip.file(fileName, validBlobs[i]);',encoding='utf8')
            (p/'index.html').write_text('''<html lang="en"><head><title>MAZANOKE | Online Image Optimizer That Runs Privately in Your Browser</title>
            <meta name="description" content="Optimize images locally and privately by converting and compressing them offline in your browser. Supports JPG, PNG, WebP, HEIC, AVIF, GIF, SVG." />
            <meta name="robots" content="noindex, nofollow" />
            <link rel="stylesheet" type="text/css" href="./assets/css/style.css" />
            <link rel="manifest" href="/manifest.json" />
            <meta name="theme-color" content="#191919" />
            <script>localStorage.getItem("theme") || "theme-dark"</script>
            </head><body><h1 class="logo-text">MAZANOKE</h1>
            <span>created by civilblur</span><span>Install MAZANOKE</span>
            <script src="browser-image-compression.js"></script>
            <script type="text/javascript" src="./assets/js/events.js"></script>
            <script>navigator.serviceWorker.register("/service-worker.js")</script></body></html>''',encoding='utf8')
            (p/'manifest.json').write_text(json.dumps({'name':'MAZANOKE','icons':[{'src':'/assets/images/android-chrome-192x192.png'}]}),encoding='utf8')
            (p/'service-worker.js').write_text('''const APP_VERSION = "v1.1.7";
            const CACHE_NAME = `mazanoke-cache-${APP_VERSION}`;
            const urlsToCache = ["/", "/index.html", "/assets/js/events.js"];
            ''',encoding='utf8')
            build.patch_site(p)
            html=(p/'index.html').read_text()
            self.assertIn('FreePhoto',html)
            self.assertIn('lang="zh-CN"',html)
            self.assertIn('freephoto-theme.css',html)
            self.assertIn('freephoto-i18n.js',html)
            self.assertIn('register("./service-worker.js")',html)
            sw=(p/'service-worker.js').read_text()
            self.assertIn('"./index.html"',sw)
            self.assertIn('freephoto-i18n.js',sw)
            globaljs=(p/'assets/js/global.js').read_text()
            self.assertIn('new URL(',globaljs)
            self.assertNotIn('`${location.origin}',globaljs)
            self.assertEqual(json.loads((p/'manifest.json').read_text())['start_url'],'./')
            self.assertTrue((p/'FORK-NOTICE.md').exists())

if __name__=='__main__': unittest.main()
