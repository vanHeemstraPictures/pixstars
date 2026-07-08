# EMQX Agents Evaluation

## Purpose

Evaluate whether EMQX Agents should be used by the Open Engineering Platform as a runtime for event-driven AI behavior.

## Source
```
EMQ webinar: EMQX Agents: From MQTT Events to AI Actions
Date: July 9, 2026
```
EMQ describes EMQX Agents as an event-driven agent runtime on EMQX Cloud that can subscribe to MQTT topics, reason over real-time and historical context, and publish actions back through the broker. (www.emqx.com)

## Summary

EMQX Agents are highly relevant to the Open Engineering Platform.

They turn EMQX from a message broker into a possible runtime for event-driven agents:
```
MQTT Event
  -> Agent Reasoning
  -> MQTT Action
```
This aligns strongly with Open Engineering concepts such as:

* Characters
* Investigations
* Systems
* Capsules
* Observations
* Actions
* Timelines
* Performances
* Connected devices

## Architectural Fit

The Open Engineering Platform should not depend directly on EMQX Agents.

Instead, EMQX Agents should be treated as one possible implementation of a generic Agent Capsule Runtime.
```
Open Engineering Agent Capsule
  -> EMQX Agents
  -> LangGraph
  -> CrewAI
  -> AutoGen
  -> OpenAI Agents
  -> Custom Python Runtime
```
This keeps the Open Engineering Platform open, portable, and independently evolvable.

## Why EMQX Agents Matter

EMQX Agents appear especially useful where AI needs to react to live events.

Examples:
```
sensor/motion/detected
  -> Character Agent
  -> lamp/head/turn
  -> lamp/voice/speak
github/build/failed
  -> Investigation Agent
  -> engineering/investigation/create
  -> engineering/findings/publish
robot/battery/low
  -> System Agent
  -> robot/speech/warn
  -> robot/motion/return_home
```
PixStars Use Case

For PixStars, EMQX Agents could support:

* lamp behavior
* microphone events
* wake-word events
* camera observations
* Home Assistant actions
* projection cues
* light states
* servo commands
* show-control feedback
* safety signals

Possible event loop:
```
pixstars/lamp/observation
  -> EMQX Agent
  -> character reasoning
  -> pixstars/lamp/speech
  -> pixstars/lamp/motion
  -> pixstars/lamp/light
```
This could reduce custom middleware.

Open Engineering Use Case

For Open Engineering, EMQX Agents could support:

* event-driven investigations
* autonomous character behavior
* system monitoring
* workflow automation
* simulation feedback
* AI-assisted operations
* closed-loop engineering actions

EMQ specifically positions the feature around MQTT topics, live events, time-series history, device context, and publishing actions back through EMQX. (www.emqx.com)

Recommended Position

Adopt EMQX Agents as:

A candidate runtime for Open Engineering Agent Capsules.

Do not adopt it as:

The core Agent architecture of Open Engineering.

Proposed Abstraction
```
Agent Capsule
  - subscribes to events
  - receives context
  - reasons over state
  - emits actions
  - records traces
  - exposes decisions
```
Runtime implementations may include:
```
EMQX Agents
LangGraph
CrewAI
AutoGen
OpenAI Agents
Custom Python Services
```
## Benefits

* Strong fit with MQTT-first architecture
* Natural match for IoT, robotics, performance, and Home Assistant
* Reduces custom event-loop services
* Supports closed-loop automation
* Keeps live device data close to reasoning
* Encourages traceable event-driven behavior

## Risks

* EMQX Agents appear tied to EMQX Cloud
* Product maturity is still early
* Runtime portability is uncertain
* Governance model must be evaluated
* Local/offline operation may be limited
* Vendor lock-in is possible if used directly

## Decision

Proceed with exploration.

EMQX Agents should be evaluated as a reference runtime for:
```
architecture/emqx/
capsules/agents/
characters/
investigations/
pixstars/
home_assistant/
```
Next Step

Create a small proof of concept:
```
MQTT topic:
pixstars/lamp/observation
Input:
{
  "event": "audience_noise_detected",
  "level": "high"
}
Agent output:
pixstars/lamp/action
{
  "speech": "I hear you.",
  "light": "warm_pulse",
  "motion": "look_at_audience"
}
```
## Recommendation

EMQX Agents should be added to the Open Engineering technology radar as:
```
Status: Evaluate
Category: Agent Runtime
Scope: Event-driven MQTT AI actions
Strategic relevance: High
Adoption risk: Medium
```
