# Changelog

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
