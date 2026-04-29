# Project Notes

## Current Version

This version implements a simulated hardware attestation flow using:

- Arduino Mega 2560 as the device / simulated Root of Trust
- Python verifier as the cloud-side verifier
- Serial over USB as the mailbox-style communication interface

## Current Flow

1. Device boots
2. Device derives DICE-style identities
3. Verifier requests attestation
4. Device returns firmware measurement and signature
5. Verifier validates signature
6. Verifier checks firmware measurement against policy
7. Verifier allows or denies trust

## Next Hardware Upgrade

The next version will integrate an ATECC608A secure element to replace the software-based device secret with a hardware-backed non-extractable key.
