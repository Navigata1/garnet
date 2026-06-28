# Lane 1 Independent Validation: Studio Desktop GUI

Host: Windows 11 Pro 10.0.26200, 64-bit.
Agent lane: Codex independent validation.
Repo: `Island-Dev-Crew/garnet`.
Commit verified: `2e2fe843e87be0c8fc9a4745a5bb138fba597d23`.
Evidence bundle: `proofs/validation/studio-desktop-gui/windows-20260628-lane1`.

## Verdict

Lane 1 is independently verified on Windows with one UI-label caveat.

The real Tauri desktop shell launched from the built executable, accepted real clicks, rendered command output, created an evidence bundle with an on-screen manifest path, showed live truth numbers, gated simple/power panels, persisted Power mode across relaunch, and kept advisory output labeled as planning evidence rather than safe output.

Caveat: the Run result panel renders `Passed` plus stdout/stderr and the sealed `command.json` records `exit_code: 0`; the UI did not visibly print the literal numeric field name `exit_code`. Treat the behavioral proof as strong, and consider a small follow-up to display `exit_code: 0` explicitly in the result panel.

## Surface Scores

- Real desktop launch and click path: 5/5.
- Run command result visibility: 4/5 because stdout is visible and exit success is visible as `Passed`, but the literal numeric exit code is file-backed rather than printed in the UI.
- Evidence bundle action: 5/5.
- Truth tile decode: 5/5.
- Version stamp: 5/5.
- Simple/power gating and persistence: 5/5.
- Advisory safety labeling: 5/5.

Premier direction: accept this as the Windows desktop behavioral proof for WV-4, with an optional UI polish follow-up for explicit numeric exit-code text.

## Confirmed Facts

- `npm run test:e2e` in `apps/garnet-studio` passed the committed browser harness: `7 passed`.
- `cargo test --manifest-path apps/garnet-studio/src-tauri/Cargo.toml` passed: `19 passed; 0 failed`; doc tests `0`.
- `npm run tauri build` produced `target/release/garnet-studio.exe` and `target/release/bundle/nsis/Garnet Studio_0.8.1_x64-setup.exe`.
- A cargo-only direct build/launch path was not counted as valid desktop proof: screenshot `03-fullscreen-after-foreground.png` shows the WebView trying to load a localhost URL and failing. The counted proof uses the Tauri build path.
- Screenshot `07-after-run-result.png` shows a real Run click producing `Passed` and stdout:
  - `mvp_01_os_simulator completed: 9`
  - `=> 9`
- The copied sealed run artifact records `exit_code: 0` in `artifacts/run-20260628-001120/run/command.json`.
- Screenshot `11-evidence-bundle-result.png` shows the Evidence action creating a bundle and rendering the manifest path:
  - `C:\Users\IslandDevCrew\Desktop\dogfood\garnet-studio-windows-linux\garnet-studio-windows-linux-manual-20260628-001424\MANIFEST.sha256`
- Screenshot `12-release-readiness-panel.png` shows truth tiles with real values, not placeholders:
  - Version `0.8.1`, latest tag `v0.8.1`
  - Tracked slices `87/87`, readiness `92.8%`
  - Primitives `80`
  - Workspace tests `1952 passed / 0 failed`
- Screenshots `08-settings-simple-mode.png` and `09-power-mode-saved.png` show Simple mode hiding power-only panels and Power mode restoring them.
- Screenshot `14-power-mode-persisted-relaunch-foreground.png` and copied `artifacts/settings-after-relaunch.json` show Power mode persisted across relaunch.
- Screenshot `17-advisory-after-terminal-close.png` shows a real advisory assist-plan result with `Status: active-assist-plan` and copy stating it is not active conversion.
- The copied assist-plan evidence contract records `advisory_output_marked_safe: false`, `no_provider_api_calls: true`, and `source_included: false`.

## Recommendations

- Add explicit numeric exit-code text to the Studio command result card, for example `exit_code: 0`, so the UI satisfies the wording of the acceptance criterion without relying on the sealed artifact.
- Keep the browser Playwright suite as regression coverage, but do not present it as desktop-shell proof. The real desktop proof in this report is screenshot/artifact based.
- Use `npm run tauri build` for desktop proof runs. A raw `cargo build --manifest-path apps/garnet-studio/src-tauri/Cargo.toml --release` is insufficient on this Windows host because it produced a binary that attempted to load a localhost page.

## Jon-Only Decisions

- Whether this proof is enough to close the WV-4 public wording gap.
- Whether to require the optional explicit `exit_code: 0` UI text before public deck or release copy changes.
- Any release, tag, or public claim update.
