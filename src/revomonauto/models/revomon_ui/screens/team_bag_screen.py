from bluepyll import BluePyllScreen

from ..elements import team_bag_elements


class TeamBagScreen(BluePyllScreen):
    """Team Bag Screen for Revomon app."""

    def __init__(self):
        super().__init__(
            name="team_bag",
            elements={
                "change_bag_left_button": team_bag_elements.change_bag_left_button,
                "change_bag_right_button": team_bag_elements.change_bag_right_button,
                "remove_from_team_button": team_bag_elements.remove_from_team_button,
                "remove_item_button": team_bag_elements.remove_item_button,
                "set_first_button": team_bag_elements.set_first_button,
            },
        )
