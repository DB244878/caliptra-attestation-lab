import serial
import time
import sys

PORT = "/dev/cu.usbmodem1101"
BAUD = 9600

# Known-good firmware measurement for firmware_v1
EXPECTED_MEASURE = "161061759"

ser = serial.Serial(PORT, BAUD)
time.sleep(2)


def flush_serial():
    ser.reset_input_buffer()


def hash_str(s):
    h = 0
    for ch in s:
        h = h * 31 + ord(ch)
        # simulate Arduino 32-bit signed long overflow
        h = ((h + 2**31) % 2**32) - 2**31
    return str(h)


def read_lines(expected_prefixes, timeout=2):
    start = time.time()
    results = []

    while time.time() - start < timeout:
        if ser.in_waiting:
            line = ser.readline().decode(errors="replace").strip()
            print("DEBUG:", line)

            for prefix in expected_prefixes:
                if line.startswith(prefix):
                    results.append(line)

        if len(results) == len(expected_prefixes):
            break

    return results


def send(cmd):
    flush_serial()
    ser.write((cmd + "\n").encode())
    time.sleep(0.2)

    if cmd == "get_ids":
        return read_lines(["IDEV=", "LDEV=", "RT="])
    elif cmd == "attest":
        return read_lines(["MEASURE=", "SIG="])
    else:
        return []


# Step 1: get DICE identity chain
ids = send("get_ids")

if len(ids) < 3:
    print("❌ Failed to read IDs properly")
    sys.exit(1)

for line in ids:
    print(line)

runtime_id = ids[2].split("=")[1]


# Step 2: get attestation quote
att = send("attest")

if len(att) < 2:
    print("❌ Failed to read attestation")
    sys.exit(1)

measurement = att[0].split("=")[1]
signature = att[1].split("=")[1]

print("\nVerifying...")

# Step 3: verify signature
expected_signature = hash_str(runtime_id + "|" + measurement)

if signature != expected_signature:
    print("❌ INVALID SIGNATURE")
    sys.exit(1)

print("✅ Signature valid")

# Step 4: verify firmware policy
if measurement != EXPECTED_MEASURE:
    print("❌ UNTRUSTED FIRMWARE")
    print(f"Expected measurement: {EXPECTED_MEASURE}")
    print(f"Actual measurement:   {measurement}")
    sys.exit(1)

print("✅ TRUSTED DEVICE + TRUSTED FIRMWARE")