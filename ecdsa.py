import secrets
from Cryptodome.Hash import keccak
from params import curve
from utils import modinv, keccak256


def sign(msg: bytes, private_key: int) -> tuple[int, int]:  # ECDSA signing
    z = int.from_bytes(keccak256(msg), "big")
    r = s = 0
    while r == 0 or s == 0:
        k = secrets.randbelow(curve.n)  # random nonce
        R = k * curve.G
        r = R.x % curve.n
        s = (modinv(k, curve.n) * (z + r * private_key)) % curve.n
    return (r, s)


def verify(msg: bytes, signature: tuple, public_key) -> bool:  # ECDSA verification
    r, s = signature
    z = int.from_bytes(keccak256(msg), "big")
    w = modinv(s, curve.n)
    u1 = (z * w) % curve.n
    u2 = (r * w) % curve.n
    point = u1 * curve.G + u2 * public_key
    return (point.x % curve.n) == r
