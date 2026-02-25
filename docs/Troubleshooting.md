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
