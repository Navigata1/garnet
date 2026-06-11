# Threat-Wall Narrative — Refresh (DRAFT)

> **Status:** Internal draft for RB-0 / website later. Nothing here is posted copy, public claim, or marketing. Calibrated-honesty discipline applies throughout: capability verbs are "designed to" / "intended to" / "would"; the word *enforced* appears only where a deterministic trap proves it.
>
> **Discipline note (must remain visible wherever this ships):** *Quotes describe the problem; no quoted person endorses Garnet.* The builders cited below have never heard of Garnet. Quoting them characterizes the field's open problem — it does not claim their support.
>
> Ground truth: Garnet is a **research-grade prototype**, latest tag **v0.8.1**. **Not production. Not v1.0.** The only surface proven by a trap on both backends (interpreter + VM) is **`@caps` + `@max_depth`**; everything else described as a mechanism below is **declared, not enforced**, and is a *design*, not a shipped runtime.

---

## The wall: every language solves execution; none solves acceptance

For fifty years, language design has answered one question — *will this code run correctly?* Types, borrow checkers, effect systems, test harnesses: all instruments for **execution** trust. They assume a human wrote the code, a human will read the diff, and a human will decide to accept it.

That assumption is breaking in 2026. Code now arrives faster than anyone can validate it, and the bottleneck has moved from *writing* to **accepting**. No language addresses acceptance. That is the gap Garnet is designed for: the moment code arrives faster than trust.

The builders of the languages we use today — none of whom know Garnet exists — have, independently, described this exact wall.

### The change you can't localize

Bjarne Stroustrup (C++), on regulated software in the AI era:

> "When a human makes a change it's localized and you can look for the effects. If an AI writes it, you don't actually know where it's changed."

He observes that senior developers in regulated fields are **retiring rather than validate AI-generated churn** — the cost of re-validating code that the tooling can rewrite wholesale on a slightly different prompt has exceeded what the people qualified to do it will absorb.

The textual diff is enormous and unlocalizable. But the **authority-and-bounds diff is machine-computable and small.** Garnet's `diff-caps` is designed as exactly that localization instrument: when the prose changes by ten thousand lines, the *capability surface* and *declared ceilings* either changed or they did not, and the change — if any — fits on one screen. (Today `diff-caps` operates over the `@caps` surface that is trap-proven; the envelope-comparison and budget-lattice extensions described in the reassessment are **post-v0.8.2 designs**, not shipped.)

### The hyperscaler already drew the line

Via DHH (Ruby on Rails / 37signals), reporting Amazon's internal conclusion after a major outage:

> Amazon "can no longer let junior programmers ship agent-generated code to production without review."

This is the acceptance crisis stated at hyperscaler scale. The reflexive remedy — *a senior must review everything* — does not scale to agent velocity; it re-creates the bottleneck under a new name. Garnet's intended answer is to package a slice of that senior review judgment into a **deterministic gate**, so that what a senior would check by eye becomes a check the author cannot fake or skip.

### Software with no human at the screen needs compile-time evidence

Simon Peyton Jones (Haskell / GHC), explaining why Stroustrup reached for static typing in the first place: a telephone switch "can't drop into a debugger." Software operated unattended cannot be rescued by a human reading a stack trace at 3 a.m.

> **The agent is the telephone switch.**

An autonomous agent is permanently unattended software. It is precisely the case that needs **compile-time evidence**, not runtime archaeology after the loss. "**Copilots need pilots**" (the framing carried in the same corpus) names the near term — a human still holds the controls. The telephone-switch case names where it's going — no human at the screen at all. Both want the same thing: evidence that travels *with* the artifact, available before it runs.

### The senior-multiplier: amortize judgment, don't replace it

Garnet does not claim to replace senior judgment — it is **designed to amortize** it. **One senior defines the envelope once** — which capabilities are permitted, which ceilings bind — and the gate applies that single judgment to every junior commit and every agent run thereafter. The expensive human decision is made one time and spent many times. This is the multiplier the field is reaching for when seniors become the only validators left: not more seniors, but more leverage per senior.

---

## The through-line

Other languages make code *run*. None of them make code **accepted**. Stroustrup names the un-localizable change; Amazon (via DHH) names the production line juniors and agents can no longer cross unattended; Peyton Jones names the unattended-software case that compile-time evidence exists to serve. They are describing one wall from four angles — the wall that goes up the moment code arrives faster than trust.

Garnet is the language designed for that moment. Its capability surface and declared bounds are intended to be the evidence acceptance needs: a small, machine-checkable diff where the textual diff is hopeless, a gate that carries one senior's judgment across every author after them, and — where a trap proves it (`@caps` + `@max_depth`, both backends) — a guarantee the author cannot fake.

> *Quotes describe the problem; no quoted person endorses Garnet.*

The resolution is one sentence:

> ## No authority without evidence.
