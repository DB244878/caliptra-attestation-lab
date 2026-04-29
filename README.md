# Caliptra-Inspired Hardware Attestation Lab

## Overview

This project implements a minimal, end-to-end **reference model** of a hardware-rooted attestation system, inspired by modern cloud infrastructure security architectures such as Caliptra, AWS Nitro, and Azure attestation services.

The objective is to understand how a device proves its runtime state, and how a cloud control plane evaluates that state to make trust decisions.

---

## System Architecture

### Architecture Overview

```text
+---------------------------+        +-----------------------------+
| Device (Root of Trust)    |        | Cloud Verifier              |
|---------------------------|        |-----------------------------|
| ROM Boot                  |        | Signature Verification      |
| DICE Identity Chain       | -----> | Policy Engine               |
| Firmware Measurement      |        | Allow / Deny Decision       |
| Attestation (Sign)        |        |                             |
+---------------------------+        +-----------------------------+

        Attestation Evidence (MEASURE + SIGNATURE)
```

---

The system consists of two logical components:

### 1. Device (Simulated Root of Trust)

Implemented on an Arduino Mega 2560.

The device models:

* ROM-style boot initialization
* DICE-style identity derivation across stages
* Firmware measurement
* Attestation generation (measurement + signature)
* Mailbox-style command interface

---

### 2. Verifier (Cloud Control Plane)

Implemented in Python on macOS.

The verifier models:

* Attestation request/response flow
* Signature validation
* Firmware policy enforcement
* Trust decision (allow / deny)

---

## End-to-End Flow

```text
Device Boot:
  ROM-style boot
    -> Firmware measurement
    -> DICE-style identity derivation
    -> Attestation generation

Verifier:
  Request attestation
    -> Validate signature
    -> Compare measurement to approved baseline
    -> Apply policy
    -> Allow / Deny decision
```

---

## Fleet-Level Simulation

In addition to single-device verification, this project includes a fleet-level simulation:

```bash
python3 verifier/fleet_verifier.py
```

The simulation models a rack with 10 nodes:

* 9 nodes running approved firmware
* 1 node running unapproved firmware

The verifier evaluates each node independently and produces a fleet summary:

* Trusted nodes remain eligible for workloads
* Untrusted nodes are quarantined

This reflects real-world cloud behavior where:

> Trust is evaluated per node, but decisions are applied at fleet level.

---

## Key Concepts Modeled

### Root of Trust (RoT)

A foundational secret (`deviceSecret`) anchors identity and measurement.

---

### DICE-Style Identity Chain

Identity evolves across stages:

```text
IDEV -> LDEV -> Runtime Identity
```

Each stage derives identity from:

* Previous identity
* Measured state

---

### Firmware Measurement

Firmware state is represented as a deterministic hash:

```text
MEASURE = hash(firmware)
```

This simulates real-world measurements such as BIOS, BMC, or OS state.

---

### Attestation

The device produces:

```text
MEASURE + SIGNATURE
```

Where:

* `MEASURE` = firmware state
* `SIGNATURE` = proof of authenticity (simulated)

---

### Verifier Policy

The verifier enforces an approved firmware baseline.

Decision logic:

```text
if signature valid AND measurement approved:
    TRUSTED
else:
    UNTRUSTED
```

---

## Critical Insight

Attestation answers: “What is this device running?”
Policy answers: “Is that acceptable?”

These are intentionally separate responsibilities:

* The device provides evidence
* The cloud enforces trust

---

## Implementation Details

### Device

* Platform: Arduino Mega 2560
* Language: C++ (Arduino)
* Communication: Serial (USB)
* Crypto: Simulated hash and signature logic

### Verifier

* Platform: macOS
* Language: Python
* Interface: Serial (pyserial)
* Functions:

  * Request identity and attestation
  * Validate signature
  * Enforce firmware policy

---

## Mapping to Real Systems

| Lab Component | Real System Equivalent                      |
| ------------- | ------------------------------------------- |
| Arduino       | Server / platform firmware environment      |
| deviceSecret  | Hardware root key (UDS / fuses / key vault) |
| boot_rom()    | Immutable ROM boot                          |
| derive()      | DICE / CDI derivation                       |
| hashStr()     | SHA engine                                  |
| Serial        | RPC / network / mailbox interface           |
| verifier.py   | Cloud attestation service                   |
| Policy check  | Security baseline enforcement               |

---

## Current Limitations

* Root key is software-based (not hardware-protected)
* Cryptographic primitives are simplified
* Serial interface instead of network API
* No rollback / version enforcement yet

---

## Next Steps

* Integrate ATECC608A secure element for hardware-backed key storage
* Replace simulated signature with real ECC signing
* Implement rollback protection (SVN / version enforcement)
* Extend to multi-node / rack-level trust decisions (real devices)
* Replace serial communication with network-based API

---

## Why This Matters

Modern cloud infrastructure relies on hardware-rooted trust to ensure that only verified systems run workloads.

This project demonstrates the fundamental separation between:

* Device-side evidence generation (attestation)
* Cloud-side trust decisions (policy enforcement)

At scale, these decisions are made continuously across thousands of nodes, making this separation critical to reliable and secure cloud operation.
