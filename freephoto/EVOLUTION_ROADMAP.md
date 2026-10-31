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
