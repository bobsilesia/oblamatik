# Diagnostic Sensors

Oblamatik integration provides several diagnostic sensors to help you monitor the health and performance of your device connection. These sensors are disabled by default or hidden in the "Diagnostic" category, but can be extremely useful for troubleshooting.

## Available Diagnostic Sensors

### 1. Ping (Latency)
- **Entity ID**: `sensor.oblamatik_ip_ping`
- **Unit**: `ms` (milliseconds)
- **Description**: Measures the round-trip time for a lightweight API call (`/api/`) to the device.
- **Update Frequency**: Same as the integration polling interval (default 5 minutes).
- **Use Case**: High latency (>500ms) might indicate weak Wi-Fi signal or network congestion.

### 2. Connection Reliability
- **Entity ID**: `sensor.oblamatik_ip_reliability`
- **Unit**: `%` (percentage)
- **Description**: Calculates the success rate of API calls since the integration started.
- **Formula**: `(Successful Calls / Total Attempts) * 100`
- **Use Case**: 
  - `100%`: Perfect connection.
  - `< 90%`: Occasional packet loss.
  - `< 50%`: Severe connectivity issues, device might be unreachable often.

### 3. Wi-Fi Signal (dBm)
- **Entity ID**: `sensor.oblamatik_ip_signal_dbm`
- **Unit**: `dBm`
- **Description**: Shows the Received Signal Strength Indicator (RSSI) of the device's Wi-Fi connection.
- **Values**:
  - `-30` to `-50 dBm`: Excellent
  - `-50` to `-60 dBm`: Very Good
  - `-60` to `-70 dBm`: Good
  - `-70` to `-80 dBm`: Weak (might cause timeouts)
  - `< -80 dBm`: Very Weak (unreliable)
- **Note**: Supports both devices reporting raw RSSI (negative values) and those reporting signal bars/quality (positive values), automatically converting them to standard dBm.

### 4. IoT Hardware Vendor
- **Entity ID**: `sensor.oblamatik_ip_iot_vendor`
- **Description**: Identifies the manufacturer of the Wi-Fi module based on its MAC Address (OUI).
- **Common Values**:
  - `8devices (Carambola2)`: Standard module used in many Oblamatik/KWC devices.
  - `Raspberry Pi`: If running on a DIY gateway.
  - `Espressif`: If using an ESP-based bridge.

## How to Enable Diagnostic Sensors
1. Go to **Settings** -> **Devices & Services**.
2. Click on **Oblamatik**.
3. Select your device.
4. Look for the **Diagnostic** section.
5. If a sensor is disabled, click on it -> **Advanced** (gear icon) -> **Enable**.
