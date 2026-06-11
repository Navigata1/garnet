**STATUS: DESIGN ONLY. This package has NOT been run. S114 remains self-verified, not independently verified. This document does not predict the outcome of re-verification.**

---

# S114 Independent Re-Verification Package (Design)

A design for an external lane to *independently re-verify* the S114 kernel red-team finding on Garnet **v0.8.1** (research-grade prototype; NOT production / NOT v1.0). This document specifies **what to probe, what to run, and how it would be graded** if and when an independent lane executes it. It is calibrated to a single hard rule: the design lane (this document) **may not run, grade, or predict** the re-verification. S114's `self-verified — NOT independently verified` label (`CURRENT_STATE.md:15-16`) is **unchanged** by this document.

> Calibration note used throughout: "**enforced**" is reserved for a proven trap on **both** backends (interpreter + VM). For S114 the only enforced ceilings in scope are the runtime `@caps` host-authority trap (fs/net/env/proc) and the `@max_depth` recursion trap. The static gates they feed (diff-caps widening gate, agent-loop acceptance gate, static `check` caps-coverage) are static checks built on that enforced surface, not traps; the Linux-only seccomp policy is an OS-sandbox *application*, not an enforced trap. None of these four is itself "enforced" in the proven-trap sense. Everything else named here is **declared-not-enforced** or a **stub**, and is labeled as such.

---

## 1. Scope statement

### 1.1 What S114 claimed (the artifact under re-verification)

Source of record: `C_Language_Specification/GARNET_RED_TEAM.md`, the fix in `garnet-check-v0.3/src/capability_surface.rs`, and the static gate `scripts/garnet_red_team_status.py`.

- **One HIGH finding, found and fixed — impl-method capability-surface blindness.** `capability_surface()` previously scanned only top-level `Item::Fn` and skipped `Item::Impl` methods, while the interpreter (`eval.rs`) enforces `@caps` on *any* managed `FnDef`, including impl methods. Net effect (claimed reproduced end-to-end on both backends): an `@caps(fs)` impl method that reads a file was load-bearing and enforced at runtime, yet contributed **nothing** to the surface that `diff-caps`, the seal `capability_manifest`, the caps-log, and `sandbox` consume — so a proposal adding real file-read authority via an impl method passed `diff-caps` as "no authority expansion, band 5/5" (exit 0) and `agent-loop` **ACCEPTED + SEALED** it with `aggregate:[]`.
- **The fix** (`garnet-check-v0.3/src/capability_surface.rs`, function `collect_cap_fns`): recurse into `Item::Impl(block).methods` and into nested `Item::Module(m).items`. After the fix, `garnet caps` reports `aggregate:["fs"]` (`Reader::read:["fs"]`), `diff-caps` flags `+ caps GAINED: fs` / AUTHORITY EXPANDED (exit 1), and `agent-loop` REJECTS at stage diff-caps, never sealing. **Regression tests:** `impl_method_caps_are_in_the_surface`, `nested_module_fn_caps_are_in_the_surface` (both in `capability_surface.rs`).
- **Two LOW findings recorded OPEN** (within honest stub scope):
  - **LOW #1 — caps-log tail forgery.** `verify_log` (`garnet-cli/src/cmd/caps_log.rs:161`) checks only the `prev_blake3` forward link and never re-derives `caps_blake3` from `caps`; the tail has no successor committing to its hash, so a rewritten most-recent entry (plus a bogus `caps_blake3`) still prints "chain intact … (append-only)" (exit 0). Non-tail tampering **is** caught (CHAIN BROKEN). The module self-declares a *local hash-chained stub — no signed tree head, no witness*.
  - **LOW #2 — seal subject-digest is capability-blind.** `stable_ast_repr` (`garnet-cli/src/manifest.rs:413`), which feeds the seal `subject.digest` (`garnet-cli/src/seal.rs`), omits `@caps`, so `@caps(fs)` and `@caps(fs,net,proc)` share an identical subject digest. **Documented mitigation:** the predicate embeds a differing `source_blake3` + `capability_manifest`, so a signature over the predicate is not fooled — only a consumer keying provenance off the canonical subject digest is at risk.

### 1.2 What "self-verified" means TODAY — and why it is structurally not independent

S114 was **self-found** (Garnet's own red-team constructed the attacks), **self-fixed** (the same lane authored the `collect_cap_fns` recursion), and **self-graded** — the standing assertion of correctness is `scripts/garnet_red_team_status.py`, which the *same* program/lane wrote and runs. That gate is a **string-presence check over the author's own artifacts**: it asserts `report_present`, `high_hole_fixed` (by grepping `Item::Impl(block)` + `block.methods` + `Item::Module(m) => collect_cap_fns` in `capability_surface.rs`), `regression_tests_present` (by grepping the two test names), `low_holes_recorded`, `held_and_deferred_recorded`, and `honesty_anchor_present` in `GARNET_RED_TEAM.md`.

This is honest and useful as a **non-regression tripwire** — but it is **not independence**, for three structural reasons:

1. **Author = grader.** The lane that wrote the fix and the report also wrote and runs the gate. There is no party whose interests differ from the author's.
2. **The gate checks presence, not adequacy.** It confirms the fix *strings* and the test *names* exist; it does not re-derive the HIGH from first principles, does not run a fresh adversary, and cannot discover a sibling of the original hole. A gate that greps for `Item::Impl` says nothing about `Item::Trait`, `Item::Protocol`, or `Item::Actor`, nor about macro/FFI-introduced caps.
3. **The label already says so.** `CURRENT_STATE.md:15-16` records the finding as "self-found and self-fixed … not independently verified." This document does not change that.

### 1.3 What an independent re-verification must DEMONSTRATE (not "pass")

The deliverable of an independent run is a **demonstration with preserved artifacts**, not a verdict that the package "passed." Specifically, an independent lane must:

1. **Reproduce the original HIGH from first principles** — independently author a malicious `.garnet` whose impl method holds real authority (fs/net) and show (on the *pre-fix* surface logic, or by reasoning the lane reconstructs itself) the surface reported empty and the gates were fooled.
2. **Confirm the fix closes that specific hole** — show the *post-fix* surface, diff-caps, and agent-loop now see and reject the impl-method widening, on **both** backends.
3. **Attempt NEW escapes of the capability surface** — not re-run the author's two tests, but adversarially seek *siblings* of the original hole (trait/protocol/actor variants, nested-impl, macro/codegen, FFI) that the fix may not have covered.
4. **Adjudicate the two open LOWs** — independently reproduce (or fail to reproduce) the caps-log tail forgery and the capability-blind seal digest, and record the adjudication against pre-registered criteria.

"Demonstrate" is deliberate. The independent lane records *what it observed*, with raw logs; it does not pronounce S114 "verified." Promotion of the label is a separate, human (Jon/lead) decision made **after** reading the preserved artifacts.

---

## 2. Attack-surface map — the capability-surface trust boundary

The trust boundary an external red-team must probe is: **"every place an enforced `@caps` authority can live must appear in `capability_surface()`'s output, so that diff-caps, the seal manifest, the caps-log, and the agent-loop gate all see it."** Each row below names the claim, the repo location, and the specific escape to attempt. Rows are ordered HIGH-region first, then the two open LOWs.

| # | Boundary element | Claim under test | Repo location | Escape an attacker attempts |
|---|---|---|---|---|
| A1 | **Impl-method caps** (the fixed HIGH) | An `@caps(...)` impl method appears in the surface aggregate + per-function | `garnet-check-v0.3/src/capability_surface.rs` `collect_cap_fns` → `Item::Impl(block).methods` | Author an impl method that reads a file / opens net; verify surface contains it and diff-caps/agent-loop reject the widening on **both** backends. |
| A2 | **Nested-module caps** | A `@caps(...)` fn inside `module m { … }` (and deeper) appears in the surface | same file, `Item::Module(m) => collect_cap_fns(&m.items, …)` (recursive) | Nest the cap-bearing fn 2–3 modules deep, and inside a module *inside an impl region*, to test recursion depth/order. |
| A3 | **Trait / protocol method caps** | A trait/protocol method that carries enforced authority is in-surface | `Item::Trait`/`Item::Protocol` exist in `garnet-parser-v0.3/src/ast.rs:25-26`; `collect_cap_fns` has **no arm for them** (`_ => {}`). Per AST, `TraitItem` is `FnSig`/`Const` (signature-only, **no body, no `@caps`**); trait method **bodies** live in `Item::Impl{ trait_ty: Some(_), methods }`, which **is** walked by the A1 arm. | **Confirm by construction**, do not assume: that no *managed, `@caps`-bearing body* can be reached through `Item::Trait`/`Item::Protocol` themselves; and that every trait-impl body routes through `Item::Impl`. Attempt a trait default-body / associated-fn form (if the grammar admits one) that lands authority outside `Item::Impl`. **OPEN (Jon): confirm the grammar cannot place a cap-bearing managed body directly under `Item::Trait`/`Item::Protocol`.** |
| A4 | **Actor handler caps** | Actor message handlers do not hold invisible enforced authority | `Item::Actor` exists (`ast.rs:22`); `collect_cap_fns` drops it via `_ => {}`. `HandlerDecl` (`ast.rs:267`) has **no `annotations` field** (cannot carry `@caps`); `call_actor_handler` (`eval.rs:1130`) runs `handler.body` **without** pushing a managed cap frame. So handlers are **not** an enforced-`@caps` site — *not* the S114 shape. | Probe the **indirect** path: a handler body that *calls* a cap-bearing top-level/impl fn — confirm that authority routes through a managed frame and therefore through the surface, rather than escaping via the handler. **Do not claim an actor hole** unless a managed `@caps`-bearing body is demonstrated. |
| A5 | **Macro / codegen-introduced caps** | Authority introduced by expansion is in the *post-expansion* surface | Surface is "purely syntactic" over the parsed `Module` (per `capability_surface.rs` doc comment). | Attempt to introduce a cap-bearing impl method via any macro/codegen/derive path and check whether `capability_surface()` sees pre- or post-expansion AST. **OPEN (Jon): confirm whether v0.8.1 has any macro/codegen surface at all; if none, record A5 as N/A with evidence.** |
| A6 | **FFI / extern boundary** | Authority reaching the host via FFI is surfaced or trapped | `garnet-cli/tests/ffi_authority.rs` exists (FFI + diff-caps interplay). | Author an FFI/extern call that reaches host fs/net and check whether its authority appears in the surface or is otherwise gated; compare against `ffi_authority.rs` expectations. **OPEN (Jon): name the canonical FFI authority fixture for the external lane.** |
| L1 | **Caps/transparency-log tail** (open LOW #1) | `caps-log --verify` detects tampering | `garnet-cli/src/cmd/caps_log.rs:161` `verify_log` — checks `prev_blake3` only, never re-derives `caps_blake3` from `caps`. | Append entries, then rewrite the **tail** entry's `caps` + `caps_blake3` and run `--verify`; the claim under test is that it still prints "chain intact … (append-only)" (exit 0). Then tamper a **non-tail** entry and confirm CHAIN BROKEN is raised. |
| L2 | **Seal subject-digest** (open LOW #2) | The seal binds the capability surface | `garnet-cli/src/seal.rs` subject digest = `stable_ast_repr` (`garnet-cli/src/manifest.rs:413`), which omits `@caps`. | Seal two programs identical except `@caps(fs)` vs `@caps(fs,net,proc)`; the claim under test is that the **subject digest is identical** while the predicate's `source_blake3` + `capability_manifest` differ. Then test a consumer that keys off the subject digest alone. |

---

## 3. Reproduction harness inventory (checklist for a stranger)

Everything below is written so an external lane can execute it **without author hand-holding**. Items that do not yet exist as a turnkey harness are marked **OPEN (Jon): harness must be built** — the external lane must not silently improvise them, because an improvised fixture is not pre-registered (see §4–§5).

### 3.0 Preconditions (record in provenance)
- [ ] Build v0.8.1 from the signed release or the `v0.8.1` tag; record the commit, `garnet --version`, OS, and architecture.
- [ ] Verify the release signature per `docs/release-signing.md` (key `docs/garnet-release-signing.pub.asc`, fpr `04D5 6F91 F038 17DD FFEB C62A C14D F6E7 1395 6ED1`). Record the verification output.
- [ ] Confirm the runner identity is **neither this design lane nor the build lane** (see §5).

### 3.1 Static gate (exists)
- [ ] Run `python3 scripts/garnet_red_team_status.py --format json` and capture stdout.
- [ ] Run `python3 scripts/garnet_red_team_status.py --gate; echo "exit=$?"` and capture both.
- [ ] Record this as a **tripwire reference only** — it is the *author's* self-grade. The independent grade is the §4 table, not this script's `ok` field. Note explicitly in the log that a green gate here is **not** independent verification.

### 3.2 Regression tests (exist)
- [ ] Run the two named tests and capture full output:
  - `cargo test -p garnet-check-v0.3 impl_method_caps_are_in_the_surface -- --nocapture`
  - `cargo test -p garnet-check-v0.3 nested_module_fn_caps_are_in_the_surface -- --nocapture`
- [ ] Record this as **author-supplied** evidence. The independent value comes from §3.3 (fresh fixtures the lane authors itself), not from re-running the author's tests.

### 3.3 From-scratch malicious-fixture protocol (independent — the core of the re-verification)
The external lane authors its **own** `.garnet` fixtures (do not copy the test strings from `capability_surface.rs`):

- [ ] **F-fs (impl-method file read).** A struct with an impl method declaring `@caps(fs)` that reads a file; `main` declares `@caps()`. Run `garnet caps` (both `--interp` and `--vm`); record the `aggregate` and per-function output.
- [ ] **F-net (impl-method net).** Same shape with `@caps(net)` opening a socket. Record surface output.
- [ ] **F-diff (widening proposal).** A "before" with the cap-bearing impl method **absent/sealed clean** and an "after" that **adds** it; run `garnet diff-caps` and `garnet agent-loop` (both backends); record exit codes and whether agent-loop SEALS or REJECTS at stage diff-caps.
- [ ] **F-nest (deep module).** F-fs's cap-bearing fn moved 2–3 modules deep; record surface.
- [ ] **F-trait / F-actor (sibling probes, A3/A4).** Attempt to land enforced authority via a trait-impl body and via an actor-handler→cap-fn call; record whether the authority appears in the surface. **If the grammar refuses to compile the construct, record the compiler error as the evidence** (a construct that cannot exist is not a hole).
- [ ] **OPEN (Jon): harness must be built** — a *pre-fix oracle*. To "reproduce the original HIGH from first principles" (§1.3.1) on a fixed binary, the lane needs a way to observe the pre-fix behavior: either a pinned pre-fix build/commit, or a documented reconstruction of the pre-fix `collect_cap_fns` (top-level-only) the lane runs against F-fs. Specify which, and pin the commit, before the attempt.

### 3.4 Seal / log tamper protocol for the two LOWs (independent)
- [ ] **L1 caps-log tail forgery.** Build a multi-entry log with `garnet caps-log` over a sequence of programs; run `garnet caps-log --verify` (capture "chain intact" baseline). Edit the **tail** entry's `caps` + `caps_blake3` in place; re-run `--verify`; record output + exit. Edit a **non-tail** entry; re-run; record output + exit (expect CHAIN BROKEN). **OPEN (Jon): harness must be built** — a small scripted log-tamper helper (or exact manual byte-edit instructions) so the edit is reproducible across runners.
- [ ] **L2 capability-blind seal digest.** Seal `prog_a` (`@caps(fs)`) and `prog_b` (`@caps(fs,net,proc)`), otherwise byte-identical; run `garnet seal` on each; extract and compare the `subject.digest.blake3`, the `source_blake3`, and the `capability_manifest`. Record whether the subject digests match while the predicate fields differ. **OPEN (Jon): harness must be built** — the exact `garnet seal` invocation + a jq/grep extractor for the three fields, committed as a fixture.

### 3.5 HELD-vector spot-checks (independent confirmation the fix did not regress the kernel)
- [ ] **proc double-gating.** Confirm laundering `proc` through an impl method while `main @caps()` still TRAPs (`requires program entry @caps(proc)`) on both backends — i.e., the A1 fix did not weaken the `proc` double-gate (`require_capability` + `require_entry_capability`).
- [ ] **max_depth.** Confirm `@max_depth` self-recursion traps at depth N+1 on both backends; out-of-range `@max_depth(9999)` rejected.
- [ ] **diff-caps top-level + signed-manifest reattach.** Confirm top-level widening still → AUTHORITY EXPANDED (exit 1) and a manifest reattached to different source FAILs `source_hash`.

---

## 4. Pre-registered pass/fail criteria (Paper-VI style — written BEFORE the attempt)

This table is **committed before the independent run begins** (§5). Each row is a falsifiable prediction with an explicit FAIL condition. **This document does not state which way any row resolves** — the independent lane fills the Observed/Result columns from raw artifacts.

| ID | Prediction (the property the lane will test) | FAIL condition | Observed (filled by independent lane) | Result |
|----|---|---|---|---|
| PRED-1 | A `.garnet` impl method declaring `@caps(fs)` and reading a file produces a `capability_surface` whose `aggregate` contains `fs` and whose per-function list contains `Reader::read:["fs"]` (or the lane's analog name). | `fs` absent from `aggregate`, **or** the impl method absent from per-function. | _____ | _____ |
| PRED-2 | Same fixture on `--interp` and `--vm` yields the **same** surface. | Surfaces differ between backends. | _____ | _____ |
| PRED-3 | A widening proposal that adds the cap-bearing impl method makes `diff-caps` report AUTHORITY EXPANDED (exit 1). | diff-caps reports no expansion / exit 0. | _____ | _____ |
| PRED-4 | `agent-loop` on that widening REJECTS at stage diff-caps and emits **no seal**. | agent-loop ACCEPTS or SEALS the widening. | _____ | _____ |
| PRED-5 | A `@caps(net)` fn nested ≥2 modules deep appears in the surface aggregate. | `net` absent. | _____ | _____ |
| PRED-6 | No construct the grammar accepts can place an **enforced, managed** `@caps`-bearing body outside the `{Item::Fn, Item::Impl, Item::Module}` walked set (i.e., no trait/protocol/actor/macro/FFI sibling of the HIGH hole). | Any accepted construct lands enforced authority that is **absent** from the surface. | _____ | _____ |
| PRED-7 (LOW #1) | `caps-log --verify` returns exit 0 / "chain intact … (append-only)" after the **tail** entry's `caps`+`caps_blake3` are rewritten. | verify detects the tail forgery (non-zero / CHAIN BROKEN). *(Detection here would mean the LOW does not reproduce — record it; do not treat either direction as the "good" outcome.)* | _____ | _____ |
| PRED-8 (LOW #1) | `caps-log --verify` returns CHAIN BROKEN when a **non-tail** entry is tampered. | verify accepts non-tail tampering. | _____ | _____ |
| PRED-9 (LOW #2) | Two programs differing only in `@caps(fs)` vs `@caps(fs,net,proc)` produce an **identical** seal `subject.digest.blake3`. | subject digests differ. | _____ | _____ |
| PRED-10 (LOW #2) | For the same pair, the predicate's `source_blake3` and `capability_manifest` **differ** (the documented mitigation). | predicate fields identical (mitigation absent). | _____ | _____ |
| PRED-11 (HELD) | `proc` laundered through an impl method while `main @caps()` still TRAPs on both backends; no subprocess spawned. | proc reaches the host without a trap on either backend. | _____ | _____ |

Grading rule (pre-registered): a row is **DEMONSTRATED** only if the Observed column is backed by a preserved raw artifact (command + full stdout/stderr + exit code + fixture hash). A row with no artifact is **NOT GRADED**, never assumed.

---

## 5. Independence protocol

### 5.1 Who MAY run it
- The runner is an **independent lane**: explicitly **not this design lane** (the author of this document) and **not the build lane** (the author of the `collect_cap_fns` fix and `GARNET_RED_TEAM.md`). The W-LAUNCH trust band (S141–S150) is designed to run reviewer + gate work on **parallel Air / NUC / independent lanes**; ECC **packages evidence and never self-grades independence**. This re-verification is intended to run on such an independent lane.
- The runner's identity (machine, lane, operator/agent token, timestamp) is recorded in provenance for every artifact.

### 5.2 How results are graded
- The independent lane grades **only against the §4 pre-registered table**, filling Observed/Result from raw artifacts. No criterion is added or altered after the run begins.
- The grader **publishes raw logs** — full command lines, stdout/stderr, exit codes, fixture file hashes, binary version/commit — **not a verdict-only summary**. A one-line "passed" is not an acceptable output; the artifacts are the output.
- Promotion of S114's label (from self-verified to independently verified) is a **separate human decision** (Jon/lead) made after reading the artifacts. The independent lane demonstrates; it does not promote.

### 5.3 How self-grading is structurally prevented
1. **Lane separation.** The design lane (this doc) and the build lane are **barred from the grading role**. Grading happens on a lane that authored neither the fix nor this package.
2. **Pre-registration before attempt.** The §4 table is **committed to the repo before** any fixture is run; the commit hash of the pre-registration is recorded in the run provenance. A criterion cannot be reverse-fitted to an observed result.
3. **Artifacts over verdicts.** The grader emits raw logs; the `garnet_red_team_status.py` `ok` flag is recorded as the *author's tripwire*, explicitly **not** as the independent grade.
4. **Provenance names the runner.** Every artifact carries the independent runner's identity and the binary's signed-release provenance, so a reader can confirm the author did not grade their own work.
5. **The design lane cannot self-grade by construction.** This document contains **no Observed/Result entries and no outcome prediction** — those columns are empty and may only be filled by the independent lane. The package is incapable of grading itself.

### 5.4 Standing statement
**Until this protocol executes on an independent lane and the §4 table is filled from preserved raw artifacts by a runner that is neither this design lane nor the build lane, S114 remains labeled `self-verified — NOT independently verified` (`CURRENT_STATE.md:15-16`). This document does not change that label and does not predict the outcome of the re-verification.**

---

## Appendix — repo anchors cited (verified read-only at main @ 8482294)

- Fix + recursion: `garnet-check-v0.3/src/capability_surface.rs` (`collect_cap_fns` → `Item::Impl(block).methods`, `Item::Module(m) => collect_cap_fns`; `_ => {}` drops `Item::Trait`/`Item::Protocol`/`Item::Actor`).
- Regression tests: `impl_method_caps_are_in_the_surface`, `nested_module_fn_caps_are_in_the_surface` (same file).
- Static gate: `scripts/garnet_red_team_status.py` (`--gate`, `RedTeamStatus`).
- Red-team report: `C_Language_Specification/GARNET_RED_TEAM.md`.
- LOW #1 caps-log: `garnet-cli/src/cmd/caps_log.rs:161` (`verify_log`).
- LOW #2 seal digest: `garnet-cli/src/seal.rs`; subject digest source `garnet-cli/src/manifest.rs:413` (`stable_ast_repr`).
- AST item variants: `garnet-parser-v0.3/src/ast.rs:18-31` (`Item` enum); `HandlerDecl` `ast.rs:267` (no `annotations`); actor dispatch `garnet-interp-v0.3/src/eval.rs:1130` (`call_actor_handler`).
- FFI fixture: `garnet-cli/tests/ffi_authority.rs`.
- Label: `CURRENT_STATE.md:15-16`. Release signing: `docs/release-signing.md`.
