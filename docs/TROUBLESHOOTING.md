# Troubleshooting

## Pi not reachable
- confirm Wi-Fi credentials
- confirm same network as Mac Mini
- try router IP lookup
- try SSH by IP instead of `.local`

## No microphone
- run `arecord -l`
- run `lsusb`
- try a simpler USB microphone

## No speaker output
- run `aplay -l`
- run `speaker-test -c 2 -t wav`
- check powered speaker volume

## LED ring does not light
- confirm GPIO18 data line
- confirm 5V and GND
- run `python led_test.py`

## HiveMind pairing fails
- regenerate client credentials
- confirm host and port
- confirm `_identity.json` exists
- confirm server is listening

## Wake word not recognized
- confirm model path
- test with a more distinctive phrase first
- reduce room noise
- verify the wake-word plugin is installed

## Speaking light does not follow audio
- confirm the state changes to `speaking`
- confirm the audio callback receives signal
- start with fixed brightness, then re-enable dynamic mode
