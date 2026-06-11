# Distribution-Band Evidence Report — Windows NUC — Claude (Fable 5) — 2026-06-11

**Lane:** S166–S178 (W-SHIP) distribution-band evidence, NUC-led per the command center.
**Machine:** GMKtec NucBox M2Pro_S (`NUCBOX_M2PRO_S`), Windows 11 Pro 10.0.26200.8457.
**Repo path:** `C:\Users\IslandDevCrew\Desktop\Garnet Opus 4.7 final\garnet` (main checkout, untouched);
evidence worktree `garnet-dist-wt` pinned **detached at `f03d414`** (= `origin/main` at run time,
"RB-0d: site stats stamped from truth.json + 0.8.1 VSIX prepared + @caps blog draft (#387)").
**Account:** `gh` = Navigata1 (fork-only). **Scope:** machine-local proof + distribution plans only —
no crate edits, no PRs, no slice implementation, no publication of anything, evidence-review language.
**Toolchain:** rustc/cargo 1.95.0, node v22.22.2, python3 3.14.4, WSL 2.6.3.0 (Ubuntu 24.04.4 LTS,
kernel 6.6.87.2), winget v1.28.240, VS Code 1.116.0, docker CLI 29.4.3 (daemon stopped).
**Companion artifacts:** `F_Project_Management/DISTRIBUTION_DRAFTS/` (this branch);
machine-local evidence bundles under `…\dist-staging-20260611\` (not committed — inventory below).

Truth labels as in the 2026-06-10 fleet reports: **[released]** GitHub release asset ·
**[committed]** on origin/main · **[machine-local]** this NUC only · **[not-proven]**.

---

## Task 1 — Reproducible Smoke Matrix (what passes today, from this machine)

### Matrix overview

| Surface | Native Windows | WSL (portability-only) | Clean-Linux | Not proven |
|---|---|---|---|---|
| Fresh CLI build off main (`f03d414`) | ✅ builds, banner **0.8.1** | n/a | — | byte-reproducibility across machines |
| `garnet check` (safe_io_layer) | ✅ 0 diagnostics | ✅ 0 diagnostics¹ | — | |
| `garnet run` (agentic example) | ✅ deterministic, exit 0 | not run | — | |
| Domain matrix (suite=all) | ✅ **20/20 cases, 60/60 commands** | not run | — | |
| v0.8.1 `.deb` [released] | n/a | ✅ dpkg install clean, banner 0.8.1¹ | ❌ no VM path from here | clean-distro install UX |
| v0.8.1 `.rpm` [released] | hash-verified only | not run | ❌ | any rpm-based install |
| Asset hashes vs SHA256SUMS | ✅ deb/rpm/SBOM match | n/a | — | macOS tarballs (out of lane) |
| GPG signature of SHA256SUMS | ✅ Good signature, fingerprint matches [committed] key | (gpg executed in WSL) | — | |
| Released VSIX on win32 | ⚠ installs (untargeted — see Task 2) | not run | — | win32-x64 VSIX target (none exists) |
| Studio (Tauri) build off main | ✅ NSIS installer produced | n/a | ❌ | clean-VM re-proof at 0.8.1; signing |
| Windows release asset | — | — | — | ❌ none exists on v0.8.1 |
| OS-sandbox enforcement (any OS) | **deferred** | **never claimable from WSL** | — | ❌ no deterministic trap exercised this pass |

¹ All WSL rows are **execution/portability evidence only — not a Linux sandbox, seccomp,
or clean-distro claim** (standing rule; seccomp claims are Linux-only and require a
deterministic trap, which was not exercised in this pass).

### Cell evidence — exact commands and outputs

**N1 · Fresh native build off current main** [machine-local]

```powershell
# cwd = garnet-dist-wt (worktree @ f03d414); warm cache reuse:
$env:CARGO_TARGET_DIR = "C:\...\garnet\target"
cargo build --release -p garnet-cli
#   Compiling garnet-cli v0.8.1 (...garnet-dist-wt\garnet-cli)
#   Finished `release` profile [optimized] target(s)   (exit 0)
```

**N2 · Version banner**

```powershell
& "C:\...\garnet\target\release\garnet.exe" --version
# garnet 0.8.1 (Top-level garnet(1) CLI — parse / check / run / test / new / keygen /
#   build --sign / verify / convert + the trust spine (caps / diff-caps / seal / sandbox /
#   caps-log / agent-loop) (v0.8.1).)
#   parser 0.3.0 · interp 0.3.0 · vm 0.5.0 · check 0.3.0 · memory 0.3.0 · actor-rt 0.4.0 ·
#   stdlib 0.4.0 (22 bridged primitives) · convert 0.4.0
```

The 0.5.0-banner staleness recorded in both 2026-06-10 NUC fleet reports is **resolved by
building from current main** — the drift was checkout age, not Windows behavior.

**N3 · Checker smoke**

```powershell
garnet.exe check "...\garnet-dist-wt\examples\safe_io_layer.garnet"
# 17 functions checked, 32 boundary call sites, 0 diagnostics   (exit 0)
```

**N4 · Run smoke** (first case of the agentic dogfood matrix per `scripts/run_agentic_dogfood_matrix.py`)

```powershell
garnet.exe run "...\garnet-dist-wt\examples\agent_toolbelt_01_triage_router.garnet"
# agent toolbelt triage score: 91
# => 91   (exit 0)
```

**N5 · Full Windows domain matrix against the fresh release binary**

```powershell
python3 -B "...\garnet-dist-wt\scripts\smoke_garnet_studio_domain_matrix.py" --suite all `
  --garnet "...\garnet\target\release\garnet.exe" `
  --output-dir "...\dist-staging-20260611\domain-matrix-v081-release" --format json
# status=passed · platform=windows · arch=AMD64
# case_count=20 passed_cases=20 failed_cases=0
# command_count=60 passed_commands=60 failed_commands=0
# (12 core-MVP + 8 agentic cases; source_included=false; provider_api_called=false; exit 0)
```

Evidence bundle (JSON + MD + per-command captures + `MANIFEST.sha256`):
`dist-staging-20260611\domain-matrix-v081-release\` [machine-local].

**W1–W4 · WSL .deb portability** (all rows portability-only)

```powershell
wsl -d Ubuntu -u root -- uname -a
# Linux NUCBOXM2PRoS 6.6.87.2-microsoft-standard-WSL2 ... x86_64   (Ubuntu 24.04.4 LTS)
wsl -d Ubuntu -u root -- dpkg -i /tmp/garnet_0.8.1-1_amd64.deb   # (copied to /tmp; spaces in /mnt/c path)
# Unpacking garnet (0.8.1-1) ... Setting up garnet (0.8.1-1) ...   — no dependency errors
wsl -d Ubuntu -u root -- garnet --version
# garnet 0.8.1 (… v0.8.1)   — matches package version
wsl -d Ubuntu -u root -- garnet check "/mnt/c/.../garnet-dist-wt/examples/safe_io_layer.garnet"
# 17 functions checked, 32 boundary call sites, 0 diagnostics
# which garnet → /usr/bin/garnet · dpkg -s garnet → Status: install ok installed
```

Package intentionally left installed in WSL Ubuntu (recorded machine-state change).

**A1–A4 · Asset integrity + signature** [released assets, verified machine-locally]

```text
garnet_0.8.1-1_amd64.deb    ca35ebf8… = SHA256SUMS line 1  ✅
garnet-0.8.1-1.x86_64.rpm   88b4e9cb… = SHA256SUMS line 2  ✅
garnet-sbom-cyclonedx.tgz   79c1d2b7… = SHA256SUMS line 5  ✅
macOS tarballs              not downloaded (out of lane) — not verified locally
VSIX (both)                 hashed (16d31c50… / 60f846a1…) — NO SHA256SUMS entry exists (see Task 2)
```

```bash
# gpg absent on Windows host; WSL gpg 2.4.4 used as execution environment only:
gpg --import .../garnet-dist-wt/docs/garnet-release-signing.pub.asc   # key C14DF6E713956ED1 imported
gpg --verify SHA256SUMS.asc SHA256SUMS
# Good signature from "Garnet Release Signing <jon-isaac@islanddevcrew.com>"
# Primary key fingerprint: 04D5 6F91 F038 17DD FFEB  C62A C14D F6E7 1395 6ED1
#   = EXACT match to docs/release-signing.md line 10 [committed]; sig dated 2026-06-07 (re-cut date)
```

**G1–G5 · Current-main gates on the worktree** [machine-local, first post-v0.8.1 run on this NUC]

```text
check-agent-contracts.py          → agent-contracts: ok (21 contracts)        exit 0
garnet_readiness_status.py        → 87/87 slices, 100.0%, 0 open              exit 0
garnet_mit_readiness_status.py    → overall_status=active-partial, 92.8%      exit 0 (first try; no temp-dir issue this run)
git diff --check                  → empty                                      exit 0
docs/truth.json                   → version 0.8.1, primitives 80 (core 40/std 40), tests 1952 passed/0 failed
   CAVEAT: truth.json generated_at_commit = c4b9e28-dirty (not f03d414) — the 1952 figure is
   carried forward, not re-measured at this exact commit.
```

**Clean-Linux column — why it is empty:** the only clean-VM path on this machine is
**Windows Sandbox** (present; used for the committed 2026-05-22 Studio proof — Windows-only).
Hyper-V `vmms` is not installed; multipass and VirtualBox are absent; the Docker daemon is
stopped. There is no UTM/Debian/Linux-VM path from here today, so clean-Linux remains
**not proven by this machine** — by environment limitation, not by failure.

## Task 2 — VSIX Naming and Republish Options Matrix

**Fact base** (worktree @ f03d414 + one live read-only REST check): the published v0.8.1
release carries `garnet-0.7.0-lsp-mvp-{darwin-arm64,linux-x64}.vsix` — the only stale-named
assets on an otherwise 0.8.1 release; no win32 VSIX; **no SHA256SUMS entries and no signed
coverage for either VSIX** (`GARNET_SIGNED_RELEASE_LANES.md` contains zero VSIX mentions).
RB-0d landed the in-tree re-sync (`editors/vscode/package.json` → 0.8.1, publisher
`island-dev-crew`), so the packaging script + CI now emit `garnet-0.8.1-lsp-mvp-<target>.vsix`;
the staged-artifact/escalation half of RB-0d is not evidenced in this repo snapshot (likely
Mac-lane local). CI's matrix is ubuntu+macos only — **no win32-x64 VSIX has ever been
produced by CI**. Marketplace/OpenVSX: never published; blocked on `OVSX_TOKEN`/`VSCE_PAT`
and Jon's account/authorship decisions; `island-dev-crew` is an unclaimed namespace assumption.

**New machine-local finding that changes the calculus:** VS Code 1.116.0 on win32-x64
**accepted and installed** `garnet-0.7.0-lsp-mvp-linux-x64.vsix` (test extension uninstalled
immediately after). Inspection of `extension.vsixmanifest` shows **no `TargetPlatform`
attribute** — the VSIX is platform-agnostic and "linux-x64" is only a filename suffix.
Neither the npm `package` script nor `scripts/package_garnet_vscode_extension.sh` passes
`vsce --target`. Consequence: filename conventions alone gate nothing; a wrongly-platformed
install simply ships a non-executable `garnet-lsp` binary.

| Option | What it is | Cost | Risk | RB-0d staged re-pack implications |
|---|---|---|---|---|
| **A · Historical-keep** | Leave 0.7.0-named assets as-is; document them as historical | none | Mixed-version assets on the flagship *signed* release contradict the "deterministic, signed, verifiable" story (Air fleet report flags this as launch risk); VSIX stays outside signed coverage; untargeted-install hazard persists | RB-0d prep work shelved; drift item A3 stays open |
| **B · Rename-in-place** | Rename existing assets to 0.8.1 names without rebuilding | trivial | **Worst option** — the packages' internal manifests say 0.7.0; renaming makes filenames lie about content, inverting the truth-drift the band exists to fix | Contradicts RB-0d (which rebuilds from the release toolchain) |
| **C · Republish (recommended)** | RB-0d path: rebuild VSIX at 0.8.1 from the release toolchain, regenerate `SHA256SUMS(.asc)` to **include** the VSIX lines, swap assets — **swap executed by Jon, never autonomously** | moderate (rebuild + re-sign + swap) | Changing assets on a published release; mitigated by regenerated signed sums, a release-notes provenance note, and archiving the originals (their hashes are recorded above: `16d31c50…`, `60f846a1…`) | This *is* RB-0d; NUC contributes the new win32-x64 target per S173 (no duplicate re-pack of mac/linux) |

**Recommendation (evidence-review, prepare-only): Option C**, with three technical riders:

1. **Stamp `targetPlatform` properly** — pass `vsce package --target <platform>` per target,
   so platform identity lives in VSIX metadata, not just filenames (directly fixes the
   untargeted-install finding).
2. **Naming: keep the CI-emitted pattern `garnet-0.8.1-lsp-mvp-<target>.vsix`** rather than
   S173's proposed `garnet-lsp-0.8.1-<target>.vsix` — the current scripts and CI already emit
   it, and switching patterns would require CI edits, which are Jon-gated and unnecessary.
3. **Bring VSIX inside the signed story** — regenerated `SHA256SUMS(.asc)` must cover the
   VSIX assets, and `GARNET_SIGNED_RELEASE_LANES.md` should gain a VSIX row (doc change,
   normal PR lane, not this branch).

The asset swap on the published v0.8.1 release remains **Jon-owned, always** (W_REBUILD_SPEC
ownership table). Nothing in this lane touched any release asset.

## Task 3 — Package-Everywhere Feasibility (drafts authored; nothing published)

All drafts live in `F_Project_Management/DISTRIBUTION_DRAFTS/` on this branch. Validation
performed on this machine today:

```powershell
winget validate --manifest ...\DISTRIBUTION_DRAFTS\winget\IslandDevCrew.Garnet\0.8.1
# Manifest validation succeeded.                       (winget v1.28.240)
ConvertFrom-Json scoop\garnet.json                     # JSON OK (version=0.8.1, bin=garnet.exe,garnet-lsp.exe)
ConvertFrom-Json docker\devcontainer.json              # JSON OK
```

| Channel | Draft state | Blocking dependency | Notes |
|---|---|---|---|
| winget | 3-file manifest set, **syntax-validated** | **No Windows asset on v0.8.1** — `InstallerUrl`/`InstallerSha256` are loud placeholders for the planned `garnet-0.8.1-x86_64-pc-windows-msvc.zip` | zip + nested-portable layout, aliases `garnet`/`garnet-lsp`; winget-pkgs submission Jon-owned |
| scoop | manifest, JSON-validated | same Windows-asset blocker | autoupdate wired to future `SHA256SUMS` lines; scoop itself absent on this NUC (install transcript deferred to the clean-machine pass) |
| Chocolatey | feasibility memo | same + moderation pipeline + maintainer commitment | **recommend defer** until winget+scoop land; same zip serves it later |
| Docker | **real Dockerfile** — pins the released `.deb` by its verified official SHA256 (`ca35ebf8…`) | daemon stopped on this NUC (`docker info`: cannot open `//./pipe/dockerDesktopLinuxEngine`) | buildable today on any daemon-equipped machine; container proof = Linux-userspace portability evidence, never a sandbox claim |
| devcontainer | JSON-validated, consumes the Dockerfile | same daemon note | |
| Clean-machine evidence | per-channel checklist committed (`CLEAN_MACHINE_EVIDENCE_CHECKLIST.md`) | — | universal bar: provisioning record, OS identity, hash+signature pre-verification, transcript bundle, functional smoke, uninstall, claim boundaries |

**The single unlock for the whole Windows column is the S167 zip asset** (`garnet.exe`,
`garnet-lsp.exe`, LICENSE, README + SHA256SUMS entry). Until it exists, winget/scoop/choco
drafts are syntax-complete but un-installable and un-submittable — and per hard stops,
producing/attaching it is implementation work outside this evidence lane.

## Task 4 — Tauri Studio State on this Machine

**Build state: healthy.** Full end-to-end build off current main succeeded today in the
isolated worktree (no contact with the MAIN checkout's historical artifacts):

```text
npm ci                  → 18 packages, 0 vulnerabilities (node v22.22.2, npm 10.9.7)
npm run tauri build     → vite ✓ 307ms; cargo release (cold, CARGO_BUILD_JOBS=4) 3m38s;
                          makensis ran from cached Tauri tooling (no download this run)
Produced: garnet-dist-wt\target\release\bundle\nsis\Garnet Studio_0.1.0_x64-setup.exe
          1,924,051 bytes · SHA256 ADA58FA117BEC0A8035A5E697B710889C012540506AEFD790A01873B2CABF98B
Isolation verified: historical installer in MAIN (1,905,569 bytes, 2026-05-22, referenced by
          the committed clean-VM proof) untouched.
```

**What blocks a valid Windows installer proof (in order):**

1. **Version truth** — `tauri.conf.json` still says `0.1.0` (productName "Garnet Studio",
   identifier `dev.islandcrew.garnet.studio`, crate `garnet-studio` 0.1.0). A 2026 installer
   stamped 0.1.0 on a 0.8.1 product fails the claim-boundary bar before any VM is booted.
   The fix belongs with the RB-0a truth surface (version sourced from `truth.json`/workspace,
   not hand-stamped) — a small slice, but **implementation, hence out of this lane**.
2. **Re-proof at the synced version** — the committed clean-VM proof (2026-05-22, Windows
   Sandbox, installer SHA `e0dd3a16…`) is valid for the 0.1.0 artifact only; a fresh
   Sandbox pass per the committed runbook is needed for any new installer.
3. **Signing (deferred/Jon)** — unsigned NSIS means SmartScreen friction; record the
   Sandbox's verbatim SmartScreen behavior as evidence for that decision. NSIS-only today
   (`bundle.targets=["nsis"]`; WiX upgradeCode present but MSI not in targets).

**Shortest path to a valid proof** (one slice + one evidence pass): sync the version stamp →
rebuild (3m38s cold, faster warm — proven today) → hash → Windows Sandbox run per
`GARNET_WINDOWS_STUDIO_CLEAN_VM_SMOKE_2026_05_21.md` → transcript + screenshot + checklist
from `DISTRIBUTION_DRAFTS/CLEAN_MACHINE_EVIDENCE_CHECKLIST.md` ("Windows installer" section).
Windows Sandbox is confirmed present on this machine; total estimated wall time ≈ 1 hour.

## Counts, claim boundaries, and machine-local inventory

**Proven today (native Windows, machine-local): 15** evidence rows (N1–N5, W-validation of
3 manifests counted once each [winget/scoop/devcontainer], A-rows deb/rpm/SBOM/GPG, G-rows
contracts/readiness/diff-check, Tauri build). **Portability-only (WSL): 4** rows (deb install,
version, check, install-state). **Not proven: 10** — clean-Linux anything (no VM path),
Linux desktop GUI, Windows release asset, signed Windows installer, winget/scoop install,
Docker image build (daemon down), win32-x64 VSIX target, Marketplace/OpenVSX publication,
macOS tarball local verification, OS-sandbox enforcement on any platform (no deterministic
trap exercised this pass; WSL categorically cannot host that proof).

**This report proves:** the facts in the cells above, on this machine, on 2026-06-11.
**It does not prove:** release-grade Windows/Linux distribution (no Windows asset exists);
clean-machine installs on any channel; reproducible builds across machines; any enforcement
claim; anything about production or v1.0. No red-team framing is used anywhere in this lane;
all verification here is evidence review against committed truth.

**Machine-local artifacts created this pass (not committed):** evidence worktree
`garnet-dist-wt` (detached @ f03d414, plus this branch); staging dir `dist-staging-20260611\`
(7 verified release assets + `domain-matrix-v081-release\` bundle); fresh
`garnet\target\release\garnet.exe` (0.8.1); worktree Tauri bundle (hash above); WSL Ubuntu now
has `garnet 0.8.1-1` installed at `/usr/bin/garnet`. Known follow-up for the next NUC session:
the MAIN checkout's untracked `F_Project_Management\FLEET_REPORTS\` copies now duplicate
committed files and will block a plain `git merge --ff-only origin/main` until moved aside.

## Recommended next commands (post-band-approval, in order)

```powershell
# S167 asset production (implementation lane, not this one):
cargo build --release -p garnet-cli; cargo build --release -p garnet-lsp
Compress-Archive garnet.exe, garnet-lsp.exe, LICENSE -DestinationPath garnet-0.8.1-x86_64-pc-windows-msvc.zip
Get-FileHash -Algorithm SHA256 .\garnet-0.8.1-x86_64-pc-windows-msvc.zip   # → SHA256SUMS regeneration (Jon-gated release surface)
# Then, evidence passes per DISTRIBUTION_DRAFTS\CLEAN_MACHINE_EVIDENCE_CHECKLIST.md:
winget validate --manifest <real-hash manifest>; winget install --manifest … (Windows Sandbox)
scoop install <local garnet.json> (Windows Sandbox, fresh scoop)
docker build -t garnet:0.8.1 F_Project_Management\DISTRIBUTION_DRAFTS\docker  (any daemon-equipped machine)
bash scripts/package_garnet_vscode_extension.sh  (on this NUC → first-ever win32-x64 VSIX; add --target rider from Task 2)
```

---

*Windows NUC Claude lane (Fable 5), 2026-06-11. Evidence pass only: no Rust crate edits, no
PRs, no tags, no releases, no registry submissions, no asset changes, no CI/gate edits, no
enforcement claims. Branch `aux/2026-06-11-windows-nuc-claude-distribution`; no PR opened.*
