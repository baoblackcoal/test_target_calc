"""PyInstaller entry point for the pycalc packaged app."""

from pycalc.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
