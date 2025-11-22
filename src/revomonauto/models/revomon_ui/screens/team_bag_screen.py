from bluepyll import BluePyllScreen

from ..elements import team_bag_elements


class TeamBagScreen(BluePyllScreen):
    """Team Bag Screen for Revomon app."""

    def __init__(self):
        super().__init__(
            name="team_bag",
            elements={
                "change_bag_left_button": team_bag_elements.change_bag_left_button,
                "change_bag_left_pixel": team_bag_elements.ChangeBagLeftPixel(),
                "change_bag_right_button": team_bag_elements.change_bag_right_button,
                "change_bag_right_pixel": team_bag_elements.ChangeBagRightPixel(),
                "remove_from_team_button": team_bag_elements.remove_from_team_button,
                "remove_from_team_pixel": team_bag_elements.RemoveFromTeamPixel(),
                "remove_item_button": team_bag_elements.remove_item_button,
                "remove_item_pixel": team_bag_elements.RemoveItemPixel(),
                "set_first_button": team_bag_elements.set_first_button,
                "set_first_pixel": team_bag_elements.SetFirstPixel(),
                "send_to_battle_button": team_bag_elements.send_to_battle_button,
                "send_to_battle_pixel": team_bag_elements.SendToBattlePixel(),
                "no_item_equipped_pixel": team_bag_elements.NoItemEquippedPixel(),
            },
        )

    def is_current_screen(
        self, bluepyll_controller, bluepyll_screenshot: bytes | None = None
    ) -> bool:
        """
        Checks if the Revomon app is on the team bag screen.

        Args:
            bluepyll_controller (BluePyllController): BluePyll controller instance.
            bluepyll_screenshot (bytes | None, optional): Screenshot of the app. Defaults to None.

        Returns:
            bool: True if the app is on the team bag screen, False otherwise.
        """
        # Team Bag Screen Scene
        bluepyll_screenshot = (
            bluepyll_screenshot or bluepyll_controller.adb.capture_screenshot()
        )

        change_bag_left_pixel = self.elements["change_bag_left_pixel"]
        change_bag_right_pixel = self.elements["change_bag_right_pixel"]
        return all(
            [
                bluepyll_controller.image.check_pixel_color(
                    target_coords=change_bag_left_pixel.center,
                    target_color=change_bag_left_pixel.pixel_color,
                    image=bluepyll_screenshot,
                ),
                bluepyll_controller.image.check_pixel_color(
                    target_coords=change_bag_right_pixel.center,
                    target_color=change_bag_right_pixel.pixel_color,
                    image=bluepyll_screenshot,
                ),
            ]
        )
