"""Build a deployable web service source artifact."""

from __future__ import annotations

import shutil
from pathlib import Path

from pycalc import __version__

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STAGING = DIST / f"pycalc-web-service-{__version__}"


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> int:
    if STAGING.exists():
        shutil.rmtree(STAGING)

    DIST.mkdir(exist_ok=True)

    copy_path(ROOT / "README.md", STAGING / "README.md")
    copy_path(ROOT / "pyproject.toml", STAGING / "pyproject.toml")
    copy_path(ROOT / "MANIFEST.in", STAGING / "MANIFEST.in")
    copy_path(ROOT / "src", STAGING / "src")

    run_script = STAGING / "run-web.ps1"
    run_script.write_text(
        "python -m pip install .\npython -m pycalc.web\n",
        encoding="utf-8",
    )

    archive_base = DIST / f"pycalc-web-service-{__version__}"
    archive_path = shutil.make_archive(str(archive_base), "zip", root_dir=STAGING)
    shutil.rmtree(STAGING)
    print(archive_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
