// DIY turntable driver: TMC2209 + NEMA 17 stepper with GT2 belt friction-drive
// on a 200 mm lazy Susan bearing.
//
// Hardware path (cave ESP32 -> TMC2209 -> NEMA 17):
//   STEP / DIR / ENABLE GPIOs (from config.h) drive a TMC2209 in standalone
//   mode (StealthChop default, 1/16 microstepping set on the driver pins).
//   Pulse generation is offloaded to the ESP32 RMT/MCPWM hardware via the
//   FastAccelStepper library (gin66/FastAccelStepper).
//
// Geometry:
//   200 motor steps/rev x 16 microsteps x ~15.7 belt reduction
//   = 50,240 microsteps per turntable revolution  (~0.00717 deg/microstep)
//
// Hall origin (SS49E / A3144 on TURNTABLE_HALL_PIN):
//   A falling-edge interrupt latches the trigger state. originSeek() drives
//   the table at a configured homing speed and direction; the main loop
//   sees the latched flag, calls forceStopAndNewPosition(0), and zeros the
//   logical position.
//
// All public functions are non-blocking. Call update() every loop tick to
// service the idle-disable timer and homing completion.

#pragma once

#include <Arduino.h>

namespace turntable {

// Mechanics. Override in config.h if the reduction ratio is retuned.
#ifndef TURNTABLE_MOTOR_STEPS_PER_REV
#define TURNTABLE_MOTOR_STEPS_PER_REV 200
#endif
#ifndef TURNTABLE_MICROSTEPS
#define TURNTABLE_MICROSTEPS 16
#endif
// Belt reduction = bearing OD circumference / pulley pitch circumference.
// 200 mm bearing (628.32 mm circumference) / 40 mm 20T GT2 pulley pitch
// circumference = ~15.708. Stored as integer hundredths to keep the math
// in preprocessor-friendly integer terms; the final steps/rev rounds to
// 50,240.
#ifndef TURNTABLE_REDUCTION_X100
#define TURNTABLE_REDUCTION_X100 1570
#endif
// Final microsteps per turntable revolution (compile-time constant).
static constexpr long STEPS_PER_REV =
    (long)TURNTABLE_MOTOR_STEPS_PER_REV *
    (long)TURNTABLE_MICROSTEPS *
    (long)TURNTABLE_REDUCTION_X100 / 100L;

// Default ramp parameters. Speeds are in degrees per second; acceleration
// in degrees per second squared. Conservative defaults keep the friction
// drive engaged without slip; tune from the show control side via
// /turntable/rotate (degrees, speed) calls.
#ifndef TURNTABLE_DEFAULT_SPEED_DPS
#define TURNTABLE_DEFAULT_SPEED_DPS 30.0f
#endif
#ifndef TURNTABLE_DEFAULT_ACCEL_DPS2
#define TURNTABLE_DEFAULT_ACCEL_DPS2 60.0f
#endif
#ifndef TURNTABLE_MIN_SPEED_DPS
#define TURNTABLE_MIN_SPEED_DPS 0.5f
#endif
#ifndef TURNTABLE_MAX_SPEED_DPS
#define TURNTABLE_MAX_SPEED_DPS 360.0f
#endif

// Homing routine speed and seek direction. The hall sensor sits at a
// fixed point on the cave plate; from any unknown position we rotate
// (positive direction by default) until the sensor triggers.
#ifndef TURNTABLE_HOMING_SPEED_DPS
#define TURNTABLE_HOMING_SPEED_DPS 20.0f
#endif
#ifndef TURNTABLE_HOMING_DIR
#define TURNTABLE_HOMING_DIR (+1)
#endif
// Maximum time a homing seek may run before we abort and report failure.
#ifndef TURNTABLE_HOMING_TIMEOUT_MS
#define TURNTABLE_HOMING_TIMEOUT_MS 30000UL
#endif

// Active level of the hall sensor digital line. A3144 (open-drain) and a
// pull-up read HIGH idle, LOW when a magnet is present. Override to HIGH
// if the wiring inverts (e.g. SS49E into a Schmitt buffer).
#ifndef TURNTABLE_HALL_ACTIVE_LEVEL
#define TURNTABLE_HALL_ACTIVE_LEVEL LOW
#endif

// Idle-disable: hold the TMC2209 ENABLE pin HIGH (motor off) after this
// long without any movement, to keep the driver/motor cool and silent
// between cues. Set to 0 to disable the auto-idle entirely.
#ifndef TURNTABLE_IDLE_TIMEOUT_MS
#define TURNTABLE_IDLE_TIMEOUT_MS 5000UL
#endif

// Initialise FastAccelStepper, pins, and hall sensor ISR. Returns true if
// the stepper attached successfully.
bool begin();

// Service idle-disable and homing completion. Call every loop iteration.
void update();

// Relative move: rotate by `degrees` (positive = same direction as
// TURNTABLE_HOMING_DIR). `speedDps` is the cruise speed in degrees per
// second; pass 0 to use the configured default. Returns false if the
// stepper is not initialised.
bool rotate(float degrees, float speedDps);

// Absolute move: travel to `degreesAbs` (signed, relative to origin = 0).
// Same speed semantics as rotate(). The travel direction follows the
// shortest unsigned step delta from the current logical position.
bool gotoAbs(float degreesAbs, float speedDps);

// Begin a homing seek toward the hall sensor at TURNTABLE_HOMING_SPEED_DPS
// in TURNTABLE_HOMING_DIR. Returns immediately; completion is handled by
// the ISR + update(). Returns false if homing is already in progress.
bool originSeek();

// Smooth-stop: ramp down with the current deceleration. Use this for
// emergency stops; it is not a hard hammer stop (which would risk losing
// position).
void stop();

// Current position in degrees, relative to last home (origin = 0). Wraps
// continuously: degrees may grow unbounded as the table rotates.
float currentDegrees();

// True while a move (rotate/gotoAbs/originSeek) is still ramping or running.
bool isRunning();

// True while a homing seek is in flight (not yet triggered or aborted).
bool isHoming();

// True if a previous homing seek triggered successfully since boot.
bool isHomed();

}  // namespace turntable
