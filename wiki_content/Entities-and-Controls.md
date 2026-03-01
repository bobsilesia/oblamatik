# Entities and Controls

The Oblamatik integration exposes various entities to Home Assistant, allowing you to monitor and control your device comprehensively.

---

## Wersja PL (skrót)

Integracja udostępnia encje pozwalające na:
- odczyt temperatury, przepływu, stanu i parametrów sieciowych,
- sterowanie odpływem (popup), trybem higieny, szybkim testem,
- precyzyjne ustawianie temperatury/przepływu oraz nowych funkcji „Fill” i „Measuring Cup”.

### Nowe uniwersalne encje (Faucet/Shower/Bath)
- `number.oblamatik_*_fill_amount` – docelowa objętość (L), lokalna wartość w HA.
- `number.oblamatik_*_fill_temperature` – docelowa temperatura (°C), lokalna wartość w HA.
- `button.oblamatik_*_start_fill` – wysyła `amount` + `temperature` do `/api/index.php?url=tlc-bathtub-fill/1/`.
- `sensor.oblamatik_*_fill_state` – stan operacji `ready|running|idle|unknown`.

### Miarka (Measuring Cup)
- `number.oblamatik_*_measuring_cup_amount` – odczyt/zapis domyślnej ilości (`GET/POST` `tlc-measuring-cup/1/get|save`).
- `button.oblamatik_*_measuring_cup_start` – dozowanie (`POST tlc-measuring-cup/1/` z `quantity`).

### Higiena
- `number.oblamatik_*_hygiene_interval` – `repetition_period` (dni).
- `number.oblamatik_*_hygiene_flush_duration` – `flush_duration` (sekundy).
- `switch.oblamatik_*_hygiene_active` – harmonogram aktywny/nieaktywny.
- `button.oblamatik_*_hygiene_start` / `_cancel` – natychmiastowe rozpoczęcie/zatrzymanie.

---
## Sensors

These entities provide real-time information about the device's state.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Current Temperature** | `sensor.oblamatik_current_temperature` | The actual water temperature (°C). |
| **Flow Rate** | `sensor.oblamatik_flow_rate` | Current water flow rate (L/min). |
| **Total Consumption** | `sensor.oblamatik_water_flow` | Total water used since power on (L). |
| **Status** | `sensor.oblamatik_status` | Device status (e.g., "OK", "Running", "Error"). |
| **Uptime** | `sensor.oblamatik_uptime` | Time since last restart (HH:MM:SS). |
| **Serial Number** | `sensor.oblamatik_serial_number` | Device serial number. |
| **Version** | `sensor.oblamatik_version` | Firmware version. |
| **Free Disk/Memory** | `sensor.oblamatik_free_disk` / `_memory` | System resources. |

## Binary Sensors

These entities show the on/off state of specific features.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Drain Position** | `binary_sensor.oblamatik_drain_position` | Indicates if the drain (popup) is OPEN (On) or CLOSED (Off). |

## Switches

These allow simple on/off control.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Water Flow** | `switch.oblamatik_water_switch` | Turn water flow ON/OFF. |
| **Heating** | `switch.oblamatik_heating_switch` | Turn heating mode ON/OFF. |

## Climate

This entity provides a thermostat-like interface for controlling water temperature.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Temp Control** | `climate.oblamatik_temp_control` | Set target temperature (°C), turn heating on/off. |

## Numbers

These entities allow precise control of values.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Temperature** | `number.oblamatik_temperature` | Set precise target temperature (4.0°C - 80.0°C). |
| **Flow** | `number.oblamatik_flow` | Set precise flow rate. |
| **Fill Amount** | `number.oblamatik_fill_amount` | Target fill volume (L). |
| **Fill Temperature** | `number.oblamatik_fill_temperature` | Target fill temperature (°C). |
| **Measuring Cup Amount** | `number.oblamatik_measuring_cup_amount` | Default measuring amount (L). |

## Buttons

These trigger specific actions on the device.

| Entity | ID | Description |
| :--- | :--- | :--- |
| **Stop** | `button.oblamatik_stop` | Immediately stops water flow and heating. |
| **Open Drain** | `button.oblamatik_open_drain` | Opens the bathtub drain. |
| **Close Drain** | `button.oblamatik_close_drain` | Closes the bathtub drain. |
| **Quick Action 1** | `button.oblamatik_quick_action_1` | Executes predefined Quick Action 1. |
| **WLAN Restart** | `button.oblamatik_wlan_restart` | Restarts the device's WLAN module (use with caution). |
| **Function Test Step 1-3** | `button.oblamatik_function_test_step_1`... | Runs diagnostic tests. |
| **Hygiene Start/Cancel** | `button.oblamatik_hygiene_start` / `_cancel` | Controls thermal disinfection cycle. |
| **Measuring Cup Start** | `button.oblamatik_measuring_cup_start` | Dispenses measuring cup amount. |
| **Start Fill** | `button.oblamatik_start_fill` | Starts universal fill with set amount and temperature. |
