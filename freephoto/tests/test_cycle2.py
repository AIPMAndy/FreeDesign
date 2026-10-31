import pathlib, sys, tempfile, unittest
BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from build import build
from cycle2_patch import patch_zip_download

class ZipIntegrity(unittest.TestCase):
    def test_partial_failure_keeps_metadata_together(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            (root/'assets/js').mkdir(parents=True)
            (root/'assets/js/download.js').write_text("""return await response.blob();
const fileSize = parseInt(compressedImages[i].dataset.filesize, 10);
      const originalName = compressedImages[i].download;
currentZip.file(fileName, validBlobs[i]);""")
            patch_zip_download(root)
            out=(root/'assets/js/download.js').read_text()
            self.assertIn('fileName: link.download',out)
            self.assertIn('fileName: originalName, fileSize } = validBlobs[i]',out)
            self.assertIn('currentZip.file(fileName, blob)',out)
            self.assertNotIn('compressedImages[i].download',out)
    def test_patch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            (root/'assets/js').mkdir(parents=True)
            (root/'assets/js/download.js').write_text('unexpected upstream')
            with self.assertRaisesRegex(RuntimeError,'expected exactly one'):patch_zip_download(root)
    def test_existing_output_rejected_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            upstream=root/'upstream';upstream.mkdir()
            dest=root/'dist';dest.mkdir()
            marker=dest/'keep.txt';marker.write_text('important')
            with self.assertRaisesRegex(RuntimeError,'destination exists'):build(dest,upstream)
            self.assertEqual(marker.read_text(),'important')
    def test_overlapping_paths_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            upstream=pathlib.Path(td)/'upstream';upstream.mkdir()
            with self.assertRaisesRegex(RuntimeError,'overlap'):build(upstream/'dist',upstream)
