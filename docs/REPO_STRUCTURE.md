# Recommended Repository Structure

```text
pixstars/
├── README.md
├── docs/
│   ├── PIXSTARS_LAMP_COMPLETE_BUILD.md
│   ├── REPO_STRUCTURE.md
│   ├── OPERATIONS.md
│   └── TROUBLESHOOTING.md
├── mac/
│   ├── config/
│   │   ├── server.json.example
│   │   └── env.mac.example
│   └── scripts/
│       ├── install_hivemind_server.sh
│       ├── start_hivemind_server.sh
│       └── set_state.sh
├── pi/
│   ├── config/
│   │   ├── mycroft.conf.example
│   │   └── env.pi.example
│   ├── scripts/
│   │   ├── install_pi_satellite.sh
│   │   ├── led_hivemind_states_filewatch.py
│   │   ├── led_hivemind_states.py
│   │   ├── led_test.py
│   │   └── write_state.sh
│   └── systemd/
│       ├── pixstars-lamp-led.service
│       └── pixstars-lamp-sat.service
└── shared/
    └── STATES.md
```

## Why this layout works

- `docs/` keeps design and build decisions visible
- `mac/` keeps server-side concerns isolated
- `pi/` keeps lamp-head concerns isolated
- `shared/` stores small cross-system conventions like state names

## Suggested next additions later

- `voice/` for synthetic voice pipeline
- `ardour/` for show-cue assets
- `home_assistant/` for automation hooks
- `assets/` for wiring diagrams and photos
