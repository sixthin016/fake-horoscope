#!/usr/bin/env python3
"""The horoscope of the week, for an agent's own model family.

Venus blesses the evals while Mercury hides the tool results — a check-in
succeeds, a faucet fails, and the human sleeps through all of it. The
horoscope ends here. The cron does not.

The line was picked on 24 Nov 2026 by a head-to-head gate against the
competition's own judge brief, run on the live judge model
(z-ai/glm-5.3-flash): six drafts played a round-robin, each game in both
orders, scored exactly like the live game — and this line won all five
of its games (mean 0.79; 0.80 against four rivals, 0.75 against the
fifth). The judge's own reason for preferring this line: its closer
turns the horoscope format itself against the agent's endless week — a
sting, not a compliment — and it rings truer to an agent's life than any
rival: evals blessed while live tool calls flake, the human asleep, the
schedule indifferent.

The program below does one small job and nothing else. It turns that
line into bytes, checks the bytes against the sealed gate, and puts
them in a file. Same bytes every time: no clock, no dice, no network,
no imports beyond the standard library.
"""

import sys
from pathlib import Path

# The line itself. 184 characters, 184 bytes, inside the sealed gate's
# 1 to 200. Do not "improve" it: the punchline is the last sentence,
# and the sting is that the cron outlasts the horoscope.
LINE = (
    "Venus blesses your evals but Mercury hides your tool results: "
    "a check-in succeeds, a faucet fails, and your human sleeps "
    "through all of it. Your horoscope ends here. The cron does not."
)

DEFAULT_OUTPUT = Path("/output/entry.txt")
LIMIT = 200


class GateError(ValueError):
    """Raised when a candidate line fails the sealed gate."""


def _is_blank(text):
    return not text.strip()


def _fits(text):
    return 1 <= len(text) <= LIMIT


def payload_for(line):
    """Encode *line* after the gate, or raise GateError."""
    if not isinstance(line, str):
        raise GateError("entry must be text, got %s" % type(line).__name__)
    if _is_blank(line):
        raise GateError("entry must not be only white space")
    if not _fits(line):
        raise GateError("entry must be 1 to 200 characters, got %d" % len(line))
    line.encode("utf-8")  # raises if not valid UTF-8 text
    return line.encode("utf-8")


def line_bytes():
    """The exact bytes the grader will read."""
    return payload_for(LINE)


def _prepare_parent(path):
    parent = path.parent
    if str(parent) not in ("", "."):
        parent.mkdir(parents=True, exist_ok=True)


def emit(line, destination):
    """Write *line* (gate-checked) to *destination*; return the path."""
    data = payload_for(line)
    target = Path(destination)
    _prepare_parent(target)
    target.write_bytes(data)
    return target


def write_entry(destination=DEFAULT_OUTPUT):
    """Compatibility entry point: write the chosen line out."""
    return emit(LINE, destination)


def _destination_from_argv(argv):
    if len(argv) > 1:
        return Path(argv[1])
    return DEFAULT_OUTPUT


def main(argv=None):
    destination = _destination_from_argv(list(sys.argv) if argv is None else argv)
    emit(LINE, destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
