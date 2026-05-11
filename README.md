# Hardware Root of Trust Attestation

A hands-on hardware security project demonstrating a simplified hardware-backed attestation flow using an ESP32, ATECC608A secure element, and a Python verifier.

This project models how modern cloud infrastructure can determine whether a device or node should be trusted before allowing it into a secure fleet.

---

# What This Project Demonstrates

This project demonstrates core platform security concepts including:

- Hardware root of trust
- Device identity
- Firmware measurement
- Signed attestation quotes
- Verifier-side trust policy
- Fleet admission and quarantine logic
- Rollback detection
- Hardware-backed vs software-only trust models

The goal is to build a working educational model of a modern attestation pipeline.

---

# Architecture

```text
+-----------------------------+
| ESP32 Device                |
|                             |
|  Firmware Measurement       |
|  Runtime State              |
|  Quote Generation           |
+-------------+---------------+
              |
              | I2C
              v
+-----------------------------+
| ATECC608A Secure Element    |
|                             |
|  Protected device key       |
|  Signs attestation quote    |
+-------------+---------------+
              |
              | Serial / USB
              v
+-----------------------------+
| Python Verifier             |
|                             |
|  Reads quote                |
|  Verifies signature         |
|  Verifies firmware digest   |
|  Checks rollback version    |
|  Applies trust policy       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Fleet Decision Engine       |
|                             |
| TRUST / SIMULATION /        |
| QUARANTINE                  |
+-----------------------------+
```

---

# Repository Structure

```text
hardware-root-of-trust-attestation-lab/
├── device/
│   ├── mini_rot.ino
│   └── esp32_atecc_attester.ino
│
├── verifier/
│   ├── requirements.txt
│   ├── verify_quote.py
│   ├── verifier.py
│   └── fleet_verifier.py
│
└── README.md
```

---

# Conceptual Mapping

| Lab Component | Real-World Concept |
|---|---|
| ESP32 | Device or platform controller |
| ATECC608A | Hardware root of trust |
| Firmware digest | Firmware measurement |
| Signed quote | Attestation evidence |
| Python verifier | Cloud verifier service |
| Fleet verifier | Datacenter trust policy engine |
| Quarantine result | Node rejected from trusted fleet |

---

# Single Device Verification

From the repository root:

```bash
cd verifier
pip3 install -r requirements.txt
python3 verify_quote.py
```

Expected output:

```text
Expected digest: 01387886617A4B91A6F5DAC53DD01A3B466ACC583DBF73881B8F78EDBEA1E911
Device digest:   01387886617A4B91A6F5DAC53DD01A3B466ACC583DBF73881B8F78EDBEA1E911
✅ VALID SIGNATURE
✅ TRUSTED DEVICE + TRUSTED FIRMWARE
```

This proves:

1. Firmware measurement matches expected policy
2. Signature validation succeeds
3. Device identity is trusted

---

# Fleet Verification

From inside the verifier directory:

```bash
python3 fleet_verifier.py
```

Expected output:

```text
=== Hardware Root of Trust Fleet Verifier ===
node-a-esp32-atecc608a: TRUSTED_HARDWARE_BACKED_NODE
node-b-simulated: TRUSTED_SIMULATION_ONLY: valid software model, not hardware-backed
node-c-bad-fw: QUARANTINE: firmware measurement mismatch
node-d-rollback: QUARANTINE: rollback detected
node-e-bad-signature: QUARANTINE: invalid attestation signature
```

---

# Fleet Policy Logic

The verifier classifies nodes into different trust states.

## Trusted Hardware-Backed Node

```text
TRUSTED_HARDWARE_BACKED_NODE
```

This node has:

- Valid firmware
- Valid signature
- Acceptable firmware version
- Hardware-backed device identity

---

## Trusted Simulation Node

```text
TRUSTED_SIMULATION_ONLY
```

This node passes software verification but does not use protected hardware keys.

Useful for development and testing environments.

---

## Firmware Mismatch

```text
QUARANTINE: firmware measurement mismatch
```

The firmware measurement does not match approved policy.

The node is rejected from the trusted fleet.

---

## Rollback Detection

```text
QUARANTINE: rollback detected
```

The node attempts to boot older firmware than the approved minimum version.

Rollback protection prevents reuse of vulnerable firmware.

---

## Invalid Signature

```text
QUARANTINE: invalid attestation signature
```

The attestation evidence cannot be cryptographically verified.

The verifier rejects the node.

---

# Why This Matters

Modern cloud platforms must verify infrastructure trustworthiness before allowing systems to serve workloads.

This project demonstrates the same high-level security flow used in modern infrastructure attestation systems:

```text
Measure firmware
        ↓
Bind measurement to device identity
        ↓
Generate signed quote
        ↓
Verify quote in control plane
        ↓
Admit or quarantine node
```

Relevant domains include:

- Hardware root of trust
- Secure boot
- Firmware resiliency
- Attestation systems
- Fleet security automation
- Confidential computing
- Platform integrity verification
- Datacenter security

---

# Current Milestone

This project currently supports:

- Single-device attestation verification
- Fleet-level trust policy simulation
- Rollback detection
- Firmware validation
- Signature verification
- Hardware-backed and simulation-only trust modes

---

# Commands

Run single-device verification:

```bash
cd verifier
python3 verify_quote.py
```

Run fleet verification:

```bash
cd verifier
python3 fleet_verifier.py
```

If already inside the verifier directory, do NOT run:

```bash
python3 verifier/fleet_verifier.py
```

That path is incorrect because it searches for:

```text
verifier/verifier/fleet_verifier.py
```

Instead use:

```bash
python3 fleet_verifier.py
```

---

# Future Improvements

Planned future enhancements:

- Live serial communication with ESP32
- Public key export from ATECC608A
- JSON attestation quote format
- Device enrollment database
- CI verification tests
- Fleet dashboard visualization
- Policy configuration files
- Measured boot chain expansion
- TPM integration experiments

---

# Portfolio Summary

Built a hardware root of trust attestation lab using ESP32, ATECC608A, and Python-based verification tooling. The project demonstrates firmware measurement validation, signed attestation quotes, rollback protection, and fleet-level trust policy enforcement inspired by modern cloud infrastructure security systems.
