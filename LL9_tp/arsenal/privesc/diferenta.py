from arsenal.privesc.enum import citeste_linii, nume, GTFO

# --- B1. Doua multimi: curat si acum ---
def cai(fisier):
    return set(citeste_linii(fisier))

baza = cai("arsenal/privesc/start/baza_suid.txt")
acum = cai("arsenal/privesc/start/suid.txt")
print("baza:", len(baza), " acum:", len(acum))

# --- B2. Diferenta: ce a aparut ---
noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

# --- B3. Dictionar de risc si filtrul final ---
risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)