# Oblamatik — Home Assistant Integration

<p align="center">
  <img src="https://raw.githubusercontent.com/bobsilesia/oblamatik/main/assets/readme_logo.jpg" alt="Oblamatik Logo" width="70%" />
</p>

[![Latest release](https://img.shields.io/github/v/release/bobsilesia/oblamatik?sort=semver)](https://github.com/bobsilesia/oblamatik/releases) ![HACS Default](https://img.shields.io/badge/HACS-Default-blue.svg) [![CI](https://github.com/bobsilesia/oblamatik/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bobsilesia/oblamatik/actions/workflows/ci.yml) [![Release](https://github.com/bobsilesia/oblamatik/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/bobsilesia/oblamatik/actions/workflows/release.yml)
[![Stars](https://img.shields.io/github/stars/bobsilesia/oblamatik?style=social)](https://github.com/bobsilesia/oblamatik/stargazers)
![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg) ![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json) ![Mypy](https://img.shields.io/badge/mypy-checked-blue)

[Latest release →](https://github.com/bobsilesia/oblamatik/releases)

> [!WARNING]  
> **DISCLAIMER & SAFETY WARNING**  
> This integration allows control of physical hardware (water flow, temperature, valves) via software. Improper use, bugs, or network issues could potentially lead to **unintended water flow, flooding, or scalding temperatures**.  
>  
> - **Use at your own risk.** The authors are not responsible for any damage to property, hardware, or personal injury caused by the use of this software.  
> - **Not for critical systems.** Do not rely on this integration for safety-critical applications.  
> - **Testing.** Always test your automations and controls with small amounts of water and safe temperatures first.  
> - If you are not comfortable with these risks, **do not use this integration**.

Oblamatik is a Home Assistant integration that allows control and parameter reading of KWC/Viega/Crosswater (TLC) devices.

## Requirements
- Home Assistant Core 2025.2+
- HTTP access to the device (e.g., `http://IP:PORT`)

## Installation (HACS)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bobsilesia&repository=oblamatik&category=integration)

1. Ensure the repository contains the `custom_components/oblamatik` directory.
2. In HACS, search for **Oblamatik** and install it directly (available in HACS Default).
3. Install the integration and restart Home Assistant.

## Installation (Manual)
1. Copy the `custom_components/oblamatik` folder to the `config/custom_components/` directory of your Home Assistant installation.
2. Restart Home Assistant.

## Configuration (Config Flow)

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=oblamatik)

1. Go to: Settings → Devices & Services → Add Integration → Oblamatik.
2. Enter the host (IP) and optionally the port (default `80`).
3. The integration will detect the device type and create the appropriate entities.

## Supported Platforms
- **Sensor**: Temperature, flow, required parameters, device state, auxiliary entities (bath/shower).
- **Switch**: Water flow control, heating switch.
- **Climate**: Heating mode and target temperature.
- **Number**: Precise control of temperature and flow values.
- **Binary Sensor**: Drain position, state monitoring.
- **Button**: Functional tests, hygiene operations, WLAN restart, Water Usage Reset.

## Localization
- Interface texts are located in `strings.json` and `translations/en.json`.

## Project Standards
- Asynchronous programming (async/await).
- Schema validation: `homeassistant.helpers.config_validation`.
- Unified TLC endpoints (`/api/tlc/1/` and `/api/tlc/1/state/`).
- Directory structure: `custom_components/oblamatik/`.

## CI and Publishing
- CI: Ruff (lint/format), Mypy (types), Hassfest (metadata validation).
- Release: tag `vMAJOR.MINOR.PATCH` (e.g., `v4.0.1`). Patch version cycles 1-9. When Patch reaches 9, increment Minor and reset Patch to 0 (e.g., `4.0.9` -> `4.1.0`).
- The version in `manifest.json` must match the version tag.

## Troubleshooting
- Check HA logs (Settings → System → Logs) for integration errors.
- Ensure the device returns valid responses at `http://IP:PORT/api/tlc/1/` and `http://IP:PORT/api/tlc/1/state/`.
- [Detailed Troubleshooting Guide](wiki_content/Troubleshooting.md)
- [Supported Devices & Features](wiki_content/Supported-Devices.md)
- [FAQ](wiki_content/FAQ.md)

## Quick Usage: Water Usage Reset
- Entity: `button.oblamatik_water_usage_reset`
- Effect: Immediately sets flow to 0 and triggers fast sensor refresh (clears “open” flow if stuck).
- Service call example:
  - Domain: `button`
  - Service: `press`
  - Data: `entity_id: button.oblamatik_water_usage_reset`

## Documentation
- [Home](wiki_content/Home.md)
- [Installation](wiki_content/Installation.md)
- [Configuration](wiki_content/Configuration.md)
- [Automations](wiki_content/Automations.md)
- [FAQ](wiki_content/FAQ.md)

## Contributing

Want to help develop the project? Check out our guidelines:
- [Contributing Guidelines (CONTRIBUTING.md)](CONTRIBUTING.md)
- [Code of Conduct (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md)
- [Report a bug or feature request](https://github.com/bobsilesia/oblamatik/issues/new/choose)

## Acknowledgements

Special thanks to the authors of the following repositories, whose work served as a guide for creating this integration:

- [AxelTerizaki/homebridge-trio-e](https://github.com/AxelTerizaki/homebridge-trio-e)
- [roelbroersma/viega_multiplex_trio_e](https://github.com/roelbroersma/viega_multiplex_trio_e)

### Priority references (Viega topics)
- **Viega Multiplex Trio E (API & control logic)** — AxelTerizaki documents endpoints and control sequences used by the official app and Homebridge, useful for understanding device behavior and safe control patterns.  
  Repo: https://github.com/AxelTerizaki/homebridge-trio-e
- **Viega hardware, wiring and serial interface (reverse engineering)** — Roel Broersma’s notes cover module identification, RS232/TTL levels, wiring, and firmware behavior on Carambola.  
  Repo: https://github.com/roelbroersma/viega_multiplex_trio_e

## Related Projects
- Homebridge plugin for Viega Multiplex Trio E (by Axel Terizaki):  
  https://github.com/AxelTerizaki/homebridge-trio-e  
  If you use Apple HomeKit via Homebridge, this plugin exposes Viega devices to HomeKit. Our project targets Home Assistant; the Homebridge plugin is an alternative path for Apple-centric setups.
