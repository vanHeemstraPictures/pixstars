#!/usr/bin/env python3
"""
Pixstars — Ardour OSC Connection Test

Tests that Ardour is listening on port 3819 and responds to OSC commands.
Make sure Ardour is running with OSC enabled before running this script.

Usage:
    source .venv/bin/activate
    python scripts/ardour_osc_test.py
"""

import time
from pythonosc import udp_client

ARDOUR_HOST = "127.0.0.1"
ARDOUR_PORT = 3819

def main():
    print("=" * 60)
    print("  PIXSTARS — Ardour OSC Connection Test")
    print(f"  Target: {ARDOUR_HOST}:{ARDOUR_PORT}")
    print("=" * 60)
    print()

    client = udp_client.SimpleUDPClient(ARDOUR_HOST, ARDOUR_PORT)

    # Test 1: Go to start
    print("  [1] Sending /goto_start ...")
    client.send_message("/goto_start", [])
    time.sleep(0.5)
    print("      → Check Ardour: playhead should be at the start")
    input("      Press ENTER to continue...")

    # Test 2: Transport play
    print("  [2] Sending /transport_play ...")
    client.send_message("/transport_play", [])
    time.sleep(2)
    print("      → Check Ardour: should be PLAYING for 2 seconds")

    # Test 3: Transport stop
    print("  [3] Sending /transport_stop ...")
    client.send_message("/transport_stop", [])
    time.sleep(0.5)
    print("      → Check Ardour: should have STOPPED")
    input("      Press ENTER to continue...")

    # Test 4: Go to start again
    print("  [4] Sending /goto_start ...")
    client.send_message("/goto_start", [])
    time.sleep(0.5)

    # Test 5: Locate to 60 seconds (at 48kHz = 2,880,000 samples)
    print("  [5] Sending /locate to 60 seconds (sample 2880000) ...")
    client.send_message("/locate", [2880000, 0])  # 0 = don't roll
    time.sleep(0.5)
    print("      → Check Ardour: playhead should be at ~1:00")
    input("      Press ENTER to continue...")

    # Test 6: Locate to 0 and play
    print("  [6] Sending /goto_start + /transport_play ...")
    client.send_message("/goto_start", [])
    time.sleep(0.3)
    client.send_message("/transport_play", [])
    time.sleep(3)
    client.send_message("/transport_stop", [])
    print("      → Check Ardour: should have played from start for 3 seconds")

    print()
    print("=" * 60)

    response = input("  Did Ardour respond to all commands? (y/n): ").strip().lower()
    if response == "y":
        print("  ✅ Ardour OSC connection VERIFIED!")
    else:
        print("  ❌ Something didn't work. Check:")
        print("     - Ardour is running with a session open")
        print("     - OSC is enabled (Ardour9 → Preferences → Control Surfaces)")
        print("     - Port is 3819 (default)")
        print("     - No firewall blocking localhost UDP")

    print("=" * 60)


if __name__ == "__main__":
    main()
