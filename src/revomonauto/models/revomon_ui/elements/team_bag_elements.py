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

remove_from_team_button = BluePyllElement(
    label="remove_from_team_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "remove_from_team.png"),
    is_static=True,
    confidence=0.6,
)

remove_item_button = BluePyllElement(
    label="remove_item_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "remove_item_button.png"),
    is_static=True,
    confidence=0.6,
)

set_first_button = BluePyllElement(
    label="set_first_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "team_bag_assets" / "set_first_button.png"),
    is_static=True,
    confidence=0.6,
)