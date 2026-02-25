# Supported Devices

The Oblamatik integration supports various devices based on the **TLC (Touch Logic Control)** system. These devices are typically used for smart water control in bathrooms and kitchens.

## Verified Models

| Manufacturer | Model | Connection | Features | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Viega** | **Multiplex Trio E** | WLAN | Temp, Flow, Drain, Hygiene | Fully supported. Standard API `/api/tlc/1/` works. |
| **KWC** | **Kitchen Faucet (Various)** | WLAN | Temp, Flow, Info | Supported. Some older firmware versions may report `uptime: 0` (handled by fallback). |
| **Crosswater** | **Digital Shower** | WLAN | Temp, Flow, Hygiene | Supported. Uses same TLC protocol. |

## Feature Support Matrix

| Feature | Viega Multiplex Trio E | KWC Faucets | Crosswater Shower |
| :--- | :---: | :---: | :---: |
| **Temperature Control** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Flow Rate Control** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Drain Position (Popup)** | :white_check_mark: | :question: (Model dependent) | :question: (Model dependent) |
| **Functional Tests** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Hygiene Mode** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **WLAN Restart** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Quick Actions** | :white_check_mark: | :white_check_mark: | :white_check_mark: |

## Connection Requirements

-   **Network**: The device must be connected to the same local network (WLAN) as Home Assistant.
-   **Static IP**: Highly recommended to prevent the IP from changing.
-   **Port 80**: Default HTTP port used for communication.
-   **API Access**: The device must expose the `/api/` endpoints. Most modern TLC devices have this enabled by default.

If you have a device that is not listed but works with this integration, please open a [Feature Request](https://github.com/bobsilesia/oblamatik/issues) to add it to the list!
