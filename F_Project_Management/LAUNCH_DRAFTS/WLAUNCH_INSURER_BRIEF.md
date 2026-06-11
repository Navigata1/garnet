# W-LAUNCH Insurer Brief: The Capability+Bounds Envelope as an Actuarial Instrument

**Status:** DRAFT — internal positioning material. No public claim, no posting, no marketing use without Jon's sign-off.
**Date:** 2026-06-11 · **Prepared for:** Jon / W-LAUNCH positioning layer (S179–S200)
**Source:** `F_Project_Management/RESEARCH/GARNET_REASSESSMENT_2026-06-11.md` §3.2; calibrated against `CURRENT_STATE.md` and the enforced/declared-not-enforced fences.
**Calibration up front:** Garnet today *enforces* only `@caps` and `@max_depth` — meaning each is proven by a deterministic trap on both the interpreter and the VM backend. Bounds and budget annotations (`@bounded` / Wasmtime fuel, `@rlm_budget`, `@fan_out`, memory, time, `@mailbox`) are **declared-not-enforced** today. The "envelope as an underwritable instrument" described below is therefore a **near-future design for a post-v0.8.2 slice, not a shipped product.** Where a claim depends on something not yet built, it is written with "designed to" / "would," and open questions are flagged `OPEN (Jon)`.

---

## 1. The gap in the forming market

An AI-agent liability insurance market is forming right now. Per the reassessment's same-day verification: **Mount (YC, 2026)** sells liability policies to companies deploying autonomous agents, and underwrites by *scanning and red-teaming the deployment, quantifying operational risk, and insuring the residual.* This is stated factually, as market evidence — Mount and its peers have never heard of Garnet, and nothing here implies they endorse it.

The structural observation is that point-in-time red-team underwriting is what you do **when there is nothing attestable to underwrite against.** The pattern repeats up the stack:

- Legacy cyber insurance prices **questionnaires** (self-attested, unverifiable).
- Agent insurance prices **red-team snapshots** (behavior-sampled, point-in-time, expensive to refresh).
- Neither has an instrument that states, verifiably and continuously, *what the insured system is capable of doing.*

The consequence shows up at claim time. When a loss occurs, liability between the model vendor, the agent operator, and the human who accepted the code is adjudicated from logs and depositions — reconstructed after the fact rather than fixed in advance. There is, today, no machine-checkable artifact that says "this system's authority was bounded *here*, and that bound was accepted by *this party* at *this time*."

That absence is the gap. The rest of this brief describes an instrument designed to fill it — and is explicit about which parts of that instrument exist today and which are post-v0.8.2 design.

---

## 2. The instrument: a sealed capability+bounds envelope

The proposal is that the insurer underwrites **the envelope, not the codebase.** An envelope is what Garnet's trust kernel is designed to emit: a capability surface (the declared authority — does it touch payments? PII? prod credentials?) plus a bounds profile (the declared ceilings) plus a sealed baseline. The actuarial mechanism, end to end:

1. **Premium priced on the declared authority surface + ceilings.** The underwriter reads the capability surface and bounds profile instead of sampling behavior. *Today's honest fence:* the capability surface is the **enforced** half — `@caps` + `@max_depth` are proven by a deterministic trap on both backends, so "this system cannot reach the network / cannot recurse past depth N" is a checkable property, not a promise. The bounds/budget ceilings (`@bounded`, `@rlm_budget`, `@fan_out`) are **declared-not-enforced** today; they are readable as *declared* risk, but pricing on them as *enforced* ceilings is part of the post-v0.8.2 design, not a current capability. `OPEN (Jon)`: which subset of the envelope a carrier would price on at first contact — likely the enforced `@caps` surface only, with bounds as declared context.

2. **Policy conditioned on the diff-caps gate staying green.** The diff-caps gate is the change-acceptance mechanism: a capability-surface *widening* is designed to fail the gate and block merge (this is one of the repo's four integrity rules — a capability-surface widening is designed to fail the gate). A live policy would be conditioned on that gate staying green for the insured artifact.

3. **Any accepted widening = a notifiable change in insured risk (automatic).** Because a widening cannot pass silently — it is an explicit acceptance event in the gate — the moment of risk-change is the same moment the gate records. The notifiable-change trigger is therefore *mechanical*, not a self-reported questionnaire update: if the authority surface grows, the insured risk has changed by construction, and the gate event is the notification artifact. This is the property legacy cyber insurance most lacks.

4. **Claims adjudicated by inside/outside-envelope.** A loss is adjudicated by a mechanical question — *was the loss-causing behavior inside or outside the attested envelope?* — rather than by reconstructing intent from logs. Inside the attested authority surface: the envelope held; the risk was the priced risk. Outside it: the authority was exceeded, which is itself a finding about *how* (a gate that should have blocked, a declared-not-enforced bound that was never a trap, an escape hatch). `OPEN (Jon)`: adjudication is only as strong as the enforced surface — a claim turning on a *declared-not-enforced* bound cannot be adjudicated as "the envelope held" today. The honest scope of inside/outside adjudication at first ship is the `@caps` + `@max_depth` surface.

5. **The seal chain as the who-accepted-which-authority-when liability firewall.** This is the property the whole agent economy is missing. The seal chain is designed to assign *who accepted which authority when* — each accepted widening is an attributed acceptance event (agent / model / gate-version are recorded on autonomous merges per the integrity rules). For an insurer, that converts liability allocation from a deposition exercise into a lookup: the chain says which party accepted the authority under which the loss occurred. `OPEN (Jon)`: binding the seal to an *operator/agent identity* claim (SPIFFE/SPIRE-class, NIST agent-identity) is named-deferred — the seal is designed to bind to such a claim where one exists, but Garnet does not invent the identity layer.

**One technical honesty note for the carrier conversation (do not paper over it):** the reassessment's appendix and the S114 trust-kernel work record that the *seal's subject digest is currently capability-blind* — a capability change need not change the digest — and a caps-log tail-forgery finding remains open (both LOW). Any instrument spec must state that the seal-binds-the-capability-surface property is a design target being hardened, not a settled guarantee. Underwriting an envelope whose seal does not yet bind the surface would be miscalibrated.

---

## 3. Why it also serves Singapore risk-bounding + EU AI Act traceability for free

The same artifact is designed to discharge two regulatory demands at no additional engineering cost — because they ask for the thing the envelope already is:

- **Singapore "risk bounding."** Per the reassessment (Gap 2), Singapore is described as shipping a national governance framework for agentic AI with *risk bounding* as a named pillar. `OPEN (Jon)`: confirm the framework's exact name, date, and "first national" / "named pillar" characterization against a primary source before any external use — ground truth here is the reassessment memo, not an independently verified fact. A sealed capability+bounds envelope is a literal, machine-checkable expression of a bounded risk surface. The standards body's vocabulary — bounding, authorization, attestation — overlaps Garnet's; the envelope is designed to be a candidate reference expression of that pillar. `OPEN (Jon)`: "converged on Garnet's vocabulary independently" overstates a vocabulary overlap as a directional finding and risks implying the standards body knows of Garnet; confirm or soften before external use.

- **EU AI Act traceability.** The Act's traceability requirements ask, in effect, *who did what under which authority.* The seal chain (§2.5) is that record by construction. Separately, the **EU Cyber Resilience Act** is the harder clock: Article 14 reporting obligations apply **from 11 September 2026** (24-hour early warning + 72-hour notification of actively exploited vulnerabilities via ENISA's Single Reporting Platform), with full obligations (SBOM, secure-by-design conformity, CE marking) from 11 December 2027, and "substantial modification" pulling legacy products into scope. *Proving a change did not substantially modify the security posture* — exactly what diff-caps-stays-green attests — has direct regulatory value, and an insurer pricing that gate is pricing a compliance signal as well as a risk signal.

The point for the carrier: the envelope is not a Garnet-only artifact requiring the world to adopt a bespoke trust format. The seal format stays a **wrapper** over in-toto / CycloneDX / GPG conventions (v0.8.1 already ships a CycloneDX SBOM + GPG-signed `SHA256SUMS.asc`). The regulatory and actuarial readers consume the same seal through different front-ends.

---

## 4. The adoption-flywheel argument

Insurance is the quiet adoption mechanism that does not require anyone to mandate a language. Nobody adopts a language because a manifesto told them to. But **insurers discount for evidence**, and a premium delta moves engineering practice harder than any advocacy:

- A carrier that can read a sealed envelope can price *lower residual uncertainty* than a carrier pricing a red-team snapshot — the envelope narrows the unknown. That is a defensible reason for a premium delta on covered, envelope-attested deployments.
- A premium delta on the order of a meaningful discount has historically moved more engineering practice than any technical argument (the reassessment's framing: "a 15% premium delta has moved more engineering practice than any manifesto" — illustrative, not a quoted carrier figure). `OPEN (Jon)`: we do not have, and must not invent, an actual carrier-quoted delta. Any number in external material must come from a real carrier conversation.
- The flywheel: insurer discounts for envelope-attested deployments → teams adopt the gate to earn the discount → the gate becomes an entitlement they will not give up → more attested artifacts in the wild → more actuarial data → tighter pricing. The instrument funds its own adoption.

This is a *positioning* argument for W-LAUNCH, not a revenue claim. The deliverable it points to is one credible carrier conversation, not a pricing model we author ourselves.

---

## 5. What it needs (and OPEN items)

**Before v0.8.2: nothing.** The trust artifact the envelope is built from already exists in the v0.8.1 line (enforced `@caps` + `@max_depth`, the diff-caps gate, sealed provenance + transparency log). This use case adds zero engineering load to the W-REBUILD sequence; its entire present-tense cost is that the kernel now knows who is waiting for it.

**After v0.8.2, two concrete artifacts:**

1. A **two-page "envelope as insurable instrument" spec** — the precise mapping from seal contents → the underwriter's inputs (priced authority surface, declared vs enforced bounds, gate-green condition, widening-as-notifiable-event, inside/outside adjudication rule, seal-chain attribution), written with the §2 honesty fences intact.
2. **One conversation with an agent-insurance carrier** (Mount-class). The goal of that conversation is to learn what a carrier would actually price on — *not* to claim they will. This brief authors no carrier endorsement and no premium number.

**OPEN (Jon) items — explicit, do not guess:**

- `OPEN (Jon)`: Which envelope subset a real carrier prices on first — almost certainly the enforced `@caps` surface, with bounds as declared context until the budget lattice is enforced (a separate post-v0.8.2 design).
- `OPEN (Jon)`: The seal-subject-digest-is-capability-blind finding and the caps-log tail-forgery finding (both LOW, open) must be resolved or explicitly disclosed before any instrument spec claims the seal binds the capability surface.
- `OPEN (Jon)`: Operator/agent-identity binding in the seal is named-deferred; the liability firewall is "who accepted which authority when" at the *gate/acceptance* layer today, not a verified runtime-operator identity.
- `OPEN (Jon)`: No carrier-quoted premium delta exists. Any figure in external material is a placeholder until a real carrier supplies one.
- `OPEN (Jon)`: Sequencing of the carrier conversation against the W-TRUST trust band (S141–S150) — an independent re-verification lane strengthens the underwritability story, but the trust band packages evidence and does not self-grade its own independence; the insurer brief must not imply that band's outcome.

---

*Calibrated-honesty reminder for anyone editing this brief: "enforced" is reserved for `@caps` + `@max_depth` (deterministic trap, both backends). Everything bounds/budget-related is "declared-not-enforced" today and must be written as "designed to" / "would." Garnet is a research-grade prototype (v0.8.1), not production / not v1.0. This is a draft; no public claim or posting without Jon's sign-off.*
