#!/usr/bin/env python3
"""Real Chromium browser smoke test for built FreePhoto; requires playwright and Pillow."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import tempfile
import threading
import time
from PIL import Image, PngImagePlugin
from playwright.sync_api import sync_playwright

PROJECT = Path(__file__).resolve().parents[1]
OUT = PROJECT / 'artifacts'
OUT.mkdir(exist_ok=True)


def run():
    source = PROJECT/'dist'
    assert (source/'assets/js/compression.js').exists(), 'Build real upstream first'
    with tempfile.TemporaryDirectory() as work:
        root = Path(work)
        shutil.copytree(source, root/'nested')
        marker = 'FREEPHOTO_PRIVATE_LOCATION_987654'
        img = Image.new('RGB', (600, 400), color=(45, 116, 87))
        meta = PngImagePlugin.PngInfo()
        meta.add_text('Description', marker)
        fixture = root/'fixture.png'
        img.save(fixture, pnginfo=meta)
        handler = partial(SimpleHTTPRequestHandler, directory=str(root))
        server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        uri = f'http://127.0.0.1:{server.server_port}/nested/'
        results = {'url': '/nested/', 'cases': []}
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                for device in ['desktop', 'mobile']:
                    ctx = browser.new_context(viewport={'width': 1280 if device == 'desktop' else 390,
                                                        'height': 820 if device == 'desktop' else 844})
                    page = ctx.new_page()
                    missing = []
                    page.on('response', lambda r: missing.append(r.url) if r.status >= 400 and '/assets/' in r.url else None)
                    page.goto(uri, wait_until='domcontentloaded')
                    page.locator('#compress').set_input_files(str(fixture))
                    link = page.locator('.image-output__item-download-button').first
                    start = time.perf_counter()
                    link.wait_for(timeout=45000)
                    elapsed_ms = round((time.perf_counter() - start)*1000, 1)
                    metadata = link.evaluate('''async a => {
                        const response = await fetch(a.href);
                        const bytes = new Uint8Array(await response.arrayBuffer());
                        const content = new TextDecoder('latin1').decode(bytes);
                        return {size:bytes.length, containsSensitiveMarker:content.includes('FREEPHOTO_PRIVATE_LOCATION_987654'),
                                filename:a.getAttribute('download')};
                    }''')
                    assert metadata['size'] > 0, 'Output image is empty'
                    assert not metadata['containsSensitiveMarker'], 'Metadata leaked into output'
                    assert not missing, f'Broken vendor requests on {device}: {missing}'

                    # Independent DOM sink probe: malicious file names must not create HTML.
                    probe = page.evaluate("""() => {
                      const name = '<img data-xss-probe src=x onerror=window.__freephoto_xss=1>.png';
                      const html = buildOutputItemHTML({
                        outputImageBlob:'blob:local-test',thumbnailDataURL:'blob:local-test',
                        outputFileNameText:name,outputFileExtension:'png',
                        width:1,height:1,fileSize:8,fileSizeSavedTrend:'-',
                        fileSizeSavedPercentage:0,fileSizeSavedClass:'badge--success'
                      });
                      const div=document.createElement('div');
                      div.innerHTML=html;
                      return {unsafe:!!div.querySelector('[data-xss-probe]'),
                              actualName:div.querySelector('a[download]')?.getAttribute('download')};
                    }""")
                    assert not probe['unsafe'], f'Untrusted filename created an element: {probe}'
                    assert '<img data-xss-probe' in probe['actualName'], 'Output filename changed'
                    page.screenshot(path=str(OUT/f'smoke-{device}.png'), full_page=True)
                    results['cases'].append({'device':device,'status':'PASS','elapsed_ms':elapsed_ms,
                        'output_bytes':metadata['size'], 'missing_assets':missing})
                    ctx.close()
                browser.close()
        finally:
            server.shutdown()
        (OUT/'smoke-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2), encoding='utf-8')
        print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__ == '__main__': run()
