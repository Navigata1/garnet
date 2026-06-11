# LAUNCH_DRAFTS — W-LAUNCH positioning drafts

**Status: DRAFTS. Not public copy. No posting, no marketing claims, no merge.**

Positioning drafts for the W-LAUNCH band (command center S179–S200), derived from
`F_Project_Management/RESEARCH/GARNET_REASSESSMENT_2026-06-11.md` §3 + Gap 1.
Every document is calibrated: capability verbs are "designed to" / "would" /
"intended to"; the word *enforced* appears only where a deterministic trap proves
it (today: `@caps` + `@max_depth`, both backends). Each carries explicit
`OPEN (Jon)` items for anything unverified or counsel-gated.

## Contents

| File | What it positions |
|---|---|
| `WLAUNCH_ENVELOPE_MODE_BRIEF.md` | Delta-certification: `diff-caps --envelope` as a post-v0.8.2 slice, framed against FDA PCCP / EU CRA "substantial modification" / UNECE R156 / DO-178C. Names the 11 Sep 2026 CRA Art. 14 clock. |
| `WLAUNCH_INSURER_BRIEF.md` | The sealed capability+bounds envelope as an actuarial instrument; the `diff-caps` gate as a notifiable-change mechanism; the seal chain as a liability firewall. ~2 pages. |
| `WLAUNCH_BUDGET_LATTICE_BRIEF.md` | Metered delegation: `@max_depth`/`@fan_out`/`@bounded`/proposed `@rlm_budget` generalized into an attenuating budget lattice; AP2 as the boundary value (interop, never compete). Honesty fence: only `@max_depth` is enforced today. |
| `WLAUNCH_REGULATORY_EVIDENCE_ONEPAGER.md` | A proposed `garnet build --evidence` flag; a table mapping each build output → CRA Annex / SBOM / PCCP / AI Act language → real-today vs design-for-post-v0.8.2 status. Not legal advice; mappings are counsel-gated. |
| `THREAT_WALL_NARRATIVE_REFRESH.md` | One-page threat narrative (feeds RB-0/website later) weaving Stroustrup's validation-retirement, the Amazon finding (via DHH), "the agent is the telephone switch" (Peyton Jones), "copilots need pilots", and the senior-multiplier framing. |

## Discipline carried in every file

- **No quoted person endorses Garnet.** The builders cited have never heard of it;
  quotes describe the field's open problem, not anyone's support. The threat-wall
  doc carries this as a persistent visible note.
- **No production / no v1.0** claim anywhere.
- **Real-today vs design-for-post-v0.8.2** is marked explicitly; the SBOM and the
  GPG-signed `SHA256SUMS.asc` are the only release artifacts called real-today.

## Provenance

Drafted 2026-06-11 by the MacBook Air / Claude (Fable 5) W-LAUNCH design lane,
read-only against `main @ 8482294`, on branch
`aux/2026-06-11-macbook-air-claude-trustband`. No PR; no merge; no gate/CI change.
