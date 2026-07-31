// Dynamixel AX-12A driver (Protocol 1.0) for the lamp head nod servo.
//
// Speaks Dynamixel Protocol 1.0 over a hardware UART in half-duplex TTL
// mode. The AX-12A shares a single data line for TX and RX; a GPIO
// direction pin (AX12_DIR_PIN) gates the TX buffer:
//   HIGH -> TX enabled (we write)
//   LOW  -> RX enabled (servo replies)
//
// The /head/nod OSC handler calls setAngle(angle, speed) where
//   angle in degrees [0..300]  -> Goal Position [0..1023]
//   speed in raw units [0..1023], -1 = don't change current Moving Speed
//
// AX-12A control table addresses used here:
//   0x06 ( 6)  CW Angle Limit L         (EEPROM)
//   0x07 ( 7)  CW Angle Limit H         (EEPROM)
//   0x08 ( 8)  CCW Angle Limit L        (EEPROM)
//   0x09 ( 9)  CCW Angle Limit H        (EEPROM)
//   0x1E (30)  Goal Position L
//   0x1F (31)  Goal Position H
//   0x20 (32)  Moving Speed L
//   0x21 (33)  Moving Speed H
//   0x24 (36)  Present Position L
//   0x25 (37)  Present Position H
//   0x28 (40)  Present Load L
//   0x29 (41)  Present Load H
//   0x2A (42)  Present Voltage          (0.1 V units)
//   0x2B (43)  Present Temperature      (degrees C)

#pragma once

#include <Arduino.h>

namespace dynamixel {

// AX-12A position range: 0..1023 maps to 0..300 degrees.
static constexpr uint16_t AX12_POSITION_MAX = 1023;
static constexpr float    AX12_ANGLE_MAX_DEG = 300.0f;

// AX-12A moving speed range: 0..1023. In joint mode, 0 means "maximum
// no-speed-control" (move as fast as possible).
static constexpr uint16_t AX12_SPEED_MAX = 1023;

// AX-12A control table addresses exposed for read-path diagnostics.
static constexpr uint8_t AX12_REG_CW_ANGLE_LIMIT   = 0x06;  // 2 bytes
static constexpr uint8_t AX12_REG_CCW_ANGLE_LIMIT  = 0x08;  // 2 bytes
static constexpr uint8_t AX12_REG_PRESENT_POSITION = 0x24;  // 2 bytes
static constexpr uint8_t AX12_REG_PRESENT_LOAD     = 0x28;  // 2 bytes
static constexpr uint8_t AX12_REG_PRESENT_VOLTAGE  = 0x2A;  // 1 byte
static constexpr uint8_t AX12_REG_PRESENT_TEMP     = 0x2B;  // 1 byte

// Initialise the UART and direction pin. Returns true on success.
bool begin();

// Convert an angle in degrees [0..300] to raw position [0..1023].
// Out-of-range angles are clamped.
uint16_t angleToPosition(float angleDeg);

// Write Goal Position (and optionally Moving Speed) to the AX-12A.
// If speed >= 0 the Moving Speed registers are written in the same
// packet (4-byte WRITE_DATA at 0x1E). If speed < 0 only the 2-byte
// Goal Position is written.
// Returns false if id is out of the Protocol 1.0 unicast range.
bool setGoalPosition(uint8_t id, uint16_t position, int32_t speed = -1);

// Convenience wrapper: degrees in, raw position computed internally.
bool setAngle(uint8_t id, float angleDeg, int32_t speed = -1);

// Send a Moving Speed write on its own (2-byte WRITE_DATA at 0x20).
bool setSpeed(uint8_t id, uint16_t speed);

// ---- Protocol 1.0 READ_DATA (instruction 0x02) ------------------------
//
// Send a READ_DATA request and copy nBytes of the reply payload into out.
// Returns true only on a fully valid status packet (header, id, length,
// zero error byte, matching checksum). timeoutMs bounds the whole
// exchange; 20 ms is comfortable at 1 Mbps with default 250 us return
// delay. The status packet's error byte is optionally returned via
// outError (unchanged on failure).
bool readData(uint8_t id, uint8_t reg, uint8_t nBytes,
              uint8_t *out, uint8_t *outError = nullptr,
              uint32_t timeoutMs = 20);

// Typed convenience readers for the registers the bench needs to
// separate ranked failure causes (angle limits / position / load /
// voltage / temperature). All return true on a valid status packet.
bool readCwAngleLimit(uint8_t id, uint16_t *outLimit);
bool readCcwAngleLimit(uint8_t id, uint16_t *outLimit);
bool readPresentPosition(uint8_t id, uint16_t *outPosition);
bool readPresentLoad(uint8_t id, uint16_t *outLoad);
bool readPresentVoltage(uint8_t id, uint8_t *outVoltageTenthsV);
bool readPresentTemperature(uint8_t id, uint8_t *outTemperatureC);

}  // namespace dynamixel
