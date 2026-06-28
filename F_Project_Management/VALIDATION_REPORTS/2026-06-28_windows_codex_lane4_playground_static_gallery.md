# Windows Codex Lane 4 Validation - Playground Static Gallery

Date: 2026-06-28
Host: Windows NUC / Windows desktop lane
Branch: `validation/2026-06-25-codex-playground-static-gallery`
Base commit: `2e2fe843e87be0c8fc9a4745a5bb138fba597d23`
Evidence bundle: `proofs/validation/playground-static-gallery/windows-20260628-lane4/`
Manifest: `proofs/validation/playground-static-gallery/windows-20260628-lane4/MANIFEST.sha256`

## Judgement

**HELD, with one concrete UI fix recommended.**

The static playground gallery is structurally valid and the desktop browser
flow renders the three recorded examples without console/runtime errors. The
page also keeps the calibrated honesty markers that say this is a static
gallery, not a live editor.

The lane is not a clean pass because a 390px mobile viewport produces
page-level horizontal overflow. The overflow diagnosis points at the preview
pane/preformatted source and output blocks, not at Garnet execution logic.

## Checks Run

Command:

```powershell
python scripts\garnet_playground_readiness.py --gate --format json
```

Result: exit code `0`.

Key output:

```json
{
  "schema": "garnet.playground_readiness/v1",
  "page_present": true,
  "manifest_present": true,
  "example_count": 3,
  "examples_well_formed": true,
  "page_references_manifest": true,
  "honesty_markers_present": true,
  "missing_markers": [],
  "ok": true
}
```

Browser validation against `http://127.0.0.1:8765/playground.html`:

- Initial desktop render: selected `Hello, Garnet`; output `Hello from Garnet!\n=> 0`; console log count `0`.
- `Docs-as-tests` tab: exactly one tab found by role; selected output includes `double(21) = 42`, `triangular(10) = 45`, and `clamp(12, 0, 9) = 9`; console log count `0`.
- `Web route dispatch` tab: exactly one tab found by role; selected output `mvp_05_web_app routes: 61\n=> 61`; console log count `0`.
- Honesty markers in normalized body text: `static gallery`, `not shipping a fake editor`, and `WebAssembly` roadmap language all present.

## Finding

At viewport `390x844`, the document reports `clientWidth=375` and
`scrollWidth=644`, so `horizontalOverflow=true`.

Largest overflow offenders recorded in
`raw/04-mobile-overflow-diagnosis.json`:

- `pre#source`: right edge `644`, overflow right `269`.
- `pre#output`: right edge `644`, overflow right `269`.
- Parent `.pane` containers match the same overflow width.

Recommended fix slice: constrain the playground panes on narrow screens,
likely with `min-width: 0` on `.pane` and wrapping/containment rules for
inline and preformatted code where appropriate. Re-run this lane after the fix
and require `horizontalOverflow=false` at `390x844`.

## Evidence Files

- `raw/01-browser-initial.json`
- `raw/02a-tabs-snapshot.txt`
- `raw/02-browser-tab-and-mobile.json`
- `raw/03-playground-readiness-gate.json`
- `raw/04-mobile-overflow-diagnosis.json`
- `raw/commands.jsonl`
- `screenshots/01-playground-initial.png`
- `screenshots/02-docs-as-tests-tab.png`
- `screenshots/03-web-route-dispatch-tab.png`
- `screenshots/04-mobile-390x844-initial.png`

## Scope Honesty

This validation proves static gallery render, example manifest integrity,
desktop tab behavior, and disclosure text. It does not prove live in-browser
Garnet execution, WASM execution, or a production playground editor.
