# FreePhoto · Competitor benchmark · Cycle 1

*All rows are **documented capabilities**, not comparative performance benchmarks. Test on equal hardware, input images, formats and quality targets before declaring a winner.*

| Product | Deployment | Strong documented capabilities | Meaningful gap / differentiation question |
|---|---|---|---|
| [MAZANOKE](https://github.com/civilblur/mazanoke) | Static/offline browser GPL-3.0 | Multiple formats incl. HEIC, batch, target size, EXIF removal | FreePhoto is derivative; must beat baseline usability, not claim better engine by rebranding |
| [Squoosh](https://github.com/GoogleChromeLabs/squoosh) | Browser Apache-2.0 | Multiple codecs, image comparison, privacy/local | Test same quality/size, decode formats and ongoing maintenance |
| [Caesium Web](https://github.com/Lymphatus/caesium-app-web) | Browser / self-host | WASM compressor, preview, metadata retention settings | FreePhoto privacy defaults vs optional metadata retention |
| [iLoveIMG](https://www.iloveimg.com/) | Hosted freemium | Wide user-facing tool catalog incl. crop/rotate/resize | FreePhoto offline privacy vs breadth of user-visible features |
| [ImageMagick](https://imagemagick.org/) | Desktop/CLI | Batch conversion and mature automation | FreePhoto should be far easier for casual mobile users |

## Required reproducible test plan

- Sources: 30 CC0/licensed photos: 10 portraits, 10 text/screenshot, 10 scenery. Preserve originals and SHA-256 checksums.
- Device: record CPU/RAM, browser + build, OS. Repeat cold/warm 5 times; exclude setup/download time.
- Metrics: output size, SSIM or suitable visual-quality metric, processing latency P50/P95, peak memory, unsupported/error count, time to first successful export.
- Privacy: verify image bytes never appear in network requests, inspect metadata after export; no blanket guarantee for inherited filenames or malformed files.
- At this cycle: **no comparable timed measurements were run**. Outstanding.


## Cycle 2: integrity-focused work

MAZANOKE remains the pinned algorithm baseline; Squoosh remains a codec/quality UX comparator. This cycle targets the correctness of partial ZIP download recovery rather than performance superiority. No competitive rank or improvement percentage is asserted without reproducible same-fixture tests.


Cycle 3 addresses a user-facing error-reporting gap in partial ZIP export. No comparative performance or product ranking is asserted.

## Cycle 4 — engineering comparison boundary

MAZANOKE remains the same pinned codec engine, so a FreePhoto UI fork cannot claim improved encoding quality by attribution alone. This cycle targets the **blob URL lifetime after output deletion**. Synthetic 30-image tests are not valid head-to-head performance evidence against Squoosh, Caesium, iLoveIMG or ImageMagick. A real benchmark still requires 30 representative licensed photographs, matching codec/quality, repeated trials on identical hardware, and measured heap/RSS alongside output file size.

## Cycle 4 verified GitHub Actions evidence — 2026-10-31

CI: https://github.com/AIPMAndy/FreeDesign/actions/runs/41176755578 (Linux Ubuntu GitHub Actions, Python 3.12, Chromium, Pillow 12.0.0, pillow-heif 1.8.1; source pinned MAZANOKE ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b).

- Final job conclusion: **success**; 12/12 Python tests, build/attributions, prior Chromium PNG/JPEG/WebP/ZIP regressions, synthetic HEIC and batch suite all completed successfully.
- 30 synthetic JPEGs, each 240×160 pixels: total processing wall time **27,271.6 ms** (single run; no warm/cold repetitions, no before/after speed comparison).
- Output and thumbnail Object URLs: 60 observed, **60 revoked, 0 retained** after individual deletion followed by clearing all results. Proxy for URL lifecycle only; **RSS, JavaScript heap, browser-native memory and true leak-free status NOT measured**.
- Synthetic 8-bit HEIC 64×48→PNG 64×48: decoded, output **85 bytes**, pixel checked. This does **not** validate high-resolution/10-bit Apple HEIC or native Safari.
- No off-device HTTP requests were detected by this test's page-level request listener. This is not a proof of all user/network environments.
- Competitor-controlled benchmark remains **NOT RUN**. Release still conditional: native iOS Safari, meaningful high-resolution corpus, license review and independent Judge remain open.
