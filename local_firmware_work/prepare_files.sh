#!/bin/bash
set -e

# Define paths
REPO_DIR="repo"
FILES_DIR="files"

# Create destination structure
mkdir -p "$FILES_DIR/etc/config"
mkdir -p "$FILES_DIR/etc/lighttpd"
mkdir -p "$FILES_DIR/etc/avahi/services"
mkdir -p "$FILES_DIR/www/html"
mkdir -p "$FILES_DIR/root/cron"

echo "Preparing filesystem structure..."

# 1. Map Configuration Files
# Network configuration
cp "$REPO_DIR/www/config/network" "$FILES_DIR/etc/config/network"

# System users/groups (CAUTION: Overwrites existing!)
cp "$REPO_DIR/www/config/passwd" "$FILES_DIR/etc/passwd"
cp "$REPO_DIR/www/config/shadow" "$FILES_DIR/etc/shadow"
cp "$REPO_DIR/www/config/group" "$FILES_DIR/etc/group"

# Lighttpd configuration
cp "$REPO_DIR/www/config/lighttpd.conf.auth" "$FILES_DIR/etc/lighttpd/lighttpd.conf"
# Ensure document-root points to /www/html in the conf file (it does in repo)

# PHP Configuration
cp "$REPO_DIR/www/config/php.ini" "$FILES_DIR/etc/php.ini"

# System startup
cp "$REPO_DIR/www/config/rc.local" "$FILES_DIR/etc/rc.local"

# Upgrade configuration
cp "$REPO_DIR/www/config/sysupgrade.conf" "$FILES_DIR/etc/sysupgrade.conf"

# Avahi/Zeroconf Services
if [ -f "$REPO_DIR/www/config/http.service" ]; then
    cp "$REPO_DIR/www/config/http.service" "$FILES_DIR/etc/avahi/services/http.service"
fi
if [ -f "$REPO_DIR/www/config/https.service" ]; then
    cp "$REPO_DIR/www/config/https.service" "$FILES_DIR/etc/avahi/services/https.service"
fi

# 2. Map Web Content
# Copy entire html directory to /www/html
cp -r "$REPO_DIR/www/html/"* "$FILES_DIR/www/html/"

# Copy include files
mkdir -p "$FILES_DIR/www/inc"
cp -r "$REPO_DIR/www/inc/"* "$FILES_DIR/www/inc/"

# 3. Map Cron Scripts
# It's unclear where cron scripts go, placing in /root/cron for safety and manual execution
cp -r "$REPO_DIR/www/cron/"* "$FILES_DIR/root/cron/"

# 4. Set Permissions
chmod +x "$FILES_DIR/etc/rc.local"
chmod 600 "$FILES_DIR/etc/shadow"
chmod 644 "$FILES_DIR/etc/passwd"
chmod 644 "$FILES_DIR/etc/group"

echo "Filesystem prepared in '$FILES_DIR/'."
