# Installation

There are two ways to install the Oblamatik integration: using **HACS (Home Assistant Community Store)** or manually.

Language: [PL](#pl) | [EN](#en)

<a id="en"></a>

---

## Wersja PL (skrót)

<a id="pl"></a>

Są dwa sposoby instalacji integracji **Oblamatik**: przez **HACS** (zalecane) lub **manualnie**.

### Metoda 1: HACS (zalecane)
1. Otwórz **HACS** w Home Assistant.
2. Przejdź do **Integrations**.
3. W menu (trzy kropki) wybierz **Custom repositories**.
4. Podaj URL repozytorium: `https://github.com/bobsilesia/oblamatik`
5. Kategoria: **Integration** → **Add**.
6. Wyszukaj **Oblamatik** i **Download**.
7. **Restart Home Assistant**.

### Metoda 2: Manualna
1. Pobierz najnowsze wydanie (zip) z sekcji **Releases**.
2. Rozpakuj.
3. Skopiuj folder `custom_components/oblamatik` do `config/custom_components/`.
4. **Restart Home Assistant**.

Po restarcie przejdź do **Configuration** i dodaj integrację.

---

## Method 1: HACS (Recommended)

Installing via HACS is the easiest method as it allows for simple updates.

1.  Open **HACS** in Home Assistant.
2.  Click on **Integrations**.
3.  Click the **Menu** (three dots) in the top right corner and select **Custom repositories**.
4.  Enter the URL: `https://github.com/bobsilesia/oblamatik`
5.  Select category: **Integration**.
6.  Click **Add**.
7.  Once the repository is added, search for **Oblamatik** in the HACS store.
8.  Click **Download**.
9.  **Restart Home Assistant**.

## Method 2: Manual Installation

If you do not use HACS, you can install the integration manually.

1.  Download the latest release zip from the [GitHub Releases page](https://github.com/bobsilesia/oblamatik/releases).
2.  Unzip the file.
3.  Copy the `custom_components/oblamatik` folder to your Home Assistant `config/custom_components/` directory.
    - The path should look like: `/config/custom_components/oblamatik/__init__.py`.
4.  **Restart Home Assistant**.

## Post-Installation

After restarting, the integration is ready to be configured. Proceed to the **[Configuration](Configuration)** page.
