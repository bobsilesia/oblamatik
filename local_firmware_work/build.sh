#!/bin/bash
set -e

echo "=== Oblamatik Firmware Builder ==="
echo "This script will build a custom OpenWrt firmware image for the Carambola 2 module."
echo "It requires Docker to be installed and running."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: docker could not be found. Please install Docker first."
    exit 1
fi

# Prepare files
echo "Step 1: Preparing file structure..."
# Generujemy archiwum z plików zrzutu (workaround na uprawnienia)
./prepare_files_dump.sh
echo "Using files payload archive (files_payload.tar.gz)..."

# Build the Docker image
echo "Step 2: Building Docker image for Apple Silicon (M1/M2/M3) via Rosetta 2..."
# Force linux/amd64 platform because OpenWrt ImageBuilder binaries are x86_64
# Using --progress=plain to show build output (including profile list from 'make info')
docker build --platform linux/amd64 --progress=plain -t oblamatik_firmware .

# Extract firmware
echo "Step 3: Extracting firmware image..."
# Create a temporary container
CONTAINER_ID=$(docker create --platform linux/amd64 oblamatik_firmware)
mkdir -p output
docker cp "$CONTAINER_ID:/builder/bin/targets/ath79/generic/" ./output/
docker rm "$CONTAINER_ID"

echo ""
echo "=== Build Complete ==="
echo "Firmware images are located in 'output/generic/'."
echo "Look for: openwrt-23.05.2-ath79-generic-8dev_carambola2-squashfs-sysupgrade.bin"
echo ""
echo "To flash via SSH (if current system is OpenWrt):"
echo "  scp output/generic/openwrt-23.05.2-ath79-generic-8dev_carambola2-squashfs-sysupgrade.bin root@<IP>:/tmp/"
echo "  ssh root@<IP> 'sysupgrade -n /tmp/openwrt-23.05.2-ath79-generic-8dev_carambola2-squashfs-sysupgrade.bin'"
echo ""
echo "WARNING: This will overwrite your current configuration. Proceed with caution."
