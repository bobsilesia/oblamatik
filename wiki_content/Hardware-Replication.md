# Hardware Replication & Cloning Guide

To guide explains how to replicate or clone the Oblamatik/Viega WLAN module based on the findings from the [bobsilesia/viega_multiplex_trio_e](https://github.com/bobsilesia/viega_multiplex_trio_e) repository.

---

## Wersja PL (skrót)

Architektura:
- Rdzeń: **8devices Carambola 2** (OpenWrt, MIPS AR9331).
- Interfejs: **RS232** do jednostki kąpielowej (konwersja poziomów wymagana: **MAX3232**).
- Zasilanie: sprawdź **VCC** (brązowy przewód), użyj przetwornicy do 3.3V/5V.

Klonowanie:
- Opcja A (1:1): Carambola 2 + OpenWrt + lighttpd + PHP, wyłącz konsolę na UART, skopiuj `/www`.
- Opcja B (emulacja): ESP32/RPi + MAX3232, logika „HTTP → Serial → HTTP”.

Bezpieczeństwo:
- Nigdy nie łącz bezpośrednio RS232 z TTL – używaj **MAX3232**.
- Nie flashuj przypadkowego OpenWrt na oryginalnym module – ryzyko brick.

Zrzut firmware:
- Konsola UART → U-Boot/Failsafe → odczyt MTD/TFTP.

---
## 1. Hardware Architecture

The original module consists of:
*   **Core:** [8devices Carambola 2](https://8devices.com/products/carambola-2) (Qualcomm Atheros AR9331 SoC, MIPS 24k, WiFi 802.11n).
*   **Interface:** RS232 (Serial) communication with the bath unit.
*   **Voltage Levels:** The Carambola 2 operates at **3.3V TTL**, while the bath unit uses **RS232** voltage levels (up to +/- 12V).
*   **Connector:** 4-wire connection (VCC, GND, TX, RX) via a JST-XH 6-pin connector.

### Pinout (Module Side)
*   **White:** GND
*   **Green:** RX (Data from Bath -> Module)
*   **Yellow:** TX (Data from Module -> Bath)
*   **Brown:** VCC (Power input)

## 2. Cloning Strategy

Since the original firmware (`1.0-4.03`) is essentially OpenWrt + PHP scripts, you do not need the exact binary dump. You can replicate the functionality by setting up a compatible environment.

### Option A: 1:1 Replica (Carambola 2)
This method recreates the original hardware environment.

**Requirements:**
*   8devices Carambola 2 module (or Dev Board).
*   MAX3232 breakout board (RS232 to TTL converter).
*   Power Supply (Step-down converter if VCC from bath is >3.3V).

**Software Setup:**
1.  **Flash OpenWrt:** Install a standard OpenWrt image supported by Carambola 2 (e.g., 15.05 Chaos Calmer or 17.01 LEDE, as newer kernels might be heavy for this old SoC, though 19.07/21.02 might work).
2.  **Install Packages:**
    ```bash
    opkg update
    opkg install lighttpd lighttpd-mod-cgi php7-cgi  # Or php5-cgi for older builds
    ```
    *Note: If the original scripts use legacy PHP functions, you might need an older PHP version.*
3.  **Disable Serial Console:**
    The Carambola 2 uses the UART port for the system console by default. You must disable this to allow the PHP scripts to control the port.
    *   Edit `/etc/inittab`: Comment out the line referencing `ttyS0` or `ttyATH0`.
    *   Edit `/etc/sysctl.conf` or boot parameters to stop kernel messages on serial.
4.  **Deploy Application:**
    *   Copy the `/www/` contents from the repository to `/www/` on the device.
    *   Configure `lighttpd.conf` to serve PHP files and listen on port 80.
    *   Ensure permissions are set (`chmod +x` for any shell scripts).

### Option B: Modern Emulation (ESP32 / Raspberry Pi)
Instead of sourcing an old Carambola 2, you can emulate the logic.

**Hardware:**
*   **ESP32 / ESP8266:** Requires a MAX3232 converter (3.3V TTL <-> RS232).
*   **Raspberry Pi Zero W:** Requires a MAX3232 converter.

**Software Logic:**
The original logic is "Stateless HTTP -> Serial Command".
1.  **Receive HTTP Request:** e.g., `GET /api/fill`.
2.  **Send Serial Command:** Send the corresponding hex/string command to the RS232 port.
3.  **Read Response:** Wait for confirmation from the bath unit.
4.  **Return HTTP Response:** Send JSON/Text back to the client.

## 3. Critical Notes
*   **RS232 vs TTL:** NEVER connect the bath unit's RS232 lines directly to a microcontroller (ESP/RPi/Carambola). The high voltage will destroy the GPIOs. Always use a **MAX3232** (or equivalent) level shifter.
*   **Power:** Check the voltage on the Brown wire (VCC) from the bath. It might be 5V or 12V. Use a Step-Down (Buck) converter to provide stable 3.3V (or 5V for RPi) to your clone module.

## 4. Recovering/Dumping Original Firmware
If you possess a working unit and want the exact `1.0-4.03` image:
1.  **Serial Console:** Solder wires to the Carambola's console pins.
2.  **Bootloader:** Interrupt boot (press 'f' or any key) to enter U-Boot/Failsafe.
3.  **Read Flash:** Use `cat /dev/mtd0 > /tmp/dump.bin` (if Linux boots) or U-Boot commands to read memory and transfer via TFTP/Serial (kermit).
