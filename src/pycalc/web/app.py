"""Flask app entry point for pycalc."""

from __future__ import annotations

import os

from flask import Flask, render_template, request, session

from pycalc.engine import CalculationResult, calculate


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates")
    app.config["SECRET_KEY"] = os.environ.get("PYCALC_SECRET_KEY", "dev-secret-key")

    @app.get("/")
    def index() -> str:
        return render_template(
            "index.html",
            expression="",
            result=None,
            history=_get_history(),
        )

    @app.post("/calculate")
    def run_calculation() -> str:
        expression = request.form.get("expression", "")
        result = calculate(expression)
        _append_history(result)
        return render_template(
            "index.html",
            expression=expression,
            result=result,
            history=_get_history(),
        )

    return app


def _append_history(result: CalculationResult) -> None:
    history = _get_history()
    history.insert(
        0,
        {
            "expression": result.expression,
            "value_text": result.value_text,
            "error_message": result.error_message,
        },
    )
    session["history"] = history[:10]


def _get_history() -> list[dict[str, str | None]]:
    history = session.get("history")
    if isinstance(history, list):
        return history
    return []


if __name__ == "__main__":
    create_app().run(debug=True)
