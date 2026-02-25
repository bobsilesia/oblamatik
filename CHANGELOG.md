# Changelog

## v2.1.25 (2026-02-25)

- Naprawa widoczności przycisków w nowych wersjach HA: użycie `EntityCategory.CONFIG/DIAGNOSTIC`
- Uzupełnienie licencji MIT

## v2.1.24 (2026-02-25)

- Binary Sensor: Zmiana nazwy na "Drain Position", ikona `mdi:valve`
- Climate: Zmiana nazwy na "Temp Control", poprawa `unique_id`
- Sensor: Ikona pompy dla "Flow Rate", usunięcie IP z nazwy "Water Flow"
- Uptime: Fallback dla urządzeń KWC zwracających 0
- CI: Pełna weryfikacja `ruff` i `mypy`

## v2.1.23 (2026-02-25)

- Wymuszenie pre-checków CI w regułach projektu
- Poprawki formatowania `ruff`

## v2.1.22 (2026-02-25)

- Formatowanie Uptime: hh:mm
- Status: mapowanie "a" -> "ok"
- Fix: TLC15F Kitchen info/uptime fallback

## v2.1.21 (2026-02-25)

- Dodanie fallback endpointu `/api/tlc/1/` dla urządzeń TLC15F

## v2.1.20 (2026-02-25)

- Dodanie platformy `binary_sensor` (Popup/Drain)
- Dodanie przycisków: Restart WLAN, Testy funkcjonalne, Higiena

## v2.1.7 (2026-02-24)

- Rejestracja ConfigFlow zgodna z HA (`class ConfigFlow(..., domain=DOMAIN)`), eliminuje “Invalid handler specified”
- mypy: wyłączenie błędu `call-arg` dla config_flow
- Manifest: podbicie wersji do `2.1.7`

## v2.1.6 (2026-02-24)

- Automatyczne wydania: workflow GitHub tworzy Release i dołącza asset `oblamatik.zip` przy tagach `v*`
- Manifest: podbicie wersji do `2.1.6`
- Utrwalenie wymagań HACS: asset zawiera pliki integracji bezpośrednio w root ZIP

## v2.1.5 (2026-02-24)

- Naprawa config_flow: rejestracja klasy `ConfigFlow` i eliminacja zależności od `FlowResult`
- Stabilizacja połączeń HTTP: użycie sesji HA `aiohttp_client.async_get_clientsession(hass)`
- Spójne timeouty: `aiohttp.ClientTimeout(total=5)` we wszystkich wywołaniach HTTP
- Poprawki lint/format: `ruff` uporządkował importy, `mypy` bez błędów
- Manifest: podbicie wersji do `2.1.5`
- ZIP dla HACS: bez zagnieżdżeń, pliki integracji w root ZIP

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
