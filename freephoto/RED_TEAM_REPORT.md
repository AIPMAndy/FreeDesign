# FreePhoto · Red Team report · Cycle 1

Independent-review limitation: Builder and Red Team are separate inspection/test stages in one execution, **not isolated agents**. No independent external judge has approved release.

| ID | Severity | Evidence / reproduction | Proposed mitigation | Status |
|---|---|---|---|---|
| RT-01 | High | Pinned upstream `assets/js/helpers.js` interpolates `outputFileNameText` into template-generated `innerHTML`, including `download` attribute. Test with malicious HTML characters in image filename and inspect resulting DOM. | HTML-escape filename prefix, suffix and attribute value | Patched, real-browser attack unverified |
| RT-02 | High | Pinned upstream `assets/js/compression.js` uses `innerHTML` with `file.name` and `fileName` in progress messages. Malicious filename may create elements. | Use `textContent` for untrusted file names | Patched, real-browser attack unverified |
| RT-03 | Medium | Compression worker URL uses `${location.origin}/assets/...`, incompatible with nested `/FreeDesign/freephoto/` deployment. Existing FreePhoto patch only changed `global.js`. | Resolve URL against current page in `compression.js` | Patched, real browser nested-path test pending |
| RT-04 | Medium | No automated real-image test or verified mobile screenshot prior to Cycle 1 | Add Chromium smoke, output validation, record screenshots | CI proposed; status pending |
| RT-05 | Medium | The PWA icons are inherited upstream; FreePhoto brand is not fully independent. | Design original assets, keep upstream attribution | Deferred, visual assets need review |
| RT-06 | Medium | Upstream issue #53 reports keyboard navigation difficulty | Visible focus ring, run keyboard-only walkthrough | Partial CSS fix, end-to-end audit pending |
| RT-07 | Low | `--from-source` build can merge into existing directory, leaving stale files | Use clean staging build, strict source/destination check | Roadmap |

Attack scope excludes execution against live users or production data. Vulnerabilities are code-review findings until exploit reproductions and fixes are independently confirmed.

| RT-08 | Medium | GitHub Actions run [41174815474](https://github.com/AIPMAndy/FreeDesign/actions/runs/41174815474) timed out waiting for image export; logs show first PWA activation reload during test. | Wait until `navigator.serviceWorker.controller` is established before submitting test input; rerun same smoke | Fix committed; CI revalidation pending |


## Cycle 2 Red Team findings

| ID | Severity | Evidence | Status |
|---|---|---|---|
| RT-08 | High | Upstream download.js filters failed fetch blobs then indexes the original image links by compacted index, potentially exporting images under another file's name. | Patched; browser ZIP regression in CI |
| RT-09 | Medium | --from-source merged into existing dist directory and could leave stale assets. | Refuse existing or overlapping destination, local unit tested |
| RT-10 | Medium | Previous network test only rejected non-GET requests; outbound GET was not detected. | Added network-origin assertion to browser suite |
| RT-11 | Medium | Previous browser tests only used PNG. | Added JPEG→WebP and real PNG/JPEG metadata checks |

**Independent reviewer limitation:** Builder, adversarial audit, and judge are separately documented stages within one assistant session, not three independent agents. iOS Safari, HEIC, large-batch load, and global benchmarks remain unverified.


### Cycle 2 Judge verification — 2026-10-31

[CI run 41175773172](https://github.com/AIPMAndy/FreeDesign/actions/runs/41175773172) passes 8 unit tests and Chromium smoke. Synthetic browser check confirms: (1) JPEG→WebP dimensions and output type, (2) PNG/JPEG private marker removed, (3) invalid middle ZIP blob excluded while remaining green/blue data retains original corresponding names, and (4) no external page request seen. Tests were run in a separate CI environment, though Red Team and Judge were phases of the same assistant session, **not fully independent agents**.

**Remaining issue:** a partially successful ZIP currently skips failed files without a prominent user-facing warning; add an explicit user-visible count/warning before general release. Safari-on-real-iPhone, HEIC variants, larger images, and full egress/dependency audit are still pending. These observations do not justify a global-best claim.
