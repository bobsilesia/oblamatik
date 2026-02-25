# Configuration

Setting up the Oblamatik integration is done through the Home Assistant UI using the **Config Flow**.

## Adding the Integration

1.  In Home Assistant, go to **Settings > Devices & Services**.
2.  Click **+ ADD INTEGRATION** in the bottom right corner.
3.  Search for **Oblamatik**.
4.  Enter the **Host** (IP address) of your device.
    - Example: `192.168.1.50`
    - **Port**: Default is `80`. Change if your device uses a different port.
5.  Click **Submit**.

## Device Detection

The integration will automatically attempt to connect to the device and detect its type (e.g., Viega Multiplex Trio E, KWC Faucet).

-   If successful, a new device will be created with all available entities.
-   If connection fails, verify the IP address and ensure the device is powered on.

## Options

After setup, you can access the integration options:

-   Go to **Settings > Devices & Services > Oblamatik**.
-   Click **Configure**.
-   Here you can update the **Host** or **Port** if they change.

> **Note:** We strongly recommend assigning a **Static IP** to your Oblamatik device in your router settings to prevent connection issues after a reboot.
