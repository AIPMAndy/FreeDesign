"""Cycle 3: visible and accessible ZIP export integrity warnings."""
from pathlib import Path
from hardening import replace_exact_once

NOTICE_JS = """// Make partial and total ZIP failures visible instead of console-only.
function freephotoZipNotice(message) {
  let notice = document.getElementById('freephoto-zip-warning');
  if (!message) {
    if (notice) notice.remove();
    return;
  }
  if (!notice) {
    notice = document.createElement('p');
    notice.id = 'freephoto-zip-warning';
    notice.setAttribute('role', 'status');
    notice.setAttribute('aria-live', 'polite');
    notice.className = 'freephoto-zip-warning';
    ui.actions.downloadAll.insertAdjacentElement('afterend', notice);
  }
  notice.textContent = message;
}

"""

def patch_zip_notice(root: Path) -> None:
    path = root / 'assets/js/download.js'
    script = path.read_text(encoding='utf-8')
    script = replace_exact_once(script, 'async function downloadAllImages() {',
        NOTICE_JS + 'async function downloadAllImages() {', 'ZIP status helper')
    script = replace_exact_once(script, '    state.isDownloadingAll = true;',
        '    state.isDownloadingAll = true;\n    freephotoZipNotice("");', 'clear stale status')
    script = replace_exact_once(script, '    const validBlobs = blobs.filter((blob) => blob !== null);',
        '    const validBlobs = blobs.filter((blob) => blob !== null);\n    const skipped = compressedImages.length - validBlobs.length;',
        'count skipped images')
    script = replace_exact_once(script,
        '  } catch (error) {\n    console.error("Download all images as zip failed:", error);',
        """    if (skipped > 0) {
      freephotoZipNotice('已下载 ' + validBlobs.length + ' 张图片，跳过 ' + skipped + ' 张失败图片。请单独重试失败项目。');
    }
  } catch (error) {
    freephotoZipNotice('ZIP 下载失败，请检查图片并重试。');
    console.error("Download all images as zip failed:", error);""",
        'warn partial/total failures')
    path.write_text(script, encoding='utf-8')
    theme = root / 'freephoto-theme.css'
    theme.write_text(theme.read_text(encoding='utf-8') +
        '\n.freephoto-zip-warning{display:block;color:#8b451d;background:#fff3dd;border:1px solid #dfb37f;border-radius:12px;padding:12px 14px;line-height:1.5;font-size:14px;margin-top:10px}\n',
        encoding='utf-8')
