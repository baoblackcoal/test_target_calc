"""Flask app entry point for pycalc."""

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        return "pycalc web scaffold ready"

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
