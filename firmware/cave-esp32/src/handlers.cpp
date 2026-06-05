// Stub implementations. Each subsystem task replaces the body of its
// handler with real hardware drive code. For now we log the address and
// the argument types so that wiring/routing can be verified end-to-end
// from the Mac Mini.

#include "handlers.h"

#include <Arduino.h>

#include "maestro.h"

static void logMessage(const char *subsystem, OSCMessage &msg) {
  char address[64] = {0};
  msg.getAddress(address, 0, sizeof(address) - 1);

  Serial.printf("[%s] %s (%d args)\n", subsystem, address, msg.size());

  for (int i = 0; i < msg.size(); i++) {
    if (msg.isInt(i)) {
      Serial.printf("  arg %d: int    = %ld\n", i, (long)msg.getInt(i));
    } else if (msg.isFloat(i)) {
      Serial.printf("  arg %d: float  = %f\n", i, msg.getFloat(i));
    } else if (msg.isString(i)) {
      char buf[64] = {0};
      msg.getString(i, buf, sizeof(buf) - 1);
      Serial.printf("  arg %d: string = %s\n", i, buf);
    } else if (msg.isBoolean(i)) {
      Serial.printf("  arg %d: bool   = %d\n", i, msg.getBoolean(i));
    } else {
      Serial.printf("  arg %d: <other>\n", i);
    }
  }
}

// Extract argument `i` as a numeric value (accepts int or float). Returns
// `fallback` if the argument is missing or of an unsupported type and
// logs a warning.
static float argAsFloat(OSCMessage &msg, int i, float fallback) {
  if (i >= msg.size()) {
    Serial.printf("[servo] missing arg %d\n", i);
    return fallback;
  }
  if (msg.isInt(i)) return (float)msg.getInt(i);
  if (msg.isFloat(i)) return msg.getFloat(i);
  Serial.printf("[servo] arg %d has unsupported type\n", i);
  return fallback;
}

static void handleServoSet(OSCMessage &msg) {
  if (msg.size() < 2) {
    Serial.println("[servo] /servo/set needs (channel, angle)");
    return;
  }
  int32_t channel = (int32_t)argAsFloat(msg, 0, -1.0f);
  float angle = argAsFloat(msg, 1, 0.0f);
  if (channel < 0 || channel > 255) {
    Serial.printf("[servo] /servo/set: channel %ld out of byte range\n",
                  (long)channel);
    return;
  }
  Serial.printf("[servo] /servo/set ch=%ld angle=%.2f\n",
                (long)channel, angle);
  maestro::setAngle((uint8_t)channel, angle);
}

static void handleServoSpeed(OSCMessage &msg) {
  if (msg.size() < 2) {
    Serial.println("[servo] /servo/speed needs (channel, speed)");
    return;
  }
  int32_t channel = (int32_t)argAsFloat(msg, 0, -1.0f);
  int32_t speed = (int32_t)argAsFloat(msg, 1, 0.0f);
  if (channel < 0 || channel > 255) {
    Serial.printf("[servo] /servo/speed: channel %ld out of byte range\n",
                  (long)channel);
    return;
  }
  if (speed < 0 || speed > 0x3FFF) {
    Serial.printf("[servo] /servo/speed: speed %ld out of 14-bit range\n",
                  (long)speed);
    return;
  }
  Serial.printf("[servo] /servo/speed ch=%ld speed=%ld\n",
                (long)channel, (long)speed);
  maestro::setSpeed((uint8_t)channel, (uint16_t)speed);
}

namespace handlers {

void servo(OSCMessage &msg, int offset) {
  // route("/servo", ...) leaves the remainder of the address (e.g.
  // "/set") to be matched starting at `offset`.
  if (msg.dispatch("/set", handleServoSet, offset)) return;
  if (msg.dispatch("/speed", handleServoSpeed, offset)) return;
  logMessage("servo", msg);
}
void head(OSCMessage &msg, int /*offset*/) { logMessage("head", msg); }
void led(OSCMessage &msg, int /*offset*/) { logMessage("led", msg); }
void turntable(OSCMessage &msg, int /*offset*/) { logMessage("turntable", msg); }

}  // namespace handlers
