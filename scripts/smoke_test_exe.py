"""Smoke-test the packaged Windows executable."""

from __future__ import annotations

import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def run_help_check(executable: Path) -> None:
    completed = subprocess.run(
        [str(executable), "--help"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"--help failed with exit code {completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    if "--web" not in completed.stdout:
        raise RuntimeError(f"Expected --web help text, got:\n{completed.stdout}")


def run_web_check(executable: Path, port: int = 8765) -> None:
    process = subprocess.Popen(
        [str(executable), "--web", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        deadline = time.time() + 60
        url = f"http://127.0.0.1:{port}/"
        while time.time() < deadline:
            if process.poll() is not None:
                stdout, stderr = process.communicate(timeout=5)
                raise RuntimeError(
                    f"web mode exited early with code {process.returncode}\n"
                    f"stdout:\n{stdout}\n"
                    f"stderr:\n{stderr}"
                )
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    body = response.read().decode("utf-8", errors="replace")
                if "pycalc" in body and 'value="1+2"' in body:
                    return
            except (OSError, urllib.error.URLError):
                time.sleep(1)
        raise RuntimeError("Executable web mode did not become ready within 60 seconds.")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if len(args) != 1:
        print("Usage: python scripts/smoke_test_exe.py <path-to-exe>", file=sys.stderr)
        return 2

    executable = Path(args[0]).resolve()
    if not executable.is_file():
        print(f"Executable not found: {executable}", file=sys.stderr)
        return 2

    run_help_check(executable)
    run_web_check(executable)
    print(f"smoke-tested {executable}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
