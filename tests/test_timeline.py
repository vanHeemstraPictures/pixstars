"""Tests for the Show Conductor timeline loading and cue dispatching."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from conductor.main import load_timeline, format_time, _dispatch_cue
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
        sender.ardour_transport_play()
        sender.ardour_transport_stop()


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


if __name__ == "__main__":
    unittest.main()
