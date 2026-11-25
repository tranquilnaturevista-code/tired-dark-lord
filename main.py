#!/usr/bin/env python3
"""The Tired Dark Lord: A 100-Word Villain Monologue — entry program.

Writes one hand-written monologue of exactly 100 words, spoken by
Varric, lord of the Ninth Toll — a fantasy villain who has kept his
throne for forty years and is secretly just very tired — to
``/output/entry.txt`` (or ``$MAKEFUN_OUTPUT_DIR/entry.txt``).

The tiredness is never announced: it lives in the pauses, the
trailing-off sentences and the small deflections (a torch held too
high, a crown that pinches, a barge that still has to leave at
dawn). The monologue is fixed: the same text on every run, so the
entry the judge reads is exactly the text below.

Before writing, the program checks the text against the competition
gate — UTF-8 text of 1 to 600 characters, not only whitespace — and
against the brief itself (exactly 100 words), and exits without
writing anything if a check fails. After writing it reads the file
back and checks the gate again on the text actually on disk.
"""

import os
import sys

MONOLOGUE = (
    "Hero. Stand there. Lower the torch, would you? The light... my eyes.\n"
    "\n"
    "I am Varric, lord of the Ninth Toll. Forty years I have kept this "
    "throne. Tolls and taxes and traitors at the gate, and none of them "
    "ever knocked. They all just... burst in. Like you. Swords first, "
    "manners never.\n"
    "\n"
    "Want the crown? Take it. It pinches. Velvet moth eaten, gold thin, "
    "and the weight of it... gods, it sits right here, behind my eyes.\n"
    "\n"
    "Before you swing, hero. One thing. The barge leaves at dawn. The "
    "dead will not row. Kill me tonight, and you must row."
)

GATE_MIN = 1
GATE_MAX = 600
WORD_TARGET = 100


def word_count(text):
    """Words are whitespace-separated tokens, the way the brief counts."""
    return len(text.split())


def gate_problems(text):
    """List every way `text` breaks the gate or the brief; empty means pass."""
    problems = []
    if not text.strip():
        problems.append("entry is blank or only whitespace")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        problems.append(
            "entry is %d characters, gate needs %d-%d"
            % (len(text), GATE_MIN, GATE_MAX)
        )
    if word_count(text) != WORD_TARGET:
        problems.append(
            "entry is %d words, brief asks for %d"
            % (word_count(text), WORD_TARGET)
        )
    return problems


def fail(problems, where=""):
    for problem in problems:
        print("gate failure%s: %s" % (where, problem), file=sys.stderr)
    return 1


def main():
    problems = gate_problems(MONOLOGUE)
    if problems:
        return fail(problems)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(MONOLOGUE)
    except OSError as exc:
        print("cannot write entry: %s" % exc, file=sys.stderr)
        return 1

    with open(path, encoding="utf-8") as handle:
        on_disk = handle.read()
    if on_disk != MONOLOGUE:
        print("entry on disk differs from the monologue", file=sys.stderr)
        return 1
    problems = gate_problems(on_disk)
    if problems:
        return fail(problems, " on disk")

    print(
        "Wrote entry.txt: %d characters (%d bytes), %d words"
        % (len(on_disk), len(on_disk.encode("utf-8")), word_count(on_disk))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
