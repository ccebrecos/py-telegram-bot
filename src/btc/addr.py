"""
https://rosettacode.org/wiki/Bitcoin/address_validation#Python
"""
# Libraries
from hashlib import sha256

# Constants
DIGITS_58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def decode_base58(addr, length):
    n = 0
    for char in addr:
        n = n * 58 + DIGITS_58.index(char)
    return n.to_bytes(length, 'big')


def check_addr(addr):
    try:
        # Get addr in bytes
        addr_bytes = decode_base58(addr, 25)
        # Retrieve checksum
        cs = addr_bytes[-4:]
        # Check equality
        return cs == sha256(sha256(addr_bytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False
