// Pololu Mini Maestro compact-protocol driver. See maestro.h.

#include "maestro.h"

#if __has_include("config.h")
#include "config.h"
#endif

// Defaults. Override in config.h / config.h.example.
#ifndef MAESTRO_UART_NUM
#define MAESTRO_UART_NUM 1   // Use Serial1 (UART1)
#endif
#ifndef MAESTRO_TX_PIN
#define MAESTRO_TX_PIN   17  // ESP32-S3 TX1 -> Maestro RX
#endif
#ifndef MAESTRO_RX_PIN
#define MAESTRO_RX_PIN   18  // ESP32-S3 RX1 <- Maestro TX (optional feedback)
#endif
#ifndef MAESTRO_BAUD
#define MAESTRO_BAUD     9600
#endif

// Pick the HardwareSerial instance at compile time.
#if MAESTRO_UART_NUM == 1
#define MAESTRO_SERIAL Serial1
#elif MAESTRO_UART_NUM == 2
#define MAESTRO_SERIAL Serial2
#else
#error "MAESTRO_UART_NUM must be 1 or 2"
#endif

namespace maestro {

bool begin() {
  MAESTRO_SERIAL.begin(MAESTRO_BAUD, SERIAL_8N1, MAESTRO_RX_PIN, MAESTRO_TX_PIN);
  Serial.printf("[maestro] UART%d @ %d baud (TX=%d RX=%d)\n",
                MAESTRO_UART_NUM, MAESTRO_BAUD, MAESTRO_TX_PIN, MAESTRO_RX_PIN);
  return true;
}

uint16_t angleToQuarterUs(float angleDeg) {
  if (angleDeg < 0.0f) angleDeg = 0.0f;
  if (angleDeg > 180.0f) angleDeg = 180.0f;
  // us = 500 + (angle / 180) * 2000
  float us = (float)SERVO_MIN_US +
             (angleDeg / 180.0f) * (float)(SERVO_MAX_US - SERVO_MIN_US);
  return (uint16_t)(us * 4.0f + 0.5f);
}

static bool checkChannel(uint8_t channel, const char *what) {
  if (channel > MAESTRO_LAST_CHANNEL) {
    Serial.printf("[maestro] %s: channel %u out of range (0..%u)\n",
                  what, (unsigned)channel, (unsigned)MAESTRO_LAST_CHANNEL);
    return false;
  }
  if (channel < 1 || channel > MAESTRO_LAST_ACTIVE_CHANNEL) {
    Serial.printf("[maestro] %s: channel %u outside active range 1..%u (allowed but unwired)\n",
                  what, (unsigned)channel, (unsigned)MAESTRO_LAST_ACTIVE_CHANNEL);
  }
  return true;
}

bool setTarget(uint8_t channel, uint16_t targetQuarterUs) {
  if (!checkChannel(channel, "setTarget")) return false;
  // Compact protocol: 0x84, channel, target_low_7, target_high_7
  uint8_t buf[4] = {
      0x84,
      channel,
      (uint8_t)(targetQuarterUs & 0x7F),
      (uint8_t)((targetQuarterUs >> 7) & 0x7F),
  };
  MAESTRO_SERIAL.write(buf, sizeof(buf));
  return true;
}

bool setAngle(uint8_t channel, float angleDeg) {
  return setTarget(channel, angleToQuarterUs(angleDeg));
}

bool setSpeed(uint8_t channel, uint16_t speed) {
  if (!checkChannel(channel, "setSpeed")) return false;
  // Compact protocol: 0x87, channel, speed_low_7, speed_high_7
  uint8_t buf[4] = {
      0x87,
      channel,
      (uint8_t)(speed & 0x7F),
      (uint8_t)((speed >> 7) & 0x7F),
  };
  MAESTRO_SERIAL.write(buf, sizeof(buf));
  return true;
}

}  // namespace maestro
