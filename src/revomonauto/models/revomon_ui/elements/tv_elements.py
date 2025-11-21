from pathlib import Path

from bluepyll import BluePyllElement

BASE_DIR = Path(__file__).parent.parent

tv_advanced_search_button = BluePyllElement(
    label="tv_advanced_search_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_advanced_search_button.png"),
    position=(145, 115),
    size=(90, 95),
    is_static=True,
    confidence=0.7,
)

tv_search_input = BluePyllElement(
    label="tv_search_input",
    ele_type="input",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_search_input.png"),
    position=(265, 125),
    size=(430, 65),
    is_static=False,
    confidence=0.6,
    ele_txt="search here...",
)

tv_search_button = BluePyllElement(
    label="tv_search_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_search_button.png"),
    position=(370, 185),
    size=(215, 60),
    is_static=True,
    confidence=0.6,
    ele_txt="search",
)

tv_previous_page_button = BluePyllElement(
    label="tv_previous_page_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_previous_page_button.png"),
    position=(780, 120),
    size=(95, 95),
    is_static=True,
    confidence=0.6,
)

tv_page_number_text = BluePyllElement(
    label="tv_page_number_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_page_number_text.png"),
    position=(880, 130),
    size=(330, 70),
    is_static=False,
)

tv_next_page_button = BluePyllElement(
    label="tv_next_page_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_next_page_button.png"),
    position=(1220, 120),
    size=(95, 95),
    is_static=True,
    confidence=0.6,
)

tv_mon_name_text = BluePyllElement(
    label="tv_mon_name_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_name_text.png"),
    position=(1320, 145),
    size=(470, 80),
    is_static=False,
)

tv_exit_button = BluePyllElement(
    label="tv_exit_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_exit_button.png"),
    position=(1785, 95),
    size=(130, 130),
    is_static=True,
    confidence=0.6,
)

tv_mon_ability_text = BluePyllElement(
    label="tv_mon_ability_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_ability_text.png"),
    position=(930, 290),
    size=(260, 70),
    is_static=False,
)

tv_mon_og_tamer_text = BluePyllElement(
    label="tv_mon_og_tamer_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_og_tamer_text.png"),
    position=(1190, 290),
    size=(220, 70),
    is_static=False,
)

tv_mon_nature_text = BluePyllElement(
    label="tv_mon_nature_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_nature_text.png"),
    position=(930, 400),
    size=(255, 55),
    is_static=False,
)

tv_mon_exp_text = BluePyllElement(
    label="tv_mon_exp_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_exp_text.png"),
    position=(1190, 400),
    size=(220, 70),
    is_static=False,
)

tv_mon_held_item_image = BluePyllElement(
    label="tv_mon_held_item_image",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_held_item_image.png"),
    position=(1795, 220),
    size=(60, 60),
    is_static=False,
)

tv_mon_types_image = BluePyllElement(
    label="tv_mon_types_image",
    ele_type="image",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_types_image.png"),
    position=(1760, 525),
    size=(130, 80),
    is_static=False,
)

tv_mon_level_text = BluePyllElement(
    label="tv_mon_level_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_level_text.png"),
    position=(1800, 600),
    size=(110, 50),
    is_static=False,
)

tv_mon_id_text = BluePyllElement(
    label="tv_mon_id_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_id_text.png"),
    position=(1500, 650),
    size=(400, 50),
    is_static=False,
)

tv_mon_hp_stat_text = BluePyllElement(
    label="tv_mon_hp_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_hp_stat_text.png"),
    position=(1195, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_hp_iv_text = BluePyllElement(
    label="tv_mon_hp_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_hp_iv_text.png"),
    position=(1270, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_hp_ev_text = BluePyllElement(
    label="tv_mon_hp_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_hp_ev_text.png"),
    position=(1340, 505),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_stat_text = BluePyllElement(
    label="tv_mon_atk_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_atk_stat_text.png"),
    position=(1195, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_iv_text = BluePyllElement(
    label="tv_mon_atk_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_atk_iv_text.png"),
    position=(1270, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_atk_ev_text = BluePyllElement(
    label="tv_mon_atk_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_atk_ev_text.png"),
    position=(1340, 535),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_stat_text = BluePyllElement(
    label="tv_mon_def_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_def_stat_text.png"),
    position=(1195, 565),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_iv_text = BluePyllElement(
    label="tv_mon_def_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_def_iv_text.png"),
    position=(1270, 565),
    size=(60, 30),
    is_static=False,
)

tv_mon_def_ev_text = BluePyllElement(
    label="tv_mon_def_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_def_ev_text.png"),
    position=(1340, 570),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_stat_text = BluePyllElement(
    label="tv_mon_spa_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spa_stat_text.png"),
    position=(1195, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_iv_text = BluePyllElement(
    label="tv_mon_spa_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spa_iv_text.png"),
    position=(1270, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spa_ev_text = BluePyllElement(
    label="tv_mon_spa_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spa_ev_text.png"),
    position=(1340, 595),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_stat_text = BluePyllElement(
    label="tv_mon_spd_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spd_stat_text.png"),
    position=(1195, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_iv_text = BluePyllElement(
    label="tv_mon_spd_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spd_iv_text.png"),
    position=(1270, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spd_ev_text = BluePyllElement(
    label="tv_mon_spd_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spd_ev_text.png"),
    position=(1340, 625),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_stat_text = BluePyllElement(
    label="tv_mon_spe_stat_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spe_stat_text.png"),
    position=(1195, 655),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_iv_text = BluePyllElement(
    label="tv_mon_spe_iv_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spe_iv_text.png"),
    position=(1270, 655),
    size=(60, 30),
    is_static=False,
)

tv_mon_spe_ev_text = BluePyllElement(
    label="tv_mon_spe_ev_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_spe_ev_text.png"),
    position=(1340, 655),
    size=(60, 30),
    is_static=False,
)

tv_add_to_party_button = BluePyllElement(
    label="tv_add_to_party_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_add_to_party_button.png"),
    position=(990, 700),
    size=(315, 120),
    is_static=True,
    confidence=0.6,
    ele_txt="add to party",
)

tv_delete_this_revomon_button = BluePyllElement(
    label="tv_delete_this_revomon_button",
    ele_type="button",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_delete_this_revomon_button.png"),
    position=(990, 825),
    size=(315, 120),
    is_static=True,
    confidence=0.6,
    ele_txt="delete this revomon",
)

tv_mon_move1_text = BluePyllElement(
    label="tv_mon_move1_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_move1_text.png"),
    position=(1315, 715),
    size=(250, 50),
    is_static=False,
)

tv_mon_move2_text = BluePyllElement(
    label="tv_mon_move2_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_move2_text.png"),
    position=(1315, 770),
    size=(250, 50),
    is_static=False,
)

tv_mon_move3_text = BluePyllElement(
    label="tv_mon_move3_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_move3_text.png"),
    position=(1315, 830),
    size=(250, 50),
    is_static=False,
)

tv_mon_move4_text = BluePyllElement(
    label="tv_mon_move4_text",
    ele_type="text",
    og_window_size=(1920, 1080),
    path=str(BASE_DIR / "assets" / "tv_assets" / "tv_mon_move4_text.png"),
    position=(1315, 880),
    size=(250, 50),
    is_static=False,
)


def _create_tv_slot_button(slot_number: int, x: int, y: int) -> BluePyllElement:
    return BluePyllElement(
        label=f"tv_slot{slot_number}_button",
        ele_type="button",
        og_window_size=(1920, 1080),
        path=str(
            BASE_DIR / "assets" / "tv_assets" / f"tv_slot{slot_number}_button.png"
        ),
        position=(x, y),
        size=(145, 135),
        is_static=False,
        confidence=0.6,
    )


tv_slot_buttons: dict[int, BluePyllElement] = {}

_start_x = 50
_start_y = 260
_x_increment = 145
_y_increment = 135
_columns = 6
_rows = 5

for _row in range(_rows):
    for _col in range(_columns):
        _slot_num = _row * _columns + _col + 1
        _x_pos = _start_x + (_col * _x_increment)
        _y_pos = _start_y + (_row * _y_increment)
        tv_slot_buttons[_slot_num] = _create_tv_slot_button(_slot_num, _x_pos, _y_pos)
