from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pycalc.cli", *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_non_interactive_mode_returns_result() -> None:
    completed = run_cli("1 + 2 * 3")
    assert completed.returncode == 0
    assert completed.stdout.strip() == "7"
    assert completed.stderr == ""


def test_non_interactive_mode_returns_failure_for_invalid_expression() -> None:
    completed = run_cli("1 + * 3")
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert "Expression syntax is invalid." in completed.stderr


def test_help_is_available() -> None:
    completed = run_cli("--help")
    assert completed.returncode == 0
    assert "interactive" in completed.stdout


def test_repl_accepts_multiple_inputs_and_recovers_from_errors() -> None:
    completed = run_cli("--repl", input_text="1 + 1\n1 / 0\n(3 + 1) * 2\nexit\n")
    assert completed.returncode == 0
    assert "pycalc REPL" in completed.stdout
    assert "2" in completed.stdout
    assert "Division by zero is not allowed." in completed.stdout
    assert "8" in completed.stdout
    assert "Bye." in completed.stdout
