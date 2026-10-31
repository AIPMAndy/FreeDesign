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
