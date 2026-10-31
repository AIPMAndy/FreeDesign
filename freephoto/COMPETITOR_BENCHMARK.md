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
