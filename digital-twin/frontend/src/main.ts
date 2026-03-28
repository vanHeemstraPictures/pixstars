/**
 * Pixstars Digital Twin — Main Entry Point
 *
 * Initializes BabylonJS, builds the stage, connects to the WebSocket bridge,
 * and runs the render loop with state-driven animation.
 */

import { Engine, Scene } from "@babylonjs/core";
import { createStage } from "./scene/stage";
import { createAnimationState, handleStageEvent, updateScene } from "./scene/animate";
import { StageWebSocket } from "./state/websocket";

// ── Initialize Engine ───────────────────────────────────────────────────────

const canvas = document.getElementById("renderCanvas") as HTMLCanvasElement;
const engine = new Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
const scene = new Scene(engine);

// ── Build Stage ─────────────────────────────────────────────────────────────

const meshes = createStage(scene);
const animState = createAnimationState();

// ── Connect WebSocket ───────────────────────────────────────────────────────

const ws = new StageWebSocket("ws://localhost:8765");
ws.onEvent((event) => {
  handleStageEvent(event, animState);
});
ws.connect();

// ── Render Loop ─────────────────────────────────────────────────────────────

engine.runRenderLoop(() => {
  const dt = engine.getDeltaTime() / 1000; // seconds
  updateScene(meshes, animState, dt);
  scene.render();
});

// ── Resize Handling ─────────────────────────────────────────────────────────

window.addEventListener("resize", () => {
  engine.resize();
});

// ── Debug Info ──────────────────────────────────────────────────────────────

console.log("Pixstars Digital Twin initialized");
console.log(`BabylonJS ${Engine.Version}`);
