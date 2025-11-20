from bluepyll import BluePyllScreen

from ..elements import battle_elements


class BattleScreen(BluePyllScreen):
    def __init__(self):
        super().__init__(
            name="battle",
            elements={
                "run_button": battle_elements.run_button,
                "run_button_pixel": battle_elements.run_button_pixel,
                "run_confirm_button_pixel": battle_elements.run_confirm_button_pixel,
                "team_bag_battle_button": battle_elements.team_bag_battle_button,
                "team_bag_battle_pixel": battle_elements.team_bag_battle_pixel,
                "attacks_button": battle_elements.attacks_button,
                "attacks_button_pixel": battle_elements.attacks_button_pixel,
                "exit_attacks_button": battle_elements.exit_attacks_button,
                "exit_attacks_button_pixel": battle_elements.exit_attacks_button_pixel,
                "player1_mon_name_text": battle_elements.player1_mon_name_text,
                "player1_mon_nameplate_pixel": battle_elements.player1_mon_nameplate_pixel,
                "player1_mon_lvl_text": battle_elements.player1_mon_lvl_text,
                "player1_mon_hp_img": battle_elements.player1_mon_hp_img,
                "player1_mon_move1_button": battle_elements.player1_mon_move1_button,
                "player1_mon_move2_button": battle_elements.player1_mon_move2_button,
                "player1_mon_move3_button": battle_elements.player1_mon_move3_button,
                "player1_mon_move4_button": battle_elements.player1_mon_move4_button,
                "player2_mon_name_text": battle_elements.player2_mon_name_text,
                "player2_mon_nameplate_pixel": battle_elements.player2_mon_nameplate_pixel,
                "player2_mon_lvl_text": battle_elements.player2_mon_lvl_text,
                "player2_mon_hp_img": battle_elements.player2_mon_hp_img,
                "waiting_for_opponent_text": battle_elements.waiting_for_opponent_text,
                "battle_log_image": battle_elements.battle_log_image,
            },
        )
