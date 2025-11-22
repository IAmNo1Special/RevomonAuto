from bluepyll import BluePyllScreen

from ..elements import main_menu_elements


class MainMenuScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="main_menu",
            elements={
                "tamer_name_text": main_menu_elements.TamerNameText(),
                "tamer_selfie_img": main_menu_elements.TamerSelfieImg(),
                "exit_menu_button": main_menu_elements.ExitMenuButton(),
                "exit_menu_pixel": main_menu_elements.ExitMenuPixel(),
                "wardrobe_button": main_menu_elements.WardrobeButton(),
                "team_bag_menu_button": main_menu_elements.TeamBagMenuButton(),
                "recall_button": main_menu_elements.RecallButton(),
                "friends_button": main_menu_elements.FriendsButton(),
                "settings_button": main_menu_elements.SettingsButton(),
                "revodex_button": main_menu_elements.RevodexButton(),
                "market_button": main_menu_elements.MarketButton(),
                "discussion_button": main_menu_elements.DiscussionButton(),
                "pvp_button": main_menu_elements.PvpButton(),
                "clan_button": main_menu_elements.ClanButton(),
                "quit_game_button": main_menu_elements.QuitGameButton(),
                "quit_game_pixel": main_menu_elements.QuitGamePixel(),
            },
        )

    def is_current_screen(
        self, bluepyll_controller, bluepyll_screenshot: bytes | None = None
    ) -> bool:
        """
        Checks if the Revomon app is on the main menu screen.

        Args:
            bluepyll_controller (BluePyllController): BluePyll controller instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the main menu screen, False otherwise.
        """
        # Main Menu Screen Scene
        bluepyll_screenshot = (
            bluepyll_screenshot or bluepyll_controller.adb.capture_screenshot()
        )

        exit_menu_pixel = self.elements["exit_menu_pixel"]
        quit_game_pixel = self.elements["quit_game_pixel"]
        return all(
            [
                bluepyll_controller.image.check_pixel_color(
                    target_coords=exit_menu_pixel.center,
                    target_color=exit_menu_pixel.pixel_color,
                    image=bluepyll_screenshot,
                ),
                bluepyll_controller.image.check_pixel_color(
                    target_coords=quit_game_pixel.center,
                    target_color=quit_game_pixel.pixel_color,
                    image=bluepyll_screenshot,
                ),
            ]
        )
