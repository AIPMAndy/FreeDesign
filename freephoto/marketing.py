"""FreePhoto marketing and product landing sections around the upstream working tool.

Only changes presentation and metadata. Original MAZANOKE image engine remains intact.
"""
from pathlib import Path
import json
import shutil

HERO = """<section class="fp-hero" aria-labelledby="fp-heading">
  <div class="fp-eyebrow"><span class="fp-led"></span> FREE &amp; OPEN SOURCE · LOCAL FIRST</div>
  <h2 id="fp-heading">每一张照片，<br><em>轻一点，自由一点。</em></h2>
  <p class="fp-lead">免费压缩图片、转换格式、调整尺寸，顺手清理可能包含定位信息的照片元数据。无需注册，图片在你的浏览器里处理。</p>
  <div class="fp-hero-actions">
    <a class="fp-action-primary" href="#tool">开始处理图片 <span aria-hidden="true">↗</span></a>
    <a class="fp-action-secondary" href="https://github.com/AIPMAndy/FreeDesign/tree/main/freephoto" target="_blank" rel="noopener noreferrer">查看开源代码 <span aria-hidden="true">↗</span></a>
  </div>
  <div class="fp-trust"><span>◎ 不用上传云端</span><span>✳ 无水印</span><span>↻ 批量处理</span><span>◈ 支持离线使用</span></div>
</section>
"""
DETAILS = """<section class="fp-lower" aria-label="FreePhoto 产品说明">
  <div class="fp-section-intro"><span class="fp-kicker">FOUR TOOLS. ONE PLACE.</span>
    <h2>常用的图片工作，<br>一次处理好。</h2><p>高频功能，做得简单。保留原始文件，结果需要时再下载。</p>
  </div>
  <div class="fp-features">
    <article><span class="fp-feature-num">01 / COMPRESS</span><h3>图片压缩</h3><p>调整质量或目标大小，适合分享照片、优化网站图片。</p></article>
    <article><span class="fp-feature-num">02 / RESIZE</span><h3>调整尺寸</h3><p>按最长边缩小图片，支持常用图片宽高限制。</p></article>
    <article><span class="fp-feature-num">03 / CONVERT</span><h3>格式转换</h3><p>支持 JPG、PNG、WebP 等输出，以及 HEIC 等图片输入。</p></article>
    <article><span class="fp-feature-num">04 / PRIVACY</span><h3>隐私处理</h3><p>处理时不发送图片给本站服务器，重新编码通常移除 EXIF 数据。</p></article>
  </div>
  <div class="fp-privacy" id="privacy"><div><span class="fp-kicker">PRIVACY BY DESIGN</span><h2>你的照片，<br>留在你的设备里。</h2></div>
    <p>FreePhoto 在浏览器本地处理图片。这里没有上传账户，也不需要订阅会员。部分格式受浏览器和设备支持限制；对涉及敏感信息的图片，请在分享前核验输出元数据。站点初次加载需要网络访问静态资源。</p>
  </div>
  <section class="fp-faq" aria-labelledby="faq-heading"><span class="fp-kicker">GOOD TO KNOW</span><h2 id="faq-heading">使用前，你可能想知道</h2>
    <details><summary>图片会发送到服务器吗？</summary><p>产品图像处理逻辑运行在浏览器本地，不设文件上传接口。页面及依赖代码首次加载仍会通过网络传输；请在可信的部署来源使用。</p></details>
    <details><summary>支持哪些图片格式？</summary><p>常见 JPG、PNG、WebP 图片可以直接处理。支持部分 HEIC、AVIF、GIF、SVG、TIFF 等图片输入，实际以浏览器和设备能力为准；部分动画只处理静态帧。</p></details>
    <details><summary>为什么图片压缩后反而更大？</summary><p>取决于原图格式、清晰度、尺寸和输出编码方式。可尝试调整画质或选择 WebP；重要图片请保留原件并检查输出效果。</p></details>
    <details><summary>开源协议和项目来源是什么？</summary><p>FreePhoto 基于 MAZANOKE 的 GPL-3.0 代码改造。感谢原作者 civilblur 及依赖项目贡献者。<a href="https://github.com/civilblur/mazanoke" target="_blank" rel="noopener noreferrer">查看上游项目</a>。</p></details>
  </section>
  <div class="fp-endnote"><strong>FreePhoto.</strong><span>免费使用 · 公开代码 · 不强制注册</span>
    <div><a href="https://github.com/AIPMAndy/FreeDesign/tree/main/freephoto" target="_blank" rel="noopener noreferrer">GitHub 源码 ↗</a><a href="https://metaver.vip/services" target="_blank" rel="noopener noreferrer">作者与 AI 服务 ↗</a></div>
  </div>
</section>"""

def enhance_website(target: Path) -> None:
    html_file = target / "index.html"
    source = html_file.read_text(encoding="utf-8")
    opening = '    <div class="content">'
    ending = '    <footer>'
    if source.count(opening) != 1 or source.count(ending) != 1:
        raise RuntimeError("Upstream DOM changed; cannot safely mount FreePhoto site")
    source = source.replace(opening, HERO + '\n    <div class="content" id="tool">', 1)
    source = source.replace(ending, DETAILS + '\n    <footer>', 1)
    target_marker = '<link rel="stylesheet" href="./freephoto-theme.css" />'
    if source.count(target_marker) != 1:
        raise RuntimeError("Missing FreePhoto theme marker")
    source = source.replace(target_marker, target_marker + '\n    <link rel="stylesheet" href="./freephoto-site.css" />', 1)
    source = source.replace('</head>', '''<meta property="og:type" content="website" />
    <meta property="og:title" content="FreePhoto — 免费本地图片工具箱" />
    <meta property="og:description" content="免费图片压缩、转换格式、调整尺寸，图片在浏览器本地处理。开源、无水印、免登录。" />
    <meta name="theme-color" content="#f7f8f3" />
  </head>''', 1)
    html_file.write_text(source, encoding="utf-8")
    shutil.copy2(Path(__file__).with_name("freephoto-site.css"), target / "freephoto-site.css")
    service_worker = target / "service-worker.js"
    if service_worker.exists():
        sw=service_worker.read_text(encoding="utf-8")
        marker='"./freephoto-theme.css",'
        if marker not in sw:
            raise RuntimeError("Required PWA asset list entry missing")
        service_worker.write_text(sw.replace(marker, marker + '\n  "./freephoto-site.css",', 1),encoding="utf-8")
    (target / "robots.txt").write_text("User-agent: *\nAllow: /\n",encoding="utf-8")
    (target / ".nojekyll").write_text("",encoding="utf-8")
