import requests
import sys

# Asigurăm afișarea corectă a caracterelor cu diacritice pe orice consolă (inclusiv Windows)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


# Partea 1: Funcții ajutătoare
def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{host}{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


# Partea 2: Trimiterea unei cereri
def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        # Trimitem cererea GET cu timeout  pentru a preveni blovarea 
        r = requests.get(url, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
    except requests.RequestException as e:
        print(f"Eroare la accesarea adresei: {e}")


# Partea 3: Un verificator reutilizabil
def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        # Folosim timeout de 5 secunde 
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type"),
            "length": len(r.content),
            "server": r.headers.get("Server") or "unknown",
        }
    except requests.RequestException as e:
        # Gestionăm  erorile fără a opri execuția
        return {
            "status": None,
            "error": str(e),
        }


# Partea 4: Verificarea mai multor site-uri
def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    # Verificăm fiecare adresă din lista SITES
    for site in SITES:
        info = check_site(site)
        info["url"] = site
        results.append(info)

    # Filtrăm doar site-urile care au returnat codul de succes 200
    successful = [item for item in results if item.get("status") == 200]

    # Sortăm descrescător după length
    successful.sort(key=lambda item: item.get("length", 0), reverse=True)

    for item in successful:
        print(f"{item['url']} -> {item['status']}, {item['length']} octeți")

    # Afișăm rezumatul final (re )
    total_reusite = len(successful)
    total_esuate = len(results) - total_reusite
    print(f"Reușite: {total_reusite} | Eșuate: {total_esuate}")
    return results


# Partea 5: Audit de securitate
def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        present = []
        missing = []

        # Parcurgem lista de anteturi păstrând ordinea din SECURITY_HEADERS
        for header in SECURITY_HEADERS:
            # Dicționarul r.headers este case-insensitive
            if header in r.headers:
                present.append(header)
            else:
                missing.append(header)

        # Calculăm procentul antetelor prezente ca număr întreg
        score = int((len(present) / len(SECURITY_HEADERS)) * 100) if SECURITY_HEADERS else 0

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.RequestException as e:
        # În caz de eroare, returnăm status None și mesajul scurt
        return {
            "status": None,
            "error": str(e),
        }


# Partea 6: Încercări repetate
def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    last_status = None
    last_error = None
    count = 0

    for i in range(1, attempts + 1):
        count = i
        try:
            r = requests.get(url, timeout=5)
            last_status = r.status_code
            last_error = None
            # Dacă statusul este sub 500 (inclusiv 404), ne oprim imediat
            if r.status_code < 500:
                return {
                    "status": last_status,
                    "attempts": count,
                }
        except requests.RequestException as e:
            last_status = None
            last_error = str(e)

    # Dacă s-au epuizat încercările
    result = {
        "status": last_status,
        "attempts": count,
    }
    # Dacă toate încercările au eșuat din cauza unei erori de conexiune
    if last_status is None and last_error is not None:
        result["error"] = last_error

    return result
