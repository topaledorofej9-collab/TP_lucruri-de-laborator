import sys

# Asigurăm afișarea corectă a caracterelor cu diacritice pe orice consolă (inclusiv Windows)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)

# Partea 1: apeluri pentru build_url și is_https
print("== Partea 1: Funcții ==")
print("Partea 1, build_url fără slash:", build_url("example.com", "login"))
print("Partea 1, build_url cu slash:", build_url("example.com", "/login"))
print("Partea 1, is_https pentru HTTPS:", is_https("https://example.com"))
print("Partea 1, is_https pentru HTTP:", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
print("\n== Partea 2: Trimiterea unei cereri ====")
print("Partea 2, show_response (example.com):")
show_response("https://example.com")
print("\nPartea 2, show_response (httpbin json):")
show_response("https://httpbin.org/json")

# Partea 3: apeluri pentru check_site
print("\n=== Partea 3: Un verificator reutilizabil ===")
print("Partea 3, check_site (site valid):", check_site("https://example.com"))
print("Partea 3, check_site (site inexistent):", check_site("http://this-site-does-not-exist.invalid"))

# Partea 4: apelul scan_sites()
print("\n=== Partea 4: Verificarea mai multor site-uri ===")
scan_sites()

# Partea 5: apeluri pentru check_headers
print("\n=== Partea 5: Audit de securitate ===")
print("Partea 5, check_headers (anteturi prezente):", check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("Partea 5, check_headers (site inexistent):", check_headers("http://this-site-does-not-exist.invalid"))

# Partea 6: apeluri pentru retry_check
print("\n=== Partea 6: Încercări repetate ===")
print("Partea 6, retry_check (status 200):", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check (status 404):", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check (status 500):", retry_check("https://httpbin.org/status/500", attempts=2))
print("Partea 6, retry_check (site inexistent):", retry_check("http://this-site-does-not-exist.invalid", attempts=2))