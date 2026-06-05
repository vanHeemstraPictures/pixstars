// Pololu Mini Maestro 24-channel servo controller driver.
//
// Speaks the Maestro "compact protocol" over a hardware UART (default
// 9600 baud, 8N1). Wraps the two commands used at runtime by the
// /servo/set and /servo/speed OSC handlers:
//
//   0x84  Set Target  - position in quarter-microseconds (14-bit)
//   0x87  Set Speed   - max speed in (0.25 us) / (10 ms), 0 = unlimited
//
// Channel map (matches wiring/WIRING.md cave servo stack):
//   Ch1  MG996R  lower arm
//   Ch2  MG996R  elbow
//   Ch3  MG90S   neck pan (carbon fibre push-pull rod)
//   Ch4  MG996R  spare
//   Ch5  MG996R  spare

#pragma once

#include <Arduino.h>

namespace maestro {

// Active channel range (1..MAESTRO_LAST_ACTIVE_CHANNEL). The Maestro
// itself accepts 0..23; we accept the full range but warn for any
// channel outside the active stage wiring.
static constexpr uint8_t MAESTRO_LAST_CHANNEL = 23;
static constexpr uint8_t MAESTRO_LAST_ACTIVE_CHANNEL = 5;

// Standard hobby servo pulse range in microseconds.
static constexpr uint16_t SERVO_MIN_US = 500;
static constexpr uint16_t SERVO_MAX_US = 2500;

// Initialise the Maestro UART. Returns true if the UART came up.
bool begin();

// Convert an angle in degrees [0..180] to quarter-microseconds in the
// 500..2500 us hobby-servo pulse range. Angles outside [0..180] are
// clamped.
uint16_t angleToQuarterUs(float angleDeg);

// Send a Set Target compact-protocol command (0x84). targetQuarterUs is
// the pulse width in quarter-microsecond units (so 6000 = 1500 us).
// Returns false if channel is out of range (0..23).
bool setTarget(uint8_t channel, uint16_t targetQuarterUs);

// Convenience wrapper: send a target derived from an angle in degrees.
bool setAngle(uint8_t channel, float angleDeg);

// Send a Set Speed compact-protocol command (0x87). speed is in
// (0.25 us) / (10 ms); 0 = unlimited.
bool setSpeed(uint8_t channel, uint16_t speed);

}  // namespace maestro
