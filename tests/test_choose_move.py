import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path so we can import revomon_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock PIL before importing revomon_app
sys.modules["PIL"] = MagicMock()
sys.modules["PIL.Image"] = MagicMock()

# Mock bluepyll before importing revomon_app
mock_bluepyll = MagicMock()
sys.modules["bluepyll"] = mock_bluepyll


# Define MockAppLifecycleState
class MockAppLifecycleState:
    READY = "READY"
    CLOSED = "CLOSED"


mock_bluepyll.AppLifecycleState = MockAppLifecycleState
mock_bluepyll.BluePyllApp = MagicMock
mock_bluepyll.BluePyllController = MagicMock

# Now import revomon_app
from revomonauto.models.revomon_app import RevomonApp  # noqa: E402
from revomonauto.models.states import GameState  # noqa: E402
from revomonauto.models.strategies import BattleStrategy  # noqa: E402

# Use the mock AppLifecycleState locally as well
AppLifecycleState = MockAppLifecycleState


class TestChooseMove(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MagicMock()
        # Mock screens to avoid loading actual UI elements
        with (
            patch("revomonauto.models.revomon_app.StartGameScreen"),
            patch("revomonauto.models.revomon_app.LoginScreen"),
            patch("revomonauto.models.revomon_app.OverworldScreen"),
            patch("revomonauto.models.revomon_app.MainMenuScreen"),
            patch("revomonauto.models.revomon_app.SharedScreen"),
            patch("revomonauto.models.revomon_app.BattleScreen"),
            patch("revomonauto.models.revomon_app.TeamBagScreen"),
        ):
            self.app = RevomonApp(self.mock_controller)

        # Suppress logging during tests
        self.app.logger = MagicMock()
        self.app.game_state = GameState.BATTLE
        self.app.app_state = MagicMock()
        self.app.app_state.current_state = AppLifecycleState.READY
        self.app.wait_for_action = MagicMock()

        # Initialize actions list for the action decorator
        self.app.actions = []
        self.app.last_action = {}

        # Mock UI elements for battle screen
        self.app.screens["battle"].elements = {
            "player1_mon_move1_button": MagicMock(),
            "player1_mon_move2_button": MagicMock(),
            "player1_mon_move3_button": MagicMock(),
            "player1_mon_move4_button": MagicMock(),
        }

        # Setup mock mon on field
        self.app.mon_on_field = {
            "moves": [
                {"name": "Tackle", "pp": {"current": 10}},
                {"name": "Growl", "pp": {"current": 5}},
                {"name": None, "pp": {"current": 0}},
                {"name": "Scratch", "pp": {"current": 0}},  # 0 PP
            ]
        }

    def test_default_random_strategy(self):
        # Should pick one of Tackle or Growl
        with patch("revomonauto.models.strategies.random.choice") as mock_choice:
            mock_choice.return_value = "Tackle"
            self.app.choose_move()
            mock_choice.assert_called_with(["Tackle", "Growl"])
            # Should click move 1 button (index 0)
            self.app.bluepyll_controller.click_element.assert_called_with(
                self.app.screens["battle"].elements["player1_mon_move1_button"]
            )

    def test_custom_strategy(self):
        class AlwaysGrowl(BattleStrategy):
            def select_move(self, valid_moves):
                return "Growl"

        self.app.choose_move(strategy=AlwaysGrowl())

        # Should click move 2 button (index 1)
        target_btn = self.app.screens["battle"].elements["player1_mon_move2_button"]

        # Manual assertion to be safe against mock identity issues
        calls = self.app.bluepyll_controller.click_element.call_args_list
        self.assertTrue(len(calls) > 0, "click_element was not called")
        self.assertIs(
            calls[0][0][0], target_btn, "click_element called with wrong argument"
        )

    def test_invalid_move_from_strategy(self):
        class InvalidMove(BattleStrategy):
            def select_move(self, valid_moves):
                return "Invalid"

        # The action decorator catches exceptions and returns the action dict
        result = self.app.choose_move(strategy=InvalidMove())

        # Verify the action failed
        self.assertFalse(result["status"], "Action should have failed")
        self.assertIn(
            "Strategy selected invalid move 'Invalid'", result["error_message"]
        )


if __name__ == "__main__":
    unittest.main()
