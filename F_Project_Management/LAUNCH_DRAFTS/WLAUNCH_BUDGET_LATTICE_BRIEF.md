# W-LAUNCH Brief — The Budget Lattice: Metered Delegation as an Attenuating Resource Lattice

**Status: DRAFT. Not for public release. No posting, no marketing claims.**
This brief is a positioning and design document for a **post-v0.8.2** workstream.
It describes a design, not a shipped runtime. Every capability verb is calibrated:
where something is proven by a deterministic trap it says "enforced"; everywhere
else it says "designed to," "intended to," "would," or "is a design for." See the
honesty fence in §4 — it governs every sentence above it.

Positioning source: `F_Project_Management/RESEARCH/GARNET_REASSESSMENT_2026-06-11.md` §3.3.
Repo enforcement truth: `C_Language_Specification/GARNET_BOUNDED_ENFORCEMENT.md`.
Release truth: Garnet research-grade prototype, latest tag **v0.8.1** — not production, not v1.0.

---

## 1. The Unowned Problem (split exactly three ways)

The money half of agent resource control is being addressed by others, and we say
so plainly. Google's **AP2** (Agent Payments Protocol — Sept 2025, v0.2 April 2026,
60+ partners), **Stripe/Tempo MPP**, and **Coinbase x402** give agents
cryptographically signed *payment mandates*: spending limits enforced at the
**wallet / rail layer**. That perimeter is real and we should interoperate with it,
never compete with it (§3).

Three things remain unowned by anyone — these are the gap the budget lattice is
designed to fill:

1. **Non-monetary resources have no mandate layer at all.** An agent swarm's token
   spend through the org's *own* API keys, its CPU-seconds, its fan-out
   amplification, and its recursion depth are not money moving across a rail — so
   AP2-class payment mandates never see them. Runaway-swarm resource spend is, per
   the reassessment, "the FinOps incident class of 2026." There is no signed
   instrument today that says what compute and spend authority a swarm holds.

2. **Attenuation across delegation in code is unsolved as language semantics.**
   When agent A delegates to B and C, an AP2 mandate does not subdivide — the
   protocol explicitly punts agent identity and delegation to other layers.
   **Macaroons** solved attenuation for *bearer credentials* a decade ago (a holder
   can mint a strictly-narrower token without talking to the issuer), but **no
   language carries attenuation as call-graph semantics** — i.e., as a property the
   *compiler* checks about how a child's authority is carved from its parent's
   across actual delegation edges in the program.

3. **First-line "provably incapable of attempting" does not exist.** The wallet
   bounces a violating transaction *after the program has already tried it*. Nothing
   today makes the program **provably incapable of attempting** the violation in the
   first place. This is the same shape as Garnet's capability story (refuse at the
   boundary, not after the breach) applied to resources instead of authority.

**Nearest neighbors (so we never overclaim novelty):** AP2 / MPP / x402 — money
only, rail-layer only. Cloud quotas — infra-level, non-compositional, and they do
not travel with the artifact. Wasmtime fuel — a metering *mechanism* with no
mandate *semantics*.

---

## 2. The Mechanism: One Gate, Two Lattices

Garnet already has, **as language syntax**, the primitives nobody else carries:
`@max_depth`, and the *declared* bounds `@bounded`, `@fan_out`, `@mailbox` (the
spec roadmap also names a proposed `@rlm_budget` for recursive-LM token budgets).
The capability lattice already propagates through the call graph and is already
XOR-diffable via `diff-caps` (`garnet-cli/tests/diff_caps.rs`). The budget lattice
is the unification of those bound primitives into the **same shape** as caps:

- **Budgets become a resource lattice that attenuates monotonically through
  delegation.** A child's budget would be *carved from* its parent's and could
  **never exceed** it. The same invariant macaroons give to bearer tokens, expressed
  as a property the compiler checks across delegation edges: every `spawn` / delegate
  edge narrows, never widens. This is the design's core claim and it is a *design*
  claim (§4).

- **XOR-diffable exactly like `diff-caps`.** Two budget surfaces would diff to a
  small, machine-computable delta — "this revision raised the child fan-out ceiling
  from 8 to 64" — the same way the authority diff already works, even when the
  textual diff is huge.

- **Compile-checked where decidable; fuel-metered where not; sealed either way.**
  Where a budget's bound is statically decidable (e.g. a literal `@max_depth(N)`,
  or a child ceiling provably ≤ parent), the check would be at compile time. Where
  it is not decidable statically (dynamic recursion under data-dependent
  conditions, CPU-seconds), the design would lower to **runtime fuel metering** —
  the Wasmtime-fuel path the spec already names as `@bounded`'s intended lowering.
  The swarm's total resource authority would be **sealed** as an auditable artifact,
  so "what is this swarm allowed to consume" is inspectable, not reconstructed.

- **Budget-widening becomes an acceptance event in the SAME gate as
  capability-widening — one gate, two lattices.** Today the acceptance gate refuses
  a diff that widens the capability surface (a widening must fail the gate and block
  merge). Under this design, a *budget* widening — a raised ceiling, a deeper
  recursion allowance, a larger fan-out — would be a notifiable acceptance event in
  the identical gate: same accept/reject, same seal chain recording who accepted
  which widening when. Two lattices (authority and resource), one acceptance
  surface. This composition is the whole point: a reviewer (human or agent) sees one
  diff that says *both* "this change grants network write" *and* "this change raises
  the per-invocation compute ceiling 8×."

---

## 3. AP2 Interop: Wallet Enforces the Perimeter, Garnet Would Prove the Interior

AP2 is the boundary value of the lattice, not a competitor.

- **The wallet enforces the perimeter.** An AP2 mandate is the outermost ceiling on
  monetary spend, enforced cryptographically at the rail. That is exactly where it
  belongs and we keep it there.
- **Garnet would prove the interior.** Inside that perimeter, the budget lattice is
  designed to attenuate the mandate down through delegation — so a sub-agent
  would (by design) be unable to draw more than the slice of the mandate carved for
  it, *before* it tries. (Design claim only; the attenuation runtime does not exist —
  see §4. Today only `@max_depth`'s trap is enforced.) The AP2 mandate is the
  **boundary value** of the lattice; the lattice is everything strictly inside it.
- **This is interop, and the interop note belongs in the spec's future-work
  section now.** The cost today is one paragraph: an AP2-interop note in the spec's
  future-work so the design is not foreclosed. Writing it now (an `@ap2_mandate` /
  AP2-mandate-as-boundary-value stub in the future-work ledger, paired with the
  Core Ring's named "AP2-mandate type stub") keeps the lattice and AP2 composable
  by construction rather than retrofitted later. It requires nothing engineered
  before v0.8.2.

**Framing for every external conversation:** interoperate with AP2; own everything
*above the rail* (non-monetary resources) and *inside the perimeter* (attenuation
through delegation). Never position Garnet as an alternative to a payments protocol.

---

## 4. CRITICAL Honesty Fence (governs everything above)

This section is load-bearing. The repo's own enforcement doc
(`C_Language_Specification/GARNET_BOUNDED_ENFORCEMENT.md`) draws the line, and this
brief must not cross it.

- **`@max_depth` IS enforced — a real, deterministic trap on BOTH backends.** The
  interpreter (S89, `garnet-interp-v0.3/src/eval.rs`) and the bytecode VM (S99,
  `garnet-vm/src/vm.rs` `VmDepthGuard`) both trap when recursion exceeds the
  declared ceiling, at the identical depth with the identical message, proven by
  `garnet-cli/tests/bounded_enforcement.rs::vm_and_interp_traps_are_identical`.
  This is the *one* budget-shaped primitive that has earned the word "enforced."

- **`@rlm_budget`, `@fan_out`, `@bounded` are DECLARED-NOT-ENFORCED today.**
  `@bounded` (CPU / Wasmtime-fuel budget) lowers to fuel metering and **Wasmtime is
  absent** — declared, not enforced. Memory and time ceilings — declared, not
  enforced. `@mailbox` / `@fan_out` — declared, not enforced (the mailbox cap exists
  at the actor-send boundary but is not a proven trap). `@rlm_budget` is a *proposed*
  annotation named in the reassessment, not a shipped runtime control. No ceiling is
  faked: a bound is either backed by a trapping test (only `@max_depth` today) or
  labelled declared/generated.

- **The budget lattice is a DESIGN for post-v0.8.2.** Do **not** imply a metering
  runtime exists. The attenuation-through-delegation semantics, the compile-time
  checks for non-`@max_depth` budgets, the fuel-metered runtime path, and the
  one-gate-two-lattices acceptance event are all *designed* / *intended* — they are
  not running code. The only enforced piece is `@max_depth`'s trap. When this brief
  says a budget "would" attenuate or the gate "would" treat widening as an
  acceptance event, the conditional is doing real work — keep it.

---

## 5. Industries, What It Needs, and Open Questions

**Industries (from §3.3):**

- **Cloud FinOps** — attested, compositional resource authority for agent swarms
  spending through org keys (the runaway-swarm incident class).
- **AI platform teams** — per-tenant / per-invocation resource authority that
  travels with the artifact instead of living only in infra quotas.
- **Grid / data-center capacity planning** — an attested worst-case draw per
  workload, derived from sealed ceilings.
- **Sustainability reporting** — declared compute ceilings as an auditable input.
- **Agentic commerce itself** — interoperate with AP2, own everything above the
  rail; cross-references the §9 "financial/transactional agents" play (agents
  carrying AP2 mandates as typed caps, post-v0.8.2).

**What it needs (and explicitly does not need before v0.8.2):**

- The RLM / bounded guardrails already named in the spec, **generalized post-v0.8.2**
  into the budget lattice (attenuation semantics + XOR-diffable budget surface +
  the second lattice on the existing acceptance gate).
- The **AP2-interop note** as one paragraph in the spec's future-work section **now**
  (this is the only present-tense cost; it forecloses nothing and unblocks nothing
  engineered before v0.8.2).
- Sequencing dependency: rides on the existing `diff-caps` gate machinery (the
  acceptance event re-uses it) and the `@bounded` → Wasmtime-fuel lowering, so it is
  gated behind the same Wasmtime decision `@bounded` already waits on.

**OPEN (Jon):**

- OPEN (Jon): Confirm the canonical annotation name for the recursive-LM token
  budget — `@rlm_budget` appears in the reassessment but I did not find it as a
  declared annotation in the spec (`grep` for `rlm_budget` hits only the
  reassessment doc). Should the brief say "proposed `@rlm_budget`" or name an
  existing annotation?
- OPEN (Jon): Should the one-paragraph AP2-interop future-work note land in the
  language spec before v0.8.2, or wait for the W-SHIP/W-LAUNCH synthesis? §3.3 says
  "now"; confirm the target file and whether it is a Jon-owned edit.
- OPEN (Jon): Does the "one gate, two lattices" design touch the **human-merge-only**
  integrity rule? A budget-widening acceptance event modifies the gate's behavior;
  per the integrity rules a PR may not modify the gate it merges under. Confirm the
  budget lattice ships as a *new* gate dimension under human-merge governance, not a
  self-modifying threshold.
- OPEN (Jon): Whether to register the budget-lattice/AP2-interop design under the
  W-LAUNCH positioning layer or as a post-v0.8.2 engineering slice in W-SHIP (the
  reassessment §7 routes it to W-LAUNCH positioning; the engineering lands later).
