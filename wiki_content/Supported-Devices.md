# Supported Devices

The Oblamatik integration supports various devices based on the **TLC (Touch Logic Control)** system. These devices are typically used for smart water control in bathrooms and kitchens.

## Verified Models

| Manufacturer | Model | Module Type | Notes |
| :--- | :--- | :--- | :--- |
| **Viega** | **Multiplex Trio E** | **Viega WLAN module 708870** | Fully supported. Identical hardware to Crosswater DGXWLAN-E. Standard API `/api/tlc/1/` works. |
| **Crosswater** | **Digital Shower (Duo/Elite)** | **DGXWLAN-E** | Fully supported. Identical hardware to Viega 708870. Uses standard TLC protocol. |
| **KWC** | **Kitchen Faucet (Various)** | **C-module** (and others) | **Experimental**. Some C-modules may restrict local API access or require specific pairing. Functionality might be limited compared to Viega/Crosswater modules. |

> **Note:** The **Viega WLAN module 708870** and **Crosswater DGXWLAN-E** are manufactured by Oblamatik and are hardware-identical. They offer the most complete feature set and stability with this integration.

## Feature Support Matrix

| Feature | Viega (708870) / Crosswater (DGXWLAN-E) | KWC Faucets (C-module) |
| :--- | :---: | :---: |
| **Temperature Control** | :white_check_mark: | :white_check_mark: |
| **Flow Rate Control** | :white_check_mark: | :white_check_mark: |
| **Drain Position (Popup)** | :white_check_mark: | :question: (Model dependent) |
| **Functional Tests** | :white_check_mark: | :white_check_mark: |
| **Hygiene Mode** | :white_check_mark: | :warning: (Keep-Alive required) |
| **WLAN Restart** | :white_check_mark: | :white_check_mark: |
| **Quick Actions** | :white_check_mark: | :white_check_mark: |

## Connection Requirements

-   **Network**: The device must be connected to the same local network (WLAN) as Home Assistant.
-   **Static IP**: Highly recommended to prevent the IP from changing.
-   **Port 80**: Default HTTP port used for communication.
-   **API Access**: The device must expose the `/api/` endpoints. Most modern TLC devices have this enabled by default.

If you have a device that is not listed but works with this integration, please open a [Feature Request](https://github.com/bobsilesia/oblamatik/issues) to add it to the list!
