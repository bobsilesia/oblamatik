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
