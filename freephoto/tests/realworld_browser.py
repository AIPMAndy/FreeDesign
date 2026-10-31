#!/usr/bin/env python3
"""Cycle 2 Chromium integration test. Synthetic fixtures; genuine iOS Safari NOT tested."""
from pathlib import Path
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from zipfile import ZipFile
from urllib.parse import urlsplit
from PIL import Image, PngImagePlugin
from playwright.sync_api import sync_playwright
import tempfile, shutil, threading, base64, json, time

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts'
ART.mkdir(exist_ok=True)
MARK='PRIVATE_FREEPHOTO_METADATA_MARKER_9876'

@contextmanager
def website():
    with tempfile.TemporaryDirectory() as td:
        folder=Path(td)
        assert (ROOT/'dist/assets/vendor/jszip.js').is_file(), 'Build the real vendor distribution first'
        shutil.copytree(ROOT/'dist',folder/'nested')
        s=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(folder)))
        threading.Thread(target=s.serve_forever,daemon=True).start()
        try:yield folder,f'http://127.0.0.1:{s.server_port}/nested/'
        finally:s.shutdown();s.server_close()

def fixtures(folder):
    im=Image.new('RGB',(800,520),(25,107,90))
    meta=Image.Exif();meta[270]=MARK
    jpg=folder/'secret-photo.jpg';im.save(jpg,'JPEG',exif=meta)
    pmeta=PngImagePlugin.PngInfo();pmeta.add_text('Description',MARK)
    green=folder/'a-green.png';im.save(green,'PNG',pnginfo=pmeta)
    red=folder/'b-red.png';Image.new('RGB',(420,350),(204,83,66)).save(red)
    blue=folder/'c-blue.png';Image.new('RGB',(260,180),(65,94,201)).save(blue)
    return jpg,green,red,blue

def bytes_from_link(link):
    encoded=link.evaluate("""async a => {
       const resp=await fetch(a.href); const data=new Uint8Array(await resp.arrayBuffer());
       let s='';for(let i=0;i<data.length;i+=8192)s+=String.fromCharCode(...data.slice(i,i+8192));
       return btoa(s);
    }""")
    return base64.b64decode(encoded)

def validate(data,fmt,size):
    with Image.open(BytesIO(data)) as im:
        im.load()
        assert im.format==fmt,(im.format,fmt)
        assert im.size==size,(im.size,size)
        assert MARK not in str(im.info)
        assert MARK not in str(im.getexif())
    assert MARK.encode() not in data,'Metadata marker retained'

def format_test(page,url,jpg,green):
    page.goto(url,wait_until='domcontentloaded')
    page.evaluate("setConvertMethod('image/webp')")
    page.locator('#compress').set_input_files(str(jpg))
    output=page.locator('.image-output__item-download-button').first
    output.wait_for(timeout=60000)
    assert output.get_attribute('download').endswith('.webp')
    validate(bytes_from_link(output),'WEBP',(800,520))
    # The output link is rendered before the compression queue fully resets.
    # Wait for the actual app ready state or a second selection is deliberately ignored.
    page.wait_for_function('window.app && !window.app.state.isCompressing',timeout=15000)
    page.evaluate("setConvertMethod('default')")
    page.locator('#compress').set_input_files(str(green))
    page.wait_for_function("document.querySelectorAll('.image-output__item-download-button').length===2",timeout=60000)
    validate(bytes_from_link(page.locator('.image-output__item-download-button').first),'PNG',(800,520))
    return {'case':'JPEG->WebP and PNG metadata removal'}

def zip_test(page,url,images):
    page.goto(url,wait_until='domcontentloaded')
    page.locator('#compress').set_input_files([str(p) for p in images])
    page.wait_for_function("document.querySelectorAll('.image-output__item-download-button').length===3",timeout=90000)
    links=page.locator('.image-output__item-download-button')
    entries=[(links.nth(i).get_attribute('download'),links.nth(i).get_attribute('href')) for i in range(3)]
    missing=entries[1]
    page.evaluate("(href) => URL.revokeObjectURL(href)",missing[1])
    with page.expect_download(timeout=45000) as event:
        page.locator('#downloadAllImagesButton').click()
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'out.zip';event.value.save_as(str(out))
        with ZipFile(out) as z:
            names=set(z.namelist())
            expected={n for n,h in entries if n!=missing[0]}
            assert names==expected,(names,expected)
            for name in names:
                with Image.open(BytesIO(z.read(name))) as im:
                    im.load();r,g,b=im.convert('RGB').getpixel((1,1))
                if 'green' in name: assert g>r,(name,r,g,b)
                elif 'red' in name: assert r>g,(name,r,g,b)
                elif 'blue' in name: assert b>r,(name,r,g,b)
                else: raise AssertionError('Unexpected output filename '+name)
    return {'case':'Partial ZIP failure preserves identities','zip_members':sorted(names)}

def main():
    results={'suite':'FreePhoto cycle 2 real browser','cases':[]}
    with website() as (folder,url):
        jpg,green,red,blue=fixtures(folder)
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for label,fn in [('formats',lambda pg:format_test(pg,url,jpg,green)),
                                 ('zip',lambda pg:zip_test(pg,url,[green,red,blue]))]:
                    ctx=browser.new_context(accept_downloads=True,service_workers='block')
                    page=ctx.new_page();external=[]
                    def audit(req):
                        u=urlsplit(req.url)
                        if u.scheme in ('data','blob'):return
                        if u.hostname!='127.0.0.1' or req.method not in ('GET','HEAD'):
                            external.append({'method':req.method,'url':req.url})
                    page.on('request',audit)
                    started=time.perf_counter()
                    try:
                        result=fn(page)
                        assert not external, f'External network request: {external}'
                        results['cases'].append({'name':label,'status':'PASS','elapsed_ms':round((time.perf_counter()-started)*1000,1),**result})
                        page.screenshot(path=str(ART/f'cycle2-{label}.png'),full_page=True)
                    finally:ctx.close()
            finally:browser.close()
    (ART/'cycle2-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(json.dumps(results,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
