// WS2812 LED ring driver. See leds.h.

#include "leds.h"

#if __has_include("config.h")
#include "config.h"
#endif

// Defaults. Override in config.h. Pins match config.h.example pin map
// (GPIO 9 = rear, GPIO 10 = front on the ESP32-S3 cave controller).
#ifndef LED_RING_REAR_PIN
#define LED_RING_REAR_PIN     9
#endif
#ifndef LED_RING_REAR_COUNT
#define LED_RING_REAR_COUNT   16
#endif
#ifndef LED_RING_FRONT_PIN
#define LED_RING_FRONT_PIN    10
#endif
#ifndef LED_RING_FRONT_COUNT
#define LED_RING_FRONT_COUNT  35
#endif

// Global brightness cap (0..255). With 51 LEDs total a cap of 64 keeps
// peak draw on the shared 5 V rail well under 1 A even at full white.
#ifndef LED_MAX_BRIGHTNESS
#define LED_MAX_BRIGHTNESS    64
#endif

// Animation periods in milliseconds.
#ifndef LED_BREATHE_PERIOD_MS
#define LED_BREATHE_PERIOD_MS 3000
#endif
#ifndef LED_PULSE_PERIOD_MS
#define LED_PULSE_PERIOD_MS   1000
#endif
#ifndef LED_RAINBOW_PERIOD_MS
#define LED_RAINBOW_PERIOD_MS 4000
#endif

#define FASTLED_INTERNAL  // suppress FastLED pragma version banner
#include <FastLED.h>

namespace leds {

struct Ring {
  CRGB     *buf;
  uint16_t  count;
  uint8_t   baseR, baseG, baseB;
  Mode      mode;
};

static CRGB rearBuf[LED_RING_REAR_COUNT];
static CRGB frontBuf[LED_RING_FRONT_COUNT];

static Ring rear  = { rearBuf,  LED_RING_REAR_COUNT,  0, 0, 0, MODE_OFF };
static Ring front = { frontBuf, LED_RING_FRONT_COUNT, 0, 0, 0, MODE_OFF };

bool begin() {
  FastLED.addLeds<WS2812B, LED_RING_REAR_PIN,  GRB>(rearBuf,  LED_RING_REAR_COUNT);
  FastLED.addLeds<WS2812B, LED_RING_FRONT_PIN, GRB>(frontBuf, LED_RING_FRONT_COUNT);
  FastLED.setBrightness(LED_MAX_BRIGHTNESS);
  FastLED.clear(true);
  Serial.printf("[leds] rear=GPIO%d (%d) front=GPIO%d (%d) brightness=%d\n",
                LED_RING_REAR_PIN,  LED_RING_REAR_COUNT,
                LED_RING_FRONT_PIN, LED_RING_FRONT_COUNT,
                (int)LED_MAX_BRIGHTNESS);
  return true;
}

// Scale an 8-bit colour channel by an 8-bit value (0..255 -> 0..value).
static inline uint8_t scale8(uint8_t c, uint8_t s) {
  return (uint16_t)c * (uint16_t)(s + 1) >> 8;
}

// Render one ring's current frame into its buffer. Returns true if any
// pixel actually changes per call (i.e. the mode is animated).
static bool renderRing(const Ring &r, unsigned long now) {
  switch (r.mode) {
    case MODE_OFF:
      fill_solid(r.buf, r.count, CRGB::Black);
      return false;
    case MODE_SOLID:
      fill_solid(r.buf, r.count, CRGB(r.baseR, r.baseG, r.baseB));
      return false;
    case MODE_BREATHE: {
      // 0..255 sine half-wave -> smooth in/out
      uint8_t s = sin8((uint8_t)((now * 256UL) / LED_BREATHE_PERIOD_MS));
      fill_solid(r.buf, r.count,
                 CRGB(scale8(r.baseR, s), scale8(r.baseG, s), scale8(r.baseB, s)));
      return true;
    }
    case MODE_PULSE: {
      // triangle 0..255..0 -- sharper than breathe
      uint16_t phase = (now % LED_PULSE_PERIOD_MS) * 256UL / LED_PULSE_PERIOD_MS;
      uint8_t s = phase < 128 ? phase * 2 : (255 - phase) * 2;
      fill_solid(r.buf, r.count,
                 CRGB(scale8(r.baseR, s), scale8(r.baseG, s), scale8(r.baseB, s)));
      return true;
    }
    case MODE_RAINBOW: {
      uint8_t base = (now * 256UL) / LED_RAINBOW_PERIOD_MS;
      uint8_t step = 256 / r.count;  // one full wheel around the ring
      fill_rainbow(r.buf, r.count, base, step);
      return true;
    }
  }
  return false;
}

void update() {
  static unsigned long lastFrame = 0;
  unsigned long now = millis();
  // Cap refresh at ~60 Hz so OSC processing always gets CPU.
  if (now - lastFrame < 16) return;
  lastFrame = now;
  bool a = renderRing(rear,  now);
  bool b = renderRing(front, now);
  // Always push at least once after a setRear/setFront call; the
  // dirty flag is implicit because setRear/setFront set lastFrame=0
  // via the static below being reset on mode change. For simplicity
  // we just always show() at the capped rate.
  (void)a; (void)b;
  FastLED.show();
}

void setRear(uint8_t r, uint8_t g, uint8_t b, Mode mode) {
  rear.baseR = r; rear.baseG = g; rear.baseB = b; rear.mode = mode;
  Serial.printf("[leds] rear r=%u g=%u b=%u mode=%d\n", r, g, b, (int)mode);
}

void setFront(uint8_t r, uint8_t g, uint8_t b, Mode mode) {
  front.baseR = r; front.baseG = g; front.baseB = b; front.mode = mode;
  Serial.printf("[leds] front r=%u g=%u b=%u mode=%d\n", r, g, b, (int)mode);
}

Mode parseMode(const char *name) {
  if (!name) return MODE_OFF;
  if (!strcasecmp(name, "off"))     return MODE_OFF;
  if (!strcasecmp(name, "solid"))   return MODE_SOLID;
  if (!strcasecmp(name, "breathe")) return MODE_BREATHE;
  if (!strcasecmp(name, "pulse"))   return MODE_PULSE;
  if (!strcasecmp(name, "rainbow")) return MODE_RAINBOW;
  Serial.printf("[leds] unknown mode '%s', defaulting to off\n", name);
  return MODE_OFF;
}

}  // namespace leds
