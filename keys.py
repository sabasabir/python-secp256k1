import secrets
from curve import Curve, Point
from params import curve
from utils import encode_point_uncompressed


def generate_private_key():  # Random scalar < n
    return secrets.randbelow(curve.n)


def derive_public_key(private_key):  # Multiply by generator
    return private_key * curve.G


# Demo keypair
private_key = generate_private_key()
public_key_point = derive_public_key(private_key)
public_key_bytes = encode_point_uncompressed(public_key_point)

print("Private key (hex):", hex(private_key))
print("Public key (bytes):", public_key_bytes.hex())
