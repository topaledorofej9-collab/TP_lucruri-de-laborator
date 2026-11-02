"""
Forensics pe fisiere — Laboratorul 6, Lucrarea B (B1-B4)
"""

import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS


# ── B1. Magic bytes ──

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap[:4] == b"%PDF":
        return "pdf"
    if cap[:4] == b"\x89PNG":
        return "png"
    if cap[:2] == b"\xff\xd8":
        return "jpeg"
    if cap[:4] == b"PK\x03\x04":
        return "zip/docx"
    return cap.hex()


# ── B2. Strings ──

def extrage_strings(cale, minim=4):
    date = open(cale, "rb").read()
    rezultate = []
    for m in re.findall(rb"[ -~]{" + str(minim).encode() + rb",}", date):
        rezultate.append(m.decode())
    return rezultate


# ── B3. Metadate EXIF și GPS din poză ──

def citeste_exif(cale):
    img = Image.open(cale)
    exif = img._getexif() or {}
    info = {}
    for id_tag, val in exif.items():
        nume = TAGS.get(id_tag, id_tag)
        info[nume] = val
    return info


def gps_grade(coord, ref):
    """Converteste coordonate GPS din (grade, minute, secunde) in grade zecimale."""
    d = float(coord[0])
    m = float(coord[1])
    s = float(coord[2])
    grade = d + m / 60.0 + s / 3600.0
    if ref in (b"S", b"W", "S", "W"):
        grade = -grade
    return round(grade, 6)


def citeste_gps(cale):
    img = Image.open(cale)
    exif = img._getexif() or {}
    gps_data = exif.get(34853, {})
    if not gps_data:
        return None, None

    lat = gps_grade(gps_data[2], gps_data[1])
    lon = gps_grade(gps_data[4], gps_data[3])
    return lat, lon


# ── B4. File carving ──

def extrage_ascuns(cale, output="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i != -1:
        open(output, "wb").write(date[i:])
        return i, output
    return -1, None


# ── Rulare ──

if __name__ == "__main__":
    print("=== B1. Magic bytes ===")
    print("foto.jpg:", tip_real("probe/foto.jpg"))
    print("ascuns.png:", tip_real("probe/ascuns.png"))
    print()

    print("=== B2. Strings din ascuns.png ===")
    siruri = extrage_strings("probe/ascuns.png")
    for s in siruri[:15]:
        print(" ", s)
    print()

    print("=== B3. Metadate EXIF ===")
    info = citeste_exif("probe/foto.jpg")
    for k, v in info.items():
        if k != "GPSInfo":
            print(f"  {k} = {v}")

    lat, lon = citeste_gps("probe/foto.jpg")
    print(f"\n  GPS: {lat} N, {lon} E")
    print(f"  Link harta: https://www.google.com/maps?q={lat},{lon}")
    print()

    print("=== B4. File carving ===")
    offset, fisier = extrage_ascuns("probe/ascuns.png", "gasit.zip")
    print(f"  Arhiva gasita la octetul {offset}")
    if fisier:
        with zipfile.ZipFile(fisier) as zf:
            print("  Continut arhiva:", zf.namelist())
            for name in zf.namelist():
                print(f"  [{name}]:", zf.read(name).decode())

