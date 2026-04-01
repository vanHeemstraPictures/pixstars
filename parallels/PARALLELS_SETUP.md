# PIXSTARS — Parallels Virtualization Setup
## Running Home Assistant and Control Infrastructure on Mac Mini M-Series

This document describes how to run the Pixstars orchestration stack using Parallels Desktop on macOS (Apple Silicon), specifically targeting:

- Mac Mini M4 Pro
- macOS (Apple Silicon)
- Parallels Desktop
- Home Assistant OS (ARM / AArch64)

This virtualization layer hosts:

- Home Assistant
- MQTT Broker
- Show supervision
- Safety automations
- Rehearsal control dashboard

For Home Assistant configuration details see:

home_assistant/HOME_ASSISTANT_SETUP.md


---------------------------------------------------------------------
1. ARCHITECTURE OVERVIEW
---------------------------------------------------------------------

Mac Mini M4 Pro

- Ardour (audio timeline)
- DigiScore (cue timeline)
- Jess+ (AI lamp control)
- Python bridge
- Projection software

Parallels VM
    Home Assistant OS
        MQTT broker
        Automation engine
        Dashboard UI
        Safety monitoring


The Mac runs real-time show control, while Home Assistant supervises:

- lamp safety
- emergency stop
- lighting triggers
- rehearsal controls
- telemetry
- manual override


---------------------------------------------------------------------
2. REQUIREMENTS
---------------------------------------------------------------------

Hardware:
- Mac Mini M-series (M1 / M2 / M3 / M4)
- 16GB RAM recommended (8GB minimum)
- SSD recommended

Software:
- Parallels Desktop (Apple Silicon version)
- Home Assistant OS (Generic AArch64)


---------------------------------------------------------------------
3. DOWNLOAD HOME ASSISTANT OS (ARM)
---------------------------------------------------------------------

Download:

https://www.home-assistant.io/installation/alternative

Choose:

Generic AArch64

File:

haos_generic-aarch64-*.img.xz

Extract:

xz -d haos_generic-aarch64-*.img.xz

You now have:

haos_generic-aarch64.img


---------------------------------------------------------------------
4. CREATE PARALLELS VIRTUAL MACHINE
---------------------------------------------------------------------

Open Parallels Desktop

Create new VM:

New → Install from image file
Select:

haos_generic-aarch64.img

Configure:

CPU:
4 cores (recommended)

Memory:
8 GB recommended
4 GB minimum

Disk:
32 GB minimum
64 GB recommended

Network:
Bridged network (IMPORTANT)

Bridged networking allows:

- Mac → Home Assistant
- Home Assistant → Lamp controller
- DigiScore → MQTT
- Tablet → Dashboard


---------------------------------------------------------------------
5. BOOT HOME ASSISTANT
---------------------------------------------------------------------

Start VM

Wait ~2 minutes

Then open:

http://homeassistant.local:8123

or

http://<VM-IP>:8123

Complete onboarding.


---------------------------------------------------------------------
6. INSTALL REQUIRED ADD-ONS
---------------------------------------------------------------------

Install inside Home Assistant:

Mosquitto MQTT Broker

Settings → Add-ons → Install:
Mosquitto Broker

Start and enable auto-start.


File Editor

Used to edit YAML:
File Editor


Terminal (optional)

For debugging:
Terminal & SSH


---------------------------------------------------------------------
7. MQTT TOPICS USED BY PIXSTARS
---------------------------------------------------------------------

pixstars/show/start
pixstars/show/abort
pixstars/show/blackout
pixstars/lamp/state/set
pixstars/lamp/temp/motor
pixstars/lamp/temp/controller
pixstars/lamp/stall
pixstars/lamp/smoke


---------------------------------------------------------------------
8. PERFORMANCE SETTINGS (IMPORTANT FOR LIVE SHOW)
---------------------------------------------------------------------

Parallels settings:

Performance Mode:
High Performance

Disable:
Pause VM when inactive

Disable:
Automatic resource management

Disable:
Sleep when Mac sleeps

This ensures:

- no audio jitter
- no cue delays
- deterministic timing


---------------------------------------------------------------------
9. RECOMMENDED CPU ALLOCATION
---------------------------------------------------------------------

Mac Mini M4 Pro:

VM CPU: 4 cores
Host remaining: rest for Ardour + DigiScore

Home Assistant uses:
~2% CPU
~500MB RAM


---------------------------------------------------------------------
10. NETWORK LAYOUT
---------------------------------------------------------------------

Mac Mini
- DigiScore
- Ardour
- Jess+
- Python Bridge

Parallels VM
    Home Assistant
        MQTT Broker
            ESP32 Lamp Controller (WiFi)

All communication via MQTT.


---------------------------------------------------------------------
11. WHY VIRTUALIZATION IS USED
---------------------------------------------------------------------

Advantages:

- isolation from show software
- restart without affecting audio
- stable environment
- easy backup snapshot
- dashboard on tablet
- safety supervision


---------------------------------------------------------------------
12. SNAPSHOT BEFORE PERFORMANCE
---------------------------------------------------------------------

Create snapshot:

Pixstars_Show_Ready

If anything breaks:
Restore snapshot instantly.


---------------------------------------------------------------------
13. BOOT ORDER BEFORE SHOW
---------------------------------------------------------------------

1. Start Mac Mini
2. Start Parallels VM
3. Wait for Home Assistant
4. Start MQTT broker
5. Start DigiScore
6. Start Ardour
7. Start Jess+
8. Power lamp controller
9. Open HA dashboard
10. Arm show


---------------------------------------------------------------------
14. TABLET CONTROL
---------------------------------------------------------------------

Open dashboard on tablet:

http://homeassistant.local:8123

You now have:

- start show
- abort show
- blackout
- rehearse lamp states
- temperature monitoring
- smoke trigger
- emergency stop


---------------------------------------------------------------------
15. BACKUP STRATEGY
---------------------------------------------------------------------

Backup recommended:

Home Assistant full backup

Store in:
pixstars/backups/

Also backup:
Parallels VM image


---------------------------------------------------------------------
16. OPTIONAL: RUN WITHOUT PARALLELS
---------------------------------------------------------------------

Alternative setups:

- Raspberry Pi
- Docker on macOS
- Intel NUC backstage
- Home Assistant Yellow

Parallels is preferred during development.


---------------------------------------------------------------------
17. INTEGRATION WITH PIXSTARS
---------------------------------------------------------------------

This VM hosts:

- show supervision
- safety automation
- telemetry
- rehearsal controls
- manual override

Real-time choreography remains in:

- DigiScore
- Jess+
- Ardour

Home Assistant is the stage supervisor.


---------------------------------------------------------------------
18. SUMMARY
---------------------------------------------------------------------

Parallels VM runs:

- Home Assistant OS (ARM)
- MQTT broker
- Pixstars dashboard
- Safety automation

Mac Mini runs:

- Audio
- Lighting cues
- Lamp choreography
- AI behavior

Together they form the full Pixstars control system.
