from pathlib import Path

from bluepyll import BluePyllElement


class StartGameButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="start_game_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "start_game_button.png"
            ),
            position=(740, 592),
            size=(440, 160),
            confidence=0.7,
            ele_txt="start game",
        )


class QualityDecreaseButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_decrease_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "quality_decrease_button.png"
            ),
            position=(670, 412),
            size=(100, 100),
            confidence=0.7,
        )


class QualityIncreaseButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quality_increase_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "quality_increase_button.png"
            ),
            position=(740, 592),
            size=(440, 160),
            confidence=0.7,
        )


class CurrentQualityText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="current_quality_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "current_quality_text.png"
            ),
            position=(785, 412),
            size=(350, 100),
            is_static=False,
        )


class CurrentVersionText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="current_version_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "start_game_assets"
                / "current_version_text.png"
            ),
            position=(20, 980),
            size=(150, 70),
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
            ele_txt="overall downloading",
        )
