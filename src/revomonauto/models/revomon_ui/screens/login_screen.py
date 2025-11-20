from bluepyll import BluePyllScreen

from ..elements import login_elements


class LoginScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="login",
            elements={
                "login_button": login_elements.LoginButton(),
                "relogin_button": login_elements.ReloginButton(),
                "disconnect_button": login_elements.DisconnectButton(),
            },
        )
