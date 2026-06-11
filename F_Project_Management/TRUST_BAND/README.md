# TRUST_BAND — design drafts for the S141–S150 trust band

**Status: DESIGN DRAFTS. Not executed, not graded, not merged.**

This directory holds design documents for Garnet's independent-trust band
(command center S141–S150). It is authored by an aux design/audit lane and
contains no executable claims.

## Hard boundaries this directory observes

- **S114 stays labeled `self-verified — NOT independently verified`** (`CURRENT_STATE.md:15-16`).
  Nothing here promotes that label or predicts the outcome of any re-verification.
- The independence of the trust band is the whole point: **the lane that designs
  a re-verification package may not run it, grade it, or characterize its likely
  result.** That separation is encoded in the package itself.
- "Enforced" means a proven deterministic trap on both backends. Today that is
  only `@caps` + `@max_depth`. Everything else is declared-not-enforced or a stub.

## Contents

| File | What it is |
|---|---|
| `S114_INDEPENDENT_REVERIFICATION_PACKAGE.md` | The design for an external lane to independently re-verify the S114 kernel red-team finding: scope, attack-surface map, reproduction-harness inventory, pre-registered pass/fail criteria, and the independence protocol (who may run it, how it is graded, how self-grading is structurally prevented). **Design only — not run.** |

## Provenance

Drafted 2026-06-11 by the MacBook Air / Claude (Fable 5) trust-band design lane,
read-only against `main @ 8482294`, on branch
`aux/2026-06-11-macbook-air-claude-trustband`. No PR; no merge; no gate/CI change.
Cited repo files were verified to exist at authoring time.
