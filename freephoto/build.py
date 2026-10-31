#!/usr/bin/env python3
"""Build GPL-3.0 FreePhoto derivative from pinned MAZANOKE source."""
from pathlib import Path
import argparse, json, re, shutil, subprocess

BASE=Path(__file__).resolve().parent
UPSTREAM="https://github.com/civilblur/mazanoke.git"
COMMIT="ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b"

def patch(out):
    index=out/"index.html"
    html=index.read_text(encoding="utf-8")
    if "MAZANOKE" not in html or "browser-image-compression.js" not in html:
        raise RuntimeError("Upstream changed; refusing unreviewed patch.")
    html=html.replace('lang="en"','lang="zh-CN"',1)
    html=html.replace("MAZANOKE | Online Image Optimizer That Runs Privately in Your Browser","FreePhoto｜免费、本地、开源的图片工具箱")
    html=html.replace("Optimize images locally and privately by converting and compressing them offline in your browser. Supports JPG, PNG, WebP, HEIC, AVIF, GIF, SVG.","免费压缩图片、调整尺寸、转换格式并清理元数据。文件在本地处理，不上传服务器。")
    html=html.replace('content="noindex, nofollow"','content="index, follow"')
    html=html.replace('localStorage.getItem("theme") || "theme-dark"','localStorage.getItem("theme") || "theme-light"')
    html=html.replace('<h1 class="logo-text">MAZANOKE</h1>','<h1 class="logo-text">FreePhoto<span class="freephoto-dot">.</span></h1>')
    html=html.replace('alt="MAZANOKE logo"','alt="FreePhoto"')
    html=html.replace('href="/manifest.json"','href="./manifest.json"')
    html=html.replace('navigator.serviceWorker.register("/service-worker.js")','navigator.serviceWorker.register("./service-worker.js")')
    html=html.replace('content="#191919"','content="#F7F8F3"')
    css='<link rel="stylesheet" type="text/css" href="./assets/css/style.css" />'
    js='<script type="text/javascript" src="./assets/js/events.js"></script>'
    if css not in html or js not in html: raise RuntimeError("Cannot patch upstream index.html safely.")
    html=html.replace(css,css+'\n    <link rel="stylesheet" href="./freephoto-theme.css" />')
    html=html.replace(js,js+'\n    <script defer src="./freephoto-i18n.js"></script>')
    html=html.replace('<span>created by civilblur</span>','<span>原始引擎 MAZANOKE © civilblur · FreePhoto 改造版</span>')
    html=html.replace('Install MAZANOKE','安装 FreePhoto')
    index.write_text(html,encoding="utf-8")
    path=out/"manifest.json"
    d=json.loads(path.read_text(encoding="utf-8"))
    d.update(name="FreePhoto",short_name="FreePhoto",description="免费本地图片工具箱",start_url="./",background_color="#F7F8F3",theme_color="#F7F8F3")
    for icon in d.get("icons",[]): icon["src"]=icon["src"].lstrip("/")
    path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sw=out/"service-worker.js"
    if sw.exists():
        s=sw.read_text(encoding="utf-8")
        s=s.replace('const APP_VERSION = "v1.1.7";','const APP_VERSION = "freephoto-0.1.0";')
        s=s.replace("mazanoke-cache-","freephoto-cache-").replace('"/",','"./",')
        s=re.sub(r'(?<=")/(?!/)(?=[^"\n]+")','./',s)
        s=s.replace('"./index.html",','"./index.html",\n  "./freephoto-theme.css",\n  "./freephoto-i18n.js",')
        sw.write_text(s,encoding="utf-8")
    globals_path=out/"assets/js/global.js"
    src=globals_path.read_text(encoding="utf-8")
    src=re.sub(r"libURL:\s*.*?/assets/vendor/browser-image-compression\.js.*?,",
       'libURL: new URL("./assets/vendor/browser-image-compression.js", location.href).href,',src)
    globals_path.write_text(src,encoding="utf-8")
    for filename in ["freephoto-theme.css","freephoto-i18n.js"]:
        shutil.copy2(BASE/filename,out/filename)
    (out/"FORK-NOTICE.md").write_text(
       "# FreePhoto — fork notice\n\n"
       "Based on MAZANOKE by civilblur (GPL-3.0).\n"
       "Upstream: https://github.com/civilblur/mazanoke\n"
       f"Pinned commit: {COMMIT}\n"
       "Preserved: original LICENSE, docs/ATTRIBUTIONS.md and original processing engine.\n"
       "Changes: brand, translations, color theme and subpath-aware PWA assets.\n",
       encoding="utf-8")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--from-source",type=Path,help="Pre-downloaded MAZANOKE tree")
    ap.add_argument("--out",type=Path,default=BASE/"dist")
    args=ap.parse_args()
    out=args.out.resolve()
    if args.from_source:
        shutil.copytree(args.from_source.resolve(),out,dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".git",".github"))
    else:
        if out.exists(): shutil.rmtree(out)
        subprocess.run(["git","clone","--quiet",UPSTREAM,str(out)],check=True)
        subprocess.run(["git","-C",str(out),"checkout","--quiet",COMMIT],check=True)
        shutil.rmtree(out/".git",ignore_errors=True)
        shutil.rmtree(out/".github",ignore_errors=True)
    patch(out)
    print("FreePhoto built:",out)
