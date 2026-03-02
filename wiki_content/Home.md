# Welcome to the Oblamatik Integration Wiki

**oblamatik** is a custom integration for Home Assistant that provides full control over **Oblamatik** based systems, including **Viega Multiplex Trio E**, **KWC** electronic faucets, and **Crosswater** digital showers.

This integration allows you to monitor and control water temperature, flow rate, drain position, and perform maintenance tasks directly from your smart home dashboard.

 

## Key Features

- **Precise Control**: Set exact water temperature and flow rate.
- **Monitoring**: Real-time sensors for current temperature, flow, and total water consumption.
- **Smart Features**: 
  - Control the bathtub drain (Popup/Drain Position).
  - Run hygiene/thermal disinfection cycles.
  - Execute functional tests.
- **Device Support**: Works with various manufacturers using the TLC (Touch Logic Control) system.
- **Easy Setup**: Automatic device detection via Home Assistant Config Flow.

## Quick Start

1. **[Installation](Installation)**: How to install via HACS or manually.
2. **[Configuration](Configuration)**: Setting up the integration with your device.
3. **[Supported Devices](Supported-Devices)**: Check if your device is compatible.

## Getting Started

## Related (Homebridge)
- Homebridge plugin for Viega Multiplex Trio E (Axel Terizaki): https://github.com/AxelTerizaki/homebridge-trio-e
  - For Apple HomeKit users — alternative to expose Viega devices in HomeKit via Homebridge.

## Further Reading (Hardware / Carambola)
- Reverse engineering 8devices Carambola 2 (Roel Broersma): https://github.com/roelbroersma/viega_multiplex_trio_e
  - Details about pinout, RS232 vs TTL, MAX3232 and firmware dumps (MTD/U‑Boot).

## Support

If you encounter any issues, please check the **[Troubleshooting](Troubleshooting)** section first. 
You may also find answers in the **[FAQ](FAQ)**.
For bugs and feature requests, open an issue on [GitHub](https://github.com/bobsilesia/oblamatik/issues).

---
*This integration is an open-source project and is not affiliated with Oblamatik, Viega, KWC, or Crosswater.*
