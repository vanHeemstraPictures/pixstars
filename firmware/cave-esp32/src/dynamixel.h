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
//   0x1E (30)  Goal Position L
//   0x1F (31)  Goal Position H
//   0x20 (32)  Moving Speed L
//   0x21 (33)  Moving Speed H

#pragma once

#include <Arduino.h>

namespace dynamixel {

// AX-12A position range: 0..1023 maps to 0..300 degrees.
static constexpr uint16_t AX12_POSITION_MAX = 1023;
static constexpr float    AX12_ANGLE_MAX_DEG = 300.0f;

// AX-12A moving speed range: 0..1023. In joint mode, 0 means "maximum
// no-speed-control" (move as fast as possible).
static constexpr uint16_t AX12_SPEED_MAX = 1023;

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

}  // namespace dynamixel
