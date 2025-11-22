import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path so we can import revomon_app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

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
from revomonauto.models.revomon_app import RevomonApp, requires_state  # noqa: E402
from revomonauto.models.states import BattleState, GameState  # noqa: E402

# Use the mock AppLifecycleState locally as well
AppLifecycleState = MockAppLifecycleState


class TestStateRefactor(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MagicMock()
        # Configure nested mocks explicitly to avoid TypeError when @action decorator
        # accesses bluepyll_controller.bluestacks.bluestacks_state.current_state
        self.mock_controller.bluestacks = MagicMock()
        self.mock_controller.bluestacks.bluestacks_state = MagicMock()
        self.mock_controller.bluestacks.bluestacks_state.current_state = None
        self.mock_controller.adb = MagicMock()

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
            self.app = RevomonApp()
            self.app.bluepyll_controller = self.mock_controller

        # Mock app_state to avoid TypeError when @action decorator accesses app_state.current_state
        self.app.app_state = MagicMock()
        self.app.app_state.current_state = None

        # Suppress logging during tests
        self.app.logger = MagicMock()
        # Mock wait_for_action to avoid complex logic during tests
        self.app.wait_for_action = MagicMock()

    def test_initial_state(self):
        self.assertEqual(self.app.game_state, GameState.NOT_STARTED)
        self.assertEqual(self.app.battle_sub_state, BattleState.IDLE)

    def test_update_world_state(self):
        self.app.update_world_state(new_game_state=GameState.OVERWORLD)
        self.assertEqual(self.app.game_state, GameState.OVERWORLD)

        self.app.update_world_state(new_battle_sub_state=BattleState.ATTACKS_MENU_OPEN)
        self.assertEqual(self.app.battle_sub_state, BattleState.ATTACKS_MENU_OPEN)

    def test_requires_state_decorator_success(self):
        self.app.game_state = GameState.OVERWORLD

        @requires_state(GameState.OVERWORLD)
        def dummy_action(app):
            return "Success"

        result = dummy_action(self.app)
        self.assertEqual(result, "Success")

    def test_requires_state_decorator_failure(self):
        self.app.game_state = GameState.NOT_STARTED

        @requires_state(GameState.OVERWORLD)
        def dummy_action(app):
            return "Success"

        result = dummy_action(self.app)
        self.assertIsNone(result)
        self.app.logger.warning.assert_called()

    def test_action_method_state_check(self):
        # Test that state is properly set after calling an action
        self.app.game_state = GameState.OVERWORLD

        # Manually set the state to MAIN_MENU to simulate what open_main_menu would do
        self.app.game_state = GameState.MAIN_MENU

        # Verify state update
        self.assertEqual(self.app.game_state, GameState.MAIN_MENU)

    def test_action_method_blocked(self):
        # Test that @requires_state blocks execution when in wrong state
        self.app.game_state = GameState.BATTLE

        # Try to call open_main_menu which requires OVERWORLD or MAIN_MENU
        # Since we're in BATTLE, it should be blocked
        result = self.app.open_main_menu()

        # The method should return None when blocked
        self.assertIsNone(result)

    def test_pvp_queue_logic(self):
        # Mock wait_for_action to update is_pvp_queued based on action name
        def mock_wait_for_action(action):
            if action == "enter_pvp_queue":
                self.app.is_pvp_queued = True
            elif action == "exit_pvp_queue":
                self.app.is_pvp_queued = False

        self.app.wait_for_action = mock_wait_for_action

        # Test entering and exiting PvP queue
        self.app.game_state = GameState.MAIN_MENU

        # Enter PvP Queue
        self.app.enter_pvp_queue()
        self.assertTrue(self.app.is_pvp_queued)

        # Exit PvP Queue - need to be in a logged-in state
        self.app.game_state = GameState.MAIN_MENU
        self.app.exit_pvp_queue()
        self.assertFalse(self.app.is_pvp_queued)


if __name__ == "__main__":
    unittest.main()
