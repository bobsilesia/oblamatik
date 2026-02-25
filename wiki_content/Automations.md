# Automations

Here are some examples of how you can use the Oblamatik integration in your Home Assistant automations.

## 1. Notification when Bath is Ready

Send a notification to your phone when the bath reaches the desired temperature.

```yaml
alias: "Bath Ready Notification"
description: "Notify when bath reaches target temperature"
trigger:
  - platform: numeric_state
    entity_id: sensor.oblamatik_current_temperature
    above: 38.0
condition:
  - condition: state
    entity_id: switch.oblamatik_water_flow
    state: "on"
action:
  - service: notify.mobile_app_my_phone
    data:
      message: "Bath is ready! Temperature reached 38°C."
      title: "Bath Ready"
```

## 2. Auto-Stop after 15 Minutes

Prevent overflowing or wasting water by automatically stopping the flow after a set time.

```yaml
alias: "Auto-Stop Bath Flow"
description: "Turn off water flow after 15 minutes"
trigger:
  - platform: state
    entity_id: switch.oblamatik_water_flow
    to: "on"
    for:
      minutes: 15
action:
  - service: switch.turn_off
    target:
      entity_id: switch.oblamatik_water_flow
  - service: notify.mobile_app_my_phone
    data:
      message: "Bath water flow stopped automatically after 15 minutes."
```

## 3. Voice Control via Assist/Alexa/Google

You can expose the `climate.oblamatik_temp_control` entity to your voice assistant to control the bath temperature.

-   **"Hey Google, set the bath temperature to 40 degrees."**
-   **"Alexa, turn on the bath."**

Ensure you have configured the Home Assistant Cloud or manual integration for your voice assistant.

## 4. Hygiene Schedule

Run a thermal disinfection cycle every week at a specific time.

```yaml
alias: "Weekly Hygiene Cycle"
description: "Run thermal disinfection every Sunday at 3 AM"
trigger:
  - platform: time
    at: "03:00:00"
    days:
      - sun
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_hygiene_start
```

## 5. Smart Drain Control

Close the drain automatically when water flow starts.

```yaml
alias: "Auto-Close Drain on Flow"
description: "Close the drain when water starts flowing"
trigger:
  - platform: state
    entity_id: switch.oblamatik_water_flow
    to: "on"
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_close_drain
```
