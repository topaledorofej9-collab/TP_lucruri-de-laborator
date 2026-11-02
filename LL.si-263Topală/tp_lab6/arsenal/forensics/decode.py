"""
Decoder universal — Laboratorul 6, Lucrarea A
"""
import re
import base64
import hashlib
import argparse
import json
from urllib.parse import unquote


# ── A1. Text si octeti ──

s = "Salut"
b = s.encode()
print("=== A1. Text si octeti ===")
print("bytes:", b, "  b[0]:", b[0])
print("hex:", b.hex())
print("din hex:", bytes.fromhex(b.hex()))
print()


# ── A2. Recunoasterea stratului ──

def ghici_strat(s):
    if "%" in s and re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"


# ── A3. Desfacerea stratului ──

def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    elif strat == "hex":
        return strat, bytes.fromhex(s)
    elif strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()


# ── A4. Decodare in bucla ──

def citibil(b):
    return all(32 <= c < 127 for c in b)


def decodare_completa(val):
    """Desfasoara toate straturile pana la text citibil."""
    straturi = []
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut":
            break
        straturi.append(strat)
        try:
            val_nou = b.decode()
        except UnicodeDecodeError:
            break
        if citibil(b) and ghici_strat(val_nou) == "necunoscut":
            return straturi, b
        val = val_nou
    return straturi, b


# ── A5. XOR brute-force ──

def sparge_xor(cale):
    date = open(cale, "rb").read()
    candidati = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            text = clar.decode()
            nr_litere = sum(c.isalpha() for c in text)
            nr_spatii = text.count(" ")
            candidati.append((nr_litere + nr_spatii * 5, k, text))
    if candidati:
        candidati.sort(reverse=True)
        _, k, text = candidati[0]
        return k, text
    return None, None


# ── A6. Hash prin dictionar ──

def sparge_hash(cale_hash, cale_wordlist):
    tinta = open(cale_hash).readline().strip()
    lung = len(tinta)

    if lung == 32:
        alg = "md5"
    elif lung == 40:
        alg = "sha1"
    elif lung == 64:
        alg = "sha256"
    else:
        return None, None, None

    for cuv in open(cale_wordlist, encoding="latin1"):
        cuv = cuv.strip()
        h = hashlib.new(alg, cuv.encode()).hexdigest()
        if h == tinta:
            return alg, cuv, tinta
    return alg, None, tinta


# ── Rulare demonstrativa ──

if __name__ == "__main__":
    print("=== A2. Recunoasterea stratului ===")
    print("ghici_strat('%2Fetc'):", ghici_strat("%2Fetc"))
    print("ghici_strat('48656c6c6f'):", ghici_strat("48656c6c6f"))
    print("ghici_strat('U2FsdXQ='):", ghici_strat("U2FsdXQ="))
    print()

    print("=== A3. Desfacerea stratului ===")
    print("desfa('U2FsdXQ='):", desfa("U2FsdXQ="))
    print("desfa('48656c6c6f'):", desfa("48656c6c6f"))
    print()

    # A4. Mesaj cu straturi multiple
    print("=== A4. Decodare in bucla ===")
    mesaj = open("probe/mesaj.txt").read().strip()
    print("Mesaj codat:", mesaj[:60], "...")
    straturi, rezultat = decodare_completa(mesaj)
    print("Straturi gasite:", straturi)
    print("Text final:", rezultat.decode() if isinstance(rezultat, bytes) else rezultat)
    print()

    # A5. XOR
    print("=== A5. Spargere XOR ===")
    cheie, text_xor = sparge_xor("probe/xor.bin")
    print("Cheie gasita:", cheie)
    print("Text:", text_xor)
    print()

    # A6. Hash
    print("=== A6. Spargere hash ===")
    alg, parola, hash_val = sparge_hash("probe/hashuri.txt", "probe/wordlist.txt")
    print("Algoritm:", alg)
    print("Hash:", hash_val)
    print("Parola gasita:", parola)
    print()

    # ── A7. argparse si fisa JSON ──

    print("=== A7. Salvare fisa JSON ===")
    fisa = {
        "mesaj_codat": {
            "straturi": straturi,
            "rezultat": rezultat.decode() if isinstance(rezultat, bytes) else str(rezultat)
        },
        "xor": {
            "cheie": cheie,
            "text": text_xor
        },
        "hash": {
            "algoritm": alg,
            "hash": hash_val,
            "parola": parola
        }
    }
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)
    print("Fisa salvata in arsenal/forensics/fisa.json")
    print(json.dumps(fisa, indent=2, ensure_ascii=False))