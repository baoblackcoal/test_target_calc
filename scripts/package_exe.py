"""Build a Windows executable for the pycalc CLI."""

import platform
import shutil
import sys
from pathlib import Path

from pycalc import __version__

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUILD_ROOT = ROOT / "build" / "pyinstaller"
ENTRYPOINT = ROOT / "scripts" / "pycalc_cli_entry.py"


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
    if final_exe.exists():
        final_exe.unlink()
    shutil.move(str(built_exe), str(final_exe))
    shutil.rmtree(temp_dist, ignore_errors=True)
    print(final_exe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
