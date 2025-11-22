from pathlib import Path

from bluepyll import BluePyllElement


class LoginButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="login_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "login_assets"
                / "login_button.png"
            ),
            position=(748, 436),
            size=(425, 160),
            is_static=True,
            confidence=0.8,
            ele_txt="login",
        )


class ReloginButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="relogin_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "login_assets"
                / "relogin_button.png"
            ),
            position=(748, 436),
            size=(425, 160),
            is_static=True,
            confidence=0.8,
            ele_txt="relogin",
        )

class LoginPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="login_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(955, 569),
            size=(1, 1),
            pixel_color=(71, 113, 178),
        )


class DisconnectButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="disconnect_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "login_assets"
                / "disconnect_button.png"
            ),
            position=(1550, 830),
            size=(300, 85),
            is_static=True,
            confidence=0.7,
            ele_txt="disconnect",
        )


class DisconnectPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="disconnect_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1693, 855),
            size=(1, 1),
            pixel_color=(224, 190, 105),
        )

class ServerSelectPixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="server_select_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(1649, 1023),
            size=(1, 1),
            pixel_color=(71, 114, 176),
        )

class RevomonBadgePixel(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="revomon_badge_pixel",
            ele_type="pixel",
            og_window_size=(1920, 1080),
            position=(964, 97),
            size=(1, 1),
            pixel_color=(20, 198, 255),
        )
