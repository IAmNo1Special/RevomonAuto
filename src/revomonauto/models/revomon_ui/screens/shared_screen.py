from bluepyll import BluePyllScreen

from ..elements import shared_elements


class SharedScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="shared",
            elements={
                "chat_button": shared_elements.chat_button,
                "battle_chat_button": shared_elements.battle_chat_button,
                "general_chat_button": shared_elements.general_chat_button,
                "chat_log_image": shared_elements.chat_log_image,
            },
        )
