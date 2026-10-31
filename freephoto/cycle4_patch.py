"""Cycle 4: revoke only generated output Blob URLs on result deletion."""
from pathlib import Path
from hardening import replace_exact_once

HELPER = '''// Release result image and thumbnail buffers when output cards are deleted.
function freephotoRevokeOutputURLs(root) {
  if (!root) return;
  const urls = new Set();
  root.querySelectorAll('a[href^="blob:"], img[src^="blob:"]').forEach(el => {
    const value = el.tagName === 'A' ? el.getAttribute('href') : el.getAttribute('src');
    if (value && value.startsWith('blob:')) urls.add(value);
  });
  urls.forEach(url => URL.revokeObjectURL(url));
}

'''

def patch_object_url_cleanup(root: Path) -> None:
    path = root/'assets/js/download.js'
    script = path.read_text(encoding='utf-8')
    script = replace_exact_once(script,
        'async function deleteImage(elementId) {',
        HELPER + 'async function deleteImage(elementId) {',
        'URL cleanup helper')
    script = replace_exact_once(script,
        '''    image.addEventListener("animationend", () => {  
      image.remove();''',
        '''    image.addEventListener("animationend", () => {  
      freephotoRevokeOutputURLs(image);
      image.remove();''',
        'single-card cleanup')
    script = replace_exact_once(script,
        '''    ui.output.content.addEventListener("animationend", () => {
      ui.output.content.innerHTML = "";''',
        '''    ui.output.content.addEventListener("animationend", () => {
      freephotoRevokeOutputURLs(ui.output.content);
      ui.output.content.innerHTML = "";''',
        'clear-all cleanup')
    path.write_text(script, encoding='utf-8')
