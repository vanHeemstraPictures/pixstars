# Home Assistant Setup
## Pixstars — Home Assistant Integration, Dashboard, Monitoring, Safety, and Bridge Design

---

# 1. Purpose

This document defines how **Home Assistant** fits into the **Pixstars** performance stack.

Home Assistant is **not** the main show orchestrator.

Home Assistant is used as:

- backstage control panel
- diagnostics dashboard
- rehearsal interface
- safety and emergency-stop layer
- monitoring system for lamp health and show readiness

The core show stack remains:

- **DigiScore** → master timeline / cue control
- **Ardour** → audio playback and master audio session
- **Jess+** → expressive AI layer for the animatronic lamp
- **ESP32 lamp controller** → hardware execution
- **Home Assistant** → monitoring, manual override, and safety

---

# 2. System Role

Home Assistant should do the following:

- show current scene and cue state
- indicate whether the show is armed and ready
- provide one-touch controls for:
  - start show
  - pause show
  - abort show
  - blackout
  - reset lamp
  - rehearsal scene tests
- monitor:
  - motor temperature
  - controller temperature
  - current draw
  - stall conditions
  - smoke activity
  - lamp connectivity
- provide emergency automations
- allow scene/state testing without running the full show

Home Assistant should **not** be used for:

- frame-accurate timing
- servo interpolation
- MIDI sequencing
- live OSC choreography curves
- audio sync logic

---

# 3. High-Level Architecture

```text
DigiScore
 ├─ Ardour
 ├─ Jess+
 └─ OSC / event bridge
        │
        ├─ ESP32 lamp controller
        └─ Home Assistant
              ├─ dashboard
              ├─ monitoring
              ├─ automations
              └─ emergency controls
```

Recommended communication topology:

```text
Home Assistant
   ↕ MQTT
Pixstars Python Bridge
   ├─ serial → ESP32 lamp controller
   ├─ OSC → DigiScore
   ├─ OSC/HTTP → projection system
   └─ local API/hooks → Jess+
```

---

# 4. Integration Strategy

The recommended integration pattern is:

1. Home Assistant publishes commands over MQTT
2. A Python bridge running on the Mac Mini subscribes to those MQTT topics
3. The bridge forwards actions to:
   - DigiScore
   - ESP32 lamp controller
   - optional projection layer
   - Jess+ runtime
4. The bridge publishes telemetry/status back to Home Assistant

This keeps Home Assistant clean and decoupled from low-level control logic.

---

# 5. Core Entities

## 5.1 Input Booleans

```yaml
input_boolean:
  pixstars_show_armed:
    name: Pixstars Show Armed
  pixstars_show_running:
    name: Pixstars Show Running
  pixstars_abort_requested:
    name: Pixstars Abort Requested
  pixstars_rehearsal_mode:
    name: Pixstars Rehearsal Mode
```

## 5.2 Input Selects

```yaml
input_select:
  pixstars_scene:
    name: Pixstars Scene
    options:
      - EMERGENCE
      - NOTICING
      - THE_FIRST_DRAWING
      - TRANSLATION
      - ASCENT
      - THREE_DEATHS
      - HOLDING
      - RETURN
      - RECOGNITION
      - TRANSFORMATION
      - SYNTHESIS
```

## 5.3 Input Buttons

```yaml
input_button:
  pixstars_start_show:
    name: Start Show
  pixstars_pause_show:
    name: Pause Show
  pixstars_abort_show:
    name: Abort Show
  pixstars_reset_lamp:
    name: Reset Lamp
  pixstars_blackout_now:
    name: Blackout Now
  pixstars_test_rebirth:
    name: Test Rebirth
  pixstars_test_smoke:
    name: Test Smoke
  pixstars_test_curious:
    name: Test Curious
  pixstars_test_arrogant:
    name: Test Arrogant
  pixstars_rehome_lamp:
    name: Rehome Lamp
```

---

# 6. MQTT Entity Model

## 6.1 Status Sensors

```yaml
mqtt:
  sensor:
    - name: "Pixstars Lamp Motor Temperature"
      state_topic: "pixstars/lamp/temp/motor"
      unit_of_measurement: "°C"
      device_class: temperature

    - name: "Pixstars Lamp Controller Temperature"
      state_topic: "pixstars/lamp/temp/controller"
      unit_of_measurement: "°C"
      device_class: temperature

    - name: "Pixstars Lamp Current Draw"
      state_topic: "pixstars/lamp/current"
      unit_of_measurement: "A"

    - name: "Pixstars Current Scene"
      state_topic: "pixstars/scene/current"

    - name: "Pixstars Lamp State"
      state_topic: "pixstars/lamp/state/current"

  binary_sensor:
    - name: "Pixstars Lamp Connected"
      state_topic: "pixstars/lamp/connected"
      payload_on: "online"
      payload_off: "offline"

    - name: "Pixstars Audio OK"
      state_topic: "pixstars/audio/status"
      payload_on: "ok"
      payload_off: "fault"

    - name: "Pixstars Lamp Stall Detected"
      state_topic: "pixstars/lamp/stall"
      payload_on: "on"
      payload_off: "off"

    - name: "Pixstars Lamp Smoke Active"
      state_topic: "pixstars/lamp/smoke"
      payload_on: "on"
      payload_off: "off"
```

## 6.2 Command Topics

Use these MQTT topics for command publishing:

```text
pixstars/show/start
pixstars/show/pause
pixstars/show/abort
pixstars/show/blackout
pixstars/lamp/reset
pixstars/lamp/rehome
pixstars/lamp/state/set
pixstars/lamp/smoke/test
pixstars/projection/logo/set
pixstars/projection/clear
```

Example payloads:

```json
{"action":"start"}
```

```json
{"action":"blackout"}
```

```json
{"state":"REBORN"}
```

```json
{"logo":"team_rockstars"}
```

---

# 7. Recommended Dashboard Layout

Create a single tablet-friendly dashboard with four sections:

## Section A — Show Control
Buttons:
- Start Show
- Pause Show
- Abort Show
- Blackout
- Reset Lamp

## Section B — Show Monitor
Display:
- current scene
- current lamp state
- show armed
- show running
- audio OK
- lamp connected

## Section C — Lamp Health
Display:
- motor temperature
- controller temperature
- current draw
- stall detected
- smoke active

## Section D — Rehearsal Tools
Buttons:
- Test Curious
- Test Arrogant
- Test Rebirth
- Test Smoke
- Rehome Lamp

---

# 8. Example Lovelace Dashboard YAML

```yaml
title: Pixstars Control
views:
  - title: Pixstars
    path: pixstars
    icon: mdi:spotlight
    cards:
      - type: grid
        columns: 5
        cards:
          - type: button
            name: Start Show
            icon: mdi:play
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/show/start
                payload: '{"action":"start"}'

          - type: button
            name: Pause Show
            icon: mdi:pause
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/show/pause
                payload: '{"action":"pause"}'

          - type: button
            name: Abort Show
            icon: mdi:stop
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/show/abort
                payload: '{"action":"abort"}'

          - type: button
            name: Blackout
            icon: mdi:lightbulb-off
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/show/blackout
                payload: '{"action":"blackout"}'

          - type: button
            name: Reset Lamp
            icon: mdi:restart
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/reset
                payload: '{"action":"reset"}'

      - type: entities
        title: Show Status
        entities:
          - input_boolean.pixstars_show_armed
          - input_boolean.pixstars_show_running
          - input_select.pixstars_scene
          - sensor.pixstars_current_scene
          - sensor.pixstars_lamp_state
          - binary_sensor.pixstars_audio_ok
          - binary_sensor.pixstars_lamp_connected

      - type: gauge
        entity: sensor.pixstars_lamp_motor_temperature
        name: Motor Temp
        min: 0
        max: 100
        severity:
          green: 0
          yellow: 50
          red: 70

      - type: gauge
        entity: sensor.pixstars_lamp_controller_temperature
        name: Controller Temp
        min: 0
        max: 100
        severity:
          green: 0
          yellow: 45
          red: 65

      - type: gauge
        entity: sensor.pixstars_lamp_current_draw
        name: Current Draw
        min: 0
        max: 10

      - type: entities
        title: Lamp Health
        entities:
          - binary_sensor.pixstars_lamp_stall_detected
          - binary_sensor.pixstars_lamp_smoke_active

      - type: grid
        columns: 5
        cards:
          - type: button
            name: Curious
            icon: mdi:eye-arrow-right
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/state/set
                payload: '{"state":"CURIOUS"}'

          - type: button
            name: Arrogant
            icon: mdi:crown
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/state/set
                payload: '{"state":"ARROGANT"}'

          - type: button
            name: Rebirth
            icon: mdi:weather-sunset-up
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/state/set
                payload: '{"state":"REBORN"}'

          - type: button
            name: Test Smoke
            icon: mdi:smoke
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/smoke/test
                payload: '{"action":"test"}'

          - type: button
            name: Rehome Lamp
            icon: mdi:home-import-outline
            tap_action:
              action: call-service
              service: mqtt.publish
              data:
                topic: pixstars/lamp/rehome
                payload: '{"action":"rehome"}'
```

---

# 9. Safety Automations

## 9.1 Emergency Stop on Overtemperature or Stall

```yaml
automation:
  - alias: Pixstars Emergency Stop
    triggers:
      - trigger: numeric_state
        entity_id: sensor.pixstars_lamp_motor_temperature
        above: 70
      - trigger: numeric_state
        entity_id: sensor.pixstars_lamp_controller_temperature
        above: 65
      - trigger: state
        entity_id: binary_sensor.pixstars_lamp_stall_detected
        to: "on"
    actions:
      - action: input_boolean.turn_on
        target:
          entity_id: input_boolean.pixstars_abort_requested

      - action: mqtt.publish
        data:
          topic: pixstars/show/blackout
          payload: '{"action":"blackout"}'

      - action: mqtt.publish
        data:
          topic: pixstars/show/abort
          payload: '{"action":"abort"}'
```

## 9.2 Prevent Start if System Not Ready

```yaml
automation:
  - alias: Pixstars Prevent Unsafe Start
    triggers:
      - trigger: state
        entity_id: input_button.pixstars_start_show
    conditions:
      - condition: state
        entity_id: binary_sensor.pixstars_audio_ok
        state: "on"
      - condition: state
        entity_id: binary_sensor.pixstars_lamp_connected
        state: "on"
      - condition: numeric_state
        entity_id: sensor.pixstars_lamp_motor_temperature
        below: 60
      - condition: numeric_state
        entity_id: sensor.pixstars_lamp_controller_temperature
        below: 55
    actions:
      - action: mqtt.publish
        data:
          topic: pixstars/show/start
          payload: '{"action":"start"}'
```

## 9.3 Rehearsal Auto-Return Example

```yaml
automation:
  - alias: Pixstars Test Curious State
    triggers:
      - trigger: state
        entity_id: input_button.pixstars_test_curious
    actions:
      - action: mqtt.publish
        data:
          topic: pixstars/lamp/state/set
          payload: '{"state":"CURIOUS"}'
      - delay: "00:00:03"
      - action: mqtt.publish
        data:
          topic: pixstars/lamp/state/set
          payload: '{"state":"FUNCTIONAL"}'
```

---

# 10. Python Bridge Design

Run this on the **Mac Mini**.

Responsibilities:
- subscribe to MQTT topics
- forward commands to ESP32 over serial
- forward show actions to DigiScore over OSC
- publish telemetry back to Home Assistant

## 10.1 Python Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install paho-mqtt pyserial python-osc
```

## 10.2 Example Bridge Script

```python
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt
import serial
from pythonosc.udp_client import SimpleUDPClient


MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

SERIAL_PORT = "/dev/tty.usbserial-0001"
SERIAL_BAUD = 115200

DIGISCORE_OSC_HOST = "127.0.0.1"
DIGISCORE_OSC_PORT = 9000


@dataclass
class LampSerial:
    port: str
    baudrate: int
    timeout: float = 0.5
    ser: Optional[serial.Serial] = None

    def connect(self) -> None:
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2.0)

    def send(self, line: str) -> str:
        if not self.ser or not self.ser.is_open:
            raise RuntimeError("Lamp serial is not connected")
        self.ser.write((line.strip() + "\n").encode("utf-8"))
        self.ser.flush()
        return self.ser.readline().decode("utf-8", errors="replace").strip()


lamp = LampSerial(port=SERIAL_PORT, baudrate=SERIAL_BAUD)
osc = SimpleUDPClient(DIGISCORE_OSC_HOST, DIGISCORE_OSC_PORT)


def publish_status(client: mqtt.Client, topic: str, payload: str) -> None:
    client.publish(topic, payload, qos=0, retain=False)


def on_connect(client: mqtt.Client, userdata, flags, rc, properties=None):
    topics = [
        ("pixstars/show/start", 0),
        ("pixstars/show/pause", 0),
        ("pixstars/show/abort", 0),
        ("pixstars/show/blackout", 0),
        ("pixstars/lamp/reset", 0),
        ("pixstars/lamp/rehome", 0),
        ("pixstars/lamp/state/set", 0),
        ("pixstars/lamp/smoke/test", 0),
        ("pixstars/projection/logo/set", 0),
        ("pixstars/projection/clear", 0),
    ]
    for topic, qos in topics:
        client.subscribe(topic, qos=qos)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    topic = msg.topic
    payload = msg.payload.decode("utf-8", errors="replace").strip()

    try:
        data = json.loads(payload) if payload else {}
    except json.JSONDecodeError:
        data = {"raw": payload}

    try:
        if topic == "pixstars/show/start":
            osc.send_message("/pixstars/show/start", 1)
            publish_status(client, "pixstars/show/running", "on")

        elif topic == "pixstars/show/pause":
            osc.send_message("/pixstars/show/pause", 1)

        elif topic == "pixstars/show/abort":
            osc.send_message("/pixstars/show/abort", 1)
            lamp.send("BLACKOUT")
            publish_status(client, "pixstars/show/running", "off")

        elif topic == "pixstars/show/blackout":
            osc.send_message("/pixstars/show/blackout", 1)
            lamp.send("BLACKOUT")

        elif topic == "pixstars/lamp/reset":
            lamp.send("RESET")

        elif topic == "pixstars/lamp/rehome":
            lamp.send("REHOME")

        elif topic == "pixstars/lamp/state/set":
            state = data["state"]
            ack = lamp.send(f"STATE {state}")
            publish_status(client, "pixstars/lamp/state/current", state)
            publish_status(client, "pixstars/lamp/ack", ack)

        elif topic == "pixstars/lamp/smoke/test":
            lamp.send("SMOKE ON")
            time.sleep(1.0)
            lamp.send("SMOKE OFF")

        elif topic == "pixstars/projection/logo/set":
            logo = data["logo"]
            osc.send_message("/pixstars/projection/logo", logo)

        elif topic == "pixstars/projection/clear":
            osc.send_message("/pixstars/projection/clear", 1)

    except Exception as exc:
        publish_status(client, "pixstars/bridge/error", str(exc))


def main():
    lamp.connect()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)
    publish_status(client, "pixstars/lamp/connected", "online")

    try:
        client.loop_forever()
    finally:
        publish_status(client, "pixstars/lamp/connected", "offline")


if __name__ == "__main__":
    main()
```

---

# 11. ESP32 Expectations

The ESP32 lamp controller should support at least:

```text
PING
RESET
REHOME
BLACKOUT
STATE FUNCTIONAL
STATE CURIOUS
STATE DISMISSIVE
STATE PLEASED
STATE ARROGANT
STATE OVERHEAT
STATE DEAD
STATE REBORN
STATE LEARNING
STATE CELEBRATE
SMOKE ON
SMOKE OFF
```

And respond with acknowledgements like:

```text
ACK READY
ACK STATE CURIOUS
ACK BLACKOUT
ACK REHOME
ERR UNKNOWN_CMD
```

---

# 12. Recommended Show Readiness Checklist

Before pressing **Start Show**, verify in Home Assistant:

- Lamp Connected = ON
- Audio OK = ON
- Motor Temperature < 60°C
- Controller Temperature < 55°C
- Stall Detected = OFF
- Smoke Active = OFF
- Show Armed = ON

---

# 13. Rehearsal Mode

Use `input_boolean.pixstars_rehearsal_mode` to unlock:

- lamp state test buttons
- projection test buttons
- smoke test buttons
- individual scene rehearsal actions

In production mode, hide these controls.

---

# 14. Suggested File Structure

```text
pixstars/
 ├── home_assistant/
 │    ├── HOME_ASSISTANT_SETUP.md
 │    ├── lovelace-pixstars.yaml
 │    ├── automations.yaml
 │    └── mqtt-entities.yaml
 │
 ├── bridge/
 │    └── pixstars_ha_bridge.py
 │
 ├── firmware/
 │    └── lamp_controller.ino
 │
 ├── ardour/
 ├── digiscore/
 └── jess_plus/
```

---

# 15. Conclusion

Home Assistant adds significant value to the Pixstars performance when used as:

- operator console
- diagnostics layer
- safety system
- rehearsal interface

It should remain outside the frame-accurate choreography loop, but it is highly valuable around that loop.

The recommended architecture is:

- **DigiScore** for cue timeline
- **Ardour** for audio
- **Jess+** for expressive lamp behavior
- **ESP32** for hardware execution
- **Home Assistant** for human control, safety, and visibility

This is the correct role for Home Assistant in Pixstars.

---
