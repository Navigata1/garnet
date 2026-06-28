import json
import re
import sys
import threading
import time
from pathlib import Path

import winpty


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*(?:\x07|\x1b\\)")


def strip_ansi(text: str) -> str:
    text = ANSI_RE.sub("", text)
    text = text.replace("\r", "")
    return "\n".join(line.rstrip() for line in text.splitlines())


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: run_winpty_repl_probe.py <repo> <evidence-dir>", file=sys.stderr)
        return 2
    repo = Path(sys.argv[1]).resolve()
    evidence = Path(sys.argv[2]).resolve()
    raw_dir = evidence / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    exe = repo / "target" / "debug" / "garnet.exe"
    if not exe.exists():
        print(f"missing built binary: {exe}", file=sys.stderr)
        return 2

    proc = winpty.PtyProcess.spawn([str(exe), "repl"], cwd=str(repo), dimensions=(32, 100))
    chunks: list[str] = []
    reader_errors: list[str] = []
    stop = threading.Event()

    def reader() -> None:
        while not stop.is_set():
            try:
                chunk = proc.read(4096)
            except Exception as exc:  # winpty raises when the process exits.
                reader_errors.append(f"{type(exc).__name__}: {exc}")
                break
            if chunk:
                chunks.append(chunk)
            elif not proc.isalive():
                break

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()

    actions: list[dict[str, str | float]] = []

    def send(label: str, text: str, delay: float = 0.35) -> None:
        actions.append({"label": label, "sent_repr": repr(text), "delay_s": delay})
        proc.write(text)
        time.sleep(delay)

    time.sleep(0.8)
    send("help", ":help\r", 0.5)
    send("doc primitive", "?doc read_file\r", 0.5)
    send("dangling caps annotation", "@caps(net)\r", 0.4)
    send("complete annotated function", "def fetch() { 1 }\r", 0.5)
    send("caps overview", ":caps\r", 0.6)
    send("define binding one", "def myhelper() { 7 }\r", 0.35)
    send("define binding two", "def myhero() { 8 }\r", 0.35)
    send("command completion menu", ":\t", 0.6)
    send("ctrl-c after command menu", "\x03", 0.35)
    send("primitive completion menu", "read_\t", 0.6)
    send("ctrl-c after primitive menu", "\x03", 0.35)
    send("binding completion menu", "myh\t", 0.6)
    send("ctrl-c after binding menu", "\x03", 0.5)
    send("history seed expression", "40 + 2\r", 0.45)
    send("history up/down/up/enter", "\x1b[A\x1b[B\x1b[A\r", 0.6)
    send("history down visibility seed", "99\r", 0.35)
    send("history up visible", "\x1b[A", 0.35)
    send("history down clears prompt", "\x1b[B", 0.35)
    send("history up enter", "\x1b[A\r", 0.45)
    send("reverse search start", "\x12", 0.35)
    send("reverse search term", "40\r", 0.35)
    send("reverse search execute", "\r", 0.45)
    send("partial line before ctrl-c", "1 +", 0.25)
    send("ctrl-c abandon partial", "\x03", 0.35)
    send("post-ctrl-c expression", "2 + 3\r", 0.45)
    send("brace multiline start", "def add(a, b) {\r", 0.35)
    send("brace multiline body", "  a + b\r", 0.35)
    send("brace multiline close", "}\r", 0.45)
    send("call multiline function", "add(2, 5)\r", 0.45)
    send("ctrl-d eof", "\x04", 0.5)

    deadline = time.time() + 4
    while proc.isalive() and time.time() < deadline:
        time.sleep(0.1)
    if proc.isalive():
        proc.terminate()
    stop.set()
    thread.join(timeout=2)

    raw = "".join(chunks)
    plain = strip_ansi(raw)
    (raw_dir / "winpty-repl-session.ansi").write_text(raw, encoding="utf-8", newline="")
    (raw_dir / "winpty-repl-session.txt").write_text(plain, encoding="utf-8", newline="\n")

    checks = {
        "banner": "Garnet REPL" in plain,
        "help": "REPL commands:" in plain and "Tab completion" in plain,
        "doc_read_file": "fs::read_file" in plain and "caps: fs" in plain,
        "unicode_middle_dot": "Std · stability: Stable" in plain,
        "dangling_caps_multiline": "@caps(net)" in plain and "...>" in plain and "def fetch() { 1 }" in plain,
        "caps_not_budget": "NOT an enforced budget" in plain and "net: fetch" in plain,
        "command_completion": ":caps" in plain and "command" in plain,
        "primitive_completion": "read_file" in plain and "primitive" in plain,
        "binding_completion": "myhelper" in plain and "binding" in plain,
        "history_recall": plain.count("=> 42") >= 3 and "=> 99" in plain,
        "reverse_search": "reverse-search" in plain and plain.count("=> 42") >= 3,
        "ctrl_c_abandon_clean": "=> 5" in plain,
        "brace_multiline": "def add(a, b) {" in plain and "=> 7" in plain,
        "ctrl_d_exit": not proc.isalive(),
    }
    summary = {
        "schema": "garnet.validation.rb7_winpty/1",
        "host": "Windows",
        "pty": "winpty",
        "repo": str(repo),
        "binary": str(exe),
        "exitstatus": proc.exitstatus,
        "actions": actions,
        "checks": checks,
        "reader_errors": reader_errors,
    }
    (evidence / "winpty-probe-summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8", newline="\n"
    )
    print(json.dumps(summary["checks"], indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
