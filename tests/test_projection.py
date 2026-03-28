"""Tests for the Projection scene definitions."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from projection.scenes import get_scene, list_scenes, Scene, SCENES


class TestProjectionScenes(unittest.TestCase):
    """Test projection scene definitions."""

    def test_all_10_scenes_defined(self):
        """All 10 projection scenes are defined."""
        expected = [
            "BLACKOUT", "GNR_LOGO", "DISNEY_CASTLE", "MICKEY_DRAWING",
            "LAMP_DRAWING", "AI_ITERATIONS", "AI_SIGNATURE",
            "WALT_SIGNATURE", "AXEL_SIGNATURE", "TEAM_ROCKSTARS",
        ]
        self.assertEqual(len(SCENES), 10)
        for name in expected:
            self.assertIn(name, SCENES)

    def test_get_scene_returns_correct_type(self):
        scene = get_scene("GNR_LOGO")
        self.assertIsInstance(scene, Scene)
        self.assertEqual(scene.name, "GNR_LOGO")

    def test_get_scene_case_insensitive(self):
        scene = get_scene("gnr_logo")
        self.assertEqual(scene.name, "GNR_LOGO")

    def test_get_scene_unknown_raises(self):
        with self.assertRaises(KeyError):
            get_scene("NONEXISTENT")

    def test_blackout_has_no_image(self):
        scene = get_scene("BLACKOUT")
        self.assertEqual(scene.image_file, "")
        self.assertEqual(scene.background_color, (0, 0, 0))

    def test_all_scenes_have_description(self):
        for scene in SCENES.values():
            self.assertIsInstance(scene.description, str)
            self.assertGreater(len(scene.description), 0)

    def test_non_blackout_scenes_have_image_file(self):
        for scene in SCENES.values():
            if scene.name != "BLACKOUT":
                self.assertTrue(scene.image_file.endswith(".png"),
                                f"{scene.name} should have a .png image file")

    def test_background_colors_are_valid_rgb(self):
        for scene in SCENES.values():
            r, g, b = scene.background_color
            self.assertTrue(0 <= r <= 255)
            self.assertTrue(0 <= g <= 255)
            self.assertTrue(0 <= b <= 255)

    def test_list_scenes_returns_all(self):
        names = list_scenes()
        self.assertEqual(len(names), 10)

    def test_timeline_scenes_all_exist(self):
        """All scene names used in the timeline exist in SCENES."""
        import yaml
        with open("conductor/timeline.yaml") as f:
            data = yaml.safe_load(f)
        for cue in data["cues"]:
            if "projection" in cue and cue["projection"]:
                self.assertIn(cue["projection"], SCENES,
                              f"Timeline scene '{cue['projection']}' not in SCENES")


class TestLightingStates(unittest.TestCase):
    """Test lighting state definitions (imported here for convenience)."""

    def test_all_9_states_defined(self):
        from lighting.states import LIGHTING_STATES
        expected = [
            "BLACKOUT", "LAMP_ONLY", "ROCKSTAR", "DISNEY_SOFT",
            "AI_COLD", "OVERHEAT", "DEATH", "REBIRTH", "FINALE",
        ]
        self.assertEqual(len(LIGHTING_STATES), 9)
        for name in expected:
            self.assertIn(name, LIGHTING_STATES)

    def test_get_state_works(self):
        from lighting.states import get_lighting_state
        state = get_lighting_state("ROCKSTAR")
        self.assertEqual(state.name, "ROCKSTAR")

    def test_get_state_case_insensitive(self):
        from lighting.states import get_lighting_state
        state = get_lighting_state("rockstar")
        self.assertEqual(state.name, "ROCKSTAR")

    def test_unknown_raises(self):
        from lighting.states import get_lighting_state
        with self.assertRaises(KeyError):
            get_lighting_state("NOPE")

    def test_blackout_all_zero(self):
        from lighting.states import get_lighting_state
        state = get_lighting_state("BLACKOUT")
        for ch, val in state.channels.items():
            self.assertEqual(val, 0, f"BLACKOUT ch{ch} should be 0")

    def test_all_channels_in_range(self):
        from lighting.states import LIGHTING_STATES
        for state in LIGHTING_STATES.values():
            for ch, val in state.channels.items():
                self.assertTrue(0 <= val <= 255,
                                f"{state.name} ch{ch}={val} out of range")
                self.assertTrue(1 <= ch <= 512,
                                f"{state.name} ch{ch} invalid channel number")

    def test_all_states_have_description(self):
        from lighting.states import LIGHTING_STATES
        for state in LIGHTING_STATES.values():
            self.assertIsInstance(state.description, str)
            self.assertGreater(len(state.description), 0)

    def test_timeline_lighting_all_exist(self):
        """All lighting states used in timeline exist."""
        from lighting.states import LIGHTING_STATES
        import yaml
        with open("conductor/timeline.yaml") as f:
            data = yaml.safe_load(f)
        for cue in data["cues"]:
            if "lighting" in cue and cue["lighting"]:
                self.assertIn(cue["lighting"], LIGHTING_STATES,
                              f"Timeline lighting '{cue['lighting']}' not in LIGHTING_STATES")

    def test_overheat_has_strobe(self):
        from lighting.states import get_lighting_state
        state = get_lighting_state("OVERHEAT")
        self.assertGreater(state.channels.get(6, 0), 0, "OVERHEAT should have strobe")


if __name__ == "__main__":
    unittest.main()
