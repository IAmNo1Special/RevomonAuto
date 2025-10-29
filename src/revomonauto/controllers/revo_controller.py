import io
import random
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
            target=self.run_from_battle, daemon=True, name="GradexAgent(Auto-Run)"
        )

        # TODO: Scene detection needs to be finetuned before this can be used
        # TODO: This should be ran only after it's confirm the user is logged in for the first time
        # maybe...maybe there's a better way
        # self.sense_thread: Thread = Thread(target=self.sense, args=(), name="RevoController Senses", daemon=True)

        # TODO: Scene detection needs to be finetuned before this can be used
        # self.update_world_state(ignore_state_change_validation=True)

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

    def extract_battle_info(self):
        logger.info("Extracting battle info...")
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
                        ui.player1_mon_hp_img.position,
                        ui.player1_mon_hp_img.size,
                        ui.player1_mon_hp_img.label,
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
                        ui.player2_mon_hp_img.position,
                        ui.player2_mon_hp_img.size,
                        ui.player2_mon_hp_img.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            mon_name = self.img_txt_checker.read_text(ui.player1_mon_name_text.path)  
            if mon_name and mon_name[0]:  
                self.mon_on_field["name"] = mon_name[0] 

            mon_lvl = self.img_txt_checker.read_text(
                ui.player1_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            if mon_lvl and mon_lvl[0] and "lvl" in mon_lvl[0]:
                level = mon_lvl[0].strip("lvl").strip()
                if level.isdigit():
                    if int(level) > 100:
                        self.mon_on_field["level"] = 100
                    else:
                        self.mon_on_field["level"] = int(level)

            mon_hp = self.extract_health_percentage(ui.player1_mon_hp_img.path)
            if mon_hp:
                self.mon_on_field["current_hp_percentage"] = float(f"{mon_hp:.2f}")

            opps_mon_name = self.img_txt_checker.read_text(
                ui.player2_mon_name_text.path
            )
            if opps_mon_name and opps_mon_name[0]:
                self.opps_mon_on_field["name"] = opps_mon_name[0]

            opps_mon_lvl = self.img_txt_checker.read_text(
                ui.player2_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            if opps_mon_lvl and opps_mon_lvl[0] and "lvl" in opps_mon_lvl[0]:
                level = opps_mon_lvl[0].strip("lvl").strip()
                if level.isdigit():
                    if int(level) > 100:
                        self.opps_mon_on_field["level"] = 100
                    else:
                        self.opps_mon_on_field["level"] = int(level)

            opps_mon_hp = self.extract_health_percentage(ui.player2_mon_hp_img.path)
            if opps_mon_hp:
                self.opps_mon_on_field["current_hp_percentage"] = float(
                    f"{opps_mon_hp:.2f}"
                )

            logger.info("Initial battle info extracted successfully")
            logger.info(
                f"ME: NAME: {self.mon_on_field['name']} LEVEL: {self.mon_on_field['level']} CURRENT HP: {self.mon_on_field['current_hp_percentage']}%"
            )
            logger.info(
                f"OPPONENT: NAME: {self.opps_mon_on_field['name']} LEVEL: {self.opps_mon_on_field['level']} CURRENT HP: {self.opps_mon_on_field['current_hp_percentage']}%"
            )
        except Exception as e:
            logger.error(f"Error extracting initial battle info: {e}")

    def extract_battle_moves(self):
        def process_move_data(move_data: list[str]):
            try:
                # Post-processing to fix common OCR mistakes
                logger.info(f"Processing raw move data: {move_data}")
                if len(move_data) < 2:
                    logger.warning(f"Incomplete move data, cannot process PP: {move_data}")
                    return move_data
                if move_data[0] == "8":
                    move_data.pop(0)
                if len(move_data) >= 3:
                    for result in move_data[2:]:
                        move_data[0] = f"{move_data[0]} {result}"
                    move_data = move_data[:2]
                if "h" in move_data[1]:
                    move_data[1] = move_data[1].replace("h", "/")
                if "o" in move_data[1]:
                    move_data[1] = move_data[1].replace("o", "0")
                if "t" in move_data[1]:
                    move_data[1] = move_data[1].replace("t", "1")
                if "i" in move_data[1]:
                    move_data[1] = move_data[1].replace("i", "1")
                if "s" in move_data[1]:
                    move_data[1] = move_data[1].replace("s", "5")
                logger.info(f"Processed move data: {move_data}")
                return move_data
            except Exception as e:
                logger.error(f"Error processing move data: {e}")
                return None

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

            move_ui_elements = [
                ui.player1_mon_move1_text,
                ui.player1_mon_move2_text,
                ui.player1_mon_move3_text,
                ui.player1_mon_move4_text,
            ]

            for i, move_ui in enumerate(move_ui_elements):
                move_text = self.img_txt_checker.read_text(move_ui.path)
                if not move_text:
                    continue

                processed_move_data = process_move_data(move_text)
                if processed_move_data and len(processed_move_data) == 2:
                    try:
                        pp_parts = processed_move_data[1].split("/")
                        if len(pp_parts) == 2:
                            self.mon_on_field["moves"][i]["name"] = processed_move_data[0]
                            self.mon_on_field["moves"][i]["pp"]["current"] = int(pp_parts[0])
                            self.mon_on_field["moves"][i]["pp"]["total"] = int(pp_parts[1])
                    except (ValueError, IndexError) as e:
                        logger.error(f"Error parsing PP for move {i+1}: {processed_move_data[1]} - {e}")

            logger.info("Current battle moves info extracted successfully")
            logger.info(
                f"MOVES: {self.mon_on_field['moves'][0]} {self.mon_on_field['moves'][1]} {self.mon_on_field['moves'][2]} {self.mon_on_field['moves'][3]}"
            )
        except Exception as e:
            logger.error(f"Error extracting current battle moves info: {e}")

    def extract_battle_log(self):
        try:
            screenshot_bytes = self.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            if self.is_main_menu_scene():
                logger.info("Closing main menu...")
                self.close_main_menu()
                logger.info("Battle over...")

            # Extract initial battle info
            self.extract_regions(
                position_x_sizes=[
                    (
                        ui.chat_log_image.position,
                        ui.chat_log_image.size,
                        ui.chat_log_image.label,
                    ),
                ],
                image=screenshot_bytes,
            )
            # Read text from the extracted regions
            battle_log = self.img_txt_checker.read_text(ui.chat_log_image.path)
            if battle_log:
                logger.info(f"Battle log: {battle_log}")
        except Exception as e:
            logger.error(f"Error extracting battle log region: {e}")
        

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
                time.sleep(0.5)
                self.click_ui([ui.exit_menu_button], max_tries=1)
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
                time.sleep(0.5)
                self.click_ui([ui.exit_menu_button], max_tries=1)
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
                raise ValueError("Not logged in!")

    @action
    def choose_move(
        self, move_name: str | None = None, choose_random: bool = False
    ) -> Action:
        """
        Chooses a move to use in battle.

        Args:
            move_name (str | None, optional): The name of the move to use. Defaults to None.
            choose_random (bool, optional): Whether to choose a random move. Defaults to False.

        Returns:
            Action: The action object representing the action performed.

        Raises:
            ValueError: If not logged in or in an invalid battle state
            RuntimeError: If no valid moves are available or if there's an error selecting a move
        """
        match self.login_sm.current_state:
            case LoginState.LOGGED_IN:
                match self.battle_sm.current_state:
                    case BattleState.NOT_IN_BATTLE:
                        if self.is_in_battle_scene():
                            self.click_coords(ui.attacks_button_pixel.center)
                        return self.actions.click(ui.attacks_button_pixel.center)
                    case BattleState.IN_BATTLE:
                        self.click_coords(ui.attacks_button_pixel.center)
                        return self.actions.click(ui.attacks_button_pixel.center)
                    case BattleState.ATTACKS_MENU_OPEN:
                        try:
                            # Get all valid moves (non-None names with PP > 0)
                            valid_moves = [
                                move
                                for move in self.mon_on_field["moves"]
                                if move.get("name") is not None
                                and move.get("pp", {}).get("current", 0) > 0
                            ]

                            # Early exit if no valid moves
                            if not valid_moves:
                                raise RuntimeError("No valid moves found (all moves have 0 PP or None names)")

                            valid_move_names = [move["name"] for move in valid_moves]

                            # Handle random move selection with safety check
                            if choose_random:
                                if not valid_move_names:
                                    raise RuntimeError("No valid moves available for random selection")
                                move_name = random.choice(valid_move_names)
                            elif move_name is not None:
                                # For specific move, verify it's valid
                                full_move_names = [
                                    move.get("name") for move in self.mon_on_field["moves"] 
                                    if move.get("name") is not None
                                ]
                                
                                if move_name not in full_move_names:
                                    raise ValueError(
                                        f"Move '{move_name}' not found in available moves: {full_move_names}"
                                    )
                                
                                if move_name not in valid_move_names:
                                    # If move exists but not in valid_moves, it must have 0 PP
                                    raise RuntimeError(f"Move '{move_name}' has no PP remaining")

                            # Find the original index from the full moves list for UI clicking
                            try:
                                original_index = next(
                                    i for i, move in enumerate(self.mon_on_field["moves"])
                                    if move.get("name") == move_name
                                )
                            except StopIteration:
                                raise RuntimeError(f"Failed to find move in moves list: {move_name}")

                            move_buttons = [
                                ui.player1_mon_move1_text,
                                ui.player1_mon_move2_text,
                                ui.player1_mon_move3_text,
                                ui.player1_mon_move4_text,
                            ]
                            
                            if 0 <= original_index < len(move_buttons):
                                return self.actions.click_ui([move_buttons[original_index]])
                            else:
                                raise RuntimeError(f"Move index {original_index} out of range for move: {move_name}")
                                
                        except Exception as e:
                            logger.error(f"Error in choose_move: {str(e)}")
                            raise  # Re-raise the exception after logging
                    case _:
                        raise ValueError("Invalid battle state for choose_move")
            case _:
                raise ValueError("Must be logged in to choose a move")

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
        ignore_state_change_validation: bool = False,
    ) -> None:

        if new_app_state:
            match (self.app_state.current_state == new_app_state):
                case False:
                    self.app_state.transition_to(
                        new_app_state, ignore_validation=ignore_state_change_validation
                    )
                    logger.info(f"App state updated to: {new_app_state}")
                case True:
                    logger.info(f"App state is already: {new_app_state}")

        if new_login_state:
            match (self.login_sm.current_state == new_login_state):
                case False:
                    self.login_sm.transition_to(
                        new_login_state,
                        ignore_validation=ignore_state_change_validation,
                    )
                    logger.info(f"Login state updated to: {new_login_state}")
                case True:
                    logger.info(f"Login state is already: {new_login_state}")

        if new_menu_state:
            match (self.menu_sm.current_state == new_menu_state):
                case False:
                    self.menu_sm.transition_to(
                        new_menu_state, ignore_validation=ignore_state_change_validation
                    )
                    logger.info(f"Menu state updated to: {new_menu_state}")
                case True:
                    logger.info(f"Menu state is already: {new_menu_state}")

        if new_battle_state:
            match (self.battle_sm.current_state == new_battle_state):
                case False:
                    self.battle_sm.transition_to(
                        new_battle_state,
                        ignore_validation=ignore_state_change_validation,
                    )
                    logger.info(f"Battle state updated to: {new_battle_state}")
                case True:
                    logger.info(f"Battle state is already: {new_battle_state}")

        if new_tv_state:
            match (self.tv_sm.current_state == new_tv_state):
                case False:
                    self.tv_sm.transition_to(
                        new_tv_state, ignore_validation=ignore_state_change_validation
                    )
                    logger.info(f"TV state updated to: {new_tv_state}")
                case True:
                    logger.info(f"TV state is already: {new_tv_state}")
        if not any(
            [
                new_app_state,
                new_login_state,
                new_menu_state,
                new_battle_state,
                new_tv_state,
            ]
        ):
            logger.info("No state changes provided.")
            logger.info(f"Scanning for current scene...")
            if any(
                [
                    self.is_start_game_scene(True),
                    self.is_login_scene(True),
                    self.is_overworld_scene(True),
                    self.is_tv_scene(True),
                    self.is_menu_bag_scene(True),
                    self.is_battle_bag_scene(True),
                    self.is_main_menu_scene(True),
                    self.is_in_battle_scene(True),
                    self.is_attacks_menu_scene(True),
                ]
            ):
                logger.info("Current scene detected. World state updated.")
                logger.info(f"Detected scene: {self.curr_scene}")
            else:
                logger.info("New World State initialized.")

    def is_start_game_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the start game scene(app open and loaded).
        Passing this check means the app is open and loaded.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "start_game"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during ' is_start_game_scene': {e}")

    def is_login_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the login scene(app open, loaded and started).
        Passing this check means the app is open, loaded and started.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "login"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_login_scene': {e}")

    def is_overworld_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the overworld scene(no menu's are open and not in any battle).
        Passing this check means the app is open, loaded, started and the User is logged in.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "overworld"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_overworld_scene': {e}")

    def is_tv_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the TV scene(TV is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the TV is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "tv"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_tv_scene': {e}")

    def is_menu_bag_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the menu bag scene(menu bag is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the menu bag is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "menu_bag"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_menu_bag_scene': {e}")

    def is_battle_bag_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        # TODO: Currently is same check as menu bag scene as the bag ui appears to be the same. Update to check for battle bag ui specific elements.
        """
        Checks if the Revomon app is in the battle bag scene(battle bag is open).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the battle bag is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "battle_bag"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_battle_bag_scene': {e}")

    def is_main_menu_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the main menu scene(main menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the main menu is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

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
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "main_menu"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_main_menu_scene': {e}")

    def is_in_battle_scene(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is in the in battle scene(User in battle).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the battle bag is closed.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is in the in battle scene, False otherwise.
        """
        try:
            # Checking for the green in the Revomon name plates that appear during battle (Player1, Player2)
            screenshot = self.capture_screenshot()
            match (
                self.check_pixel_color(
                    coords=ui.player1_mon_nameplate_pixel.position,
                    target_color=ui.player1_mon_nameplate_pixel.pixel_color,
                    image=screenshot,
                    tolerance=10,
                ),
                self.check_pixel_color(
                    coords=ui.player2_mon_nameplate_pixel.position,
                    target_color=ui.player2_mon_nameplate_pixel.pixel_color,
                    image=screenshot,
                    tolerance=10,
                ),
            ):
                case (True, True):
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.IN_BATTLE,
                        new_tv_state=TVState.TV_CLOSED,
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "in_battle"
                    self.extract_battle_info()
                    return True
                case _:
                    return False

        except Exception as e:
            logger.error(f"Error getting battle info(is_in_battle_scene): {e}")
            return False

    def is_attacks_menu_scene(
        self, ignore_state_change_validation: bool = False
    ) -> bool:
        """
        Checks if the Revomon app is in the attacks menu scene(attacks menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the attacks menu is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is in the attacks menu scene, False otherwise.
        """
        try:
            screenshot = self.capture_screenshot()
            match self.check_pixel_color(
                coords=ui.exit_attacks_button_pixel.position,
                target_color=ui.exit_attacks_button_pixel.pixel_color,
                image=screenshot,
                tolerance=5,
            ):
                case True:
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_login_state=LoginState.LOGGED_IN,
                        new_menu_state=MenuState.MAIN_MENU_CLOSED,
                        new_battle_state=BattleState.ATTACKS_MENU_OPEN,
                        new_tv_state=TVState.TV_CLOSED,
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_scene = "attacks_menu"
                    self.extract_battle_moves()
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"Error setting is_attacks_menu_scene(): {e}")

    def is_waiting_for_opponent(
        self, ignore_state_change_validation: bool = False
    ) -> bool:
        try:
            screenshot_bytes = self.capture_screenshot()

            # Extract waiting for opponent text
            self.extract_regions(
                position_x_sizes=[
                    (
                        ui.waiting_for_opponent_text.position,
                        ui.waiting_for_opponent_text.size,
                        ui.waiting_for_opponent_text.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            result = self.img_txt_checker.read_text(ui.waiting_for_opponent_text.path)
            if len(result) > 0:
                for text in result:
                    if "for opponent" in str(text).lower():
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_login_state=LoginState.LOGGED_IN,
                            new_menu_state=MenuState.MAIN_MENU_CLOSED,
                            new_battle_state=BattleState.WAITING_FOR_OPPONENT,
                            new_tv_state=TVState.TV_CLOSED,
                            ignore_state_change_validation=ignore_state_change_validation,
                        )
                        self.curr_scene = "waiting_for_opponent"
                        return True
            return False
        except Exception as e:
            raise Exception(f"Error setting is_waiting_for_opponent(): {e}")

    def wait_for_action(self, action: str):
        try:
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
                        self.curr_scene = "overworld"
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
                        self.curr_scene = "overworld"
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
                    case "choose_move":
                        while self.is_waiting_for_opponent():
                            time.sleep(0.5)
                        match self.is_overworld_scene():
                            case True:
                                logger.info("Opening main menu...")
                                self.open_main_menu()
                                logger.info("Extracting battle log...")
                                self.extract_battle_log()
                                return
                            case False:
                                match self.is_in_battle_scene():
                                    case True:
                                        logger.info("Extracting battle log...")
                                        self.extract_battle_log()
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

    def reset(self, auto_update: bool = False) -> None:
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
