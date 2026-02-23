## v2.1.3 (2026-02-23)
 
- Migracja integracji do `custom_components/oblamatik` zgodnie z zasadami projektu
- Poprawne rozładowywanie platform: `async_unload_platforms` w `__init__.py`
- Adnotacje typów i pełna asynchroniczność (zgodność z HA 2025.2+)
- Config Flow: dodany `OptionsFlow`, wykrywanie typu urządzenia, obsługa błędów
- WebSocket: użycie `async_get_clientsession(hass)`, obsługa `WSMsgType`, adnotacje typów
- Ujednolicone endpointy TLC w sensorach/number/switch (`/api/tlc/1/state/`)
- Lokalizacje: `strings.json` oraz `translations/en.json`
- CI: workflow `ruff`, `mypy`, `hassfest` na `push`/`pull_request`
- Release: workflow budujący ZIP dla HACS przy tagu `v*`
- HACS: dodany `hacs.json` (`zip_release`, minimalna wersja HA)
 
Instrukcje wydania:
- Zaktualizuj `manifest.json` jeśli zmieniasz wersję
- Utwórz tag zgodny z SemVer, np. `v2.1.3`
- Opublikuj release — workflow automatycznie doda `oblamatik.zip` jako asset
- Upewnij się, że README opisuje instalację, config_flow i wspierane platformy
