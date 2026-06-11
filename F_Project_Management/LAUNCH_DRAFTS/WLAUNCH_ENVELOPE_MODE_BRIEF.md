# W-LAUNCH Positioning Brief — Delta-Certification via `diff-caps --envelope`

**Status:** DRAFT — internal positioning material, not a public claim, not marketing copy, not a roadmap commitment. No posting.
**Prepared for:** Jon / W-LAUNCH (S179–S200) positioning layer.
**Source of record:** `F_Project_Management/RESEARCH/GARNET_REASSESSMENT_2026-06-11.md` §0, §1.5, §2 (Gap 1/2), §3.1, §4 entry #8; `CURRENT_STATE.md`; `CLAUDE.md` named-deferred fences.
**Subject:** an `--envelope` comparison mode for `garnet diff-caps`, framed as a post-v0.8.2 slice against the change-certification regimes regulators already run by hand (FDA PCCP, EU CRA, UNECE R156, DO-178C).

> **Calibration banner (read first).** Envelope mode **does not exist** in the codebase today. `garnet diff-caps` today takes two artifacts (`pub fn run(old, new)` in `garnet-cli/src/cmd/diff_caps.rs`) and reports capability widening between them; there is **no `--envelope` flag anywhere in the source** (verified: empty grep for `--envelope` across all `.rs` at `main @ 8482294`). Everything below describing envelope mode is a **DESIGN for a future slice**, written in the conditional. The only capabilities Garnet **enforces** today — the only place the word "enforced" is licensed — are `@caps` and `@max_depth`, proven by a deterministic trap on both backends. `@bounded` (Wasmtime fuel), memory, time, and `@mailbox` ceilings are **declared-not-enforced**; OS-sandbox application is Linux-seccomp-only. The bounds half of any envelope inherits those fences exactly (see §5).

---

## 1. The problem regulators already invented

Regulators did not wait for a mechanism. Across four independent safety regimes, the compliance rule is already the **same shape**: a change is permitted **if and only if it stays inside a pre-approved envelope.**

- **FDA PCCP** (Predetermined Change Control Plan; final guidance Dec 2024, Aug 2025 device-wide draft extension) lets a device maker pre-authorize a *class* of future modifications. Compliance = the change stays within the authorized plan; a change outside it triggers a full new submission.
- **EU Cyber Resilience Act** pulls a legacy product back into scope on **"substantial modification"** — so *proving a change did not substantially modify the security posture* has direct legal value.
- **UNECE R156** (automotive software-update management) and **DO-178C** (avionics change-impact analysis) encode the identical envelope-membership test for OTA updates and certified flight software.

In every one of these regimes, the envelope-membership test is performed **by humans reading documents.** That is the failure mode, and a builder who has never heard of Garnet named it precisely. Per the reassessment (§0), **Bjarne Stroustrup** described the regulated-software AI crisis verbatim:

> "There's regulatory bodies, there's validation. You have to be able to validate what you changed when you make a change… even if you make a slightly different prompt, a lot of the code will change and you have to now check it again… When a human makes a change, it's localized and you can look for the effects. If an AI writes it, you don't actually know where it's changed."

He added that senior developers in his field are **retiring rather than validate AI churn** (§0, §1.5).

> **Attribution discipline.** Stroustrup is quoted as an independent description of the *problem*. He has never heard of Garnet and does **not** endorse it. He is naming the failure mode (human-document validation cannot keep pace with AI-velocity change), not the solution.

The gap, stated plainly and verified against today's landscape (reassessment §3.1): **there is no mechanism, anywhere, that machine-verifies a code change's membership in a certified envelope.** PCCP tooling consultancies produce documents, not mechanisms; SBOM-diff tools diff inventory, not authority. The demand exists and is about to acquire a statutory deadline (§3); the instrument does not.

---

## 2. The mechanism Garnet would add (DESIGN — does not exist yet)

An envelope is, structurally, what Garnet's kernel already emits for a sealed artifact: a **capability surface** + a **bounds profile** + a **sealed baseline**. Delta-certification is then a comparison against a *certified* envelope rather than against the previous artifact.

The proposed mechanism (reassessment §3.1), **stated as a design**:

```
garnet diff-caps --envelope cert/PCCP-2026-001.envelope  →  INSIDE | OUTSIDE
```

with the exact membership semantics from §3.1. The result **would** be `INSIDE` when **all** of:

1. **authority surface ⊆ certified surface** — the change's capability surface is a subset of the certified envelope's surface (no new authority);
2. **bounds ⊆ certified ceilings** — declared bounds are within the certified ceilings (see the §5 enforcement fence — bounds are *declared* today, not enforced);
3. **intended-use caps unchanged** — the capabilities defining the device/product's intended use are identical, not merely subset-compatible.

Otherwise the result **would** be `OUTSIDE`, and the design intent is that it **emits the widening** — the specific authority or ceiling that left the envelope — so a human escalation reviews *one screen*, not the textual diff.

This is the localization instrument Stroustrup described as missing. As §3.1 frames it: the textual diff may be ten thousand agent-written lines; the *certification-relevant* diff is one screen. The design rationale for why a language is required (not a linter): the envelope must be a **compiler-derived semantic object**, not a convention an author can hand-edit — "no linter on Rust or Python can do this" (§3.1). The intended deliverable shape: **certify the envelope once with humans; verify every subsequent change mechanically.**

> **What this section is NOT claiming.**
> - It is **not** claiming envelope mode exists, is implemented, is merged, or is scheduled. It is a design for a post-v0.8.2 slice (§4).
> - It is **not** claiming the bounds-membership test is *enforced*. Membership is a **static comparison of declared bounds** against declared ceilings; today's enforcement surface is `@caps` + `@max_depth` only (§5).
> - It is **not** claiming a certified envelope confers regulatory approval. The envelope file would be an input the operator supplies; certifying it remains a human/regulator act outside Garnet.

The reassessment is explicit that diff-caps output should serve **both** a human one-glance artifact **and** a structured machine verdict (§1.6, Directive 15) — relevant here because the envelope verdict's downstream consumers (auditors, CI gates, regulator-format annexes) each need a different rendering of the same result. **OPEN(Jon):** whether the `--machine`/structured-verdict rendering of an envelope result ships in the same slice as the human verdict, or follows it, is a sequencing call, not decided here.

---

## 3. The regulatory mapping

The four regimes map onto the membership test as follows. This mapping is a **positioning argument**, not a compliance opinion (§5, OPEN items).

| Regime | The envelope object | The membership trigger | What `--envelope` would mechanize |
|---|---|---|---|
| **FDA PCCP** | The pre-authorized *class of changes* in the plan | Change outside the plan → full new submission | INSIDE = "modification contemplated by the plan"; OUTSIDE = escalate to submission |
| **EU CRA** | The certified security posture of the placed-on-market product | **"Substantial modification"** pulls a legacy product back into scope | INSIDE = the authority/bounds surface did not widen → evidence the change is **not** substantial at the capability layer |
| **UNECE R156** | The approved software-update envelope for the vehicle type | OTA update must stay within the type approval | INSIDE = the update's authority surface ⊆ approved surface before flashing |
| **DO-178C** | The change-impact-analysis baseline | Change impact must be bounded and analyzed | INSIDE = the authority+bounds delta is empty or subset; OUTSIDE = the precise delta to analyze |

**The CRA clock (verified, reassessment §2 Gap 1):** CRA **Article 14 reporting obligations apply from 11 September 2026** — 24-hour early warning and 72-hour notification of actively exploited vulnerabilities via ENISA's Single Reporting Platform — with full obligations (SBOM, secure-by-design conformity assessment, CE marking, technical documentation) from **11 December 2027**. Penalties run up to **€15M or 2.5% of global revenue.** The "substantial modification" trigger is the line that makes a machine-computable authority-and-bounds diff legally interesting: a product that can show its sealed capability surface did not widen has evidence bearing on whether a change is substantial.

The common edge across all four (§3.1): the textual diff may be huge, but the **authority+bounds diff is machine-computable and small.** That is the same property `diff-caps` is built on today, pointed at a certified baseline instead of the previous artifact.

> **Boundary.** "Evidence bearing on whether a change is substantial" is **not** "Garnet determines substantial modification." Whether an INSIDE verdict satisfies a given regulator is a legal/regulatory question (§5, OPEN). Garnet would compute the authority/bounds membership fact; the regime decides what that fact means for compliance.

---

## 4. What it requires from the roadmap

Per the reassessment (§3.1, §4 entry #8, §7), the honest answer is: **nothing new before v0.8.2.**

- **It is flagship demo #3 grown into a market.** §3.1: "It is flagship demo #3 (safety-critical trust artifact) grown into a market: the demo's artifact *is* an envelope; the only addition is an `--envelope` comparison mode on diff-caps, a natural post-v0.8.2 slice." The kernel that emits a sealed capability surface + bounds profile already exists at v0.8.1; envelope mode reuses it with a certified baseline as the comparison target.
- **The present-tense cost is zero engineering** (§7): "the three unrealized use cases require zero engineering before v0.8.2. Their entire present-tense cost is that the kernel now knows who else is waiting for it."
- **W-LAUNCH placement.** W-LAUNCH = S179–S200; the v0.8.2 launch-readiness gate sits at S191–S200, Jon-owned. The S129–S200 command center already lists envelope mode as one of three post-v0.8.2 skins in the W-LAUNCH positioning trio (envelope mode, insurer/underwriting brief, metered-delegation budget lattice). This brief is the envelope leg of that trio.
- **One mode on an existing command.** The new surface is a single `--envelope <file>` comparison mode on `diff-caps`, plus an envelope file format. `diff-caps` already takes two artifacts and reports widening; envelope mode generalizes the right-hand side from "previous artifact" to "certified ceiling/surface."

**OPEN(Jon):** the envelope **file format** (how a certified surface + ceilings + intended-use caps are serialized and sealed) is not specified in the reassessment and is not designed here. It is the one genuinely new artifact the slice introduces. Scoping it is a v0.8.2-or-later design task, not assumed solved.

**OPEN(Jon):** §3.1 lists "trap tests green" as part of an INSIDE verdict. Whether envelope mode *runs* trap tests or merely *records* their status from the sealed baseline is unspecified and affects the slice's scope. Flagging rather than guessing.

---

## 5. Honest boundaries + OPEN(Jon) items

**Enforcement fence (non-negotiable, per `CLAUDE.md` and the reassessment §3.3 honest fence).**
- The authority-surface half of the membership test rests on `@caps`, which **is** enforced (deterministic trap, both backends). The depth dimension rests on `@max_depth`, which **is** enforced (trap).
- The **bounds half is declared-not-enforced today.** `@bounded` is Wasmtime-fuel-shaped and not yet metered; memory, time, and `@mailbox` ceilings are declared-not-enforced. So "bounds ⊆ certified ceilings" is, today, a **static comparison of declared values** — it does **not** mean the runtime is metered to those ceilings. The brief must never imply the metering runtime exists.
- OS-sandbox application is **Linux-seccomp-only**; macOS/Windows OS-sandbox application is declared-not-enforced.

**Maturity fence.** Garnet is a **research-grade prototype, latest tag v0.8.1** — **not production, not v1.0.** An envelope-mode brief does not change that. Envelope mode is a design for a post-v0.8.2 slice; presenting it as shippable today would be false.

**Verb fence.** Throughout: "would," "is designed to," "the mechanism would." The word **enforced** appears in this brief only for `@caps` and `@max_depth`. Anywhere the membership test touches bounds, it is "compared," "declared," or "checked statically" — never "enforced."

**Attribution fence.** Stroustrup (and any other builder quoted in W-LAUNCH material) describes the *problem* with attribution and does **not** endorse Garnet. No quoted person may be implied to endorse the tool.

**OPEN(Jon) items:**
1. **Envelope file format** — undefined; the one new artifact (see §4). Needs a design pass; likely a sealed wrapper over the existing capability-manifest seed (`GARNET_CAPABILITY_MANIFEST_STANDARD.md`, S98), which is itself single-implementation with no external adopter.
2. **Legal sufficiency** — whether an INSIDE verdict is *accepted* as evidence by any of FDA / a CRA conformity-assessment body / a UNECE type-approval authority / a DO-178C DER is a regulatory question outside this repo. The brief claims the verdict is *computable and relevant*, not that it is *accepted*. Do not upgrade this without counsel.
3. **"Intended-use caps unchanged"** — the §3.1 criterion presumes a way to mark which capabilities define intended use vs. incidental authority. That marking does not exist in the syntax today and would need design.
4. **Trap-test handling in the verdict** — see §4 OPEN.
5. **Bounds enforcement dependency** — the bounds half of the value proposition strengthens materially if/when `@bounded` becomes fuel-enforced (the RB-6 / Wasmtime lean, Jon-gated, memo-only today). Until then, position the bounds membership test as a **declared-value comparison**, and say so.

---

### One-paragraph W-LAUNCH framing (draft, for Jon to approve or cut)

Regulators across medical devices, automotive, avionics, and now all EU software have independently converged on the same rule — a change is allowed only if it stays inside a pre-approved envelope — and today they test that membership by hand, reading documents, at a speed AI-generated change has already outrun. Garnet's kernel already emits the object that test needs: a sealed capability surface and bounds profile. The design `garnet diff-caps --envelope` **would** turn envelope membership into a one-line machine verdict — INSIDE, or OUTSIDE with the exact widening — so the envelope is certified once by humans and every later change is checked mechanically. It does not exist yet; it is a single comparison mode on a command that already ships, requiring nothing new before v0.8.2; and the only authority it can speak about with the word "enforced" is the capability surface, with bounds membership a declared-value comparison until metering lands.
