# Windows Codex Lane 4 Validation - Playground Static Gallery Post-Fix

Date: 2026-06-28
Host: Windows NUC / Windows desktop lane
Branch: `validation/2026-06-28-codex-playground-static-gallery-postfix`
Base commit: `29febc2c6b8657bdd0d9bcc3d61908e2389fa582`
Fix PR: `#425` (`fix(docs): prevent playground mobile overflow`)
Evidence bundle: `proofs/validation/playground-static-gallery/windows-20260628-lane4-postfix/`
Manifest: `proofs/validation/playground-static-gallery/windows-20260628-lane4-postfix/MANIFEST.sha256`

## Judgement

**PASS.**

This re-runs Lane 4 after PR #425 merged. The prior validation branch found
desktop playground behavior correct but held the lane because a `390x844`
mobile viewport produced page-level horizontal overflow. Current `main`
contains the fix and the same browser check now reports no horizontal overflow.

## Checks Run

Command:

```powershell
python scripts\garnet_playground_readiness.py --gate --format json
```

Result: exit code `0`.

Command:

```powershell
python scripts\test_garnet_playground_readiness.py
```

Result: exit code `0`; 4 tests passed.

Browser validation against `http://127.0.0.1:8765/playground.html`:

- Desktop initial render: selected `Hello, Garnet`; output `Hello from Garnet!\n=> 0`; console log count `0`.
- `Docs-as-tests` tab: exactly one tab found by role; selected output includes `double(21) = 42`, `triangular(10) = 45`, and `clamp(12, 0, 9) = 9`; console log count `0`.
- `Web route dispatch` tab: exactly one tab found by role; selected output `mvp_05_web_app routes: 61\n=> 61`; console log count `0`.
- Mobile `390x844`: `clientWidth=375`, `scrollWidth=375`, `horizontalOverflow=false`.
- Computed fix signals: `.pane` `min-width=0px`; inline `code` `overflow-wrap=anywhere`.
- Honesty markers remain present: `static gallery`, `not shipping a fake editor`, and `WebAssembly` roadmap language.

## Evidence Files

- `raw/01-playground-readiness-gate.json`
- `raw/02-browser-postfix-desktop-mobile.json`
- `raw/03-playground-readiness-tests.txt`
- `raw/commands.jsonl`
- `screenshots/01-desktop-initial-hello.png`
- `screenshots/02-desktop-docs-as-tests.png`
- `screenshots/03-desktop-web-route-dispatch.png`
- `screenshots/04-mobile-390x844-initial.png`

## Scope Honesty

This validation proves static gallery render, example manifest integrity,
desktop tab behavior, mobile containment after the fix, and disclosure text.
It does not prove live in-browser Garnet execution, WASM execution, or a
production playground editor.
