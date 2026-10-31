"""Fail-closed patch: ZIP entries must keep the same file metadata after failed fetches."""
from pathlib import Path
from hardening import replace_exact_once

def patch_zip_download(root: Path) -> None:
    path = root / 'assets/js/download.js'
    s = path.read_text(encoding='utf-8')
    s = replace_exact_once(s, 'return await response.blob();',
        'return { blob: await response.blob(), fileName: link.download, fileSize: Number(link.dataset.filesize) };',
        'keep ZIP blob metadata together')
    s = replace_exact_once(s, 'const fileSize = parseInt(compressedImages[i].dataset.filesize, 10);',
        'const { blob, fileName: originalName, fileSize } = validBlobs[i];', 'ZIP metadata index')
    s = replace_exact_once(s, '      const originalName = compressedImages[i].download;\n', '', 'remove stale index')
    s = replace_exact_once(s, 'currentZip.file(fileName, validBlobs[i]);',
        'currentZip.file(fileName, blob);', 'ZIP correct blob')
    path.write_text(s, encoding='utf-8')
