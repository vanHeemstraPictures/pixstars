"""
OSC Echo Test — verifies localhost OSC send/receive works.

Usage:
    source .venv/bin/activate
    python scripts/osc_test.py

Expected output:
    OSC server listening on 127.0.0.1:9999
    Sending test message...
    Received: /test/ping ['hello', 'pixstars']
    OSC OK
"""

import threading
import time
from pythonosc import osc_server, dispatcher, udp_client


def main():
    test_port = 9999
    received = []

    # Set up dispatcher
    disp = dispatcher.Dispatcher()
    disp.map("/test/ping", lambda addr, *args: received.append((addr, args)))

    # Start server in background thread
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", test_port), disp)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"OSC server listening on 127.0.0.1:{test_port}")

    # Give server time to start
    time.sleep(0.2)

    # Send test message
    client = udp_client.SimpleUDPClient("127.0.0.1", test_port)
    print("Sending test message...")
    client.send_message("/test/ping", ["hello", "pixstars"])

    # Wait for message to arrive
    time.sleep(0.5)

    # Check result
    if received:
        addr, args = received[0]
        print(f"Received: {addr} {list(args)}")
        print("OSC OK")
    else:
        print("ERROR: No message received!")
        exit(1)

    server.shutdown()


if __name__ == "__main__":
    main()
