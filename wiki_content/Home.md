# Oblamatik Home Assistant Integration

> [!WARNING]  
> **DISCLAIMER & SAFETY WARNING**  
> This integration allows control of physical hardware (water flow, temperature, valves) via software. Improper use, bugs, or network issues could potentially lead to **unintended water flow, flooding, or scalding temperatures**.  
>  
> - **Use at your own risk.** The authors are not responsible for any damage to property, hardware, or personal injury caused by the use of this software.  
> - **Not for critical systems.** Do not rely on this integration for safety-critical applications.  
> - If you are not comfortable with these risks, **do not use this integration**.

This integration brings KWC, Viega, Crosswater, and other Oblamatik TLC-based water controllers into Home Assistant.

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

- [Automations](Automations.md)
- [Diagnostics](Diagnostics.md)
- [FAQ](FAQ.md)
- [UiMatic (Lovelace Card)](UiMatic.md)

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
