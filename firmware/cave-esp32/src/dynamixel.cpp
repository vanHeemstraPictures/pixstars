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

}  // namespace dynamixel
