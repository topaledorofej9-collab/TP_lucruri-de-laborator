"""
Steganografie LSB — Laboratorul 6, Lucrarea B (B5-B6)
"""

from PIL import Image


# ── B5. Ascunderea mesajului prin LSB ──

def ascunde_lsb(cale_intrare, mesaj_bytes, cale_iesire="stego.png"):
    img = Image.open(cale_intrare).convert("RGB")
    px = list(img.getdata())

    # Adaugam un octet 0 ca terminator
    mesaj_bytes += b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_bytes)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul e prea mare pentru aceasta imagine")

    px_nou = []
    idx_bit = 0
    for (r, g, b) in px:
        canale = [r, g, b]
        for i in range(3):
            if idx_bit < len(biti):
                canale[i] = (canale[i] & ~1) | int(biti[idx_bit])
                idx_bit += 1
        px_nou.append(tuple(canale))

    img.putdata(px_nou)
    img.save(cale_iesire, "PNG")
    return cale_iesire


# ── B6. Dezvaluirea mesajului ──

def dezvaluie_lsb(cale):
    px = list(Image.open(cale).convert("RGB").getdata())
    biti = ""
    for (r, g, b) in px:
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    # Grupam cate 8 biti si convertim in octeti
    octeti = []
    for i in range(0, len(biti), 8):
        octet = int(biti[i:i+8], 2)
        if octet == 0:
            break
        octeti.append(octet)

    return bytes(octeti)


# ── Rulare ──

if __name__ == "__main__":
    mesaj = b"FLAG{ascuns_in_pixeli}"

    print("=== B5. Ascundere LSB ===")
    fisier = ascunde_lsb("probe/foto.jpg", mesaj, "stego.png")
    print(f"  Mesaj ascuns: {mesaj.decode()}")
    print(f"  Imagine salvata: {fisier}")
    print()

    print("=== B6. Dezvaluire LSB ===")
    gasit = dezvaluie_lsb("stego.png")
    print(f"  Mesaj gasit: {gasit.decode()}")
    print(f"  Verificare: {'OK' if gasit == mesaj else 'EROARE'}")

