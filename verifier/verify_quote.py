from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import hashlib

MESSAGE = b"firmware_v1|config_v1|challenge_123"

DIGEST_HEX = "01387886617A4B91A6F5DAC53DD01A3B466ACC583DBF73881B8F78EDBEA1E911"

PUBLIC_KEY_HEX = "87DE789423496F3B8AC782BD800A44B094BFD3CADE19EF362B7F50F355D025B6A7114069E785EE8897C17278D25CA5467167FEAFEEBAA1A5B7E73A9F02B46265"

SIGNATURE_HEX = "4BBA651AE34B8D870C88D91D7C577F70B5306CE067BFBF2576FBA2AD43517D4633A59842870F765C52DD2C8226FC03BF12CB053D357268F477F07BF65A3A7668"

digest = bytes.fromhex(DIGEST_HEX)
public_key_raw = bytes.fromhex(PUBLIC_KEY_HEX)
sig_raw = bytes.fromhex(SIGNATURE_HEX)

expected_digest = hashlib.sha256(MESSAGE).digest()

print("Expected digest:", expected_digest.hex().upper())
print("Device digest:  ", digest.hex().upper())

if expected_digest != digest:
    print("❌ DIGEST MISMATCH")
    exit(1)

x = int.from_bytes(public_key_raw[:32], "big")
y = int.from_bytes(public_key_raw[32:], "big")

public_numbers = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1())
public_key = public_numbers.public_key()

r = int.from_bytes(sig_raw[:32], "big")
s = int.from_bytes(sig_raw[32:], "big")

der_sig = utils.encode_dss_signature(r, s)

try:
    public_key.verify(
        der_sig,
        digest,
        ec.ECDSA(utils.Prehashed(hashes.SHA256()))
    )

    print("✅ VALID SIGNATURE")
    print("✅ TRUSTED DEVICE + TRUSTED FIRMWARE")

except InvalidSignature:
    print("❌ INVALID SIGNATURE")
    print("❌ DO NOT TRUST DEVICE")
