# fleet_verifier.py
# Simulates rack-level attestation decisions across multiple devices.

EXPECTED_MEASURE = "161061760"  # firmware_v2
MIN_ALLOWED_SVN = 2


def hash_str(s):
    h = 0
    for ch in s:
        h = h * 31 + ord(ch)
        h = ((h + 2**31) % 2**32) - 2**31
    return str(h)


def derive(parent, measurement):
    return hash_str(parent + "|" + measurement)


def simulate_device(node_id, firmware, svn, device_secret):
    firmware_measurement = hash_str(firmware)
    idev = derive(device_secret, firmware_measurement)

    config_measurement = hash_str("config_v1")
    ldev = derive(idev, config_measurement)

    runtime_measurement = hash_str("runtime_v1")
    runtime_id = derive(ldev, runtime_measurement)

    signature = hash_str(runtime_id + "|" + firmware_measurement + "|" + str(svn))

    return {
        "node_id": node_id,
        "firmware": firmware,
        "svn": svn,
        "measurement": firmware_measurement,
        "runtime_id": runtime_id,
        "signature": signature,
    }


def verify_device(device):
    expected_signature = hash_str(
        device["runtime_id"] + "|" + device["measurement"] + "|" + str(device["svn"])
    )

    if device["signature"] != expected_signature:
        return "INVALID_SIGNATURE"

    if device["svn"] < MIN_ALLOWED_SVN:
        return "ROLLBACK_DETECTED"

    if device["measurement"] != EXPECTED_MEASURE:
        return "UNTRUSTED_FIRMWARE"

    return "TRUSTED"


fleet = []

# 8 good nodes running firmware_v2
for i in range(1, 9):
    fleet.append(
        simulate_device(
            node_id=f"rack1-node{i:02d}",
            firmware="firmware_v2",
            svn=2,
            device_secret=f"device_secret_{i}",
        )
    )

# 1 rollback node: old firmware but still valid-looking
fleet.append(
    simulate_device(
        node_id="rack1-node09",
        firmware="firmware_v1",
        svn=1,
        device_secret="device_secret_9",
    )
)

# 1 compromised node
fleet.append(
    simulate_device(
        node_id="rack1-node10",
        firmware="firmware_hacked",
        svn=0,
        device_secret="device_secret_10",
    )
)


trusted = []
quarantined = []

print("=== Fleet Attestation Report ===\n")

for device in fleet:
    result = verify_device(device)

    print(f"Node:        {device['node_id']}")
    print(f"Firmware:    {device['firmware']}")
    print(f"SVN:         {device['svn']}")
    print(f"Measurement: {device['measurement']}")
    print(f"Decision:    {result}")
    print("-" * 40)

    if result == "TRUSTED":
        trusted.append(device["node_id"])
    else:
        quarantined.append(
            {
                "node_id": device["node_id"],
                "reason": result,
                "measurement": device["measurement"],
                "svn": device["svn"],
            }
        )

print("\n=== Fleet Summary ===")
print(f"Trusted nodes:     {len(trusted)}")
print(f"Quarantined nodes: {len(quarantined)}")

print("\nTrusted:")
for node in trusted:
    print(f"  ✅ {node}")

print("\nQuarantined:")
for node in quarantined:
    print(
        f"  ❌ {node['node_id']} | "
        f"Reason={node['reason']} | "
        f"SVN={node['svn']} | "
        f"Measurement={node['measurement']}"
    )
