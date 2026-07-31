// Stub implementations. Each subsystem task replaces the body of its
// handler with real hardware drive code. For now we log the address and
// the argument types so that wiring/routing can be verified end-to-end
// from the Mac Mini.

#include "handlers.h"

#include <Arduino.h>

#include "dynamixel.h"
#include "leds.h"
#include "maestro.h"
#include "turntable.h"

#if __has_include("config.h")
#include "config.h"
#endif

#ifndef AX12_ID
#define AX12_ID 1
#endif

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
static void handleHeadNod(OSCMessage &msg) {
  if (msg.size() < 1) {
    Serial.println("[head] /head/nod needs (angleDeg[, speed])");
    return;
  }
  float angle = argAsFloat(msg, 0, 150.0f);
  int32_t speed = -1;
  if (msg.size() >= 2) {
    speed = (int32_t)argAsFloat(msg, 1, -1.0f);
    if (speed > 1023) speed = 1023;
    if (speed < 0) speed = -1;
  }
  Serial.printf("[head] /head/nod angle=%.2f speed=%ld\n",
                angle, (long)speed);
  dynamixel::setAngle((uint8_t)AX12_ID, angle, speed);
}

// Mirror one AX-12A read result to both Serial (HWCDC) and Serial0
// (UART0 bridge) so bench captures on either port see the same lines.
// `word` is the 16-bit value for two-byte registers or the 8-bit value
// widened to 16 bits for one-byte registers.
static void axReadLog(const char *name, bool ok, uint16_t word,
                      uint8_t err, uint8_t nBytes) {
  if (ok) {
    if (nBytes == 2) {
      Serial.printf("[DIAG] AX12_READ %s = %u (0x%04X) err=0x%02X ok=1\n",
                    name, (unsigned)word, (unsigned)word, (unsigned)err);
      Serial0.printf("[DIAG] AX12_READ %s = %u (0x%04X) err=0x%02X ok=1\r\n",
                     name, (unsigned)word, (unsigned)word, (unsigned)err);
    } else {
      Serial.printf("[DIAG] AX12_READ %s = %u (0x%02X) err=0x%02X ok=1\n",
                    name, (unsigned)word, (unsigned)word, (unsigned)err);
      Serial0.printf("[DIAG] AX12_READ %s = %u (0x%02X) err=0x%02X ok=1\r\n",
                     name, (unsigned)word, (unsigned)word, (unsigned)err);
    }
  } else {
    Serial.printf("[DIAG] AX12_READ %s = TIMEOUT/BAD_PACKET ok=0\n", name);
    Serial0.printf("[DIAG] AX12_READ %s = TIMEOUT/BAD_PACKET ok=0\r\n", name);
  }
}

// Bench-only: query AX-12A servo state to separate mechanical bind vs
// EEPROM wheel-mode vs supply sag vs latched status error. Reads (in
// order): CW Angle Limit, CCW Angle Limit, Present Position, Present
// Load, Present Voltage, Present Temperature. Each result and its
// status-error byte are mirrored to Serial0 for the USB-UART bridge.
static void handleHeadRead(OSCMessage & /*msg*/) {
  Serial.printf("[DIAG] AX12_READ START id=%u\n", (unsigned)AX12_ID);
  Serial0.printf("[DIAG] AX12_READ START id=%u\r\n", (unsigned)AX12_ID);

  uint16_t w = 0;
  uint8_t  b = 0;
  uint8_t  err = 0;
  bool ok;

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_CW_ANGLE_LIMIT, 2,
                           reinterpret_cast<uint8_t *>(&w), &err);
  axReadLog("CW_ANGLE_LIMIT", ok, w, err, 2);

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_CCW_ANGLE_LIMIT, 2,
                           reinterpret_cast<uint8_t *>(&w), &err);
  axReadLog("CCW_ANGLE_LIMIT", ok, w, err, 2);

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_PRESENT_POSITION, 2,
                           reinterpret_cast<uint8_t *>(&w), &err);
  axReadLog("PRESENT_POSITION", ok, w, err, 2);

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_PRESENT_LOAD, 2,
                           reinterpret_cast<uint8_t *>(&w), &err);
  axReadLog("PRESENT_LOAD", ok, w, err, 2);

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_PRESENT_VOLTAGE, 1,
                           &b, &err);
  axReadLog("PRESENT_VOLTAGE", ok, (uint16_t)b, err, 1);

  err = 0;
  ok = dynamixel::readData((uint8_t)AX12_ID,
                           dynamixel::AX12_REG_PRESENT_TEMP, 1,
                           &b, &err);
  axReadLog("PRESENT_TEMPERATURE", ok, (uint16_t)b, err, 1);

  Serial.println("[DIAG] AX12_READ END");
  Serial0.println("[DIAG] AX12_READ END");
}

void head(OSCMessage &msg, int offset) {
  if (msg.dispatch("/nod",  handleHeadNod,  offset)) return;
  if (msg.dispatch("/read", handleHeadRead, offset)) return;
  logMessage("head", msg);
}
// Apply (r, g, b, mode) from an OSC message to a single ring. Channels
// accepted as ints or floats and clamped to 0..255; mode is a trailing
// string ("off", "solid", "breathe", "pulse", "rainbow").
static void applyLedMessage(const char *which, OSCMessage &msg,
                            void (*setFn)(uint8_t, uint8_t, uint8_t, leds::Mode)) {
  if (msg.size() < 4) {
    Serial.printf("[led] /led/%s needs (r, g, b, mode)\n", which);
    return;
  }
  int32_t r = (int32_t)argAsFloat(msg, 0, 0.0f);
  int32_t g = (int32_t)argAsFloat(msg, 1, 0.0f);
  int32_t b = (int32_t)argAsFloat(msg, 2, 0.0f);
  if (r < 0) r = 0; if (r > 255) r = 255;
  if (g < 0) g = 0; if (g > 255) g = 255;
  if (b < 0) b = 0; if (b > 255) b = 255;
  char modeName[16] = {0};
  if (msg.isString(3)) {
    msg.getString(3, modeName, sizeof(modeName) - 1);
  } else {
    Serial.printf("[led] /led/%s: mode (arg 3) must be a string\n", which);
    return;
  }
  setFn((uint8_t)r, (uint8_t)g, (uint8_t)b, leds::parseMode(modeName));
}

static void handleLedRear(OSCMessage &msg)  { applyLedMessage("rear",  msg, leds::setRear); }
static void handleLedFront(OSCMessage &msg) { applyLedMessage("front", msg, leds::setFront); }

void led(OSCMessage &msg, int offset) {
  if (msg.dispatch("/rear",  handleLedRear,  offset)) return;
  if (msg.dispatch("/front", handleLedFront, offset)) return;
  logMessage("led", msg);
}
static void handleTurntableRotate(OSCMessage &msg) {
  if (msg.size() < 1) {
    Serial.println("[turntable] /turntable/rotate needs (degrees[, speedDps])");
    return;
  }
  float degrees = argAsFloat(msg, 0, 0.0f);
  float speed   = msg.size() >= 2 ? argAsFloat(msg, 1, 0.0f) : 0.0f;
  ::turntable::rotate(degrees, speed);
}

static void handleTurntableGoto(OSCMessage &msg) {
  if (msg.size() < 1) {
    Serial.println("[turntable] /turntable/goto needs (degreesAbs[, speedDps])");
    return;
  }
  float degrees = argAsFloat(msg, 0, 0.0f);
  float speed   = msg.size() >= 2 ? argAsFloat(msg, 1, 0.0f) : 0.0f;
  ::turntable::gotoAbs(degrees, speed);
}

static void handleTurntableOrigin(OSCMessage & /*msg*/) {
  ::turntable::originSeek();
}

static void handleTurntableStop(OSCMessage & /*msg*/) {
  ::turntable::stop();
}

void turntable(OSCMessage &msg, int offset) {
  if (msg.dispatch("/rotate", handleTurntableRotate, offset)) return;
  if (msg.dispatch("/goto",   handleTurntableGoto,   offset)) return;
  if (msg.dispatch("/origin", handleTurntableOrigin, offset)) return;
  if (msg.dispatch("/stop",   handleTurntableStop,   offset)) return;
  logMessage("turntable", msg);
}

}  // namespace handlers
