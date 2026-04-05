from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pycalc.engine import calculate
from pycalc.web.app import create_app

ROOT = Path(__file__).resolve().parents[1]
EXPRESSIONS = ["1 + 2 * 3", "(1 + 2) / 4", "10 / 0", "1 + * 2"]


def _cli_outcome(expression: str) -> tuple[bool, str]:
    completed = subprocess.run(
        [sys.executable, "-m", "pycalc.cli", expression],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode == 0:
        return True, completed.stdout.strip()
    return False, completed.stderr.strip()


def _web_outcome(expression: str) -> tuple[bool, str]:
    app = create_app()
    client = app.test_client()
    response = client.post("/calculate", data={"expression": expression})
    body = response.get_data(as_text=True)
    result = calculate(expression)
    if result.ok:
        assert result.value_text is not None
        assert result.value_text in body
        return True, result.value_text
    assert result.error_message is not None
    assert result.error_message in body
    return False, result.error_message


def test_cli_and_web_match_engine_behavior() -> None:
    for expression in EXPRESSIONS:
        engine = calculate(expression)
        cli_ok, cli_payload = _cli_outcome(expression)
        web_ok, web_payload = _web_outcome(expression)

        assert cli_ok == web_ok == engine.ok
        if engine.ok:
            assert cli_payload == web_payload == engine.value_text
        else:
            assert cli_payload == web_payload == engine.error_message
