# Troubleshooting

If you encounter issues with the Oblamatik integration, follow these steps to diagnose and resolve them.

## Common Issues

### 1. Integration initialization fails ("Connection refused" / "Timeout")

**Symptoms:**
- Error in Home Assistant logs: `ClientConnectorError: Cannot connect to host`
- Entities become unavailable.

**Solution:**
- Verify the device is powered on and connected to WLAN.
- Check if you can access `http://DEVICE_IP/` in your browser.
- Ensure the device has a **Static IP** assigned in your router. Dynamic IPs (DHCP) can change after a reboot, breaking the configuration.

### 2. Device shows `uptime: 0` or missing info

**Symptoms:**
- Sensor `sensor.uptime` shows `0` or `unknown`.
- Log warnings about "Primary endpoint failed".

**Solution:**
- This is a known behavior of some KWC/TLC15F devices.
- The integration automatically tries a fallback endpoint (`/api/tlc/1/state/`).
- If entities are working correctly (you can control water/temp), you can ignore this.
- Ensure you are running version **v2.1.25+** which includes improved fallback logic.

### 3. Button entities are missing (Tests, Hygiene)

**Symptoms:**
- You cannot find "Functional Test" or "Hygiene" buttons.

**Solution:**
- These buttons are categorized as `Diagnostic` or `Configuration`.
- Check if they are disabled by default in HA (Settings -> Devices -> Oblamatik -> Entities).
- Make sure you are on HA 2025.2+ and integration v2.1.25+.

### 4. Frequent polling/logs during Hygiene mode (Keep-Alive)

**Symptoms:**
- You see frequent network activity or logs when Hygiene mode is active.
- Device stays connected and responsive during long operations.

**Explanation:**
- The integration implements an aggressive **Keep-Alive mechanism** (polling every 1 second with `?q=random`) when the device is in a running state (Hygiene/Flow active).
- This is **required behavior** to prevent the device from timing out or sleeping during operation, mimicking the official app's behavior. Do not disable this.

### 5. Firmware Updates

**Status:**
- Official firmware updates for these modules (Viega/Oblamatik/Crosswater) are **not publicly available**.
- Known versions: `1.0-3.12`, `1.0-4.03`.
- **Warning:** Do not attempt to flash generic OpenWrt/Carambola firmware. This will likely brick your device and remove the proprietary Oblamatik control software.

## Debugging

To get detailed logs, enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.oblamatik: debug
```

Restart Home Assistant and check the logs (Settings -> System -> Logs) after reproducing the issue.
Paste these logs when opening a [Bug Report](https://github.com/bobsilesia/oblamatik/issues/new?template=bug_report.yml).

## API Endpoints

For advanced troubleshooting, you can check the following endpoints in your browser:

-   `http://IP/api/tlc/1/` (Primary)
-   `http://IP/api/tlc/1/state/` (Fallback for KWC)
-   `http://IP/api/tlc/1/popup/` (Drain state)
-   `http://IP/api/` (System info)
