#!/usr/bin/env python3
"""Synthetic browser verification; not a substitute for native Safari or 20MP camera images."""
from io import BytesIO
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from realworld_browser import website, bytes_from_link as result_bytes, ART as ARTIFACTS
from urllib.parse import urlsplit

def no_external_requests(page):
    outside=[]
    def audit(request):
        u=urlsplit(request.url)
        if u.scheme in ('blob', 'data'): return
        if u.hostname!='127.0.0.1' or request.method not in ('GET','HEAD'):
            outside.append({'method':request.method,'url':request.url})
    page.on('request',audit)
    return outside
import json, time

def fixtures(folder):
    paths=[]
    for i in range(30):
        im=Image.new('RGB',(240,160),((i*37)%255,(i*71)%255,(i*113)%255))
        path=folder/f'batch-{i:02d}.jpg'; im.save(path,'JPEG',quality=90);paths.append(path)
    from pillow_heif import register_heif_opener
    register_heif_opener()
    heic=folder/'synthetic-iphone.heic'
    Image.new('RGB',(64,48),(25,130,195)).save(heic,format='HEIF',quality=85)
    return paths,heic

def urls(page):
    return page.evaluate('''() => [...document.querySelectorAll(".image-output__item")].flatMap(card =>
    [...card.querySelectorAll('a[href^="blob:"],img[src^="blob:"]')].map(el => el.tagName === 'A' ? el.href : el.src))''')

def check_batch(page,url,paths):
    page.add_init_script('''(() => {
      const previous=URL.revokeObjectURL.bind(URL); window.__fpRevoked=[];
      URL.revokeObjectURL=function(url){window.__fpRevoked.push(url);return previous(url);};
    })();''')
    page.goto(url,wait_until='domcontentloaded')
    started=time.perf_counter()
    page.locator('#compress').set_input_files([str(p) for p in paths])
    page.wait_for_function('document.querySelectorAll(".image-output__item-download-button").length === 30',timeout=180000)
    elapsed=round((time.perf_counter()-started)*1000,1)
    first=page.locator('.image-output__item-download-button').first
    with Image.open(BytesIO(result_bytes(first))) as im:
        im.load();assert im.size==(240,160),im.size
    known=set(urls(page))
    assert len(known)>=60, f'Expected output and thumbnail URLs, found {len(known)}'
    page.locator('.image-output__item-delete-button').first.click()
    page.wait_for_function('document.querySelectorAll(".image-output__item").length === 29',timeout=15000)
    first_revoked=set(page.evaluate('window.__fpRevoked'))
    assert len(first_revoked.intersection(known))>=2, 'Deleted card URLs were not revoked'
    page.evaluate('deleteAllImages()')
    page.wait_for_function('document.querySelectorAll(".image-output__item").length === 0',timeout=15000)
    revoked=set(page.evaluate('window.__fpRevoked'))
    leaked=known-revoked
    assert not leaked, f'{len(leaked)} result object URLs retained after clear'
    return {'images':30,'processing_wall_ms':elapsed,'output_blob_urls':len(known),
            'released_output_blob_urls':len(known.intersection(revoked)),
            'retained_output_blob_urls':len(leaked),
            'warning':'Object URL count is NOT actual browser peak memory.'}

def check_heic(page,url,path):
    page.goto(url,wait_until='domcontentloaded')
    page.evaluate("setConvertMethod('image/png')")
    page.locator('#compress').set_input_files(str(path))
    link=page.locator('.image-output__item-download-button').first
    link.wait_for(timeout=120000)
    out=result_bytes(link)
    with Image.open(BytesIO(out)) as im:
        im.load()
        assert im.format=='PNG' and im.size==(64,48),(im.format,im.size)
        rgb=im.convert('RGB').getpixel((32,24))
        assert all(abs(a-b)<35 for a,b in zip(rgb,(25,130,195))),rgb
    return {'input':'synthetic 8-bit HEIC 64x48','output':'PNG 64x48','bytes':len(out),
            'warning':'Chromium/WASM decode does NOT verify native iOS Safari.'}

def main():
    output={'suite':'FreePhoto cycle 4','environment':'GitHub Actions Linux Chromium',
            'status':'IN_PROGRESS','cases':[]}
    try:
        with website() as (folder,url):
            paths,heic=fixtures(folder)
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True)
                try:
                    for name,fn in [('30-jpeg-batch',lambda page:check_batch(page,url,paths)),
                                    ('heic-to-png',lambda page:check_heic(page,url,heic))]:
                        context=browser.new_context(accept_downloads=True,service_workers='block')
                        page=context.new_page(); page.set_default_timeout(120000)
                        outbound=no_external_requests(page)
                        try:
                            detail=fn(page)
                            assert not outbound,f'External request detected: {outbound}'
                            output['cases'].append({'case':name,'status':'PASS',**detail})
                            page.screenshot(path=str(ARTIFACTS/f'cycle4-{name}.png'),full_page=True)
                        finally:context.close()
                finally:browser.close()
        output['status']='PASS'
    except Exception as e:
        output['status']='FAIL';output['failure']=repr(e)
        raise
    finally:
        (ARTIFACTS/'cycle4-results.json').write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
        print(json.dumps(output,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
