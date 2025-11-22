from pathlib import Path

from bluepyll import BluePyllElement


class CurrentTimeText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="current_time_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "overworld_assets"
                / "current_time_text.png"
            ),
            position=(1690, 15),
            size=(130, 70),
            is_static=False,
            confidence=0.58,
            ele_txt="current time",
        )

class DayTimePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="day_time_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1875, 30),
            size=(1, 1),
            pixel_color=(255, 244, 91),
        )


class NightTimePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="night_time_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1875, 30),
            size=(1, 1),
            pixel_color=(255, 249, 192),
        )


class MainMenuButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="main_menu_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "overworld_assets"
                / "main_menu_button.png"
            ),
            position=(1785, 185),
            size=(75, 70),
            is_static=True,
            confidence=0.58,
            ele_txt="menu",
        )

class MainMenuPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="main_menu_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1827, 218),
            size=(1, 1),
            pixel_color=(214, 232, 235),
        )

class ReleaseFirstMonButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="release_first_mon_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "overworld_assets"
                / "release_first_mon_button.png"
            ),
            position=(1785, 350),
            size=(75, 70),
            is_static=True,
            confidence=0.6,
            ele_txt="release 1st revomon",
        )

class ReleaseFirstMonPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="release_first_mon_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1827, 401),
            size=(1, 1),
            pixel_color=(255, 255, 255),
        )

class AimShootButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="aim_shoot_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(   
                Path(__file__).parent.parent
                / "assets"
                / "overworld_assets"
                / "aim_shoot_button.png"
            ),
            position=(1785, 515),
            size=(75, 70),
            is_static=True,
            confidence=0.6,
            ele_txt="aim for wild revomon",
        )

class AimShootPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="aim_shoot_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1820, 546),
            size=(1, 1),
            pixel_color=(254, 254, 254),
        )
