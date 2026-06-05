// TMC2209 turntable driver. See turntable.h for architecture overview.

#include "turntable.h"

#include <FastAccelStepper.h>

#if __has_include("config.h")
#include "config.h"
#endif

#ifndef TURNTABLE_STEP_PIN
#define TURNTABLE_STEP_PIN    4
#endif
#ifndef TURNTABLE_DIR_PIN
#define TURNTABLE_DIR_PIN     5
#endif
#ifndef TURNTABLE_ENABLE_PIN
#define TURNTABLE_ENABLE_PIN  6
#endif
#ifndef TURNTABLE_HALL_PIN
#define TURNTABLE_HALL_PIN    7
#endif

namespace turntable {

static FastAccelStepperEngine engine = FastAccelStepperEngine();
static FastAccelStepper *stepper = nullptr;

static volatile bool hallTriggered = false;
static bool homing = false;
static bool homed = false;
static unsigned long homingStartMs = 0;
static unsigned long lastMoveEndMs = 0;
static bool motorEnabled = false;

// Hall ISR -- latch only; the main loop services the stop+zero.
static void IRAM_ATTR onHallTrigger() { hallTriggered = true; }

// Clamp a requested speed (degrees/second) into the configured envelope.
// Pass 0 (or anything <= 0) to fall back to the default cruise speed.
static float clampSpeedDps(float speedDps) {
  if (speedDps <= 0.0f) speedDps = TURNTABLE_DEFAULT_SPEED_DPS;
  if (speedDps < TURNTABLE_MIN_SPEED_DPS) speedDps = TURNTABLE_MIN_SPEED_DPS;
  if (speedDps > TURNTABLE_MAX_SPEED_DPS) speedDps = TURNTABLE_MAX_SPEED_DPS;
  return speedDps;
}

static long degreesToSteps(float degrees) {
  return (long)((double)degrees * (double)STEPS_PER_REV / 360.0);
}

static float stepsToDegrees(long steps) {
  return (float)((double)steps * 360.0 / (double)STEPS_PER_REV);
}

// Convert degrees/s and degrees/s^2 into the integer steps/s and steps/s^2
// units that FastAccelStepper expects, with a minimum of 1 to avoid the
// library rejecting near-zero values.
static uint32_t dpsToSps(float dps) {
  double sps = (double)dps * (double)STEPS_PER_REV / 360.0;
  if (sps < 1.0) sps = 1.0;
  return (uint32_t)sps;
}

// Push the configured speed/accel into the active stepper. Called before
// every motion command so per-cue overrides take effect immediately.
static void applyMotionParams(float speedDps) {
  if (!stepper) return;
  stepper->setSpeedInHz(dpsToSps(clampSpeedDps(speedDps)));
  stepper->setAcceleration((int32_t)dpsToSps(TURNTABLE_DEFAULT_ACCEL_DPS2));
}

static void ensureEnabled() {
  if (!stepper) return;
  if (!motorEnabled) {
    stepper->enableOutputs();
    motorEnabled = true;
  }
}

bool begin() {
  pinMode(TURNTABLE_HALL_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(TURNTABLE_HALL_PIN),
                  onHallTrigger,
                  TURNTABLE_HALL_ACTIVE_LEVEL == LOW ? FALLING : RISING);

  engine.init();
  stepper = engine.stepperConnectToPin(TURNTABLE_STEP_PIN);
  if (!stepper) {
    Serial.println("[turntable] FastAccelStepper attach failed");
    return false;
  }
  stepper->setDirectionPin(TURNTABLE_DIR_PIN);
  // TMC2209 EN is active-LOW (LOW=motor energised, HIGH=idle). The library
  // takes a (pin, activeLow) pair via the two-argument setEnablePin().
  stepper->setEnablePin(TURNTABLE_ENABLE_PIN, true /* active low */);
  stepper->setAutoEnable(false);  // we drive ENABLE ourselves for idle timeout
  stepper->disableOutputs();
  motorEnabled = false;

  stepper->setSpeedInHz(dpsToSps(TURNTABLE_DEFAULT_SPEED_DPS));
  stepper->setAcceleration((int32_t)dpsToSps(TURNTABLE_DEFAULT_ACCEL_DPS2));

  Serial.printf("[turntable] STEP=%d DIR=%d EN=%d HALL=%d steps/rev=%ld\n",
                TURNTABLE_STEP_PIN, TURNTABLE_DIR_PIN, TURNTABLE_ENABLE_PIN,
                TURNTABLE_HALL_PIN, STEPS_PER_REV);
  return true;
}

bool rotate(float degrees, float speedDps) {
  if (!stepper) return false;
  ensureEnabled();
  applyMotionParams(speedDps);
  long steps = degreesToSteps(degrees);
  stepper->move(steps);
  Serial.printf("[turntable] rotate %.3f deg (%ld steps) @ %.2f dps\n",
                degrees, steps, clampSpeedDps(speedDps));
  return true;
}

bool gotoAbs(float degreesAbs, float speedDps) {
  if (!stepper) return false;
  ensureEnabled();
  applyMotionParams(speedDps);
  long target = degreesToSteps(degreesAbs);
  stepper->moveTo(target);
  Serial.printf("[turntable] goto %.3f deg (target %ld steps) @ %.2f dps\n",
                degreesAbs, target, clampSpeedDps(speedDps));
  return true;
}

bool originSeek() {
  if (!stepper) return false;
  if (homing) {
    Serial.println("[turntable] originSeek: already homing");
    return false;
  }
  ensureEnabled();
  applyMotionParams(TURNTABLE_HOMING_SPEED_DPS);
  hallTriggered = false;
  homing = true;
  homed = false;
  homingStartMs = millis();
  // Move far enough that at least one full revolution is guaranteed to
  // cross the sensor; the ISR latches and update() will halt the move.
  long sweep = (long)TURNTABLE_HOMING_DIR * (STEPS_PER_REV + STEPS_PER_REV / 8);
  stepper->move(sweep);
  Serial.printf("[turntable] origin seek dir=%+d @ %.2f dps\n",
                TURNTABLE_HOMING_DIR, (float)TURNTABLE_HOMING_SPEED_DPS);
  return true;
}

void stop() {
  if (!stepper) return;
  stepper->stopMove();  // smooth decel using the configured acceleration
  homing = false;
  Serial.println("[turntable] stop (decel)");
}

float currentDegrees() {
  if (!stepper) return 0.0f;
  return stepsToDegrees(stepper->getCurrentPosition());
}

bool isRunning() { return stepper && stepper->isRunning(); }
bool isHoming()  { return homing; }
bool isHomed()   { return homed; }

void update() {
  if (!stepper) return;

  // Homing completion: ISR latched -> halt and zero position.
  if (homing && hallTriggered) {
    stepper->forceStopAndNewPosition(0);
    homing = false;
    homed = true;
    hallTriggered = false;
    lastMoveEndMs = millis();
    Serial.println("[turntable] homed (origin = 0)");
  }
  // Homing timeout: abort cleanly if the sensor never fired.
  if (homing && (millis() - homingStartMs > TURNTABLE_HOMING_TIMEOUT_MS)) {
    stepper->stopMove();
    homing = false;
    Serial.println("[turntable] homing timeout, aborting");
  }

  // Idle-disable: hold ENABLE HIGH after the configured quiet period.
  bool running = stepper->isRunning();
  if (running) {
    lastMoveEndMs = millis();
  } else if (motorEnabled && TURNTABLE_IDLE_TIMEOUT_MS > 0 &&
             (millis() - lastMoveEndMs > TURNTABLE_IDLE_TIMEOUT_MS)) {
    stepper->disableOutputs();
    motorEnabled = false;
  }
}

}  // namespace turntable
