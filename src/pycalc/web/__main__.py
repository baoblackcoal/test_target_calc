"""Run the pycalc web app as a module."""

from pycalc.web.app import create_app

if __name__ == "__main__":
    create_app().run(debug=True)
