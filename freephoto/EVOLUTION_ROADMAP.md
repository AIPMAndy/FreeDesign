# FreePhoto · Evolution roadmap · Next cycles

## Cycle 1 (this PR)

- Preserve pinned mature MAZANOKE engine and GPL/third-party notices.
- Fix nested-URL worker bug, filename HTML injection paths and keyboard focus visibility.
- Add unit tests and GitHub Actions Chromium desktop/mobile smoke; report actual workflow outcome before accepting.
- Keep main branch and live website unchanged until review.

## Cycle 2 — Release blockers before publication

1. Verify real PNG/JPEG/WebP/HEIC decode/export, corrupt file recovery, metadata and ZIP on desktop and real mobile Safari.
2. Independently reproduce malicious filename injection attempts and document pass/fail; inspect network traffic for image byte upload.
3. Replace inherited imagery, favicon and PWA icons with independently licensed original brand assets.
4. Validate nested GitHub Pages deployment, SEO links, mobile accessibility and offline cache.
5. Compare identical 30-image dataset with MAZANOKE, Squoosh and Caesium; do not claim superiority without numerical data.

## Cycle 3 — User value

- Interview 5–10 real users about confusing format names, batch actions, privacy and download behavior.
- Only add highly requested features such as side-by-side quality comparison or drag-to-crop after validated need.
- Consider independent repo `AIPMAndy/FreePhoto` and live deployment only after owner approval.

## Stop conditions

If any file leaves the device unexpectedly, image bytes are modified without clear notice, license obligations fail, or a high-severity flaw remains, **do not release**. Revert regressions and keep the prior version.


## Cycle 2 execution and Cycle 3 gate

1. Fix partial ZIP blob/name association and stale build destination; retain original GPL engine.
2. Run Chromium JPEG/PNG/WebP, ZIP, and same-origin request smoke in CI; collect raw evidence.
3. Keep PR draft until CI and independent real-device checks.
4. Next: real Safari iPhone; HEIC realistic fixtures; 30-image identical-environment P50/P95 and peak memory benchmark; accessibility keyboard walkthrough. Do not deploy without user confirmation.


### Next cycle after green CI (2026-10-31)

- Release-blocking: user-visible **partial ZIP failure warning**, so a successful ZIP cannot silently hide omitted files.
- On-device: actual iPhone Safari HEIC/JPEG/PNG plus ZIP downloads; Android Chrome and keyboard-only tests.
- Benchmark: 30 common-image corpus under identical browser/hardware settings, collecting P50/P95 and peak memory against pinned MAZANOKE and Squoosh where fair.
- Security: adversarial SVG/EXIF input, malformed images, oversized files, supply-chain inventory and offline PWA validation.
- Keep both PR #3 and stacked PR #4 in Draft until independent release approval and user confirmation for production publish.


Cycle 3: add accessible partial/total ZIP warnings, verify with 10 Python tests and the CI Chromium failed-middle-blob test. Keep PR draft. After CI: real Safari iPhone/HEIC and a 30-image same-hardware competitor benchmark.

## Cycle 4 — working branch `feat/freephoto-cycle-4-blob-lifecycle`

1. Builder: clean up output image and thumbnail object URLs after single-item and all-result deletion; do not touch upstream compression algorithms.
2. Attack: test repeated create/delete behavior with 30 synthetic JPEGs, generate HEIC in CI, inspect external requests and output pixel identity.
3. Judge: inspect GitHub Actions logs + JSON and reject release on any critical regression.
4. Next: native Safari on iPhone, 10/12-bit and corrupt HEIC, genuine 20MP×30 batch RSS/heap profiling, image comparison against stock MAZANOKE, independent UX accessibility testing.
5. Keep PR as Draft; no merge or deployment until user approves and blockers are addressed.

## Cycle 4 verified GitHub Actions evidence — 2026-10-31

CI: https://github.com/AIPMAndy/FreeDesign/actions/runs/41176755578 (Linux Ubuntu GitHub Actions, Python 3.12, Chromium, Pillow 12.0.0, pillow-heif 1.8.1; source pinned MAZANOKE ceab516ade2a68f3c0abef8bd8fa03ada3ac3e7b).

- Final job conclusion: **success**; 12/12 Python tests, build/attributions, prior Chromium PNG/JPEG/WebP/ZIP regressions, synthetic HEIC and batch suite all completed successfully.
- 30 synthetic JPEGs, each 240×160 pixels: total processing wall time **27,271.6 ms** (single run; no warm/cold repetitions, no before/after speed comparison).
- Output and thumbnail Object URLs: 60 observed, **60 revoked, 0 retained** after individual deletion followed by clearing all results. Proxy for URL lifecycle only; **RSS, JavaScript heap, browser-native memory and true leak-free status NOT measured**.
- Synthetic 8-bit HEIC 64×48→PNG 64×48: decoded, output **85 bytes**, pixel checked. This does **not** validate high-resolution/10-bit Apple HEIC or native Safari.
- No off-device HTTP requests were detected by this test's page-level request listener. This is not a proof of all user/network environments.
- Release still conditional: native iOS Safari, meaningful high-resolution corpus, license review and independent Judge remain open.
