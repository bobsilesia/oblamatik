# Automations

Here are some examples of how you can use the Oblamatik integration in your Home Assistant automations.

## Najlepsze praktyki (PL)

- Używaj rozsądnych limitów:
  - Fill Amount: 10–300 L (zalecane limity guard w automatyce, np. < 200 L).
  - Fill Temperature: 20–50°C (bezpieczny komfort).
- Nie uruchamiaj „Start Fill” bezpośrednio z triggera czasowego – dodaj warunki (presence, drain closed, max amount).
- Dodaj powiadomienia po zakończeniu lub błędzie (czujnik „Water Fill State”).
- Zawsze miej „Emergency Stop” pod ręką (przycisk integracji).
- Higiena: modyfikuj interwał/duration razem z przeglądem instalacji (np. po serwisie), nie ustawiaj bardzo krótkich interwałów w ruchu ciągłym.

### Guard dla objętości (PL)

```yaml
alias: "Start Fill (z limitem)"
description: "Uruchom napełnianie tylko gdy ilość <= 200 L"
trigger:
  - platform: state
    entity_id: button.oblamatik_start_fill
    to: "pressed"
condition:
  - condition: numeric_state
    entity_id: number.oblamatik_fill_amount
    below: 200
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_start_fill
```

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

## 6. Universal Water Fill (Faucet/Shower/Bath)

Use the new universal entities to start a controlled fill with defined amount and temperature.

### Manual Start from Dashboard
- Set `number.oblamatik_*_fill_amount` (liters)
- Set `number.oblamatik_*_fill_temperature` (°C)
- Press `button.oblamatik_*_start_fill`

### Safe Start with Amount Guard

```yaml
alias: "Start Fill (Guarded)"
description: "Start fill only if amount <= 200 L"
trigger:
  - platform: state
    entity_id: button.oblamatik_start_fill
    to: "pressed"
condition:
  - condition: numeric_state
    entity_id: number.oblamatik_fill_amount
    below: 200
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_start_fill
```

### Start Fill via Scene

```yaml
alias: "Evening Bath Scene"
sequence:
  - service: number.set_value
    data:
      value: 120
    target:
      entity_id: number.oblamatik_fill_amount
  - service: number.set_value
    data:
      value: 39
    target:
      entity_id: number.oblamatik_fill_temperature
  - service: button.press
    target:
      entity_id: button.oblamatik_start_fill
mode: single
```

## 7. Measuring Cup Dispense

Dispense a precise amount using the measuring cup.

```yaml
alias: "Dispense Measuring Cup"
sequence:
  - service: number.set_value
    data:
      value: 0.5
    target:
      entity_id: number.oblamatik_measuring_cup_amount
  - service: button.press
    target:
      entity_id: button.oblamatik_measuring_cup_start
mode: single
```
