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
#include <OSCBundle.h>
#include <OSCMessage.h>

#if __has_include("config.h")
#include "config.h"
#else
#error "config.h not found. Copy src/config.h.example to src/config.h and fill in your WiFi credentials."
#endif

#include "handlers.h"
#include "maestro.h"

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

  maestro::begin();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[wifi] connection lost, reconnecting");
    ledMode = LED_ERROR;
    updateStatusLed();
    connectWiFi();
    udp.begin(OSC_LISTEN_PORT);
  }

  OSCMessage msg;
  int size = udp.parsePacket();
  if (size > 0) {
    while (size--) msg.fill(udp.read());
    if (!msg.hasError()) {
      msg.dispatch("/ping", handlePing);
      msg.route("/servo", handlers::servo);
      msg.route("/head", handlers::head);
      msg.route("/led", handlers::led);
      msg.route("/turntable", handlers::turntable);
    } else {
      oscError = msg.getError();
      Serial.printf("[osc] parse error: %d\n", (int)oscError);
    }
  }

  updateStatusLed();
}
