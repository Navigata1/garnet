# Fleet Report - Windows NUC - Codex - W-SHIP Preflight - 2026-06-15

**Machine:** Windows NUC / GMKtec NucBox lane.
**Agent/model:** Codex on Windows NUC.
**Date/time:** 2026-06-15, America/Chicago.
**Repo path:** `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet`.
**Report scope:** Studio and W-SHIP evidence preflight only. No Rust crate edits, no tag, no release edit, no package submission, no CI/gate mutation.

## Bottom Line

This Windows NUC now has a current-main, 0.8.1-stamped unsigned x64 Garnet Studio NSIS clean-VM proof. The proof installs `Garnet Studio_0.8.1_x64-setup.exe` inside Windows Sandbox, records registry version `0.8.1`, runs installed `--studio-smoke`, and captures a live launch screenshot.

This upgrades the local Windows Studio evidence from the older 0.1.0 installer proof to a 0.8.1 unsigned x64 clean-VM proof. It does **not** prove signed MSI, Authenticode, winget, scoop, Windows ARM64, clean non-WSL Linux desktop GUI, Linux seccomp, production, or v1.0 readiness.

## Source Contracts Read

- `F_Project_Management/AGENTS.md:12` requires verification evidence to preserve commands, platform, commit, pass/fail state, and known gaps.
- `apps/garnet-studio/src-tauri/AGENTS.md:11` keeps Windows/Linux Studio as a thin wrapper over existing Garnet surfaces.
- `apps/garnet-studio/src-tauri/AGENTS.md:16` forbids adding provider API, credential, or network handoff paths in Studio.
- `apps/garnet-studio/src-tauri/AGENTS.md:25` routes Windows/Linux Studio evidence to the Desktop dogfood root.
- `apps/garnet-studio/src-tauri/AGENTS.md:38` makes the Tauri Cargo.toml version the single Studio version stamp.
- `F_Project_Management/GARNET_S129_S200_ECC_DOGFOOD_COMMAND_CENTER.md:44` records the v0.8.1 release VSIX naming drift.
- `F_Project_Management/GARNET_S129_S200_ECC_DOGFOOD_COMMAND_CENTER.md:212` assigns S166-S178 Distribution reach to the NUC-led package smoke and OS-specific evidence lane.
- `F_Project_Management/GARNET_S129_S200_ECC_DOGFOOD_COMMAND_CENTER.md:639` through `:643` define the Windows/Linux package and smoke plan boundary, including Linux desktop GUI proof not being confused with WSL portability.
- `F_Project_Management/GARNET_S129_S200_ECC_DOGFOOD_COMMAND_CENTER.md:650` through `:652` forbid ECC hooks, public claims, and Linux seccomp or OS-sandbox claims from WSL.
- `F_Project_Management/W_REBUILD/W_REBUILD_SPEC.md:465` through `:467` identify Windows/Linux/Tauri smoke plus packaging plans as parallel-safe while freezing W-REBUILD implementation crates.
- `F_Project_Management/W_REBUILD/W_REBUILD_SPEC.md:473` through `:474` identifies W-SHIP as S166-S178, NUC-led distribution work.

## Repo Truth

| Fact | Evidence |
|---|---|
| Active checkout | `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet` |
| Branch at recon | `main` tracking `origin/main` |
| Report branch | `fleet/2026-06-15-windows-nuc-codex-wship-preflight` |
| HEAD | `9d155903c39eb1faefef87e1fa32f65dc53e954c` |
| origin/main | `9d155903c39eb1faefef87e1fa32f65dc53e954c` |
| Local status before report | tracked tree clean; untracked `F_Project_Management/FLEET_REPORTS.local-backup-20260612/` and `audit-windows/` pre-existing |
| Open PRs | none returned by `gh pr list --repo Island-Dev-Crew/garnet --state open --limit 20` |
| Latest PR state sample | latest 12 PRs queried with `--state all --limit 12` were merged, ending at #406 through #395 |

## Release Asset Truth

`gh release view v0.8.1 --repo Island-Dev-Crew/garnet --json tagName,publishedAt,url,targetCommitish,assets` reported:

- Release: `v0.8.1`, published `2026-06-07T07:55:45Z`, targetCommitish `main`.
- Assets: Linux `.deb`, Linux `.rpm`, macOS aarch64/x86_64 tarballs, SBOM, `SHA256SUMS`, `SHA256SUMS.asc`, and two VSIX files named `garnet-0.7.0-lsp-mvp-*`.
- No Windows release asset is attached to the GitHub release.

## Toolchain Truth

| Tool | Result |
|---|---|
| Rust | `rustc 1.95.0 (59807616e 2026-04-14)` |
| Cargo | `cargo 1.95.0 (f2d3ce0bd 2026-03-21)` |
| Node | `v22.22.2` |
| Java | OpenJDK `1.8.0_492` |
| WSL | Default distribution `Ubuntu`, default version 2; `Ubuntu` and `docker-desktop` both stopped at recon |
| GitHub auth | `gh` authenticated as `Navigata1`; scopes include `repo` and `workflow` |

## Verification Snapshot

| Command | Result | Notes |
|---|---:|---|
| `git fetch origin main --tags --prune` | pass | Current Desktop checkout remained at `origin/main` |
| `git status --short --branch` | pass | tracked clean; two pre-existing untracked local evidence dirs |
| `git rev-parse HEAD` / `origin/main` | pass | both `9d155903c39eb1faefef87e1fa32f65dc53e954c` |
| `gh pr list --repo Island-Dev-Crew/garnet --state all --limit 12` | pass | latest 12 listed PRs were merged |
| `gh pr list --repo Island-Dev-Crew/garnet --state open --limit 20` | pass | no open PR output |
| `python -B scripts\check-agent-contracts.py` | pass | `agent-contracts: ok (23 contracts)` |
| `python -B scripts\garnet_readiness_status.py --format json` | pass | 87/87 tracked slices, 100.0% |
| `python -B scripts\garnet_mit_readiness_status.py --format json` | pass | `overall_status=active-partial`, `completion_percent=92.7` |
| `python -B scripts\garnet_windows_clean_vm_installer_status.py --format json` | pass | latest proof is 0.8.1 clean-VM verified |
| `python -B scripts\garnet_windows_linux_studio_status.py --format json` | pass | Windows clean-VM verified; Linux gate replay verified; Linux desktop still open |
| `python -B scripts\garnet_v0_8_1_release_readiness.py --format json` | pass | release-ready reporter still includes legacy `red-team` wording in subgate names |
| `python -B scripts\garnet_vscode_publish_readiness.py --format json` | pass | marketplace path is ready but publication is deferred pending tokens |
| `git diff --check` | pass | no whitespace errors |

Cargo workspace test/clippy were not rerun because this lane made no source-code change and the current goal is fleet evidence/reporting. The report did run the contract/readiness/status reporters relevant to the touched evidence surface.

## Native Windows Proof

### Current 0.8.1 Studio executable smoke

A current 0.8.1 Studio executable exists in the sibling distribution worktree:

- Worktree: `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet-dist-wt`
- Worktree HEAD: `9d155903c39eb1faefef87e1fa32f65dc53e954c`
- Worktree status: detached `HEAD`, no branch output beyond `## HEAD (no branch)`
- Executable: `target\release\garnet-studio.exe`, length `9636352`, modified `2026-06-12 07:16:55`

Command run:

```powershell
& 'C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet-dist-wt\target\release\garnet-studio.exe' --studio-smoke
```

Result:

- Exit code: 0
- Output: `Garnet Studio smoke passed`
- Evidence bundle: `C:\Users\IslandDevCrew\Desktop\dogfood\garnet-studio-windows-linux\garnet-studio-windows-linux-smoke-20260615-163201`
- `studio-smoke.json` SHA-256: `A19BE54664D95756926B7884E02D0C5D87FAB4F1BC3D1D12B8F5F08A69F5B056`
- JSON summary: `app_version=0.8.1`, `platform=windows`, `arch=x86_64`, `status=passed`, `source_included=false`, `provider_api_called=false`.

### Current 0.8.1 unsigned NSIS clean-VM proof

Artifact found:

- Path: `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet-dist-wt\target\release\bundle\nsis\Garnet Studio_0.8.1_x64-setup.exe`
- Length: `2027878`
- Modified: `2026-06-12 07:16:55`
- SHA-256: `07585423B286EE85105187E9573D994973F9F4BE2022B3B04867996C7352A17C`

Clean-VM command path:

- Created fresh evidence root: `C:\Users\IslandDevCrew\Desktop\dogfood\garnet-studio-windows-clean-vm\clean-vm-sandbox-20260615-175702`
- Copied the 0.8.1 installer into `sandbox-share`.
- Adapted the existing guest smoke script to use `Garnet Studio_0.8.1_x64-setup.exe`.
- Launched `WindowsSandbox.exe` with `GarnetCleanVmSandbox.wsb`.
- Waited for `proof-ready.marker`.
- Recorded proof with `scripts\garnet_windows_clean_vm_installer_status.py --record-proof --mode clean-vm`.

Verified proof:

- Proof JSON: `C:\Users\IslandDevCrew\Desktop\dogfood\garnet-studio-windows-clean-vm\clean-vm-sandbox-20260615-175702\windows-clean-vm-installer-proof.json`
- Proof JSON SHA-256: `BE98D2FD330411E49016621564190655A4C822130856C0E3036F710E23484E83`
- Screenshot: `C:\Users\IslandDevCrew\Desktop\dogfood\garnet-studio-windows-clean-vm\clean-vm-sandbox-20260615-175702\sandbox-share\installed-studio-launch.png`
- Screenshot SHA-256: `D90DD247F3EE346BF4CBC9ACDB94AC3577C0BFA4A602323FC7BBBDB2CD456565`
- VM: `WindowsSandbox-285F1B15-3C3E-4`
- Guest: `Microsoft Windows 11 Enterprise 10.0.26100 build 26100`, `AMD64`
- Installer SHA-256 inside guest: `07585423b286ee85105187e9573d994973f9f4be2022b3b04867996c7352a17c`
- Installer exit code: 0
- Registry candidate: `Garnet Studio`, version `0.8.1`, install location `C:\Users\WDAGUtilityAccount\AppData\Local\Garnet Studio`
- Installed executable: `C:\Users\WDAGUtilityAccount\AppData\Local\Garnet Studio\garnet-studio.exe`
- Installed `--studio-smoke` exit code: 0
- Smoke JSON: `status=passed`, `source_included=false`, `provider_api_called=false`, `app_version=0.8.1`
- Launch screenshot dimensions: `1220x840`

Claim boundary for this proof:

- Proves unsigned x64 NSIS installer install/smoke/launch in Windows Sandbox.
- Does not prove signed MSI.
- Does not prove Authenticode.
- Does not prove winget or scoop.
- Does not prove Windows ARM64.
- Does not prove Linux package/runtime completion.
- Does not prove provider-backed conversion.

## WSL And Linux Evidence Taxonomy

| Column | Current state | Claim boundary |
|---|---|---|
| Native Windows proof | Verified for 0.8.1 unsigned x64 NSIS clean-VM install, installed smoke, launch screenshot | Not signed; not package-manager published; not ARM64 |
| WSL execution | WSL2 Ubuntu exists; repo reporters show committed WSL/WSLg package/runtime/display/domain/release shell evidence | Execution/portability only; never Linux seccomp or OS-sandbox enforcement |
| Clean Linux proof | Not produced on this NUC in this pass | A real non-WSL Linux VM or desktop session is still needed |
| Linux desktop GUI | Not proven | WSLg/Xvfb rows do not upgrade to clean/non-WSL desktop GUI proof |
| Not proven | signed MSI, Authenticode, winget, scoop, Windows ARM64, clean Linux desktop GUI, Linux seccomp from this machine | Jon-only or other-machine evidence required |

## VSIX Naming / Publication Readiness

Confirmed release drift: the v0.8.1 release still carries VSIX assets named `garnet-0.7.0-lsp-mvp-*`. The repo's `garnet_vscode_publish_readiness.py` reporter returns marketplace readiness, but actual OpenVSX and VS Code Marketplace publication remain deferred pending tokens.

Recommendation: keep the historical v0.7.0-named VSIX assets on v0.8.1 unless Jon chooses a release-asset cleanup. Prepare new 0.8.1-named VSIX artifacts and checksums for future release or asset replacement, but do not mutate the published release from this lane.

## Legacy Review-Lane Wording

The release-readiness reporter still prints legacy `red-team` wording for S114 in `scripts/garnet_v0_8_1_release_readiness.py` and `scripts/garnet_red_team_status.py`. This report uses `S114 review lane` language, but did not edit those gate/reporting files because gate semantics and release-readiness wording are outside this report-only W-SHIP lane.

Recommended cleanup, if Jon approves: rename user-facing S114 labels from `red-team` to `review team` / `S114 review lane` while preserving script compatibility or adding aliases. Do not change pass/fail semantics in the same cleanup.

## W-SHIP Next Package / Smoke Slices

These are recommended slice targets after this report:

1. **S166 - Preserve 0.8.1 Windows Studio clean-VM proof in repo-visible form.** Commit a reduced proof manifest that points to the Desktop dogfood bundle hashes without adding binary installer or screenshot payloads to git.
2. **S167 - Windows Studio release artifact staging.** Produce a release-candidate Windows x64 Studio installer bundle with checksum and install transcript; Jon decides whether it attaches to an existing or future release.
3. **S168 - Signed MSI / Authenticode plan.** Validate `signtool` path and certificate requirements; no signing claim until a certificate signs the artifact and clean-machine smoke verifies it.
4. **S169 - winget and scoop draft manifests.** Draft and locally validate manifests against the Windows artifact, but submit nowhere.
5. **S170 - Windows ARM64 proof.** Install `aarch64-pc-windows-msvc`, build the ARM64 NSIS target, and smoke it on real Windows ARM64 hardware or a suitable VM.
6. **S171 - Linux evidence taxonomy lock.** Keep WSL/WSLg rows labeled execution/portability only and add a clean Linux proof checklist that cannot be satisfied by WSL.
7. **S172 - Clean Linux CLI package proof.** Install the v0.8.1 `.deb`/`.rpm` in a non-WSL Linux VM and run CLI smoke plus checksum verification.
8. **S173 - Clean Linux desktop GUI proof.** Launch the Tauri shell in a real Linux desktop session and capture screenshot plus smoke transcript.
9. **S174 - VSIX 0.8.1 naming prep.** Build 0.8.1-named VSIX artifacts for darwin-arm64, linux-x64, and win32-x64; no release mutation without Jon.
10. **S175 - W-SHIP report rollup.** Consolidate Windows, WSL-portability, clean Linux, package-manager, and VSIX state into a release decision memo.

## Proven / Portability-Only / Not-Proven Counts

| Bucket | Count | Items |
|---|---:|---|
| Proven on this Windows NUC | 6 | current repo HEAD==origin/main; agent contracts; tracked readiness; 0.8.1 Studio exe smoke; 0.8.1 unsigned x64 NSIS clean-VM install/smoke/launch; git diff whitespace check |
| Portability-only | 3 | WSL2 availability; committed WSL/WSLg Studio package/display/domain/release-shell evidence; Linux/Tauri gate replay status |
| Not proven | 8 | signed MSI; Authenticode; winget; scoop; Windows ARM64; clean non-WSL Linux CLI install; clean non-WSL Linux desktop GUI; Linux seccomp/OS-sandbox enforcement from this machine |

## Jon-Only Decisions

- Whether to attach any Windows Studio artifact to a GitHub release.
- Whether to mutate existing v0.8.1 release assets or leave them historical.
- Whether to rename/republish VSIX assets on v0.8.1.
- Whether to proceed with Authenticode signing credentials.
- Whether to submit winget/scoop manifests.
- Whether to rename legacy `red-team` reporter labels to `review team` / `S114 review lane`.
- Any tag, release, marketplace, or public launch action.

## Safe Next Action

Commit this report branch only. Do not open a PR unless the consolidation lane asks for it. Next implementation work should be a separate S166/S167 slice that commits a small proof index, not the large binary installer/screenshot artifacts themselves.
