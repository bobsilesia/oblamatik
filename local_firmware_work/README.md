# Oblamatik Firmware Build Kit

This directory contains tools to build a custom OpenWrt firmware image for the Oblamatik/Viega/Crosswater WLAN module (Carambola 2).

## Prerequisites
- Docker installed on your machine.
- Internet connection (to download OpenWrt ImageBuilder).

## How to Build
1. Open a terminal in this directory.
2. Run the build script:
   ```bash
   ./build.sh
   ```
3. The script will:
   - Prepare the file structure from the local `repo/` clone.
   - Download the official OpenWrt ImageBuilder (21.02.7).
   - Inject the Oblamatik PHP/Lighttpd files.
   - Compile the firmware image.

## Output
The resulting firmware binary (`.bin`) will be placed in `output/generic/`.
Look for a file named like `openwrt-ath79-generic-8devices_carambola2-squashfs-sysupgrade.bin`.

## Flashing
Upload the `.bin` file to your device via SCP to `/tmp/` and run `sysupgrade -n /tmp/<filename>`.
**Warning:** This will overwrite your current configuration and data. Ensure you have backups.
