# Memo 2 — Refactoring PixStars as an Open Engineering Native Application

Status: Proposed  
Project: PixStars  
Repository: vanHeemstraPictures/pixstars  
Date: 2026-08-16  
Subject: Open Engineering adherence, Minikube runtime, local AI, and implementation strategy  

⸻

## 1. Executive Summary

PixStars should be refactored from a largely bespoke robotics/performance system into an Open Engineering native application.

The central architectural principle is:

PixStars owns the performance. Open Engineering owns the reusable engineering capabilities required to perform it.

PixStars should therefore no longer independently implement concepts such as character behaviour, robotics abstractions, voice processing, AI integration, memory, messaging, execution orchestration, or runtime composition where these capabilities can instead be supplied by the Open Engineering ecosystem.

PixStars becomes a composition of Open Engineering capabilities.

The target local runtime will be a Minikube Kubernetes cluster running on the Mac Mini M4 Pro.

The resulting stack becomes:
```
PixStars
    │
    ▼
Open Engineering
    │
    ▼
Kubernetes
    │
    ▼
Minikube
    │
    ▼
Mac Mini M4 Pro
```
Physical devices such as the animatronic lamp remain edge systems connected to this local platform.

Local AI inference, currently provided by MLXServe and Qwen3-Coder-30B-A3B-Instruct-4bit, remains initially outside Minikube as a native macOS service and is exposed to Open Engineering through an AI provider abstraction.

This architecture makes PixStars more than an application.

PixStars becomes a reference implementation and vertical integration test for Open Engineering.

⸻

## 2. Context

PixStars combines several unusually diverse engineering disciplines:

* theatrical performance;
* storytelling;
* intelligent characters;
* robotics;
* servo control;
* voice interaction;
* computer vision;
* AI inference;
* memory;
* lighting;
* audio;
* projection;
* messaging;
* orchestration;
* timeline execution;
* physical computing.

Originally, many of these concerns naturally evolved inside PixStars itself.

Meanwhile, Open Engineering has developed a broader architecture containing concepts such as:

* Kernel capabilities;
* Capsules;
* Operating Systems;
* Picos;
* Definitions;
* Parsers;
* Rules;
* Composers;
* Sandcastles;
* Crossplane;
* Kubernetes;
* federated Systems of Record.

The two architectures have now reached the point where continuing to build equivalent capabilities directly inside PixStars would create unnecessary duplication.

The appropriate next step is therefore architectural convergence.

⸻

## 3. Strategic Decision

PixStars will become an Open Engineering native application.

This means that PixStars may depend on Open Engineering, but Open Engineering must never depend on PixStars.

The dependency direction is:
```
PixStars
    │
    │ uses
    ▼
Open Engineering
```
Never:
```
Open Engineering
    │
    ▼
PixStars
```
Open Engineering must remain completely usable without PixStars.

PixStars is one consumer of the platform.

⸻

## 4. Architectural Principle

The refactoring should continuously ask one question:

Is this capability unique to the PixStars performance, or could another Open Engineering application use it?

If it is reusable, it should normally belong to Open Engineering.

If it defines the artistic identity, story, staging, or particular physical configuration of PixStars, it should remain in PixStars.

For example:

| Concern | Owner |  
| —- | —- |  
| AX-12A servo abstraction | Open Engineering Robotics |  
| generic head movement | Open Engineering Robotics |  
| character emotional state	| Character Capsule |  
| speech recognition | Voice Capsule |  
| AI provider integration | AI Capsule |
| character memory | Memory Capsule |  
| camera perception | Vision Capsule |  
| event semantics | Open Engineering Kernel |  
| execution orchestration | Runner OS |  
| performance semantics	| Star OS |  
| Walt | PixStars |  
| A.I. character definition | PixStars |  
| Mickey Mouse drawing scene | PixStars |  
| lamp arrogance scene | PixStars |  
| bulb removal scene | PixStars |  
| musical score | PixStars |  
| projections | PixStars |  
| exact stage layout | PixStars |  

This boundary should guide the entire migration.

⸻

## 5. Target Architecture

The intended architecture is approximately:
```
Open Engineering Platform
│
├── Kernel
│   ├── Events
│   ├── Messaging
│   ├── Workflow
│   ├── Memory
│   ├── Evidence
│   ├── Execution
│   └── Composition
│
├── Capsules
│   ├── Character
│   ├── Robotics
│   ├── Voice
│   ├── Vision
│   ├── Memory
│   ├── AI
│   ├── Story
│   ├── Simulation
│   └── Documentation
│
├── Operating Systems
│   ├── Star OS
│   └── Runner OS
│
├── Definitions
├── Parsers
├── Rules
├── Composers
├── Sandcastles
└── Runtime
    ├── Kubernetes
    ├── Crossplane
    ├── MQTT / EMQX
    └── edge runtimes
                ▲
                │ consumes
                │
PixStars
│
├── Picos
│   ├── Lamp
│   ├── Walt
│   ├── Stage
│   ├── Audio
│   └── Projection
│
├── Characters
│   ├── WALT
│   └── A.I.
│
├── Story
├── Screenplay
├── Performance
├── Scenes
├── Cues
├── Music
├── Projections
├── Stage
└── Physical Configuration
```
⸻

## 6. Mac Mini M4 Pro as the Local Open Engineering Host

The Mac Mini M4 Pro should become the principal local compute platform for PixStars.

It should no longer merely be regarded as the computer running various supporting applications.

It becomes the local Open Engineering host.

The initial architecture should be:
```
Mac Mini M4 Pro
│
├── macOS
│
├── Minikube
│   │
│   ├── Open Engineering Kernel
│   ├── Star OS
│   ├── Runner OS
│   ├── Character services
│   ├── Voice services
│   ├── Robotics services
│   ├── Memory services
│   ├── AI integration
│   ├── PixStars workloads
│   ├── EMQX
│   └── Crossplane
│
├── MLXServe
│   └── Qwen3-Coder-30B-A3B-Instruct-4bit
│
├── Ardour
│
└── native macOS hardware integrations
```
Minikube therefore becomes the default development and performance Kubernetes environment.

⸻

## 7. Why Minikube

Using Minikube provides several important benefits.

### 7.1 Architectural parity

PixStars begins exercising the same Kubernetes concepts intended for the wider Open Engineering ecosystem.

The architecture stops being theoretical.

⸻

### 7.2 Declarative deployment

Components can increasingly be described rather than manually assembled.

Ultimately, something conceptually similar to this should become possible:
```
apiVersion: open-engineering.io/v1alpha1
kind: Composition
metadata:
  name: pixstars
spec:
  picos:
    - lamp
    - walt
  capsules:
    - character
    - robotics
    - voice
    - vision
    - memory
    - ai
    - story
  operatingSystems:
    - star
    - runner
```
A Composer and Crossplane can progressively turn such declarations into actual runtime resources.

⸻

### 7.3 Isolation

Services can be independently deployed, upgraded, restarted, inspected, and eventually sandboxed.

⸻

### 7.4 Reproducibility

The complete PixStars software environment becomes substantially easier to reproduce.

This is important both for development and for eventual performance deployment.

⸻

### 7.5 Observability

Kubernetes gives us a natural environment for:

* health checks;
* logs;
* metrics;
* service discovery;
* configuration;
* lifecycle management.

This becomes particularly valuable when diagnosing a complex physical performance.

⸻

## 8. Local AI Strategy

Local AI inference has become an important architectural capability.

The Mac Mini M4 Pro can now successfully run:

Qwen3-Coder-30B-A3B-Instruct-4bit

through MLXServe.

This should become an Open Engineering capability rather than a PixStars-specific dependency.

PixStars should therefore never contain logic equivalent to:

call Qwen through MLXServe

Instead:
```
PixStars
    │
    ▼
AI Capsule
    │
    ▼
AI Provider Interface
    │
    ├── Local MLXServe
    │       │
    │       ▼
    │      Qwen
    │
    ├── OpenAI
    ├── Anthropic
    └── future providers
```
PixStars requests reasoning.

Open Engineering determines how that reasoning is provided.

⸻

## 9. Keep MLXServe Outside Kubernetes Initially

MLXServe should initially remain a native macOS service.

This is intentional.

The Mac Mini currently has 24 GB of unified memory, and the local Qwen model already represents a significant workload.

Running MLXServe inside Minikube would initially introduce:

* additional resource management complexity;
* container integration complexity;
* GPU/Metal considerations;
* additional debugging surfaces;
* little immediate architectural benefit.

Therefore:
```
Minikube
    │
    │ HTTP/API
    ▼
MLXServe on macOS
    │
    ▼
Qwen
```
The Open Engineering AI Capsule should abstract this boundary.

Containerizing or Kubernetes-managing local inference can be reconsidered later.

⸻

## 10. The Lamp Becomes a Pico

One of the most important changes is that the physical lamp should be represented as an Open Engineering Pico.

Conceptually:

Pico: pixstars.lamp

The Lamp Pico composes capabilities rather than implementing all of them itself.
```
Lamp Pico
│
├── Character
├── Robotics
├── Voice
├── Vision
├── Memory
└── AI
```
A future declarative definition could resemble:
```
apiVersion: open-engineering.io/v1alpha1
kind: Pico
metadata:
  name: pixstars-lamp
spec:
  character:
    ref: pixstars-ai
  capabilities:
    - robotics
    - voice
    - vision
    - memory
    - ai
  runtime:
    target: lamp
```
The exact API is not yet important.

The architectural separation is.

⸻

## 11. Edge Runtime

Kubernetes should not directly control individual servo movements at low latency.

Physical control should remain close to the hardware.

The architecture should therefore distinguish orchestration from execution.
```
Open Engineering
      │
      │ intent
      ▼
Runner OS
      │
      │ command/event
      ▼
MQTT / EMQX
      │
      ▼
Lamp Edge Runtime
      │
      ▼
Hardware Driver
      │
      ▼
AX-12A
```
For example:

look_down

is a high-level instruction.

The edge runtime translates it into:

* target servo position;
* velocity;
* acceleration;
* movement profile;
* safety constraints.

Kubernetes decides what should happen.

The device runtime determines how it physically happens.

⸻

## 12. Raspberry Pi as Edge Compute

The Raspberry Pi associated with the lamp should therefore evolve toward an Open Engineering edge runtime.

Its responsibilities may include:

* hardware access;
* servo control;
* LED control;
* microphone capture;
* speaker output;
* camera capture;
* local safety logic;
* heartbeat;
* telemetry;
* MQTT communication.

The Pi should remain capable of safely handling hardware even if communication with the Mac temporarily disappears.

This is particularly important for robotics.

⸻

## 13. MQTT / EMQX as the Nervous System

PixStars already has a strong reason to use MQTT.

Under Open Engineering, MQTT/EMQX should become part of the messaging infrastructure connecting:

* Picos;
* Runner OS;
* Star OS;
* edge devices;
* sensors;
* AI;
* robotics;
* performance systems.

Example topics might initially include:
```
pixstars/lamp/heard
pixstars/lamp/thought
pixstars/lamp/emotion
pixstars/lamp/look
pixstars/lamp/nod
pixstars/lamp/light
pixstars/performance/cue
```
However, the semantics of the messages should increasingly derive from the Open Engineering ontology.

That gives us a progression from transport-specific messages toward meaningful engineering events.

For example:
```
Observation
     │
     ▼
Event
     │
     ▼
Messaging
     │
 ┌───┼──────────┐
 ▼   ▼          ▼
AI  Character  Runner
 │     │          │
 └─────┴────┬─────┘
            ▼
         Robotics
            │
            ▼
           Lamp
```
⸻

## 14. Star OS

Star OS should become responsible for the semantics of an intelligent performer.

Responsibilities can include:

* character state;
* emotional state;
* interaction;
* expression;
* presence;
* reaction;
* performance intent;
* character-driven decisions.

For example:

A.I. feels offended

or:

A.I. arrogantly rejects Walt

belongs closer to Star OS and the Character capability than to robotics.

⸻

## 15. Runner OS

Runner OS should be responsible for execution.

Responsibilities include:

* cue execution;
* timing;
* sequencing;
* synchronization;
* retries;
* hardware actions;
* deterministic transitions;
* performance state.

The distinction becomes:
```
Story
   │
   ▼
Star OS
   │
   ▼
Performance Intent
   │
   ▼
Runner OS
   │
   ▼
Execution
   │
   ├── Servo
   ├── Light
   ├── Audio
   ├── Projection
   └── Effects
```
This distinction is particularly important for PixStars.

AI and character behaviour can tolerate some nondeterminism.

A theatrical cue often cannot.

⸻

## 16. Deterministic Core, Intelligent Edge

The live performance should therefore follow an important safety principle:

AI may enrich the performance, but it must not become a single point of failure for the performance.

The essential screenplay and cues should remain executable deterministically.

For example:
```
Performance Timeline
        │
        ├──────── deterministic ────────► Runner OS
        │
        └──────── intelligent ──────────► Star OS / AI
```
If local inference fails during a performance, the core performance should still be capable of continuing.

This distinction will make PixStars considerably more robust.

⸻

## 17. Sandcastles

Open Engineering Sandcastles can provide controlled environments for experimental or autonomous behaviour.

This becomes especially useful for:

* AI-generated actions;
* experimental character logic;
* scripts;
* generated code;
* simulations;
* untrusted automation.

A Sandcastle should define the allowed execution envelope.

The AI can operate within that envelope without gaining unrestricted access to the physical performance environment.

This reinforces the principle:

Automate the envelope while preserving control of the performance.

⸻

## 18. Crossplane

Crossplane should progressively become responsible for composing the Open Engineering resources required by PixStars.

The long-term workflow becomes:
```
PixStars definition
       │
       ▼
Open Engineering Composer
       │
       ▼
Crossplane
       │
       ▼
Kubernetes Resources
       │
       ▼
Minikube
```
Crossplane should not be introduced everywhere simultaneously.

We should first establish a working Minikube deployment and then progressively replace manually deployed resources with compositions.

⸻

## 19. Definitions, Parsers, and Rules

PixStars should also consume the emerging Open Engineering definition infrastructure.

For example:
```
Definition
    │
    ▼
Parser
    │
    ▼
Validated Model
    │
    ▼
Rules
    │
    ▼
Composer
    │
    ▼
Runtime
```
Definitions might eventually exist for:

* Pico;
* Character;
* Robot;
* Servo;
* Sensor;
* Performance;
* Scene;
* Cue;
* Projection;
* Audio channel;
* Stage;
* Capability.

PixStars can become an important real-world consumer that tests whether these abstractions are actually useful.

⸻

## 20. What Must Remain in PixStars

Open Engineering adherence does not mean moving everything out of PixStars.

PixStars remains responsible for its creative identity.

The repository should continue to own things such as:
```
PixStars
│
├── story/
├── screenplay/
├── characters/
├── scenes/
├── performance/
├── cues/
├── music/
├── projections/
├── stage/
├── props/
└── physical-configuration/
```
The following remain unmistakably PixStars:

* Walt;
* A.I.;
* the Mickey Mouse drawing;
* the Lamp drawing;
* the rivalry between Walt and A.I.;
* the artificial intelligence reveal;
* the storm;
* removal of power;
* removal of the bulb;
* A.I.’s apparent death;
* Walt’s remorse;
* reconciliation;
* the yellow bandana;
* the final blackout.

Open Engineering enables these ideas.

It does not own them.

⸻

## 21. Repository Direction

The PixStars repository should gradually move toward a structure such as:
```
pixstars/
│
├── README.md
│
├── memo1.md
├── memo2.md
│
├── architecture/
│   ├── open-engineering/
│   ├── kubernetes/
│   ├── edge/
│   ├── messaging/
│   └── ai/
│
├── compositions/
│   └── pixstars/
│
├── picos/
│   ├── lamp/
│   ├── walt/
│   ├── stage/
│   ├── audio/
│   └── projection/
│
├── characters/
│   ├── ai/
│   └── walt/
│
├── story/
├── screenplay/
├── scenes/
├── cues/
├── music/
├── projections/
├── stage/
├── props/
│
├── deployments/
│   └── minikube/
│
└── tests/
    ├── integration/
    └── performance/
```
This is an intended direction rather than an immediate mandatory restructuring.

⸻

## 22. Implementation Strategy

The refactor should be evolutionary.

We should avoid attempting a complete rewrite.

### Phase 1 — Establish the Local Cluster

Install and validate Minikube on the Mac Mini M4 Pro.

Establish:
```
Mac Mini
    ↓
Minikube
    ↓
PixStars namespace
```
Create initial namespaces such as:
```
open-engineering
pixstars
observability
```
The first objective is simply a reliable local Kubernetes environment.

⸻

### Phase 2 — Deploy Messaging

Deploy EMQX or the selected MQTT infrastructure into Minikube.

Verify communication between:
```
Minikube
    ↕
MQTT
    ↕
Mac
    ↕
Raspberry Pi
```
This establishes the basic nervous system.

⸻

### Phase 3 — Introduce the Lamp Pico

Create the first Open Engineering representation of the Lamp.

Initially it can be deliberately small.

For example:
```
Lamp Pico
    │
    ├── identity
    ├── status
    ├── heartbeat
    └── command interface
```
Then progressively attach capabilities.

⸻

### Phase 4 — Extract Robotics

Move generic robotics concepts away from PixStars-specific code.

Introduce abstractions such as:
```
look-left
look-right
look-up
look-down
nod
shake
home
```
The Lamp maps these actions onto its particular AX-12A hardware.

This creates reusable robotics semantics.

⸻

### Phase 5 — Character Capsule Integration

Represent A.I. as a Character definition.

Separate:

Character Intent

from:

Physical Expression

For example:
```
Character:
    emotion: offended
Expression:
    look-away
Robotics:
    rotate-head(...)
```
This separation will become highly reusable.

⸻

### Phase 6 — AI Provider Abstraction

Expose MLXServe through the Open Engineering AI capability.

The first provider becomes:

local-qwen

with:
```
AI Capsule
    ↓
MLXServe
    ↓
Qwen3
```
PixStars should no longer directly depend on MLXServe.

⸻

### Phase 7 — Runner OS Integration

Move deterministic performance execution into Runner OS.

Represent:

* acts;
* scenes;
* cues;
* timing;
* synchronization;
* actions.

Runner OS becomes capable of running the essential performance without AI.

⸻

### Phase 8 — Star OS Integration

Move intelligent performer behaviour into Star OS.

Star OS can combine:

* Character;
* AI;
* Memory;
* Voice;
* Vision;
* Story context.

This creates the intelligent layer around the deterministic performance.

⸻

### Phase 9 — Crossplane Composition

Once the components work independently, describe them declaratively through Open Engineering resources and Crossplane.

The goal becomes increasingly close to:

kubectl apply -f pixstars.yaml

followed by:
```
PixStars
   ↓
Composer
   ↓
Crossplane
   ↓
Open Engineering resources
   ↓
Minikube
```
⸻

### Phase 10 — Full Performance Validation

Finally run the complete performance through the Open Engineering architecture.

Validate failure scenarios including:

* AI unavailable;
* MQTT interrupted;
* Raspberry Pi disconnected;
* servo unavailable;
* camera unavailable;
* voice unavailable;
* Kubernetes workload restart;
* MLXServe restart;
* network latency.

The deterministic performance should degrade gracefully rather than collapse.

⸻

## 23. Development Mode Versus Performance Mode

PixStars should eventually support at least two runtime profiles.

### Development

pixstars-development

Characteristics:

* verbose logging;
* live reload where appropriate;
* interactive AI;
* debugging interfaces;
* simulations;
* hardware optional.

### Performance

pixstars-performance

Characteristics:

* deterministic;
* preflight validation;
* fixed configuration;
* reduced moving parts;
* controlled AI behaviour;
* health checks;
* automatic recovery;
* predictable fallback behaviour.

Performance mode should prioritize reliability over experimentation.

⸻

## 24. Simulation

The Open Engineering Simulation Capsule should eventually allow PixStars to run without physical hardware.

For example:
```
Lamp Pico
    │
    ├── physical runtime
    │       └── AX-12A
    │
    └── simulated runtime
            └── virtual lamp
```
This would allow development of:

* character behaviour;
* cues;
* messaging;
* AI;
* timelines;
* failure handling;

without continuously operating the physical lamp.

It will also significantly improve automated testing.

⸻

## 25. PixStars as an Open Engineering Reference Application

PixStars should ultimately be presented as an Open Engineering reference implementation for:

Intelligent Character Performance

It demonstrates that Open Engineering can compose:
```
Story
+
Character
+
AI
+
Memory
+
Voice
+
Vision
+
Robotics
+
Messaging
+
Workflow
+
Execution
+
Physical Hardware
```
into one functioning system.

This makes PixStars an unusually powerful validation environment.

⸻

## 26. Architectural Fitness Test

PixStars can therefore serve as an architectural fitness test for Open Engineering.

Whenever Open Engineering introduces an abstraction, we can ask:

Can PixStars actually use it?

If the answer is no, we should investigate whether:

1. PixStars is incorrectly designed;
2. the abstraction is incomplete;
3. the abstraction is too theoretical;
4. another capability is missing.

This creates a productive feedback loop:
```
Open Engineering
       │
       ▼
    PixStars
       │
       ▼
Real physical performance
       │
       ▼
Architectural feedback
       │
       └──────────────► Open Engineering
```
This is not a dependency from Open Engineering to PixStars.

It is architectural validation through a consumer.

⸻

## 27. Definition of Success

The refactor can be considered successful when the following statement becomes true:

A developer can provision the PixStars software environment on the Mac Mini M4 Pro through Open Engineering, connect the physical Lamp edge runtime, start the performance, and execute the complete PixStars story without PixStars itself implementing generic infrastructure already supplied by Open Engineering.

A particularly compelling future command might become:

oe compose pixstars

which ultimately results in:
```
PixStars Composition
        ↓
Open Engineering
        ↓
Crossplane
        ↓
Minikube
        ↓
Mac Mini M4 Pro
        ↓
MQTT / EMQX
        ↓
Edge Runtime
        ↓
Physical Lamp
```
with:
```
Open Engineering AI
        ↓
MLXServe
        ↓
Local Qwen
```
providing local intelligence.

⸻

## 28. Guiding Principle

The most important rule for the implementation is simple:

Do not rebuild Open Engineering inside PixStars.

Whenever we discover a generally reusable capability while developing PixStars:
```
discover
    ↓
generalize
    ↓
move to Open Engineering
    ↓
expose as capability
    ↓
consume from PixStars
```
PixStars should become progressively smaller at the infrastructure level while becoming richer at the creative level.

That is desirable.

Its repository should increasingly describe:

who performs, what happens, when it happens, and why it matters.

Open Engineering should increasingly provide:

how the underlying engineering capabilities make that performance possible.

⸻

## 29. Conclusion

The next generation of PixStars should therefore be built as:

An Open Engineering native intelligent-character performance running on a local Kubernetes environment, using Minikube on the Mac Mini M4 Pro, connected to physical edge hardware, and capable of consuming locally hosted AI.

This architecture aligns PixStars with the wider Open Engineering ecosystem while simultaneously giving Open Engineering something extremely valuable:

a demanding, physical, theatrical, AI-driven system against which its architecture can continuously be tested.

PixStars therefore becomes both:

a performance

and:

a proof that Open Engineering works.
