/**
 * Pixstars Digital Twin — State-Driven Animation
 *
 * Updates the 3D scene based on incoming stage events.
 * Handles smooth transitions (lerping) between states.
 */

import { Color3, StandardMaterial, Vector3 } from "@babylonjs/core";
import type { StageMeshes } from "./stage";
import type { StageEvent } from "../state/websocket";
import { LAMP_STATES, LIGHTING_STATES, PROJECTION_SCENES, type LampParams, type LightingParams } from "../state/states";

interface AnimationState {
  // Current targets (lerped toward)
  lampTarget: LampParams;
  lampCurrent: LampParams;
  lightingTarget: LightingParams;
  lightingCurrent: LightingParams;
  projectionR: number; projectionG: number; projectionB: number;
  projTargetR: number; projTargetG: number; projTargetB: number;
  projectionLabel: string;
  projectionLabelDirty: boolean;

  // Transport
  isPlaying: boolean;

  // Animation timing
  time: number;
  strobePhase: number;
}

export function createAnimationState(): AnimationState {
  const inert = LAMP_STATES["INERT"];
  const blackout = LIGHTING_STATES["BLACKOUT"];
  return {
    lampTarget: { ...inert },
    lampCurrent: { ...inert },
    lightingTarget: { ...blackout },
    lightingCurrent: { ...blackout },
    projectionR: 0, projectionG: 0, projectionB: 0,
    projTargetR: 0, projTargetG: 0, projTargetB: 0,
    projectionLabel: "",
    projectionLabelDirty: true,
    isPlaying: false,
    time: 0,
    strobePhase: 0,
  };
}

export function handleStageEvent(event: StageEvent, state: AnimationState): void {
  switch (event.type) {
    case "lamp": {
      const params = LAMP_STATES[event.value];
      if (params) state.lampTarget = { ...params };
      break;
    }
    case "lighting": {
      const params = LIGHTING_STATES[event.value];
      if (params) state.lightingTarget = { ...params };
      break;
    }
    case "transport": {
      state.isPlaying = event.value === "PLAYING" || event.value === "ROLLING";
      break;
    }
    case "projection": {
      const params = PROJECTION_SCENES[event.value];
      if (params) {
        state.projTargetR = params.r;
        state.projTargetG = params.g;
        state.projTargetB = params.b;
        state.projectionLabel = params.label;
        state.projectionLabelDirty = true;
      }
      break;
    }
  }
}

/**
 * Called every frame to update the 3D scene with smooth transitions.
 */
export function updateScene(
  meshes: StageMeshes,
  state: AnimationState,
  deltaTime: number,
): void {
  state.time += deltaTime;
  const lerpSpeed = 3.0 * deltaTime; // smooth transition speed

  // ── Lerp lamp parameters ──────────────────────────────────────────────
  const lc = state.lampCurrent;
  const lt = state.lampTarget;
  lc.energy   = lerp(lc.energy,   lt.energy,   lerpSpeed);
  lc.speed    = lerp(lc.speed,    lt.speed,    lerpSpeed);
  lc.range    = lerp(lc.range,    lt.range,    lerpSpeed);
  lc.jitter   = lerp(lc.jitter,   lt.jitter,   lerpSpeed);
  lc.tiltBias = lerp(lc.tiltBias, lt.tiltBias, lerpSpeed);

  // ── Animate lamp ──────────────────────────────────────────────────────
  // Head tilt based on tiltBias (-1 = collapsed down, +1 = proud up)
  const baseTilt = -lc.tiltBias * 0.5; // map to rotation range
  const jitterAmount = lc.jitter * 0.15 * Math.sin(state.time * 15 + Math.random() * 0.5);
  const swayAmount = lc.range * 0.2 * Math.sin(state.time * lc.speed * 5);
  meshes.lampHeadPivot.rotation.x = baseTilt + jitterAmount;
  meshes.lampHeadPivot.rotation.z = swayAmount + jitterAmount * 0.5;

  // Bulb glow
  const bulbMat = meshes.lampBulb.material as StandardMaterial;
  const glowIntensity = lc.energy;
  bulbMat.emissiveColor = new Color3(
    glowIntensity * 1.0,
    glowIntensity * 0.95,
    glowIntensity * 0.7,
  );
  meshes.lampBulbLight.intensity = glowIntensity * 1.5;

  // ── Lerp lighting ────────────────────────────────────────────────────
  const llc = state.lightingCurrent;
  const llt = state.lightingTarget;
  llc.r = lerp(llc.r, llt.r, lerpSpeed);
  llc.g = lerp(llc.g, llt.g, lerpSpeed);
  llc.b = lerp(llc.b, llt.b, lerpSpeed);
  llc.intensity = lerp(llc.intensity, llt.intensity, lerpSpeed);
  llc.strobe = lerp(llc.strobe, llt.strobe, lerpSpeed);

  // Apply to spotlights
  let spotIntensity = llc.intensity * 3;

  // Strobe effect
  if (llc.strobe > 0.05) {
    state.strobePhase += deltaTime * llc.strobe * 30;
    const strobeFactor = Math.sin(state.strobePhase) > 0 ? 1 : 0.1;
    spotIntensity *= strobeFactor;
  }

  const spotColor = new Color3(llc.r, llc.g, llc.b);
  meshes.spotLeft.diffuse = spotColor;
  meshes.spotLeft.intensity = spotIntensity;
  meshes.spotRight.diffuse = spotColor;
  meshes.spotRight.intensity = spotIntensity;

  // Update cone visuals
  const coneLMat = meshes.spotConeLeft.material as StandardMaterial;
  const coneRMat = meshes.spotConeRight.material as StandardMaterial;
  const coneColor = new Color3(llc.r * 0.3, llc.g * 0.3, llc.b * 0.3);
  coneLMat.emissiveColor = coneColor;
  coneLMat.alpha = llc.intensity * 0.12;
  coneRMat.emissiveColor = coneColor;
  coneRMat.alpha = llc.intensity * 0.12;

  // ── Lerp projection screen ───────────────────────────────────────────
  state.projectionR = lerp(state.projectionR, state.projTargetR, lerpSpeed);
  state.projectionG = lerp(state.projectionG, state.projTargetG, lerpSpeed);
  state.projectionB = lerp(state.projectionB, state.projTargetB, lerpSpeed);

  // Redraw dynamic texture when scene changes
  if (state.projectionLabelDirty) {
    const tex = meshes.projectionTexture;
    const ctx = tex.getContext();
    const w = tex.getSize().width;
    const h = tex.getSize().height;

    // Background color
    const r = Math.round(state.projTargetR * 255);
    const g = Math.round(state.projTargetG * 255);
    const b = Math.round(state.projTargetB * 255);
    ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
    ctx.fillRect(0, 0, w, h);

    // Text
    if (state.projectionLabel) {
      // Pick contrasting text color
      const brightness = (r + g + b) / 3;
      ctx.fillStyle = brightness > 128 ? "#000000" : "#ffffff";
      ctx.font = "bold 72px Arial";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(state.projectionLabel, w / 2, h / 2);
    }

    tex.update();
    state.projectionLabelDirty = false;
  }

  // Keep emissive glow on the screen material
  meshes.projectionMaterial.emissiveColor = new Color3(
    state.projectionR * 0.8,
    state.projectionG * 0.8,
    state.projectionB * 0.8,
  );

  // ── Performer arms + hands animation ─────────────────────────────
  // Shoulders are fixed. Arms are computed to bridge shoulder→hand.
  const shoulderL = new Vector3(-0.2, 0.95, -0.48);
  const shoulderR = new Vector3(0.2, 0.95, -0.48);
  const speed = 0.08;

  let handLTarget: Vector3;
  let handRTarget: Vector3;

  if (state.isPlaying) {
    // Hands on keys, oscillating left/right across registers
    const spread = Math.sin(state.time * 0.8) * 0.15;
    const flutter = Math.sin(state.time * 3.5) * 0.05;
    handLTarget = new Vector3(-0.2 + spread - flutter, 0.855, -0.1);
    handRTarget = new Vector3(0.2 - spread + flutter, 0.855, -0.1);
  } else {
    // Hands resting in lap
    handLTarget = new Vector3(-0.15, 0.65, -0.35);
    handRTarget = new Vector3(0.15, 0.65, -0.35);
  }

  // Smoothly move hands toward target
  meshes.handL.position = Vector3.Lerp(meshes.handL.position, handLTarget, speed);
  meshes.handR.position = Vector3.Lerp(meshes.handR.position, handRTarget, speed);

  // Compute arm position and rotation to connect shoulder to hand
  // Arm center = midpoint between shoulder and current hand position
  // Arm rotation = angle from shoulder down to hand in the YZ plane
  const hL = meshes.handL.position;
  const hR = meshes.handR.position;

  // Left arm
  const midL = new Vector3(
    (shoulderL.x + hL.x) / 2,
    (shoulderL.y + hL.y) / 2,
    (shoulderL.z + hL.z) / 2
  );
  const dyL = shoulderL.y - hL.y;
  const dzL = hL.z - shoulderL.z;
  const angleL = Math.atan2(dzL, dyL);  // angle from vertical in YZ plane

  meshes.armL.position = Vector3.Lerp(meshes.armL.position, midL, speed);
  meshes.armL.rotation.x = lerp(meshes.armL.rotation.x, angleL, speed);

  // Right arm
  const midR = new Vector3(
    (shoulderR.x + hR.x) / 2,
    (shoulderR.y + hR.y) / 2,
    (shoulderR.z + hR.z) / 2
  );
  const dyR = shoulderR.y - hR.y;
  const dzR = hR.z - shoulderR.z;
  const angleR = Math.atan2(dzR, dyR);

  meshes.armR.position = Vector3.Lerp(meshes.armR.position, midR, speed);
  meshes.armR.rotation.x = lerp(meshes.armR.rotation.x, angleR, speed);
}

function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * Math.min(t, 1);
}
