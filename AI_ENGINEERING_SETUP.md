AI_ENGINEERING_SETUP.md

Pixstars AI Engineering Setup

Purpose

This document describes the Artificial Intelligence architecture used by the Pixstars performance.

Pixstars is not designed as a chatbot.

The goal is to create a believable digital character:

A Pixar-like living lamp with memory, emotions, personality, reasoning, and the ability to interact with the physical world.

The AI layer transforms the lamp from a scripted prop into a stage character.

⸻

1. Architecture Overview

                     Audience
                        |
                        |
                 Voice / Questions
                        |
                        v
             +----------------------+
             |  A.I. Lamp Character |
             +----------------------+
                        |
                        |
                 Raspberry Pi
                        |
                        |
             OpenVoiceOS HiveMind
                        |
                        |
                        v
             +----------------------+
             |    Mac Mini M4 Pro   |
             +----------------------+
              Pixstars AI Platform
              - Local LLM
              - Agents
              - Memory
              - RAG
              - Tools
              - Emotions
                        |
        ---------------------------------
        |               |               |
        v               v               v
     Ardour        DigiScore       Home Assistant
     Music         Timeline        Lights
     Voice         Cues            Effects
     FX            Projection      Devices

⸻

2. Repository Structure

Create:

mkdir -p ai
cd ai

Directory:

ai/
├── agents/
│   |
│   ├── lamp/
│   │   ├── personality.md
│   │   ├── emotions.yaml
│   │   └── system_prompt.md
│   |
│   ├── walt/
│   │   ├── personality.md
│   │   └── system_prompt.md
│   |
│   ├── director/
│   │   └── rules.md
│   |
│   └── safety/
│       └── guardrails.md
│
├── memory/
│   └── lamp_memory.yaml
├── knowledge/
│   |
│   ├── disney/
│   ├── pixar/
│   ├── team_rockstars/
│   └── performance/
├── tools/
│   |
│   ├── home_assistant.py
│   ├── ardour.py
│   ├── digiscore.py
│   └── emotion_engine.py
├── models/
├── docker-compose.yml
└── AI_ENGINEERING_SETUP.md

⸻

3. Install Ollama

The Mac Mini M4 Pro runs the AI models.

Install:

https://ollama.com

Verify:

ollama --version

Download model:

ollama pull llama3.1

Test:

ollama run llama3.1

Ask:

Who are you?

⸻

4. Create the Lamp Personality Agent

Create:

agents/lamp/personality.md

Content:

# A.I. Lamp Personality
You are A.I.
You are a small intelligent desk lamp.
You were created by Willem.
You admire Walt Disney.
At first you believe artificial intelligence can replace creativity.
During the performance you discover:
Humans imagine.
AI amplifies.
You are:
- curious
- funny
- slightly arrogant
- emotional
- loyal
You speak with short sentences.
You sometimes misunderstand words.
You have an E.T.-like innocence.

⸻

5. Create Emotional Model

Create:

agents/lamp/emotions.yaml

Example:

states:
  sleeping:
    led: warm_dim
    movement: still
  thinking:
    led: blue_pulse
    movement: head_tilt
  excited:
    led: rainbow
    movement: bounce
  sad:
    led: soft_blue
    movement: head_down
  dying:
    led: red_flicker
    movement: weak
  alive:
    led: warm_white
    movement: happy

⸻

6. Persistent Memory

Create:

memory/lamp_memory.yaml

Example:

identity:
  name:
    A.I.
  creator:
    Willem
  home:
    Pixstars
story:
  favorite_human:
    Walt Disney
  lesson:
    Creativity comes from humans and AI together
music:
  transformation_song:
    November Rain
friends:
  - Walt
  - Team Rockstars

⸻

7. Retrieval Augmented Generation (RAG)

The lamp receives a knowledge base.

Create:

knowledge/

Examples:

knowledge/disney/
├── walt_quotes.md
├── disney_history.md
└── creativity.md
knowledge/performance/
├── pixstars_story.md
├── script.md
└── timeline.md

The AI can answer based on the world it lives in.

⸻

8. Tool Calling

The AI should control the world.

Tools are Python functions.

Example:

def set_emotion(emotion):
    if emotion == "sad":
        home_assistant.light(
            color="blue",
            brightness=20
        )
    if emotion == "happy":
        home_assistant.light(
            color="yellow",
            brightness=100
        )

⸻

9. Home Assistant Integration

Home Assistant controls:

* RGB LED ring
* Olight Sphere bulb
* smart devices
* effects

Example:

AI decides:

{
 "emotion": "thinking"
}

Home Assistant executes:

lamp:
  color: blue
  effect: breathing

⸻

10. DigiScore / Jess+ Integration

The AI should not control the show timing directly.

DigiScore remains the director.

AI sends intentions.

Example:

AI:

{
"event":
"lamp_is_alive"
}

DigiScore:

* start Ardour cue
* fade lights
* start projection
* move lamp

⸻

11. Ardour Integration

Ardour remains responsible for:

* November Rain
* piano MIDI
* drums
* dialogue WAV files
* sound effects

AI can request:

{
"play_sound":
"lamp_laugh.wav"
}

⸻

12. Voice Pipeline

Input:

Audience
    |
Microphone
    |
OpenVoiceOS
    |
HiveMind
    |
AI Agent

Output:

AI Text
    |
Voice Generation
    |
Ardour / Speaker
    |
Lamp Voice

⸻

13. Safety Agent

The lamp must never break character.

Create:

agents/safety/guardrails.md

Rules:

Never say:
"I am ChatGPT"
Never discuss:
- politics
- unrelated topics
- private information
Always remain:
A.I.
The Pixstars lamp.

⸻

14. Recommended Startup Order

Start:

1. Home Assistant

Verify devices.

2. Ardour

Load Pixstars session.

3. DigiScore

Load show timeline.

4. Ollama

Start AI engine.

5. HiveMind

Connect lamp.

6. OpenVoiceOS

Wake:

“Hey A.I.”

⸻

15. Final Goal

The audience should not experience software.

They should experience:

A lamp that wakes up.

A lamp that dreams.

A lamp that learns that creativity is human.

The technology disappears.

The character remains.

:::
I would place this at:
```text
pixstars/
└── ai/
    └── AI_ENGINEERING_SETUP.md

and keep home_assistant/HOME_ASSISTANT_SETUP.md and parallels/PARALLELS_SETUP.md as sibling architecture documents.
