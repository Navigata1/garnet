# Clean-Machine Evidence Checklist — per distribution channel (S166–S178)

The bar any future "Garnet installs via X" claim must clear. A claim that
skips a row below is machine-local evidence at best — label it that way.
Evidence-review language only; no enforcement claims ride along with an
install proof.

## Universal requirements (every channel)

| # | Requirement |
|---|---|
| U1 | Fresh environment: VM/sandbox checkpoint or container with **no Rust/Node toolchains** and no prior Garnet install; record how it was provisioned |
| U2 | Record OS/distro identity: Windows build number (`cmd /c ver` + edition) or `cat /etc/os-release` + `uname -a` |
| U3 | Verify the artifact under test against the release's signed `SHA256SUMS` **before** install (hash + `gpg --verify SHA256SUMS.asc SHA256SUMS` against the committed public key; record the fingerprint line) |
| U4 | Full transcript: every command + output, kept as a durable bundle (dogfood-style manifest with hashes) |
| U5 | Functional smoke after install: `garnet --version` (banner must match the release version), `garnet check` on a known-good example → "0 diagnostics", one `garnet run` |
| U6 | Uninstall/rollback step recorded (channel-appropriate) |
| U7 | Claim-boundary block: what this proves, what it does not (no sandbox/enforcement claims; portability-only labels where applicable) |

## Channel-specific additions

### winget
- Clean Windows 11 VM (Hyper-V checkpoint or Windows Sandbox; Sandbox resets on close — capture evidence before closing).
- `winget install --manifest <local-manifest-dir>` first (pre-submission proof), then post-publication `winget install IslandDevCrew.Garnet`.
- Record SmartScreen/Defender behavior verbatim for the unsigned zip (this is evidence for the signing decision, which is Jon-owned).
- `winget uninstall` restores a garnet-free PATH; prove `garnet` no longer resolves.

### scoop
- Clean VM; install scoop fresh (record its own bootstrap command).
- `scoop install <local-manifest-path>` pre-submission; `scoop bucket add` + install post-publication.
- Prove shim works from a new shell; `scoop uninstall` removes shims.

### Chocolatey (deferred — see chocolatey/FEASIBILITY.md)
- As winget, plus moderation-version pinning: prove the moderated version, not a local build.

### Docker
- Any machine with a daemon counts as "clean" for the *image* claim (the container is the environment); record `docker --version` and base-image digest.
- `docker build` from the committed Dockerfile only — no local edits; record the checksum-verification line passing in the build log.
- `docker run --rm garnet:<v> --version` + U5 smokes with a bind-mounted example.
- Explicitly label: container proof is **Linux-userspace portability** evidence; it is not a clean-distro desktop proof and never a sandbox-enforcement claim.

### Dev Containers
- Consume the committed `devcontainer.json` from a clean VS Code profile; record the `postCreateCommand` output.

### .deb / .rpm (clean Linux — the grade the fleet still lacks)
- Real VM (Hyper-V/UTM/etc.), **not WSL** — WSL results are portability-only by standing rule.
- `dpkg -i` / `rpm -i` from the verified asset; U5 smokes; `apt remove`/`rpm -e` rollback.
- Desktop GUI (Studio) proof additionally needs a real desktop session + screenshot series.

### VSIX
- Clean VS Code (fresh profile or clean VM): `code --install-extension <platform-vsix>`.
- Prove the bundled/required `garnet-lsp` actually starts: open a `.garnet` file, record one LSP-powered feature (diagnostics/hover) with a screenshot.
- Wrong-platform refusal of the other targets is itself recordable evidence.
- Marketplace/open-vsx publication state is separate from install proof and Jon-owned.

### Windows installer (Studio NSIS/MSI)
- Windows Sandbox or clean VM per the committed 2026-05-21 runbook (`GARNET_WINDOWS_STUDIO_CLEAN_VM_SMOKE_2026_05_21.md`).
- Installer version string must match the CLI/truth.json version (the 0.1.0-vs-0.8.1 drift is the current blocker — see Task 4 of the companion report).
- Install → launch → open example → run → screenshot; uninstall via Apps & Features.
