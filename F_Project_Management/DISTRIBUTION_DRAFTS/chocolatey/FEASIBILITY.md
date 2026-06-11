# Chocolatey Feasibility — S166–S178 draft note (no package authored)

**Verdict: feasible but recommend DEFER until after winget + scoop land.**

## What Chocolatey would require

1. A real Windows release asset (same S167 blocker as winget/scoop).
2. A `.nuspec` + `tools/chocolateyInstall.ps1` package that downloads the zip
   and verifies its checksum (`Install-ChocolateyZipPackage` with
   `-Checksum`/`-ChecksumType sha256`).
3. A community-repo account and **human moderation review** on first
   submission (days-to-weeks latency; re-review on flagged updates).
4. Ongoing maintainer commitment — unlike winget/scoop, the community repo
   expects timely version pushes; stale packages get flagged.

## Why defer

- winget ships with Windows 10/11 and is the zero-install default; scoop is
  the developer-tools standard. Together they cover the Windows CLI audience
  the band targets.
- Chocolatey adds a moderation pipeline and a maintainer obligation without
  reaching a new audience segment for a developer CLI.
- The same zip asset serves all three channels — adding Chocolatey later is
  cheap once the asset + SHA256SUMS discipline exists, and the manifest can
  be generated from the winget draft in under an hour.

## If/when pursued

- Package id `garnet` (check for squatting first), version synced from
  `docs/truth.json` (RB-0a) — never hand-stamped.
- Submission and account ownership: **Jon-owned**, like all publication acts.
