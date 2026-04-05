"""Build a Windows executable for the pycalc packaged app."""

import platform
import shutil
import sys
import time
from pathlib import Path

from pycalc import __version__

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD_ROOT = ROOT / "build" / "pyinstaller"
ENTRYPOINT = ROOT / "scripts" / "pycalc_cli_entry.py"
TEMPLATES = ROOT / "src" / "pycalc" / "templates"


def normalize_windows_arch(raw_arch: str) -> str:
    normalized = raw_arch.lower()
    if normalized in {"amd64", "x86_64"}:
        return "x64"
    if normalized in {"arm64", "aarch64"}:
        return "arm64"
    if normalized in {"x86", "i386", "i686"}:
        return "x86"
    return normalized


def artifact_path() -> Path:
    arch = normalize_windows_arch(platform.machine())
    return DIST / f"pycalc-cli-{__version__}-windows-{arch}.exe"


def remove_with_retries(path: Path, attempts: int = 10, delay_seconds: float = 1.0) -> None:
    if not path.exists():
        return

    last_error: PermissionError | None = None
    for _ in range(attempts):
        try:
            path.unlink()
            return
        except PermissionError as error:
            last_error = error
            time.sleep(delay_seconds)

    if last_error is not None:
        raise last_error


def main() -> int:
    if sys.platform != "win32":
        print("Windows executable packaging is only supported on Windows.")
        return 1

    try:
        import PyInstaller.__main__
    except ImportError:
        print(
            "PyInstaller is not installed. "
            "Install dev dependencies with `pip install -e .[dev]`."
        )
        return 1

    temp_dist = DIST / "pyinstaller"
    if temp_dist.exists():
        shutil.rmtree(temp_dist)
    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)

    DIST.mkdir(exist_ok=True)

    PyInstaller.__main__.run(
        [
            "--noconfirm",
            "--clean",
            "--onefile",
            "--name",
            "pycalc-cli",
            "--add-data",
            f"{TEMPLATES};pycalc/templates",
            "--paths",
            str(ROOT / "src"),
            "--distpath",
            str(temp_dist),
            "--workpath",
            str(BUILD_ROOT / "work"),
            "--specpath",
            str(BUILD_ROOT / "spec"),
            str(ENTRYPOINT),
        ]
    )

    built_exe = temp_dist / "pycalc-cli.exe"
    final_exe = artifact_path()
    remove_with_retries(final_exe)
    shutil.move(str(built_exe), str(final_exe))
    shutil.rmtree(temp_dist, ignore_errors=True)
    print(final_exe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
