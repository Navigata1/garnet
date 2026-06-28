# Fleet Report — Windows NUC Cross-OS Verification — Tier-0 Checkpoint — 2026-06-15

**Lane:** Windows NUC cross-OS verification (Claude Code, Opus 4.8, ultracode), parallel to the
MacBook Pro foundation-integrity lead. **Machine:** GMKtec NucBox M2Pro_S (`NUCBOX_M2PRO_S`),
**Windows 10.0.26200.8457**. WSL2 Ubuntu (root) at `~/garnet` (ext4).
**Commit verified against:** `origin/main` @ **`0d3c1d2`** (PR-3; WV-1/WV-3 verified at `82c3e8e`/PR-2).
Windows checkout fast-forwarded to `0d3c1d2`. **No frozen crate edited** (garnet-check/interp/vm/cli-core/xtask
are read-only on this lane). Evidence-only; OS-stamped. No authority claimed without a Windows trap.

## Tier-0 PR merge status (recon)
| PR | Merged? | Unblocks | Result |
|---|---|---|---|
| PR-1 `truth-gate fail-closed + examples-gate` (#409, e73ecc8) | ✅ merged | WV-3 | see below |
| PR-2 `test-runner entry-authority parity` (#410, 82c3e8e) | ✅ merged | WV-1 | ✅ VERIFIED |
| PR-3 `VM⇄interp block-local scope parity` (#411, 0d3c1d2) | ✅ merged | WV-2 | ✅ VERIFIED |

---

## WV-1 — test-runner entry-authority parity (PR-2) — ✅ VERIFIED on Windows
`garnet test` routes test functions through the program-entry capability frame, so a `@caps()`
test exercising undeclared host authority FAILS with the same deterministic trap `garnet run`
raises — proven on Windows, not inferred from Mac.

- **Integration test** `cargo test -p garnet-cli --test test_entry_authority` → **4/4 pass** on
  Windows (`NUCBOX_M2PRO_S`): `test_runner_enforces_entry_authority_like_run`,
  `run_rejects_undeclared_fs_at_entry`, `test_runner_allows_declared_caps`,
  `test_runner_passes_pure_computational_test`.
- **Manual probe (verbatim Windows trap):** a `@caps()` test calling `read_file` via a helper →
  `exit=1`, output:
  `test test_fs_leak ... FAILED: capability: ` + "`fs::read_file` requires @caps(fs), not declared in the calling chain"` ` ; `test result: FAILED. 0 passed; 1 failed`.
- **Note vs the slice text:** WV-1 described an "`@caps(proc)` helper"; the merged fixture uses the
  **fs** authority trap (`requires @caps(fs)`). Verified the trap as actually merged.
- **Proposed cross-OS proof-table row** (for `GARNET_CROSS_OS_REPRODUCIBILITY.md`, lead-lane to merge):
  `test-runner entry-authority parity (PR-2) | ✅ Windows (4/4 + manual trap) | (Mac per lead) | (Linux per lead) | garnet-cli/tests/test_entry_authority.rs`.

## WV-2 — VM⇄interpreter block-local scope parity (PR-3) — ✅ VERIFIED on Windows
PR-3 detects enclosing-scope `let`/`var`/`const`/`for`-var shadowing at compile time and forces
those functions onto the tree-walk fallback (the interpreter reference), with **no over-fallback**
for the common case. Proven on Windows at `0d3c1d2`:

- **Acceptance proptest** `cargo test -p garnet-vm --test scope_shadowing_parity` → **5/5 pass** on
  Windows (`NUCBOX_M2PRO_S`): `probe_program_matches_interpreter` (the historically-divergent
  `let x=1; if true { let x=2  x }; x` now agrees at `1` and lowers to fallback, not native),
  `non_shadowing_program_stays_native_and_matches`, `same_scope_rebind_stays_native_and_matches`,
  the generator meta-guard, and **`prop_vm_matches_interp_on_random_shadowing_programs` (300 random
  nested-block programs, VM output == interpreter output on every one → zero block-local leakage)**.
- **CLI-boundary probe (rebuilt @ 0d3c1d2):** on the divergent program, `garnet run --interp` → `=> 1`
  and `garnet run --vm` → `=> 1` — identical on Windows. (Pre-PR-3 the VM would have returned `2`.)

## WV-3 — truth-gate + examples-gate (PR-1)
**Examples-gate: ✅ GREEN on Windows.** All 33 `examples/*.garnet` check with **exit 0**;
PR-1's new `documented_math.garnet` → "4 functions checked, 6 boundary call sites, 0 diagnostics".
(3 `novel_*` examples emit an expected **stability advisory** for the experimental
`std::base64::encode` primitive — still exit 0, not a failure.)

**Truth-gate mechanism: ✅ works on Windows** (`truth --check` correctly fails-closed). **But the
gate is RED on Windows for a non-PR-1 reason — a confirmed Windows-only reporter divergence (see
Finding A).** `cargo run -p xtask -- truth --check` →
`docs/truth.json: truth:readiness_pct expected 92.7, found 92.8` (exit 1). truth.json's value
(92.8) is **correct** (matches the committed-proofs / Linux reading); Windows is the outlier at 92.7.

---

## FINDING A (BLOCKER — Windows-only divergence) — readiness reporter is blind to committed proof bundles on Windows
**What:** `scripts/garnet_mit_readiness_status.py` computes **`completion_percent` = 92.7 on Windows
vs 92.8 on WSL/Linux at the same commit `82c3e8e`** (truth.json = 92.8). This makes `truth.json`
non-reproducible cross-OS and fails `truth --check` on Windows only.

**Root cause (pinpointed, OS-stamped):** two evidence-scored lanes diverge —
- `windows_linux_domain_proof_matrix`: **win = 60 `source-present` `class=local`** vs
  **lin = 100 `verified` `class=committed`**. The Linux run reads the committed bundle
  `proofs/windows/domains/windows-domain-matrix-20260603-0855/garnet-studio-domain-matrix.json`;
  the Windows run reports it "found no verified `--suite all` bundle" and falls back to a
  machine-local desktop root.
- `windows_linux_distribution`: win = 74 vs lin = 71.

**Proof it is a Windows discovery bug, not local-state contamination:**
1. The committed bundle file **is present and git-tracked** in the Windows checkout (`Test-Path` = True; `git ls-tree origin/main` = yes).
2. Re-running the Windows reporter with `GARNET_STUDIO_DOMAIN_MATRIX_ROOT` pointed at a **fresh empty dir** (so no local bundle can shadow the committed one) **still** yields 60/`source-present`/`local` and overall 92.7 — i.e. Windows never reads the committed `proofs/...` bundle at all.

**Impact / why it's a blocker:** if/when `truth --check` is wired into CI (currently Jon-gated per
`xtask/src/truth.rs`), it would **fail on any Windows runner** while passing on Linux/Mac. The truth
surface is currently only reproducible on non-Windows.
**Recommended fix (reporter, `scripts/` — non-frozen; proposed, NOT applied by this lane):** make the
committed-proofs discovery for these lanes path-portable on Windows (likely a `/`-separated glob or
`Path` join that doesn't match on Windows). Verify by re-running the reporter on Windows and Linux
and confirming identical `completion_percent`. **Held as a flagged finding, not patched**, per
"prefer forcing fallback over shipping a Windows behavior that disagrees with the reference" + the
truth surface being gate-adjacent.

## FINDING B (crash-surface — cross-OS latent) — `garnet test` panics on a parse-error test file — ✅ CLOSED by #414 (Checkpoint 2)
**What:** `garnet test <dir>` **panics** — `thread 'main' panicked at garnet-cli/src/cmd/test.rs:180:18:
attempt to subtract with overflow` (exit 101) — when a discovered test file fails to parse.
Reproduced on Windows with a clean (no-BOM) file `tests/bad.garnet` containing `}` →
`parse error … UnexpectedToken { … RBrace … span { start: 0, len: 1 } }` then the panic.

**Root cause (read-only inspection of the frozen crate):** `test.rs:180` is
`let passed = total_run - total_failed;`. A test *file* that fails to parse increments
`total_failed` without incrementing `total_run`, so `0 - 1` underflows (`usize`) → debug panic /
release silent-wrap. **OS-independent integer arithmetic → cross-OS latent** (not a Windows
divergence; lead lane should confirm the Mac/Linux debug-build panic). PR-2 touched `cmd/test.rs`,
so this is adjacent to the just-merged change. **Frozen crate — recorded + flagged, not patched.**
Suggested fix for the owner: `total_run.saturating_sub(total_failed)`, or count unparseable files
separately from test pass/fail.

---

## Tier-0 complete — what's next
**All three Tier-0 fixes (PR-1/PR-2/PR-3) now verified to hold on Windows** (WV-1 ✅, WV-2 ✅,
WV-3 examples-gate ✅; WV-3 truth-gate mechanism ✅ but RED on Windows via Finding A).
- **WV-4** (Studio/app-workbench Playwright + Tauri smoke): not run this checkpoint — next loop.
- **WV-5** (Windows/Linux distribution smoke): not run this checkpoint — next loop.
  (Prior machine-local facts available: NSIS installer `Garnet Studio_0.8.1_x64-setup.exe` builds;
  `winget validate` passed on the draft manifest; no Linux hypervisor on this box → clean-Linux
  buckets stay DEFERRED, WSL = portability-only.)

---

## Checkpoint 2 — next-tier verification (origin/main @ `0ec71b2`)
Five PRs merged after the Tier-0 set; the new Foundation tier + firewall work verified on Windows
(`NUCBOX_M2PRO_S / Windows 10.0.26200.8457`), all green:

| PR | What | Windows acceptance test | Result |
|---|---|---|---|
| PR-4 #412 | capability callable-identity unification (Tier-0) | `garnet-check --test caps_callable_identity` | ✅ 4/4 |
| #413 | checked +/−/×/unary-neg integer overflow, BOTH backends (RFC-0002) | `garnet-cli --test overflow_parity` + `garnet-interp --test overflow_guards` | ✅ 6/6 + 14/14 |
| #414 (J8) | process-abort firewall on eval/repl/**test**/doctest lanes | `garnet-cli --test panic_firewall_lanes` | ✅ 6/6 |
| #415 | cycle/depth guard in `Value::display/debug` (firewall follow-up) | `garnet-cli --test cyclic_value_render` | ✅ 1/1 |

**Finding B — CLOSED by #414 (verified on Windows).** Re-ran the exact parse-error probe
(`tests/bad.garnet` = `}`) against the firewalled binary @ `0ec71b2`: **exit code 1, no panic**
(was exit 101 + `attempt to subtract with overflow`). Output now degrades cleanly to
`garnet test: parse error … UnexpectedToken { … RBrace … }` then `test result: FAILED. 0 passed;
1 failed` — the `usize` underflow is gone, the file counts as one failed unit. The firewall test's
own docstring names this exact case ("a parse-error file, which used to underflow (`usize`) and
abort the summary with exit 101"). Flagged → fixed by the lead lane → re-verified on Windows.

**Finding A — STILL OPEN.** None of #412–#416 touch `scripts/garnet_mit_readiness_status.py` or its
committed-proof discovery, so the Windows readiness divergence (92.7 Win vs 92.8 Linux; reporter
blind to committed `proofs/` bundles on Windows) persists and `truth --check` stays RED on Windows.
Carried forward for the lead lane / reporter owner.

**Still ungated for this lane (next loop):** WV-4 (no Playwright harness exists in-repo — only the
Tauri build/`--studio-smoke` is runnable; the `app_workbench` is the agentic-matrix skip toggle) and
WV-5 (winget present; scoop absent; docker daemon down; NSIS installer present). No further Tier-0/1
PRs pending verification at `0ec71b2` (#416 is a Jon-gated release-prep PR, not a runtime trap).

---

## Checkpoint 3 — #417 (truth-check CI gate) + WV-4/WV-5 smoke (origin/main @ `a7f946d`, 2026-06-25)

**#417 `wire truth --check into CI` — verified on Windows; intersects Finding A.** The new
machine-truth drift job is **`runs-on: ubuntu-latest`** (Linux only — not a Windows matrix), so the
gate runs where it is green. `docs/truth.json` was touched but `readiness_pct` stays **92.8**
(stamp still `c4b9e28-dirty`); the reporter was **not** changed. Re-ran `cargo run -p xtask -- truth
--check` on Windows @ `a7f946d` → still **RED**: `readiness_pct expected 92.7, found 92.8` (exit 1).
**Net:** Finding A's CI-break risk is correctly mitigated (Linux-only gate), but the **root reporter
divergence is unfixed** — `truth --check` is a false-RED for any Windows contributor running it
locally. **Finding A remains OPEN**, now with reduced blast radius.

**WV-4 (Studio/app-workbench) — PARTIAL on Windows.** `apps/garnet-studio` is unchanged since the
2026-06-12 build (0 commits since `9d15590`), so the committed Tauri **0.8.1** build proof stands;
`garnet-studio.exe --studio-smoke` → **exit 0** (machine-local). **The "Playwright pass over the
Studio UI" is NOT runnable — no Playwright harness exists in-repo** (`git ls-files | grep playwright`
= empty; the `app_workbench` token is only the agentic-matrix `--skip-app-workbench` toggle).
*Recommendation (fix-slice, not evidence):* add a Playwright config + a minimal Studio-UI smoke spec
so this lane can actually exercise the UI rather than just the headless shell smoke.

**WV-5 (distribution smoke, portability-labeled) — PARTIAL on Windows.** Tooling: winget v1.28.240
present (validate available); **scoop absent**; docker 29.4.3 present but **daemon DOWN** (no image
build); NSIS installer `Garnet Studio_0.8.1_x64-setup.exe` present (`07585423B286EE85…`). Draft
winget/scoop manifests were authored + `winget validate`-passed on 2026-06-11 (fork branch
`aux/2026-06-11-windows-nuc-claude-distribution`). **Deferred (honest):** live winget/scoop install
needs a clean Windows Sandbox VM; Docker/devcontainer build needs the daemon up; **clean-Linux** needs
a hypervisor — **none on this box (only Windows Sandbox)**, so clean-Linux + Linux-desktop-GUI stay
DEFERRED, WSL = portability-only. No registry submission, no asset mutation.

**Lane status @ a7f946d:** all merged Tier-0/1 runtime traps verified on Windows (WV-1/2/3, PR-4,
#413/#414/#415, #417); Finding B closed; Finding A open (CI-mitigated); WV-4/WV-5 advanced as far as
the environment allows (Playwright harness + clean VMs are the remaining blockers). No further
unverified Tier-0/1 PRs pending.

---

## Checkpoint 4 — Phase 1 of the loop: #421 deny-by-default caps mediation (origin/main @ `47a7ba7`, 2026-06-25)
Recon found 3 commits since `a7f946d`: **#421** (`47a7ba7`, deny-by-default capability mediation, Jon-approved),
**`4994867`** (S114 load-time caps + max-depth gates), and **#419** (docs-only S114 dossier). #421 closes the
exact residual fail-open the prior Codex map flagged: `4994867` installed the program-entry `@caps` frame on
run/VM/agent-loop, but `require_capability` stayed **fail-open at `active_frames == 0`**, so the host-authority
bypass survived on the `eval`/`test`/`doctest`/preload lanes; #421 makes mediation deny-by-default on every lane.

**✅ VERIFIED on Windows** (`NUCBOX_M2PRO_S / Windows 10.0.26200.8457 @ 47a7ba7`), **28/28**:
- `garnet-cli --test s114_residual_lanes` → **6/6** (the keystone: `garnet eval read_file(secret)` and a
  top-level-`let` test-file read both REFUSE with `requires @caps(fs)`; the `S114-RESIDUAL-SECRET` marker never
  reaches stdout on any lane — exfiltration blocked).
- `--test agent_loop` 10/10 · `--test bounded_enforcement` 5/5 · `--test test_entry_authority` 7/7 (extended with
  the load-time gate cases). Source changes are in frozen crates (garnet-cli/interp/vm) — run-only, not edited.
Finding A untouched (caps mediation, not the reporter) → still open. #419 is docs-only (no Windows trap).

## Checkpoint 5 — loop Phase 2: WV-4 Playwright Studio-UI harness (the WV-4 gap closed)
Built the first committed Playwright harness for the Studio UI (there was **none** in-repo despite the
agentic-matrix `app_workbench` lane existing): `apps/garnet-studio/playwright.config.ts` +
`e2e/studio-ui.spec.ts` + `@playwright/test` devDep + a `pretest:e2e` browser-install hook. It drives the
built Vite `dist` in headless Chromium and asserts the overhaul's UI structure + pure-frontend behaviour.

- **✅ 7/7 on Windows** (`NUCBOX_M2PRO_S`): splash holds→dismisses, all 8 panels present, simple-mode hides
  the power-only panels, panel switching, safety-contract copy, ≥30 tooltips, status bar version+mode. Shell
  contract gate (`test_garnet_windows_linux_studio_shell.py`) stays 7/7.
- **Adversarial review** (correctness/contract-drift/flakiness/honesty + per-finding verify): 3 confirmed
  findings APPLIED before PR — pretest auto-installs the pinned Chromium (no cold-checkout browser gap);
  `reuseExistingServer:false` + env-port (no stale-server false pass); dropped a non-existent fleet-section
  cite. Re-verified 7/7 after fixes.
- **PR [#422] open, CI CLEAN/green** (PR dogfood evidence ✓, agentic matrix ✓, machine-truth drift guard ✓,
  cargo test windows/macos/ubuntu ✓). Non-frozen `apps/garnet-studio` only; does NOT modify the gate it
  merges under (the CI e2e job is a deliberate Jon-gated follow-up, NOT added here).
- **PENDING:** the fork→IDC squash-merge needs the work-profile browser selection (asked; awaiting). The
  desktop-shell drive (tauri-driver: Run→CommandResult, evidence bundle, persisted toggle) is the flagged
  WV-4 follow-up — the Codex computer-use lane is the rigorous path for it.
  **UPDATE:** #422 was MERGED (squash, `952b3be`) — the WV-4 harness is on `origin/main`. Phase 2 complete.

## Checkpoint 6 — loop Phase 3: WV-5 distribution happy-path (evidence + honest deferrals)
| Item | Result |
|---|---|
| NSIS installer (0.8.1) | **Built + pinned** — `Garnet Studio_0.8.1_x64-setup.exe`, SHA256 `07585423B286EE85105187E9573D994973F9F4BE2022B3B04867996C7352A17C` |
| Host `--studio-smoke` | **✅ green** (exit 0, `status=passed`, `app_version=0.8.1`) — proven earlier this session on `NUCBOX_M2PRO_S` |
| winget manifest | **Validated 2026-06-11** (`winget validate` → "succeeded", BOM-free); content unchanged on fork `aux/2026-06-11-windows-nuc-claude-distribution`. Today's re-validate hit git-ref/extraction friction (the `aux/`-named branch + a PS-injected BOM), not a manifest defect. |
| Automated clean-VM install (Windows Sandbox) | **Attempted twice, DEFERRED.** A `.wsb` with a `LogonCommand` that silent-installs (`/S`) → launches `--studio-smoke` → seals the bundle to a writable mapped folder produced **no host-visible output** on either run (even a heartbeat written to the mapped root before the install never propagated). This is the well-known Windows Sandbox `LogonCommand`/mapped-write-back fragility on this box — **not** an installer defect. The rigorous clean-VM + GUI proof is **deferred to the Codex computer-use lane** (which drives the Sandbox GUI directly rather than via `LogonCommand` automation — exactly the lane scoped in `GARNET_CODEX_VALIDATION_GOALMODE`). |
| Docker image build | **DEFERRED — daemon DOWN.** The checksum-pinned Dockerfile (pins the released `.deb` by its official SHA256) is ready on the `aux` branch; the build is a quick follow-up once Docker Desktop is running. Container output would be Linux-userspace **portability** only. |
| Clean-Linux CLI / Linux-desktop-GUI | **DEFERRED** — no Linux hypervisor on this box (only Windows Sandbox, Windows-only); WSL = portability-only. |

**Net WV-5:** the installer is real + pinned and the app's smoke runs green; live channel installs and the
clean-VM/GUI/Docker/Linux proofs are honestly deferred to their right tools (Codex computer-use; a running
Docker daemon; a hypervisor) rather than faked. No registry submission, no signing, no asset mutation.

## Checkpoint 7 — loop Phase 3 RESUMED ("proceed with phase 3") — clean-Linux install proof LANDED; Docker/Sandbox diagnosed
**Stamp:** `NUCBOX_M2PRO_S / Windows 10.0.26200 / 2026-06-28`, against `origin/main` @ **`2e2fe84`**
(#423 docs-only since Checkpoint 6's `952b3be` — no Windows trap to verify). The two Checkpoint-6
deferrals (Docker, clean-Linux) were re-attempted to completion; the clean-Linux proof now PASSES.

| Item | Checkpoint 6 | Checkpoint 7 (resumed) |
|---|---|---|
| **Clean-Linux CLI install** | DEFERRED (no hypervisor; WSL=portability-only) | **✅ PROVEN** — see below |
| **Docker image build** | DEFERRED (daemon down) | **❌ BLOCKED on this box** — Docker Desktop engine non-functional (diagnosed) |
| **Automated clean-VM (Sandbox)** | DEFERRED (2 attempts, no write-back) | **❌ confirmed non-functional** — 3rd controlled failure |
| **Windows clean-VM GUI proof** | → Codex computer-use lane | unchanged — computer-use access approval **timed out (300s, no operator)** |

### ✅ Clean-Linux distribution proof — released `.deb` installs + runs on a fresh toolchain-free Debian
Docker Desktop's engine would not start on this box (see below), so the clean-environment Linux
install was proven on an **equivalent headless vehicle**: a freshly-imported `wsl --install Debian
--no-launch` distro (**Debian 13 trixie**, WSL2 kernel `6.6.87.2-microsoft-standard-WSL2`), run as
root. Same proof content as the checksum-pinned Dockerfile.

- **Distro confirmed clean pre-install:** `garnet`, `rustc`, `cargo` all **ABSENT**.
- **Released artifact, hash-verified twice:** host `Get-FileHash` and in-distro `sha256sum -c`
  both `ca35ebf881cc1d16f288f850eb767305c590112a05966c6778e5fa3d2a42e0cc` == the release pin.
- **Install:** `dpkg -i /tmp/garnet.deb` → `Setting up garnet (0.8.1-1)` with **zero extra deps**
  (proves the binary is self-contained on a stock Debian).
- **Smoke:** `garnet --version` → **exit 0**, full banner (`garnet 0.8.1`; parser/interp/vm/check/
  memory/actor-rt/stdlib/convert all reported). `dpkg -l garnet` → `ii  garnet  0.8.1-1  amd64`.
- **Scope (honest):** clean-LINUX-USERLAND proof on the **shared WSL2 kernel** — the same kernel
  caveat a Docker container carries. NOT a separate-kernel VM, NOT Windows, NOT a GUI, NOT
  OS-sandbox enforcement. Evidence: `dist-staging-20260611/debian-wv5/proof-output.txt`.

### ❌ Docker — engine non-functional on this box (diagnosed, not just "down")
Docker Desktop launches (`com.docker.backend` procs appear) then **exits within ~1 min without
starting the Linux engine**; the `docker-desktop` WSL2 distro stays `Stopped` and the
`npipe:////./pipe/dockerDesktopLinuxEngine` pipe never appears. Survived `wsl --shutdown` +
`DockerCli -SwitchLinuxEngine` + restart + a 6-min poll. This needs interactive GUI repair (which
needs the computer-use grant that timed out). The pinned Dockerfile is staged at
`dist-staging-20260611/docker-wv5/Dockerfile`; its **intent (clean-container `.deb` install) is now
satisfied by the WSL Debian proof above**, which is arguably stronger (real distro, zero-dep install).

### ❌ Sandbox automated clean-VM — write-back definitively broken here (3rd controlled failure)
A minimal diagnostic `.wsb` (writable mapped folder + a `LogonCommand` that writes only a heartbeat
+ `dir` listing) was launched against a **verified-fresh** Sandbox (all prior Sandbox procs killed →
0 confirmed → fresh launch → 2 procs confirmed). After 115 s, **no heartbeat propagated to the host**
— matching the two Checkpoint-6 failures. Conclusion: Windows Sandbox `LogonCommand`/mapped
write-back is non-functional on this machine; the automated-evidence-egress path is a dead end here.
The remaining clean-VM **GUI** proof needs computer-use to drive the Sandbox window directly, and the
`request_access` approval **timed out at 300 s** (no operator at the console) — so it stays for the
Codex computer-use lane or a user-present session. Installer remains pinned
(`07585423B286EE85105187E9573D994973F9F4BE2022B3B04867996C7352A17C`); host `--studio-smoke` green.

**Net Checkpoint 7:** WV-5's **Linux clean-environment install is now PROVEN** on the genuine
released binary; the **Windows clean-VM GUI** proof is the single honest remaining gap, with a sharp
root-cause (Sandbox write-back dead + no operator for computer-use), not a hand-wave. No frozen
crate, gate, CI, signing, registry, or release asset was touched.

## Claim boundaries
Proves: WV-1/WV-2/WV-3 traps hold on Windows; the new tier (PR-4/#413/#414/#415), #417's gate, and #421's
deny-by-default caps mediation behave correctly on Windows; Finding B closed and re-verified; WV-4 shell smoke +
WV-5 tooling, with exact commands/outputs, on `NUCBOX_M2PRO_S / Windows 10.0.26200.8457` across `82c3e8e`→`47a7ba7`. Does
**not** prove: anything about Mac/Linux beyond the WSL readiness comparison used to isolate Finding A;
a Studio-UI Playwright pass (no harness); live channel installs; clean-Linux; any OS-sandbox
enforcement. No production/1.0/tag claim. No frozen crate, gate, CI, or release asset was modified.
