import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from cycle4_patch import patch_object_url_cleanup

class URLCleanup(unittest.TestCase):
    def test_single_and_all_cleanup(self):
        src='''async function deleteImage(elementId) {
    image.addEventListener("animationend", () => {  
      image.remove();
}
async function deleteAllImages() {
    ui.output.content.addEventListener("animationend", () => {
      ui.output.content.innerHTML = "";
}
'''
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td); (p/'assets/js').mkdir(parents=True)
            f=p/'assets/js/download.js'; f.write_text(src)
            patch_object_url_cleanup(p)
            actual=f.read_text()
            self.assertEqual(actual.count('freephotoRevokeOutputURLs(image);'),1)
            self.assertEqual(actual.count('freephotoRevokeOutputURLs(ui.output.content);'),1)
            self.assertIn("const urls = new Set()",actual)
            self.assertIn("URL.revokeObjectURL(url)", actual)
            self.assertNotIn("URL.revokeObjectURL(link.href)",actual)

    def test_unrecognized_upstream_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td); (p/'assets/js').mkdir(parents=True)
            f=p/'assets/js/download.js';f.write_text('unrecognized upstream')
            with self.assertRaises(RuntimeError):patch_object_url_cleanup(p)
            self.assertEqual(f.read_text(),'unrecognized upstream')
