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
