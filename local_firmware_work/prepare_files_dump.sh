#!/bin/bash
set -e

# Ścieżki
DUMP_DIR="../oblamatik_dump"
WORK_DIR="./temp_files"
ARCHIVE="files_payload.tar.gz"

echo "=== Przygotowanie archiwum firmware z zrzutu ==="

# 1. Przygotowanie struktury tymczasowej
echo "-> Tworzenie struktury..."
rm -rf "$WORK_DIR" "$ARCHIVE"
mkdir -p "$WORK_DIR/www"
mkdir -p "$WORK_DIR/etc/config"
mkdir -p "$WORK_DIR/etc/init.d"
mkdir -p "$WORK_DIR/etc/lighttpd"
mkdir -p "$WORK_DIR/etc/php"

# 2. Kopiowanie plików (z flagą -X dla pewności)
echo "-> Kopiowanie plików..."
# Używamy prostego cp bez -rX, aby uniknąć problemów z atrybutami,
# ale dodajemy -L (dereference symlinks) i -p (preserve mode/ownership) ostrożnie.
# Lepiej cp -R (standardowy recursive)
cp -R "$DUMP_DIR/inc" "$WORK_DIR/www/"
cp -R "$DUMP_DIR/html" "$WORK_DIR/www/"

if [ -f "$DUMP_DIR/config/lighttpd.conf" ]; then
    cp "$DUMP_DIR/config/lighttpd.conf" "$WORK_DIR/etc/lighttpd/"
    cp "$DUMP_DIR/config/"lighttpd.conf.* "$WORK_DIR/etc/lighttpd/" 2>/dev/null || true
fi

if [ -f "$DUMP_DIR/config/php.ini" ]; then
    cp "$DUMP_DIR/config/php.ini" "$WORK_DIR/etc/php/"
fi

# 3. Generowanie konfiguracji sieci
cat > "$WORK_DIR/etc/config/network" <<EOF
config interface 'loopback'
	option device 'lo'
	option proto 'static'
	option ipaddr '127.0.0.1'
	option netmask '255.0.0.0'

config globals 'globals'
	option ula_prefix 'fd19:9516:e83e::/48'

config device
	option name 'br-lan'
	option type 'bridge'
	list ports 'eth0'
	list ports 'eth1'

config interface 'lan'
	option device 'br-lan'
	option proto 'static'
	option ipaddr '192.168.1.1'
	option netmask '255.255.255.0'
	option ip6assign '60'

config interface 'wwan'
	option proto 'dhcp'
EOF

cat > "$WORK_DIR/etc/config/wireless" <<EOF
config wifi-device 'radio0'
	option type 'mac80211'
	option path 'platform/ar933x_wmac'
	option channel '1'
	option band '2g'
	option htmode 'HT20'
	option disabled '0'

config wifi-iface 'default_radio0'
	option device 'radio0'
	option network 'lan'
	option mode 'ap'
	option ssid 'Oblamatik_Setup'
	option encryption 'none'
EOF

# 4. Ustawianie uprawnień i pakowanie
echo "-> Pakowanie do $ARCHIVE..."
# Ustawiamy uprawnienia przed pakowaniem
# Najpierw katalogi na 755, pliki na 644
find "$WORK_DIR/www" -type d -exec chmod 755 {} \;
find "$WORK_DIR/www" -type f -exec chmod 644 {} \;
# Skrypty PHP muszą być wykonywalne
find "$WORK_DIR/www" -name "*.php" -exec chmod 755 {} \;

# Pakujemy bez atrybutów macOS (--no-xattrs jeśli dostępne, ale standardowy tar powinien być ok)
# Używamy COPYFILE_DISABLE=1 aby powstrzymać macOS przed dodawaniem ._ plików
export COPYFILE_DISABLE=1
tar -czf "$ARCHIVE" -C "$WORK_DIR" .

echo "-> Sprzątanie..."
rm -rf "$WORK_DIR"

echo "=== Gotowe! Archiwum $ARCHIVE utworzone ==="
