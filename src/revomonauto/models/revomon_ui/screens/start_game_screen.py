from bluepyll import BluePyllScreen

from ..elements import start_game_elements


class StartGameScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="start_game",
            elements={
                "start_game_button": start_game_elements.StartGameButton(),
                "quality_decrease_button": start_game_elements.QualityDecreaseButton(),
                "quality_increase_button": start_game_elements.QualityIncreaseButton(),
                "current_quality_text": start_game_elements.CurrentQualityText(),
                "current_version_text": start_game_elements.CurrentVersionText(),
                "game_update_text": start_game_elements.GameUpdateText(),
            },
        )
