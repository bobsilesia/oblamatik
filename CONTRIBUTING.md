# Współpraca przy projekcie Oblamatik

Cieszymy się, że chcesz pomóc w rozwoju integracji Oblamatik! Poniżej znajdziesz kilka wskazówek, które ułatwią nam współpracę.

## Zgłaszanie błędów

Jeśli znalazłeś błąd, zgłoś go w zakładce [Issues](https://github.com/bobsilesia/oblamatik/issues), korzystając z przygotowanego szablonu "Zgłoszenie błędu". Pamiętaj o dołączeniu logów i opisu kroków do powtórzenia błędu.

## Proponowanie zmian (Pull Requests)

1. **Fork**: Sforkuj repozytorium i utwórz nową gałąź dla swojej zmiany (`git checkout -b feature/moja-zmiana`).
2. **Standardy kodu**: Przestrzegamy rygorystycznych standardów jakości kodu.
   - Używamy `ruff` do lintingu i formatowania.
   - Używamy `mypy` do sprawdzania typów.
   - Kod musi być w pełni asynchroniczny (`async`/`await`).
3. **Lokalne testy**: Przed wysłaniem zmian uruchom:
   ```bash
   ruff format custom_components/oblamatik
   ruff check custom_components/oblamatik
   mypy custom_components/oblamatik
   ```
4. **Zatwierdź zmiany**: Opisz swoje zmiany w commit message w sposób jasny i zwięzły.
5. **Pull Request**: Wyślij PR do głównej gałęzi (`main`). Opisz, co zmienia Twój kod i dlaczego.

## Środowisko deweloperskie

Zalecamy korzystanie z `uv` lub `venv` do zarządzania zależnościami.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install homeassistant ruff mypy
```

## Struktura projektu

- `custom_components/oblamatik/` - Główny kod integracji.
- `.github/workflows/` - Konfiguracja CI/CD.

Dziękujemy za Twój wkład!
