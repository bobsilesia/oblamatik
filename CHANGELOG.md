## v4.3.9
- Fix: Improved MAC address parsing in `IoT Hardware Vendor` sensor to handle formats with hyphens (e.g., `C4-93-00...`) instead of colons, ensuring 8devices/Carambola2 modules are correctly identified.

## v4.3.8
- Maintenance: Changed log level from WARNING to INFO when a device reports >99°C (missing temperature sensor), to reduce log noise.

## v4.3.7
- Hotfix: Resolved `IndentationError` in `sensor.py` that caused integration setup failure (and subsequent `import_module` blocking call error).
- **Note**: Please skip v4.3.6 and upgrade directly to v4.3.7.

## v4.3.6 [BROKEN]
- ⚠️ **DO NOT USE** - This release contains a syntax error.
- Docs: Added prominent `DISCLAIMER & SAFETY WARNING` to README, HACS info, and Wiki. This integration controls physical hardware; improper use may lead to unintended water flow or scalding. Use at your own risk.

## v4.3.5
- Feature: Added `Connection Reliability` sensor (diagnostic) to track API success rate %.
- Docs: Added `Diagnostics.md` to Wiki covering all diagnostic sensors (Ping, Reliability, Signal, Vendor).

## v4.3.4
- Feature: Added `IoT Hardware Vendor` sensor (diagnostic) which detects the Wi-Fi module manufacturer (e.g. 8devices, Espressif, RPi) based on MAC address OUI.

## v4.3.3
- Feature: Added `Ping` sensor (diagnostic) to monitor API latency.
- Fix: Improved `Wi-Fi Signal (dBm)` logic to handle both RSSI (negative dBm) and Bars/Quality (0-5 or 0-100 scale) correctly.

## v4.3.2
- Chore: Remove `device_backup/` folder from repository to ensure compliance with HACS repository rules (clean repo without vendor binaries).
- Docs: Add `info.md` for better HACS integration presentation.

## v4.3.1
- Fix: Restore original Oblamatik logo and icon (from `assets/readme_logo.jpg`) for HACS branding, replacing the temporary KWC logo.

## v4.3.0
- Feature: HACS Compliance - added `hacs.json`, `images/` folder with logo/icon, and GitHub Actions workflows for HACS validation.
- Docs: Updated `README.md` with installation instructions for HACS and manual methods.
- Chore: Prepare repository for submission to HACS Default repository list.

## v4.2.10
- Fix: Use valid `mdi:wifi` icon for Wi-Fi Signal (dBm) sensor (previously invalid `mdi:wifi-strength`).

## v4.2.9
- Fix: Brand/Model diagnostics now read directly from `/api/` (uses `vendor` and `model` fields) with fallbacks.
- Fix: Device Registry manufacturer/model now prefer `/api/` so they match device-reported values (e.g. Crosswater/Digital, Oblamatik AG/Twinlevel, Viega/Trio-E).

## v4.2.8
- Fix: Quick Action 1/2/3 now reads presets from `/api/tlc/1/quick/{n}/` and keeps flow alive during the computed runtime.
- Improvement: Runtime is derived from device preset `amount` and `flow` (amount/flow*60), then auto-stops the flow.

## v4.2.7
- Revert: Wi‑Fi sensors restored to Diagnostic category (no header chips) per user decision.
- Feature: Enforce Quick Action 1/2/3 duration — read presets when available and explicitly set temperature/flow, then auto‑stop after configured seconds (fallback 30s).

## v4.2.6
- Fix: Move Wi‑Fi Signal sensors out of Diagnostic category, so Home Assistant can render signal chips in the device header.
- Maintenance: No functional changes to polling. dBm/quality fallbacks remain as in 4.2.5.

## v4.2.5
- Fix: Ensure Wi‑Fi Signal sensors render in device header by setting device class also for percentage sensor and adding fallback to `/api/info`.
- Improvement: More robust dBm/quality derivation when `/api/wlan` scan is unavailable (AP/Ethernet).

## v4.2.4
- Feature: Auto-populate manufacturer (vendor) in Device Registry during setup.
- Feature: Wi‑Fi Signal (dBm) sensor with SIGNAL_STRENGTH device class (enabled by default) to show in device header.
- Note: dBm uses `/api/wlan` and falls back from `rawsignal` if needed.

## v4.2.3
- **Docs**: Changed README logo path to absolute URL (raw.githubusercontent.com) to fix visibility issues in HACS.

## v4.2.2
- **Branding Fix**: Adjusted logo and icon rendering (added shadow) to improve visibility in HACS on both light and dark themes.
- **Assets**: Regenerated all branding assets with improved contrast.

## v4.2.1
- **Branding**: Updated integration logo and icons to use Garamond font in light gray.
- **Assets**: Added high-resolution (`@2x`) logo and icon variants for HACS and Home Assistant brands.
- **Docs**: Updated README to use the specific logo requested by the user.
- **CI**: Fixed branding workflow dependencies and asset generation logic.

## v4.2.0
- Feature: Added service `oblamatik.force_refresh` to refresh all or a single device (host parameter).
- Feature: Added Force Refresh button entity per device (Diagnostics) to trigger refresh from UI.
- Improvement: Always perform initial coordinator refresh also in "minimal" polling mode.
- Improvement: Sensors now seed coordinator cache on direct HTTP fallback and include guarded verbose debug logs.
- Options: Added `verbose_debug` toggle in integration Options to enable extra debug logs.
- Docs: README already centers logo; branding unchanged.

## v4.1.9
- Docs: Align README badges between GitHub and HACS (remove Release Date, Issues, PRs, Last Commit).
- Rules: Add README badges + HACS icon policy to project rules.
- No Breaking Changes.

## v4.1.8
- **Fix**: Improved `IoT Serial Number` detection for stock firmware (e.g. 1.0-4.03).
- **Feature**: Added fallback to `/getserial.php` (fw_printenv) for reading serial number.
- **Feature**: Added fallback to MAC Address (formatted as serial) if no other serial number is found, ensuring a unique identifier is always available.
- **No Breaking Changes**: Existing entities unchanged.

## v4.1.7
- Fix: Force stable entity_id for Water Usage Reset in single-device setups (button.oblamatik_water_usage_reset).
- No Breaking Changes.

## v4.1.6
- Fix: Ensure Water Usage Reset button appears by adding base entity mapping in strings.json.
- Docs: Minor README clarification about Water Usage Reset availability.
- No Breaking Changes.

## v4.1.5
- New: Added button.oblamatik_water_usage_reset to immediately set flow to 0 and refresh sensors.
- Docs: Wiki updated (Entities & Controls) with Water Usage Reset description and usage scenarios.
- No Breaking Changes: Existing entities and APIs unchanged; optional control addition.

## v4.1.4
- **Change**: Changed default polling mode to **Normal** (5 minutes). "Minimal" mode is now optional.
- **Docs**: Added detailed warnings in Wiki about RS232 communication hanging due to excessive polling.
- **Improvement**: Simplified sensor logic in code (`sensor.py`) - always returns available data from coordinator.

## v4.1.3
- **Improvement**: Ulepszono obsługę przeładowania integracji (`async_unload_entry`) — czyszczenie `hass.data` (devices, coordinators, options) przy kliknięciu "Reload" w UI.
- **Note**: Aktualizacja kodu integracji (np. przez HACS) nadal wymaga restartu HA ze względu na architekturę platformy.

## v4.1.2
- Fix: Resolved `awk` syntax error in release workflow (`in` variable collision) to ensure automated releases.
- No changes to integration code or functionality.

## v4.1.1
- Feature: Added Integration Options UI for Polling Mode (`minimal` / `normal`) and Polling Interval (minutes).
- Improvement: Options are now clearly separated from connection settings (Host/Port stay in initial Config Flow).
- Docs: GitHub Wiki cleaned up to English-only with an expanded "Polling Modes" explanation.
- No Breaking Changes: entities and API remain compatible with 4.1.0 and 4.0.9.

## v4.1.0
- Improvement: Stabilized Release Notes automation — the release body update uses robust CHANGELOG section extraction (line-number based) and supports manual `workflow_dispatch` with a `tag` input.
- Fix: Resolved quoting issues for multi-line `awk/sed` programs on GitHub Actions runners that caused errors and empty release bodies.
- CI: Verified locally with `ruff format`, `ruff check`, and `mypy`; CI tool versions are pinned per repository rules.
- No Breaking Changes: no changes to API/entities; only release process improvements.

## v4.0.9
- **Fix**: Ograniczono odpytywanie modułów WLAN (tryb „Minimalny” bez cyklicznych zapytań).
- **Improvement**: Dodano tryb „Normalny” z konfigurowalnym interwałem oraz centralny DataUpdateCoordinator; po akcjach użyto kontrolowanego `request_refresh` zamiast wielokrotnego `update_entity`.
- **Impact**: Zmniejszone obciążenie HTTP/RS232 i poprawiona responsywność fizycznych przycisków.
- **Docs**: Wiki uzupełniona o sekcję „Polling Modes” (PL/EN) w Entities & Controls.

## v4.0.8
- **Fix**: Rozdzielenie źródeł numerów seryjnych:
  - IoT Serial pobierany wyłącznie z `serial_number_iot` (moduł WLAN).
  - Zwykły Serial pozostaje oddzielnym sensorem (`serial_number`/`serial`) — jednostka wykonawcza (procesor wody).
- **Improvement**: IoT Serial ma wielopoziomowy fallback po endpointach (`inc/info.txt`, `api/index.php?url=info`, `api/info`, `api/tlc/1/`, `api/tlc/1/state/`) bez mieszania pól.
- **No Breaking Changes**: nazwy encji bez zmian; zachowanie spójne na różnych firmware (Crosswater/KWC/Viega).

## v4.0.7
- **Docs-only**: Usprawnienia nawigacji i kontekstu:
  - Language toggles (PL/EN) na wszystkich stronach wiki + kotwice #pl/#en.
  - Widoczny sidebar z linkami PL/EN dla początkujących.
  - Sekcja „Getting Started” na Home (PL/EN).
  - Wzmianki i linki do projektów: Homebridge (Axel Terizaki) oraz Carambola (Roel Broersma) — README i Home/Hardware.
- **No Breaking Changes**: brak zmian w API/funcjonalności integracji.

## v4.0.6
- **Docs**: Dwujęzyczna wiki (PL + EN) rozszerzona o:
  - FAQ oraz FAQ Highlights na stronie głównej (skrótowe automatyzacje: Guarded Fill, Emergency Stop, powiadomienia).
  - Sekcje PL w Installation, Configuration, Troubleshooting, Supported Devices, Entities & Controls, Hardware Replication.
  - Linki do FAQ w README i Home wiki.
- **No Breaking Changes**: Zmiany wyłącznie w dokumentacji; integracja bez zmian API.

## v4.0.5
- **Fix**: Improved implementation of `OblamatikIoTSerialSensor` to reliably fetch serial number from `/inc/info.txt` or fallback API endpoints.

## 4.0.4
- **Docs**: Added 'Release Date' and 'Pull Requests' badges to README.

## 4.0.3
- **Docs**: Added GitHub stats badges (Stars, Issues, Last Commit) to README.

## 4.0.2
- **Fix**: Reverted `OblamatikIPAddressSensor` to read from API response (reflects true device IP after firmware fix).

## 4.0.1

> **Versioning Change**: Starting from version 4.0.0, the versioning scheme follows `Major.Minor.Patch` where `Patch` cycles from 1 to 9. When `Patch` reaches 9, the next version increments `Minor` by 1 and resets `Patch` to 0 (e.g., `4.0.9` -> `4.1.0`).

- Fix: IoT Serial Number now reads from `/inc/info.txt` if not available in API.
- Fix: IP Address now reflects the configured host instead of potentially incorrect internal IP.
- Remove: Redundant "IoT Firmware Version" entity (use Device Firmware Version instead).
- Change: "Heating" (Climate) entity is now disabled by default (users prefer direct slider/preset control).

## 3.1.17
- **New**: Enabled `sensor.oblamatik_signal_strength` by default for immediate availability after installation.
- **Improvement**: Wi-Fi Signal Strength now provides diagnostics without manual enabling (note: updates may be slower due to device scanning).

## v3.1.16
- **New**: Added "Visit Device" link to Device Info panel (via `configuration_url`) for easy access to device Web UI.
- **Fix**: Resolved `number` entity bug where changing Flow Rate incorrectly triggered Temperature updates.
- **Fix**: Improved Flow and Temperature control logic for better real-time regulation and presetting.
- **Improvement**: Enhanced code compliance (removed unused imports, fixed line lengths).

## v3.1.15
- **New**: Added `sensor.oblamatik_network_mode` to diagnose connection type (`Access Point`, `Client (WiFi)`, `Client (Ethernet)`, `Client (Bridged)`).
- **New**: Added `sensor.oblamatik_ip_address` for better network diagnostics.
- **Improvement**: Enhanced `sensor.oblamatik_mac_address` reliability by ensuring correct update logic.
- **Improvement**: Reflected firmware findings (e.g., `br-lan` handling) in integration logic to improve stability and diagnostics.

## v3.1.14
- **Maintenance**: Repository cleanup for HACS Default compliance (removed outdated `docs/` folder, `.DS_Store`, `RELEASE_TEMPLATE.md`).
- **Fix**: Resolved deprecated ConfigFlow decorator warning (HA 2025.2+).
- **Docs**: Updated README to point to GitHub Wiki for documentation.

## v3.1.13
- **Maintenance**: Code cleanup for HACS compliance (removed deprecated ConfigFlow decorator, cleaned up repository root).

## v3.1.12
- **Change**: Switched license to Apache 2.0.

## v3.1.11
- **Fix**: Ignore 'brands' check in HACS validation (pending HACS Action update for local brands support).

## v3.1.10
- **Maintenance**: Added HACS validation workflow and compliance fixes.

## v3.1.9
- **Change**: Renamed `sensor.oblamatik_bath_button` to `sensor.oblamatik_bath_drain` to better reflect its function (Drain Position).
- **Change**: Updated icon for `sensor.oblamatik_bath_drain` to `mdi:valve`.

## v3.1.8
- **Change**: Renamed "Start Thermal Desinfection" button to "Hygiene Start".
- **Change**: Renamed "Cancel Thermal Desinfection" button to "Hygiene Stop".

## v3.1.7
- **Fix**: Removed "DEVELOPER / TEST VERSION" warning from README (merged into main by mistake).
- **Fix**: Replaced potentially invalid license badge with static MIT badge.

## v3.1.6
- **Fix**: Improved Keep-Alive mechanism with aggressive 1s heartbeat and random query parameter (`?q=...`) to mimic original app behavior and prevent "Hygiene Active" timeouts.

## v3.1.5
- **Fix**: Code formatting compliance (ruff).

## v3.1.4
- **Fix**: Added "Hygiene Active" state recognition (`f`) and implemented Keep-Alive polling (2s interval) for active states (`Running`, `Hygiene Active`) to prevent premature process termination.
- **Fix**: Replaced `mdi:octagon-alert` (too new) with `mdi:alert-octagon` to ensure compatibility with all Home Assistant versions.

## v3.1.3
- **Fix**: Replaced `mdi:octagon-alert` (too new) with `mdi:alert-octagon` to ensure compatibility with all Home Assistant versions.

## v3.1.2
- **Fix**: Emergency Stop button added to stop water flow and cancel hygiene process simultaneously.
- **New**: Added `OblamatikEmergencyStopButton` entity.

## v3.1.1
- **Fix**: Removed `homeassistant` key from `manifest.json` to comply with hassfest (moved to `hacs.json`).
- **Fix**: Updated `hacs.json` to include `homeassistant` version requirement (2025.2.0).
- **Docs**: Updated README.md with detailed installation and configuration instructions.

## v3.1.0
- **Feature**: Added support for Viega Multiplex Trio E.
- **Feature**: Added `OblamatikHygieneStartButton` and `OblamatikHygieneCancelButton`.
- **Feature**: Added `OblamatikOpenDrainButton` and `OblamatikCloseDrainButton` (for bath).
- **Feature**: Added `OblamatikBathFaucetSensor` and `OblamatikBathButtonSensor`.
- **Feature**: Added `OblamatikFlowRateLiterPerHourSensor`.
- **Fix**: Improved device type detection and naming.

## v3.0.0
- **Breaking Change**: Refactored to support multiple device types (Kitchen, Shower, Bath).
- **Feature**: Added `OblamatikWaterSwitch` for water flow control.
- **Feature**: Added `OblamatikWaterFlowSensor` and `OblamatikRequiredFlowSensor`.
- **Feature**: Added `OblamatikCurrentTemperatureSensor` and `OblamatikRequiredTemperatureSensor`.
- **Feature**: Added `OblamatikUptimeSensor`, `OblamatikSerialSensor`, `OblamatikVersionSensor`.
- **Feature**: Added `OblamatikFreeDiskSensor`, `OblamatikFreeMemorySensor`, `OblamatikWifiSsidSensor`, `OblamatikMacAddressSensor`.
- **Fix**: Fixed "Fast Refresh" logic.

## v2.1.7
- **Fix**: Improved `manifest.json` compliance.

## v2.1.6
- **Fix**: Added `hacs.json` for HACS compatibility.

## v2.1.5
- **Initial Release**: Basic support for Oblamatik devices.
