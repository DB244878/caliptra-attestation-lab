# ESP32 + ATECC608A Hardware Attestation Lab

## Architecture

ESP32 acts as:
- host CPU
- embedded controller
- mini BMC / server node

ATECC608A acts as:
- hardware Root of Trust
- TPM-like secure element
- non-exportable key vault

## Flow

1. ESP32 creates firmware/config measurement
2. SHA256 digest computed
3. ATECC608A signs digest internally
4. Public key + signature exported
5. Python verifier validates signature

## Security Properties

- private key never leaves hardware
- hardware-backed signing
- immutable secure identity
- verifier-based trust decision

## Future Work

- DICE CDI derivation
- measured boot chain
- rollback protection
- WiFi verifier service
- BMC control plane
- fleet orchestration
