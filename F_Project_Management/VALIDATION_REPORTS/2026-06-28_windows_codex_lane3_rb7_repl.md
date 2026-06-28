# Lane 3 - RB-7 REPL Interactive Windows Validation

Date: 2026-06-28
Reviewer lane: Codex on Windows
Host OS: Windows 10.0.26200.0 on `NUCBOX_M2PRO_S`
Validation branch: `validation/2026-06-25-codex-rb7-repl`
Reviewed commit: `2e2fe843e87be0c8fc9a4745a5bb138fba597d23`
Evidence bundle: `proofs/validation/rb7-repl/windows-20260628-lane3/`
Evidence manifest: `proofs/validation/rb7-repl/windows-20260628-lane3/MANIFEST.sha256` (15 files)

## Verdict

RB-7 HELD for the Windows interactive REPL path under a real Windows PTY (`winpty`) and the Codex allocated PTY. It is still not a literal Windows Terminal GUI/computer-use recording because no callable desktop computer-use tool was exposed in this session. The claim should be phrased as "Windows PTY verified", not "Windows Terminal GUI verified".

The `winpty` probe drove `target/debug/garnet.exe repl` interactively and recorded raw ANSI plus stripped text transcripts. The probe verified the banner, help, `?doc`, `:caps`, dangling `@caps` multiline continuation, brace multiline continuation, command/primitive/live-binding Tab completion menus, Up/Down history, reverse search, Ctrl-C abandon from a clean partial line, Ctrl-D exit, and Unicode rendering for the runtime output that actually appears.

The plain non-TTY path also held when driven with a clean input script. However, the handoff wording that says to pipe `docs/demos/repl-session.txt` into `garnet repl` is stale or imprecise: that file is an output transcript, not a clean input script. Piping it exits 0 but produces parse errors because prompts, prose, and recorded output are fed back into the REPL. This is a documentation/handoff mismatch, not an RB-7 runtime failure.

## Surface Scores

| Surface | Score | Classification | Evidence |
| --- | ---: | --- | --- |
| Interactive REPL launch on Windows PTY | 5/5 | HELD | `raw/winpty-repl-session.ansi`, `winpty-probe-summary.json` |
| `:help`, `?doc`, `:caps` rendering | 5/5 | HELD | `winpty-probe-summary.json`; `raw/101-plain-scripted-session.stdout` |
| `:caps` honesty label | 5/5 | HELD | `NOT an enforced budget` appears in winpty and plain transcripts |
| Multiline annotation and brace continuation | 5/5 | HELD | `@caps(net)` -> `...>` -> `def fetch`; `def add(a,b){...}` -> `=> 7` |
| Tab completion over commands, primitives, live bindings | 5/5 | HELD | winpty checks `command_completion`, `primitive_completion`, `binding_completion` all true |
| History Up/Down and reverse-search recall | 5/5 | HELD | winpty checks `history_recall` and `reverse_search` true; manual Codex PTY also showed Up and Down behavior |
| Ctrl-C and Ctrl-D | 4/5 | HELD WITH CAVEAT | winpty clean partial-line Ctrl-C and Ctrl-D passed; manual menu-abandon once left a partial `+ 2` parse error before a clean retest passed |
| Unicode / console rendering | 4/5 | HELD FOR RUNTIME OUTPUT SEEN | banner em dash and `Std · stability` rendered; no runtime box-drawing surface was emitted in this run |
| Plain non-TTY dispatch | 5/5 | HELD | `101-plain-scripted-session` exit 0 with expected help/doc/caps/multiline output |
| Handoff docs-demo pipe | 2/5 | DOC MISMATCH | `100-plain-docs-demo-file-piped` exit 0 but parse errors because the file is an output transcript |

## Confirmed Facts

- Read `/AGENTS.md`, `garnet-cli/AGENTS.md`, `F_Project_Management/W_REBUILD/RB7_NUC_HANDOFF.md`, `F_Project_Management/W_REBUILD/W_REBUILD_FINAL_REPORT.md`, and `garnet-cli/src/cmd/repl.rs`.
- `F_Project_Management/W_REBUILD/RB7_NUC_HANDOFF.md` is the current handoff path; `W_REBUILD/RB7_NUC_HANDOFF.md` does not exist at repo root on this commit.
- `cargo build -p garnet-cli` exited 0 (`010-cargo-build-garnet-cli`).
- `cargo test -p garnet-cli repl -- --nocapture` exited 0. The REPL unit surface included 21 passing `cmd::repl::tests` plus REPL-adjacent filtered matches.
- `winpty-probe-summary.json` recorded all 14 interactive checks as true and process `exitstatus: 0`.
- A PowerShell `Start-Transcript` log exists but is partial because reedline clears/redraws the screen; the stronger raw evidence is `raw/winpty-repl-session.ansi`.
- No Windows or macOS OS-sandbox enforcement claim is made here.

## Recommendations

- If public wording requires literal "Windows Terminal" proof, rerun this lane with a desktop-control or screen-recording tool and Windows Terminal itself. The current evidence proves the Windows PTY/reedline interactive path, not the GUI terminal host.
- Split `docs/demos/repl-session.txt` into an input script plus an expected-output transcript, or update the handoff text to stop telling reviewers to pipe an output transcript back into the REPL.
- Keep the `:caps` wording exactly calibrated: declared plus available, not an enforced budget.
- If the menu-abandon Ctrl-C edge matters, add an explicit automated winpty regression that opens a completion menu, sends Ctrl-C, then verifies the next clean expression is not contaminated by the abandoned line.

## Jon-Only Decisions

- Whether Windows PTY proof is enough to close the NUC side of RB-7, or whether a literal Windows Terminal GUI/screen recording is still required.
- Whether to revise the RB-7 handoff and demo transcript structure.
- Any public claim that RB-7 is cross-OS complete; this host cannot verify the macOS terminal side.
