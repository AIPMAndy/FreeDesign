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
