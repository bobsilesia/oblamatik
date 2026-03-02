# FAQ

## English

- **Why aggressive polling (keep-alive) during Hygiene?**  
  To prevent the device from sleeping or timing out during long operations, the integration polls status every second with a random `?q=` parameter, mirroring the official app behavior.

- **Safe limits for “Fill”?**  
  Recommended: `Fill Amount` 10–300 L, `Fill Temperature` 20–50°C. Add a guard condition in automations (e.g., `amount <= 200 L`).

- **Is “Fill” bathtub-only?**  
  No. Entities are universal (faucet/shower/bath). They call `tlc-bathtub-fill` API but use neutral names and icons.

- **Measuring Cup: why `quantity` vs `amount`?**  
  `tlc-measuring-cup/1/` expects `quantity` to dispense; `tlc-measuring-cup/1/save/` stores default `amount`. The integration supports both: number stores `amount`, button sends `quantity`.

- **How to stop immediately?**  
  Use `Emergency Stop` (stops flow and cancels hygiene). Keep it visible on the dashboard.

- **What does “Water Fill State” mean: ready / running / idle?**  
  `ready` – system ready, `running` – fill in progress, `idle` – no operation or returned to standby.

- **“IoT Serial Number” not always visible – why?**  
  On older firmware the value may only exist in `/inc/info.txt` or `/api/index.php?url=info`. The integration tries several sources and shows it when found.

- **What network modes are shown?**  
  `Access Point (wlan_ap)`, `Client (WiFi) (wlan_cl)`, `Client (Ethernet) (ethernet)`, `Client (Bridged) (br-lan)`. Icons and labels are adapted.

- **Can I schedule “Fill” purely by time?**  
  Yes, but add sensible conditions (presence, drain closed, amount guard) and a completion/error notification.
