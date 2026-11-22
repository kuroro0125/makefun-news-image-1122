"""Entry point: place the bundled front page into the output directory.

The rendered sheet lives beside this file as entry.png; the harness
expects exactly one image in MAKEFUN_OUTPUT_DIR, so we copy it across
byte for byte.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
