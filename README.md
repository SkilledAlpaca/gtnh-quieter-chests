<p align="center">
  <img src="pack.png" alt="Quieter Chests pack icon" width="160">
</p>

<h1 align="center">GTNH Quieter Chests</h1>

Resource packs for Minecraft 1.7.10 (GregTech: New Horizons) that lower the volume of the chest open and close sounds.

## Download

Download one pack from the [latest release](https://github.com/SkilledAlpaca/gtnh-quieter-chests/releases/latest):

| File | Chest volume |
| --- | --- |
| `quieter-chests-0.75.zip` | 75% |
| `quieter-chests-0.5.zip` | 50% |
| `quieter-chests-0.25.zip` | 25% |
| `quieter-chests-0.zip` | Muted |

## Install

1. Copy the zip into the `resourcepacks` folder of your instance.
2. In Minecraft, go to **Options > Resource Packs** and move the pack to the selected column.

## Build

To build all four packs into `dist/`, run:

```bash
python3 build.py
```

The build needs Python 3 and no other dependencies. Pushing a `v*` tag builds the packs in GitHub Actions and attaches them to a new release.

The packs opt in to the [GTNH resource pack update notifier](https://wiki.gtnewhorizons.com/wiki/Resource_Packs#Update_Notifier). The tag sets the pack version, so use two-part numeric tags such as `v1.1`. Each release also carries the `gtnh-pack-update.json` asset that the notifier requires.

The 25%, 50%, and 75% packs override `sounds.json`. The muted pack replaces the two sound files with `silence.ogg`, because Minecraft 1.7.10 rejects a `sounds.json` volume of 0.
