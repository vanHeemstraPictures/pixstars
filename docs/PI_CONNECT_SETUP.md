# Raspberry Pi Connect Setup

## What is Raspberry Pi Connect?

Raspberry Pi Connect is a free remote access service from Raspberry Pi that allows youto access your Pi from anywhere in the world via a web browser. It uses a secure relayhosted by Raspberry Pi to establish a connection without needing port forwarding, VPN,or a static IP.

## Pixstars Lamp Device

The Raspberry Pi for the lamp (hostname: `pixstars-lamp`) is registered withRaspberry Pi Connect and can be accessed from a browser at:

[**https://connect.raspberrypi.com/devices/94c572bf-62dd-48f1-a55d-d55db3da1bcf**](https://connect.raspberrypi.com/devices/94c572bf-62dd-48f1-a55d-d55db3da1bcf)

This provides:

- **Remote shell** access from any browser (no SSH client needed)
- **Screen sharing** (if a desktop environment is installed — not applicable for Lite)
- Works from any network, even when the Pi and your computer are on different networks

## When to Use It

| Scenario | Use |
| --- | --- |
| Same local network | SSH: ssh pi@pixstars-lamp.local |
| Different network / on the road | Raspberry Pi Connect (browser) |
| Automated scripts / file transfer | SSH + SCP (local network only) |

## Setup

Raspberry Pi Connect was enabled during the initial flashing via Raspberry Pi Imager.No additional setup is required. The Pi registers itself on first boot.

To manage your devices, sign in at [https://connect.raspberrypi.com](https://connect.raspberrypi.com) with yourRaspberry Pi ID.

## Troubleshooting

If the device shows as offline:

1. Check the Pi is powered on and connected to WiFi
2. SSH in locally and check the service: `sudo systemctl status rpi-connect`
3. Restart if needed: `sudo systemctl restart rpi-connect`

## Security

- Raspberry Pi Connect uses end-to-end encryption
- Access requires your Raspberry Pi ID credentials
- The device URL is not guessable (UUID-based)
- You can revoke access at any time from the Connect dashboard