# FreePhoto · Product scorecard · Cycle 1

Status: **provisional / NOT RELEASE APPROVED**. Target product: nontechnical users who want batch image compression, format conversion, and basic privacy without uploading photos.

| Dimension | Weight | Measured baseline | Target/verification |
|---|---:|---|---|
| Core functionality | 30% | No real-image E2E baseline on FreePhoto recorded | PNG/JPEG/HEIC conversions, metadata removal, ZIP download; 100% critical smoke success |
| Performance | 20% | **Not measured** | Same-machine 30-image suite, compare P50/P95, heap and output quality against MAZANOKE and Caesium |
| User experience | 20% | **Not measured** | Test desktop/mobile 3-step flow and keyboard-only operation, report task completion |
| Security & reliability | 20% | Code-review finding: HTML injection via filename + root worker URL; fixes proposed | Runtime attack test, network egress test, malformed image errors, dependency report |
| Engineering | 10% | 1 local mock test passed before Cycle 1; 4 local unit tests pass after patch | CI must build locked upstream, verify licenses and run real Chromium tests |

A numeric weighted score or worldwide ranking is **not warranted** until measured data exists. CI output should be used as ground truth; a proposed test is not a passed test.

## Evidence and baseline

- Upstream: [MAZANOKE](https://github.com/civilblur/mazanoke), commit `ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b`, GPL-3.0.
- Original FreePhoto included only four files in `FreeDesign/freephoto/`; no test or CI source files under that directory.
- Local `python -m unittest discover -s tests -v`: before patch 1/1; after patch 4/4. Tests use fixtures and validate code transforms, **not** real image encode/decode.
- Actual Chromium/browser result: pending PR CI; do not claim functionality success from static unit tests alone.

## CI observations (not a benchmark)

- [Initial quality gate run 41174771555](https://github.com/AIPMAndy/FreeDesign/actions/runs/41174771555): 4/4 unit tests and Chromium desktop/mobile-viewport smoke passed. Example processing times **1,032.6 ms desktop**, **253.2 ms mobile viewport** for one synthetic PNG; different warm-up conditions make these **not comparable performance results**.
- [Subsequent run 41174815474](https://github.com/AIPMAndy/FreeDesign/actions/runs/41174815474): browser test timed out after PWA first activation/reload. A test synchronization patch is under review. Stable green repetition and physical device testing remain pending.


## Cycle 2 evidence (until independent CI verification)

- Local mock/unit suite: 4/4 → 8/8. These numbers refer to transformation/build tests, **not** image processing accuracy.
- New real-browser CI: image codec/dimensions, EXIF/PNG metadata marker removal, external HTTP request detection, ZIP corruption test with a revoked middle blob.
- Performance: no same-host competitor baseline or measurable improvement established.
- Release approval: NOT APPROVED pending CI and real-device verification.


### Cycle 2 CI-verified results — 2026-10-31

Evidence: [GitHub Actions quality gate #41175773172](https://github.com/AIPMAndy/FreeDesign/actions/runs/41175773172), commit `9ffcb5294e16e25ca2bb8ab4189d8ad7b170b6d5`.

- Unit tests: **8/8 passed**, compared with 4/4 in Cycle 1.
- Pinned-upstream production build: passed; license, vendor files and attributions present.
- Chromium desktop and 390px mobile viewport PNG smoke: passed. Recorded smoke task time desktop **1333.4 ms** and mobile viewport **315.5 ms**, *not directly comparable due to caching/warmup*.
- Chromium synthetic format/privacy suite: JPEG→WebP and PNG metadata marker removal **passed** (whole-test scenario elapsed **5343.1 ms**).
- Corrupted-middle-blob ZIP test: **passed**, expected `a-green.png` and `c-blue.png` retained correct filenames/pixel identity (scenario elapsed **4469.2 ms**).
- External network request check: none observed in the two synthetic browser scenarios (not a full production network audit).
- Numeric global score: **not assigned**, since iPhone Safari, HEIC, peak memory and same-host competitor quality/performance baselines remain unmeasured.


### Cycle 3 candidate (CI pending)

Product-value fix: partial ZIP exports must visibly disclose skipped-image count; total failure must display an accessible error. Baseline Cycle 2: correctness of ZIP members was proven but skipped files were only logged to the console. Added 2 mock unit tests and a Chromium warning assertion; do not claim passing before CI. No quantified performance changes.

## Cycle 4 — candidate metrics (not yet release-approved)

- Local Python test baseline before cycle: **10/10 passed**. Candidate source checks: **12/12 passed** on local Python 3.13.
- New test: 30 synthetic 240×160 JPEGs; verify completed count and actual decoded output, observed/result object URL count after deleting single card and all cards. Heap memory not measured.
- New test: synthetic 64×48 HEIC→PNG decoded and checked in Linux Chromium. Native iPhone Safari not tested.
- Browser test results and processing time: **pending CI**. Do not claim success or improvement until run is inspected.
- Numerical quality score and same-input competitor performance: **withheld** for lack of comparable controlled measurements.
- Release judgment: NOT RELEASE APPROVED while Safari and representative large-image/peak-memory tests remain outstanding.

## Cycle 4 verified GitHub Actions evidence — 2026-10-31

CI: https://github.com/AIPMAndy/FreeDesign/actions/runs/41176755578 (Linux Ubuntu GitHub Actions, Python 3.12, Chromium, Pillow 12.0.0, pillow-heif 1.8.1; source pinned MAZANOKE ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b).

- Final job conclusion: **success**; 12/12 Python tests, build/attributions, prior Chromium PNG/JPEG/WebP/ZIP regressions, synthetic HEIC and batch suite all completed successfully.
- 30 synthetic JPEGs, each 240×160 pixels: total processing wall time **27,271.6 ms** (single run; no warm/cold repetitions, no before/after speed comparison).
- Output and thumbnail Object URLs: 60 observed, **60 revoked, 0 retained** after individual deletion followed by clearing all results. Proxy for URL lifecycle only; **RSS, JavaScript heap, browser-native memory and true leak-free status NOT measured**.
- Synthetic 8-bit HEIC 64×48→PNG 64×48: decoded, output **85 bytes**, pixel checked. This does **not** validate high-resolution/10-bit Apple HEIC or native Safari.
- No off-device HTTP requests were detected by this test's page-level request listener. This is not a proof of all user/network environments.
- Release still conditional: native iOS Safari, meaningful high-resolution corpus, license review and independent Judge remain open.
