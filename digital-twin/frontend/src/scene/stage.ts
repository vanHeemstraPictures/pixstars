/**
 * Pixstars Digital Twin — 3D Stage Scene
 *
 * Builds the complete stage with:
 * - Stage floor + rear wall
 * - Projection screen (on rear wall)
 * - Roland keyboard on a stand (center stage)
 * - Pixar-style desk lamp on top of keyboard
 * - Two overhead spotlights (left/right, angled at keyboard)
 * - Performer silhouette (seated behind keyboard)
 */

import {
  Scene,
  Engine,
  ArcRotateCamera,
  Vector3,
  Color3,
  Color4,
  HemisphericLight,
  MeshBuilder,
  StandardMaterial,
  SpotLight,
  PointLight,
  GlowLayer,
  Mesh,
  TransformNode,
  DynamicTexture,
} from "@babylonjs/core";

export interface StageMeshes {
  // Lamp parts (for animation)
  lampBase: Mesh;
  lampLowerArm: Mesh;
  lampUpperArm: Mesh;
  lampHead: Mesh;
  lampBulb: Mesh;
  lampBulbLight: PointLight;
  lampPivot: TransformNode;
  lampHeadPivot: TransformNode;

  // Spotlights
  spotLeft: SpotLight;
  spotRight: SpotLight;
  spotConeLeft: Mesh;
  spotConeRight: Mesh;

  // Projection screen
  projectionScreen: Mesh;
  projectionMaterial: StandardMaterial;
  projectionTexture: DynamicTexture;

  // Stage
  floor: Mesh;
  rearWall: Mesh;

  // Performer arms and hands (for animation)
  armL: Mesh;
  armR: Mesh;
  handL: Mesh;
  handR: Mesh;

  // Glow
  glowLayer: GlowLayer;
}

export function createStage(scene: Scene): StageMeshes {
  // ── Background ────────────────────────────────────────────────────────
  scene.clearColor = new Color4(0.02, 0.02, 0.05, 1);

  // ── Ambient Light (low fill) ──────────────────────────────────────────
  const ambient = new HemisphericLight("ambient", new Vector3(0, 1, 0), scene);
  ambient.intensity = 0.15;
  ambient.diffuse = new Color3(0.4, 0.4, 0.5);

  // ── Glow Layer ────────────────────────────────────────────────────────
  const glowLayer = new GlowLayer("glow", scene, { blurKernelSize: 32 });
  glowLayer.intensity = 0.6;

  // ── Camera (audience perspective) ─────────────────────────────────────
  const camera = new ArcRotateCamera("camera", Math.PI / 2, Math.PI / 2.1, 10, new Vector3(0, 1.0, -1.0), scene);
  camera.lowerRadiusLimit = 3;
  camera.upperRadiusLimit = 20;
  camera.lowerBetaLimit = 0.2;
  camera.upperBetaLimit = Math.PI / 2.1;
  camera.attachControl(scene.getEngine().getRenderingCanvas(), true);

  // ── Materials ─────────────────────────────────────────────────────────
  const darkFloor = new StandardMaterial("darkFloor", scene);
  darkFloor.diffuseColor = new Color3(0.08, 0.08, 0.08);
  darkFloor.specularColor = new Color3(0.05, 0.05, 0.05);

  const wallMat = new StandardMaterial("wallMat", scene);
  wallMat.diffuseColor = new Color3(0.1, 0.1, 0.12);

  const keyboardMat = new StandardMaterial("keyboardMat", scene);
  keyboardMat.diffuseColor = new Color3(0.15, 0.15, 0.15);
  keyboardMat.specularColor = new Color3(0.3, 0.3, 0.3);

  const keysMat = new StandardMaterial("keysMat", scene);
  keysMat.diffuseColor = new Color3(0.9, 0.9, 0.85);

  const standMat = new StandardMaterial("standMat", scene);
  standMat.diffuseColor = new Color3(0.2, 0.2, 0.2);

  const lampMat = new StandardMaterial("lampMat", scene);
  lampMat.diffuseColor = new Color3(0.3, 0.3, 0.3);
  lampMat.specularColor = new Color3(0.5, 0.5, 0.5);

  const lampHeadMat = new StandardMaterial("lampHeadMat", scene);
  lampHeadMat.diffuseColor = new Color3(0.25, 0.25, 0.25);

  const bulbMat = new StandardMaterial("bulbMat", scene);
  bulbMat.diffuseColor = new Color3(1, 0.95, 0.7);
  bulbMat.emissiveColor = new Color3(0, 0, 0); // controlled by state

  const screenTexture = new DynamicTexture("screenTexture", { width: 1024, height: 640 }, scene, false);
  const screenMat = new StandardMaterial("screenMat", scene);
  screenMat.diffuseTexture = screenTexture;
  screenMat.emissiveTexture = screenTexture;
  screenMat.specularColor = new Color3(0, 0, 0);

  const performerMat = new StandardMaterial("performerMat", scene);
  performerMat.diffuseColor = new Color3(0.08, 0.08, 0.08);
  performerMat.alpha = 0.7;

  // ── Stage Floor ───────────────────────────────────────────────────────
  const floor = MeshBuilder.CreateGround("floor", { width: 10, height: 8 }, scene);
  floor.material = darkFloor;
  floor.receiveShadows = true;

  // ── Rear Wall ─────────────────────────────────────────────────────────
  const rearWall = MeshBuilder.CreatePlane("rearWall", { width: 10, height: 4 }, scene);
  rearWall.position = new Vector3(0, 2.0, -4);
  rearWall.material = wallMat;

  // ── Projection Screen (on rear wall) ──────────────────────────────────
  const projectionScreen = MeshBuilder.CreatePlane("projScreen", { width: 3.5, height: 2 }, scene);
  projectionScreen.position = new Vector3(0, 2.0, -3.95);
  projectionScreen.rotation.y = Math.PI;
  projectionScreen.material = screenMat;
  screenMat.backFaceCulling = false;

  // ── Keyboard Stand ────────────────────────────────────────────────────
  // Two vertical legs
  const legL = MeshBuilder.CreateBox("legL", { width: 0.05, height: 0.75, depth: 0.4 }, scene);
  legL.position = new Vector3(-0.55, 0.375, 0);
  legL.material = standMat;

  const legR = MeshBuilder.CreateBox("legR", { width: 0.05, height: 0.75, depth: 0.4 }, scene);
  legR.position = new Vector3(0.55, 0.375, 0);
  legR.material = standMat;

  // Cross bar
  const crossBar = MeshBuilder.CreateBox("crossBar", { width: 1.15, height: 0.03, depth: 0.03 }, scene);
  crossBar.position = new Vector3(0, 0.3, 0);
  crossBar.material = standMat;

  // ── Roland Keyboard ───────────────────────────────────────────────────
  const keyboard = MeshBuilder.CreateBox("keyboard", { width: 1.2, height: 0.08, depth: 0.35 }, scene);
  keyboard.position = new Vector3(0, 0.79, 0);
  keyboard.material = keyboardMat;

  // White keys area (visual)
  const keys = MeshBuilder.CreateBox("keys", { width: 1.1, height: 0.01, depth: 0.12 }, scene);
  keys.position = new Vector3(0, 0.84, -0.1);
  keys.material = keysMat;

  // ── Pixar-style Desk Lamp (articulated hierarchy) ────────────────────
  // Hierarchy: lampPivot → base → lowerJoint → lowerArm → upperJoint → upperArm → head + bulb
  // Each joint pivot sits at the connection point so rotations look natural.

  // Root pivot on the keyboard (left side from audience)
  const lampPivot = new TransformNode("lampPivot", scene);
  lampPivot.position = new Vector3(-0.35, 0.83, 0.05);

  // Base (flat cylinder, sits on keyboard)
  const lampBase = MeshBuilder.CreateCylinder("lampBase", { height: 0.04, diameter: 0.15 }, scene);
  lampBase.material = lampMat;
  lampBase.parent = lampPivot;
  lampBase.position = new Vector3(0, 0.02, 0);

  // Lower joint (pivot at top of base)
  const lowerJoint = new TransformNode("lowerJoint", scene);
  lowerJoint.parent = lampPivot;
  lowerJoint.position = new Vector3(0, 0.04, 0);
  lowerJoint.rotation.z = -0.4;  // lean toward center of keyboard
  lowerJoint.rotation.x = 0.15;  // lean slightly toward keys

  // Lower arm (cylinder with origin at bottom, so it extends upward from the joint)
  const lampLowerArm = MeshBuilder.CreateCylinder("lampLowerArm", {
    height: 0.25, diameterTop: 0.025, diameterBottom: 0.03
  }, scene);
  lampLowerArm.material = lampMat;
  lampLowerArm.parent = lowerJoint;
  lampLowerArm.position = new Vector3(0, 0.125, 0); // half height up from joint

  // Head pivot / upper joint (at top of lower arm)
  const lampHeadPivot = new TransformNode("lampHeadPivot", scene);
  lampHeadPivot.parent = lowerJoint;
  lampHeadPivot.position = new Vector3(0, 0.25, 0); // top of lower arm
  lampHeadPivot.rotation.z = 0.3;  // bend back slightly to arc over keyboard
  lampHeadPivot.rotation.x = 0.2;  // tilt toward keys

  // Upper arm (extends from upper joint)
  const lampUpperArm = MeshBuilder.CreateCylinder("lampUpperArm", {
    height: 0.2, diameterTop: 0.02, diameterBottom: 0.025
  }, scene);
  lampUpperArm.material = lampMat;
  lampUpperArm.parent = lampHeadPivot;
  lampUpperArm.position = new Vector3(0, 0.1, 0); // half height up from joint

  // Lamp head (cone/shade, at top of upper arm)
  const lampHead = MeshBuilder.CreateCylinder("lampHead", {
    height: 0.08, diameterTop: 0.03, diameterBottom: 0.12
  }, scene);
  lampHead.material = lampHeadMat;
  lampHead.parent = lampHeadPivot;
  lampHead.position = new Vector3(0, 0.22, 0);
  lampHead.rotation.x = 0.8; // angled down at keys

  // Bulb (inside head)
  const lampBulb = MeshBuilder.CreateSphere("lampBulb", { diameter: 0.04 }, scene);
  lampBulb.material = bulbMat;
  lampBulb.parent = lampHeadPivot;
  lampBulb.position = new Vector3(0, 0.20, 0);

  // Bulb light
  const lampBulbLight = new PointLight("lampBulbLight", new Vector3(0, 0, 0), scene);
  lampBulbLight.parent = lampBulb;
  lampBulbLight.diffuse = new Color3(1, 0.95, 0.7);
  lampBulbLight.intensity = 0;
  lampBulbLight.range = 2;

  // ── Two Stage Spotlights ──────────────────────────────────────────────
  // Upper-left spotlight
  const spotLeft = new SpotLight(
    "spotLeft",
    new Vector3(-2.5, 4, 1.5),    // upper-left
    new Vector3(0.5, -0.8, -0.3).normalize(), // aimed at keyboard
    Math.PI / 4,
    2,
    scene
  );
  spotLeft.diffuse = new Color3(1, 0.2, 0); // ROCKSTAR default
  spotLeft.intensity = 0;

  // Visible cone for left spot
  const spotConeLeft = MeshBuilder.CreateCylinder("spotConeL", {
    height: 3.5, diameterTop: 0.1, diameterBottom: 2.2
  }, scene);
  const coneLMat = new StandardMaterial("coneLMat", scene);
  coneLMat.diffuseColor = new Color3(1, 0.2, 0);
  coneLMat.emissiveColor = new Color3(0.3, 0.06, 0);
  coneLMat.alpha = 0.08;
  spotConeLeft.material = coneLMat;
  spotConeLeft.position = new Vector3(-2.5, 2.3, 1.5);
  spotConeLeft.rotation = new Vector3(0.35, 0, 0.45);

  // Upper-right spotlight
  const spotRight = new SpotLight(
    "spotRight",
    new Vector3(2.5, 4, 1.5),     // upper-right
    new Vector3(-0.5, -0.8, -0.3).normalize(),
    Math.PI / 4,
    2,
    scene
  );
  spotRight.diffuse = new Color3(1, 0.2, 0);
  spotRight.intensity = 0;

  // Visible cone for right spot
  const spotConeRight = MeshBuilder.CreateCylinder("spotConeR", {
    height: 3.5, diameterTop: 0.1, diameterBottom: 2.2
  }, scene);
  const coneRMat = new StandardMaterial("coneRMat", scene);
  coneRMat.diffuseColor = new Color3(1, 0.2, 0);
  coneRMat.emissiveColor = new Color3(0.3, 0.06, 0);
  coneRMat.alpha = 0.08;
  spotConeRight.material = coneRMat;
  spotConeRight.position = new Vector3(2.5, 2.3, 1.5);
  spotConeRight.rotation = new Vector3(0.35, 0, -0.45);

  // Spotlight fixtures (small boxes)
  const fixtureL = MeshBuilder.CreateBox("fixtureL", { width: 0.3, height: 0.15, depth: 0.2 }, scene);
  fixtureL.position = new Vector3(-2.5, 4, 1.5);
  fixtureL.material = standMat;

  const fixtureR = MeshBuilder.CreateBox("fixtureR", { width: 0.3, height: 0.15, depth: 0.2 }, scene);
  fixtureR.position = new Vector3(2.5, 4, 1.5);
  fixtureR.material = standMat;

  // ── Performer Silhouette (seated at keyboard) ────────────────────────
  // Piano bench
  const bench = MeshBuilder.CreateBox("bench", { width: 0.6, height: 0.05, depth: 0.3 }, scene);
  bench.position = new Vector3(0, 0.55, -0.5);
  bench.material = performerMat;
  const benchLegL = MeshBuilder.CreateCylinder("benchLegL", { height: 0.55, diameter: 0.04 }, scene);
  benchLegL.position = new Vector3(-0.25, 0.275, -0.5);
  benchLegL.material = performerMat;
  const benchLegR = MeshBuilder.CreateCylinder("benchLegR", { height: 0.55, diameter: 0.04 }, scene);
  benchLegR.position = new Vector3(0.25, 0.275, -0.5);
  benchLegR.material = performerMat;

  // Torso (seated upright on bench)
  const torso = MeshBuilder.CreateCylinder("torso", { height: 0.5, diameter: 0.3 }, scene);
  torso.position = new Vector3(0, 1.05, -0.5);
  torso.material = performerMat;

  // Head
  const head = MeshBuilder.CreateSphere("head", { diameter: 0.22 }, scene);
  head.position = new Vector3(0, 1.45, -0.5);
  head.material = performerMat;

  // Upper legs (thighs — horizontal, going forward toward keyboard)
  const thighL = MeshBuilder.CreateCylinder("thighL", { height: 0.4, diameter: 0.1 }, scene);
  thighL.position = new Vector3(-0.12, 0.6, -0.3);
  thighL.rotation.x = Math.PI / 2;
  thighL.material = performerMat;
  const thighR = MeshBuilder.CreateCylinder("thighR", { height: 0.4, diameter: 0.1 }, scene);
  thighR.position = new Vector3(0.12, 0.6, -0.3);
  thighR.rotation.x = Math.PI / 2;
  thighR.material = performerMat;

  // Lower legs (vertical, going down from knee)
  const shinL = MeshBuilder.CreateCylinder("shinL", { height: 0.45, diameter: 0.08 }, scene);
  shinL.position = new Vector3(-0.12, 0.35, -0.1);
  shinL.material = performerMat;
  const shinR = MeshBuilder.CreateCylinder("shinR", { height: 0.45, diameter: 0.08 }, scene);
  shinR.position = new Vector3(0.12, 0.35, -0.1);
  shinR.material = performerMat;

  // Arms (reaching forward toward keyboard keys at Y=0.84, Z=-0.1)
  const armL = MeshBuilder.CreateCylinder("armL", { height: 0.35, diameter: 0.06 }, scene);
  armL.position = new Vector3(-0.2, 0.92, -0.3);
  armL.rotation.x = Math.PI / 2.5;
  armL.material = performerMat;
  const armR = MeshBuilder.CreateCylinder("armR", { height: 0.35, diameter: 0.06 }, scene);
  armR.position = new Vector3(0.2, 0.92, -0.3);
  armR.rotation.x = Math.PI / 2.5;
  armR.material = performerMat;

  // Hands (start in lap, animate to keys when playing)
  const handMat = new StandardMaterial("handMat", scene);
  handMat.diffuseColor = new Color3(0.15, 0.12, 0.1);
  handMat.alpha = 0.85;

  const handL = MeshBuilder.CreateBox("handL", { width: 0.12, height: 0.04, depth: 0.08 }, scene);
  handL.position = new Vector3(-0.15, 0.65, -0.35);
  handL.material = handMat;
  const handR = MeshBuilder.CreateBox("handR", { width: 0.12, height: 0.04, depth: 0.08 }, scene);
  handR.position = new Vector3(0.15, 0.65, -0.35);
  handR.material = handMat;

  return {
    lampBase,
    lampLowerArm,
    lampUpperArm,
    lampHead,
    lampBulb,
    lampBulbLight,
    lampPivot,
    lampHeadPivot,
    projectionScreen,
    projectionMaterial: screenMat,
    projectionTexture: screenTexture,
    armL,
    armR,
    handL,
    handR,
    spotLeft,
    spotRight,
    spotConeLeft,
    spotConeRight,
    floor,
    rearWall,
    glowLayer,
  };
}
