"""Minimal, fail-closed patches for pinned MAZANOKE source (GPL-3.0)."""
from pathlib import Path

ORIGINAL_WORKER = 'libURL: `${location.origin}/assets/vendor/browser-image-compression.js`,'
RELATIVE_WORKER = 'libURL: new URL("./assets/vendor/browser-image-compression.js", location.href).href,'
ORIGINAL_BAD_FILE = 'ui.progress.text.innerHTML = `Unsupported file "<div class=\'progress-file-name\'>${file.name}</div>"`;'
SAFE_BAD_FILE = 'ui.progress.text.textContent = `Unsupported file "${file.name}"`;'
ORIGINAL_PROGRESS = 'ui.progress.text.innerHTML = `Optimizing "<div class=\'progress-file-name\'>${fileName}</div>"`;'
SAFE_PROGRESS = 'ui.progress.text.textContent = `Optimizing "${fileName}"`;'
ESCAPE_CODE = """  // Never interpolate user-supplied image filenames as raw HTML.
  const escapeHTML = value => value.replace(/[&<>"']/g, ch =>
    ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[ch]));
"""


def replace_exact_once(content: str, needle: str, replacement: str, feature: str) -> str:
    count = content.count(needle)
    if count != 1:
        raise RuntimeError(f'{feature}: expected exactly one occurrence, got {count}')
    return content.replace(needle, replacement, 1)


def harden_distribution(root: Path) -> None:
    """Fix subpath worker URL and prevent stored filename HTML injection."""
    path = root / 'assets/js/compression.js'
    text = path.read_text(encoding='utf-8')
    text = replace_exact_once(text, ORIGINAL_WORKER, RELATIVE_WORKER, 'compression worker URL')
    text = replace_exact_once(text, ORIGINAL_BAD_FILE, SAFE_BAD_FILE, 'invalid filename')
    text = replace_exact_once(text, ORIGINAL_PROGRESS, SAFE_PROGRESS, 'progress filename')
    path.write_text(text, encoding='utf-8')

    helpers_path = root / 'assets/js/helpers.js'
    helpers = helpers_path.read_text(encoding='utf-8')
    helpers = replace_exact_once(helpers, '  // Create the output dom for compressed images.',
        ESCAPE_CODE + '  // Create the output dom for compressed images.', 'output filename escaping marker')
    helpers = replace_exact_once(helpers, '${outputFileNameText.slice(0, -8)}',
        '${escapeHTML(outputFileNameText.slice(0, -8))}', 'filename prefix')
    helpers = replace_exact_once(helpers, '${outputFileNameText.slice(-8)}',
        '${escapeHTML(outputFileNameText.slice(-8))}', 'filename suffix')
    helpers = replace_exact_once(helpers, 'download="${outputFileNameText}"',
        'download="${escapeHTML(outputFileNameText)}"', 'download attribute')
    helpers_path.write_text(helpers, encoding='utf-8')

    css = root / 'freephoto-theme.css'
    css.write_text(css.read_text(encoding='utf-8') +
        '\n:focus-visible { outline: 3px solid #277455 !important; outline-offset: 3px; }\n', encoding='utf-8')
