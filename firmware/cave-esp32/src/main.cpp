// Pixstars cave ESP32 firmware
//
// Connects to WiFi, listens for OSC messages from the Mac Mini on
// OSC_LISTEN_PORT, and routes them to subsystem handler stubs.
//
// Status LED:
//   On ESP32-S3-DevKitC-1 the onboard indicator is an addressable WS2812
//   RGB LED on GPIO 48 (driven via neopixelWrite() from the Arduino-ESP32
//   core). On a classic ESP32 we fall back to a plain digital LED_BUILTIN.
//   slow blink (1 Hz)   -> connecting to WiFi   (blue on S3)
//   solid on            -> WiFi connected, OSC server running (green on S3)
//   fast blink (10 Hz)  -> error state (WiFi lost, etc.) (red on S3)

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ESPmDNS.h>
#include <OSCBundle.h>
#include <OSCMessage.h>

#if __has_include("config.h")
#include "config.h"
#else
#error "config.h not found. Copy src/config.h.example to src/config.h and fill in your WiFi credentials."
#endif

#include "dynamixel.h"
#include "handlers.h"
#include "leds.h"
#include "maestro.h"
#include "turntable.h"

// --- Watchdog / health-monitoring tunables (override in config.h) ---
//
// If no OSC packet is received for WATCHDOG_TIMEOUT_MS milliseconds we
// drop all outputs into a safe state: LEDs fade to dim blue, turntable
// stops, servos and AX-12A hold their last commanded positions. The
// next valid OSC packet clears the safe state.
#ifndef WATCHDOG_TIMEOUT_MS
#define WATCHDOG_TIMEOUT_MS 5000UL
#endif

// Period for the heap-free debug log line on Serial. 0 disables.
#ifndef HEAP_LOG_INTERVAL_MS
#define HEAP_LOG_INTERVAL_MS 10000UL
#endif

// mDNS hostname (the cave will answer as <MDNS_HOSTNAME>.local).
#ifndef MDNS_HOSTNAME
#define MDNS_HOSTNAME "pixstars-cave"
#endif

// Optional OTA password. Leave empty to disable password authentication.
#ifndef OTA_PASSWORD
#define OTA_PASSWORD ""
#endif

// RGB colour written to both rings while the watchdog is asserted.
// Dim blue is the project convention for "no host, holding safe".
#ifndef SAFE_LED_R
#define SAFE_LED_R 0
#endif
#ifndef SAFE_LED_G
#define SAFE_LED_G 0
#endif
#ifndef SAFE_LED_B
#define SAFE_LED_B 24
#endif

#ifdef CONFIG_IDF_TARGET_ESP32S3
  #ifndef STATUS_LED_PIN
    #define STATUS_LED_PIN 48
  #endif
#else
  #ifndef LED_BUILTIN
    #define LED_BUILTIN 2
  #endif
  #ifndef STATUS_LED_PIN
    #define STATUS_LED_PIN LED_BUILTIN
  #endif
#endif

enum LedMode { LED_CONNECTING, LED_CONNECTED, LED_ERROR };

static WiFiUDP udp;
static OSCErrorCode oscError;
static LedMode ledMode = LED_CONNECTING;

// Watchdog / health state.
static volatile unsigned long lastOscMs = 0;
static bool safeStateActive = false;
static unsigned long lastHeapLogMs = 0;

// Forward declarations for state helpers used by setup()/loop() below.
static void enterSafeState();
static void exitSafeState();
static void serviceWatchdog();
static void serviceHeapLog();
static void startLedTask();

// Write the status LED at a given on/off state. On the S3 this drives the
// onboard WS2812 with a colour that encodes the current ledMode; on a
// classic ESP32 it toggles a plain digital pin.
static void writeStatusLed(bool on) {
#ifdef CONFIG_IDF_TARGET_ESP32S3
  if (!on) {
    neopixelWrite(STATUS_LED_PIN, 0, 0, 0);
    return;
  }
  switch (ledMode) {
    case LED_CONNECTING: neopixelWrite(STATUS_LED_PIN, 0,  0,  16); break;  // blue
    case LED_ERROR:      neopixelWrite(STATUS_LED_PIN, 16, 0,  0);  break;  // red
    case LED_CONNECTED:  neopixelWrite(STATUS_LED_PIN, 0,  16, 0);  break;  // green
  }
#else
  digitalWrite(STATUS_LED_PIN, on ? HIGH : LOW);
#endif
}

// Non-blocking LED pattern driver.
static void updateStatusLed() {
  static unsigned long lastToggle = 0;
  static bool state = false;
  unsigned long now = millis();
  unsigned long interval = 0;

  switch (ledMode) {
    case LED_CONNECTING: interval = 500; break;   // 1 Hz
    case LED_ERROR:      interval = 50;  break;   // 10 Hz
    case LED_CONNECTED:
      writeStatusLed(true);
      return;
  }

  if (now - lastToggle >= interval) {
    lastToggle = now;
    state = !state;
    writeStatusLed(state);
  }
}

// /ping -> reply /pong with uptime millis to the sender.
static void handlePing(OSCMessage &msg) {
  IPAddress remoteIp = udp.remoteIP();
  uint16_t remotePort = udp.remotePort();

  Serial.printf("[ping] from %s:%u\n", remoteIp.toString().c_str(), remotePort);

  OSCMessage reply("/pong");
  reply.add((int32_t)millis());

  udp.beginPacket(remoteIp, remotePort);
  reply.send(udp);
  udp.endPacket();
  reply.empty();
}

// /status -> reply /status/reply with a flat tuple of diagnostic values:
//   (i) uptime ms        - millis() since boot
//   (i) free heap bytes  - ESP.getFreeHeap()
//   (i) RSSI dBm         - WiFi.RSSI() (negative, e.g. -62)
//   (s) IP address       - dotted-quad
//   (i) safe-state flag  - 1 while the watchdog is asserted
//   (i) turntable homed  - 1 if originSeek() has triggered since boot
//   (i) turntable running- 1 if a motion is in flight
//   (f) turntable degrees- current logical position
// Kept as a flat OSC message (not a bundle) so the Mac Mini side stays simple.
static void handleStatus(OSCMessage & /*msg*/) {
  IPAddress remoteIp = udp.remoteIP();
  uint16_t remotePort = udp.remotePort();

  OSCMessage reply("/status/reply");
  reply.add((int32_t)millis());
  reply.add((int32_t)ESP.getFreeHeap());
  reply.add((int32_t)WiFi.RSSI());
  reply.add(WiFi.localIP().toString().c_str());
  reply.add((int32_t)(safeStateActive ? 1 : 0));
  reply.add((int32_t)(turntable::isHomed()   ? 1 : 0));
  reply.add((int32_t)(turntable::isRunning() ? 1 : 0));
  reply.add(turntable::currentDegrees());

  udp.beginPacket(remoteIp, remotePort);
  reply.send(udp);
  udp.endPacket();
  reply.empty();

  Serial.printf("[status] reply to %s:%u (heap=%u RSSI=%d)\n",
                remoteIp.toString().c_str(), remotePort,
                (unsigned)ESP.getFreeHeap(), (int)WiFi.RSSI());
}

// Drive every output into a known-safe configuration. Called by the
// watchdog when OSC silence exceeds WATCHDOG_TIMEOUT_MS, and may be
// triggered by other unrecoverable conditions (e.g. WiFi loss).
//
//   LEDs        : dim blue, solid (visual cue that the host is gone)
//   Turntable   : smooth stop (uses configured decel ramp; preserves
//                 position so the next cue continues cleanly)
//   Servos      : no-op -- the Maestro holds the last commanded target
//   AX-12A head : no-op -- AX-12A holds its goal position by default
static void enterSafeState() {
  if (safeStateActive) return;
  safeStateActive = true;
  Serial.printf("[watchdog] safe state ENGAGED (no OSC for >%lu ms)\n",
                (unsigned long)WATCHDOG_TIMEOUT_MS);
  leds::setRear (SAFE_LED_R, SAFE_LED_G, SAFE_LED_B, leds::MODE_SOLID);
  leds::setFront(SAFE_LED_R, SAFE_LED_G, SAFE_LED_B, leds::MODE_SOLID);
  turntable::stop();
}

// Released as soon as any valid OSC packet arrives. We do not auto-restore
// the previous LED state -- the host is expected to re-issue cues -- but
// we log the transition so it's traceable in the show log.
static void exitSafeState() {
  if (!safeStateActive) return;
  safeStateActive = false;
  Serial.println("[watchdog] safe state CLEARED (OSC restored)");
}

static void serviceWatchdog() {
  if (lastOscMs == 0) return;  // no traffic yet since boot; don't latch
  if (millis() - lastOscMs > WATCHDOG_TIMEOUT_MS) {
    enterSafeState();
  }
}

static void serviceHeapLog() {
  if (HEAP_LOG_INTERVAL_MS == 0) return;
  unsigned long now = millis();
  if (now - lastHeapLogMs < HEAP_LOG_INTERVAL_MS) return;
  lastHeapLogMs = now;
  Serial.printf("[health] heap=%u min=%u RSSI=%d uptime=%lus safe=%d\n",
                (unsigned)ESP.getFreeHeap(),
                (unsigned)ESP.getMinFreeHeap(),
                (int)WiFi.RSSI(),
                now / 1000UL,
                (int)safeStateActive);
}

// LED rendering runs on core 0 at a lower priority than the Arduino main
// loop (loopTask runs on core 1 at priority 1). This keeps WiFi/OSC and
// servo dispatch on core 1 from being delayed by FastLED frame pushes.
// FastLED.show() on the ESP32-S3 uses the RMT peripheral, which is
// itself ISR-driven, so the actual pixel clocking is independent of the
// task that triggers it.
static void ledTask(void * /*arg*/) {
  const TickType_t period = pdMS_TO_TICKS(10);  // ~100 Hz wakeup; leds::update() self-throttles to ~60 Hz
  TickType_t lastWake = xTaskGetTickCount();
  for (;;) {
    leds::update();
    vTaskDelayUntil(&lastWake, period);
  }
}

static void startLedTask() {
  xTaskCreatePinnedToCore(
      ledTask,
      "leds",
      4096,
      nullptr,
      1,    // priority 1 (same nominal as loopTask, but pinned to the other core)
      nullptr,
      0);   // core 0 (loopTask runs on core 1)
}

// Configure ArduinoOTA (firmware updates over WiFi) and announce the
// cave as <MDNS_HOSTNAME>.local for service discovery. Called once
// after WiFi is up. ArduinoOTA itself starts an mDNS responder, so we
// only call MDNS.begin() if it isn't already running.
static void startOtaAndMdns() {
  ArduinoOTA.setHostname(MDNS_HOSTNAME);
  if (strlen(OTA_PASSWORD) > 0) {
    ArduinoOTA.setPassword(OTA_PASSWORD);
  }
  ArduinoOTA
      .onStart([]() {
        // Stop motion before flashing so the table doesn't drift mid-update.
        turntable::stop();
        leds::setRear (0, 0, 16, leds::MODE_PULSE);
        leds::setFront(0, 0, 16, leds::MODE_PULSE);
        Serial.println("[ota] update starting");
      })
      .onEnd([]()  { Serial.println("\n[ota] update finished"); })
      .onError([](ota_error_t error) {
        Serial.printf("[ota] error %u\n", (unsigned)error);
      })
      .onProgress([](unsigned int progress, unsigned int total) {
        static unsigned int lastPct = 101;
        unsigned int pct = (progress * 100U) / (total ? total : 1U);
        if (pct != lastPct) {
          Serial.printf("[ota] %u%%\r", pct);
          lastPct = pct;
        }
      });
  ArduinoOTA.begin();

  // ArduinoOTA already starts mDNS; calling MDNS.begin() again is benign
  // on the ESP32 core and lets us add a generic OSC service record.
  if (MDNS.begin(MDNS_HOSTNAME)) {
    MDNS.addService("osc", "udp", OSC_LISTEN_PORT);
    Serial.printf("[mdns] %s.local advertised (osc/udp:%d)\n",
                  MDNS_HOSTNAME, OSC_LISTEN_PORT);
  } else {
    Serial.println("[mdns] start failed");
  }
}

static void connectWiFi() {
  ledMode = LED_CONNECTING;
  WiFi.mode(WIFI_STA);
  WiFi.setHostname(DEVICE_HOSTNAME);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.printf("[wifi] connecting to %s", WIFI_SSID);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    updateStatusLed();
    delay(50);
    if (millis() - start > 1000) {
      Serial.print(".");
      start = millis();
    }
  }
  Serial.println();
  Serial.printf("[wifi] connected, IP = %s\n", WiFi.localIP().toString().c_str());
  ledMode = LED_CONNECTED;
}

void setup() {
#ifndef CONFIG_IDF_TARGET_ESP32S3
  pinMode(STATUS_LED_PIN, OUTPUT);
#endif
  writeStatusLed(false);

  Serial.begin(SERIAL_BAUD);
  delay(100);
  Serial.println();
  Serial.println("[boot] Pixstars cave ESP32 firmware");

  connectWiFi();

  udp.begin(OSC_LISTEN_PORT);
  Serial.printf("[osc] listening on UDP port %d\n", OSC_LISTEN_PORT);

  startOtaAndMdns();

  maestro::begin();
  dynamixel::begin();
  leds::begin();
  turntable::begin();

  // LED rendering runs in its own task on core 0; loop() (core 1) no
  // longer needs to call leds::update().
  startLedTask();

  Serial.printf("[boot] ready. heap=%u\n", (unsigned)ESP.getFreeHeap());
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[wifi] connection lost, reconnecting");
    enterSafeState();
    ledMode = LED_ERROR;
    updateStatusLed();
    connectWiFi();
    udp.begin(OSC_LISTEN_PORT);
  }

  ArduinoOTA.handle();

  OSCMessage msg;
  int size = udp.parsePacket();
  if (size > 0) {
    while (size--) msg.fill(udp.read());
    if (!msg.hasError()) {
      lastOscMs = millis();
      exitSafeState();
      msg.dispatch("/ping", handlePing);
      msg.dispatch("/status", handleStatus);
      msg.route("/servo", handlers::servo);
      msg.route("/head", handlers::head);
      msg.route("/led", handlers::led);
      msg.route("/turntable", handlers::turntable);
    } else {
      oscError = msg.getError();
      Serial.printf("[osc] parse error: %d\n", (int)oscError);
    }
  }

  serviceWatchdog();
  serviceHeapLog();
  turntable::update();
  updateStatusLed();
}
