# Regulatory `--evidence`: Garnet Build Outputs → CRA / SBOM / PCCP Language

**DRAFT — internal positioning. Not a public claim, not marketing, not legal advice.**
Garnet is a research-grade prototype (latest tag `v0.8.1`), **not production / not v1.0**.
Garnet is **not a legal-compliance product**. It is designed to *emit artifacts that a
compliance process can consume* — it does not perform, attest, or guarantee conformity.

---

## Why now — the regulatory clock

- **EU Cyber Resilience Act, Article 14 reporting obligations apply from 11 September 2026.**
  24-hour early-warning + 72-hour notification of *actively exploited* vulnerabilities via
  ENISA's Single Reporting Platform; covers products already on the EU market. Fines up to
  €15M or 2.5% of global revenue. (Source: `GARNET_REASSESSMENT_2026-06-11.md` §2 Gap 1.)
- **CRA full obligations apply from 11 December 2027** — SBOM, secure-by-design conformity
  assessment, CE marking, technical documentation.
- The CRA pulls legacy products into scope on **"substantial modification."** *Proving a
  change did not substantially modify the security posture* is the exact shape of Garnet's
  authority-surface diff — which is the bridge into PCCP-style envelope language (FDA PCCP,
  UNECE R156, DO-178C change-impact all encode "permitted iff inside a pre-approved envelope").

The proposal: a single **`garnet build --evidence`** flag that bundles the build outputs Garnet
already (partially) emits into one regulator-/auditor-/insurer-readable evidence package.
**`--evidence` as a single flag is a DESIGN; the underlying artifacts only partially exist today.**

---

## Mapping: build output → regulatory artifact → status

| Garnet build output | Regulatory artifact it is designed to feed | Status |
|---|---|---|
| **CycloneDX SBOM** (`garnet-sbom-cyclonedx.tgz`) | CRA SBOM obligation (full application 11 Dec 2027); CRA technical-documentation component | **EXISTS TODAY** — attached to the `v0.8.1` release (per `docs/release-signing.md`) |
| **GPG-signed `SHA256SUMS.asc`** (key fpr `04D5 6F91 F038 17DD FFEB C62A C14D F6E7 1395 6ED1`) | Integrity/authenticity evidence supporting CRA secure-by-design + technical documentation; supply-chain attestation a compliance dossier can cite | **EXISTS TODAY** — on the re-cut `v0.8.1` release; verify per `docs/release-signing.md` |
| **Capability manifest** (compiler-derived authority surface; `@caps` is enforced via a proven trap on both backends) | CRA technical documentation (declared authority surface); PCCP envelope authority component; AI Act traceability input | **PARTIAL** — manifest is emitted for `.garnet` artifacts; an aggregated `--evidence` rendering is a DESIGN for post-v0.8.2 |
| **Bounds profile** (`@max_depth` enforced via trap; `@bounded`/`@rlm_budget`/`@fan_out`/memory/time are **declared-not-enforced**) | PCCP envelope ceilings component; CRA technical documentation (declared operating bounds) | **PARTIAL** — `@max_depth` is enforced; the rest are **named-deferred** and would be labeled declared-not-enforced in any package. Aggregated rendering is a DESIGN |
| **Sealed provenance + transparency log** (in-toto-style seal for `.garnet` artifacts; transparency-log chain) | CRA technical documentation (build provenance); AI Act traceability (who/what/when of the build); audit trail a compliance process can consume | **PARTIAL** — seal + transparency log exist for `.garnet` artifacts as a separate, additive layer; they cover `.garnet` artifacts, **not the release binaries** |
| **The `.garnet` seal** (four trust artifacts + `decision.md`, binding the above into one sealed unit) | PCCP envelope baseline (the certified-against object); single evidence anchor a CRA dossier / insurer / auditor reads | **PARTIAL today / DESIGN as a `--evidence` bundle** — the seal exists for `.garnet` artifacts; folding SBOM + release-signing + manifest + bounds into one `--evidence` package is the post-v0.8.2 design |

---

## Real-today vs proposed — read this before citing anything

- **Real today (verifiable on the `v0.8.1` release):** the CycloneDX SBOM and the GPG-signed
  `SHA256SUMS.asc`. Both are concrete release assets.
- **Real today, but scoped to `.garnet` artifacts (not release binaries):** the capability
  manifest, the `@caps`/`@max_depth` enforcement (proven traps), the seal, and the
  transparency log.
- **Design for post-v0.8.2 (does not exist as a single command):** the unified
  `garnet build --evidence` flag, the regulator-format rendering of the bundle, and the
  PCCP `--envelope` comparison mode on `diff-caps`. These require **nothing new before
  v0.8.2**; they are documentation-and-skin work over the existing kernel.
- **Honesty fence on bounds:** only `@caps` + `@max_depth` are enforced (proven trap, both
  backends). `@bounded` (Wasmtime fuel), `@rlm_budget`, `@fan_out`, memory, time, and
  macOS/Windows OS-sandbox application are **declared-not-enforced** and must be labeled as
  such in any evidence package. Never represent a declared bound as enforced.

## What no conformity claim means here

`garnet build --evidence` is designed to **produce inputs to a compliance process, not a
compliance verdict.** The mechanism would emit artifacts (SBOM, signed checksums, capability
manifest, bounds profile, sealed provenance) that a CRA technical-documentation file, an SBOM
obligation, a PCCP envelope submission, or an AI Act traceability record *can consume*. Garnet
does not assert conformity, does not produce CE marking, and does not replace conformity
assessment, notified-body review, or legal counsel. The seal attests what the build *declares*
(its capability surface and bounds) and binds the build outputs into one unit; only the `@caps`
and `@max_depth` traps are proven, and everything else the seal carries is declared, not proven —
nothing more.

---

**OPEN (Jon — legal-counsel-gated):** every CRA Annex / PCCP / AI Act mapping in the table is
a *positioning hypothesis* about which regulatory artifact each build output could feed; it has
**not** been reviewed by EU CRA / FDA / AI Act counsel. The precise Annex numbers, conformity
pathway, and whether any Garnet output is *sufficient* (vs merely *useful*) for a given
obligation are counsel questions before this leaves internal use. Also OPEN: whether emitting
this evidence package itself triggers any regulatory representation that needs disclaimer review.
