// Subsystem handler stubs. Each task that implements a subsystem
// (Maestro servos, AX-12A head nod, WS2812 LED ring, TMC2209 turntable)
// fills in the matching handler in handlers.cpp.
//
// All handlers receive the OSC message that was dispatched to them.

#pragma once

#include <OSCMessage.h>

namespace handlers {

// The `offset` argument is the number of characters in the address that
// matched the route prefix (passed by OSCMessage::route()).
void servo(OSCMessage &msg, int offset);      // /servo/...
void head(OSCMessage &msg, int offset);       // /head/...
void led(OSCMessage &msg, int offset);        // /led/...
void turntable(OSCMessage &msg, int offset);  // /turntable/...

}  // namespace handlers
