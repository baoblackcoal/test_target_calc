"""Run the local quality gate for pycalc."""

from __future__ import annotations

import subprocess
import sys


def run_step(*args: str) -> int:
    print(f"> {' '.join(args)}")
    completed = subprocess.run(args, check=False)
    return completed.returncode


def main() -> int:
    steps = [
        (sys.executable, "-m", "ruff", "check", "."),
        (sys.executable, "-m", "pytest"),
    ]

    for step in steps:
        exit_code = run_step(*step)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
