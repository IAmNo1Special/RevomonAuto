from bluepyll import BluePyllScreen

from ..elements import overworld_elements


class OverworldScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="overworld",
            elements={
                "current_time_text": overworld_elements.CurrentTimeText(),
                "day_time_pixel": overworld_elements.DayTimePixel(),
                "night_time_pixel": overworld_elements.NightTimePixel(),
                "main_menu_button": overworld_elements.MainMenuButton(),
                "release_first_mon_button": overworld_elements.ReleaseFirstMonButton(),
                "aim_shoot_button": overworld_elements.AimShootButton(),
            },
        )
