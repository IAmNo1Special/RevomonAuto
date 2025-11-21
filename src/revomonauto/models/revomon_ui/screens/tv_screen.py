from bluepyll import BluePyllScreen

from ..elements import tv_elements


class TVScreen(BluePyllScreen):
    def __init__(self):
        elements = {
            "tv_advanced_search_button": tv_elements.tv_advanced_search_button,
            "tv_search_input": tv_elements.tv_search_input,
            "tv_search_button": tv_elements.tv_search_button,
            "tv_previous_page_button": tv_elements.tv_previous_page_button,
            "tv_page_number_text": tv_elements.tv_page_number_text,
            "tv_next_page_button": tv_elements.tv_next_page_button,
            "tv_mon_name_text": tv_elements.tv_mon_name_text,
            "tv_exit_button": tv_elements.tv_exit_button,
            "tv_mon_ability_text": tv_elements.tv_mon_ability_text,
            "tv_mon_og_tamer_text": tv_elements.tv_mon_og_tamer_text,
            "tv_mon_nature_text": tv_elements.tv_mon_nature_text,
            "tv_mon_exp_text": tv_elements.tv_mon_exp_text,
            "tv_mon_held_item_image": tv_elements.tv_mon_held_item_image,
            "tv_mon_types_image": tv_elements.tv_mon_types_image,
            "tv_mon_level_text": tv_elements.tv_mon_level_text,
            "tv_mon_id_text": tv_elements.tv_mon_id_text,
            "tv_mon_hp_stat_text": tv_elements.tv_mon_hp_stat_text,
            "tv_mon_hp_iv_text": tv_elements.tv_mon_hp_iv_text,
            "tv_mon_hp_ev_text": tv_elements.tv_mon_hp_ev_text,
            "tv_mon_atk_stat_text": tv_elements.tv_mon_atk_stat_text,
            "tv_mon_atk_iv_text": tv_elements.tv_mon_atk_iv_text,
            "tv_mon_atk_ev_text": tv_elements.tv_mon_atk_ev_text,
            "tv_mon_def_stat_text": tv_elements.tv_mon_def_stat_text,
            "tv_mon_def_iv_text": tv_elements.tv_mon_def_iv_text,
            "tv_mon_def_ev_text": tv_elements.tv_mon_def_ev_text,
            "tv_mon_spa_stat_text": tv_elements.tv_mon_spa_stat_text,
            "tv_mon_spa_iv_text": tv_elements.tv_mon_spa_iv_text,
            "tv_mon_spa_ev_text": tv_elements.tv_mon_spa_ev_text,
            "tv_mon_spd_stat_text": tv_elements.tv_mon_spd_stat_text,
            "tv_mon_spd_iv_text": tv_elements.tv_mon_spd_iv_text,
            "tv_mon_spd_ev_text": tv_elements.tv_mon_spd_ev_text,
            "tv_mon_spe_stat_text": tv_elements.tv_mon_spe_stat_text,
            "tv_mon_spe_iv_text": tv_elements.tv_mon_spe_iv_text,
            "tv_mon_spe_ev_text": tv_elements.tv_mon_spe_ev_text,
            "tv_add_to_party_button": tv_elements.tv_add_to_party_button,
            "tv_delete_this_revomon_button": tv_elements.tv_delete_this_revomon_button,
            "tv_mon_move1_text": tv_elements.tv_mon_move1_text,
            "tv_mon_move2_text": tv_elements.tv_mon_move2_text,
            "tv_mon_move3_text": tv_elements.tv_mon_move3_text,
            "tv_mon_move4_text": tv_elements.tv_mon_move4_text,
        }

        # Add the dynamically generated slot buttons
        for slot_num, button in tv_elements.tv_slot_buttons.items():
            elements[button.label] = button

        super().__init__(
            name="tv",
            elements=elements,
        )
