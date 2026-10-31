import pathlib,sys,tempfile,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from cycle3_patch import patch_zip_notice

class NoticeTest(unittest.TestCase):
    def test_accessible_warning_and_safe_text(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            (root/'assets/js').mkdir(parents=True)
            (root/'freephoto-theme.css').write_text('')
            (root/'assets/js/download.js').write_text("""async function downloadAllImages() {
    state.isDownloadingAll = true;
    const validBlobs = blobs.filter((blob) => blob !== null);
  } catch (error) {
    console.error("Download all images as zip failed:", error);
}""")
            patch_zip_notice(root)
            s=(root/'assets/js/download.js').read_text()
            for needle in ('aria-live', 'role', 'const skipped', '跳过 ', 'ZIP 下载失败','notice.textContent'):
                self.assertIn(needle, s)
            self.assertNotIn('innerHTML',s)
    def test_unexpected_upstream_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td);(root/'assets/js').mkdir(parents=True)
            (root/'assets/js/download.js').write_text('bad')
            (root/'freephoto-theme.css').write_text('')
            with self.assertRaises(RuntimeError):patch_zip_notice(root)
