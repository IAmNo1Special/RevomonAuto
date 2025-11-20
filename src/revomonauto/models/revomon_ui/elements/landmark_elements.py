from pathlib import Path

from bluepyll import BluePyllElement

BASE_DIR = Path(__file__).parent.parent

arktos_outside_center_image = BluePyllElement(
    label="arktos_outside_center_image",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(
        BASE_DIR
        / "assets"
        / "landmark_assets"
        / "arktos_outside_revocenter_img.png"
    ),
    is_static=False,
    confidence=0.6,
)

inside_revocenter_landmark = BluePyllElement(
    label="inside_revocenter_landmark",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(
        BASE_DIR
        / "assets"
        / "landmark_assets"
        / "inside_revocenter_landmark.png"
    ),
    position=(0, 0),
    size=(1700, 300),
    is_static=True,
    confidence=0.6,
)