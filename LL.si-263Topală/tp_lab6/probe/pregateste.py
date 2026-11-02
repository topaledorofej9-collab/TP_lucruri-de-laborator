"""
Script de pregatire: genereaza fisierele-tinta pentru Laboratorul 6.
"""

import base64, os, hashlib, struct, zipfile, io

OUT = os.path.join(os.path.dirname(__file__))

# --- mesaj.txt: sir codat in mai multe straturi (hex -> base64 -> url) ---
text_original = "Securitatea incepe cu curiozitatea"
strat1 = text_original.encode().hex()                       # hex
strat2 = base64.b64encode(strat1.encode()).decode()         # base64 peste hex
strat3 = strat2.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")  # url peste base64
with open(os.path.join(OUT, "mesaj.txt"), "w") as f:
    f.write(strat3)
print("[+] mesaj.txt creat")

# --- xor.bin: text criptat cu XOR pe un octet ---
xor_text = b"Forensics dezvaluie ce ochiul nu vede"
xor_key = 42
xor_data = bytes(b ^ xor_key for b in xor_text)
with open(os.path.join(OUT, "xor.bin"), "wb") as f:
    f.write(xor_data)
print("[+] xor.bin creat (cheie:", xor_key, ")")

# --- hashuri.txt: hash-uri de spart ---
parole = ["parola", "admin", "securitate"]
with open(os.path.join(OUT, "hashuri.txt"), "w") as f:
    for p in parole:
        h = hashlib.md5(p.encode()).hexdigest()
        f.write(h + "\n")
print("[+] hashuri.txt creat")

# --- wordlist.txt: dictionar de parole ---
cuvinte = [
    "test", "password", "123456", "admin", "root",
    "parola", "securitate", "qwerty", "letmein", "welcome",
    "monkey", "dragon", "master", "login", "abc123"
]
with open(os.path.join(OUT, "wordlist.txt"), "w") as f:
    for c in cuvinte:
        f.write(c + "\n")
print("[+] wordlist.txt creat")

# --- foto.jpg: imagine JPEG cu EXIF si GPS ---
from PIL import Image
import struct

img = Image.new("RGB", (200, 150), color=(100, 149, 237))
# Desenam un gradient
px = img.load()
for y in range(150):
    for x in range(200):
        px[x, y] = (x % 256, y % 256, (x + y) % 256)

# Construim EXIF manual cu piexif
try:
    import piexif
except ImportError:
    os.system("pip install piexif")
    import piexif

# GPS: Chisinau, Moldova (47.0105, 28.8638)
def to_rational(val):
    d = int(val)
    m = int((val - d) * 60)
    s = int(((val - d) * 60 - m) * 60 * 100)
    return ((d, 1), (m, 1), (s, 100))

gps_ifd = {
    piexif.GPSIFD.GPSLatitudeRef: b"N",
    piexif.GPSIFD.GPSLatitude: to_rational(47.0105),
    piexif.GPSIFD.GPSLongitudeRef: b"E",
    piexif.GPSIFD.GPSLongitude: to_rational(28.8638),
}
exif_dict = {
    "0th": {
        piexif.ImageIFD.Make: b"LabCamera",
        piexif.ImageIFD.Model: b"Forensics-6",
        piexif.ImageIFD.Software: b"Python PIL",
    },
    "GPS": gps_ifd,
    "Exif": {},
    "1st": {},
}
exif_bytes = piexif.dump(exif_dict)
img.save(os.path.join(OUT, "foto.jpg"), "JPEG", exif=exif_bytes, quality=95)
print("[+] foto.jpg creat (cu EXIF si GPS: 47.0105 N, 28.8638 E)")

# --- ascuns.png: imagine PNG cu o arhiva ZIP lipita la coada ---
img2 = Image.new("RGB", (160, 120), color=(50, 50, 50))
px2 = img2.load()
for y in range(120):
    for x in range(160):
        px2[x, y] = ((x * 3) % 256, (y * 5) % 256, 128)

png_path = os.path.join(OUT, "ascuns.png")
img2.save(png_path, "PNG")

# Cream arhiva ZIP in memorie
zip_buf = io.BytesIO()
with zipfile.ZipFile(zip_buf, "w") as zf:
    zf.writestr("secret.txt", "Felicitari! Ai gasit fisierul ascuns in imagine.\n")
zip_bytes = zip_buf.getvalue()

# Lipim ZIP-ul la coada PNG-ului
with open(png_path, "ab") as f:
    f.write(zip_bytes)
print("[+] ascuns.png creat (cu arhiva ZIP ascunsa)")

print("\n=== Toate fisierele au fost generate in", OUT, "===")

