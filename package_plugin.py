#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Release packager for IngeTrazo Organize Toolbar Plugin."""
from __future__ import annotations

import os
import shutil
import zipfile
from pathlib import Path

VERSION = "1.0.0"
PLUGIN_FILE = "organize_toolbar.py"
PACKAGE_NAME = f"ingetrazo-organize-toolbar-v{VERSION}"

def build() -> None:
    root = Path(__file__).resolve().parent
    dist = root / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir(parents=True, exist_ok=True)

    zip_path = dist / f"{PACKAGE_NAME}.zip"
    print(f"Creating release package: {zip_path.name}...")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        # Include the plugin file at the root of the archive
        z.write(root / PLUGIN_FILE, arcname=PLUGIN_FILE)
        z.write(root / "README.md", arcname="README.md")
        z.write(root / "LICENSE", arcname="LICENSE")
        if (root / "assets" / "preview.png").exists():
            z.write(root / "assets" / "preview.png", arcname="assets/preview.png")

    print(f"Successfully packaged {zip_path.name} ({os.path.getsize(zip_path)} bytes)")
    print(f"Path: {zip_path}")

if __name__ == "__main__":
    build()
