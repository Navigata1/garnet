# Distribution Drafts — S166–S178 (W-SHIP) — STATUS: DRAFT, NOTHING PUBLISHED

Authored 2026-06-11 by the Windows NUC Claude lane (Fable 5) as part of the
distribution-band evidence pass. Companion report:
`F_Project_Management/FLEET_REPORTS/2026-06-11_windows-nuc_claude-fable_distribution.md`.

**Nothing in this directory has been submitted, published, or registered
anywhere.** Every channel submission (winget-pkgs PR, scoop bucket upstream,
Chocolatey moderation, Docker Hub/GHCR push, Marketplace/open-vsx publication,
release-asset changes) is **Jon-owned** and out of scope for this lane.

## Contents

| Path | Channel | State |
|---|---|---|
| `winget/IslandDevCrew.Garnet/0.8.1/` | winget (3-file manifest set) | syntax-validated draft; **blocked by missing Windows release asset** — `InstallerUrl`/`InstallerSha256` are explicit placeholders |
| `scoop/garnet.json` | scoop | syntax-validated draft; same Windows-asset blocker, same placeholders |
| `chocolatey/FEASIBILITY.md` | Chocolatey | feasibility memo only — recommends deferring |
| `docker/Dockerfile` | Docker | **real** — pins the published v0.8.1 `.deb` by its official SHA256; buildable today on any machine with a Docker daemon (daemon on this NUC was stopped; not built here) |
| `docker/devcontainer.json` | Dev Containers | real — consumes the Dockerfile |
| `CLEAN_MACHINE_EVIDENCE_CHECKLIST.md` | all channels | the per-channel evidence bar for any future "it installs" claim |

## The one blocking fact

The v0.8.1 release contains **no Windows asset**. Both Windows package
managers below are drafted against the *planned* asset name
`garnet-0.8.1-x86_64-pc-windows-msvc.zip` (expected contents: `garnet.exe`,
`garnet-lsp.exe`, `LICENSE`, `README`). Until such an asset exists on a
release and lands in a signed `SHA256SUMS`, these manifests are
syntax-complete but **un-installable and un-submittable**. Producing that
asset is the first implementation slice of the band (S167 in the draft plan)
and is not done here (this lane is evidence/plans-only).

## Claim boundaries

- Draft manifests prove *syntax feasibility only* (see the companion report
  for the exact validation commands and outputs).
- The Dockerfile proves *recipe correctness* only to the extent recorded in
  the companion report; no image was built or pushed from this machine.
- No sandbox/enforcement claims of any kind are made by anything here.
