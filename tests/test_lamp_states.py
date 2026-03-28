"""Tests for the Lamp state definitions and adapter."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lamp.states import get_state, list_states, LampState, LAMP_STATES


class TestLampStates(unittest.TestCase):
    """Test lamp state definitions."""

    def test_all_14_states_defined(self):
        """All 14 Pixstars lamp states are defined."""
        expected = [
            "INERT", "FUNCTIONAL", "CURIOUS", "DISMISSIVE", "PLEASED",
            "ARROGANT", "OVERHEATING", "DYING", "DEAD", "WEAK",
            "REBORN", "LEARNING", "CELEBRATE", "OFF"
        ]
        self.assertEqual(len(LAMP_STATES), 14)
        for name in expected:
            self.assertIn(name, LAMP_STATES)

    def test_get_state_returns_correct_type(self):
        """get_state returns a LampState dataclass."""
        state = get_state("CURIOUS")
        self.assertIsInstance(state, LampState)
        self.assertEqual(state.name, "CURIOUS")

    def test_get_state_case_insensitive(self):
        """get_state accepts any case."""
        state = get_state("curious")
        self.assertEqual(state.name, "CURIOUS")

    def test_get_state_unknown_raises(self):
        """get_state raises KeyError for unknown state."""
        with self.assertRaises(KeyError):
            get_state("UNKNOWN_STATE")

    def test_energy_bounds(self):
        """All states have energy in [0, 1]."""
        for state in LAMP_STATES.values():
            self.assertGreaterEqual(state.energy, 0.0)
            self.assertLessEqual(state.energy, 1.0)

    def test_speed_bounds(self):
        """All states have speed in [0, 1]."""
        for state in LAMP_STATES.values():
            self.assertGreaterEqual(state.speed, 0.0)
            self.assertLessEqual(state.speed, 1.0)

    def test_range_bounds(self):
        """All states have range in [0, 1]."""
        for state in LAMP_STATES.values():
            self.assertGreaterEqual(state.range, 0.0)
            self.assertLessEqual(state.range, 1.0)

    def test_jitter_bounds(self):
        """All states have jitter in [0, 1]."""
        for state in LAMP_STATES.values():
            self.assertGreaterEqual(state.jitter, 0.0)
            self.assertLessEqual(state.jitter, 1.0)

    def test_tilt_bias_bounds(self):
        """All states have tilt_bias in [-1, 1]."""
        for state in LAMP_STATES.values():
            self.assertGreaterEqual(state.tilt_bias, -1.0)
            self.assertLessEqual(state.tilt_bias, 1.0)

    def test_inert_and_dead_are_still(self):
        """INERT, DEAD, and OFF should have zero energy."""
        for name in ["INERT", "DEAD", "OFF"]:
            state = get_state(name)
            self.assertEqual(state.energy, 0.0)
            self.assertEqual(state.speed, 0.0)

    def test_overheating_has_high_jitter(self):
        """OVERHEATING should have high jitter."""
        state = get_state("OVERHEATING")
        self.assertGreater(state.jitter, 0.5)

    def test_dead_has_lowest_tilt(self):
        """DEAD should have the most collapsed tilt bias."""
        state = get_state("DEAD")
        self.assertEqual(state.tilt_bias, -1.0)

    def test_list_states_returns_all(self):
        """list_states returns all 14 state names."""
        names = list_states()
        self.assertEqual(len(names), 14)

    def test_all_states_have_description(self):
        """Every state has a non-empty description."""
        for state in LAMP_STATES.values():
            self.assertIsInstance(state.description, str)
            self.assertGreater(len(state.description), 0)


if __name__ == "__main__":
    unittest.main()
