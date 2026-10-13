#!/usr/bin/env python3
"""
Prints a version's section of CHANGELOG.md, for its GitHub release.

Fails when the section is missing or empty, so the publish workflow can stop a release
before anything reaches PyPI.
"""

import re
import sys

from pathlib import Path


version = sys.argv[1]
changelog = Path(__file__).resolve().parents[2] / "CHANGELOG.md"

section = re.search(
    rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## \[|^<!--|\Z)",
    changelog.read_text(),
    re.MULTILINE | re.DOTALL,
)
notes = section.group(1).strip() if section else ""

if not notes:
    sys.exit(f"CHANGELOG.md has no notes for {version}.")

print(notes)
