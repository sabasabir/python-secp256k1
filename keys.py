import secrets
from curve import Curve, Point
from params import curve
from utils import encode_point_uncompressed


def generate_private_key():  # Random scalar < n
    return secrets.randbelow(curve.n)


def derive_public_key(private_key):  # Multiply by generator
    return private_key * curve.G
