from pathlib import Path

from bluepyll import BluePyllElement


class StartGameButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="start_game_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(740, 592),
            size=(440, 160),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "start_game_button.png"
            ),
            confidence=0.7,
            ele_txt="start game",
        )

class StartGamePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="start_game_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(956, 635),
            size=(1, 1),
            pixel_color=(96, 223, 251),
        )


class QualityDecreaseButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_decrease_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(670, 412),
            size=(100, 100),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "quality_decrease_button.png"
            ),
            confidence=0.7,
        )

class QualityDecreasePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_decrease_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(729, 464),
            size=(1, 1),
            pixel_color=(187, 238, 255),
        )


class QualityIncreaseButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_increase_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(740, 592),
            size=(440, 160),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "quality_increase_button.png"
            ),
            confidence=0.7,
        )

class QualityIncreasePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_increase_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1198, 464),
            size=(1, 1),
            pixel_color=(204, 238, 255),
        )


class CurrentQualityText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="current_quality_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(785, 412),
            size=(350, 100),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "current_quality_text.png"
            ),
            is_static=False,
        )


class CurrentVersionText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="current_version_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(20, 980),
            size=(150, 70),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "current_version_text.png"
            ),
            is_static=False,
        )


class GameUpdateText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="game_update_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "game_update_text.png"
            ),
            is_static=False,
            confidence=0.7,
        )


class RevomonBadgePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="revomon_badge_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(99, 132),
            size=(1, 1),
            pixel_color=(23, 195, 255),
        )