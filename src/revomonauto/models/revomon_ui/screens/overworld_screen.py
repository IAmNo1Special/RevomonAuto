from bluepyll import BluePyllScreen

from ..elements import overworld_elements


class OverworldScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="overworld",
            elements={
                "current_time_text": overworld_elements.CurrentTimeText(),
                "day_time_pixel": overworld_elements.DayTimePixel(),
                "night_time_pixel": overworld_elements.NightTimePixel(),
                "main_menu_button": overworld_elements.MainMenuButton(),
                "main_menu_pixel": overworld_elements.MainMenuPixel(),
                "release_first_mon_button": overworld_elements.ReleaseFirstMonButton(),
                "release_first_mon_pixel": overworld_elements.ReleaseFirstMonPixel(),
                "aim_shoot_button": overworld_elements.AimShootButton(),
                "aim_shoot_pixel": overworld_elements.AimShootPixel(),
            },
        )

    def is_current_screen(
        self, bluepyll_controller, bluepyll_screenshot: bytes | None = None
    ) -> bool:
        """
        Checks if the Revomon app is on the overworld screen.

        Args:
            bluepyll_controller (BluePyllController): BluePyll controller instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the overworld screen, False otherwise.
        """
        # Overworld Screen Scene
        try:
            bluepyll_screenshot = (
                bluepyll_screenshot or bluepyll_controller.adb.capture_screenshot()
            )
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return False

        try:
            main_menu_pixel = self.elements["main_menu_pixel"]
            release_first_mon_pixel = self.elements["release_first_mon_pixel"]
            aim_shoot_pixel = self.elements["aim_shoot_pixel"]
            return all(
                [
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=main_menu_pixel.center,
                        target_color=main_menu_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=release_first_mon_pixel.center,
                        target_color=release_first_mon_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=aim_shoot_pixel.center,
                        target_color=aim_shoot_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                ]
            )
        except Exception as e:
            self.logger.error(
                f"Failed to check if app is on the {self.name} screen: {e}"
            )
            return False
