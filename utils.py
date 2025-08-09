from Cryptodome.Hash import keccak


def modinv(x, p):  # Modular inverse
    return pow(x, -1, p)


def keccak256(msg):  # Keccak-256 hash
    k = keccak.new(digest_bits=256)
    k.update(msg)
    return k.digest()


def encode_point_uncompressed(point):  # 0x04 | x | y
    return b"\x04" + point.x.to_bytes(32, "big") + point.y.to_bytes(32, "big")


def decode_point(bytestr):  # Parse uncompressed point
    if bytestr[0] != 0x04 or len(bytestr) != 65:
        raise ValueError("Invalid uncompressed point format")
    return (int.from_bytes(bytestr[1:33], "big"), int.from_bytes(bytestr[33:], "big"))
