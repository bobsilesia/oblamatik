# Oblamatik — integracja Home Assistant

![Latest release](https://img.shields.io/github/v/release/bobsilesia/oblamatik?sort=semver) ![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg) ![CI](https://github.com/bobsilesia/oblamatik/actions/workflows/ci.yml/badge.svg?branch=main) ![Release](https://github.com/bobsilesia/oblamatik/actions/workflows/release.yml/badge.svg?branch=main)
![License](https://img.shields.io/github/license/bobsilesia/oblamatik) ![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json) ![Mypy](https://img.shields.io/badge/mypy-checked-blue)

[Latest release →](https://github.com/bobsilesia/oblamatik/releases)

Oblamatik to integracja dla Home Assistant, umożliwiająca sterowanie i odczyt parametrów urządzeń KWC/Viega/Crosswater (TLC).

## Wymagania
- Home Assistant Core 2025.2+
- Dostęp HTTP do urządzenia (np. `http://IP:PORT`)

## Instalacja (HACS)
1. Upewnij się, że repozytorium zawiera katalog `custom_components/oblamatik`.
2. Wydaj release z tagiem `vX.Y.Z` (np. `v2.0.10`). Workflow doda `oblamatik.zip` jako asset.
3. W HACS dodaj repozytorium jako niestandardowe (Custom repositories) lub skorzystaj z dostępnego źródła, jeśli repo jest publicznie wspierane przez HACS.
4. Zainstaluj integrację i zrestartuj Home Assistant.

## Instalacja (manualna)
1. Skopiuj folder `custom_components/oblamatik` do katalogu `config/custom_components/` Twojej instalacji Home Assistant.
2. Zrestartuj Home Assistant.

## Konfiguracja (Config Flow)
1. Przejdź do: Ustawienia → Urządzenia i usługi → Dodaj integrację → Oblamatik.
2. Podaj host (IP) i opcjonalnie port (domyślnie `80`).
3. Integracja wykryje typ urządzenia i utworzy odpowiednie encje.

## Wspierane platformy
- Sensor: temperatura, przepływ, wymagane parametry, stan urządzenia, pomocnicze encje (łazienka/prysznic).
- Switch: sterowanie przepływem wody, przełącznik ogrzewania.
- Climate: tryb ogrzewania i docelowa temperatura.
- Number: precyzyjne sterowanie wartością temperatury i przepływu.

## Lokalizacja
- Teksty interfejsu znajdują się w `strings.json` oraz `translations/en.json`.

## Zasady projektu
- Asynchroniczność (async/await).
- Walidacja schematów: `homeassistant.helpers.config_validation`.
- Ujednolicone endpointy TLC (`/api/tlc/1/` oraz `/api/tlc/1/state/`).
- Struktura katalogów: `custom_components/oblamatik/`.

## CI i publikacja
- CI: Ruff (lint/format), Mypy (typy), Hassfest (walidacja metadanych).
- Release: tag `vMAJOR.MINOR.PATCH` (np. `v2.0.10`) — workflow publikuje `oblamatik.zip`.
- Wersja w `manifest.json` powinna odpowiadać tagowi wersji.

## Rozwiązywanie problemów
- Sprawdź logi HA (Settings → System → Logs) dla błędów integracji.
- Upewnij się, że urządzenie zwraca poprawne odpowiedzi pod `http://IP:PORT/api/tlc/1/` i `http://IP:PORT/api/tlc/1/state/`.

## Współpraca (Contributing)

Chcesz pomóc w rozwoju projektu? Zapoznaj się z naszymi zasadami:
- [Zasady współpracy (CONTRIBUTING.md)](CONTRIBUTING.md)
- [Kodeks postępowania (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md)
- [Zgłoś błąd lub propozycję](https://github.com/bobsilesia/oblamatik/issues/new/choose)
