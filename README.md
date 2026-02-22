# Oblamatik Home Assistant Custom Integration

## 🎯 Opis

Integracja **Oblamatik** dla Home Assistant umożliwia sterowanie urządzeniami KWC (KWC Direct) za pomocą interfejsu API.

## 🚀 Funkcjonalność

### 🔄 Przełączniki (Switch)
- **Water Flow** - włącz/wyłącz przepływ wody
- **Heating** - włącz/wyłącz ogrzewanie

### 🌡️ Klimatyzacja (Climate)
- **Kontrola temperatury** - ustawianie temperatury wody
- **Tryby HVAC** - grzanie, chłodzenie, automatyczne

### 📊 Sensory (Sensor)
- **Temperatura** - aktualna temperatura wody
- **Przepływ** - aktualny przepływ wody
- **Status urządzenia** - stan połączenia

### 🔢 Precyzyjna kontrola (Number)
- **Temperatura** - precyzyjne ustawienie temperatury
- **Przepływ** - precyzyjne ustawienie przepływu

## 📋 Wymagania

- Home Assistant >= 2023.1
- aiohttp (dla zapytań HTTP)
- Dostęp do sieci urządzenia KWC

## 🎨 Ikona

Integracja używa oficjalnej ikony z repozytorium Home Assistant brands.

## 📦 Instalacja

1. Skopiuj folder `oblamatik-hacs` do `custom_components/oblamatik/`
2. Zrestartuj Home Assistant
3. Dodaj integrację w Ustawienia > Integracje

## 📄 Wersja

**v2.0.3** - najnowsza wersja z poprawkami:
- Naprawiono błędy konfiguracji 500
- Dodano wsparcie dla wielu urządzeń
- Poprawiono obsługę flagi `changed`
- Dodano oficjalną ikonę

## 👨‍💻 Autor

Robert Psiurski - rozwój i utrzymanie integracji Home Assistant
