import io
import time
from logging import getLogger
from pathlib import Path
from threading import Thread

from bluepyll.controller import BluepyllController
from bluepyll.state_machine import AppLifecycleState
from PIL import Image

from revomonauto.models.action import Action, Actions, action
from revomonauto.models.revo_app import (
    BattleState,
    LoginState,
    MenuState,
    RevomonApp,
    TVState,
)
from revomonauto.revomon import revomon_ui as ui

logger = getLogger(__name__)


class RevoAppController(BluepyllController, RevomonApp):
    def __init__(self):
        # Initialize parent classes
        BluepyllController.__init__(self)
        RevomonApp.__init__(self)

        # Initialize instance variables
        self.last_action = None
        self.actions = Actions()
        self._auto_run_thread: Thread = Thread(
            target=self._auto_run, daemon=True, name="GradexAgent(Auto-Run)"
        )
        # self.sense_thread: Thread = Thread(target=self.sense, args=(), name="RevoController Senses", daemon=True)

    def get_current_state(self) -> Action:
        """
        Returns the current state of the Revomon app.

        Returns:
            dict: The current state of the app.
        """
        return {
            "current_scene": self.curr_scene,
            "tv_current_page": self.tv_current_page,
            "tv_slot_selceted": self.tv_slot_selected,
            "tv_searching_for": self.tv_searching_for,
            "current_city": self.current_city,
            "current_location": self.current_location,
            "bluestacks_state": self.bluestacks_state.current_state,
            "app_state": self.app_state.current_state,
            "login_state": self.login_sm.current_state,
            "menu_state": self.menu_sm.current_state,
            "battle_state": self.battle_sm.current_state,
            "tv_state": self.tv_sm.current_state,
        }

    def _auto_run(self):
        while self.is_auto_run.is_set():
            self.run_from_battle()

    def extract_regions(
        self,
        position_x_sizes: list[tuple[tuple[int, int], tuple[int, int], str]],
        image: bytes | str,
    ) -> Image:
        """
        Extract a region from an image using position and size.

        Args:
            position_x_sizes (list[tuple[tuple[int, int], tuple[int, int], str]]): List of tuples containing the position, size and the label of the element to extract.

        Returns:
            Image: The extracted region as a PIL Image object
        """
        if isinstance(image, bytes):
            image = Image.open(io.BytesIO(image))
        else:
            image = Image.open(image)
        cropped_imgs = []
        for position_x_size in position_x_sizes:
            # Calculate region boundaries
            left = position_x_size[0][0]
            top = position_x_size[0][1]
            right = left + position_x_size[1][0]
            bottom = top + position_x_size[1][1]

            # Extract the region
            cropped_img = image.crop((left, top, right, bottom))

            # Save to the repo battles directory: src/revomonauto/revomon/battles/
            battles_dir = Path(__file__).resolve().parent.parent / "revomon" / "battles"
            battles_dir.mkdir(parents=True, exist_ok=True)
            dest_path = battles_dir / f"{position_x_size[2]}.png"
            cropped_img.save(dest_path)
            cropped_imgs.append(cropped_img)

        return cropped_imgs

    def extract_health_percentage(self, image_path: str, padding: int = 5) -> float:
        """
        Calculates the health percentage from a health bar image, ignoring padding.
        It assumes anything not black is health and ignores a specified number of
        pixels on the left and right sides.

        Args:
            image_path (str): The file path to the image.
            padding (int): The number of pixels to ignore on each side.

        Returns:
            float: The percentage of health remaining (0.0 to 100.0),
                or -1 if an error occurs.
        """
        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                width, height = img.size
                pixels = img.load()

                health_pixels = 0
                missing_health_pixels = 0

                # Scan a representative row of pixels in the middle of the image.
                y_scan = height // 2

                # Adjust the range to ignore the padding on the left and right.
                # We also ensure the width is large enough to handle the padding.
                if width <= 2 * padding:
                    print("Error: Image width is too small to account for padding.")
                    return -1.0

                for x in range(padding, width - padding):
                    r, g, b = pixels[x, y_scan]

                    # Assume any pixel that's not a shade of black is health.
                    if r < 50 and g < 50 and b < 50:
                        missing_health_pixels += 1
                    else:
                        health_pixels += 1

                total_pixels = health_pixels + missing_health_pixels

                if total_pixels == 0:
                    # Handle cases where the health bar might be entirely missing or unreadable.
                    return 0.0

                health_percentage = (health_pixels / total_pixels) * 100

                return health_percentage

        except FileNotFoundError:
            print(f"Error: The file at {image_path} was not found.")
            return -1.0
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1.0

    def extract_initial_battle_info(self):
        try:
            screenshot_bytes = self.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            # Extract initial battle info
            self.extract_regions(
                position_x_sizes=[
                    (
                        ui.player1_mon_name_text.position,
                        ui.player1_mon_name_text.size,
                        ui.player1_mon_name_text.label,
                    ),
                    (
                        ui.player1_mon_lvl_text.position,
                        ui.player1_mon_lvl_text.size,
                        ui.player1_mon_lvl_text.label,
                    ),
                    (
                        ui.player1_mon_hp_text.position,
                        ui.player1_mon_hp_text.size,
                        ui.player1_mon_hp_text.label,
                    ),
                    (
                        ui.player2_mon_name_text.position,
                        ui.player2_mon_name_text.size,
                        ui.player2_mon_name_text.label,
                    ),
                    (
                        ui.player2_mon_lvl_text.position,
                        ui.player2_mon_lvl_text.size,
                        ui.player2_mon_lvl_text.label,
                    ),
                    (
                        ui.player2_mon_hp_text.position,
                        ui.player2_mon_hp_text.size,
                        ui.player2_mon_hp_text.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            player1_mon_name = self.img_txt_checker.read_text(
                ui.player1_mon_name_text.path
            )
            player1_mon_lvl = self.img_txt_checker.read_text(
                ui.player1_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            for result in player1_mon_lvl:
                if "lvl " in result:
                    level = result.strip("lvl ")
                    if level.isdigit():
                        if int(level) > 100:
                            player1_mon_lvl = ["lvl 100"]
                if result[3] != " ":
                    level = result.strip("lvl")
                    if level.isdigit():
                        player1_mon_lvl = [f"lvl {level}"]
            percentage1 = self.extract_health_percentage(ui.player1_mon_hp_text.path)

            player2_mon_name = self.img_txt_checker.read_text(
                ui.player2_mon_name_text.path
            )
            player2_mon_lvl = self.img_txt_checker.read_text(
                ui.player2_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            for result in player2_mon_lvl:
                if "lvl " in result:
                    level = result.strip("lvl ")
                    if level.isdigit():
                        if int(level) > 100:
                            player2_mon_lvl = ["lvl 100"]
                if result[3] != " ":
                    level = result.strip("lvl")
                    if level.isdigit():
                        player2_mon_lvl = [f"lvl {level}"]
            percentage2 = self.extract_health_percentage(ui.player2_mon_hp_text.path)

            logger.info("Initial battle info extracted successfully")
            logger.info(
                f"ME: {player1_mon_name} {player1_mon_lvl} Health: {percentage1:.2f}%"
            )
            logger.info(
                f"OPPONENT: {player2_mon_name} {player2_mon_lvl} Health: {percentage2:.2f}%"
            )
        except Exception as e:
            logger.error(f"Error extracting initial battle info: {e}")

    def extract_current_battle_moves_info(self):
        def process_move_data(move_data: list[str]):
            # Post-processing to fix common OCR mistakes
            if len(move_data) >= 3:
                for result in move_data[2:]:
                    move_data[0] = f"{move_data[0]} {result}"
                move_data = move_data[:2]

            if move_data[1] in ["toho", "ioh1o", "oh1o"]:
                move_data[1] = "10/10"
            return move_data

        try:
            screenshot_bytes = self.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            # Extract current battle moves info
            self.extract_regions(
                position_x_sizes=[
                    (
                        ui.player1_mon_move1_text.position,
                        ui.player1_mon_move1_text.size,
                        ui.player1_mon_move1_text.label,
                    ),
                    (
                        ui.player1_mon_move2_text.position,
                        ui.player1_mon_move2_text.size,
                        ui.player1_mon_move2_text.label,
                    ),
                    (
                        ui.player1_mon_move3_text.position,
                        ui.player1_mon_move3_text.size,
                        ui.player1_mon_move3_text.label,
                    ),
                    (
                        ui.player1_mon_move4_text.position,
                        ui.player1_mon_move4_text.size,
                        ui.player1_mon_move4_text.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            player1_mon_move1 = self.img_txt_checker.read_text(
                ui.player1_mon_move1_text.path
            )
            player1_mon_move1 = process_move_data(player1_mon_move1)
            player1_mon_move2 = self.img_txt_checker.read_text(
                ui.player1_mon_move2_text.path
            )
            player1_mon_move2 = process_move_data(player1_mon_move2)
            player1_mon_move3 = self.img_txt_checker.read_text(
                ui.player1_mon_move3_text.path
            )
            player1_mon_move3 = process_move_data(player1_mon_move3)
            player1_mon_move4 = self.img_txt_checker.read_text(
                ui.player1_mon_move4_text.path
            )
            player1_mon_move4 = process_move_data(player1_mon_move4)

            logger.info("Current battle moves info extracted successfully")
            logger.info(
                f"MOVES: {player1_mon_move1} {player1_mon_move2} {player1_mon_move3} {player1_mon_move4}"
            )
        except Exception as e:
            logger.error(f"Error extracting current battle moves info: {e}")

    @action
    def open_revomon_app(self) -> Action:
        """
        Opens the Revomon app if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """

        match self.app_state.current_state:
            case AppLifecycleState.CLOSED:
                self.open_app(app=self, timeout=60, wait_time=60)

    @action
    def close_revomon_app(self) -> Action:
        """
        Closes the Revomon app if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.app_state.current_state:
            case AppLifecycleState.LOADING | AppLifecycleState.READY:
                self.close_app(app=self)

    @action
    def start_game(self) -> Action:
        """
        Starts the game if it is not already started.

        Returns:
            Action (dict): The action object representing the action performed.
        """

        # Wait for the app to be ready
        logger.info("Waiting for app to be ready...")
        max_attempts = 10
        for attempt in range(max_attempts):
            current_state = self.app_state.current_state
            logger.info(
                f"Current app state: {current_state} state type: {type(current_state)} (attempt {attempt + 1}/{max_attempts})"
            )
            if current_state == AppLifecycleState.READY:
                logger.info("App is ready")
                break
            time.sleep(2.0)
        else:
            logger.warning("Timed out waiting for app to be ready")

        match self.app_state.current_state:
            case AppLifecycleState.READY:
                match self.login_sm.current_state:
                    case LoginState.NOT_STARTED:
                        self.click_ui([ui.start_game_button], max_tries=1)

    @action
    def log_in(self) -> Action:
        """
        Logs in to the game if it is not already logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.STARTED:
                self.click_ui([ui.login_button, ui.relogin_button], max_tries=1)

    @action
    def open_main_menu(self) -> Action:
        """
        Opens the main menu if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.menu_sm.current_state:
            case MenuState.MAIN_MENU_CLOSED:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.tv_sm.current_state:
                            case TVState.TV_CLOSED:
                                self.click_ui([ui.main_menu_button], max_tries=1)

    @action
    def close_main_menu(self) -> Action:
        """
        Closes the main menu if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.menu_sm.current_state:
            case MenuState.MAIN_MENU_OPEN:
                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Main Menu is not open!")

    @action
    def enter_pvp_queue(self) -> Action:
        # TODO: FIND A WAY TO DETRIMINE IF USER IS ACTAULLY QUEUED FOR PVP BATTLE.
        match self.battle_sm.current_state:
            case BattleState.NOT_IN_BATTLE:
                match self.menu_sm.current_state:
                    case MenuState.MAIN_MENU_CLOSED:
                        self.open_main_menu()
                self.click_ui([ui.pvp_button], max_tries=1)
            case _:
                raise ValueError(f"Already in or queued for a battle!")

    @action
    def exit_pvp_queue(self) -> Action:
        # TODO: FIND A WAY TO DETRIMINE IF USER IS ACTAULLY QUEUED FOR PVP BATTLE.
        """
        Exits the PVP queue if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.battle_sm.current_state:
            case BattleState.IN_PVP_QUEUE:
                match self.menu_sm.current_state:
                    case MenuState.MAIN_MENU_CLOSED:
                        self.open_main_menu()
                self.click_ui([ui.pvp_button], max_tries=1)
            case _:
                raise ValueError(f"Not in a battle or queued for a battle!")

    @action
    def toggle_auto_run(self) -> Action:
        """
        Toggles the auto run feature.
        Auto run feature runs from all battles automatically whenever the user gets in battle.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.is_auto_run.is_set():
            case True:
                self.is_auto_run.clear()
                self._auto_run_thread.join()
            case False:
                self.is_auto_run.set()
                self._auto_run_thread.start()

    @action
    def run_from_battle(self) -> Action:
        """
        Runs from the current battle if the user is in battle.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.battle_sm.current_state:
            case BattleState.BATTLE_BAG_OPEN:
                self.close_battle_bag()
            case BattleState.ATTACKS_MENU_OPEN:
                self.close_attacks_menu()
            case BattleState.IN_BATTLE:
                self.click_coords(ui.run_button_pixel.center)
                logger.info("RUN BUTTON CLICKED")
                time.sleep(1.0)
                self.click_coords(ui.run_confirm_button_pixel.center)
                logger.info("RUN CONFIRM BUTTON CLICKED")

    @action
    def open_menu_bag(self) -> Action:
        """
        Opens the menu bag if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.team_bag_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_menu_bag(self) -> Action:
        """
        Closes the menu bag if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MENU_BAG_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_wardrobe(self) -> Action:
        # TODO: Implement a 'set_is_wardrobe_open' method
        """
        Opens the wardrobe if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.wardrobe_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_wardrobe(self) -> Action:
        # TODO: Implement a 'set_is_wardrobe_open' method
        """
        Closes the wardrobe if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.WARDROBE_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def recall_revomon(self) -> Action:
        # TODO: Implement a 'set_is_mon_recalled' method
        """
        Recalls the revomon if it is not already recalled.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.recall_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_friends_list(self) -> Action:
        # TODO: Implement a 'set_is_friends_list_open' method
        """
        Opens the friends list if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.friends_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_friends_list(self) -> Action:
        # TODO: Implement a 'set_is_friends_list_open' method
        """
        Closes the friends list if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.FRIENDS_LIST_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_settings(self) -> Action:
        # TODO: Implement a 'set_is_settings_open' method
        """
        Opens the settings menu if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.settings_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_settings(self) -> Action:
        # TODO: Implement a 'set_is_settings_open' method
        """
        Closes the settings menu if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.SETTINGS_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_revodex(self) -> Action:
        # TODO: Implement a 'set_is_revodex_open' method
        """
        Opens the revodex if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.revodex_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_revodex(self) -> Action:
        # TODO: Implement a 'set_is_revodex_open' method
        """
        Closes the revodex if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.REVODEX_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_market(self) -> Action:
        # TODO: Implement a 'set_is_market_open' method
        """
        Opens the in-game marketplace if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.market_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_market(self) -> Action:
        # TODO: Implement a 'set_is_market_open' method
        """
        Closes the in-game marketplace if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MARKET_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_discussion(self) -> Action:
        # TODO: Implement a 'set_is_discussion_open' method
        """
        Opens the discussion menuif it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.discussion_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_discussion(self) -> Action:
        # TODO: Implement a 'set_is_discussion_open' method
        """
        Closes the discussion menu if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.DISCUSSION_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_clan(self) -> Action:
        # TODO: Implement a 'set_is_clan_open' method
        """
        Opens the clan menu if it is not already open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.clan_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_clan(self) -> Action:
        # TODO: Implement a 'set_is_clan_open' method
        """
        Closes the clan menu if it is open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.CLAN_OPEN:
                                self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_attacks_menu(self) -> Action:
        """
        Opens the attacks menu if it is not already open.
        User must be in battle and not already have the attacks menu open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        if self.is_in_battle_scene():
                            self.click_coords(ui.attacks_button_pixel.center)
                    case BattleState.IN_BATTLE:
                        self.click_coords(ui.attacks_button_pixel.center)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_attacks_menu(self) -> Action:
        """
        Closes the attacks menu if it is open.
        User must be in battle and attacks menu must be open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.ATTACKS_MENU_OPEN:
                        self.click_coords(ui.exit_attacks_button_pixel.center)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_battle_bag(self) -> Action:
        """
        Opens the battle bag if it is not already open.
        User must be in battle and battle bag must not be open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        if self.is_in_battle_scene():
                            self.click_coords(ui.team_bag_battle_pixel.center)
                    case BattleState.ATTACKS_MENU_OPEN:
                        self.close_attacks_menu()
                    case BattleState.IN_BATTLE:
                        self.click_coords(ui.team_bag_battle_pixel.center)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_battle_bag(self) -> Action:
        """
        Closes the battle bag if it is open.
        User must be in battle and battle bag must be open.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.BATTLE_BAG_OPEN:
                        self.click_ui([ui.exit_menu_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_available_bag(self) -> Action:
        """
        Opens either the battle bag if the user is in battle,
        or the menu bag if the user is not in battle.
        User must be logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.IN_BATTLE:
                        self.open_battle_bag()
                    case BattleState.NOT_IN_BATTLE:
                        if self.is_in_battle_scene():
                            self.open_battle_bag()
                        else:
                            self.open_menu_bag()
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_available_bag(self) -> Action:
        """
        Closes either the battle bag if the user is in battle,
        or the menu bag if the user is not in battle.
        User must be logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.BATTLE_BAG_OPEN:
                        self.close_battle_bag()
                match self.menu_sm.current_state:
                    case MenuState.MENU_BAG_OPEN:
                        self.close_menu_bag()
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def open_tv(self) -> Action:
        """
        Opens the TV if it is not already open.
        User must be logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.tv_sm.current_state:
                            case TVState.TV_CLOSED:
                                self.double_click_ui([ui.tv_screen_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def close_tv(self) -> Action:
        """
        Closes the TV if it is open.
        User must be logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.tv_sm.current_state:
                            case TVState.TV_OPEN:
                                self.click_ui([ui.tv_exit_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def tv_search_for_revomon(self, revomon_name: str) -> Action:
        # TODO: Implement a 'set_is_searching_for_mon' method
        """
        Searches for a revomon in the TV.
        User must be logged in and the TV must be open.

        Args:
            revomon_name (str): The name of the revomon to search for.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.tv_sm.current_state:
                            case TVState.TV_OPEN:
                                self.click_ui(ui.tv_search_input)
                                time.sleep(1.0)
                                self.type_text(revomon_name)
                                time.sleep(2.0)
                                self.click_ui(ui.tv_search_button)
                                self.mon_searching_for = revomon_name
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def select_tv_slot(self, slot_number: int) -> Action:
        # TODO: Implement a 'set_is_mon_selected' method
        """
        Selects a specific slot in the TV.
        User must be logged in and the TV must be open.

        Args:
            slot_number (int): The number of the slot you want to select in the TV

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.tv_sm.current_state:
                            case TVState.TV_OPEN:
                                print(f"SELECTING SLOT #: {slot_number}")
                                if slot_number != self.tv_slot_selected:
                                    self.click_coords(
                                        ui.tv_slots[slot_number - 1].center
                                    )
                                    self.tv_slot_selected = slot_number - 1
                                    self.is_mon_selected = True
            case _:
                raise ValueError(f"Not logged in!")

    @action
    def quit_game(self) -> Action:
        """
        Quits the game if the user is logged in and not in battle.
        User must be logged in.

        Returns:
            Action (dict): The action object representing the action performed.
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_CLOSED:
                                self.open_main_menu()
                        match self.menu_sm.current_state:
                            case MenuState.MAIN_MENU_OPEN:
                                self.click_ui([ui.quit_game_button], max_tries=1)
            case _:
                raise ValueError(f"Not logged in!")

    # STATE UPDATE FUNCTIONS
    def update_world_state(
        self,
        new_app_state: AppLifecycleState | None = None,
        new_login_state: LoginState | None = None,
        new_menu_state: MenuState | None = None,
        new_battle_state: BattleState | None = None,
        new_tv_state: TVState | None = None,
    ):

        if new_app_state:
            match (self.app_state.current_state == new_app_state):
                case False:
                    self.app_state.transition_to(new_app_state)
                    logger.info(f"App state updated to: {new_app_state}")
                case True:
                    logger.info(f"App state is already: {new_app_state}")

        if new_login_state:
            match (self.login_sm.current_state == new_login_state):
                case False:
                    self.login_sm.transition_to(new_login_state)
                    logger.info(f"Login state updated to: {new_login_state}")
                case True:
                    logger.info(f"Login state is already: {new_login_state}")

        if new_menu_state:
            match (self.menu_sm.current_state == new_menu_state):
                case False:
                    self.menu_sm.transition_to(new_menu_state)
                    logger.info(f"Menu state updated to: {new_menu_state}")
                case True:
                    logger.info(f"Menu state is already: {new_menu_state}")

        if new_battle_state:
            match (self.battle_sm.current_state == new_battle_state):
                case False:
                    self.battle_sm.transition_to(new_battle_state)
                    logger.info(f"Battle state updated to: {new_battle_state}")
                case True:
                    logger.info(f"Battle state is already: {new_battle_state}")

        if new_tv_state:
            match (self.tv_sm.current_state == new_tv_state):
                case False:
                    self.tv_sm.transition_to(new_tv_state)
                    logger.info(f"TV state updated to: {new_tv_state}")
                case True:
                    logger.info(f"TV state is already: {new_tv_state}")

    def is_start_game_scene(self) -> bool:
        """
        Checks if the Revomon app is in the start game scene(app open and loaded).
        Passing this check means the app is open and loaded.

        Returns:
            bool: True if the app is in the start game scene, False otherwise.
        """
        # Start Game Screen Scene
        try:

            match self.find_ui([ui.start_game_button], max_tries=1):
                case tuple():
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.NOT_STARTED,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.NOT_IN_BATTLE,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "start_game"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during ' is_start_game_scene': {e}")

    def is_login_scene(self) -> bool:
        """
        Checks if the Revomon app is in the login scene(app open, loaded and started).
        Passing this check means the app is open, loaded and started.

        Returns:
            bool: True if the app is in the login scene, False otherwise.
        """
        # Login Screen Scene
        try:

            match self.find_ui([ui.login_button, ui.relogin_button], max_tries=1):
                case tuple():
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.STARTED,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.NOT_IN_BATTLE,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "login"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_login_scene': {e}")

    def is_overworld_scene(self) -> bool:
        """
        Checks if the Revomon app is in the overworld scene(no menu's are open and not in any battle).
        Passing this check means the app is open, loaded, started and the User is logged in.

        Returns:
            bool: True if the app is in the overworld scene, False otherwise.
        """
        # Overworld Screen Scene
        try:

            match self.find_ui([ui.main_menu_button], max_tries=1):
                case tuple():
                    new_battle_state = (
                        BattleState.IN_PVP_QUEUE
                        if self.battle_sm.current_state == BattleState.IN_PVP_QUEUE
                        else BattleState.NOT_IN_BATTLE
                    )
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=new_battle_state,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "overworld"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_overworld_scene': {e}")

    def is_tv_scene(self) -> bool:
        """
        Checks if the Revomon app is in the TV scene(TV is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the TV is open.

        Returns:
            bool: True if the app is in the TV scene, False otherwise.
        """
        try:

            match self.find_ui([ui.tv_advanced_search_button], max_tries=1):
                case tuple():
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_tv_state=TVState.TV_OPEN,
                    )
                    self.curr_scene = "tv"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_tv_scene': {e}")

    def is_menu_bag_scene(self) -> bool:
        """
        Checks if the Revomon app is in the menu bag scene(menu bag is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the menu bag is open.

        Returns:
            bool: True if the app is in the menu bag scene, False otherwise.
        """
        try:

            match (
                self.find_ui([ui.change_bag_left_button], max_tries=1),
                self.find_ui([ui.change_bag_right_button], max_tries=1),
            ):
                case (tuple(), tuple()):
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MENU_BAG_OPEN,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "menu_bag"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_menu_bag_scene': {e}")

    def is_battle_bag_scene(self) -> bool:
        # TODO: Currently is same check as menu bag scene as the bag ui appears to be the same. Update to check for battle bag ui specific elements.
        """
        Checks if the Revomon app is in the battle bag scene(battle bag is open).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the battle bag is open.

        Returns:
            bool: True if the app is in the battle bag scene, False otherwise.
        """
        try:

            match (
                self.find_ui([ui.change_bag_left_button], max_tries=1),
                self.find_ui([ui.change_bag_right_button], max_tries=1),
            ):
                case (tuple(), tuple()):
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.BATTLE_BAG_OPEN,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "battle_bag"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_battle_bag_scene': {e}")

    def is_main_menu_scene(self) -> bool:
        """
        Checks if the Revomon app is in the main menu scene(main menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the main menu is open.

        Returns:
            bool: True if the app is in the main menu scene, False otherwise.
        """
        try:

            match self.find_ui([ui.pvp_button], max_tries=1):
                case tuple():
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_OPEN,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "main_menu"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_main_menu_scene': {e}")

    def is_in_battle_scene(self) -> bool:
        """
        Checks if the Revomon app is in the in battle scene(User in battle).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the battle bag is closed.

        Returns:
            bool: True if the app is in the in battle scene, False otherwise.
        """
        try:
            # Checking for the green in the Revomon name plates that appear during battle (Player1, Player2)
            match (
                self.check_pixel_color(
                    coords=ui.player1_mon_nameplate_pixel.position,
                    target_color=ui.player1_mon_nameplate_pixel.pixel_color,
                    image=self.capture_screenshot(),
                    tolerance=5,
                ),
                self.check_pixel_color(
                    coords=ui.player2_mon_nameplate_pixel.position,
                    target_color=ui.player2_mon_nameplate_pixel.pixel_color,
                    image=self.capture_screenshot(),
                    tolerance=5,
                ),
            ):
                case (True, True):
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.IN_BATTLE,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "in_battle"
                    self.extract_initial_battle_info()
                    return True
                case _:
                    return False

        except Exception as e:
            logger.error(f"Error getting battle info(is_in_battle_scene): {e}")
            return False

    def is_attacks_menu_scene(self) -> bool:
        """
        Checks if the Revomon app is in the attacks menu scene(attacks menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the attacks menu is open.

        Returns:
            bool: True if the app is in the attacks menu scene, False otherwise.
        """
        try:
            match self.check_pixel_color(
                coords=ui.exit_attacks_button_pixel.position,
                target_color=ui.exit_attacks_button_pixel.pixel_color,
                image=self.capture_screenshot(),
                tolerance=5,
            ):
                case True:
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.ATTACKS_MENU_OPEN,
                        new_tv_state=TVState.TV_CLOSED,
                    )
                    self.curr_scene = "attacks_menu"
                    self.extract_current_battle_moves_info()
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"Error setting is_attacks_menu_scene(): {e}")

    def wait_for_action(self, action: str):
        try:
            time.sleep(2.0)

            while True:
                logger.info(f"Waiting for {action} action to complete...")
                match action:
                    case "open_revomon_app":
                        match self.is_start_game_scene():
                            case True:
                                logger.info("Revomon app opened successfully.")
                                return
                            case False:
                                continue
                    case "close_revomon_app":
                        match self.is_app_running(app=self):
                            case True:
                                continue
                            case False:
                                self.update_world_state(
                                    new_app_state=AppLifecycleState.CLOSED,
                                    new_login_state=LoginState.NOT_STARTED,
                                    new_menu_state=MenuState.MAIN_MENU_CLOSED,
                                    new_battle_state=BattleState.NOT_IN_BATTLE,
                                    new_tv_state=TVState.TV_CLOSED,
                                )
                                self.curr_scene = None
                                logger.info("Revomon app closed successfully.")
                                return
                    case "start_game":
                        match self.is_login_scene():
                            case True:
                                logger.info("Game started successfully.")
                                return
                            case False:
                                continue
                    case "log_in":
                        match self.is_overworld_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_main_menu":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_main_menu":
                        match self.is_overworld_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "enter_pvp_queue":
                        # TODO: Implement a way to tell if user is/isn't in pvp queue. For now, just assume the user joined the queue successfully.
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MAIN_MENU_OPEN,
                            new_battle_state=BattleState.IN_PVP_QUEUE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "main_menu"
                        return
                    case "exit_pvp_queue":
                        # TODO: Implement a way to tell if user is/isn't in pvp queue. For now, just assume the user exited the queue successfully.
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MAIN_MENU_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "main_menu"
                        return
                    case "toggle_auto_run":
                        return
                    case "run_from_battle":
                        match self.is_overworld_scene():
                            case True:
                                return
                            case False:
                                match self.is_login_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_menu_bag":
                        match self.is_menu_bag_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_menu_bag":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_wardrobe":
                        # TODO: Implement a way to tell if user is/isn't in wardrobe. For now, just assume the user opened the wardrobe successfully.
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.WARDROBE_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "wardrobe_menu"
                        return
                    case "close_wardrobe":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "recall_revomon":
                        # TODO:
                        self.is_mon_recalled = True
                        return
                    case "open_friends_list":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.FRIENDS_LIST_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "friends_list_menu"
                        return
                    case "close_friends_list":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_settings":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.SETTINGS_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "settings_menu"
                        return
                    case "close_settings":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_revodex":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.REVODEX_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "revodex_menu"
                        return
                    case "close_revodex":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_market":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MARKET_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "market_menu"
                        return
                    case "close_market":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_discussion":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.DISCUSSION_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "discussion_menu"
                        return
                    case "close_discussion":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_clan":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.CLAN_OPEN,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.TV_CLOSED,
                        )
                        self.curr_scene = "clan_menu"
                        return
                    case "close_clan":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_attacks_menu":
                        match self.is_attacks_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_login_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "close_attacks_menu":
                        match self.is_in_battle_scene():
                            case True:
                                return
                            case False:
                                match self.is_login_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_battle_bag":
                        match self.is_battle_bag_scene():
                            case True:
                                return
                            case False:
                                match self.is_login_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "close_battle_bag":
                        match self.is_in_battle_scene():
                            case True:
                                return
                            case False:
                                match self.is_login_scene():
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_available_bag":
                        match self.is_menu_bag_scene():
                            case True:
                                return
                            case False:
                                match self.is_battle_bag_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_in_battle_scene():
                                            case True:
                                                return
                                            case False:
                                                match self.is_login_scene():
                                                    case True:
                                                        return
                                                    case False:
                                                        continue
                    case "close_available_bag":
                        match self.is_main_menu_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_tv":
                        match self.is_tv_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_tv":
                        match self.is_overworld_scene():
                            case True:
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_scene():
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "tv_search_for_revomon":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MAIN_MENU_CLOSED,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.SEARCHING_MON,
                        )
                        self.curr_scene = "tv"
                        return
                    case "tv_select_revomon":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MAIN_MENU_CLOSED,
                            new_battle_state=BattleState.NOT_IN_BATTLE,
                            new_tv_state=TVState.MON_SELECTED,
                        )
                        self.curr_scene = "tv"
                        return
                    case "quit_game":
                        match not self.is_app_running(app=self):
                            case True:
                                self.update_world_state(
                                    new_app_state=AppLifecycleState.CLOSED,
                                    new_login_state=LoginState.NOT_STARTED,
                                    new_menu_state=MenuState.MAIN_MENU_CLOSED,
                                    new_battle_state=BattleState.NOT_IN_BATTLE,
                                    new_tv_state=TVState.TV_CLOSED,
                                )
                                return
                            case False:
                                continue
                    case _:
                        raise ValueError(f"Invalid action: {action}")

        except Exception as e:
            raise Exception(f"Error waiting for action: {e}")

    def refresh_location(self) -> tuple[str, str]:
        try:
            match self.find_ui(ui_elements=[ui.inside_revocenter_landmark]):
                case tuple():
                    self.current_location = "inside revocenter"
                    return

            match self.find_ui(ui_elements=[ui.arktos_outside_center_image]):
                case tuple():
                    self.current_location = "outside revocenter"
                    self.current_city = "arktos"
                    return
        except Exception as e:
            raise Exception(f"Error updating location: {e}")

        return self.location, self.current_city

    def reset(self, auto_update: bool = True) -> None:
        self.curr_scene = None
        self.is_mon_recalled = None
        self.tv_current_page = 1
        self.tv_searching_for = None
        self.tv_slot_selected = 0
        self.tv_slot_selected_attribs = None
        self.is_grading = False
        self.is_mons_graded = False

        self.current_city = None
        self.current_location = None

        self.mon_details_img = None
        self.mon_detail_imgs = None

        if auto_update:
            self.update_world_state()
