from pathlib import Path

from bluepyll import BluePyllElement

run_button = BluePyllElement(
    label="run_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "run_button.png"),
    position=(562, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="run",
)

run_button_pixel = BluePyllElement(
    label="run_button_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(625, 930),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

# TODO: @dev - need to add run confirm button
# run_confirm_button = BluePyllElement()

run_confirm_button_pixel = BluePyllElement(
    label="run_confirm_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(1130, 660),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

team_bag_battle_button = BluePyllElement(
    label="team_bag_battle_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "team_bag_battle_button.png"),
    position=(862, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="team & bag",
)

team_bag_battle_pixel = BluePyllElement(
    label="team_bag_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(957, 930),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

attacks_button = BluePyllElement(
    label="attack_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "attacks_button.png"),
    position=(1162, 815),
    size=(200, 230),
    is_static=True,
    confidence=0.6,
    ele_txt="attacks",
)

attacks_button_pixel = BluePyllElement(
    label="attacks_button_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(1260, 925),
    size=(1, 1),
    pixel_color=(248, 245, 244),
)

exit_attacks_button = BluePyllElement(
    label="exit_attacks_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "exit_attacks_button.png"),
    position=(410, 950),
    size=(90, 90),
    is_static=True,
    confidence=0.6,
)

exit_attacks_button_pixel = BluePyllElement(
    label="exit_attacks_button_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(470, 990),
    size=(1, 1),
    pixel_color=(255, 255, 255),
)

player1_mon_name_text = BluePyllElement(
    label="player1_mon_name",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_name.png"),
    position=(0, 45),
    size=(386, 50),
    is_static=True,
)

player1_mon_nameplate_pixel = BluePyllElement(
    label="player1_mon_nameplate_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(290, 130),
    size=(1, 1),
    pixel_color=(0, 206, 155),
)

player1_mon_lvl_text = BluePyllElement(
    label="player1_mon_lvl",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_lvl.png"),
    position=(0, 106),
    size=(126, 40),
    is_static=True,
)

player1_mon_hp_img = BluePyllElement(
    label="player1_mon_hp",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_hp.png"),
    position=(0, 5),
    size=(410, 43),
    is_static=False,
)

player1_mon_move1_button = BluePyllElement(
    label="player1_mon_move1",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_move1.png"),
    position=(554, 800),
    size=(390, 125),
    is_static=True,
)

player1_mon_move2_button = BluePyllElement(
    label="player1_mon_move2",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_move2.png"),
    position=(976, 800),
    size=(390, 125),
    is_static=True,
)

player1_mon_move3_button = BluePyllElement(
    label="player1_mon_move3",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_move3.png"),
    position=(554, 936),
    size=(390, 125),
    is_static=True,
)

player1_mon_move4_button = BluePyllElement(
    label="player1_mon_move4",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player1_mon_move4.png"),
    position=(976, 936),
    size=(390, 125),
    is_static=True,
)

player2_mon_name_text = BluePyllElement(
    label="player2_mon_name",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player2_mon_name.png"),
    position=(1534, 45),
    size=(386, 50),
    is_static=True,
)

player2_mon_nameplate_pixel = BluePyllElement(
    label="player2_mon_nameplate_pixel",
    ele_type="pixel",
    og_window_size=(1920, 1080),
    position=(1620, 130),
    size=(1, 1),
    pixel_color=(0, 201, 154),
)

player2_mon_lvl_text = BluePyllElement(
    label="player2_mon_lvl",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player2_mon_lvl.png"),
    position=(1794, 106),
    size=(126, 40),
    is_static=True,
)

player2_mon_hp_img = BluePyllElement(
    label="player2_mon_hp",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "player2_mon_hp.png"),
    position=(1510, 5),
    size=(410, 43),
    is_static=False,
)

waiting_for_opponent_text = BluePyllElement(
    label="waiting_for_opponent_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "waiting_for_opponent_text.png"),
    position=(577, 906),
    size=(777, 75),
    is_static=False,
)

run_confirm_button = BluePyllElement(
    label="run_confirm_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "run_confirm_button.png"),
    confidence=0.6,
    ele_txt="yes",
)
run_deny_button = BluePyllElement(
    label="run_deny_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "run_deny_button.png"),
    confidence=0.6,
    ele_txt="no",
)
run_message_text = BluePyllElement(
    label="run_message",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "run_message.png"),
    confidence=0.6,
    ele_txt="run away?",
)
send_to_battle_button = BluePyllElement(
    label="send_to_battle_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "send_to_battle_button.png"),
    confidence=0.6,
    ele_txt="send to battle",
)

battle_log_image = BluePyllElement(
    label="battle_log_image",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(Path(__file__).parent.parent / "assets" / "battle_assets" / "battle_log_image.png"),
    position=(1490, 220),
    size=(435, 775),
    is_static=False,
)