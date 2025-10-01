from dataclasses import dataclass
from pathlib import Path

from bluepyll.ui import UIElement

BASE_DIR = Path(__file__).parent


########################### START GAME SCENE #############################
start_game_button = UIElement(
    label="start_game_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "start_game_button.png"),
    position=(740, 592),
    size=(440, 160),
    is_static=True,
    confidence=0.7,
    ele_txt="start game",
)

quality_decrease_button = UIElement(
    label="quality_decrease_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "game_quality_decrease_button.png"),
    position=(670, 412),
    size=(100, 100),
    is_static=True,
    confidence=0.7,
)

quality_increase_button = UIElement(
    label="quality_increase_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "game_quality_increase_button.png"),
    position=(740, 592),
    size=(440, 160),
    is_static=True,
    confidence=0.7,
)

current_quality_text = UIElement(
    label="current_quality_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "login" / "current_quality_text.png"),
    position=(785, 412),
    size=(350, 100),
    is_static=False,
)

current_version_text = UIElement(
    label="current_version_text",
    path=str(BASE_DIR / "game_ui" / "login" / "current_version_text.png"),
    position=(20, 980),
    size=(150, 70),
    ele_type="text",
    is_static=False,
)

game_update_text = UIElement(
    label="game_update_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "login" / "game_update_text.png"),
    position=None,
    size=None,
    is_static=False,
    confidence=0.7,
    ele_txt="overall downloading",
)
########################### LOGIN SCENE #############################

login_button = UIElement(
    label="login_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "login_button.png"),
    position=(748, 436),
    size=(425, 160),
    is_static=True,
    confidence=0.8,
    ele_txt="login",
)

relogin_button = UIElement(
    label="relogin_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "relogin_button.png"),
    position=(748, 436),
    size=(425, 160),
    is_static=True,
    confidence=0.77,
    ele_txt="relogin",
)

disconnect_button = UIElement(
    label="disconnect_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "disconnect_button.png"),
    position=(1550, 830),
    size=(300, 85),
    is_static=True,
    confidence=0.7,
    ele_txt="disconnect",
)

########################### PASSPORT LOGIN SCENE #############################

gmail_login_button = UIElement(
    label="gmail_login_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "gmail_login_button.png"),
    position=(825, 425),
    size=(125, 125),
    is_static=True,
    confidence=0.7,
)

apple_login_button = UIElement(
    label="apple_login_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "login" / "apple_login_button.png"),
    position=(970, 425),
    size=(125, 125),
    is_static=True,
    confidence=0.7,
)

email_login_input = UIElement(
    label="email_login_input",
    ele_type="input",
    path=str(BASE_DIR / "game_ui" / "login" / "email_login_input.png"),
    position=(610, 610),
    size=(698, 122),
    is_static=False,
    confidence=0.7,
    ele_txt="enter email address  ",
)
########################### OVERWORLD SCENE #############################

current_time_text = UIElement(
    label="current_time_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "overworld" / "current_time_text.png"),
    position=(1690, 15),
    size=(130, 70),
    is_static=False,
    confidence=0.58,
    ele_txt="current time",
)

day_time_pixel = UIElement(
    label="day_time_pixel",
    ele_type="pixel",
    position=(1875, 30),
    size=(1, 1),
    pixel_color=(255, 244, 91),
)

night_time_pixel = UIElement(
    label="night_time_pixel",
    ele_type="pixel",
    position=(1875, 30),
    size=(1, 1),
    pixel_color=(255, 249, 192),
)

main_menu_button = UIElement(
    label="main_menu_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "main_menu_button.png"),
    position=(1785, 185),
    size=(75, 70),
    is_static=True,
    confidence=0.58,
    ele_txt="menu",
)

release_first_mon_button = UIElement(
    label="release_first_mon_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "release_first_mon_button.png"),
    position=(1785, 350),
    size=(75, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="release 1st revomon",
)

aim_shoot_button = UIElement(
    label="aim_shoot_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "aim_shoot_button.png"),
    position=(1785, 515),
    size=(75, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="aim for wild revomon",
)

########################### CHAT SCENE #############################

chat_button = UIElement(
    label="chat_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "chat" / "chat_button.png"),
    position=(1820, 1000),
    size=(90, 70),
    is_static=True,
    confidence=0.6,
)

battle_chat_button = UIElement(
    label="battle_chat_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "chat" / "battle_chat_button.png"),
    position=(1530, 140),
    size=(140, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="battle",
)

general_chat_button = UIElement(
    label="general_chat_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "chat" / "general_chat_button.png"),
    position=(1725, 140),
    size=(140, 70),
    is_static=True,
    confidence=0.6,
    ele_txt="general",
)

chat_log_image = UIElement(
    label="chat_log_image",
    ele_type="image",
    path=str(BASE_DIR / "game_ui" / "chat" / "chat_log_image.png"),
    position=(1490, 220),
    size=(430, 775),
    is_static=False,
)

########################### MENU SCENE #############################

tamer_name_text = UIElement(
    label="tamer_name_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "menu" / "tamer_name_text.png"),
    position=(60, 15),
    size=(1150, 80),
    is_static=True,
    confidence=0.7,
    ele_txt="tamer name",
)

tamer_selfie_img = UIElement(
    label="tamer_selfie_img",
    ele_type="image",
    path=str(BASE_DIR / "game_ui" / "menu" / "tamer_selfie_img.png"),
    position=(30, 110),
    size=(375, 375),
    is_static=False,
)

exit_menu_button = UIElement(
    label="exit_menu_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "exit_menu_button.png"),
    position=(1800, 5),
    size=(110, 110),
    is_static=True,
    confidence=0.7,
)

wardrobe_button = UIElement(
    label="wardrobe_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "wardrobe" / "wardrobe_button.png"),
    position=(580, 205),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="wardrobe",
)

team_bag_menu_button = UIElement(
    label="team_bag_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "team_bag" / "team_bag_menu_button.png"),
    position=(780, 205),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="team/bag",
)

recall_button = UIElement(
    label="recall_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "recall_button.png"),
    position=(980, 205),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="recall",
)

friends_button = UIElement(
    label="friends_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "friends" / "friends_button.png"),
    position=(1180, 205),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="friends",
)

settings_button = UIElement(
    label="settings_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "settings" / "settings_button.png"),
    position=(580, 415),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="settings",
)

revodex_button = UIElement(
    label="revodex_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "revodex" / "revodex_button.png"),
    position=(780, 415),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="revodex",
)

market_button = UIElement(
    label="market_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "market" / "market_button.png"),
    position=(980, 415),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="market",
)

discussion_button = UIElement(
    label="discussion_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "discussion" / "discussion_button.png"),
    position=(1180, 415),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="discussion",
)

pvp_button = UIElement(
    label="pvp_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "pvp_button.png"),
    position=(580, 625),
    size=(200, 210),
    is_static=True,
    confidence=0.8,
    ele_txt="pvp",
)

clan_button = UIElement(
    label="clan_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "clan" / "clan_button.png"),
    position=(780, 650),
    size=(200, 50),
    is_static=True,
    confidence=0.8,
    ele_txt="clan",
)

game_wallet_text = UIElement(
    label="game_wallet_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "menu" / "game_wallet_text.png"),
    position=(40, 730),
    size=(530, 50),
    is_static=False,
    ele_txt="game wallet",
)

revomon_seen_text = UIElement(
    label="revomon_seen_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "menu" / "revomon_seen_text.png"),
    position=(300, 805),
    size=(170, 50),
    is_static=False,
    ele_txt="revomon seen",
)

pvp_rating_text = UIElement(
    label="pvp_rating_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "menu" / "pvp_rating_text.png"),
    position=(300, 880),
    size=(170, 50),
    is_static=False,
    ele_txt="pvp rating",
)

reset_position_button = UIElement(
    label="reset_position_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "reset_position_button.png"),
    position=(785, 870),
    size=(360, 70),
    is_static=True,
    confidence=0.8,
    ele_txt="reset my position",
)
quit_game_button = UIElement(
    label="quit_game_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "quit_game_button.png"),
    position=(30, 980),
    size=(180, 80),
    is_static=True,
    confidence=0.8,
)

########################### BATTLE SCENE #############################

run_button = UIElement(
    label="run_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "battle" / "run_button.png"),
    position=(562, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="run",
)

run_button_pixel = UIElement(
    label="run_button_pixel",
    ele_type="pixel",
    position=(625, 930),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

# TODO: @dev - need to add run confirm button
# run_confirm_button = UIElement()

run_confirm_button_pixel = UIElement(
    label="run_confirm_pixel",
    ele_type="pixel",
    position=(1130, 660),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

team_bag_battle_button = UIElement(
    label="team_bag_battle_button",
    ele_type="button",
    path=str(
        BASE_DIR / "game_ui" / "overworld" / "battle" / "team_bag_battle_button.png"
    ),
    position=(862, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="team & bag",
)

team_bag_battle_pixel = UIElement(
    label="team_bag_pixel",
    ele_type="pixel",
    position=(957, 930),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

attacks_button = UIElement(
    label="attack_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "battle" / "attacks_button.png"),
    position=(1162, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="attacks",
)

attacks_button_pixel = UIElement(
    label="attacks_button_pixel",
    ele_type="pixel",
    position=(1260, 925),
    size=(1, 1),
    pixel_color=(248, 245, 244),
)

exit_attacks_button = UIElement(
    label="exit_attacks_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "overworld" / "battle" / "exit_attacks_button.png"),
    position=(410, 950),
    size=(90, 90),
    is_static=True,
    confidence=0.6,
)

exit_attacks_button_pixel = UIElement(
    label="exit_attacks_button_pixel",
    ele_type="pixel",
    position=(470, 990),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

player1_mon_name_text = UIElement(
    label="player1_mon_name",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player1_mon_name.png"),
    position=(0, 45),
    size=(386, 50),
    is_static=True,
)

player1_mon_nameplate_pixel = UIElement(
    label="player1_mon_nameplate_pixel",
    ele_type="pixel",
    position=(346, 126),
    size=(1, 1),
    pixel_color=(0, 210, 155),
)

player1_mon_lvl_text = UIElement(
    label="player1_mon_lvl",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player1_mon_lvl.png"),
    position=(0, 106),
    size=(126, 40),
    is_static=True,
)

player1_mon_hp_text = UIElement(
    label="player1_mon_hp",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player1_mon_hp.png"),
    position=(0, 5),
    size=(410, 43),
    is_static=True,
)

player1_mon_move1_text = UIElement(
    label="player1_mon_move1",
    ele_type="button",
    path=str(BASE_DIR / "battles" / "player1_mon_move1.png"),
    position=(554, 800),
    size=(390, 125),
    is_static=True,
)

player1_mon_move2_text = UIElement(
    label="player1_mon_move2",
    ele_type="button",
    path=str(BASE_DIR / "battles" / "player1_mon_move2.png"),
    position=(976, 800),
    size=(390, 125),
    is_static=True,
)

player1_mon_move3_text = UIElement(
    label="player1_mon_move3",
    ele_type="button",
    path=str(BASE_DIR / "battles" / "player1_mon_move3.png"),
    position=(554, 936),
    size=(390, 125),
    is_static=True,
)

player1_mon_move4_text = UIElement(
    label="player1_mon_move4",
    ele_type="button",
    path=str(BASE_DIR / "battles" / "player1_mon_move4.png"),
    position=(976, 936),
    size=(390, 125),
    is_static=True,
)

player2_mon_name_text = UIElement(
    label="player2_mon_name",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player2_mon_name.png"),
    position=(1534, 45),
    size=(386, 50),
    is_static=True,
)

player2_mon_nameplate_pixel = UIElement(
    label="player2_mon_nameplate_pixel",
    ele_type="pixel",
    position=(1577, 115),
    size=(1, 1),
    pixel_color=(0, 210, 155),
)
player2_mon_lvl_text = UIElement(
    label="player2_mon_lvl",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player2_mon_lvl.png"),
    position=(1794, 106),
    size=(126, 40),
    is_static=True,
)

player2_mon_hp_text = UIElement(
    label="player2_mon_hp",
    ele_type="text",
    path=str(BASE_DIR / "battles" / "player2_mon_hp.png"),
    position=(1510, 5),
    size=(410, 43),
    is_static=True,
)

########################### REVOCENTER SCENE #############################

clerk_npc_button = UIElement(
    label="clerk_npc_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "clerk" / "clerk_npc.png"),
    position=(550, 520),
    size=(75, 120),
    is_static=True,
    confidence=0.6,
)

clerk_npc_pixel = UIElement(
    label="clerk_npc_pixel",
    ele_type="pixel",
    position=(575, 650),
    size=(1, 1),
    pixel_color=(53, 101, 147),
)

doctor_npc_button = UIElement(
    label="doctor_npc_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "doctor" / "doctor_npc.png"),
    position=(400, 540),
    size=(110, 165),
    is_static=True,
    confidence=0.6,
)

doctor_npc_pixel = UIElement(
    label="doctor_npc_pixel",
    ele_type="pixel",
    position=(456, 653),
    size=(1, 1),
    pixel_color=(27, 57, 122),
)
move_tutor_npc_button = UIElement(
    label="move_tutor_npc_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "move_tutor" / "move_tutor_npc.png"),
    position=(125, 512),
    size=(100, 200),
    is_static=True,
    confidence=0.6,
)

move_tutor_npc_pixel = UIElement(
    label="move_tutor_npc_pixel",
    ele_type="pixel",
    position=(160, 640),
    size=(1, 1),
    pixel_color=(52, 100, 146),
)

tv_screen_button = UIElement(
    label="tv_screen_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_screen.png"),
    position=(931, 562),
    size=(80, 71),
    is_static=True,
    confidence=0.7,
)

tv_screen_pixel = UIElement(
    label="tv_screen_pixel",
    ele_type="pixel",
    position=(943, 592),
    size=(1, 1),
    pixel_color=(23, 41, 42),
)
########################### OPEN TV SCENE #############################

tv_advanced_search_button = UIElement(
    label="tv_advanced_search_button",
    ele_type="button",
    path=str(
        BASE_DIR
        / "game_ui"
        / "revocenter"
        / "tv"
        / "advanced_search"
        / "tv_advanced_search_button.png"
    ),
    position=(145, 115),
    size=(90, 95),
    is_static=True,
    confidence=0.7,
)

tv_search_input = UIElement(
    label="tv_search_input",
    ele_type="input",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_search_input.png"),
    position=(265, 125),
    size=(430, 65),
    is_static=False,
    confidence=0.6,
    ele_txt="search here...",
)

tv_search_button = UIElement(
    label="tv_search_button",
    ele_type="button",
    path=str(
        BASE_DIR
        / "game_ui"
        / "revocenter"
        / "tv"
        / "advanced_search"
        / "tv_search_button.png"
    ),
    position=(370, 185),
    size=(215, 60),
    is_static=True,
    confidence=0.6,
    ele_txt="search",
)

tv_previous_page_button = UIElement(
    label="tv_previous_page_button",
    ele_type="button",
    path=str(
        BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_previous_page_button.png"
    ),
    position=(780, 120),
    size=(95, 95),
    is_static=True,
    confidence=0.6,
)

tv_page_number_text = UIElement(
    label="tv_page_number_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_page_number_text.png"),
    position=(880, 130),
    size=(330, 70),
    is_static=False,
)

tv_next_page_button = UIElement(
    label="tv_next_page_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_next_page_button.png"),
    position=(1220, 120),
    size=(95, 95),
    is_static=True,
    confidence=0.6,
)

tv_mon_name_text = UIElement(
    label="tv_mon_name_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_name_text.png"),
    position=(1320, 145),
    size=(470, 80),
    is_static=False,
)

tv_exit_button = UIElement(
    label="tv_exit_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_exit_button.png"),
    position=(1785, 95),
    size=(130, 130),
    is_static=True,
    confidence=0.6,
)

tv_mon_ability_text = UIElement(
    label="tv_mon_ability_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_ability_text.png"),
    position=(930, 290),
    size=(260, 70),
    is_static=False,
)

tv_mon_og_tamer_text = UIElement(
    label="tv_mon_og_tamer_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_og_tamer_text.png"),
    position=(1190, 290),
    size=(220, 70),
    is_static=False,
)

tv_mon_nature_text = UIElement(
    label="tv_mon_nature_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / ",tv_mon_nature_text.png"),
    position=(930, 400),
    size=(255, 55),
    is_static=False,
)

tv_mon_exp_text = UIElement(
    label="tv_mon_exp_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_exp_text.png"),
    position=(1190, 400),
    size=(220, 70),
    is_static=False,
)

tv_mon_held_item_image = UIElement(
    label="tv_mon_held_item_image",
    ele_type="image",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_held_item_image.png"),
    position=(1795, 220),
    size=(60, 60),
    is_static=False,
)

tv_mon_types_image = UIElement(
    label="tv_mon_types_image",
    ele_type="image",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_types_image.png"),
    position=(1760, 525),
    size=(130, 80),
    is_static=False,
)

tv_mon_level_text = UIElement(
    label="tv_mon_level_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_level_text.png"),
    position=(1800, 600),
    size=(110, 50),
    is_static=False,
)

tv_mon_id_text = UIElement(
    label="tv_mon_id_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_id_text.png"),
    position=(1500, 650),
    size=(400, 50),
    is_static=False,
)

tv_mon_hp_stat_text = UIElement(
    label="tv_mon_hp_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_hp_stat_text.png"),
    position=(1195, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_hp_iv_text = UIElement(
    label="tv_mon_hp_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_hp_iv_text.png"),
    position=(1270, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_hp_ev_text = UIElement(
    label="tv_mon_hp_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_hp_ev_text.png"),
    position=(1340, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_stat_text = UIElement(
    label="tv_mon_atk_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_atk_stat_text.png"),
    position=(1195, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_iv_text = UIElement(
    label="tv_mon_atk_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_atk_iv_text.png"),
    position=(1270, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_ev_text = UIElement(
    label="tv_mon_atk_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_atk_ev_text.png"),
    position=(1340, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_stat_text = UIElement(
    label="tv_mon_def_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_def_stat_text.png"),
    position=(1195, 565),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_iv_text = UIElement(
    label="tv_mon_def_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_def_iv_text.png"),
    position=(1270, 565),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_ev_text = UIElement(
    label="tv_mon_def_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_def_ev_text.png"),
    position=(1340, 570),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_stat_text = UIElement(
    label="tv_mon_spa_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spa_stat_text.png"),
    position=(1195, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_iv_text = UIElement(
    label="tv_mon_spa_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spa_iv_text.png"),
    position=(1270, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_ev_text = UIElement(
    label="tv_mon_spa_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spa_ev_text.png"),
    position=(1340, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_stat_text = UIElement(
    label="tv_mon_spd_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spd_stat_text.png"),
    position=(1195, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_iv_text = UIElement(
    label="tv_mon_spd_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spd_iv_text.png"),
    position=(1270, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_ev_text = UIElement(
    label="tv_mon_spd_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spd_ev_text.png"),
    position=(1340, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_stat_text = UIElement(
    label="tv_mon_spe_stat_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spe_stat_text.png"),
    position=(1195, 655),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_iv_text = UIElement(
    label="tv_mon_spe_iv_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spe_iv_text.png"),
    position=(1270, 655),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_ev_text = UIElement(
    label="tv_mon_spe_ev_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_spe_ev_text.png"),
    position=(1340, 655),
    size=(60, 30),
    is_static=False,
)

tv_add_to_party_button = UIElement(
    label="tv_add_to_party_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_add_to_party_button.png"),
    position=(990, 700),
    size=(315, 120),
    is_static=True,
    confidence=0.6,
    ele_txt="add to party",
)

tv_delete_this_revomon_button = UIElement(
    label="tv_delete_this_revomon_button",
    ele_type="button",
    path=str(
        BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_delete_this_revomon_button.png"
    ),
    position=(990, 825),
    size=(315, 120),
    is_static=True,
    confidence=0.6,
    ele_txt="delete this revomon",
)

tv_mon_move1_text = UIElement(
    label="tv_mon_move1_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_move1_text.png"),
    position=(1315, 715),
    size=(250, 50),
    is_static=False,
)

tv_mon_move2_text = UIElement(
    label="tv_mon_move2_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_move2_text.png"),
    position=(1315, 770),
    size=(250, 50),
    is_static=False,
)

tv_mon_move3_text = UIElement(
    label="tv_mon_move3_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_move3_text.png"),
    position=(1315, 830),
    size=(250, 50),
    is_static=False,
)

tv_mon_move4_text = UIElement(
    label="tv_mon_move4_text",
    ele_type="text",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_mon_move4_text.png"),
    position=(1315, 880),
    size=(250, 50),
    is_static=False,
)

tv_slot1_button = UIElement(
    label="tv_slot1_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot1_button.png"),
    position=(50, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot2_button = UIElement(
    label="tv_slot2_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot2_button.png"),
    position=(195, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot3_button = UIElement(
    label="tv_slot3_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot3_button.png"),
    position=(340, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot4_button = UIElement(
    label="tv_slot4_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot4_button.png"),
    position=(485, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot5_button = UIElement(
    label="tv_slot5_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot5_button.png"),
    position=(630, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot6_button = UIElement(
    label="tv_slot6_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot6_button.png"),
    position=(775, 260),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot7_button = UIElement(
    label="tv_slot7_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot7_button.png"),
    position=(50, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot8_button = UIElement(
    label="tv_slot8_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot8_button.png"),
    position=(195, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot9_button = UIElement(
    label="tv_slot9_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot9_button.png"),
    position=(340, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot10_button = UIElement(
    label="tv_slot10_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot10_button.png"),
    position=(485, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot11_button = UIElement(
    label="tv_slot11_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot11_button.png"),
    position=(630, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot12_button = UIElement(
    label="tv_slot12_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot12_button.png"),
    position=(775, 395),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot13_button = UIElement(
    label="tv_slot13_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot13_button.png"),
    position=(50, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot14_button = UIElement(
    label="tv_slot14_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot14_button.png"),
    position=(195, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot15_button = UIElement(
    label="tv_slot15_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot15_button.png"),
    position=(340, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot16_button = UIElement(
    label="tv_slot16_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot16_button.png"),
    position=(485, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot17_button = UIElement(
    label="tv_slot17_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot17_button.png"),
    position=(630, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot18_button = UIElement(
    label="tv_slot18_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot18_button.png"),
    position=(775, 530),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot19_button = UIElement(
    label="tv_slot19_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot19_button.png"),
    position=(50, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot20_button = UIElement(
    label="tv_slot20_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot20_button.png"),
    position=(195, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot21_button = UIElement(
    label="tv_slot21_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot21_button.png"),
    position=(340, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot22_button = UIElement(
    label="tv_slot22_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot22_button.png"),
    position=(485, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot23_button = UIElement(
    label="tv_slot23_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot23_button.png"),
    position=(630, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot24_button = UIElement(
    label="tv_slot24_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot24_button.png"),
    position=(775, 665),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)


tv_slot25_button = UIElement(
    label="tv_slot25_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot25_button.png"),
    position=(50, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot26_button = UIElement(
    label="tv_slot26_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot26_button.png"),
    position=(195, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot27_button = UIElement(
    label="tv_slot27_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot27_button.png"),
    position=(340, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot28_button = UIElement(
    label="tv_slot28_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot28_button.png"),
    position=(485, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot29_button = UIElement(
    label="tv_slot29_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot29_button.png"),
    position=(630, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slot30_button = UIElement(
    label="tv_slot30_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_slot30_button.png"),
    position=(775, 800),
    size=(145, 135),
    is_static=False,
    confidence=0.6,
)

tv_slots = [
    tv_slot1_button,
    tv_slot2_button,
    tv_slot3_button,
    tv_slot4_button,
    tv_slot5_button,
    tv_slot6_button,
    tv_slot7_button,
    tv_slot8_button,
    tv_slot9_button,
    tv_slot10_button,
    tv_slot11_button,
    tv_slot12_button,
    tv_slot13_button,
    tv_slot14_button,
    tv_slot15_button,
    tv_slot16_button,
    tv_slot17_button,
    tv_slot18_button,
    tv_slot19_button,
    tv_slot20_button,
    tv_slot21_button,
    tv_slot22_button,
    tv_slot23_button,
    tv_slot24_button,
    tv_slot25_button,
    tv_slot26_button,
    tv_slot27_button,
    tv_slot28_button,
    tv_slot29_button,
    tv_slot30_button,
]

########################### LANDMARK SCENES #############################

inside_revocenter_landmark = UIElement(
    label="inside_revocenter_landmark",
    ele_type="image",
    path=str(
        BASE_DIR
        / "game_ui"
        / "overworld"
        / "landmarks"
        / "inside_revocenter_landmark.png"
    ),
    position=(0, 0),
    size=(1700, 300),
    is_static=True,
    confidence=0.6,
)


change_bag_left_button = UIElement(
    label="change_bag_left_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "team_bag" / "change_bag_left_button.png"),
    is_static=True,
    confidence=0.6,
)

change_bag_right_button = UIElement(
    label="change_bag_right_button",
    ele_type="button",
    path=str(
        BASE_DIR / "game_ui" / "menu" / "team_bag" / "change_bag_right_button.png"
    ),
    is_static=True,
    confidence=0.6,
)

remove_from_team_button = UIElement(
    label="remove_from_team_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "team_bag" / "remove_from_team.png"),
    is_static=True,
    confidence=0.6,
)

remove_item_button = UIElement(
    label="remove_item_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "team_bag" / "remove_item_button.png"),
    is_static=True,
    confidence=0.6,
)

set_first_button = UIElement(
    label="set_first_button",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "menu" / "team_bag" / "set_first_button.png"),
    is_static=True,
    confidence=0.6,
)

arktos_outside_center_image = UIElement(
    label="arktos_outside_center_image",
    ele_type="image",
    path=str(
        BASE_DIR
        / "game_ui"
        / "overworld"
        / "landmarks"
        / "arktos_outside_revocenter_img.png"
    ),
    is_static=False,
    confidence=0.6,
)

tv_screen_drassius_button = UIElement(
    label="tv_screen_drassius",
    ele_type="button",
    path=str(BASE_DIR / "game_ui" / "revocenter" / "tv" / "tv_screen_drassius.png"),
    is_static=False,
    confidence=0.6,
)


@dataclass(frozen=True)
class RevomonUiPaths:

    ########################### In-BATTLE #############################
    run_confirm_button = (
        str(
            BASE_DIR / "game_ui" / "overworld" / "in-battle" / "run_confirm_button.png"
        ),
        0.5,
    )
    run_deny_button_path = (
        str(BASE_DIR / "game_ui" / "overworld" / "in-battle" / "run_deny_button.png"),
        0.5,
    )
    run_message_path = (
        str(BASE_DIR / "game_ui" / "overworld" / "in-battle" / "run_message.png"),
        0.5,
    )
    send_to_battle_button_path = (
        str(
            BASE_DIR
            / "game_ui"
            / "overworld"
            / "in-battle"
            / "send_to_battle_button.png"
        ),
        0.6,
    )
