# RB-0 Precheck - MacBook Air Codex - 2026-06-11

Lane: RB-0 pre-verification input for RB-0b/RB-0c and Air branch hygiene.
Agent slot: MacBook Air Codex.
Write scope used: this report file only.
No merges, tag edits, releases, branch deletions, cherry-picks, ECC hooks, gate changes, CI changes, or policy changes were performed.

## Gate-Relevant Facts

Authoritative checkout for this report:

- Repo: `/Users/idc2.0/Desktop/GARNET Opus 4.7 Final/E_Engineering_Artifacts`
- Branch: `aux/2026-06-11-macbook-air-codex-rb0`
- Report base: `HEAD = origin/main = c4b9e28ae2bd184b41f3556bb44e3f7d3aa87f38`
- Latest visible commits on `origin/main`:
  - `c4b9e28 RB-0c: version-narrative fixes - stale strings to zero on public surfaces (#386)`
  - `8482294 RB-0b: README replacement - verified front door, walkthroughs relocated to docs/internals/ (#385)`
  - `3ccfd38 RB-0a: xtask truth - machine-truth generator + marker stamping + --check drift guard (#384)`

Fetch evidence:

- `git fetch origin main --tags --prune` updated `main` but exited `1` because local tag `v0.4.2` would be clobbered.
- Local `v0.4.2`: `1ccde0d7cd27351f24f3e0e754d687c0f939808d`
- Origin `v0.4.2`: `6e945d6a151c2b97ae842c21aeeaa5a678ae65f5`
- This is local machine hygiene. I did not delete, move, or repoint any tag.

Release truth:

- `gh release view v0.8.1 --repo Island-Dev-Crew/garnet --json tagName,publishedAt,targetCommitish,assets`
- Tag: `v0.8.1`
- Published: `2026-06-07T07:55:45Z`
- Target commitish: `main`
- Assets: `garnet-0.7.0-lsp-mvp-darwin-arm64.vsix`, `garnet-0.7.0-lsp-mvp-linux-x64.vsix`, `garnet-0.8.1-1.x86_64.rpm`, `garnet-0.8.1-aarch64-apple-darwin.tar.gz`, `garnet-0.8.1-x86_64-apple-darwin.tar.gz`, `garnet-sbom-cyclonedx.tgz`, `garnet_0.8.1-1_amd64.deb`, `SHA256SUMS`, `SHA256SUMS.asc`

Local tag pollution affecting tag-derived tooling:

- `git tag --list 'v*' --sort=-v:refname | head` begins with `v1.17.0`, `v1.16.0`, `v1.15.0`.
- `git tag --merged origin/main --list 'v*' --sort=-v:refname | head` begins with `v0.8.1`, `v0.8.0`, `v0.5.0`, `v0.4.2`.
- `git ls-remote --tags origin 'v1.17.0' 'v0.8.1' 'v0.4.2'` returned origin tags for `v0.8.1` and `v0.4.2`, not `v1.17.0`.
- `cargo run -p xtask -- truth --check` failed locally because `truth:latest_tag` expected `"v1.17.0"` while `docs/truth.json` records `"v0.8.1"`.
- Interpretation: project release truth remains `v0.8.1`; this machine has stale/foreign local tags that can poison local tag-derived truth checks until Jon approves cleanup.

Readiness and machine-truth numbers:

- `python3 scripts/garnet_readiness_status.py --format json`: `87/87` tracked slices, `100.0%`, no open slices.
- `python3 scripts/garnet_mit_readiness_status.py --format json`: `overall_status = active-partial`, `completion_percent = 92.8`; current truth explicitly says tracked plan completion is not full MIT/productization completion.
- `python3 scripts/garnet_stdlib_layer_gate.py --format json`: `80` primitives, `40` Core, `40` Std, `54` Stable, `26` Experimental, `100.0%` explicit stability metadata, no deprecated primitives.
- `cargo metadata --no-deps --format-version 1`: `14` workspace packages: `garnet-parser`, `garnet-interp`, `garnet-memory`, `garnet-stdlib`, `garnet-check`, `garnet-cli`, `garnet-convert`, `garnet-cst`, `garnet-registry-stub`, `garnet-vm`, `garnet-actor-runtime`, `garnet-suggest-llm`, `garnet-lsp`, `xtask`.
- `docs/truth.json`: `latest_tag = v0.8.1`, `primitive_count = 80`, `readiness_pct = 92.8`, `tracked_slices = 87/87`, `version = 0.8.1`, `workspace_tests.passed = 1951`, `workspace_tests.failed = 0`; `security_test_count` intentionally omitted because the old public `136 security tests` number has no trusted derivation.

## RB-0c Stale-String Sweep

Command:

```sh
rg -n "post-v0\.5\.0|24 stdlib|24 registry|24 bridged|v0\.5\.0 is research-grade|S1 LSP|0\.7\.0-lsp|monthly is the floor" README.md FAQ.md docs CURRENT_STATE.md spec
```

Result:

- `spec/` is absent in this checkout, so `rg` returned `spec: No such file or directory` and exit code `2` after still searching the existing requested surfaces.
- No hits in `README.md`.
- No hits in `FAQ.md`.
- Two remaining hits:

| File:line | Text anchor | Classification | RB-0c input verdict |
|---|---|---|---|
| `CURRENT_STATE.md:120` | `garnet-0.7.0-lsp-precision.vsix` | Context-sensitive | Historical/current-state nuance. It names a local VSIX packaging artifact in the S16 editor row, not a public release-truth claim. Do not mechanically scrub without checking current extension packaging and release-asset naming. |
| `docs/blog/index.html:80` | `monthly is the floor, not the ceiling` | Context-sensitive | Public cadence language. It is not a stale version number, but it is a public promise-like phrase. Reword only with Jon/RB-0c public-site intent. |

First-pass cleanup files needing human-aware review:

- `CURRENT_STATE.md`: one historical/current-state LSP artifact reference.
- `docs/blog/index.html`: one cadence statement.
- No README/FAQ first-pass stale-string cleanup remains after RB-0b/RB-0c.

## RB-0b README_PROPOSED Verification

Status of draft:

- `F_Project_Management/W_REBUILD/README_PROPOSED.md` starts with a status comment saying it landed as root `README.md` by RB-0b on `2026-06-11`.
- `origin/main` includes RB-0b at `8482294`.
- Principle line is present:
  - `README.md:10`: `No authority without evidence. Acceptance is a decision made on evidence the author cannot fake.`
  - `F_Project_Management/W_REBUILD/README_PROPOSED.md:15`: same sentence.
- PR-B/RB-0b is merged. This is not pending.

Line-count budget:

- `README.md`: `172` lines.
- `F_Project_Management/W_REBUILD/README_PROPOSED.md`: `167` lines.
- Both are under the `<=180` budget.

Scripted link/path checks:

- Root README as landed: `13` local links OK, `0` local failures, `5` external links checked as HTTP `200`.
- README_PROPOSED under intended root-README semantics: `11` local links OK, `0` local failures, `5` external links checked as HTTP `200`.
- README_PROPOSED under physical file-location semantics has expected false positives because it lives under `F_Project_Management/W_REBUILD/` while the draft links are root-relative for replacement use. The physical-location false positives were: `docs/release-signing.md`, `CURRENT_STATE.md`, `A_Research_Papers/`, `C_Language_Specification/GARNET_v1_0_Mini_Spec.md`, `C_Language_Specification/GARNET_v0_4_2_Conformance_Matrix.md`, `FAQ.md#whats-the-capability-model`, `FAQ.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`.

External links checked as HTTP `200`:

- `https://garnet-lang.org/status.html`
- `https://garnet-lang.org/getting-started.html`
- `https://garnet-lang.org/blog/`
- `https://github.com/Island-Dev-Crew/garnet/discussions`
- `https://github.com/Island-Dev-Crew/garnet/issues`

Internal vocabulary gate:

- Search: `Objective Pulse|Continuation Pulse|manifested dogfood bundle|manifested .*dogfood|\bS[0-9]+\b`
- Result: no hits in `README.md` or `F_Project_Management/W_REBUILD/README_PROPOSED.md`.
- Verdict: no surviving Objective/Continuation Pulse language, no bare S-number workflow shorthand, and no manifested-dogfood-bundle phrasing in the front-door README/draft.

Number cross-check verdict:

- Safe for presentation from machine truth:
  - Latest release is `v0.8.1`, published `2026-06-07T07:55:45Z`, with signed checksums asset present.
  - Tracked implementation plan is `87/87`, but that is not full productization.
  - MIT/readiness status is `active-partial`, `92.8%`.
  - Primitive count is `80`, split `40` Core / `40` Std.
  - Workspace package count is `14`.
  - Last truth JSON records `1951` workspace tests passing and `0` failing at its recorded generation point.
- Needs rewording or careful framing:
  - Do not use this machine's local `xtask truth --check` failure as project-release failure; it is caused by local tag pollution.
  - Do not restamp or revive any historical `136 security tests` claim without a trusted derivation.
  - Do not claim production, v1.0, or enforcement beyond deterministic trap evidence.

## Air Branch Hygiene Verdicts

Air clone checked:

- Repo: `/Users/idc2.0/clawd/repos/garnet-agent-contracts`
- Fetch: `git fetch origin main --tags --prune` updated `main` but hit the same local `v0.4.2` clobber rejection.
- Status: current branch `aux/2026-06-11-macbook-air-claude-trustband`; untracked `F_Project_Management/GARNET_CODEX_TO_CLAUDE_HANDOFF_2026-05-09.md`.
- Air clone `HEAD`: `63e11d235cc0fe07170f1fdd647b4a02ecdf412f`
- Air clone `origin/main`: `c4b9e28ae2bd184b41f3556bb44e3f7d3aa87f38`

Summary:

- Local non-main branches checked: `28`.
- Safe-delete verdicts: `25`.
- Keep verdicts: `1`.
- Needs-Jon verdicts: `2`.
- Cherry-pick-first verdicts: `0`.
- No branch was deleted or cherry-picked.

| Branch | Verdict | Evidence |
|---|---|---|
| `codex/blog-v0-5-launch` | safe-delete | Ancestry-merged into `origin/main` (`git branch --merged origin/main`). |
| `codex/contact-truth-security` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/mit-windows-linux-lane` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/phase-id-collision-convention` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/priority-slices-plan` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-animated-terminal` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-blog-first-post` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-build-stamp` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-comparison-table` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-density-pass` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-discussions-link` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-funding-governance` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-migrate-tighten` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-os-detect-banner` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-p0-install-funnel` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-p1-trust-community` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-p2-meta-footer` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-p2-polish` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/site-studio-tighten` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/website-index-improvements` | safe-delete | Ancestry-merged into `origin/main`. |
| `feat/agent-documentation-contracts` | safe-delete | Ancestry-merged into `origin/main`. |
| `codex/phase4bi-nil-relational-const-guards` | safe-delete | Not ancestry-merged, but `git cherry -v origin/main` reports `- 9aedc966...`; patch-equivalent to upstream. |
| `codex/reconcile-current-state-ledger-count` | safe-delete | Not ancestry-merged, but `git cherry -v origin/main` reports `- 9ce6dd9...`; patch-equivalent to upstream. |
| `codex/website-refactor` | safe-delete | Not ancestry-merged, but `git cherry -v origin/main` reports `- cf7e66f...`; patch-equivalent to upstream. |
| `codex/fleet-report-macbook-air-claude` | safe-delete | `git cherry` reports `+ d09fad2...`, but the only file is `F_Project_Management/FLEET_REPORTS/2026-06-10_macbook-air_claude-fable.md` and `git diff origin/main..codex/fleet-report-macbook-air-claude -- <file>` is empty. Content is already in `origin/main` via `1cfadda S131-S134`. |
| `aux/2026-06-11-macbook-air-claude-trustband` | keep | Current Air clone branch. Unique draft content: `F_Project_Management/LAUNCH_DRAFTS/*` and `F_Project_Management/TRUST_BAND/*`; `git cherry` reports `+ 63e11d2...`. Keep until Jon decides whether these drafts get a PR, archive, or deletion. |
| `agent-mac-codex/s18-llm-package` | needs-Jon | Cherry-positive branch; see S18 analysis below. Main appears to contain equivalent S18 substance under different commits, so do not blind cherry-pick or delete without lead review. |
| `agent-mac-codex/s19-suggest-llm` | needs-Jon | Cherry-positive branch; see S19 analysis below. Main appears to contain equivalent S19 substance under different commits, so do not blind cherry-pick or delete without lead review. |

### S18 Cherry-Positive Analysis

Branch: `agent-mac-codex/s18-llm-package`

`git cherry -v origin/main agent-mac-codex/s18-llm-package`:

- `+ 8c00294 Seed Layer-2 packages through a reproducible local registry`
- `+ 8fe5ec7 Record the S18 PR-open boundary`
- `+ 4e7eed8 Record the S18 review boundary`

Touched areas from `git diff --name-only origin/main...agent-mac-codex/s18-llm-package`:

- `.agent/plans/mac-codex-S18-plan.md`
- `CHANGELOG.md`, `CURRENT_STATE.md`
- `F_Project_Management/AGENT_COORDINATION_LEDGER.md`
- `F_Project_Management/GARNET_v0_5_READINESS_BASELINE.json`
- `F_Project_Management/GARNET_v0_7_SLICE_DOGFOOD.md`
- `examples/garnet_lang_registry_seed/*`
- `examples/mvp_18_all_official_packages/*`
- `scripts/garnet_mit_readiness_status.py`
- `scripts/smoke_garnet_lang_packages_seed.py`
- `scripts/test_garnet_mit_readiness_status.py`
- `tools/garnet-lang-template/*`

Main-side evidence already present:

- `git log --all --grep 'S18|Layer-2 package|registry seed'` shows `05968d8 Make Layer-2 package work reproducible before org publication` and `6157a24 Record the S18 merge state after green CI`.
- `origin/main` contains `tools/garnet-lang-template/`, `examples/garnet_lang_registry_seed/`, and `examples/mvp_18_all_official_packages/`.
- `CURRENT_STATE.md:113-115` records the S18 scaffold, local registry seed, and all-packages consumer smoke with calibrated "not published externally" language.

Verdict: `needs-Jon`. The branch is cherry-positive, but its functional content appears to have landed through different commits. A lead should compare intent/history before deleting the branch; no cherry-pick is recommended from this precheck alone.

### S19 Cherry-Positive Analysis

Branch: `agent-mac-codex/s19-suggest-llm`

`git cherry -v origin/main agent-mac-codex/s19-suggest-llm`:

- `+ 4228652 Isolate the LLM suggest tier behind an explicit advisory boundary`
- `+ 2b7e21e Record S19 PR-open state without widening release claims`
- `+ 0968012 Clarify S19 trait boundary while S18 remains separate`
- `+ 83d1458 Record S19 review confidence before CI completion`

Touched areas from `git diff --name-only origin/main...agent-mac-codex/s19-suggest-llm`:

- `.agent/plans/mac-codex-S19-plan.md`
- `.github/workflows/ci.yml`
- `AGENTS.md`
- `CHANGELOG.md`, `CURRENT_STATE.md`
- `Cargo.lock`, `Cargo.toml`
- `F_Project_Management/AGENT_COORDINATION_LEDGER.md`
- `F_Project_Management/GARNET_v0_5_READINESS_BASELINE.json`
- `F_Project_Management/GARNET_v0_7_SLICE_DOGFOOD.md`
- `benchmarks/paper_vi_exp3_compiler_as_agent/*`
- `garnet-suggest-llm/*`
- `scripts/check-agent-contracts.py`
- `scripts/check_determinism_no_llm.py`
- `scripts/garnet_mit_readiness_status.py`
- `scripts/test_check_determinism_no_llm.py`
- `scripts/test_garnet_mit_readiness_status.py`

Main-side evidence already present:

- `git log --all --grep 'S19|LLM suggest|advisory boundary'` shows `10e7562 Keep LLM suggestions optional behind a reproducible advisory boundary` and `b5cfcbf Record the S19 merge state after green CI`.
- `origin/main` contains `garnet-suggest-llm/` and `benchmarks/paper_vi_exp3_compiler_as_agent/`.
- `CURRENT_STATE.md:119` records the S19 LLM tier as feature-gated-source-ready, non-default `llm`, advisory, and not yet shipped end-to-end through public CLI wiring.
- `CURRENT_STATE.md:129` records the Paper VI Exp 3 harness as harness-only, with no h3a/h3b/h3c result claim.

Verdict: `needs-Jon`. The branch is cherry-positive, but its functional content appears to have landed through different commits. A lead should compare intent/history before deleting the branch; no cherry-pick is recommended from this precheck alone.
