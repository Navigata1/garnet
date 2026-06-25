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

## Claim boundaries
Proves: WV-1/WV-2/WV-3 traps hold on Windows; the new tier (PR-4/#413/#414/#415) and #417's gate
behave correctly on Windows; Finding B closed and re-verified; WV-4 shell smoke + WV-5 tooling, with
exact commands/outputs, on `NUCBOX_M2PRO_S / Windows 10.0.26200.8457` across `82c3e8e`→`a7f946d`. Does
**not** prove: anything about Mac/Linux beyond the WSL readiness comparison used to isolate Finding A;
a Studio-UI Playwright pass (no harness); live channel installs; clean-Linux; any OS-sandbox
enforcement. No production/1.0/tag claim. No frozen crate, gate, CI, or release asset was modified.
