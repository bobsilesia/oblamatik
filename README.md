# Oblamatik — Home Assistant Integration

![Latest release](https://img.shields.io/github/v/release/bobsilesia/oblamatik?sort=semver) ![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg) ![CI](https://github.com/bobsilesia/oblamatik/actions/workflows/ci.yml/badge.svg?branch=main) ![Release](https://github.com/bobsilesia/oblamatik/actions/workflows/release.yml/badge.svg?branch=main)
![License](https://img.shields.io/github/license/bobsilesia/oblamatik) ![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json) ![Mypy](https://img.shields.io/badge/mypy-checked-blue)

[Latest release →](https://github.com/bobsilesia/oblamatik/releases)

Oblamatik is a Home Assistant integration that allows control and parameter reading of KWC/Viega/Crosswater (TLC) devices.

## Requirements
- Home Assistant Core 2025.2+
- HTTP access to the device (e.g., `http://IP:PORT`)

## Installation (HACS)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bobsilesia&repository=oblamatik&category=integration)

1. Ensure the repository contains the `custom_components/oblamatik` directory.
2. In HACS, add the repository as a Custom Repository or use the available source if the repo is publicly supported by HACS.
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
- **Button**: Functional tests, hygiene operations, WLAN restart.

## Localization
- Interface texts are located in `strings.json` and `translations/en.json`.

## Project Standards
- Asynchronous programming (async/await).
- Schema validation: `homeassistant.helpers.config_validation`.
- Unified TLC endpoints (`/api/tlc/1/` and `/api/tlc/1/state/`).
- Directory structure: `custom_components/oblamatik/`.

## CI and Publishing
- CI: Ruff (lint/format), Mypy (types), Hassfest (metadata validation).
- Release: tag `vMAJOR.MINOR.PATCH` (e.g., `v2.0.10`) — workflow publishes `oblamatik.zip`.
- The version in `manifest.json` must match the version tag.

## Troubleshooting
- Check HA logs (Settings → System → Logs) for integration errors.
- Ensure the device returns valid responses at `http://IP:PORT/api/tlc/1/` and `http://IP:PORT/api/tlc/1/state/`.
- [Detailed Troubleshooting Guide](docs/Troubleshooting.md)
- [Supported Devices & Features](docs/Supported_Devices.md)

## Contributing

Want to help develop the project? Check out our guidelines:
- [Contributing Guidelines (CONTRIBUTING.md)](CONTRIBUTING.md)
- [Code of Conduct (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md)
- [Report a bug or feature request](https://github.com/bobsilesia/oblamatik/issues/new/choose)
