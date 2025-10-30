from enum import Enum, auto
from threading import Event

from bluepyll.app import BluePyllApp
from bluepyll.state_machine import StateMachine


class LoginState(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    LOGGED_IN = auto()

    @classmethod
    def get_transitions(cls) -> dict:
        """
        Define valid state transitions for the Login state machine.

        Returns:
            dict: A dictionary mapping current states to their allowed next states
        """
        return {
            cls.NOT_STARTED: [cls.STARTED],
            cls.STARTED: [cls.NOT_STARTED, cls.LOGGED_IN],
            cls.LOGGED_IN: [cls.NOT_STARTED, cls.STARTED],
        }


class BattleState(Enum):
    NOT_IN_BATTLE = auto()
    IN_PVP_QUEUE = auto()  # Automatic matchmaking queue
    PVP_CHALLENGE_RECEIVED = auto()  # Direct challenge from another player
    PVP_CHALLENGE_SENT = auto()  # User sent a challenge to another player
    IN_BATTLE = auto()
    BATTLE_BAG_OPEN = auto()
    ATTACKS_MENU_OPEN = auto()
    WAITING_FOR_OPPONENT = auto()

    @classmethod
    def get_transitions(cls) -> dict:
        """
        Define valid state transitions for the App state machine.

        Returns:
            dict: A dictionary mapping current states to their allowed next states
        """
        return {
            cls.NOT_IN_BATTLE: [
                cls.IN_PVP_QUEUE,  # User queued for PVP
                cls.PVP_CHALLENGE_RECEIVED,  # User received a PVP challenge
                cls.PVP_CHALLENGE_SENT,  # User sent a PVP challenge
                cls.IN_BATTLE,  # User is in a PVP battle
            ],
            cls.IN_PVP_QUEUE: [
                cls.NOT_IN_BATTLE,  # Cancel queue or the app was closed
                cls.IN_BATTLE,  # Match found
            ],
            cls.PVP_CHALLENGE_RECEIVED: [
                cls.NOT_IN_BATTLE,  # Decline challenge or the app was closed
                cls.IN_BATTLE,  # Accept challenge
            ],
            cls.PVP_CHALLENGE_SENT: [
                cls.NOT_IN_BATTLE,  # Challenge withdrawn or declined by other player or the app was closed
                cls.IN_BATTLE,  # Challenge accepted by other player
            ],
            cls.IN_BATTLE: [
                cls.NOT_IN_BATTLE,  # Battle ended or the app was closed
                cls.BATTLE_BAG_OPEN,  # Battle bag opened
                cls.ATTACKS_MENU_OPEN,  # Attacks menu opened
                cls.WAITING_FOR_OPPONENT,  # Waiting for opponent
            ],
            cls.BATTLE_BAG_OPEN: [cls.IN_BATTLE, cls.NOT_IN_BATTLE],
            cls.ATTACKS_MENU_OPEN: [cls.IN_BATTLE, cls.NOT_IN_BATTLE, cls.WAITING_FOR_OPPONENT],
            cls.WAITING_FOR_OPPONENT: [cls.IN_BATTLE, cls.NOT_IN_BATTLE],
        }


class MenuState(Enum):
    MAIN_MENU_CLOSED = auto()
    MAIN_MENU_OPEN = auto()
    MENU_BAG_OPEN = auto()
    WARDROBE_OPEN = auto()
    FRIENDS_LIST_OPEN = auto()
    SETTINGS_OPEN = auto()
    REVODEX_OPEN = auto()
    MARKET_OPEN = auto()
    DISCUSSION_OPEN = auto()
    CLAN_OPEN = auto()

    @classmethod
    def get_transitions(cls) -> dict:
        """
        Define valid state transitions for the Menu state machine.

        Returns:
            dict: A dictionary mapping current states to their allowed next states
        """
        return {
            cls.MAIN_MENU_CLOSED: [cls.MAIN_MENU_OPEN],
            cls.MAIN_MENU_OPEN: [
                cls.MAIN_MENU_CLOSED,
                cls.MENU_BAG_OPEN,
                cls.WARDROBE_OPEN,
                cls.FRIENDS_LIST_OPEN,
                cls.SETTINGS_OPEN,
                cls.REVODEX_OPEN,
                cls.MARKET_OPEN,
                cls.DISCUSSION_OPEN,
                cls.CLAN_OPEN,
            ],
            cls.MENU_BAG_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.WARDROBE_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.FRIENDS_LIST_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.SETTINGS_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.REVODEX_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.MARKET_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.DISCUSSION_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
            cls.CLAN_OPEN: [cls.MAIN_MENU_CLOSED, cls.MAIN_MENU_OPEN],
        }


class TVState(Enum):
    TV_CLOSED = auto()
    TV_OPEN = auto()
    SEARCHING_MON = auto()
    MON_SELECTED = auto()

    @classmethod
    def get_transitions(cls) -> dict:
        return {
            cls.TV_CLOSED: [cls.TV_OPEN],
            cls.TV_OPEN: [cls.TV_CLOSED, cls.SEARCHING_MON, cls.MON_SELECTED],
            cls.SEARCHING_MON: [cls.TV_CLOSED, cls.MON_SELECTED, cls.TV_OPEN],
            cls.MON_SELECTED: [cls.TV_CLOSED, cls.SEARCHING_MON, cls.TV_OPEN],
        }


class RevomonApp(BluePyllApp):
    def __init__(self):
        super().__init__(app_name="revomon", package_name="com.revomon.vr")

        # State Machines
        self.login_sm = StateMachine(
            current_state=LoginState.NOT_STARTED,
            transitions=LoginState.get_transitions(),
        )

        self.battle_sm = StateMachine(
            current_state=BattleState.NOT_IN_BATTLE,
            transitions=BattleState.get_transitions(),
        )

        self.menu_sm = StateMachine(
            current_state=MenuState.MAIN_MENU_CLOSED,
            transitions=MenuState.get_transitions(),
        )

        self.tv_sm = StateMachine(
            current_state=TVState.TV_CLOSED, transitions=TVState.get_transitions()
        )

        # Remaining attributes that don't fit into state machines
        self.is_auto_run: Event = Event()
        self.curr_scene = None
        self.is_mon_recalled = None
        self.tv_current_page = 1
        self.tv_searching_for = None
        self.tv_slot_selected = 0
        self.tv_slot_selected_attribs = None
        self.is_grading = False
        self.is_mons_graded = False

        self.current_city = None
        self.current_location = None

        self.mon_details_img = None
        self.mon_detail_imgs = None

        self.team = None  # [{name: xxxx, level: xx, type: xxxx, ability: xxxx, nature: xxxx, current_hp: xx, max_hp: xx, moves: [xxxx, xxxx, xxxx, xxxx],}, ...]
        self.mon_on_field = {
            "name": None,
            "level": None,
            "current_hp_percentage": None,
            "current_hp": None,
            "max_hp": None,
            "ability": None,
            "nature": None,
            "moves": [
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
            ],
        }
        self.last_move_used = None  # {used_by: xxxx, move_name: xxxx, move_type: xxxx, starting_pp: xx, ending_pp: xx, total_pp: xx}

        self.opps_team = None  # [{name: xxxx, level: xx, type: xxxx, ability: xxxx, nature: xxxx, current_hp: xx, max_hp: xx, moves: [xxxx, xxxx, xxxx, xxxx],}, ...]
        self.opps_mon_on_field = {
            "name": None,
            "level": None,
            "current_hp_percentage": None,
            "current_hp": None,
            "max_hp": None,
            "ability": None,
            "nature": None,
            "moves": [
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
                {"name": None, "type": None, "pp": {"current": None, "total": None}},
            ],
        }
        self.opps_last_move_used = None  # {used_by: xxxx, move_name: xxxx, move_type: xxxx, starting_pp: xx, ending_pp: xx, total_pp: xx}
