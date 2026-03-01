## 4.0.5
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
