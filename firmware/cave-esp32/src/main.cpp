// Pixstars cave ESP32 firmware
//
// Connects to WiFi, listens for OSC messages from the Mac Mini on
// OSC_LISTEN_PORT, and routes them to subsystem handler stubs.
//
// LED_BUILTIN status:
//   slow blink (1 Hz)   -> connecting to WiFi
//   solid on            -> WiFi connected, OSC server running
//   fast blink (10 Hz)  -> error state (WiFi lost, etc.)

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

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

enum LedMode { LED_CONNECTING, LED_CONNECTED, LED_ERROR };

static WiFiUDP udp;
static OSCErrorCode oscError;
static LedMode ledMode = LED_CONNECTING;

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
      digitalWrite(LED_BUILTIN, HIGH);
      return;
  }

  if (now - lastToggle >= interval) {
    lastToggle = now;
    state = !state;
    digitalWrite(LED_BUILTIN, state ? HIGH : LOW);
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
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Serial.begin(SERIAL_BAUD);
  delay(100);
  Serial.println();
  Serial.println("[boot] Pixstars cave ESP32 firmware");

  connectWiFi();

  udp.begin(OSC_LISTEN_PORT);
  Serial.printf("[osc] listening on UDP port %d\n", OSC_LISTEN_PORT);
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
