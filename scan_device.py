import socket
import requests
from requests.exceptions import RequestException
import sys

def scan_host(ip, ports):
    print(f"Skanowanie hosta {ip}...")
    
    # Skanowanie portów
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((ip, port), timeout=2):
                open_ports.append(port)
                print(f"Port {port} jest OTWARTY")
        except OSError:
            pass

    if not open_ports:
        print("Brak otwartych portów w badanym zakresie.")

    # Próba identyfikacji usług HTTP
    print("\nPróba połączenia HTTP na porcie 80...")
    try:
        response = requests.get(f"http://{ip}", timeout=3)
        print(f"Status HTTP: {response.status_code}")
        print(f"Nagłówek Server: {response.headers.get('Server', 'Nieznany')}")
        print(f"Tytuł strony: {extract_title(response.text)}")
    except RequestException as e:
        print(f"Błąd połączenia HTTP: {e}")

    # Sprawdzenie API Oblamatika (jeśli to już działa)
    print("\nSprawdzanie endpointów Oblamatik...")
    endpoints = [
        "/api/v1/status",
        "/api/tlc/1/state",  # Poprawny endpoint dla tego urządzenia
        "/api/tlc/1/",       # Główny endpoint z pełnymi danymi
        "/api/tlc/",
        "/api/",
        "/api/index.php",
        "/api/wlan/",
        "/status",
        "/cgi-bin/luci",
        "/cgi-bin/webui" # Stare interfejsy
    ]

    for endpoint in endpoints:
        try:
            url = f"http://{ip}{endpoint}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"[OK] {endpoint} (200)")
                print(f"Treść: {response.text[:100]}...")
            elif response.status_code == 403:
                print(f"[ZABRONIONE] {endpoint} (403 Forbidden)")
            elif response.status_code == 401:
                print(f"[AUTORYZACJA] {endpoint} (401 Unauthorized)")
            elif response.status_code != 404:
                print(f"[INFO] {endpoint} ({response.status_code})")
        except RequestException:
            pass
            
def extract_title(html):
    try:
        start = html.find("<title>") + len("<title>")
        end = html.find("</title>")
        if start > len("<title>") - 1 and end > start:
            return html[start:end]
    except:
        pass
    return "Brak tytułu"

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        target_ip = sys.argv[1]
    else:
        target_ip = "192.168.1.36"
    # Najczęstsze porty: 22 (SSH), 23 (Telnet), 80 (HTTP), 443 (HTTPS), 8080 (Alt HTTP)
    ports_to_scan = [21, 22, 23, 80, 443, 8080, 9090]
    scan_host(target_ip, ports_to_scan)
