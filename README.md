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

Build release artifacts:

```powershell
python -m build
python scripts/package_web.py
python scripts/package_exe.py
```

`package_exe.py` must run on Windows and emits `dist/pycalc-cli-<version>-windows-<arch>.exe`.
Use `python scripts/smoke_test_exe.py dist\\pycalc-cli-<version>-windows-<arch>.exe` to verify both CLI
and web mode in one pass.

## Usage

CLI:

```powershell
python -m pycalc.cli "1 + 2 * 3"
python -m pycalc.cli --repl
python -m pycalc.cli --web --host 127.0.0.1 --port 5000
dist\pycalc-cli-0.1.4-windows-x64.exe "1 + 2 * 3"
dist\pycalc-cli-0.1.4-windows-x64.exe --web --host 127.0.0.1 --port 5000
```

Web:

```powershell
python -m pycalc.web.app
```
