import io
import logging
from pathlib import Path
from time import sleep

from bluepyll import AppLifecycleState, BluePyllApp
from PIL import Image

from .action import Actions, action
from .revomon_ui.screens.battle_screen import BattleScreen
from .revomon_ui.screens.login_screen import LoginScreen
from .revomon_ui.screens.main_menu_screen import MainMenuScreen
from .revomon_ui.screens.overworld_screen import OverworldScreen
from .revomon_ui.screens.shared_screen import SharedScreen
from .revomon_ui.screens.start_game_screen import StartGameScreen
from .revomon_ui.screens.team_bag_screen import TeamBagScreen
from .states import BattleState, GameState, requires_state
from .strategies import BattleStrategy, RandomMove

LOGGED_IN_STATES = (
    GameState.OVERWORLD,
    GameState.MAIN_MENU,
    GameState.MENU_BAG,
    GameState.WARDROBE,
    GameState.FRIENDS_LIST,
    GameState.SETTINGS,
    GameState.REVODEX,
    GameState.MARKET,
    GameState.DISCUSSION,
    GameState.CLAN,
    GameState.TV,
)


class RevomonApp(BluePyllApp):
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__(
            app_name="revomon",
            package_name="com.revomon.vr",
            screens={
                "shared": SharedScreen(),
                "start_game": StartGameScreen(),
                "login": LoginScreen(),
                "overworld": OverworldScreen(),
                "main_menu": MainMenuScreen(),
                "battle": BattleScreen(),
                "team_bag": TeamBagScreen(),
            },
        )

        self.last_action = None
        self.actions = Actions()

        # TODO: Scene detection needs to be finetuned before this can be used
        # TODO: This should be ran only after it's confirm the user is logged in for the first time
        # maybe...maybe there's a better way
        # self.sense_thread: Thread = Thread(target=self.update_world_state, args=(ignore_state_change_validation=True), name="revomon_app", daemon=True)

        # State Machines
        self.bluestacks_state = None
        self.game_state = GameState.NOT_STARTED
        self.battle_sub_state = BattleState.IDLE

        # Remaining attributes that don't fit into state machines
        self.auto_run: bool = False
        self.auto_battle: bool = False
        self.curr_screen = None
        self.is_mon_recalled = True
        self.tv_current_page = 1
        self.tv_searching_for = None
        self.tv_slot_selected = 0
        self.tv_slot_selected_attribs = None
        self.is_grading = False
        self.is_mons_graded = False
        self.is_pvp_queued = False

        self.current_city = None
        self.current_location = None

        self.mon_details_img = None
        self.mon_detail_imgs = None

        self.team = None  # [{name: xxxx, level: xx, type: xxxx, ability: xxxx, nature: xxxx, current_hp: xx, max_hp: xx, moves: [xxxx, xxxx, xxxx, xxxx],}, ...]
        self.mon_on_field = {
            "name": None,
            "level": None,
            "current_hp_percentage": None,
            "current_hp": None,
            "max_hp": None,
            "ability": None,
            "nature": None,
            "moves": [
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
            ],
        }
        self.last_move_used = None  # {used_by: xxxx, move_name: xxxx, move_type: xxxx, starting_pp: xx, ending_pp: xx, total_pp: xx}

        self.opps_team = None  # [{name: xxxx, level: xx, type: xxxx, ability: xxxx, nature: xxxx, current_hp: xx, max_hp: xx, moves: [xxxx, xxxx, xxxx, xxxx],}, ...]
        self.opps_mon_on_field = {
            "name": None,
            "level": None,
            "current_hp_percentage": None,
            "current_hp": None,
            "max_hp": None,
            "ability": None,
            "nature": None,
            "moves": [
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
            ],
        }
        self.opps_last_move_used = None  # {used_by: xxxx, move_name: xxxx, move_type: xxxx, starting_pp: xx, ending_pp: xx, total_pp: xx}

    def get_current_state(self) -> dict:
        """
        Returns the current state of the Revomon app.

        Returns:
            dict: The current state of the app.
        """
        return {
            "current_screen": self.curr_screen,
            "tv_current_page": self.tv_current_page,
            "tv_slot_selceted": self.tv_slot_selected,
            "tv_searching_for": self.tv_searching_for,
            "current_city": self.current_city,
            "current_location": self.current_location,
            "bluestacks_state": self.bluepyll_controller.bluestacks.bluestacks_state.current_state,
            "app_state": self.app_state.current_state,
            "game_state": self.game_state,
            "battle_sub_state": self.battle_sub_state,
        }

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

            # Save to the repo battles directory: src/revomonauto/revomon_ui/assets/battle_assets/
            battles_dir = (
                Path(__file__).resolve().parent
                / "revomon_ui"
                / "assets"
                / "battle_assets"
            )
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
        self.logger.info("Extracting battle info...")
        try:
            screenshot_bytes = self.bluepyll_controller.adb.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            player1_mon_name_text = self.screens["battle"].elements[
                "player1_mon_name_text"
            ]
            player1_mon_lvl_text = self.screens["battle"].elements[
                "player1_mon_lvl_text"
            ]
            player1_mon_hp_img = self.screens["battle"].elements["player1_mon_hp_img"]
            player2_mon_name_text = self.screens["battle"].elements[
                "player2_mon_name_text"
            ]
            player2_mon_lvl_text = self.screens["battle"].elements[
                "player2_mon_lvl_text"
            ]
            player2_mon_hp_img = self.screens["battle"].elements["player2_mon_hp_img"]
            # Extract initial battle info
            self.extract_regions(
                position_x_sizes=[
                    (
                        player1_mon_name_text.position,
                        player1_mon_name_text.size,
                        player1_mon_name_text.label,
                    ),
                    (
                        player1_mon_lvl_text.position,
                        player1_mon_lvl_text.size,
                        player1_mon_lvl_text.label,
                    ),
                    (
                        player1_mon_hp_img.position,
                        player1_mon_hp_img.size,
                        player1_mon_hp_img.label,
                    ),
                    (
                        player2_mon_name_text.position,
                        player2_mon_name_text.size,
                        player2_mon_name_text.label,
                    ),
                    (
                        player2_mon_lvl_text.position,
                        player2_mon_lvl_text.size,
                        player2_mon_lvl_text.label,
                    ),
                    (
                        player2_mon_hp_img.position,
                        player2_mon_hp_img.size,
                        player2_mon_hp_img.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            mon_name = self.bluepyll_controller.image.img_txt_checker.read_text(
                player1_mon_name_text.path
            )
            if mon_name and mon_name[0]:
                self.mon_on_field["name"] = mon_name[0]

            mon_lvl = self.bluepyll_controller.image.img_txt_checker.read_text(
                player1_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            if mon_lvl and mon_lvl[0] and "lvl" in mon_lvl[0]:
                level = mon_lvl[0].strip("lvl").strip()
                if level.isdigit():
                    if int(level) > 100:
                        self.mon_on_field["level"] = 100
                    else:
                        self.mon_on_field["level"] = int(level)

            mon_hp = self.extract_health_percentage(player1_mon_hp_img.path)
            if mon_hp:
                self.mon_on_field["current_hp_percentage"] = float(f"{mon_hp:.2f}")

            opps_mon_name = self.bluepyll_controller.image.img_txt_checker.read_text(
                player2_mon_name_text.path
            )
            if opps_mon_name and opps_mon_name[0]:
                self.opps_mon_on_field["name"] = opps_mon_name[0]

            opps_mon_lvl = self.bluepyll_controller.image.img_txt_checker.read_text(
                player2_mon_lvl_text.path, allowlist="lvl1234567890 "
            )
            if opps_mon_lvl and opps_mon_lvl[0] and "lvl" in opps_mon_lvl[0]:
                level = opps_mon_lvl[0].strip("lvl").strip()
                if level.isdigit():
                    if int(level) > 100:
                        self.opps_mon_on_field["level"] = 100
                    else:
                        self.opps_mon_on_field["level"] = int(level)

            opps_mon_hp = self.extract_health_percentage(player2_mon_hp_img.path)
            if opps_mon_hp:
                self.opps_mon_on_field["current_hp_percentage"] = float(
                    f"{opps_mon_hp:.2f}"
                )

            self.logger.info("Initial battle info extracted successfully")
            self.logger.info(
                f"ME: NAME: {self.mon_on_field['name']} LEVEL: {self.mon_on_field['level']} CURRENT HP: {self.mon_on_field['current_hp_percentage']}%"
            )
            self.logger.info(
                f"OPPONENT: NAME: {self.opps_mon_on_field['name']} LEVEL: {self.opps_mon_on_field['level']} CURRENT HP: {self.opps_mon_on_field['current_hp_percentage']}%"
            )
        except Exception as e:
            self.logger.error(f"Error extracting initial battle info: {e}")

    def extract_battle_moves(self):
        def process_move_data(move_data: list[str]):
            try:
                # Post-processing to fix common OCR mistakes
                self.logger.info(f"Processing raw move data: {move_data}")
                if len(move_data) < 2:
                    self.logger.warning(
                        f"Incomplete move data, cannot process PP: {move_data}"
                    )
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
                self.logger.info(f"Processed move data: {move_data}")
                return move_data
            except Exception as e:
                self.logger.error(f"Error processing move data: {e}")
                return None

        try:
            screenshot_bytes = self.bluepyll_controller.adb.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            player1_mon_move1_button = self.screens["battle"].elements[
                "player1_mon_move1_button"
            ]
            player1_mon_move2_button = self.screens["battle"].elements[
                "player1_mon_move2_button"
            ]
            player1_mon_move3_button = self.screens["battle"].elements[
                "player1_mon_move3_button"
            ]
            player1_mon_move4_button = self.screens["battle"].elements[
                "player1_mon_move4_button"
            ]

            # Extract current battle moves info
            self.extract_regions(
                position_x_sizes=[
                    (
                        player1_mon_move1_button.position,
                        player1_mon_move1_button.size,
                        player1_mon_move1_button.label,
                    ),
                    (
                        player1_mon_move2_button.position,
                        player1_mon_move2_button.size,
                        player1_mon_move2_button.label,
                    ),
                    (
                        player1_mon_move3_button.position,
                        player1_mon_move3_button.size,
                        player1_mon_move3_button.label,
                    ),
                    (
                        player1_mon_move4_button.position,
                        player1_mon_move4_button.size,
                        player1_mon_move4_button.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            move_ui_elements = [
                player1_mon_move1_button,
                player1_mon_move2_button,
                player1_mon_move3_button,
                player1_mon_move4_button,
            ]

            for i, move_ui in enumerate(move_ui_elements):
                move_text = self.bluepyll_controller.image.img_txt_checker.read_text(
                    move_ui.path
                )
                if not move_text:
                    continue

                processed_move_data = process_move_data(move_text)
                if processed_move_data and len(processed_move_data) == 2:
                    try:
                        pp_parts = processed_move_data[1].split("/")
                        if len(pp_parts) == 2:
                            self.mon_on_field["moves"][i]["name"] = processed_move_data[
                                0
                            ]
                            self.mon_on_field["moves"][i]["pp"]["current"] = int(
                                pp_parts[0]
                            )
                            self.mon_on_field["moves"][i]["pp"]["total"] = int(
                                pp_parts[1]
                            )
                    except (ValueError, IndexError) as e:
                        self.logger.error(
                            f"Error parsing PP for move {i+1}: {processed_move_data[1]} - {e}"
                        )

            self.logger.info("Current battle moves info extracted successfully")
            self.logger.info(
                f"MOVES: {self.mon_on_field['moves'][0]} {self.mon_on_field['moves'][1]} {self.mon_on_field['moves'][2]} {self.mon_on_field['moves'][3]}"
            )
        except Exception as e:
            self.logger.error(f"Error extracting current battle moves info: {e}")

    def extract_battle_log(self):
        try:
            screenshot_bytes = self.bluepyll_controller.adb.capture_screenshot()
            if not screenshot_bytes:
                raise Exception("Failed to take screenshot")

            if self.is_main_menu_screen():
                self.logger.info("Closing main menu...")
                self.close_main_menu()
                self.logger.info("Battle over...")

            battle_log_image = self.screens["battle"].elements["battle_log_image"]

            # Extract initial battle info
            self.extract_regions(
                position_x_sizes=[
                    (
                        battle_log_image.position,
                        battle_log_image.size,
                        battle_log_image.label,
                    ),
                ],
                image=screenshot_bytes,
            )
            # Read text from the extracted regions
            battle_log = self.bluepyll_controller.image.img_txt_checker.read_text(
                battle_log_image.path
            )
            if battle_log:
                self.logger.info(f"Battle log: {battle_log}")
        except Exception as e:
            self.logger.error(f"Error extracting battle log region: {e}")

    @action
    def open_revomon_app(self) -> None:
        match self.app_state.current_state:
            case AppLifecycleState.CLOSED:
                self.open()

    @action
    def close_revomon_app(self) -> None:
        match self.app_state.current_state:
            case AppLifecycleState.READY | AppLifecycleState.LOADING:
                self.close()

    @requires_state(GameState.NOT_STARTED)
    @action
    def start_game(self) -> None:
        start_btn = self.screens["start_game"].elements["start_game_button"]
        if self.is_element_visible(start_btn):
            self.bluepyll_controller.click_element(start_btn)

    @requires_state(GameState.STARTED)
    @action
    def login(self) -> None:
        login_btn = self.screens["login"].elements["login_button"]
        relogin_btn = self.screens["login"].elements["relogin_button"]
        if self.is_element_visible(login_btn):
            self.bluepyll_controller.click_element(login_btn)
        elif self.is_element_visible(relogin_btn):
            self.bluepyll_controller.click_element(relogin_btn)

    @requires_state(GameState.OVERWORLD)
    @action
    def open_main_menu(self) -> None:
        main_menu_btn = self.screens["overworld"].elements["main_menu_button"]
        self.bluepyll_controller.click_element(main_menu_btn)

    @requires_state(GameState.MAIN_MENU)
    @action
    def close_main_menu(self) -> None:
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)

    @requires_state(GameState.MAIN_MENU, GameState.OVERWORLD)
    @action
    def enter_pvp_queue(self) -> None:
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()
        pvp_btn = self.screens["main_menu"].elements["pvp_button"]
        self.bluepyll_controller.click_element(pvp_btn)
        # TODO: Current missing a way to tell if the user is or isn't in the pvp queue.

    @requires_state(*LOGGED_IN_STATES)
    @action
    def exit_pvp_queue(self) -> None:
        self.open_main_menu()
        pvp_btn = self.screens["main_menu"].elements["pvp_button"]
        self.bluepyll_controller.click_element(pvp_btn)
        # TODO: Current missing a way to tell if the user is or isn't in the pvp queue.

    @requires_state(GameState.BATTLE)
    @action
    def run_from_battle(self) -> None:
        """
        Runs from the current battle if the user is in battle.

        Returns:
            None
        """
        if self.battle_sub_state == BattleState.BAG_OPEN:
            self.close_battle_bag()
        elif self.battle_sub_state == BattleState.ATTACKS_MENU_OPEN:
            self.close_attacks_menu()

        # Now we should be in IDLE or similar
        run_btn_pixel = self.screens["battle"].elements["run_button_pixel"]
        run_confirm_btn_pixel = self.screens["battle"].elements[
            "run_confirm_button_pixel"
        ]
        self.bluepyll_controller.click_coord(run_btn_pixel.center)
        sleep(1)
        self.bluepyll_controller.click_coord(run_confirm_btn_pixel.center)

    @requires_state(LOGGED_IN_STATES)
    @action
    def toggle_auto_run(self) -> None:
        """
        Toggles the auto run feature.
        Auto run feature runs from all battles automatically whenever the user gets in battle.

        Returns:
            None
        """
        match self.auto_run:
            case True:
                self.auto_run = False
            case False:
                self.auto_run = True

    @requires_state(LOGGED_IN_STATES)
    @action
    def toggle_auto_battle(self) -> None:
        """
        Toggles the auto battle feature.
        Auto battle feature automatically decides whether to run from battle or engage in battle.

        Returns:
            None
        """
        match self.auto_battle:
            case True:
                self.auto_battle = False
            case False:
                self.auto_battle = True

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_menu_bag(self) -> None:
        """
        Opens the menu bag if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            team_bag_btn = self.screens["main_menu"].elements["team_bag_menu_button"]
            self.bluepyll_controller.click_element(team_bag_btn)

    @requires_state(GameState.MENU_BAG)
    @action
    def close_menu_bag(self) -> None:
        """
        Closes the menu bag if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_wardrobe(self) -> None:
        # TODO: Implement a 'set_is_wardrobe_open' method
        """
        Opens the wardrobe if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            wardrobe_btn = self.screens["main_menu"].elements["wardrobe_button"]
            self.bluepyll_controller.click_element(wardrobe_btn)
            self.game_state = GameState.WARDROBE

    @requires_state(GameState.WARDROBE)
    @action
    def close_wardrobe(self) -> None:
        # TODO: Implement a 'set_is_wardrobe_open' method
        """
        Closes the wardrobe if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def recall_revomon(self) -> None:
        # TODO: Implement a 'set_is_mon_recalled' method
        """
        Recalls the revomon if it is not already recalled.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            recall_btn = self.screens["main_menu"].elements["recall_button"]
            self.bluepyll_controller.click_element(recall_btn)

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_friends_list(self) -> None:
        """
        Opens the friends list if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            friends_btn = self.screens["main_menu"].elements["friends_button"]
            self.bluepyll_controller.click_element(friends_btn)
            self.game_state = GameState.FRIENDS_LIST

    @requires_state(GameState.FRIENDS_LIST)
    @action
    def close_friends_list(self) -> None:
        """
        Closes the friends list if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_settings(self) -> None:
        """
        Opens the settings if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            settings_btn = self.screens["main_menu"].elements["settings_button"]
            self.bluepyll_controller.click_element(settings_btn)
            self.game_state = GameState.SETTINGS

    @requires_state(GameState.SETTINGS)
    @action
    def close_settings(self) -> None:
        """
        Closes the settings if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_revodex(self) -> None:
        """
        Opens the revodex if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            revodex_btn = self.screens["main_menu"].elements["revodex_button"]
            self.bluepyll_controller.click_element(revodex_btn)
            self.game_state = GameState.REVODEX

    @requires_state(GameState.REVODEX)
    @action
    def close_revodex(self) -> None:
        """
        Closes the revodex if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_market(self) -> None:
        """
        Opens the market if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            market_btn = self.screens["main_menu"].elements["market_button"]
            self.bluepyll_controller.click_element(market_btn)
            self.game_state = GameState.MARKET

    @requires_state(GameState.MARKET)
    @action
    def close_market(self) -> None:
        """
        Closes the market if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_discussion(self) -> None:
        """
        Opens the discussion if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            discussion_btn = self.screens["main_menu"].elements["discussion_button"]
            self.bluepyll_controller.click_element(discussion_btn)
            self.game_state = GameState.DISCUSSION

    @requires_state(GameState.DISCUSSION)
    @action
    def close_discussion(self) -> None:
        """
        Closes the discussion if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def open_clan(self) -> None:
        """
        Opens the clan menu if it is not already open.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            clan_btn = self.screens["main_menu"].elements["clan_button"]
            self.bluepyll_controller.click_element(clan_btn)
            self.game_state = GameState.CLAN

    @requires_state(GameState.CLAN)
    @action
    def close_clan(self) -> None:
        """
        Closes the clan menu if it is open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.game_state = GameState.MAIN_MENU

    @requires_state(GameState.BATTLE)
    @action
    def open_attacks_menu(self) -> None:
        """
        Opens the attacks menu if it is not already open.
        User must be in battle and not already have the attacks menu open.

        Returns:
            None
        """
        # Click attacks button using coordinates from battle screen
        attacks_btn = self.screens["battle"].elements["attacks_button"]
        self.bluepyll_controller.click_element(attacks_btn)
        self.battle_sub_state = BattleState.ATTACKS_MENU_OPEN

    @requires_state(GameState.BATTLE)
    @action
    def choose_move(self, strategy: BattleStrategy | None = None) -> None:
        """
        Chooses a move to use in battle using the provided strategy.

        Args:
            strategy (BattleStrategy | None, optional): The strategy to use for selecting a move.
                Defaults to RandomMove if None.

        Returns:
            None

        Raises:
            ValueError: If not in battle or in an invalid battle state
            RuntimeError: If no valid moves are available or if there's an error selecting a move
        """
        try:
            # Default to RandomMove if no strategy provided
            if self.auto_run is True:
                self.run_from_battle()
                return "ran from battle"
            if self.auto_battle is True:
                self.open_attacks_menu()

                if strategy is None:
                    strategy = RandomMove()

                # Get all valid moves (non-None names with PP > 0)
                valid_moves = [
                    move
                    for move in self.mon_on_field["moves"]
                    if move.get("name") is not None
                    and move.get("pp", {}).get("current", 0) > 0
                ]

                # Early exit if no valid moves
                if not valid_moves:
                    raise RuntimeError(
                        "No valid moves found (all moves have 0 PP or None names)"
                    )

                valid_move_names = [move["name"] for move in valid_moves]
                if not valid_move_names:
                    raise RuntimeError("No valid moves available for selection")

                # Use strategy to select move
                move_name = strategy.select_move(valid_move_names)

                # Verify the selected move is valid
                if move_name not in valid_move_names:
                    raise ValueError(
                        f"Strategy selected invalid move '{move_name}'. Valid moves: {valid_move_names}"
                    )

                # Find the original index from the full moves list for UI clicking
                try:
                    original_index = next(
                        i
                        for i, move in enumerate(self.mon_on_field["moves"])
                        if move.get("name") == move_name
                    )
                except StopIteration:
                    raise RuntimeError(f"Failed to find move in moves list: {move_name}")

                move_button_keys = [
                    "player1_mon_move1_button",
                    "player1_mon_move2_button",
                    "player1_mon_move3_button",
                    "player1_mon_move4_button",
                ]

                if 0 <= original_index < len(move_button_keys):
                    move_btn = self.screens["battle"].elements[
                        move_button_keys[original_index]
                    ]
                    self.bluepyll_controller.click_element(move_btn)
                    return move_name
                else:
                    raise RuntimeError(
                        f"Move index {original_index} out of range for move: {move_name}"
                    )
            sleep(1)
        except Exception as e:
            self.logger.error(f"Error in choose_move: {str(e)}")
            raise  # Re-raise the exception after logging

    @requires_state(GameState.BATTLE)
    @action
    def close_attacks_menu(self) -> None:
        """
        Closes the attacks menu if it is open.
        User must be in battle and attacks menu must be open.

        Returns:
            None
        """
        exit_attacks_btn = self.screens["battle"].elements["exit_attacks_button"]
        self.bluepyll_controller.click_element(exit_attacks_btn)
        self.battle_sub_state = BattleState.IDLE

    @requires_state(GameState.BATTLE)
    @action
    def open_battle_bag(self) -> None:
        """
        Opens the battle bag if it is not already open.
        User must be in battle and battle bag must not be open.

        Returns:
            None
        """
        battle_bag_btn = self.screens["battle"].elements["team_bag_battle_button"]
        self.bluepyll_controller.click_element(battle_bag_btn)
        self.battle_sub_state = BattleState.BAG_OPEN

    @requires_state(GameState.BATTLE)
    @action
    def close_battle_bag(self) -> None:
        """
        Closes the battle bag if it is open.
        User must be in battle and battle bag must be open.

        Returns:
            None
        """
        exit_menu_btn = self.screens["main_menu"].elements["exit_menu_button"]
        self.bluepyll_controller.click_element(exit_menu_btn)
        self.battle_sub_state = BattleState.IDLE

    @requires_state(GameState.OVERWORLD)
    @action
    def open_tv(self) -> None:
        """
        Opens the TV if it is not already open.
        User must be in the Revocenter (Overworld).

        Returns:
            None
        """
        tv_screen_button = self.screens["revocenter"].elements["tv_screen_button"]
        self.bluepyll_controller.click_element(tv_screen_button, times=2)
        self.game_state = GameState.TV

    @requires_state(GameState.TV)
    @action
    def close_tv(self) -> None:
        """
        Closes the TV if it is open.
        User must be logged in.

        Returns:
            None
        """
        tv_exit_button = self.screens["tv"].elements["tv_exit_button"]
        self.bluepyll_controller.click_element(tv_exit_button)
        self.game_state = GameState.OVERWORLD

    @requires_state(GameState.TV)
    @action
    def tv_search_for_revomon(self, revomon_name: str) -> None:
        # TODO: Implement a 'set_is_searching_for_mon' method
        """
        Searches for a revomon in the TV.
        User must be logged in and the TV must be open.

        Args:
            revomon_name (str): The name of the revomon to search for.

        Returns:
            None
        """
        tv_search_input = self.screens["tv"].elements["tv_search_input"]
        self.bluepyll_controller.click_element(tv_search_input)
        sleep(1)
        self.bluepyll_controller.adb.type_text(revomon_name)
        sleep(2)
        tv_search_button = self.screens["tv"].elements["tv_search_button"]
        self.bluepyll_controller.click_element(tv_search_button)
        self.mon_searching_for = revomon_name

    @requires_state(GameState.TV)
    @action
    def select_tv_slot(self, slot_number: int) -> None:
        # TODO: Implement a 'set_is_mon_selected' method
        """
        Selects a specific slot in the TV.
        User must be logged in and the TV must be open.

        Args:
            slot_number (int): The number of the slot you want to select in the TV

        Returns:
            None
        """
        print(f"SELECTING SLOT #: {slot_number}")
        if slot_number != self.tv_slot_selected:
            tv_slot_button = self.screens["tv"].elements[
                f"tv_slot{slot_number - 1}_button"
            ]
            self.bluepyll_controller.click_element(tv_slot_button)
            self.tv_slot_selected = slot_number - 1
            self.is_mon_selected = True

    @requires_state(GameState.OVERWORLD, GameState.MAIN_MENU)
    @action
    def quit_game(self) -> None:
        """
        Quits the game if the user is logged in and not in battle.
        User must be logged in.

        Returns:
            None
        """
        if self.game_state == GameState.OVERWORLD:
            self.open_main_menu()

        if self.game_state == GameState.MAIN_MENU:
            quit_game_button = self.screens["main_menu"].elements["quit_game_button"]
            self.bluepyll_controller.click_element(quit_game_button)

    # STATE UPDATE FUNCTIONS
    def update_world_state(
        self,
        new_app_state: AppLifecycleState | None = None,
        new_game_state: GameState | None = None,
        new_battle_sub_state: BattleState | None = None,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> None:

        if new_app_state:
            if self.app_state.current_state != new_app_state:
                self.app_state.transition_to(
                    new_app_state, ignore_validation=ignore_state_change_validation
                )
                self.logger.info(f"App state updated to: {new_app_state}")
            else:
                self.logger.info(f"App state is already: {new_app_state}")

        if new_game_state:
            if self.game_state != new_game_state:
                self.game_state = new_game_state
                self.logger.info(f"Game state updated to: {new_game_state}")
            else:
                self.logger.info(f"Game state is already: {new_game_state}")

        if new_battle_sub_state:
            if self.battle_sub_state != new_battle_sub_state:
                self.battle_sub_state = new_battle_sub_state
                self.logger.info(f"Battle sub-state updated to: {new_battle_sub_state}")
            else:
                self.logger.info(f"Battle sub-state is already: {new_battle_sub_state}")

        if not any([new_app_state, new_game_state, new_battle_sub_state]):
            self.logger.info("No state changes provided.")
            self.logger.info("Scanning for current screen...")
            screenshot_bytes = (
                bluepyll_screenshot or self.bluepyll_controller.adb.capture_screenshot()
            )
            if any(
                [
                    self.is_start_game_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_login_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_overworld_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_tv_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_team_bag_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_main_menu_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_on_battle_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                    self.is_attacks_menu_screen(
                        bluepyll_screenshot=screenshot_bytes,
                        ignore_state_change_validation=True,
                    ),
                ]
            ):
                self.logger.info("Current screen detected. World state updated.")
                self.logger.info(f"Detected screen: {self.curr_screen}")
            else:
                self.logger.info("New World State initialized.")

    def is_start_game_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the start game screen.
        Passing this check means the app is open and loaded.

        Args:
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the start game screen, False otherwise.
        """
        # Start Game Screen Scene
        match self.screens["start_game"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.NOT_STARTED,
                    new_battle_sub_state=BattleState.IDLE,
                    ignore_state_change_validation=ignore_state_change_validation,
                )
                self.curr_screen = "start_game"
                return True
            case _:
                return False

    def is_login_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the login screen.
        Passing this check means the app is open, loaded and started.

        Args:
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the login screen, False otherwise.
        """
        # Login Screen Scene
        match self.screens["login"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.STARTED,
                    new_battle_sub_state=BattleState.IDLE,
                    ignore_state_change_validation=ignore_state_change_validation,
                )
                self.curr_screen = "login"
                return True
            case _:
                return False

    def is_overworld_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the overworld screen(no menu's are open and not in any battle).
        Passing this check means the app is open, loaded, started and the User is logged in.

        Args:
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the overworld screen, False otherwise.
        """
        # Overworld Screen Scene
        match self.screens["overworld"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.OVERWORLD,
                    new_battle_sub_state=BattleState.IDLE,
                    ignore_state_change_validation=ignore_state_change_validation,
                )
                self.curr_screen = "overworld"
                return True
            case _:
                return False

    def is_tv_screen(
        self,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the TV screen(TV is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the TV is open.

        Args:
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the TV screen, False otherwise.
        """
        try:
            tv_advanced_search_button = self.screens["tv_advanced_search"].elements[
                "tv_advanced_search_button"
            ]
            match self.is_element_visible(tv_advanced_search_button):
                case True:
                    self.update_world_state(
                        new_app_state=AppLifecycleState.READY,
                        new_game_state=GameState.TV,
                        new_battle_sub_state=BattleState.IDLE,
                        ignore_state_change_validation=ignore_state_change_validation,
                    )
                    self.curr_screen = "tv_advanced_search"
                    return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_tv_screen': {e}")

    def is_team_bag_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the team bag screen(team bag is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the team bag is open.

        Args:
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the team bag screen, False otherwise.
        """
        try:
            match self.screens["team_bag"].is_current_screen(
                bluepyll_controller=self.bluepyll_controller,
                bluepyll_screenshot=bluepyll_screenshot,
            ):
                case True:
                    print(self.game_state)
                    if self.game_state == GameState.BATTLE:
                        print("Team battle bag screen detected")
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.BATTLE,
                            new_battle_sub_state=BattleState.BAG_OPEN,
                            ignore_state_change_validation=ignore_state_change_validation,
                        )
                        self.curr_screen = "battle_bag"
                        return True
                    elif self.game_state == GameState.MAIN_MENU:
                        print("Team menu bag screen detected")
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.MENU_BAG,
                            new_battle_sub_state=BattleState.IDLE,
                            ignore_state_change_validation=ignore_state_change_validation,
                        )
                        self.curr_screen = "menu_bag"
                        return True
                case _:
                    return False

        except Exception as e:
            raise Exception(f"error during 'is_team_bag_screen': {e}")

    def is_main_menu_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the main menu screen(main menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in and the main menu is open.

        Args:
            bluepyll_screenshot (bytes | None, optional): The screenshot to check. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the main menu screen, False otherwise.
        """
        match self.screens["main_menu"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.MAIN_MENU,
                    new_battle_sub_state=BattleState.IDLE,
                    ignore_state_change_validation=ignore_state_change_validation,
                )
                self.curr_screen = "main_menu"
                return True
            case _:
                return False

    def is_on_battle_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the in battle screen(User in battle).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the battle bag is closed.

        Args:
            bluepyll_screenshot (bytes | None, optional): The screenshot to check. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the in battle screen, False otherwise.
        """
        match self.screens["battle"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.BATTLE,
                    new_battle_sub_state=BattleState.IDLE,
                    ignore_state_change_validation=ignore_state_change_validation,
                )

                self.curr_screen = "in_battle"
                self.extract_battle_info()
                return True
            case _:
                return False

    def is_attacks_menu_screen(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        """
        Checks if the Revomon app is on the attacks menu screen(attacks menu is open).
        Passing this check means the app is open, loaded, started, the User is logged in, in a battle and the attacks menu is open.

        Args:
            bluepyll_screenshot (bytes | None, optional): The screenshot to check. Defaults to None.
            ignore_state_change_validation (bool, optional): Whether to ignore state change validation. Defaults to False.

        Returns:
            bool: True if the app is on the attacks menu screen, False otherwise.
        """
        match self.screens["battle"].is_current_screen(
            bluepyll_controller=self.bluepyll_controller,
            bluepyll_screenshot=bluepyll_screenshot,
            phase="attacks_menu",
        ):
            case True:
                self.update_world_state(
                    new_app_state=AppLifecycleState.READY,
                    new_game_state=GameState.BATTLE,
                    new_battle_sub_state=BattleState.ATTACKS_MENU_OPEN,
                    ignore_state_change_validation=ignore_state_change_validation,
                )
                self.curr_screen = "attacks_menu"
                self.extract_battle_moves()
                return True
            case _:
                return False

    def is_waiting_for_opponent(
        self,
        bluepyll_screenshot: bytes | None = None,
        ignore_state_change_validation: bool = False,
    ) -> bool:
        try:
            screenshot_bytes = (
                bluepyll_screenshot or self.bluepyll_controller.adb.capture_screenshot()
            )
            waiting_for_opponent_text = self.screens["battle"].elements[
                "waiting_for_opponent_text"
            ]
            # Extract waiting for opponent text
            self.extract_regions(
                position_x_sizes=[
                    (
                        waiting_for_opponent_text.position,
                        waiting_for_opponent_text.size,
                        waiting_for_opponent_text.label,
                    ),
                ],
                image=screenshot_bytes,
            )

            # Read text from the extracted regions
            result = self.bluepyll_controller.image.img_txt_checker.read_text(
                waiting_for_opponent_text.path
            )
            if len(result) > 0:
                for text in result:
                    if "for opponent" in str(text).lower():
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.BATTLE,
                            new_battle_sub_state=BattleState.WAITING_FOR_OPPONENT,
                            ignore_state_change_validation=ignore_state_change_validation,
                        )
                        self.curr_screen = "battle"
                        return True
            return False
        except Exception as e:
            raise Exception(f"Error setting is_waiting_for_opponent(): {e}")

    def wait_for_action(self, action: str):
        try:
            while True:
                self.logger.info(f"Waiting for {action} action to complete...")
                screenshot_bytes = self.bluepyll_controller.adb.capture_screenshot()
                match action:
                    case "open_revomon_app":
                        match self.is_start_game_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                self.logger.info("Revomon app opened successfully.")
                                return
                    case "close_revomon_app":
                        match self.bluepyll_controller.adb.is_app_running(
                            app=self, timeout=10, wait_time=10
                        ):
                            case False:
                                self.update_world_state(
                                    new_app_state=AppLifecycleState.CLOSED,
                                    new_game_state=GameState.NOT_STARTED,
                                    new_battle_sub_state=BattleState.IDLE,
                                )
                                self.curr_screen = None
                                self.logger.info("Revomon app closed successfully.")
                                return
                    case "start_game":
                        match self.is_login_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                self.logger.info("Game started successfully.")
                                return
                            case False:
                                continue
                    case "login":
                        match self.is_overworld_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_main_menu":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_main_menu":
                        match self.is_overworld_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                print("-->Main menu closed successfully.")
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "enter_pvp_queue":
                        # TODO: Implement a way to tell if user is/isn't in pvp queue. For now, just assume the user joined the queue successfully.
                        self.is_pvp_queued = True
                        self.logger.info("Entered PvP Queue successfully.")
                        return
                    case "exit_pvp_queue":
                        # TODO: Implement a way to tell if user is/isn't in pvp queue. For now, just assume the user exited the queue successfully.
                        self.is_pvp_queued = False
                        self.logger.info("Exited PvP Queue successfully.")
                        return

                    case "toggle_auto_run":
                        return
                    case "run_from_battle":
                        match self.is_overworld_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                        match self.is_login_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                    case "open_menu_bag":
                        match self.is_team_bag_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_menu_bag":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_wardrobe":
                        # TODO: Implement a way to tell if user is/isn't in wardrobe. For now, just assume the user opened the wardrobe successfully.
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.WARDROBE,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "wardrobe_menu"
                        return
                    case "close_wardrobe":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
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
                            new_game_state=GameState.FRIENDS_LIST,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "friends_list_menu"
                        return
                    case "close_friends_list":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_settings":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.SETTINGS,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "settings_menu"
                        return
                    case "close_settings":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_revodex":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.REVODEX,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "revodex_menu"
                        return
                    case "close_revodex":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_market":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.MARKET,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "market_menu"
                        return
                    case "close_market":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_discussion":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.DISCUSSION,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "discussion_menu"
                        return
                    case "close_discussion":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_clan":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.CLAN,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "clan_menu"
                        return
                    case "close_clan":
                        match self.is_main_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_attacks_menu":
                        match self.is_attacks_menu_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_login_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "choose_move":
                        match self.is_waiting_for_opponent(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                sleep(0.5)
                                continue
                        match self.is_overworld_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                self.logger.info("Opening main menu...")
                                self.open_main_menu()
                                self.logger.info("Extracting battle log...")
                                self.extract_battle_log()
                                return
                        match self.is_on_battle_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                self.logger.info("Extracting battle log...")
                                self.extract_battle_log()
                                return
                        match self.is_login_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                        continue
                    case "close_attacks_menu":
                        match self.is_on_battle_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_login_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_battle_bag":
                        match self.is_team_bag_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_login_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "close_battle_bag":
                        match self.is_on_battle_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_login_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        continue
                    case "open_available_bag":
                        match self.is_team_bag_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_available_bag":
                        match self.is_team_bag_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "open_tv":
                        match self.is_tv_screen(bluepyll_screenshot=screenshot_bytes):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "close_tv":
                        match self.is_overworld_screen(
                            bluepyll_screenshot=screenshot_bytes
                        ):
                            case True:
                                return
                            case False:
                                match self.is_on_battle_screen(
                                    bluepyll_screenshot=screenshot_bytes
                                ):
                                    case True:
                                        return
                                    case False:
                                        match self.is_login_screen(
                                            bluepyll_screenshot=screenshot_bytes
                                        ):
                                            case True:
                                                return
                                            case False:
                                                continue
                    case "tv_search_for_revomon":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.TV,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "tv"
                        return
                    case "tv_select_revomon":
                        self.update_world_state(
                            new_app_state=AppLifecycleState.READY,
                            new_game_state=GameState.TV,
                            new_battle_sub_state=BattleState.IDLE,
                        )
                        self.curr_screen = "tv"
                        return
                    case "quit_game":
                        match not self.bluepyll_controller.adb.is_app_running(
                            app=self, timeout=10, wait_time=10
                        ):
                            case True:
                                self.update_world_state(
                                    new_app_state=AppLifecycleState.CLOSED,
                                    new_game_state=GameState.NOT_STARTED,
                                    new_battle_sub_state=BattleState.IDLE,
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
            inside_revocenter_landmark = self.screens["landmark"].elements[
                "inside_revocenter_landmark"
            ]
            match self.bluepyll_controller.is_element_visible(
                inside_revocenter_landmark
            ):
                case tuple():
                    self.current_location = "inside revocenter"
                    return
            outside_revocenter_landmark = self.screens["landmark"].elements[
                "outside_revocenter_landmark"
            ]
            match self.bluepyll_controller.is_element_visible(
                outside_revocenter_landmark
            ):
                case tuple():
                    self.current_location = "outside revocenter"
                    self.current_city = "arktos"
                    return
        except Exception as e:
            raise Exception(f"Error updating location: {e}")

        return self.location, self.current_city

    def reset(self, auto_update: bool = False) -> None:
        self.curr_screen = None
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
