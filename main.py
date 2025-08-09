from keys import generate_private_key, derive_public_key
from utils import encode_point_uncompressed
from ecdsa import sign, verify
from params import curve

# 1. Generate key pair
priv_key = generate_private_key()
pub_key_point = derive_public_key(priv_key)
pub_key_bytes = encode_point_uncompressed(pub_key_point)

print("[+] Private key:", hex(priv_key))
print("[+] Public key:", pub_key_bytes.hex())

# 2. Message to sign
msg = b"Elliptic curves are cool"

# 3. Sign message
signature = sign(msg, priv_key)
print("[+] Signature:", signature)

# 4. Verify signature
is_valid = verify(msg, signature, pub_key_point)
print("[+] Signature valid?", is_valid)
