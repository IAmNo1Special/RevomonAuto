from pathlib import Path

from bluepyll import BluePyllElement

BASE_DIR = Path(__file__).parent.parent

clerk_npc_button = BluePyllElement(
    label="clerk_npc_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "revocenter_assets" / "clerk_npc.png"),
    position=(550, 520),
    size=(75, 120),
    is_static=True,
    confidence=0.6,
)

clerk_npc_pixel = BluePyllElement(
    label="clerk_npc_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(575, 650),
    size=(1, 1),
    pixel_color=(53, 101, 147),
)

doctor_npc_button = BluePyllElement(
    label="doctor_npc_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "revocenter_assets" / "doctor_npc.png"),
    position=(400, 540),
    size=(110, 165),
    is_static=True,
    confidence=0.6,
)

doctor_npc_pixel = BluePyllElement(
    label="doctor_npc_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(456, 653),
    size=(1, 1),
    pixel_color=(27, 57, 122),
)
move_tutor_npc_button = BluePyllElement(
    label="move_tutor_npc_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "revocenter_assets" / "move_tutor_npc.png"),
    position=(125, 512),
    size=(100, 200),
    is_static=True,
    confidence=0.6,
)

move_tutor_npc_pixel = BluePyllElement(
    label="move_tutor_npc_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(160, 640),
    size=(1, 1),
    pixel_color=(52, 100, 146),
)

tv_screen_button = BluePyllElement(
    label="tv_screen_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "revocenter_assets" / "tv_screen.png"),
    position=(931, 562),
    size=(80, 71),
    is_static=True,
    confidence=0.7,
)

tv_screen_pixel = BluePyllElement(
    label="tv_screen_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(943, 592),
    size=(1, 1),
    pixel_color=(23, 41, 42),
)

tv_screen_drassius_button = BluePyllElement(
    label="tv_screen_drassius",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "revocenter_assets" / "tv_screen_drassius.png"),
    is_static=False,
    confidence=0.6,
)
