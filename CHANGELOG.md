# Changelog

## v3.0.3
- **Fix**: Corrected `Flow Rate` slider to use target temperature (`required_temp`) instead of actual temperature, preventing temperature drops during adjustment.
- **Fix**: Corrected `Stop` button to preserve the current target temperature instead of resetting it to 10°C.
- **Fix**: Corrected `Temperature` slider to use target flow (`required_flow`) instead of actual flow.

## v3.0.2
- **Enhancement**: Renamed "Restart WLAN (Reset to AP)" button to "WLAN (AP mode)" for clarity.
- **New Feature**: Added a diagnostic sensor displaying the current Wi-Fi SSID.
- **Documentation**: Added acknowledgements to the authors of `homebridge-trio-e` and `viega_multiplex_trio_e` for their pioneering work.

## v3.0.1
- **Documentation**: Added professional "Open in Home Assistant" badges for easy installation (HACS) and configuration (Config Flow) in `README.md`.
- **Version**: Bumped version to 3.0.1 to reflect major documentation and usability improvements.

## v2.1.39
- **Change**: Disabled `Free Disk Space`, `Free Memory`, and `Uptime` sensors by default (can be enabled manually).

## v2.1.38
- **Fix**: Removed temperature sensors for devices reporting invalid temperatures (>99°C), which indicates a missing thermistor (e.g., KWC models).

## v2.1.37
- **New Feature**: Added buttons for `Quick Action 2` and `Quick Action 3` (based on user request and Multiplex Trio E capabilities).

## v2.1.36
- **Fix**: Added missing `async_press` implementation for `Quick Action 1` button.

## v2.1.35
- **Icons**: Changed icon for `Flow Rate L/h` sensor to `mdi:gauge-low` (requested by user).

## v2.1.34
- **Icons**: Fixed invalid icon for `Flow Rate L/h` sensor (changed to `mdi:hydro-power`).

## v2.1.33
- **Branding**: Verified and confirmed local brand structure for Home Assistant 2026.3.0+.
- **Cleanup**: Removed legacy brand submission folder.

## v2.1.32
- **Branding**: Added local brand icons (logo and icon) to support Home Assistant 2026.3.0+ features.

## v2.1.31
- **Fixes**: Corrected `manifest.json` key sorting to pass Hassfest validation.

## v2.1.30
- **Naming**: Removed IP address from `Water Flow` switch name (e.g., "Water Flow" instead of "Water Flow (IP)").
- **Fixes**: Cleaned up `manifest.json` structure.

## v2.1.29
- **Icons**: Changed "Flow Rate" icon to `mdi:hydro-power`.
- **Icons**: Changed "Cancel Thermal Desinfection" icon to `mdi:stop-circle-outline`.

## v2.1.28
- **Discovery**: Added automatic device discovery via DHCP (MAC OUI: 8devices) and Zeroconf (mDNS).
- **Config Flow**: Introduced "Automatic vs Manual" configuration mode selection.
- **Config Flow**: Removed default IP address to prevent accidental configuration of incorrect devices.

## v2.1.27
- **Naming**: Improved device naming to use device type (e.g., "Oblamatik Kitchen") instead of IP address. This results in cleaner entity IDs for new installations (e.g., `switch.oblamatik_kitchen_water_flow` instead of `switch.water_flow_192_168_1_36`).
- **Fixes**: Corrected automatic device info updates for existing devices with ugly names.

## v2.1.26
- **Documentation**: Added comprehensive Wiki (Home, Installation, Configuration, Devices, Entities, Automations, Troubleshooting).
- **Security**: Added `SECURITY.md` with vulnerability reporting policy.
- **Community**: Added `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and Issue Templates.
- **License**: Added MIT License.
- **Localization**: Translated all documentation and changelogs to English.

## v2.1.25 (2026-02-25)

- Fix button visibility in newer HA versions: used `EntityCategory.CONFIG/DIAGNOSTIC`
- Added MIT License

## v2.1.24 (2026-02-25)

- Binary Sensor: Renamed to "Drain Position", icon `mdi:valve`
- Climate: Renamed to "Temp Control", fixed `unique_id`
- Sensor: Pump icon for "Flow Rate", removed IP from "Water Flow" name
- Uptime: Fallback for KWC devices returning 0
- CI: Full `ruff` and `mypy` verification

## v2.1.23 (2026-02-25)

- Enforced CI pre-checks in project rules
- `ruff` formatting fixes

## v2.1.22 (2026-02-25)

- Uptime formatting: hh:mm
- Status: mapping "a" -> "ok"
- Fix: TLC15F Kitchen info/uptime fallback

## v2.1.21 (2026-02-25)

- Added fallback endpoint `/api/tlc/1/` for TLC15F devices

## v2.1.20 (2026-02-25)

- Added `binary_sensor` platform (Popup/Drain)
- Added buttons: Restart WLAN, Functional Tests, Hygiene

## v2.1.7 (2026-02-24)

- ConfigFlow registration compatible with HA (`class ConfigFlow(..., domain=DOMAIN)`), eliminates “Invalid handler specified”
- mypy: disabled `call-arg` error for config_flow
- Manifest: bumped version to `2.1.7`

## v2.1.6 (2026-02-24)

- Automatic releases: GitHub workflow creates Release and attaches `oblamatik.zip` asset on `v*` tags
- Manifest: bumped version to `2.1.6`
- Enforced HACS requirements: asset contains integration files directly in root ZIP

## v2.1.5 (2026-02-24)

- Config flow fix: `ConfigFlow` class registration and elimination of `FlowResult` dependency
- HTTP connection stabilization: using HA session `aiohttp_client.async_get_clientsession(hass)`
- Consistent timeouts: `aiohttp.ClientTimeout(total=5)` in all HTTP calls
- Lint/format fixes: `ruff` organized imports, `mypy` without errors
- Manifest: bumped version to `2.1.5`
- ZIP for HACS: no nesting, integration files in root ZIP

## v2.1.3 (2026-02-23)

- Integration migration to `custom_components/oblamatik` according to project rules
- Correct platform unloading: `async_unload_platforms` in `__init__.py`
- Type annotations and full async (HA 2025.2+ compatibility)
- Config Flow: added `OptionsFlow`, device type detection, error handling
- WebSocket: using `async_get_clientsession(hass)`, `WSMsgType` handling, type annotations
- Unified TLC endpoints in sensors/number/switch (`/api/tlc/1/state/`)
- Localization: `strings.json` and `translations/en.json`
- CI: `ruff`, `mypy`, `hassfest` workflow on `push`/`pull_request`
- Release: workflow building ZIP for HACS on `v*` tag
- HACS: added `hacs.json` (`zip_release`, minimalna wersja HA)
