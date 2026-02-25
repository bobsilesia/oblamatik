# Supported Devices

The Oblamatik integration supports devices based on the TLC (Touch Logic Control) system, used by various manufacturers.

## Validated Models

| Manufacturer | Model | Connection | Notes |
|---|---|---|---|
| **Viega** | Multiplex Trio E | WLAN | Fully supported. Standard API endpoints `/api/tlc/1/` work correctly. |
| **KWC** | (Various Kitchen/Bath models) | WLAN | Supported. Some older firmware versions may report `uptime: 0` (handled by integration fallback). |
| **Crosswater** | Digital Showers | WLAN | Supported. Uses same TLC protocol. |

## Feature Matrix

| Feature | Viega | KWC | Crosswater |
|---|---|---|---|
| Water Flow Control | ✅ | ✅ | ✅ |
| Temperature Control | ✅ | ✅ | ✅ |
| Drain Position | ✅ | ❓ | ❓ |
| Functional Tests | ✅ | ✅ | ✅ |
| Hygiene Mode | ✅ | ✅ | ✅ |
| WLAN Restart | ✅ | ✅ | ✅ |

## Device Detection

The integration automatically attempts to identify the device type during configuration (Config Flow).
It checks:
1. Primary endpoint: `http://IP/api/tlc/1/`
2. Fallback endpoint: `http://IP/api/tlc/1/state/` (used by some KWC models with restrictive APIs)

If your device is not detected correctly or shows as "Unknown", please open an [Issue](https://github.com/bobsilesia/oblamatik/issues) and provide the JSON output from `http://DEVICE_IP/api/`.
