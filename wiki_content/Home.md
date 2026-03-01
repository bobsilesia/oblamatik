# Welcome to the Oblamatik Integration Wiki

**oblamatik** is a custom integration for Home Assistant that provides full control over **Oblamatik** based systems, including **Viega Multiplex Trio E**, **KWC** electronic faucets, and **Crosswater** digital showers.

This integration allows you to monitor and control water temperature, flow rate, drain position, and perform maintenance tasks directly from your smart home dashboard.

---

## Wersja PL (skrót)

Integracja **Oblamatik** dla Home Assistant umożliwia:
- sterowanie temperaturą i przepływem,
- odczyt stanu urządzenia (np. „Water Fill State”),
- sterowanie odpływem (popup),
- uruchamianie cykli higieny (thermal desinfection),
- testy funkcjonalne.

Nowe „uniwersalne” encje:
- `number.oblamatik_*_fill_amount` – objętość (L),
- `number.oblamatik_*_fill_temperature` – temperatura (°C),
- `button.oblamatik_*_start_fill` – start napełniania,
- `sensor.oblamatik_*_fill_state` – stan operacji.

Sprawdź przykłady w: **[Automations](Automations)** (sekcja „Najlepsze praktyki (PL)”).

---

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

## FAQ Highlights
- Higiena i „keep-alive”: dlaczego intensywne odpytywanie co 1s — zobacz **[FAQ](FAQ)**.
- Bezpieczne limity dla Fill i zalecany „guard” w automatyzacji — zobacz **[FAQ](FAQ)**.
- Szybkie zatrzymanie (Emergency Stop) i dobre praktyki dashboardu — zobacz **[FAQ](FAQ)**.
- Uniwersalność Fill dla faucet/shower/bath oraz różnice `quantity` vs `amount` — zobacz **[FAQ](FAQ)**.

### Skrócone przykłady (PL)

```yaml
alias: "Guarded Water Fill"
trigger:
  - platform: button.press
    entity_id: button.oblamatik_start_fill
condition:
  - condition: numeric_state
    entity_id: number.oblamatik_fill_amount
    below: 200
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_start_fill
mode: single
```

```yaml
alias: "Emergency Stop on Leak"
trigger:
  - platform: state
    entity_id: binary_sensor.kitchen_leak
    to: "on"
action:
  - service: button.press
    target:
      entity_id: button.oblamatik_stop
mode: single
```

```yaml
alias: "Notify on Fill Complete"
trigger:
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "idle"
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "ready"
action:
  - service: persistent_notification.create
    data:
      title: "Fill Complete"
      message: "Water fill has finished."
mode: single
```

```yaml
alias: "Push Notify (Generic) on Fill Complete"
trigger:
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "idle"
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "ready"
action:
  - service: notify.notify
    data:
      title: "Fill Complete"
      message: "Water fill has finished."
mode: single
```
## Support
```yaml
alias: "Push Notify (Generic Android) on Fill Complete"
trigger:
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "idle"
  - platform: state
    entity_id: sensor.oblamatik_fill_state
    from: "running"
    to: "ready"
action:
  - service: notify.notify
    data:
      title: "Fill Complete"
      message: "Water fill has finished."
mode: single
```
## Support

If you encounter any issues, please check the **[Troubleshooting](Troubleshooting)** section first. 
You may also find answers in the **[FAQ](FAQ)** (PL + EN).
For bugs and feature requests, open an issue on [GitHub](https://github.com/bobsilesia/oblamatik/issues).

---
*This integration is an open-source project and is not affiliated with Oblamatik, Viega, KWC, or Crosswater.*
