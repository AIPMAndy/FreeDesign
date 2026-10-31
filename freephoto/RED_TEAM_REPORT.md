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
