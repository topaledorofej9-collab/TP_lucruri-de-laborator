"""
Teste pentru decodorul universal.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from arsenal.forensics.decode import desfa, ghici_strat, citibil


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc%2Fpasswd")
    assert strat == "url"
    assert b == b"/etc/passwd"


def test_citibil():
    assert citibil(b"Hello World") == True
    assert citibil(b"\x00\x01") == False


def test_ghici_strat():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("U2FsdXQ=") == "base64"
    assert ghici_strat("!!!") == "necunoscut"


if __name__ == "__main__":
    test_base64()
    print("test_base64 OK")
    test_hex()
    print("test_hex OK")
    test_url()
    print("test_url OK")
    test_citibil()
    print("test_citibil OK")
    test_ghici_strat()
    print("test_ghici_strat OK")
    print("\nToate testele au trecut!")

