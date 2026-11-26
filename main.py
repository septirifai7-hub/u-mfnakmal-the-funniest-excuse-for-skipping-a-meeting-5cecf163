#!/usr/bin/env python3
"""Entry for the make.fun bounty "The Funniest Excuse for Skipping a Meeting".

The meeting was pointless, the calendar knew it, and the
rectangle on the video call added nothing. This program is
the excuse that gets you out of it with your dignity intact:
one sharp line, no apology tour. It keeps the line as one
constant, checks it against the gate before writing anything,
and writes it byte-for-byte to entry.txt in the output
directory, with no trailing newline. If the line ever grew
past the gate, the program refuses to write instead of
handing the judge an invalid entry.

The output directory defaults to /output and can be pointed
elsewhere with MAKEFUN_OUTPUT_DIR, which is how the grading
sandbox aims the program at its own folder. The judge then
reads the single line and pairs it against the other excuses,
keeping the sharper, more relatable laugh each time — the
winner survives the most head-to-heads, and the pool splits
across the top ten places. The excuse works because everyone
in the meeting has thought the same thing.
"""

import os
import sys
from pathlib import Path

ENTRY = "Sorry, I can't make the meeting — my calendar and I had a long talk and agreed my presence adds nothing but a rectangle."

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the gate: 1-200 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry contains control characters")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    path = out_dir / "entry.txt"
    path.write_text(text, encoding="utf-8")
    # The grader collects outputs as another user: leave it world-readable.
    path.chmod(0o644)


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
