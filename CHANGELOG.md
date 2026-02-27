# Changelog

## v3.1.3
- **Fix**: Replaced `mdi:octagon-alert` (too new) with `mdi:alert-octagon` to ensure compatibility with all Home Assistant versions.

## v3.1.2
- **Change**: Renamed "Stop" button to "Emergency Stop" and updated icon to `mdi:octagon-alert`.
- **Enhancement**: "Emergency Stop" now sends both `flow=0` (stop water) and `hygiene/cancel` commands to ensure all active water functions are terminated immediately.

## v3.1.1
- **Fix**: Corrected logic for retrieving status sensor `entity_id` in fast refresh mechanism (replaced incorrect `er.async_get_entity_id` with `registry.async_get_entity_id`).

## v3.1.0
- Enhancement: Fast post-command refresh — after any successful command, the integration forces the Status sensor to update every ~1s for ~10s, so state changes (e.g., Idle/Running) appear quickly in HA.
- Internal: Applied across Buttons, Switches, Climate, and Number platforms without changing user-facing configuration.

## v3.0.9
- **Change**: Mapped device `state` values to friendly names in `Status` sensor (`a`→`Idle`, `b`→`Running`).

## v3.0.8
- **Fix**: Fixed `MAC Address` sensor to read from `mac_address` in `/api/tlc/1/` response.

## v3.0.7
- **Fix**: Corrected `Wi-Fi SSID` sensor to read from nested `wlan.name` field in API response.
- **New Feature**: Added `MAC Address` diagnostic sensor.

## v3.0.6
- **Fix**: Changed `Wi-Fi SSID` sensor to read from `/api/tlc/1/` instead of `/api/` (as requested by user).

## v3.0.5
- **Fix**: Aligned "Reboot Device" request payload with device UI (`Content-Type: application/x-www-form-urlencoded`, body `0=1`).

## v3.0.4
- **New Feature**: Added "Reboot Device" button (replaces "Function Test Stop") based on user request and code analysis.
- **Enhancement**: Renamed "Function Test Stop" to "Reboot Device" as they use the same API endpoint (`/api/tlc/1/functional-test/step/0/`).

## v3.0.3
- **Fix**: Corrected `Flow Rate` slider to use target temperature (`required_temp`) instead of actual temperature, preventing temperature drops during adjustment.
- **Fix**: Corrected `Stop` button to preserve the current target temperature instead of resetting it to 10°C.
- **Fix**: Corrected `Temperature` slider to use target flow (`required_flow`) instead of actual flow.

## v3.0.2
- **Enhancement**: Renamed "Restart WLAN (Reset to AP)" button to "WLAN (AP mode)" for clarity.
- **New Feature**: Added a diagnostic sensor displaying the current Wi-Fi SSID.
- **Documentation**: Added acknowledgements to the authors of `homebridge-trio-e` and `viega_multiplex_trio_e` for their pioneering work.

## v3.0.1
