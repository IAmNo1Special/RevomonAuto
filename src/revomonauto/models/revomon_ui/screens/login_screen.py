from bluepyll import BluePyllScreen

from ..elements import login_elements


class LoginScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="login",
            elements={
                "login_button": login_elements.LoginButton(),
                "relogin_button": login_elements.ReloginButton(),
                "login_pixel": login_elements.LoginPixel(),
                "disconnect_button": login_elements.DisconnectButton(),
                "disconnect_pixel": login_elements.DisconnectPixel(),
                "server_select_pixel": login_elements.ServerSelectPixel(),
                "revomon_badge_pixel": login_elements.RevomonBadgePixel(),
            },
        )

    def is_current_screen(
        self,
        bluepyll_controller,
        bluepyll_screenshot: bytes | None = None,
    ) -> bool:
        """
        Checks if the Revomon app is on the login screen.
        Args:
            bluepyll_controller (BluePyllController): The BluePyllController instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the login screen, False otherwise.
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
            login_pixel = self.elements["login_pixel"]
            disconnect_pixel = self.elements["disconnect_pixel"]
            server_select_pixel = self.elements["server_select_pixel"]
            revomon_badge_pixel = self.elements["revomon_badge_pixel"]
            return all(
                [
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=login_pixel.center,
                        target_color=login_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=disconnect_pixel.center,
                        target_color=disconnect_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=server_select_pixel.center,
                        target_color=server_select_pixel.pixel_color,
                        image=bluepyll_screenshot,
                    ),
                    bluepyll_controller.image.check_pixel_color(
                        target_coords=disconnect_pixel.center,
                        target_color=disconnect_pixel.pixel_color,
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
