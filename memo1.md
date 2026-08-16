# PixStars — Local AI Architecture

Memo: 1  
Status: Vision / Architecture Direction  
Project: PixStars  
Repository: vanHeemstraPictures/pixstars  
Date: 15 August 2026  

⸻

## 1. Executive Summary

PixStars can now incorporate a powerful local Large Language Model as a first-class part of its runtime architecture.

A Qwen3-Coder-30B-A3B-Instruct-4bit model has been successfully run locally on the Mac Mini M4 Pro, served through MLXServe.

This changes an important assumption in the PixStars architecture.

The Mac Mini no longer needs to be considered merely a performance workstation, orchestration machine, or gateway to cloud-hosted artificial intelligence.

It can become the local AI brain of PixStars.

The resulting architectural principle is:

AI improvises; the screenplay conducts.

The PixStars performance remains fundamentally deterministic. Its story beats, dramatic timing, safety constraints, physical limits, music, projections, and critical cues remain under explicit orchestration.

Within those boundaries, however, the lamp character A.I. can perceive, interpret, reason, respond, and improvise using a real locally running AI model.

This creates an unusual alignment between story and implementation:

The character called A.I. is actually powered by artificial intelligence running locally in the theatre.

⸻

## 2. Context

PixStars is an animatronic theatrical performance centered on the relationship between WALT, a human creator, and A.I., an intelligent lamp.

The performance explores creativity, competition, arrogance, fear of replacement, destruction, remorse, and reconciliation.

Its central message is:

AI is not here to replace us. AI is here to find someone. That someone is us.

Until now, PixStars has been designed around several complementary technologies:

* Raspberry Pi-based physical control;
* Dynamixel servos;
* microphones and speakers;
* cameras;
* programmable LEDs;
* MQTT messaging;
* EMQX;
* voice processing;
* character intelligence;
* Ardour-based audio and timeline orchestration;
* projection;
* deterministic stage cues;
* Open Engineering reusable capabilities.

The successful deployment of a capable local LLM on the Mac Mini M4 Pro adds another important component:

local inference.

⸻

## 3. Proven Local AI Capability

The following model has successfully been operated locally:

Qwen3-Coder-30B-A3B-Instruct-4bit

on:
```
Mac Mini M4 Pro
Apple M4 Pro
24 GB unified memory
```
using:

MLXServe

This establishes that local inference is no longer an experimental possibility for PixStars.

It is a working capability.

The next engineering question therefore changes from:

Can PixStars run sufficiently capable AI locally?

to:

How should PixStars safely and artistically exploit local AI?

⸻

## 4. Architectural Principle

The local LLM must not become the performance director.

It becomes an actor.

The distinction is fundamental.
```
Screenplay / Timeline
        │
        │ defines boundaries
        ▼
Character Runtime
        │
        │ requests interpretation
        ▼
Local AI
        │
        │ proposes meaning / response
        ▼
Character Runtime
        │
        │ validates behaviour
        ▼
Performance Actions
```
The AI may interpret and improvise.

The performance system retains authority.

Therefore:

AI improvises; the screenplay conducts.

⸻

## 5. Proposed Runtime Architecture

The high-level architecture becomes:
```
                         PIXSTARS
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
   PHYSICAL CHARACTER                    AI / ORCHESTRATION
   Raspberry Pi Zero 2 WH                Mac Mini M4 Pro
          │                                   │
          │                              ┌────┴────┐
          │                              │MLXServe │
          │                              └────┬────┘
          │                                   │
          │                           Qwen3-Coder-30B
          │                                   │
          │                            Character Runtime
          │                                   │
          └──────────── MQTT / EMQX ──────────┤
                                              │
                         ┌────────────────────┼────────────────────┐
                         │                    │                    │
                     Perception            Memory              Actions
                         │                    │                    │
                         └────────────────────┼────────────────────┘
                                              │
                                      PixStars Timeline
                                              │
                                 Music / Projection / Cues
```
This establishes a useful separation between:

1. physical embodiment;
2. character intelligence;
3. performance orchestration.

⸻

## 6. Raspberry Pi: The Nervous System

The Raspberry Pi in the lamp should primarily operate as the character’s physical nervous system.

Responsibilities may include:

Input

* microphone capture;
* camera capture;
* buttons;
* sensors;
* physical state;
* servo feedback.

Output

* Dynamixel servo movement;
* head nodding and shaking;
* LEDs;
* speaker playback;
* physical effects;
* other future actuators.

The Pi should not need to host the large reasoning model.

Instead, it exchanges structured events and commands with the Mac Mini.

For example:
```
pixstars/perception/speech
pixstars/perception/vision
pixstars/state/servo
pixstars/state/light
pixstars/action/head
pixstars/action/light
pixstars/action/voice
```
The precise MQTT ontology should be defined separately.

⸻

## 7. Mac Mini: The Brain

The Mac Mini M4 Pro becomes the principal computational brain of the performance.

Its responsibilities can include:

* speech-to-text;
* natural-language interpretation;
* scene awareness;
* character reasoning;
* dialogue generation;
* emotional-state interpretation;
* memory retrieval;
* behaviour selection;
* orchestration;
* music playback;
* projection control;
* logging;
* observability.

MLXServe provides access to the locally hosted Qwen model.

Conceptually:
```
Mac Mini M4 Pro
│
├── PixStars Orchestrator
│
├── Character Runtime
│
├── Voice Services
│
├── Memory
│
├── EMQX / MQTT
│
├── MLXServe
│    └── Qwen3-Coder-30B-A3B-Instruct-4bit
│
├── Ardour
│
└── Projection / Stage Services
```
The Mac Mini therefore becomes a local edge AI server for the performance.

⸻

## 8. Local-First AI

PixStars should adopt a local-first inference strategy.
```
Character request
       │
       ▼
Local inference
       │
       ├── success ─────► continue
       │
       └── unavailable
              │
              ▼
        deterministic fallback
```
Cloud inference should not be required for the core performance.

A cloud model may remain useful during development, experimentation, evaluation, or optional non-critical capabilities.

The stage performance itself should be capable of operating without Internet connectivity.

This improves:

* reliability;
* latency;
* privacy;
* reproducibility;
* cost;
* independence from external API availability.

⸻

## 9. The Character Runtime

The LLM should not directly control hardware.

Instead, it should operate behind a Character Runtime.

The Character Runtime represents A.I. as a character rather than as a chatbot.

Conceptually:
```
A.I.
│
├── Identity
├── Personality
├── Emotional State
├── Scene Awareness
├── Perception
├── Dialogue
├── Memory
├── Intent
├── Behaviour
└── Inference
```
The inference component may use:
```
Inference
│
├── Local
│    └── MLXServe
│         └── Qwen3
│
└── Optional External Providers
```
This abstraction is important.

A.I. should not become:

“the Qwen lamp.”

Qwen is an implementation detail behind the character.

Models can therefore be upgraded, replaced, compared, or combined without redefining A.I.’s identity.

⸻

## 10. From Speech to Behaviour

Consider a scene in which WALT has shown A.I. his drawing.

WALT might say:

“Oh come on. It doesn’t look that bad.”

The performance should not depend upon this exact wording.

The pipeline could instead be:
```
WALT speaks
     │
     ▼
Microphone
     │
     ▼
Speech-to-Text
     │
     ▼
Character Runtime
     │
     ▼
Local LLM
     │
     ▼
Structured interpretation
```
For example:
```
{
  "intent": "defend_drawing",
  "emotion": "playful_defensive",
  "scene": "mickey_rejection",
  "confidence": 0.94
}
```
The Character Runtime can then map this interpretation onto permitted actions.
```
defend_drawing
      │
      ▼
A.I. response policy
      │
      ├── shake head
      ├── annoyed light state
      └── sarcastic response
```
The resulting physical commands might become MQTT messages.

The LLM interprets.

The Character Runtime decides what is allowed.

The actuator layer executes.

⸻

## 11. Structured AI Outputs

Free-form LLM output should not directly reach hardware.

Where possible, inference should produce validated structured data.

For example:
```
{
  "scene": "lamp_drawing",
  "speaker": "ai",
  "emotion": "curious",
  "intent": "inspect_drawing",
  "response": "Wait... is that me?",
  "behaviours": [
    "peek",
    "lean_closer"
  ]
}
```
This output should be validated against:

* the current scene;
* permitted behaviours;
* servo limits;
* timing constraints;
* safety rules;
* character rules;
* performance state.

Only validated actions should enter the physical execution system.

⸻

## 12. Scene-Constrained Intelligence

The LLM should always know the current dramatic context.

For example:
```
Scene
  04
Name
  Lamp Drawing
WALT objective
  Recover from having offended A.I.
A.I. emotional state
  Disinterested / suspicious
Allowed transitions
  ignore
  peek
  inspect
  recognize
  become impressed
Forbidden transitions
  leave stage
  skip confrontation
  reveal future events
  address audience
```
The model can therefore improvise inside a dramatic envelope.

This is significantly safer and artistically stronger than unconstrained conversation.

⸻

## 13. Deterministic Story Beats

Several PixStars moments should remain completely deterministic.

These include major narrative events such as:

1. WALT draws A.I. as Mickey Mouse;
2. A.I. rejects the drawing;
3. WALT draws A.I. as a lamp;
4. A.I. secretly becomes interested;
5. A.I. recognizes itself;
6. WALT signs his work;
7. A.I. attempts to outperform WALT;
8. A.I. becomes increasingly excessive;
9. WALT becomes threatened;
10. WALT attempts to switch A.I. off;
11. A.I. survives;
12. power connections are removed;
13. A.I. survives again;
14. the bulb is removed;
15. A.I. apparently dies;
16. WALT experiences remorse;
17. reconciliation occurs;
18. the final message is delivered.

The AI should enrich these events, not replace them.

⸻

## 14. Controlled Improvisation

Between deterministic beats, controlled improvisation can make A.I. feel genuinely alive.

Examples include:

* reacting to slight differences in WALT’s wording;
* varying small verbal responses;
* changing the timing of a suspicious glance;
* expressing irritation differently;
* reacting to unexpected pauses;
* interpreting WALT’s emotional intent;
* remembering something that happened earlier in the performance.

This creates variability without sacrificing narrative structure.

A useful hierarchy is:
```
LEVEL 0 — HARD CUE
Exact behaviour and timing.
LEVEL 1 — PARAMETERIZED CUE
Fixed action with variable intensity/timing.
LEVEL 2 — CHARACTER CHOICE
Choose among approved behaviours.
LEVEL 3 — DIALOGUE IMPROVISATION
Generate language inside strict scene constraints.
LEVEL 4 — FREE IMPROVISATION
Not permitted during the primary performance.
```
Most PixStars AI behaviour should remain within Levels 1–3.

⸻

## 15. The Timeline Remains Supreme

Ardour and the broader PixStars timeline remain crucial.

Music, projection and theatrical timing cannot simply wait indefinitely for an LLM.

The orchestration system therefore remains authoritative.
```
                 PERFORMANCE CLOCK
                        │
                        ▼
                 PixStars Timeline
                        │
          ┌─────────────┼─────────────┐
          │             │             │
        Music       Projection     Character
                                      │
                                      ▼
                                   Local AI
```
The arrow is intentionally downward.

The AI participates in the performance.

It does not own the performance clock.

⸻

16. Timeout and Fallback Behaviour

Every AI-assisted cue should have a deterministic fallback.

For example:

Cue starts
    │
    ▼
Request character response
    │
    ├── response within deadline
    │        │
    │        ▼
    │   validated AI response
    │
    └── timeout
             │
             ▼
       scripted fallback

This ensures that:

* model latency cannot stop the show;
* model failure cannot stop the show;
* MLXServe failure cannot stop the show;
* malformed model output cannot stop the show.

The theatrical principle is simple:

The show must continue even if the AI disappears.

⸻

17. Hardware Safety Boundary

The LLM must never directly specify unrestricted servo positions, velocities, electrical states, or other low-level hardware parameters.

Avoid:

{
  "servo_position": 842,
  "servo_speed": 1000
}

Prefer:

{
  "behaviour": "shake_head",
  "intensity": "annoyed"
}

A deterministic behaviour controller then translates:

shake_head + annoyed

into safe servo commands.

For example:

Character Behaviour
        │
        ▼
Motion Primitive
        │
        ▼
Safety Envelope
        │
        ▼
Dynamixel Command

This is especially important for the AX-12A-driven lampshade mechanism.

⸻

18. MQTT / EMQX as the Nervous-System Bus

MQTT remains an excellent fit for connecting the distributed components.

Conceptually:

Perception
   │
   ▼
 MQTT
   │
   ▼
Character
   │
   ▼
 MQTT
   │
   ▼
Behaviour
   │
   ▼
 MQTT
   │
   ▼
Physical Lamp

EMQX can provide the messaging backbone and potentially host additional intelligent routing or agent capabilities.

This keeps components loosely coupled.

For example, the character system does not need to know whether shake_head is implemented by:

* AX-12A;
* another Dynamixel servo;
* a simulation;
* a future robotics controller.

It publishes intent.

The physical subsystem realizes that intent.

⸻

19. Character Memory

Local inference also makes character memory particularly interesting.

A.I. could maintain short-term performance memory such as:

WALT showed Mickey drawing.
A.I. rejected it.
WALT appeared disappointed.
WALT started another drawing.
A.I. pretended not to care.
A.I. peeked.
A.I. recognized itself.

The model can use this context to maintain emotional continuity.

Memory should nevertheless be separated from inference.

Character
│
├── Memory
│
└── Inference

This prevents the model’s context window from becoming the authoritative system of record.

⸻

20. Observability

Every inference should be observable during development and rehearsals.

Useful records include:

timestamp
scene
input transcript
character state
prompt version
model
inference latency
structured response
validation result
selected behaviour
fallback used

This allows rehearsals to reveal:

* slow responses;
* misunderstood dialogue;
* unsafe suggestions;
* weak prompts;
* unnecessary model calls;
* opportunities for deterministic optimization.

A rehearsal can therefore become an engineering dataset.

⸻

21. Rehearsal Mode

PixStars should eventually support a dedicated rehearsal mode.

For example:

pixstars run --mode rehearsal

Rehearsal mode could record:

* every spoken line;
* every LLM interpretation;
* every generated response;
* every MQTT event;
* every servo movement;
* every timeline cue;
* timing deviations.

This could later be replayed without the physical performance.

Such replayability would greatly improve debugging.

⸻

22. Simulation

Because the AI communicates through semantic behaviours rather than directly controlling hardware, the same character can operate against a simulator.

                 Character Runtime
                        │
                        ▼
                       MQTT
                        │
               ┌────────┴────────┐
               │                 │
             Stage           Simulator
               │                 │
           Real Lamp         Virtual Lamp

This allows development of A.I.’s behaviour without continuously operating the physical mechanism.

⸻

23. Local AI and Voice

The existing voice architecture can now increasingly become local.

A future local pipeline may look like:

Microphone
    │
    ▼
Local VAD
    │
    ▼
Local STT
    │
    ▼
Character Runtime
    │
    ▼
Qwen via MLXServe
    │
    ▼
Local TTS
    │
    ▼
Speaker

This would make the entire conversational loop independent of cloud APIs.

The Raspberry Pi can remain responsible for audio capture and playback while computationally expensive processing occurs on the Mac Mini.

⸻

24. Latency as a Dramatic Tool

AI latency is normally considered purely an engineering problem.

In PixStars it can sometimes become theatrical behaviour.

For example, a 500–1500 ms delay can be represented as:

WALT speaks
     │
     ▼
A.I. freezes
     │
     ▼
small head movement
     │
     ▼
light pulses
     │
     ▼
response

The audience interprets computation time as thinking.

Nevertheless, excessive latency must still trigger deterministic fallback.

Engineering limitations can therefore occasionally become character animation.

⸻

25. Theatrical Significance

There is a particularly compelling consequence of this architecture.

A.I. is no longer merely an animatronic prop pretending to be artificial intelligence.

During the performance:

WALT
  │
  │ speaks
  ▼
A.I.
  │
  │ perceives
  ▼
local artificial intelligence
  │
  │ reasons
  ▼
A.I.
  │
  │ reacts
  ▼
WALT

The theatrical fiction and engineering reality partially coincide.

This can remain invisible to the audience.

They do not need to see:

* Qwen;
* MLXServe;
* prompts;
* MQTT;
* JSON;
* inference logs.

They simply experience a lamp that appears to understand WALT.

⸻

26. The Death of A.I.

This architecture becomes particularly meaningful during the climactic sequence.

WALT attempts to regain control.

A.I. initially survives attempts to disable it.

Eventually WALT removes the bulb.

At this point the Character Runtime can deliberately cease participating.

Qwen
 │
 ▼
Character Runtime
 │
 X
 │
 ▼
digital distortion
servo movement stops
light disappears
voice disappears
MQTT behaviour stops
                 SILENCE

The screenplay takes complete control.

The absence of intelligence becomes part of the performance.

The audience sees the physical character become lifeless.

WALT realizes what he has done.

The technical architecture therefore reinforces the emotional architecture of the story.

⸻

27. Reconciliation

When A.I. eventually returns, its systems can reappear progressively.

For example:

light
  ↓
small movement
  ↓
perception
  ↓
voice
  ↓
character intelligence

Rather than simply switching everything back on simultaneously, restoration can become part of the dramatic language.

The final A.I. may also behave differently from the competitive character seen earlier.

Its emotional state has changed.

So has WALT’s.

The technology serves that transformation.

⸻

28. Relationship to Open Engineering Character

Although PixStars is the immediate implementation, the architecture should not make the Character capability specific to the lamp.

Conceptually:

Character
     │
     ├──────────────┬───────────────┐
     │              │               │
     ▼              ▼               ▼
 PixStars       Detective       Snowy Owl
    A.I.         Character       Character

All may share capabilities such as:

* identity;
* personality;
* memory;
* emotion;
* dialogue;
* perception;
* behaviour;
* inference.

The local inference provider is therefore reusable infrastructure.

PixStars becomes a particularly demanding proving ground for the Character architecture because the character has a physical body.

⸻

29. Separation of Character and Model

One important design rule follows:

A character is not a model.

A.I.’s personality should not live exclusively inside a Qwen system prompt.

Instead:

A.I.
│
├── Character Definition
├── Personality
├── Story Context
├── Memory
├── Behaviour Vocabulary
├── Safety Rules
└── Inference Provider
      │
      └── Qwen3

This permits migration to future models without losing the character.

⸻

30. Development vs Performance

PixStars should distinguish between at least two operating environments.

Development

May allow:

* unrestricted debugging;
* alternative models;
* cloud models;
* verbose logging;
* prompt experimentation;
* generated behaviours;
* experimental integrations.

Performance

Should prioritize:

* local inference;
* known model;
* fixed configuration;
* validated prompts;
* strict behaviour vocabulary;
* deterministic fallbacks;
* predictable latency;
* offline operation.

The performance environment should therefore be treated much more like a production system than an AI playground.

⸻

31. Model Configuration

The Qwen configuration should eventually be version-controlled alongside PixStars runtime configuration.

Relevant parameters may include:

model
quantization
context size
maximum output tokens
temperature
top-p
timeout
prompt version
behaviour schema version

The exact runtime parameters should be determined experimentally.

They should be tuned for performance reliability, rather than maximum model creativity.

⸻

32. Progressive Context Expansion

The current local deployment should be optimized incrementally.

Rather than immediately maximizing context length, development should progressively evaluate:

context
   ↓
memory usage
   ↓
latency
   ↓
response quality
   ↓
performance stability

PixStars does not necessarily require extremely large context windows.

Good architectural memory and scene-state management can often be more valuable than feeding the entire screenplay into every inference request.

⸻

33. Cost Implications

The local inference architecture also reduces recurring operational costs.

Instead of:

performance
   ↓
API request
   ↓
cloud inference
   ↓
per-token cost

PixStars can use:

performance
   ↓
Mac Mini
   ↓
local inference

The Mac Mini is therefore not only a development workstation.

It becomes reusable AI infrastructure.

This can support:

* PixStars;
* Open Engineering development;
* character experiments;
* coding agents;
* local automation;
* future performances.

Cloud AI becomes an optional resource rather than a prerequisite.

⸻

34. Reliability Principle

PixStars should be designed around the following hierarchy:

THE SHOW
   │
   ▼
STORY
   │
   ▼
ORCHESTRATION
   │
   ▼
CHARACTER
   │
   ▼
AI
   │
   ▼
MODEL

Not:

MODEL
  │
  ▼
everything else

This hierarchy protects both engineering reliability and artistic intent.

⸻

35. Proposed Implementation Phases

Phase 1 — Establish Local Inference Service

Formalize the existing working configuration:

Mac Mini
   ↓
MLXServe
   ↓
Qwen3-Coder-30B-A3B-Instruct-4bit

Provide:

* startup;
* shutdown;
* health checking;
* configuration;
* logging.

Phase 2 — Structured Character Interpretation

Introduce a minimal interface:

speech + scene
      ↓
     Qwen
      ↓
structured intent

No hardware control yet.

Phase 3 — Character Behaviour Vocabulary

Define behaviours such as:

look_away
peek
lean_closer
nod
shake_head
hesitate
celebrate
dismiss
freeze
wake
sleep

Phase 4 — MQTT Integration

Translate validated behaviours into MQTT commands.

Phase 5 — Physical Lamp Integration

Connect behaviour primitives to:

* AX-12A movement;
* lighting;
* audio;
* other actuators.

Phase 6 — Timeline Integration

Allow selected screenplay moments to request character interpretation.

Phase 7 — Deterministic Fallbacks

Provide scripted alternatives for every AI-assisted cue.

Phase 8 — Rehearsal Instrumentation

Record:

* inference;
* timing;
* behaviour;
* errors;
* fallbacks.

Phase 9 — Controlled Improvisation

Gradually enable character improvisation within approved scenes.

Phase 10 — Performance Lock

Freeze:

* model;
* configuration;
* prompts;
* schemas;
* behaviour vocabulary;
* timing limits.

Then rehearse the exact production configuration.

⸻

36. Proposed Repository Direction

The PixStars repository can eventually represent this architecture approximately as:

pixstars/
│
├── architecture/
│   ├── ai/
│   ├── character/
│   ├── messaging/
│   ├── robotics/
│   ├── voice/
│   └── orchestration/
│
├── character/
│   └── ai/
│       ├── identity/
│       ├── personality/
│       ├── behaviours/
│       └── prompts/
│
├── inference/
│   ├── mlxserve/
│   └── schemas/
│
├── mqtt/
│
├── robotics/
│
├── screenplay/
│
├── timeline/
│
├── rehearsal/
│
└── simulation/

This is illustrative rather than prescriptive.

Existing repository structure should be respected when implementation begins.

⸻

37. Architectural Decision

PixStars should adopt local AI inference on the Mac Mini M4 Pro as the preferred intelligence provider for the A.I. character.

The current reference implementation is:

Qwen3-Coder-30B-A3B-Instruct-4bit
             │
             ▼
          MLXServe
             │
             ▼
       Mac Mini M4 Pro

The model should sit behind a Character Runtime and must not directly control physical hardware.

The PixStars timeline remains authoritative.

Every AI-dependent theatrical cue must have a deterministic fallback.

Internet connectivity must not be required for the core performance.

⸻

38. Guiding Principles

The implementation should follow these principles:

1. Local first.
2. Character before model.
3. Intent before hardware commands.
4. Structured output before free-form control.
5. Deterministic story, controlled improvisation.
6. Every AI cue has a fallback.
7. The performance clock remains authoritative.
8. Physical safety is enforced outside the LLM.
9. Inference must be observable and replayable.
10. The character survives model replacement.
11. Internet connectivity is optional.
12. AI improvises; the screenplay conducts.

⸻

39. Conclusion

Running Qwen3-Coder-30B-A3B-Instruct-4bit successfully on the Mac Mini M4 Pro represents more than a local-LLM experiment.

For PixStars, it establishes the missing computational foundation for a genuinely intelligent physical character.

The Raspberry Pi can become the lamp’s nervous system.

The Mac Mini can become its brain.

MQTT and EMQX can connect perception, intelligence and physical action.

The Character Runtime can turn model inference into character behaviour.

And the screenplay can remain the conductor that ensures all of those systems serve the story.

The result should not be an LLM demonstration with a lamp attached.

It should be theatre.

The audience should never need to think about tokens, models, MQTT topics, inference servers, context windows, or quantization.

They should see WALT draw something.

They should see a lamp look at it.

They should see the lamp think.

And, for just a moment, they should wonder whether it really understood him.

Because this time, perhaps it did.

AI improvises; the screenplay conducts.
