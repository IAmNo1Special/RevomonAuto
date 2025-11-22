from pathlib import Path

from bluepyll import BluePyllElement

BASE_DIR = Path(__file__).parent.parent

change_bag_left_button = BluePyllElement(
    label="change_bag_left_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "change_bag_left_button.png"),
    is_static=True,
    confidence=0.6,
)

class ChangeBagLeftPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="change_bag_left_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(78, 251),
            size=(1, 1),
            pixel_color=(71, 231, 168),
        )

change_bag_right_button = BluePyllElement(
    label="change_bag_right_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(
        BASE_DIR / "assets" / "team_bag_assets" / "change_bag_right_button.png"
    ),
    is_static=True,
    confidence=0.6,
)

class ChangeBagRightPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="change_bag_right_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(518, 251),
            size=(1, 1),
            pixel_color=(69, 231, 167),
        )

remove_from_team_button = BluePyllElement(
    label="remove_from_team_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "remove_from_team.png"),
    is_static=True,
    confidence=0.6,
)

class RemoveFromTeamPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="remove_from_team_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1876, 675),
            size=(1, 1),
            pixel_color=(241, 76, 76),
        )

remove_item_button = BluePyllElement(
    label="remove_item_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "remove_item_button.png"),
    is_static=True,
    confidence=0.6,
)

class RemoveItemPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="remove_item_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1878, 255),
            size=(1, 1),
            pixel_color=(142, 159, 170),
        )

set_first_button = BluePyllElement(
    label="set_first_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "set_first_button.png"),
    is_static=True,
    confidence=0.6,
)

class SetFirstPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="set_first_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1878, 537),
            size=(1, 1),
            pixel_color=(203, 181, 73),
        )

send_to_battle_button = BluePyllElement(
    label="send_to_battle_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "send_to_battle_button.png"),
    confidence=0.6,
    ele_txt="send to battle",
)

class SendToBattlePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="send_to_battle_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1878, 537),
            size=(1, 1),
            pixel_color=(203, 181, 73),
        )

class NoItemEquippedPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="no_item_equipped_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1816, 285),
            size=(1, 1),
            pixel_color=(255, 255, 255),
        )