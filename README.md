# pycalc

Minimal Python calculator product with:

- shared safe calculation engine
- non-interactive CLI
- interactive CLI REPL
- Flask web UI
- tests and GitHub Actions workflows

## Development

Create a virtual environment and install dev dependencies:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -U pip
.venv\Scripts\python -m pip install -e .[dev]
```

Run quality checks:

```powershell
python scripts/check.py
```

## Usage

CLI:

```powershell
python -m pycalc.cli "1 + 2 * 3"
python -m pycalc.cli --repl
```

Web:

```powershell
python -m pycalc.web.app
```
