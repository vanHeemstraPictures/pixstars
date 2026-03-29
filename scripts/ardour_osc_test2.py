#!/usr/bin/env python3
"""
Pixstars — Ardour OSC Test v2

Tests alternative transport commands to find which one produces audio.
"""

import time
from pythonosc import udp_client

ARDOUR_HOST = "127.0.0.1"
ARDOUR_PORT = 3819

def main():
    client = udp_client.SimpleUDPClient(ARDOUR_HOST, ARDOUR_PORT)

    print("=" * 60)
    print("  PIXSTARS — Ardour OSC Test v2 (finding audio playback)")
    print("=" * 60)
    print()

    # First, make sure we're at the start
    client.send_message("/goto_start", [])
    time.sleep(0.3)

    # Test A: /toggle_roll (equivalent to spacebar)
    print("  [A] /toggle_roll (spacebar equivalent)")
    print("      Playing for 8 seconds (piano starts at ~5s)...")
    client.send_message("/toggle_roll", [])
    time.sleep(8)
    client.send_message("/toggle_roll", [])  # toggle off
    time.sleep(0.5)
    response = input("      Did you hear audio? (y/n): ").strip().lower()
    if response == "y":
        print("      ✅ /toggle_roll works!\n")
        report_result("toggle_roll")
        return

    # Reset
    client.send_message("/goto_start", [])
    time.sleep(0.3)

    # Test B: /transport_play with speed argument
    print("  [B] /transport_play 1.0 (with speed argument)")
    print("      Playing for 8 seconds (piano starts at ~5s)...")
    client.send_message("/transport_play", [1.0])
    time.sleep(8)
    client.send_message("/transport_stop", [])
    time.sleep(0.5)
    response = input("      Did you hear audio? (y/n): ").strip().lower()
    if response == "y":
        print("      ✅ /transport_play 1.0 works!\n")
        report_result("transport_play_with_speed")
        return

    # Reset
    client.send_message("/goto_start", [])
    time.sleep(0.3)

    # Test C: /set_transport_speed 1.0
    print("  [C] /set_transport_speed 1.0")
    print("      Playing for 8 seconds (piano starts at ~5s)...")
    client.send_message("/set_transport_speed", [1.0])
    time.sleep(8)
    client.send_message("/set_transport_speed", [0.0])
    time.sleep(0.5)
    response = input("      Did you hear audio? (y/n): ").strip().lower()
    if response == "y":
        print("      ✅ /set_transport_speed works!\n")
        report_result("set_transport_speed")
        return

    # Reset
    client.send_message("/goto_start", [])
    time.sleep(0.3)

    # Test D: /ardour/transport_play (with prefix)
    print("  [D] /ardour/transport_play (prefixed path)")
    print("      Playing for 8 seconds (piano starts at ~5s)...")
    client.send_message("/ardour/transport_play", [])
    time.sleep(8)
    client.send_message("/ardour/transport_stop", [])
    time.sleep(0.5)
    response = input("      Did you hear audio? (y/n): ").strip().lower()
    if response == "y":
        print("      ✅ /ardour/transport_play works!\n")
        report_result("ardour_prefixed")
        return

    print()
    print("  ❌ None of the commands produced audio.")
    print("  Try: click 'Show Protocol Settings' in Ardour's OSC preferences")
    print("  and check if there's a 'Gain Mode' or 'Transport Mode' setting.")
    print("=" * 60)


def report_result(method: str):
    print("=" * 60)
    print(f"  RESULT: Use '{method}' for transport control")
    print("  Update conductor/ardour_osc.py accordingly.")
    print("=" * 60)


if __name__ == "__main__":
    main()
