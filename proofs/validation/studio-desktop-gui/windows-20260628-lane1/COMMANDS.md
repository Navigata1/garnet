# Lane 1 Command Log

Host: Windows 11 Pro 10.0.26200, 64-bit.
Repo HEAD and origin/main: `2e2fe843e87be0c8fc9a4745a5bb138fba597d23`.

## Recon

```powershell
git fetch origin main --tags --prune
git rev-parse HEAD
git rev-parse origin/main
gh pr list --repo Island-Dev-Crew/garnet --state open --limit 10 --json number,title,headRefName,author,mergeStateStatus
```

Result: HEAD equals origin/main at `2e2fe843e87be0c8fc9a4745a5bb138fba597d23`; no open PR rows returned.

```powershell
rustc --version
cargo --version
node --version
npm --version
gh auth status
```

Result:

```text
rustc 1.95.0 (59807616e 2026-04-14)
cargo 1.95.0 (f2d3ce0bd 2026-03-21)
v22.22.2
10.9.7
github.com account Navigata1 authenticated for HTTPS git operations
```

## Studio Build And Baseline Tests

```powershell
cd apps/garnet-studio
npm run test:e2e
```

Result: `7 passed (7.1s)`.

```powershell
cargo test --manifest-path apps/garnet-studio/src-tauri/Cargo.toml
```

Result: `19 passed; 0 failed`; doc tests `0 passed; 0 failed`.

```powershell
cd apps/garnet-studio
npm run tauri build
```

Result observed during validation: built `target/release/garnet-studio.exe` and `target/release/bundle/nsis/Garnet Studio_0.8.1_x64-setup.exe`.

## Desktop Driving

The Tauri executable was launched from:

```text
C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet\target\release\garnet-studio.exe
```

The UI was driven by real Windows foreground clicks and screenshots. See `05-` through `17-` PNGs for the counted evidence. `01-`, `02-`, and `04-` are capture false starts. `03-` records the cargo-only launch failure mode where the WebView tried to load a localhost URL; the counted launch used `npm run tauri build`.

## File-Backed Results

Run artifact:

```text
artifacts/run-20260628-001120/run/command.json
exit_code: 0
provider_api_called: false
source_included: false
```

Run stdout:

```text
mvp_01_os_simulator completed: 9
=> 9
```

Manual evidence artifact:

```text
artifacts/manual-20260628-001424/MANIFEST.sha256
```

Assist-plan artifact:

```text
artifacts/assist-plan-20260628-001917/evidence-contract.json
advisory_output_marked_safe: false
no_provider_api_calls: true
source_included: false
```

Persisted settings:

```text
artifacts/settings-after-relaunch.json
mode: power
theme: dark
```
