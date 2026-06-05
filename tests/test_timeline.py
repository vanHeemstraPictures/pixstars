"""Tests for the Show Conductor timeline loading and cue dispatching."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

import subprocess

from conductor.main import (
    load_timeline,
    format_time,
    _dispatch_cue,
    _RehearsalArdourOSC,
)
from conductor.osc_sender import OSCSender
from conductor.ardour_osc import ArdourOSC


class TestTimelineLoading(unittest.TestCase):
    """Test timeline YAML loading and validation."""

    def test_load_default_timeline(self):
        """Default timeline.yaml loads without errors."""
        cues = load_timeline("conductor/timeline.yaml")
        self.assertIsInstance(cues, list)
        self.assertGreater(len(cues), 0)

    def test_cues_sorted_by_time(self):
        """Cues are returned sorted by time."""
        cues = load_timeline("conductor/timeline.yaml")
        times = [c["time"] for c in cues]
        self.assertEqual(times, sorted(times))

    def test_all_cues_have_required_fields(self):
        """Every cue has at least 'time' and 'name'."""
        cues = load_timeline("conductor/timeline.yaml")
        for cue in cues:
            self.assertIn("time", cue)
            self.assertIn("name", cue)
            self.assertIsInstance(cue["time"], (int, float))
            self.assertIsInstance(cue["name"], str)

    def test_first_cue_is_show_start(self):
        """First cue should be SHOW_START at time 0."""
        cues = load_timeline("conductor/timeline.yaml")
        self.assertEqual(cues[0]["name"], "SHOW_START")
        self.assertEqual(cues[0]["time"], 0.0)

    def test_last_cue_is_show_end(self):
        """Last cue should be SHOW_END."""
        cues = load_timeline("conductor/timeline.yaml")
        self.assertEqual(cues[-1]["name"], "SHOW_END")

    def test_show_duration_is_reasonable(self):
        """Show should be roughly 9 minutes (within 5-15 min range)."""
        cues = load_timeline("conductor/timeline.yaml")
        duration = cues[-1]["time"]
        self.assertGreater(duration, 300)   # > 5 min
        self.assertLess(duration, 900)      # < 15 min

    def test_total_cue_count_at_least_90(self):
        """Screenplay-aligned timeline should have >= 90 cues."""
        cues = load_timeline("conductor/timeline.yaml")
        self.assertGreaterEqual(len(cues), 90)

    def test_every_act_1_to_10_has_cues(self):
        """Every act from 1 through 10 must have at least one cue."""
        cues = load_timeline("conductor/timeline.yaml")
        acts_present = {c.get("act") for c in cues if "act" in c}
        for act in range(1, 11):
            self.assertIn(act, acts_present,
                          f"Act {act} has no cues in timeline")

    def test_cave_commands_have_valid_structure(self):
        """Each cave sub-command must have a 'cmd' field and required params."""
        cues = load_timeline("conductor/timeline.yaml")
        required_params = {
            "servo": {"ch", "angle"},
            "servo_speed": {"ch", "speed"},
            "head_nod": {"angle"},
            "led_rear": {"r", "g", "b"},
            "led_front": {"r", "g", "b"},
            "turntable_rotate": {"degrees", "speed"},
            "turntable_goto": {"degrees", "speed"},
            "turntable_origin": set(),
            "turntable_stop": set(),
            "ping": set(),
        }
        for cue in cues:
            if "cave" not in cue or not cue["cave"]:
                continue
            self.assertIsInstance(cue["cave"], list,
                                  f"cue {cue['name']} cave must be list")
            for sub in cue["cave"]:
                self.assertIn("cmd", sub,
                              f"cue {cue['name']} cave entry missing cmd")
                cmd = sub["cmd"]
                self.assertIn(cmd, required_params,
                              f"cue {cue['name']} unknown cave cmd: {cmd}")
                for param in required_params[cmd]:
                    self.assertIn(param, sub,
                                  f"cue {cue['name']} cave cmd {cmd} "
                                  f"missing param {param}")

    def test_laser_placeholders_present(self):
        """Laser placeholder cues are present for acts 5, 9, and 10."""
        cues = load_timeline("conductor/timeline.yaml")
        laser_cues = [c for c in cues if "laser" in c and c["laser"]]
        self.assertGreaterEqual(len(laser_cues), 4)
        # Each laser cue has a cmd
        for cue in laser_cues:
            self.assertIn("cmd", cue["laser"])
            self.assertTrue(cue["laser"]["cmd"].startswith("LASER_"))


class TestFormatTime(unittest.TestCase):
    """Test time formatting utility."""

    def test_zero(self):
        self.assertEqual(format_time(0), "00:00.00")

    def test_seconds(self):
        self.assertEqual(format_time(30), "00:30.00")

    def test_minutes(self):
        self.assertEqual(format_time(125), "02:05.00")

    def test_fractional(self):
        self.assertEqual(format_time(90.5), "01:30.50")


class TestOSCSender(unittest.TestCase):
    """Test OSC sender in dry-run mode."""

    def test_dry_run_does_not_create_clients(self):
        sender = OSCSender(dry_run=True)
        self.assertEqual(len(sender.clients), 0)

    def test_dry_run_send_prints(self):
        sender = OSCSender(dry_run=True)
        # Should not raise
        sender.send("lamp", "/lamp/state", "CURIOUS")
        sender.lamp_state("CURIOUS")
        sender.projection_scene("GNR_LOGO")
        sender.lighting_state("BLACKOUT")
        sender.ardour_play()
        sender.ardour_stop()


class TestArdourOSC(unittest.TestCase):
    """Test Ardour OSC command interface."""

    def setUp(self):
        self.sender = OSCSender(dry_run=True)
        self.ardour = ArdourOSC(self.sender)

    def test_process_cue_play(self):
        """transport_play command is processed."""
        self.ardour.process_cue({"command": "transport_play"})

    def test_process_cue_stop(self):
        """transport_stop command is processed."""
        self.ardour.process_cue({"command": "transport_stop"})

    def test_process_cue_locate(self):
        """locate command converts seconds to samples."""
        self.ardour.process_cue({"command": "locate", "seconds": 60.0})

    def test_locate_seconds_calculation(self):
        """Verify sample calculation: 1 second = SAMPLE_RATE samples."""
        sender = MagicMock()
        ardour = ArdourOSC(sender)
        ardour.locate_seconds(1.0)
        sender.ardour_locate.assert_called_once_with(48000, 1)

    def test_locate_seconds_no_roll(self):
        """Locate with roll=False passes 0."""
        sender = MagicMock()
        ardour = ArdourOSC(sender)
        ardour.locate_seconds(2.0, roll=False)
        sender.ardour_locate.assert_called_once_with(96000, 0)


class TestCueDispatching(unittest.TestCase):
    """Test that cues dispatch to correct subsystems."""

    def test_full_cue_dispatches_all(self):
        """A cue with all fields dispatches to all subsystems."""
        sender = MagicMock(spec=OSCSender)
        sender._ardour_rolling = False
        ardour = MagicMock(spec=ArdourOSC)

        cue = {
            "time": 0.0,
            "name": "SHOW_START",
            "lamp": "INERT",
            "projection": "BLACKOUT",
            "lighting": "BLACKOUT",
            "ardour": {"command": "transport_play"},
        }

        _dispatch_cue(cue, 0, 1, sender, ardour)

        ardour.process_cue.assert_called_once_with({"command": "transport_play"})
        sender.lamp_state.assert_called_once_with("INERT")
        sender.projection_scene.assert_called_once_with("BLACKOUT")
        sender.lighting_state.assert_called_once_with("BLACKOUT")

    def test_partial_cue_dispatches_only_present(self):
        """A cue with only lamp field only dispatches lamp."""
        sender = MagicMock(spec=OSCSender)
        sender._ardour_rolling = False
        ardour = MagicMock(spec=ArdourOSC)

        cue = {
            "time": 190.0,
            "name": "MICKEY_DRAWING",
            "lamp": "PLEASED",
            "projection": "MICKEY_DRAWING",
        }

        _dispatch_cue(cue, 0, 1, sender, ardour)

        sender.lamp_state.assert_called_once_with("PLEASED")
        sender.projection_scene.assert_called_once_with("MICKEY_DRAWING")
        ardour.process_cue.assert_not_called()
        sender.lighting_state.assert_not_called()


class TestOSCSenderCaveMethods(unittest.TestCase):
    """Test the cave OSC convenience methods send the correct messages.

    Patches udp_client.SimpleUDPClient so the sender constructs mock UDP
    clients and we can inspect send_message calls.
    """

    def setUp(self):
        patcher = patch("conductor.osc_sender.udp_client.SimpleUDPClient")
        self.mock_client_cls = patcher.start()
        self.addCleanup(patcher.stop)
        # Return a fresh MagicMock for each constructor call so each
        # subsystem client (ardour, lamp, cave, projection, lighting, twin)
        # is independently inspectable.
        self.mock_client_cls.side_effect = lambda *a, **kw: MagicMock()
        self.sender = OSCSender(dry_run=False)
        self.cave_client = self.sender.clients["cave"]
        self.twin_client = self.sender.clients["twin"]

    def test_cave_servo_sends_correct_message(self):
        self.sender.cave_servo(1, 90)
        self.cave_client.send_message.assert_called_once_with(
            "/servo/set", [1, 90]
        )

    def test_cave_head_nod_sends_correct_message(self):
        self.sender.cave_head_nod(150)
        self.cave_client.send_message.assert_called_once_with(
            "/head/nod", [150.0]
        )

    def test_cave_head_nod_with_speed(self):
        self.sender.cave_head_nod(140, speed=50)
        self.cave_client.send_message.assert_called_once_with(
            "/head/nod", [140.0, 50]
        )

    def test_cave_led_rear_sends_correct_message(self):
        self.sender.cave_led_rear(255, 180, 60, "solid")
        self.cave_client.send_message.assert_called_once_with(
            "/led/rear", [255, 180, 60, "solid"]
        )

    def test_cave_led_rear_default_mode(self):
        self.sender.cave_led_rear(10, 20, 30)
        self.cave_client.send_message.assert_called_once_with(
            "/led/rear", [10, 20, 30, "solid"]
        )

    def test_cave_turntable_rotate_sends_correct_message(self):
        self.sender.cave_turntable_rotate(45.0, 10)
        self.cave_client.send_message.assert_called_once_with(
            "/turntable/rotate", [45.0, 10]
        )

    def test_cave_turntable_origin_sends_correct_message(self):
        self.sender.cave_turntable_origin()
        self.cave_client.send_message.assert_called_once_with(
            "/turntable/origin", []
        )


class TestCueDispatchingCaveLaser(unittest.TestCase):
    """Test _dispatch_cue handling of cave and laser fields."""

    def setUp(self):
        self.sender = MagicMock(spec=OSCSender)
        self.sender._ardour_rolling = False
        self.ardour = MagicMock(spec=ArdourOSC)

    def test_cue_with_cave_list_dispatches_all_commands(self):
        """A cue with multiple cave commands dispatches every one."""
        cue = {
            "time": 0.0,
            "name": "SHOW_START",
            "cave": [
                {"cmd": "led_rear", "r": 0, "g": 0, "b": 0, "mode": "off"},
                {"cmd": "head_nod", "angle": 150},
                {"cmd": "servo", "ch": 1, "angle": 90},
                {"cmd": "turntable_origin"},
            ],
        }

        _dispatch_cue(cue, 0, 1, self.sender, self.ardour)

        self.sender.cave_led_rear.assert_called_once_with(0, 0, 0, "off")
        self.sender.cave_head_nod.assert_called_once_with(150)
        self.sender.cave_servo.assert_called_once_with(1, 90)
        self.sender.cave_turntable_origin.assert_called_once_with()

    def test_cue_with_turntable_rotate_passes_args(self):
        """turntable_rotate cmd forwards degrees and speed."""
        cue = {
            "time": 60.0,
            "name": "LAMP_ROTATE",
            "cave": [{"cmd": "turntable_rotate", "degrees": 45, "speed": 10}],
        }
        _dispatch_cue(cue, 0, 1, self.sender, self.ardour)
        self.sender.cave_turntable_rotate.assert_called_once_with(45, 10)

    def test_unknown_cave_command_logs_warning_no_crash(self):
        """Unknown cave cmd prints a warning but does not raise."""
        cue = {
            "time": 0.0,
            "name": "BAD_CUE",
            "cave": [{"cmd": "not_a_real_command", "foo": "bar"}],
        }
        with patch("builtins.print") as mock_print:
            _dispatch_cue(cue, 0, 1, self.sender, self.ardour)
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("CAVE WARNING", printed)
        self.assertIn("not_a_real_command", printed)

    def test_laser_placeholder_logs(self):
        """A cue with a laser field logs the placeholder and does not crash."""
        cue = {
            "time": 210.0,
            "name": "LASER_SWEEP_CUE",
            "laser": {"cmd": "LASER_SWEEP"},
        }
        with patch("builtins.print") as mock_print:
            _dispatch_cue(cue, 0, 1, self.sender, self.ardour)
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("LASER", printed)
        self.assertIn("LASER_SWEEP", printed)

    def test_cue_without_cave_does_not_call_cave_methods(self):
        """Cues without a cave key do not trigger cave dispatch."""
        cue = {"time": 0.0, "name": "PLAIN", "projection": "BLACKOUT"}
        _dispatch_cue(cue, 0, 1, self.sender, self.ardour)
        self.sender.cave_servo.assert_not_called()
        self.sender.cave_head_nod.assert_not_called()
        self.sender.cave_led_rear.assert_not_called()


class TestRehearseMode(unittest.TestCase):
    """Test --rehearse flag plumbing and the no-op Ardour wrapper."""

    def test_rehearse_flag_in_help(self):
        """--rehearse is exposed via the CLI --help output."""
        result = subprocess.run(
            [sys.executable, "-m", "conductor.main", "--help"],
            capture_output=True, text=True,
            cwd=str(Path(__file__).parent.parent),
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--rehearse", result.stdout)

    def test_rehearse_and_dry_run_are_mutually_exclusive(self):
        """Combining --rehearse and --dry-run is rejected by argparse."""
        result = subprocess.run(
            [sys.executable, "-m", "conductor.main",
             "--rehearse", "--dry-run"],
            capture_output=True, text=True,
            cwd=str(Path(__file__).parent.parent),
        )
        self.assertNotEqual(result.returncode, 0)

    def test_rehearsal_ardour_logs_and_skips(self):
        """_RehearsalArdourOSC prints a skipped marker for every cue."""
        rehearsal = _RehearsalArdourOSC()
        with patch("builtins.print") as mock_print:
            rehearsal.process_cue({"command": "transport_play"})
            rehearsal.process_cue({"command": "locate", "seconds": 30.0})
        printed = " ".join(str(c.args[0]) for c in mock_print.call_args_list)
        self.assertIn("REHEARSAL", printed)
        self.assertIn("transport_play", printed)
        self.assertIn("locate", printed)
        self.assertIn("skipped", printed)


if __name__ == "__main__":
    unittest.main()
