#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Holds the entry line as a constant, checks it against the kit's gate
(UTF-8 text, 1-160 characters, not only whitespace, a single line),
prints it, and writes it to /output/entry.txt.
"""

import os
import sys

ENTRY = (
    "I'm away until Monday \u2014 my inbox is being watched by my cat, "
    "who has already sat on your email, knocked it off the desk, "
    "and gone back to sleep."
)

MAX_CHARS = 160


def gate_check(text: str) -> None:
    """Enforce the competition gate; raise ValueError on any violation."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch != "\t" for ch in text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    text.encode("utf-8")  # raises UnicodeEncodeError if not UTF-8


def main() -> int:
    gate_check(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    print(ENTRY)
    print(f"({len(ENTRY)} characters, single line, gate OK)")
    return 0


def self_test() -> None:
    """Small self-test: the printed line must be byte-identical to ENTRY."""
    import subprocess

    out = subprocess.run(
        [sys.executable, __file__], capture_output=True, text=True, check=True
    )
    first_line = out.stdout.splitlines()[0]
    assert first_line == ENTRY, "printed line differs from ENTRY"
    assert len(ENTRY) == 144, f"expected 144 characters, got {len(ENTRY)}"
    print("self-test passed: printed line is byte-identical to ENTRY")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        self_test()
    else:
        sys.exit(main())
