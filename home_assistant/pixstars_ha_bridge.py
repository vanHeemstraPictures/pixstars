import json
import time

import paho.mqtt.client as mqtt
import serial
from pythonosc.udp_client import SimpleUDPClient


MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883

SERIAL_PORT = "/dev/tty.usbserial-0001"
SERIAL_BAUD = 115200

DIGISCORE_OSC_HOST = "127.0.0.1"
DIGISCORE_OSC_PORT = 9000


ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
osc = SimpleUDPClient(DIGISCORE_OSC_HOST, DIGISCORE_OSC_PORT)


def send_lamp(cmd):
    ser.write((cmd + "\n").encode())
    return ser.readline().decode().strip()


def on_connect(client, userdata, flags, rc):
    client.subscribe("pixstars/#")


def on_message(client, userdata, msg):

    topic = msg.topic
    payload = msg.payload.decode()

    try:
        data = json.loads(payload)
    except:
        data = {}

    if topic == "pixstars/show/start":
        osc.send_message("/show/start", 1)

    elif topic == "pixstars/show/abort":
        osc.send_message("/show/abort", 1)
        send_lamp("BLACKOUT")

    elif topic == "pixstars/show/blackout":
        send_lamp("BLACKOUT")

    elif topic == "pixstars/lamp/reset":
        send_lamp("RESET")

    elif topic == "pixstars/lamp/rehome":
        send_lamp("REHOME")

    elif topic == "pixstars/lamp/state/set":
        state = data["state"]
        send_lamp(f"STATE {state}")

    elif topic == "pixstars/lamp/smoke/test":
        send_lamp("SMOKE ON")
        time.sleep(1)
        send_lamp("SMOKE OFF")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
