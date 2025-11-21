from pathlib import Path

from bluepyll import BluePyllElement

BASE_DIR = Path(__file__).parent.parent

chat_button = BluePyllElement(
    label="chat_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "shared_assets" / "chat_button.png"),
    position=(1820, 1000),
    size=(90, 70),
    is_static=True,
    confidence=0.6,
)

battle_chat_button = BluePyllElement(
    label="battle_chat_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "shared_assets" / "battle_chat_button.png"),
    position=(1530, 140),
    size=(140, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="battle",
)

general_chat_button = BluePyllElement(
    label="general_chat_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "shared_assets" / "general_chat_button.png"),
    position=(1725, 140),
    size=(140, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="general",
)

chat_log_image = BluePyllElement(
    label="chat_log_image",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "shared_assets" / "chat_log_image.png"),
    position=(1490, 220),
    size=(435, 775),
    is_static=False,
)
