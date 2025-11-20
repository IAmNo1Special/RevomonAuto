from pathlib import Path

from bluepyll import BluePyllElement


class TamerNameText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="tamer_name_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(60, 15),
            size=(1150, 80),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "tamer_name_text.png"
            ),
            confidence=0.7,
            ele_txt="tamer name",
        )


class TamerSelfieImg(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="tamer_selfie_img",
            ele_type="image",
            og_window_size=(1920, 1080),
            position=(30, 110),
            size=(375, 375),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "tamer_selfie_img.png"
            ),
            is_static=False,
        )


class ExitMenuButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="exit_menu_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(1800, 5),
            size=(110, 110),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "exit_menu_button.png"
            ),
            confidence=0.7,
        )


class WardrobeButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="wardrobe_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(580, 205),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "wardrobe_button.png"
            ),
            confidence=0.8,
            ele_txt="wardrobe",
        )

class TeamBagMenuButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="team_bag_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(780, 205),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "team_bag_menu_button.png"
            ),
            confidence=0.8,
            ele_txt="team/bag",
        )

class RecallButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="recall_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(980, 205),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "recall_button.png"
            ),
            confidence=0.8,
            ele_txt="recall",
        )

class FriendsButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="friends_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(1180, 205),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "friends_button.png"
            ),
            confidence=0.8,
            ele_txt="friends",
        )

class SettingsButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="settings_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(580, 415),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "settings_button.png"
            ),
            confidence=0.8,
            ele_txt="settings",
        )

class RevodexButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="revodex_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(780, 415),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "revodex_button.png"
            ),
            confidence=0.8,
            ele_txt="revodex",
        )

class MarketButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="market_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(980, 415),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "market_button.png"
            ),
            confidence=0.8,
            ele_txt="market",
        )

class DiscussionButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="discussion_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(1180, 415),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "discussion_button.png"
            ),
            confidence=0.8,
            ele_txt="discussion",
        )

class PvpButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="pvp_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(580, 625),
            size=(200, 210),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "pvp_button.png"
            ),
            confidence=0.8,
            ele_txt="pvp",
        )

class ClanButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="clan_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(780, 650),
            size=(200, 50),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "clan_button.png"
            ),
            confidence=0.8,
            ele_txt="clan",
        )

class GameWalletText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="game_wallet_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(40, 730),
            size=(530, 50),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "game_wallet_text.png"
            ),            
            is_static=False,
        )

class RevomonSeenText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="revomon_seen_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(300, 805),
            size=(170, 50),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "revomon_seen_text.png"
            ),
            is_static=False,
        )

class PvpRatingText(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="pvp_rating_text",
            ele_type="text",
            og_window_size=(1920, 1080),
            position=(300, 880),
            size=(170, 50),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "pvp_rating_text.png"
            ),
            is_static=False,
        )

class ResetPositionButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="reset_position_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            position=(785, 870),
            size=(360, 70),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "reset_position_button.png"
            ),
            confidence=0.8,
            ele_txt="reset my position",
        )

class QuitGameButton(BluePyllElement):
    def __init__(self):
        super().__init__(
            label="quit_game_button",
            ele_type="button",
            og_window_size=(1920, 1080),
            path=str(
                Path(__file__).parent.parent
                / "assets"
                / "main_menu_assets"
                / "quit_game_button.png"
            ),
            position=(30, 980),
            size=(180, 80),
            confidence=0.8,
        )