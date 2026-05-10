# Mini Caliptra Hardware Attestation Lab

Hardware-backed attestation lab using:

- ESP32
- ATECC608A secure element
- Python verifier

This project models core concepts behind:

- Caliptra
- TPMs
- DICE attestation
- Azure host attestation
- Nitro-style platform security

## Hardware

- ESP32 Dev Board
- ATECC608A secure element
- Breadboard + jumper wires

## Wiring

| ATECC608A | ESP32 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GPIO21 |
| SCL | GPIO22 |

## Features

- hardware-backed ECC identity
- non-exportable private keys
- SHA256 measurement hashing
- hardware signature generation
- Python verifier validation

## Repo Structure

device/
- esp32_atecc_attester.ino

verifier/
- verify_quote.py

docs/
- hardware_lab.md

## Example Verifier Output

✅ VALID SIGNATURE  
✅ TRUSTED DEVICE + TRUSTED FIRMWARE

