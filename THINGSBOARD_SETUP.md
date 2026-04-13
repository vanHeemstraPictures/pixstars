# Pixstars — ThingsBoard Integration Setup

> ThingsBoard serves as the **monitoring, telemetry, and dashboard layer** on top of the
> existing Show Conductor. The Conductor keeps real-time control (OSC, sub-50ms timing);
> ThingsBoard provides professional dashboards, historical telemetry, device health
> monitoring, and alarm management.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Mac Mini M4 Pro                                 │
│                                                                         │
│  ┌──────────────┐     OSC (UDP)      ┌───────────────────────────────┐  │
│  │  Show         │──────────────────▶│  Ardour 9 (port 3819)        │  │
│  │  Conductor    │──────────────────▶│  Lamp Adapter (port 9001)    │  │
│  │  (Python)     │──────────────────▶│  Projection (port 9002)      │  │
│  │              │──────────────────▶│  Lighting/DMX (port 9003)    │  │
│  │              │──────────────────▶│  Digital Twin (port 9004)    │  │
│  │              │                    └───────────────────────────────┘  │
│  │              │                                                       │
│  │              │     MQTT            ┌───────────────────────────────┐  │
│  │              │────────────────────▶│  ThingsBoard                 │  │
│  │              │                    │  (Cloud or local CE)          │  │
│  └──────────────┘                    │                               │  │
│                                      │  ┌─────────────────────────┐  │  │
│                                      │  │ Dashboard: Show Monitor │  │  │
│                                      │  │ Alarms: Device Health   │  │  │
│                                      │  │ History: Show Telemetry │  │  │
│                                      │  └─────────────────────────┘  │  │
│                                      └───────────────────────────────┘  │
│                                                                         │
│  ┌──────────────┐     MQTT            ┌───────────────────────────────┐  │
│  │  Home         │◀──────────────────▶│  ThingsBoard                 │  │
│  │  Assistant    │                    │  (bidirectional via MQTT)     │  │
│  │  (Parallels)  │                    └───────────────────────────────┘  │
│  └──────────────┘                                                       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Design Decision: Why a Monitoring Layer, Not a Replacement

| Concern | Conductor (keeps) | ThingsBoard (adds) |
|---------|------------------|--------------------|
| Real-time cue dispatch (<50ms) | ✅ OSC over UDP | ❌ Rule Engine latency ~200ms+ |
| Ardour transport sync | ✅ /toggle_roll | ❌ No DAW integration |
| DMX lighting timing | ✅ Direct serial | ❌ No DMX protocol |
| Device health monitoring | ❌ No visibility | ✅ Connectivity status + alarms |
| Show history / replay | ❌ Console logs only | ✅ Time-series telemetry |
| Professional dashboards | ❌ BabylonJS twin only | ✅ Configurable widgets |
| Multi-show management | ❌ Single instance | ✅ Multi-tenant |
| Venue automation (HA bridge) | ❌ Not connected | ✅ MQTT ↔ HA |

---

## ThingsBoard Edition

| Edition | Use Case | Notes |
|---------|----------|-------|
| **Cloud (free tier)** | Getting started, testing | https://thingsboard.io/installations |
| **Community Edition (CE)** | Self-hosted on Mac Mini or Parallels VM | Free, Apache 2.0 |
| **Professional Edition (PE)** | If you need integrations, entity groups, white-labelling | Commercial licence |

**Recommendation:** Start with ThingsBoard Cloud free tier. Migrate to self-hosted CE later if needed.

---

## Entity Model

### Devices (5 subsystems)

Each Pixstars subsystem is registered as a ThingsBoard **Device** with a dedicated **Device Profile**.

| Device Name | Device Profile | Protocol | Description |
|-------------|---------------|----------|-------------|
| `pixstars-ardour` | `Ardour DAW` | MQTT | Audio playback — Ardour 9 with Pianoteq + MODO DRUM |
| `pixstars-lamp` | `Jess+ Lamp` | MQTT | Desk lamp with 14 personality states |
| `pixstars-projection` | `Projection Display` | MQTT | Pygame display with 10 scenes |
| `pixstars-lighting` | `DMX Lighting` | MQTT | DMX Enttec Pro with 9 lighting states |
| `pixstars-conductor` | `Show Conductor` | MQTT | Central orchestrator (meta-device) |

### Asset Hierarchy

```
Asset: "Pixstars Show" (type: Show)
  ├── Device: pixstars-conductor
  ├── Device: pixstars-ardour
  ├── Device: pixstars-lamp
  ├── Device: pixstars-projection
  └── Device: pixstars-lighting
```

### Device Profiles

#### Ardour DAW

| Telemetry Key | Type | Description |
|---------------|------|-------------|
| `transport_state` | string | "PLAYING", "STOPPED" |
| `playhead_seconds` | float | Current playhead position in seconds |
| `sample_rate` | int | Session sample rate (48000) |

**Alarm Rules:**
- CRITICAL: `transport_state == "STOPPED"` during active show (unexpected stop)

#### Jess+ Lamp

| Telemetry Key | Type | Description |
|---------------|------|-------------|
| `state` | string | Current state name (e.g. "CURIOUS", "PLEASED") |
| `energy` | float | 0.0–1.0 |
| `speed` | float | 0.0–1.0 |
| `range` | float | 0.0–1.0 |
| `jitter` | float | 0.0–0.5 |
| `tilt_bias` | float | -1.0 to +1.0 |
| `servo_connected` | bool | Physical servo connection status |

**Alarm Rules:**
- WARNING: `state == "OVERHEATING"` (lamp in distress)
- CRITICAL: `servo_connected == false` during active show

#### Projection Display

| Telemetry Key | Type | Description |
|---------------|------|-------------|
| `scene` | string | Current scene name (e.g. "GNR_LOGO", "DISNEY_CASTLE") |
| `display_connected` | bool | Pygame display active |

**Alarm Rules:**
- CRITICAL: `display_connected == false` during active show

#### DMX Lighting

| Telemetry Key | Type | Description |
|---------------|------|-------------|
| `state` | string | Current lighting state (e.g. "ROCKSTAR", "DISNEY_SOFT") |
| `dmx_device` | string | "mock", "auto", or serial port path |
| `dmx_connected` | bool | DMX USB interface connected |
| `channels` | json | Current DMX channel values {r, g, b, w, strobe, dimmer} |

**Alarm Rules:**
- CRITICAL: `dmx_connected == false` during active show
- WARNING: any channel value stuck (no change for >30s during show)

#### Show Conductor

| Telemetry Key | Type | Description |
|---------------|------|-------------|
| `show_state` | string | "IDLE", "RUNNING", "PAUSED", "COMPLETE", "ABORTED" |
| `current_cue` | int | Current cue index (1–15) |
| `cue_name` | string | Current cue name (e.g. "SHOW_START", "GNR_LOGO") |
| `elapsed_seconds` | float | Seconds since show start |
| `total_cues` | int | Total number of cues (15) |
| `show_duration` | float | Total show duration in seconds (555.0) |

**Alarm Rules:**
- WARNING: `elapsed_seconds > show_duration + 10` (show running longer than expected)
- CRITICAL: `show_state == "ABORTED"`

---

## MQTT Telemetry Bridge

### MQTT Broker

Use the **Mosquitto MQTT broker** already running in the Parallels Home Assistant VM,
or connect directly to ThingsBoard's built-in MQTT transport.

| Setting | Value |
|---------|-------|
| Broker Host | `localhost` (or Parallels VM IP) |
| Broker Port | 1883 |
| ThingsBoard MQTT Port | 1883 (Cloud) or 1883 (CE) |

### Topic Convention

ThingsBoard uses device access tokens for authentication. Each device publishes to:

```
v1/devices/me/telemetry
```

With the device's access token as MQTT username (no password).

### Bridge Script: `thingsboard/telemetry_bridge.py`

**Purpose:** Subscribes to OSC state changes from the conductor and publishes them as
MQTT telemetry to ThingsBoard.

```
Conductor → OSC → Telemetry Bridge → MQTT → ThingsBoard
```

**Implementation approach:**

1. Listen on a dedicated OSC port (e.g. 9005) for mirrored state updates
2. OR: Import the conductor's OSCSender and add MQTT publishing directly
3. Publish telemetry JSON to ThingsBoard via MQTT

**Telemetry JSON format:**

```json
{
  "ts": 1711700000000,
  "values": {
    "transport_state": "PLAYING",
    "current_cue": 3,
    "cue_name": "LAMP_ON",
    "elapsed_seconds": 12.0
  }
}
```

---

## Dashboard Layout

### Main Dashboard: "Pixstars Show Monitor"

```
┌─────────────────────────────────────────────────────────────────┐
│  PIXSTARS SHOW MONITOR                              [LIVE] 🟢  │
├──────────────────────┬──────────────────────────────────────────┤
│                      │                                          │
│  SHOW STATUS         │  TIMELINE                                │
│  ┌────────────────┐  │  ┌────────────────────────────────────┐  │
│  │ State: RUNNING │  │  │ ████████░░░░░░░░  Cue 7/15        │  │
│  │ Cue: AI_ITER.  │  │  │ 4:30 / 9:15                       │  │
│  │ Elapsed: 4:30  │  │  └────────────────────────────────────┘  │
│  └────────────────┘  │                                          │
│                      │  CUE HISTORY (time-series chart)         │
│  DEVICE STATUS       │  ┌────────────────────────────────────┐  │
│  ┌────────────────┐  │  │  ─── lamp states                   │  │
│  │ 🟢 Ardour      │  │  │  ─── lighting states               │  │
│  │ 🟢 Lamp        │  │  │  ─── projection scenes             │  │
│  │ 🟢 Projection  │  │  │                                    │  │
│  │ 🟢 Lighting    │  │  └────────────────────────────────────┘  │
│  │ 🟢 Conductor   │  │                                          │
│  └────────────────┘  │  ACTIVE ALARMS                           │
│                      │  ┌────────────────────────────────────┐  │
│  LAMP TELEMETRY      │  │ (none)                             │  │
│  ┌────────────────┐  │  └────────────────────────────────────┘  │
│  │ State: ARROGANT│  │                                          │
│  │ Energy: ███░ .7│  │                                          │
│  │ Speed:  ██░░ .5│  │                                          │
│  │ Range:  ████ 1 │  │                                          │
│  └────────────────┘  │                                          │
├──────────────────────┴──────────────────────────────────────────┤
│  SHOW HISTORY (last 10 shows)                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ #10  2026-04-12 20:00  COMPLETE  9:15  15/15 cues         │  │
│  │ #9   2026-04-12 14:30  ABORTED   3:22  7/15 cues          │  │
│  │ ...                                                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Setup (Future Implementation)

### Phase 1: ThingsBoard Account + Devices

1. Sign up at https://thingsboard.cloud (free tier)
2. Create Asset: "Pixstars Show" (type: Show)
3. Create 5 Devices with profiles (see Entity Model above)
4. Note each device's **Access Token** for MQTT authentication

### Phase 2: Telemetry Bridge

1. Install `paho-mqtt` in the Pixstars venv
2. Create `thingsboard/telemetry_bridge.py`
3. Configure device access tokens in `thingsboard/config.py`
4. Add MQTT publishing to the conductor's cue dispatch loop
5. Test: run conductor, verify telemetry appears in ThingsBoard

### Phase 3: Dashboard

1. Create "Pixstars Show Monitor" dashboard in ThingsBoard
2. Add widgets: show status, device connectivity, timeline progress
3. Add time-series charts for lamp energy/speed, cue history
4. Add alarm table widget

### Phase 4: Alarm Rules

1. Configure alarm rules on each Device Profile (see above)
2. Set up Notification Centre: email/push for CRITICAL alarms
3. Test: disconnect a device during show, verify alarm fires

### Phase 5: Home Assistant Bridge

1. Configure HA → ThingsBoard MQTT bridge (see `home_assistant/` docs)
2. Add HA entities as ThingsBoard devices
3. Unified dashboard: show devices + venue automation on one screen

---

## MQTT Topics Reference (Home Assistant Bridge)

These topics are already defined in `home_assistant/pixstars_ha_bridge.py`:

| Topic | Direction | Purpose |
|-------|-----------|---------|
| `pixstars/show/start` | HA → Conductor | Start the show |
| `pixstars/show/pause` | HA → Conductor | Pause the show |
| `pixstars/show/abort` | HA → Conductor | Emergency stop |
| `pixstars/show/blackout` | HA → Conductor | Full blackout |
| `pixstars/lamp/state/set` | HA → Lamp | Override lamp state |
| `pixstars/lamp/reset` | HA → Lamp | Reset lamp to INERT |
| `pixstars/lamp/rehome` | HA → Lamp | Re-home servos |
| `pixstars/lamp/smoke/test` | HA → Lamp | Test smoke effect |
| `pixstars/projection/logo/set` | HA → Projection | Set projection scene |
| `pixstars/projection/clear` | HA → Projection | Clear projection |

---

## 15 Show Cues (Timeline Reference)

| # | Time | Cue Name | Ardour | Lamp | Projection | Lighting |
|---|------|----------|--------|------|------------|----------|
| 1 | 0:00 | SHOW_START | play | INERT | BLACKOUT | BLACKOUT |
| 2 | 0:05 | GNR_LOGO | — | — | GNR_LOGO | ROCKSTAR |
| 3 | 0:12 | LAMP_ON | — | FUNCTIONAL | — | LAMP_ONLY |
| 4 | 1:00 | DRUMS_BEGIN | — | CURIOUS | — | ROCKSTAR |
| 5 | 2:00 | SCENE_TRANSFORM_WALT | — | CURIOUS | DISNEY_CASTLE | DISNEY_SOFT |
| 6 | 3:10 | MICKEY_DRAWING | — | PLEASED | MICKEY_DRAWING | — |
| 7 | 4:30 | AI_ITERATION | — | ARROGANT | AI_ITERATIONS | AI_COLD |
| 8 | 5:40 | OVERHEATING | — | OVERHEATING | — | OVERHEAT |
| 9 | 6:20 | LAMP_DEATH | — | DYING | — | DEATH |
| 10 | 6:25 | LAMP_DEAD | — | DEAD | BLACKOUT | — |
| 11 | 7:40 | REVEAL_AI | — | WEAK | AI_SIGNATURE | REBIRTH |
| 12 | 8:00 | REVEAL_WALT | — | LEARNING | WALT_SIGNATURE | — |
| 13 | 8:10 | REVEAL_AXEL | — | REBORN | AXEL_SIGNATURE | — |
| 14 | 8:20 | TEAM_ROCKSTARS | — | CELEBRATE | TEAM_ROCKSTARS | FINALE |
| 15 | 9:15 | SHOW_END | stop | OFF | BLACKOUT | BLACKOUT |

---

## Files To Create (When Implementing)

```
thingsboard/
├── config.py                  # Device access tokens, MQTT broker settings
├── telemetry_bridge.py        # OSC → MQTT bridge for ThingsBoard
├── device_profiles/           # ThingsBoard device profile JSON exports
│   ├── ardour_daw.json
│   ├── jess_lamp.json
│   ├── projection_display.json
│   ├── dmx_lighting.json
│   └── show_conductor.json
└── dashboards/
    └── show_monitor.json      # ThingsBoard dashboard JSON export
```

---

## Resources

- ThingsBoard website: https://thingsboard.io
- ThingsBoard Cloud (free tier): https://thingsboard.io/installations
- ThingsBoard docs: https://thingsboard.io/docs
- ThingsBoard MQTT API: https://thingsboard.io/docs/reference/mqtt-api
- AI Solution Creator: https://thingsboard.io/blog/ai-solution-creator
- Luxo Jr. ThingsBoard series: https://github.com/vanHeemstraPublications/dev-to/blob/main/articles/luxo_jr_thingsboard_series/
