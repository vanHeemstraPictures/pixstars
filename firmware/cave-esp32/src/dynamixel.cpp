// Dynamixel AX-12A Protocol 1.0 driver. See dynamixel.h.

#include "dynamixel.h"

#if __has_include("config.h")
#include "config.h"
#endif

// Defaults. Override in config.h / config.h.example.
#ifndef AX12_UART_NUM
#define AX12_UART_NUM 2    // Use Serial2 (UART2)
#endif
#ifndef AX12_TX_PIN
#define AX12_TX_PIN   15   // ESP32-S3 TX2 -> AX-12A data line (via buffer)
#endif
#ifndef AX12_RX_PIN
#define AX12_RX_PIN   16   // ESP32-S3 RX2 <- AX-12A data line (via buffer)
#endif
#ifndef AX12_DIR_PIN
#define AX12_DIR_PIN  8    // TX_EN / half-duplex direction control
#endif
#ifndef AX12_BAUD
#define AX12_BAUD     1000000  // AX-12A factory default 1 Mbps
#endif
#ifndef AX12_ID
#define AX12_ID       1    // Default unicast ID for the head nod servo
#endif

// Pick the HardwareSerial instance at compile time.
#if AX12_UART_NUM == 1
#define AX12_SERIAL Serial1
#elif AX12_UART_NUM == 2
#define AX12_SERIAL Serial2
#else
#error "AX12_UART_NUM must be 1 or 2"
#endif

// Protocol 1.0 constants.
static constexpr uint8_t AX12_HEADER             = 0xFF;
static constexpr uint8_t AX12_INSTR_WRITE_DATA   = 0x03;
static constexpr uint8_t AX12_INSTR_READ_DATA    = 0x02;
static constexpr uint8_t AX12_REG_GOAL_POSITION  = 0x1E;
static constexpr uint8_t AX12_REG_MOVING_SPEED   = 0x20;
static constexpr uint8_t AX12_ID_MAX             = 0xFD;  // 254 (0xFE = broadcast)

namespace dynamixel {

bool begin() {
  pinMode(AX12_DIR_PIN, OUTPUT);
  digitalWrite(AX12_DIR_PIN, LOW);  // RX (idle)
  AX12_SERIAL.begin(AX12_BAUD, SERIAL_8N1, AX12_RX_PIN, AX12_TX_PIN);
  Serial.printf("[ax12] UART%d @ %d baud (TX=%d RX=%d DIR=%d) default ID=%d\n",
                AX12_UART_NUM, AX12_BAUD, AX12_TX_PIN, AX12_RX_PIN,
                AX12_DIR_PIN, AX12_ID);
  return true;
}

uint16_t angleToPosition(float angleDeg) {
  if (angleDeg < 0.0f) angleDeg = 0.0f;
  if (angleDeg > AX12_ANGLE_MAX_DEG) angleDeg = AX12_ANGLE_MAX_DEG;
  float pos = (angleDeg / AX12_ANGLE_MAX_DEG) * (float)AX12_POSITION_MAX;
  return (uint16_t)(pos + 0.5f);
}

// Build and send a Protocol 1.0 WRITE_DATA packet:
//   0xFF 0xFF ID LEN 0x03 ADDR PARAM[0..n-1] CHECKSUM
// LEN = nParams + 3 (instr + addr + checksum body); see AX-12A manual.
// Returns false on invalid ID.
static bool writePacket(uint8_t id, uint8_t reg,
                        const uint8_t *params, uint8_t nParams) {
  if (id > AX12_ID_MAX) {
    Serial.printf("[ax12] writePacket: id %u out of range (0..%u)\n",
                  (unsigned)id, (unsigned)AX12_ID_MAX);
    return false;
  }
  // Packet length field per Protocol 1.0:
  //   length = (number of parameters) + 2
  // where the "parameters" of WRITE_DATA are: ADDR + DATA bytes.
  uint8_t length = (uint8_t)(nParams + 1 + 2);  // +1 addr, +2 instr+checksum
  uint8_t buf[16];
  uint8_t i = 0;
  buf[i++] = AX12_HEADER;
  buf[i++] = AX12_HEADER;
  buf[i++] = id;
  buf[i++] = length;
  buf[i++] = AX12_INSTR_WRITE_DATA;
  buf[i++] = reg;
  for (uint8_t k = 0; k < nParams; k++) buf[i++] = params[k];

  // Checksum over ID, LENGTH, INSTRUCTION, and all parameters (incl. ADDR).
  uint16_t sum = 0;
  for (uint8_t k = 2; k < i; k++) sum += buf[k];
  buf[i++] = (uint8_t)(~sum & 0xFF);

  // Half-duplex: assert TX, send, flush, release.
  digitalWrite(AX12_DIR_PIN, HIGH);
  AX12_SERIAL.write(buf, i);
  AX12_SERIAL.flush();
  digitalWrite(AX12_DIR_PIN, LOW);
  return true;
}

bool setGoalPosition(uint8_t id, uint16_t position, int32_t speed) {
  if (position > AX12_POSITION_MAX) position = AX12_POSITION_MAX;
  if (speed >= 0) {
    if (speed > AX12_SPEED_MAX) speed = AX12_SPEED_MAX;
    uint8_t params[4] = {
        (uint8_t)(position & 0xFF),
        (uint8_t)((position >> 8) & 0xFF),
        (uint8_t)(speed & 0xFF),
        (uint8_t)((speed >> 8) & 0xFF),
    };
    return writePacket(id, AX12_REG_GOAL_POSITION, params, 4);
  }
  uint8_t params[2] = {
      (uint8_t)(position & 0xFF),
      (uint8_t)((position >> 8) & 0xFF),
  };
  return writePacket(id, AX12_REG_GOAL_POSITION, params, 2);
}

bool setAngle(uint8_t id, float angleDeg, int32_t speed) {
  return setGoalPosition(id, angleToPosition(angleDeg), speed);
}

bool setSpeed(uint8_t id, uint16_t speed) {
  if (speed > AX12_SPEED_MAX) speed = AX12_SPEED_MAX;
  uint8_t params[2] = {
      (uint8_t)(speed & 0xFF),
      (uint8_t)((speed >> 8) & 0xFF),
  };
  return writePacket(id, AX12_REG_MOVING_SPEED, params, 2);
}

// Read one byte from the AX-12A UART with a deadline. Returns -1 on
// timeout. Kept local to avoid touching the shared write path.
static int readByteUntil(uint32_t deadlineMs) {
  while ((int32_t)(deadlineMs - millis()) > 0) {
    int b = AX12_SERIAL.read();
    if (b >= 0) return b;
    // Small yield to keep WiFi / other tasks responsive at 1 Mbps.
    delayMicroseconds(50);
  }
  return -1;
}

bool readData(uint8_t id, uint8_t reg, uint8_t nBytes,
              uint8_t *out, uint8_t *outError, uint32_t timeoutMs) {
  if (id > AX12_ID_MAX) {
    Serial.printf("[ax12] readData: id %u out of range (0..%u)\n",
                  (unsigned)id, (unsigned)AX12_ID_MAX);
    return false;
  }
  if (out == nullptr || nBytes == 0) return false;

  // Request packet: 0xFF 0xFF ID LEN 0x02 ADDR NBYTES CHECKSUM
  //   length field = nParams + 2 = 2 + 2 = 4
  uint8_t buf[8];
  uint8_t i = 0;
  buf[i++] = AX12_HEADER;
  buf[i++] = AX12_HEADER;
  buf[i++] = id;
  buf[i++] = 4;                       // length
  buf[i++] = AX12_INSTR_READ_DATA;
  buf[i++] = reg;
  buf[i++] = nBytes;
  uint16_t sum = 0;
  for (uint8_t k = 2; k < i; k++) sum += buf[k];
  buf[i++] = (uint8_t)(~sum & 0xFF);

  // Drain any stale bytes so we align on the reply's header.
  while (AX12_SERIAL.available()) (void)AX12_SERIAL.read();

  // Half-duplex send, then release the bus for the servo to reply.
  digitalWrite(AX12_DIR_PIN, HIGH);
  AX12_SERIAL.write(buf, i);
  AX12_SERIAL.flush();
  digitalWrite(AX12_DIR_PIN, LOW);

  // Expected status packet:
  //   0xFF 0xFF ID LEN ERROR PARAM[0..nBytes-1] CHECKSUM
  //   length field = nBytes + 2
  const uint32_t deadline = millis() + timeoutMs;
  int b;

  // Sync on two consecutive 0xFF header bytes.
  uint8_t headerSeen = 0;
  while (headerSeen < 2) {
    b = readByteUntil(deadline);
    if (b < 0) return false;
    headerSeen = (b == AX12_HEADER) ? (uint8_t)(headerSeen + 1) : 0;
  }

  int rxId  = readByteUntil(deadline); if (rxId  < 0) return false;
  int rxLen = readByteUntil(deadline); if (rxLen < 0) return false;
  int rxErr = readByteUntil(deadline); if (rxErr < 0) return false;

  if ((uint8_t)rxId != id) return false;
  if ((uint8_t)rxLen != (uint8_t)(nBytes + 2)) return false;

  uint16_t chk = (uint16_t)rxId + (uint16_t)rxLen + (uint16_t)rxErr;
  for (uint8_t k = 0; k < nBytes; k++) {
    int p = readByteUntil(deadline);
    if (p < 0) return false;
    out[k] = (uint8_t)p;
    chk += (uint8_t)p;
  }
  int rxChk = readByteUntil(deadline);
  if (rxChk < 0) return false;
  if ((uint8_t)rxChk != (uint8_t)(~chk & 0xFF)) return false;

  if (outError) *outError = (uint8_t)rxErr;
  return true;
}

static bool readWordAt(uint8_t id, uint8_t reg, uint16_t *out) {
  if (!out) return false;
  uint8_t b[2] = {0, 0};
  if (!readData(id, reg, 2, b)) return false;
  *out = (uint16_t)b[0] | ((uint16_t)b[1] << 8);
  return true;
}

bool readCwAngleLimit(uint8_t id, uint16_t *outLimit) {
  return readWordAt(id, AX12_REG_CW_ANGLE_LIMIT, outLimit);
}

bool readCcwAngleLimit(uint8_t id, uint16_t *outLimit) {
  return readWordAt(id, AX12_REG_CCW_ANGLE_LIMIT, outLimit);
}

bool readPresentPosition(uint8_t id, uint16_t *outPosition) {
  return readWordAt(id, AX12_REG_PRESENT_POSITION, outPosition);
}

bool readPresentLoad(uint8_t id, uint16_t *outLoad) {
  return readWordAt(id, AX12_REG_PRESENT_LOAD, outLoad);
}

bool readPresentVoltage(uint8_t id, uint8_t *outVoltageTenthsV) {
  if (!outVoltageTenthsV) return false;
  return readData(id, AX12_REG_PRESENT_VOLTAGE, 1, outVoltageTenthsV);
}

bool readPresentTemperature(uint8_t id, uint8_t *outTemperatureC) {
  if (!outTemperatureC) return false;
  return readData(id, AX12_REG_PRESENT_TEMP, 1, outTemperatureC);
}

}  // namespace dynamixel
