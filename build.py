#!/usr/bin/env python3
"""Build the Quieter Chests resource packs into dist/, one zip per volume."""

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VOLUMES = ["0.75", "0.5", "0.25", "0"]
SOUNDS = ["chestopen", "chestclosed"]
# GTNH version lines the packs support, for the GTNHLib update notifier.
GAME_VERSION = "2.8.X;2.9.X"
GITHUB_OWNER = "SkilledAlpaca"
GITHUB_REPO = "gtnh-quieter-chests"
# Fixed timestamp so the same commit always produces byte-identical zips.
EPOCH = (2026, 10, 3, 0, 0, 0)


def pack_files(volume, version):
    description = "Muted Chests" if volume == "0" else f"Quieter Chests ({volume} Volume)"
    mcmeta = {
        "pack": {"pack_format": 1, "description": description},
        "gtnh_resource_pack_updater": {
            "schema": 1,
            "pack_name": description,
            "pack_version": version,
            "pack_game_version": GAME_VERSION,
            "source": {"type": "github_releases", "owner": GITHUB_OWNER, "repo": GITHUB_REPO},
        },
    }
    files = {
        "pack.mcmeta": json.dumps(mcmeta, indent=2).encode(),
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
    # The release workflow passes the tag as the version; local builds get "0".
    version = sys.argv[1] if len(sys.argv) > 1 else "0"
    DIST.mkdir(exist_ok=True)
    for volume in VOLUMES:
        path = DIST / f"quieter-chests-{volume}.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(pack_files(volume, version).items()):
                info = zipfile.ZipInfo(name, EPOCH)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, data)
        print(path.relative_to(ROOT))
    # GTNHLib ignores releases that lack this asset.
    update = {"schema": 1, "pack_game_version": GAME_VERSION, "pack_version": version}
    (DIST / "gtnh-pack-update.json").write_text(json.dumps(update, indent=2) + "\n")


if __name__ == "__main__":
    main()
