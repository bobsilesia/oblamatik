# Use Ubuntu 22.04 for newer OpenWrt 23.05 tools
# Explicitly target linux/amd64 to ensure correct emulation on Apple Silicon (M1/M2/M3)
FROM --platform=linux/amd64 ubuntu:22.04

# Set environment variables to non-interactive (prevents prompts during package installation)
ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y \
    build-essential \
    libncurses5-dev \
    zlib1g-dev \
    gawk \
    git \
    gettext \
    libssl-dev \
    xsltproc \
    wget \
    unzip \
    python3 \
    python3-distutils \
    file \
    rsync \
    libc6:i386 \
    libstdc++6:i386 \
    && rm -rf /var/lib/apt/lists/*

# Fix for "ld.so: object 'runas.so' from LD_PRELOAD cannot be preloaded"
# This is caused by ImageBuilder tools being 32-bit or having weird LD_PRELOAD behavior in Docker
# Installing 32-bit libs above usually helps, but we also ensure env is clean.
RUN unset LD_PRELOAD

# Download and extract ImageBuilder (OpenWrt 23.05.2 for ath79/generic - supports Carambola 2)
WORKDIR /builder
RUN wget https://downloads.openwrt.org/releases/23.05.2/targets/ath79/generic/openwrt-imagebuilder-23.05.2-ath79-generic.Linux-x86_64.tar.xz \
    && tar xJvf openwrt-imagebuilder-*.tar.xz --strip-components=1 \
    && rm openwrt-imagebuilder-*.tar.xz

# Copy custom files archive (workaround for permission errors on macOS)
ADD files_payload.tar.gz files/

# Packages to include in the firmware
# Updated for OpenWrt 23.05 (PHP 8.1/8.2 included)
# Removed php8-mod-iconv as it causes build failures on some platforms/emulation
# Excluding ppp packages as they fail in Docker emulation (Error 255)
# Removed php8-mod-json (might be built-in or causing issues)
ENV PACKAGES="luci -ppp -ppp-mod-pppoe -luci-proto-ppp php8-cgi php8-mod-curl lighttpd lighttpd-mod-cgi"

# Build the firmware
# Profile: 8dev_carambola2 (confirmed via make info)
# Using V=s to debug any potential package issues
RUN make image PROFILE="8dev_carambola2" PACKAGES="$PACKAGES" FILES="files/" V=s

# The output will be in bin/targets/ath79/generic/
