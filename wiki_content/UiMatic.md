# UiMatic — Lovelace Card

UiMatic is a modern, minimalist Lovelace custom card for Home Assistant to control Oblamatik / KWC / Viega / Crosswater bath controllers.

Project: https://github.com/bobsilesia/UiMatic

## Features
- Temperature control (10–45°C) — arc dial (classic) or iOS-style drum picker (modern)
- Water ON/OFF button (with ripple animation)
- Flow rate control (0–10 L/min) — arc dial or drum picker
- Drain open/close toggle (default: open, flood-safe)
- Toast notifications on action
- Two layouts: `classic` and `modern`

## Installation

### HACS (recommended)
1. In HACS, click ⋮ → Custom repositories
2. Add URL: `https://github.com/bobsilesia/UiMatic` → Category: `Dashboard`
3. Download, then hard refresh the browser (Ctrl+Shift+R / Cmd+Shift+R)

### Manual
1. Download `oblamatik-card.js` from the latest UiMatic release
2. Copy it to `/config/www/oblamatik-card.js`
3. In Home Assistant: Settings → Dashboards → Resources → Add resource:
   - URL: `/local/oblamatik-card.js`
   - Type: JavaScript module
4. Restart Home Assistant

## Configuration

### Step 1 — Find your entity IDs
Go to Developer Tools → States and filter by `oblamatik`.

### Step 2 — Add the card
Add a Manual card with YAML like this (replace entity IDs with yours):

```yaml
type: custom:oblamatik-card
name: Bath Controller
entity_switch: switch.water_flow_192.168.1.36
entity_temperature: sensor.temperature_192.168.1.36
entity_flow: sensor.flow_rate_192.168.1.36
entity_drain: binary_sensor.bath_drain_192.168.1.36
entity_number_temp: number.temperature_192.168.1.36
entity_number_flow: number.flow_rate_192.168.1.36
min_temp: 10
max_temp: 45
min_flow: 0
max_flow: 10
layout: classic
```

UiMatic supports entity IDs that contain dots in the IP address. Your exact entity IDs may differ depending on your Home Assistant naming and detected device model.
