from bluepyll import BluePyllScreen

from ..elements import start_game_elements


class StartGameScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="start_game",
            elements={
                "start_game_button": start_game_elements.StartGameButton(),
                "start_game_pixel": start_game_elements.StartGamePixel(),
                "quality_decrease_button": start_game_elements.QualityDecreaseButton(),
                "quality_decrease_pixel": start_game_elements.QualityDecreasePixel(),
                "quality_increase_button": start_game_elements.QualityIncreaseButton(),
                "quality_increase_pixel": start_game_elements.QualityIncreasePixel(),
                "current_quality_text": start_game_elements.CurrentQualityText(),
                "current_version_text": start_game_elements.CurrentVersionText(),
                "game_update_text": start_game_elements.GameUpdateText(),
                "revomon_badge_pixel": start_game_elements.RevomonBadgePixel(),
            },
        )

    def is_current_screen(
        self, bluepyll_controller, bluepyll_screenshot: bytes | None = None
    ) -> bool:
        """
        Checks if the Revomon app is on the start game screen.

        Args:
            bluepyll_controller (BluePyllController): BluePyll controller instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the start game screen, False otherwise.
        """
        # Start Game Screen Scene
        try:
            bluepyll_screenshot = (
                bluepyll_screenshot or bluepyll_controller.adb.capture_screenshot()
            )
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return False

        try:
            start_game_pixel = self.elements["start_game_pixel"]
            quality_decrease_pixel = self.elements["quality_decrease_pixel"]
            quality_increase_pixel = self.elements["quality_increase_pixel"]
            revomon_badge_pixel = self.elements["revomon_badge_pixel"]
            return all(
                [
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=start_game_pixel.center,
                        target_color=start_game_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=quality_decrease_pixel.center,
                        target_color=quality_decrease_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=quality_increase_pixel.center,
                        target_color=quality_increase_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=revomon_badge_pixel.center,
                        target_color=revomon_badge_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                ]
            )
        except Exception as e:
            self.logger.error(
                f"Failed to check if app is on the {self.name} screen: {e}"
            )
            return False
