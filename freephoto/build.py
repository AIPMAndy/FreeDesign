#!/usr/bin/env python3
"""Reproducible FreePhoto derivative of MAZANOKE (GPL-3.0).

Fetches pinned upstream source, preserves the original engine and notices,
adds FreePhoto Chinese localization/visual style and nested-path-safe PWA paths.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
from hardening import harden_distribution
from cycle2_patch import patch_zip_download

UPSTREAM = 'https://github.com/civilblur/mazanoke.git'
UPSTREAM_COMMIT = 'ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b'
BASE = Path(__file__).resolve().parent

def patch_site(target: Path) -> None:
    index = target / 'index.html'
    if not index.exists():
        raise RuntimeError('Upstream source missing index.html')
    html = index.read_text(encoding='utf-8')
    if 'MAZANOKE' not in html or 'browser-image-compression.js' not in html:
        raise RuntimeError('Upstream structure changed: review fork patch before continuing.')
    html = html.replace('lang="en"','lang="zh-CN"',1)
    html = html.replace('MAZANOKE | Online Image Optimizer That Runs Privately in Your Browser', 'FreePhoto｜免费、本地、开源的图片工具箱')
    html = html.replace('Optimize images locally and privately by converting and compressing them offline in your browser. Supports JPG, PNG, WebP, HEIC, AVIF, GIF, SVG.', '免费压缩、调整图片尺寸、转换格式、清理照片元数据。图片在浏览器本地处理，不上传服务器。')
    html = html.replace('<meta name="robots" content="noindex, nofollow" />', '<meta name="robots" content="index, follow" />')
    html = html.replace('localStorage.getItem("theme") || "theme-dark"', 'localStorage.getItem("theme") || "theme-light"')
    html = html.replace('<h1 class="logo-text">MAZANOKE</h1>', '<h1 class="logo-text">FreePhoto<span class="freephoto-dot">.</span></h1>')
    html = html.replace('alt="MAZANOKE logo"', 'alt="FreePhoto"')
    html = html.replace('href="/manifest.json"','href="./manifest.json"')
    html = html.replace('navigator.serviceWorker.register("/service-worker.js")', 'navigator.serviceWorker.register("./service-worker.js")')
    html = html.replace('<meta name="theme-color" content="#191919" />', '<meta name="theme-color" content="#F7F8F3" />')
    marker = '<link rel="stylesheet" type="text/css" href="./assets/css/style.css" />'
    if marker not in html:
        raise RuntimeError('Cannot find upstream CSS link')
    html = html.replace(marker, marker + '\n    <link rel="stylesheet" href="./freephoto-theme.css" />', 1)
    scripts = '<script type="text/javascript" src="./assets/js/events.js"></script>'
    if scripts not in html:
        raise RuntimeError('Cannot find upstream events script')
    html = html.replace(scripts, scripts + '\n    <script defer src="./freephoto-i18n.js"></script>', 1)
    html = html.replace('<span>created by civilblur</span>', '<span>原始引擎 MAZANOKE © civilblur · FreePhoto 改造版</span>')
    html = html.replace('Install MAZANOKE', '安装 FreePhoto')
    index.write_text(html, encoding='utf-8')

    manifest_path = target/'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update(name='FreePhoto · 私密图片工具', short_name='FreePhoto', description='免费、本地、开源的图片处理工具',start_url='./',background_color='#F7F8F3',theme_color='#F7F8F3')
    for icon in manifest.get('icons', []):
        icon['src'] = icon['src'].lstrip('/')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    sw_path = target/'service-worker.js'
    if sw_path.exists():
        sw = sw_path.read_text(encoding='utf-8')
        # Base-path-safe PWA assets and versioned cache for FreePhoto release.
        sw = sw.replace('const APP_VERSION = "v1.1.7";', 'const APP_VERSION = "freephoto-0.1.0";')
        sw = sw.replace('mazanoke-cache-', 'freephoto-cache-')
        sw = sw.replace('"/",', '"./",')
        sw = re.sub(r'(?<=")/(?!/)(?=[^"\n]+")', './', sw)
        sw = sw.replace('"./index.html",', '"./index.html",\n  "./freephoto-theme.css",\n  "./freephoto-i18n.js",')
        sw_path.write_text(sw, encoding='utf-8')
    global_js = target/'assets/js/global.js'
    if global_js.exists():
        src = global_js.read_text(encoding='utf-8')
        src = src.replace('`${location.origin}/assets/vendor/browser-image-compression.js`', 'new URL("./assets/vendor/browser-image-compression.js", location.href).href')
        global_js.write_text(src, encoding='utf-8')
    shutil.copy2(BASE/'freephoto-theme.css', target/'freephoto-theme.css')
    shutil.copy2(BASE/'freephoto-i18n.js', target/'freephoto-i18n.js')
    harden_distribution(target)
    patch_zip_download(target)
    (target/'FORK-NOTICE.md').write_text(
        '# FreePhoto fork notice\n\n'
        'This distribution is a modified version of **MAZANOKE** by civilblur.\n'
        f'Original: {UPSTREAM}\nPinned commit: `{UPSTREAM_COMMIT}`\n'
        'Original and derivative code remain under **GNU GPL-3.0**.\n'
        'All upstream copyright, license, bundled vendor components and attribution files are preserved.\n'
        'Changes: Chinese UI overlays, FreePhoto styling/branding, privacy copy and relative PWA paths.\n'
        'Some icons/favicon are inherited from upstream; replace them before separate commercial brand launch.\n',encoding='utf-8')


def build(out: Path, source: Path | None = None) -> None:
    out = out.resolve()
    if source:
        origin = source.resolve()
        if not origin.is_dir(): raise RuntimeError(f'Not a source directory: {origin}')
        if out == origin or out in origin.parents or origin in out.parents:
            raise RuntimeError('Build destination must not overlap the upstream source directory')
        if out.exists():
            raise RuntimeError('Build destination exists; use a clean directory to avoid stale assets')
        shutil.copytree(origin, out, ignore=shutil.ignore_patterns('.git', '.github'))
    else:
        if out.exists(): shutil.rmtree(out)
        subprocess.run(['git','clone','--quiet',UPSTREAM,str(out)],check=True)
        subprocess.run(['git','-C',str(out),'checkout','--quiet',UPSTREAM_COMMIT],check=True)
        shutil.rmtree(out/'.git',ignore_errors=True)
        shutil.rmtree(out/'.github',ignore_errors=True)
    patch_site(out)
    print(f'Built modified FreePhoto into {out}')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=BASE/'dist')
    p.add_argument('--from-source',type=Path,help='Use pre-downloaded upstream source (offline patch/test)')
    args=p.parse_args()
    build(args.out,args.from_source)
