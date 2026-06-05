// Stub implementations. Each subsystem task replaces the body of its
// handler with real hardware drive code. For now we log the address and
// the argument types so that wiring/routing can be verified end-to-end
// from the Mac Mini.

#include "handlers.h"

#include <Arduino.h>

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

namespace handlers {

void servo(OSCMessage &msg, int /*offset*/) { logMessage("servo", msg); }
void head(OSCMessage &msg, int /*offset*/) { logMessage("head", msg); }
void led(OSCMessage &msg, int /*offset*/) { logMessage("led", msg); }
void turntable(OSCMessage &msg, int /*offset*/) { logMessage("turntable", msg); }

}  // namespace handlers
