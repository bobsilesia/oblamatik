# Supported Devices

This integration supports devices manufactured by **Oblamatik AG**, which are often sold under different brand names depending on the region.

Language: [PL](#pl) | [EN](#en)

<a id="en"></a>

---

## Wersja PL (skrót)

<a id="pl"></a>

Integracja wspiera urządzenia **Oblamatik** sprzedawane także jako **Viega**, **Crosswater**, **Deca**, **Sigma**:
- Multiplex Trio E (Viega), Digital Duo/Elite (Crosswater), Touch Digital (Deca), Sigma Touch (USA, TLC30).
- Moduły WLAN: **708870** (Viega) / **DGXWLAN-E** (Crosswater) – sprzętowo identyczne.
- Identyfikacja: obudowa Carambola (OpenWrt), etykiety z Oblamatik/Viega lub odpowiednim FCC/CE.

Jeżeli urządzenie odpowiada na `http://IP/api/tlc/1/` lub `http://IP/api/`, jest wysokie prawdopodobieństwo zgodności.

---

## Confirmed Supported Models

The following devices share the same underlying hardware and API, making them fully compatible with this integration:

| Brand | Model Name | Region | Notes |
| :--- | :--- | :--- | :--- |
| **Viega** | Multiplex Trio E / E2 / E3 | Europe / USA | The most common version. WLAN module usually 708870. |
| **Oblamatik** | Prime / Gentle | Global (OEM) | The original manufacturer's branding. |
| **Crosswater** | Digital Duo / Elite | UK / USA | Uses **DGXWLAN-E** module (hardware-identical to Viega 708870). |
| **Deca** | Touch Digital / Digital Banho | Brazil | E.g. **2875.C.TCH.DIG** (Monocomando). Uses the same control logic. |
| **Sigma** | Sigma Touch (Discontinued) | USA | Sold by **American Faucet & Coatings Corp**. SKU **1.0000710.xx**. Internal model **TLC30**. |

> **Note:** The **Viega WLAN module 708870** and **Crosswater DGXWLAN-E** are manufactured by Oblamatik and are hardware-identical.

## Experimental / Likely Compatible

| Brand | Model Name | Region | Notes |
| :--- | :--- | :--- | :--- |
| **KWC** | ONO touch light PRO | Global | Based on Oblamatik technology ("TLC" = Touch Light Control). |
| **Laufen / Arwa** | arwa-twinprime tronic | Switzerland / EU | "Tronic" series (electronic mixers) share features like bath fill/presets. |
| **Similor Kugler** | Electronic Mixers | Switzerland | Part of Laufen group; high probability of shared Oblamatik OEM platform. |
| **Hansa** | Electra | Europe | Some high-end digital models may share this platform. |

## Hardware Identification

If your device has a WLAN module that looks like a small white or grey box with a label mentioning **Oblamatik**, **Viega**, or FCC ID starting with **2AC...** (or similar Swiss/German codes), it is likely supported.

The firmware typically runs on an **8devices Carambola** (OpenWrt-based) module.

### Model Codes
You might find these codes on the controller unit (black box):
- **TLC30...** (e.g., `TLC30FTD`) - Likely stands for "**T**ouch **L**ight **C**ontrol".
- **1.0000710.xx** - Sigma Touch commercial SKU (e.g., 1.0000710.26 for Chrome).
- **Vision Bad** - Internal project name seen on some units.

## Feature Support by Device

| Feature | Viega / Oblamatik | Crosswater | Deca Touch | Sigma Touch |
| :--- | :--- | :--- | :--- | :--- |
| **On/Off Control** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Temperature Set** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Flow Rate Set** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Presets (Quick)** | ✅ Yes (3 slots) | ✅ Yes | ✅ Yes | ✅ Yes |
| **Bath Fill Mode** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

## Troubleshooting

If your device is not discovered automatically:
1. Ensure it is connected to the same Wi-Fi network as Home Assistant.
2. Check if you can access `http://<device_ip>/api/` in your browser.
3. Try adding it manually using the IP address in the integration configuration.

## Further Reading (Viega topics)
- AxelTerizaki — Homebridge for Viega Multiplex Trio E (API endpoints, control logic):  
  https://github.com/AxelTerizaki/homebridge-trio-e
- Roel Broersma — Reverse engineering, wiring, module details for Viega/Oblamatik:  
  https://github.com/roelbroersma/viega_multiplex_trio_e
