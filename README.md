# secp256k1-ecdsa-poc

A minimal Python implementation of the secp256k1 elliptic curve and ECDSA digital signatures.  
Includes full curve math, key generation, signing, and verification.

## Features
- secp256k1 curve operations (point addition, doubling, scalar multiplication)
- Private/public key generation
- Message signing with ECDSA (Keccak-256)
- Signature verification

## Install
```bash
git clone https://github.com/0xMouiz/python-secp256k1.git
cd secp256k1-ecdsa-poc
pip install pycryptodome
```

## Usage
```bash
python3 main.py
```

## Example Output
```bash
[+] Private key: 0x1393b6573adf24c61b73561768d9ea4ba1670dcc77554f25938cbca621ed7645

[+] Public key: 0475ca8eaf8393377b7026664e661f63c130db105be05dd26f4431095feeed37ea48f35d4c941730943c37f5df7402e3afbbfd6e0739c67474218f8abdcd4a4dbe

[+] Signature: (23130664403154537087452900596597043914635898182345128000144997681634561679895, 80900801433921084062591453631520598013543041876276918936230036858357811199263)

[+] Signature valid? True
```

## How It Works
1. Generates a random 256-bit private key.

2. Derives the corresponding public key by scalar multiplication of the generator point `G` on the secp256k1 curve.

3. Hashes the input message with Keccak-256.

4. Produces an ECDSA signature `(r, s)`.

5. Verifies the signature using the public key.