#include <Wire.h>
#include <ArduinoECCX08.h>

void printHex(const byte *data, int len) {
  for (int i = 0; i < len; i++) {
    if (data[i] < 16) Serial.print("0");
    Serial.print(data[i], HEX);
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("=== Mini Caliptra Hardware Attestation ===");

  Wire.begin(21, 22);

  if (!ECCX08.begin()) {
    Serial.println("FAILED: ATECC608A not detected");
    while (1);
  }

  Serial.println("ATECC608A detected");

  byte publicKey[64];

  if (!ECCX08.generatePublicKey(0, publicKey)) {
    Serial.println("FAILED: could not read public key");
    while (1);
  }

  const char *message = "firmware_v1|config_v1|challenge_123";

  byte digest[32];
  byte signature[64];

  if (!ECCX08.beginSHA256()) {
    Serial.println("FAILED: SHA256 begin");
    while (1);
  }

  if (!ECCX08.endSHA256((const byte *)message, strlen(message), digest)) {
    Serial.println("FAILED: SHA256 digest");
    while (1);
  }

  if (!ECCX08.ecSign(0, digest, signature)) {
    Serial.println("FAILED: hardware signing");
    while (1);
  }

  Serial.println("MESSAGE:");
  Serial.println(message);

  Serial.println("DIGEST:");
  printHex(digest, 32);

  Serial.println("PUBLIC_KEY:");
  printHex(publicKey, 64);

  Serial.println("SIGNATURE:");
  printHex(signature, 64);

  Serial.println("SUCCESS: hardware-backed attestation quote generated");
}

void loop() {
}
