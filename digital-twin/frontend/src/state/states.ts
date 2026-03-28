/**
 * Pixstars Digital Twin — State Definitions
 *
 * Mirrors the Python state definitions for lamp, lighting, and projection.
 */

// ── Lamp States ─────────────────────────────────────────────────────────────

export interface LampParams {
  energy: number;   // 0–1
  speed: number;    // 0–1
  range: number;    // 0–1
  jitter: number;   // 0–1
  tiltBias: number; // -1 to +1
}

export const LAMP_STATES: Record<string, LampParams> = {
  INERT:       { energy: 0.0, speed: 0.0, range: 0.0, jitter: 0.0,  tiltBias:  0.0 },
  FUNCTIONAL:  { energy: 0.1, speed: 0.2, range: 0.1, jitter: 0.0,  tiltBias:  0.0 },
  CURIOUS:     { energy: 0.4, speed: 0.3, range: 0.4, jitter: 0.1,  tiltBias:  0.3 },
  DISMISSIVE:  { energy: 0.3, speed: 0.4, range: 0.3, jitter: 0.05, tiltBias: -0.2 },
  PLEASED:     { energy: 0.5, speed: 0.3, range: 0.3, jitter: 0.05, tiltBias:  0.4 },
  ARROGANT:    { energy: 0.7, speed: 0.5, range: 0.5, jitter: 0.1,  tiltBias:  0.6 },
  OVERHEATING: { energy: 0.9, speed: 0.8, range: 0.3, jitter: 0.8,  tiltBias:  0.1 },
  DYING:       { energy: 0.4, speed: 0.2, range: 0.2, jitter: 0.6,  tiltBias: -0.5 },
  DEAD:        { energy: 0.0, speed: 0.0, range: 0.0, jitter: 0.0,  tiltBias: -1.0 },
  WEAK:        { energy: 0.1, speed: 0.1, range: 0.1, jitter: 0.2,  tiltBias: -0.6 },
  REBORN:      { energy: 0.5, speed: 0.3, range: 0.4, jitter: 0.1,  tiltBias:  0.2 },
  LEARNING:    { energy: 0.4, speed: 0.3, range: 0.3, jitter: 0.15, tiltBias:  0.1 },
  CELEBRATE:   { energy: 0.8, speed: 0.6, range: 0.6, jitter: 0.1,  tiltBias:  0.5 },
  OFF:         { energy: 0.0, speed: 0.0, range: 0.0, jitter: 0.0,  tiltBias:  0.0 },
};

// ── Lighting States (DMX → RGB for 3D) ─────────────────────────────────────

export interface LightingParams {
  r: number; g: number; b: number;   // 0–1 (normalized from 0–255)
  intensity: number;                  // 0–1 (from master dimmer)
  strobe: number;                     // 0=off, >0 = strobe speed
}

export const LIGHTING_STATES: Record<string, LightingParams> = {
  BLACKOUT:    { r: 0,    g: 0,    b: 0,    intensity: 0,    strobe: 0 },
  LAMP_ONLY:   { r: 1,    g: 0.78, b: 0.39, intensity: 0.31, strobe: 0 },
  ROCKSTAR:    { r: 1,    g: 0.20, b: 0,    intensity: 1.0,  strobe: 0 },
  DISNEY_SOFT: { r: 0.39, g: 0.47, b: 1,    intensity: 0.71, strobe: 0 },
  AI_COLD:     { r: 0.16, g: 0.71, b: 1,    intensity: 0.78, strobe: 0 },
  OVERHEAT:    { r: 1,    g: 0.31, b: 0,    intensity: 1.0,  strobe: 0.71 },
  DEATH:       { r: 0.31, g: 0,    b: 0.08, intensity: 0.16, strobe: 0 },
  REBIRTH:     { r: 0.78, g: 0.71, b: 0.86, intensity: 0.63, strobe: 0 },
  FINALE:      { r: 1,    g: 0.86, b: 0.71, intensity: 1.0,  strobe: 0 },
};

// ── Projection Scenes (background colors) ───────────────────────────────────

export interface ProjectionParams {
  r: number; g: number; b: number;
  label: string;
}

export const PROJECTION_SCENES: Record<string, ProjectionParams> = {
  BLACKOUT:       { r: 0,    g: 0,    b: 0,    label: "" },
  GNR_LOGO:       { r: 0,    g: 0,    b: 0,    label: "GUNS N' ROSES" },
  DISNEY_CASTLE:  { r: 0.04, g: 0.04, b: 0.12, label: "DISNEY CASTLE" },
  MICKEY_DRAWING: { r: 1,    g: 1,    b: 1,    label: "MICKEY DRAWING" },
  LAMP_DRAWING:   { r: 1,    g: 1,    b: 1,    label: "LAMP DRAWING" },
  AI_ITERATIONS:  { r: 0.08, g: 0.08, b: 0.16, label: "AI ITERATIONS" },
  AI_SIGNATURE:   { r: 0,    g: 0,    b: 0,    label: "A.I." },
  WALT_SIGNATURE: { r: 0,    g: 0,    b: 0,    label: "W.A.L.T." },
  AXEL_SIGNATURE: { r: 0,    g: 0,    b: 0,    label: "A.X.E.L." },
  TEAM_ROCKSTARS: { r: 0,    g: 0,    b: 0,    label: "TEAM ROCKSTARS" },
};
