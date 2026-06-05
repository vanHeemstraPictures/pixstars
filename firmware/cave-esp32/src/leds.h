// WS2812 LED ring driver for the lamp head.
//
// Drives two independent rings via the ESP32 RMT peripheral (FastLED
// backend on the Arduino-ESP32 core selects RMT automatically for
// WS2812 strips on the S3):
//
//   rear  : 16 x WS2812 5050  on LED_RING_REAR_PIN
//   front : 35 x WS2812B      on LED_RING_FRONT_PIN
//
// Both rings have an independent base colour and animation mode. The
// animation engine is non-blocking and millis()-driven; call update()
// every loop iteration. A configurable global brightness cap
// (LED_MAX_BRIGHTNESS, 0..255) protects the shared 5 V rail.

#pragma once

#include <Arduino.h>

namespace leds {

enum Mode {
  MODE_OFF = 0,
  MODE_SOLID,
  MODE_BREATHE,   // smooth sinusoidal in/out, ~3 s period
  MODE_PULSE,     // sharper triangle pulse, ~1 s period
  MODE_RAINBOW,   // hue sweep around the ring (base colour ignored)
};

// Initialise both rings, clear, apply brightness cap. Returns true on
// success.
bool begin();

// Advance any active animations. Cheap when nothing is moving. Must be
// called every loop tick so OSC processing stays responsive.
void update();

// Set the rear ring (16 LEDs) base colour and mode.
void setRear(uint8_t r, uint8_t g, uint8_t b, Mode mode);

// Set the front ring (35 LEDs) base colour and mode.
void setFront(uint8_t r, uint8_t g, uint8_t b, Mode mode);

// Parse a mode name as sent by the Mac Mini ("off", "solid", "breathe",
// "pulse", "rainbow"). Case-insensitive. Returns MODE_OFF and logs a
// warning for unknown names.
Mode parseMode(const char *name);

}  // namespace leds
