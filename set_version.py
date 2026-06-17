#!/usr/bin/env python3
"""Set the apworld version across every file that hardcodes it.

The version is written explicitly in three places that must stay in sync,
or the client refuses to connect (see the version gate in Sly3Client.py):
  - Sly 3.yaml          'Sly 3: Honor Among Thieves': X.Y.Z
  - archipelago.json    "world_version": "X.Y.Z"
  - Sly3Client.py       self.version = [X, Y, Z]

Usage: ./set_version.py 0.1.3
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def replace(path: Path, pattern: str, repl: str) -> None:
  text = path.read_text()
  new_text, count = re.subn(pattern, repl, text)
  if count != 1:
    raise SystemExit(
      f"error: expected exactly 1 version match in {path.name}, found {count}"
    )
  path.write_text(new_text)
  print(f"updated {path.name}")


def main() -> None:
  if len(sys.argv) != 2:
    raise SystemExit("usage: set_version.py <X.Y.Z>")

  version = sys.argv[1]
  match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
  if not match:
    raise SystemExit(f"error: version must look like X.Y.Z, got '{version}'")
  major, minor, patch = match.groups()

  replace(
    ROOT / "Sly 3.yaml",
    r"('Sly 3: Honor Among Thieves': )\d+\.\d+\.\d+",
    rf"\g<1>{version}",
  )
  replace(
    ROOT / "archipelago.json",
    r'("world_version": ")\d+\.\d+\.\d+(")',
    rf"\g<1>{version}\g<2>",
  )
  replace(
    ROOT / "Sly3Client.py",
    r"(self\.version = )\[\d+\s*,\s*\d+\s*,\s*\d+\]",
    rf"\g<1>[{major},{minor},{patch}]",
  )

  print(f"version set to {version}")


if __name__ == "__main__":
  main()
