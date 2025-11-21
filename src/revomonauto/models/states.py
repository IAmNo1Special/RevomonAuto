from enum import Enum, auto
from functools import wraps


class GameState(Enum):
    # Login Flow
    NOT_STARTED = auto()
    STARTED = auto()

    # Main Game Loop
    OVERWORLD = auto()  # Walking around, idle
    MAIN_MENU = auto()  # Main menu is open

    # Sub-menus
    MENU_BAG = auto()
    WARDROBE = auto()
    FRIENDS_LIST = auto()
    SETTINGS = auto()
    REVODEX = auto()
    MARKET = auto()
    DISCUSSION = auto()
    CLAN = auto()

    # Battle Flow
    PVP_QUEUE = auto()
    BATTLE = auto()

    # TV
    TV = auto()


class BattleState(Enum):
    # Sub-states for when GameState is BATTLE
    IDLE = auto()
    BAG_OPEN = auto()
    ATTACKS_MENU_OPEN = auto()
    WAITING_FOR_OPPONENT = auto()


def requires_state(*allowed_states):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.game_state not in allowed_states:
                self.logger.warning(
                    f"Action {func.__name__} skipped. Required: {allowed_states}, Current: {self.game_state}"
                )
                return
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
