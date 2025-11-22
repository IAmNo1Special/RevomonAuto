from bluepyll import BluePyllScreen

from ..elements import battle_elements


class BattleScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="battle",
            elements={
                "run_button": battle_elements.run_button,
                "run_button_pixel": battle_elements.run_button_pixel,
                "run_confirm_button_pixel": battle_elements.run_confirm_button_pixel,
                "team_bag_battle_button": battle_elements.team_bag_battle_button,
                "team_bag_battle_pixel": battle_elements.team_bag_battle_pixel,
                "attacks_button": battle_elements.attacks_button,
                "attacks_button_pixel": battle_elements.attacks_button_pixel,
                "exit_attacks_button": battle_elements.exit_attacks_button,
                "exit_attacks_button_pixel": battle_elements.exit_attacks_button_pixel,
                "player1_mon_name_text": battle_elements.player1_mon_name_text,
                "player1_mon_nameplate_pixel": battle_elements.player1_mon_nameplate_pixel,
                "player1_mon_lvl_text": battle_elements.player1_mon_lvl_text,
                "player1_mon_hp_img": battle_elements.player1_mon_hp_img,
                "player1_mon_move1_button": battle_elements.player1_mon_move1_button,
                "player1_mon_move2_button": battle_elements.player1_mon_move2_button,
                "player1_mon_move3_button": battle_elements.player1_mon_move3_button,
                "player1_mon_move4_button": battle_elements.player1_mon_move4_button,
                "player2_mon_name_text": battle_elements.player2_mon_name_text,
                "player2_mon_nameplate_pixel": battle_elements.player2_mon_nameplate_pixel,
                "player2_mon_lvl_text": battle_elements.player2_mon_lvl_text,
                "player2_mon_hp_img": battle_elements.player2_mon_hp_img,
                "waiting_for_opponent_text": battle_elements.waiting_for_opponent_text,
                "battle_log_image": battle_elements.battle_log_image,
            },
        )

    def is_current_screen(
        self,
        bluepyll_controller,
        bluepyll_screenshot: bytes | None = None,
        phase: str = None,
    ) -> bool:
        """
        Checks if the Revomon app is on the battle screen.

        Args:
            bluepyll_controller (BluePyllController): BluePyll controller instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the battle screen, False otherwise.
        """
        # Battle Screen Scene
        try:
            bluepyll_screenshot = (
                bluepyll_screenshot or bluepyll_controller.adb.capture_screenshot()
            )
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return False

        try:
            if phase is None:
                # Checking for the green in the Revomon name plates that appear during battle (Player1, Player2)
                player1_mon_nameplate_pixel = self.elements[
                    "player1_mon_nameplate_pixel"
                ]
                player2_mon_nameplate_pixel = self.elements[
                    "player2_mon_nameplate_pixel"
                ]
                return all(
                    [
                        bluepyll_controller.image.check_pixel_color(
                            target_coords=player1_mon_nameplate_pixel.center,
                            target_color=player1_mon_nameplate_pixel.pixel_color,
                            image=bluepyll_screenshot,
                        ),
                        bluepyll_controller.image.check_pixel_color(
                            target_coords=player2_mon_nameplate_pixel.center,
                            target_color=player2_mon_nameplate_pixel.pixel_color,
                            image=bluepyll_screenshot,
                        ),
                    ]
                )
            elif phase == "attacks_menu":
                exit_attacks_button_pixel = self.elements["exit_attacks_button_pixel"]
                return bluepyll_controller.image.check_pixel_color(
                    target_coords=exit_attacks_button_pixel.center,
                    target_color=exit_attacks_button_pixel.pixel_color,
                    image=bluepyll_screenshot,
                )
        except Exception as e:
            self.logger.error(
                f"Failed to check if app is on the {self.name} screen: {e}"
            )
            return False
