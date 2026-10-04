#!/usr/bin/env python3
"""Build the Quieter Chests resource packs into dist/, one zip per volume."""

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VOLUMES = ["0.75", "0.5", "0.25", "0"]
SOUNDS = ["chestopen", "chestclosed"]
# Fixed timestamp so the same commit always produces byte-identical zips.
EPOCH = (2026, 10, 3, 0, 0, 0)


def pack_files(volume):
    description = "Muted Chests" if volume == "0" else f"Quieter Chests ({volume} Volume)"
    files = {
        "pack.mcmeta": json.dumps({"pack": {"pack_format": 1, "description": description}}).encode(),
        "pack.png": (ROOT / "pack.png").read_bytes(),
    }
    if volume == "0":
        # Minecraft 1.7.10 rejects a sounds.json volume of 0, so the muted
        # pack replaces the sound files with silence instead.
        silence = (ROOT / "silence.ogg").read_bytes()
        for sound in SOUNDS:
            files[f"assets/minecraft/sounds/random/{sound}.ogg"] = silence
    else:
        sounds = {
            f"random.{sound}": {
                "category": "block",
                "replace": True,
                "sounds": [{"name": f"random/{sound}", "volume": float(volume)}],
            }
            for sound in SOUNDS
        }
        files["assets/minecraft/sounds.json"] = (json.dumps(sounds, indent=2) + "\n").encode()
    return files


def main():
    DIST.mkdir(exist_ok=True)
    for volume in VOLUMES:
        path = DIST / f"quieter-chests-{volume}.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(pack_files(volume).items()):
                info = zipfile.ZipInfo(name, EPOCH)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, data)
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
