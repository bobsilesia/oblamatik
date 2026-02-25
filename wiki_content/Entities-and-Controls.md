# Entities and Controls

The Oblamatik integration exposes various entities to Home Assistant, allowing you to monitor and control your device comprehensively.

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
