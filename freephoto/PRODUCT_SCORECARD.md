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
