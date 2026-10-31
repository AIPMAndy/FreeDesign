import pathlib
import sys
import tempfile
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from hardening import harden_distribution, replace_exact_once, ORIGINAL_WORKER, RELATIVE_WORKER, ORIGINAL_BAD_FILE, ORIGINAL_PROGRESS


class HardeningTest(unittest.TestCase):
    def test_pinned_upstream_snippets_are_safely_replaced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root/'assets/js').mkdir(parents=True)
            original = '\n'.join((ORIGINAL_WORKER, ORIGINAL_BAD_FILE, ORIGINAL_PROGRESS))
            (root/'assets/js/compression.js').write_text(original, encoding='utf-8')
            (root/'assets/js/helpers.js').write_text('  // Create the output dom for compressed images.\n${outputFileNameText.slice(0, -8)}\n${outputFileNameText.slice(-8)}\ndownload=\"${outputFileNameText}\"', encoding='utf-8')
            (root/'freephoto-theme.css').write_text('.theme-light {}', encoding='utf-8')
            harden_distribution(root)
            updated = (root/'assets/js/compression.js').read_text(encoding='utf-8')
            self.assertIn(RELATIVE_WORKER, updated)
            self.assertNotIn('file.name}</div>', updated)
            self.assertNotIn('fileName}</div>', updated)
            self.assertEqual(updated.count('textContent'), 2)
            self.assertIn('escapeHTML(outputFileNameText)', (root/'assets/js/helpers.js').read_text(encoding='utf-8'))
            self.assertIn(':focus-visible', (root/'freephoto-theme.css').read_text(encoding='utf-8'))

    def test_upstream_drift_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'expected exactly one'):
            replace_exact_once('unrelated', 'missing', 'replacement', 'worker')
        with self.assertRaisesRegex(RuntimeError, 'expected exactly one'):
            replace_exact_once('aa', 'a', 'b', 'duplicate')

    def test_injection_payload_is_never_inserted_as_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root/'assets/js').mkdir(parents=True)
            (root/'assets/js/compression.js').write_text('\n'.join((ORIGINAL_WORKER, ORIGINAL_BAD_FILE, ORIGINAL_PROGRESS)),encoding='utf-8')
            (root/'assets/js/helpers.js').write_text('  // Create the output dom for compressed images.\n${outputFileNameText.slice(0, -8)}\n${outputFileNameText.slice(-8)}\ndownload=\"${outputFileNameText}\"',encoding='utf-8')
            (root/'freephoto-theme.css').write_text('',encoding='utf-8')
            harden_distribution(root)
            result=(root/'assets/js/compression.js').read_text(encoding='utf-8')
            self.assertNotIn('innerHTML = `Unsupported file', result)
            self.assertNotIn('innerHTML = `Optimizing', result)


if __name__ == '__main__':
    unittest.main()
