from bluepyll import BluePyllScreen

from ..elements import main_menu_elements


class MainMenuScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="main_menu",
            elements={
                "tamer_name_text": main_menu_elements.TamerNameText(),
                "tamer_selfie_img": main_menu_elements.TamerSelfieImg(),
                "exit_menu_button": main_menu_elements.ExitMenuButton(),
                "wardrobe_button": main_menu_elements.WardrobeButton(),
                "team_bag_button": main_menu_elements.TeamBagMenuButton(),
                "recall_button": main_menu_elements.RecallButton(),
                "friends_button": main_menu_elements.FriendsButton(),
                "settings_button": main_menu_elements.SettingsButton(),
                "revodex_button": main_menu_elements.RevodexButton(),
                "market_button": main_menu_elements.MarketButton(),
                "discussion_button": main_menu_elements.DiscussionButton(),
                "pvp_button": main_menu_elements.PvpButton(),
                "clan_button": main_menu_elements.ClanButton(),
                "quit_game_button": main_menu_elements.QuitGameButton(),
            },
        )
