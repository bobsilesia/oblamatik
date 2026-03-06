# Oblamatik

> [!WARNING]  
> **DISCLAIMER & SAFETY WARNING**  
> This integration allows control of physical hardware (water flow, temperature, valves) via software. Improper use, bugs, or network issues could potentially lead to **unintended water flow, flooding, or scalding temperatures**.  
>  
> - **Use at your own risk.** The authors are not responsible for any damage to property, hardware, or personal injury caused by the use of this software.  
> - **Not for critical systems.** Do not rely on this integration for safety-critical applications.  
> - If you are not comfortable with these risks, **do not use this integration**.

This integration allows you to control KWC, Viega, and Crosswater (TLC) smart water controllers in Home Assistant.

## Features

- **Control**: Start/stop water flow, set temperature, set amount.
- **Sensors**: Current flow, temperature, total water usage, device state.
- **Configuration**: Auto-discovery of device type (Viega/KWC/Crosswater).
- **Localization**: Supports English, German, Polish, and more.

## Supported Devices

- KWC ZOE touch light PRO
- Viega Multiplex Trio E
- Crosswater Digital
- Oblamatik Twinlevel
- And other devices based on the Oblamatik TLC controller.

## Installation

1. Click "Download" in HACS.
2. Restart Home Assistant.
3. Add the integration via **Settings** -> **Devices & Services** -> **Add Integration** -> **Oblamatik**.
