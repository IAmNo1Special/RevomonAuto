from logging import getLogger

logger = getLogger(__name__)


class Action(dict):
    def __init__(
        self,
        action_id: int | None = None,
        status: bool | None = None,
        error_message: str | None = None,
        action_name: str | None = None,
        state_diff: dict = {},
        last_action: dict = {},
    ):
        super().__init__()
        # Initialize with default values
        self.update(
            {
                "action_id": action_id,
                "status": status,
                "error_message": error_message,
                "action_name": action_name,
                "state_diff": state_diff,
                "last_action": last_action,
            }
        )

    def __setitem__(self, key, value):
        allowed_keys = {
            "action_id",
            "status",
            "error_message",
            "action_name",
            "state_diff",
            "last_action",
        }
        if key not in allowed_keys:
            raise KeyError(f"Invalid key: {key}. Only {allowed_keys} are allowed")
        super().__setitem__(key, value)

    def update(self, other=None, **kwargs):
        if other is not None:
            for k, v in other.items() if hasattr(other, "items") else other:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __delitem__(self, key):
        raise TypeError("Deleting keys is not allowed")


class Actions(list):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if args and isinstance(args[0], (list, tuple)):
            for item in args[0]:
                self.append(item)

    def append(self, item):
        if not isinstance(item, Action):
            raise TypeError("Only FixedKeysDict objects can be added to this list")
        super().append(item)

    def extend(self, items):
        for item in items:
            self.append(item)

    def __setitem__(self, index, value):
        if not isinstance(value, Action):
            raise TypeError("Only FixedKeysDict objects can be added to this list")
        super().__setitem__(index, value)

    def __delitem__(self, index):
        raise TypeError("Removing items is not allowed")

    def remove(self, value):
        raise TypeError("Removing items is not allowed")

    def pop(self, index=-1):
        raise TypeError("Removing items is not allowed")

    def clear(self):
        raise TypeError("Clearing the list is not allowed")


def action(func):
    def wrapper(self, *args, **kwargs):
        def get_state_value(value):
            # Convert enum values to their string representation
            if hasattr(value, "name"):
                return value.name
            return value

        old_state = {
            "current_scene": get_state_value(self.curr_scene),
            "tv_current_page": get_state_value(self.tv_current_page),
            "tv_slot_selceted": get_state_value(self.tv_slot_selected),
            "tv_searching_for": get_state_value(self.tv_searching_for),
            "current_city": get_state_value(self.current_city),
            "current_location": get_state_value(self.current_location),
            "bluestacks_state": get_state_value(
                self.bluestacks_state.current_state
                if hasattr(self.bluestacks_state, "current_state")
                else None
            ),
            "app_state": get_state_value(
                self.app_state.current_state
                if hasattr(self.app_state, "current_state")
                else None
            ),
            "login_state": get_state_value(
                self.login_sm.current_state
                if hasattr(self.login_sm, "current_state")
                else None
            ),
            "menu_state": get_state_value(
                self.menu_sm.current_state
                if hasattr(self.menu_sm, "current_state")
                else None
            ),
            "battle_state": get_state_value(
                self.battle_sm.current_state
                if hasattr(self.battle_sm, "current_state")
                else None
            ),
            "tv_state": get_state_value(
                self.tv_sm.current_state
                if hasattr(self.tv_sm, "current_state")
                else None
            ),
        }

        # Create a new action
        current_action = Action()

        try:
            func(self, *args, **kwargs)
            self.wait_for_action(action=func.__name__)
            new_state = {
                "current_scene": get_state_value(self.curr_scene),
                "tv_current_page": get_state_value(self.tv_current_page),
                "tv_slot_selceted": get_state_value(self.tv_slot_selected),
                "tv_searching_for": get_state_value(self.tv_searching_for),
                "current_city": get_state_value(self.current_city),
                "current_location": get_state_value(self.current_location),
                "bluestacks_state": get_state_value(
                    self.bluestacks_state.current_state
                    if hasattr(self.bluestacks_state, "current_state")
                    else None
                ),
                "app_state": get_state_value(
                    self.app_state.current_state
                    if hasattr(self.app_state, "current_state")
                    else None
                ),
                "login_state": get_state_value(
                    self.login_sm.current_state
                    if hasattr(self.login_sm, "current_state")
                    else None
                ),
                "menu_state": get_state_value(
                    self.menu_sm.current_state
                    if hasattr(self.menu_sm, "current_state")
                    else None
                ),
                "battle_state": get_state_value(
                    self.battle_sm.current_state
                    if hasattr(self.battle_sm, "current_state")
                    else None
                ),
                "tv_state": get_state_value(
                    self.tv_sm.current_state
                    if hasattr(self.tv_sm, "current_state")
                    else None
                ),
            }
            current_action.update(
                {
                    "action_id": len(self.actions) + 1,
                    "status": True,
                    "error_message": None,
                    "action_name": func.__name__,
                    "state_diff": {
                        k: {"prev": str(old_state.get(k)), "new": str(new_state.get(k))}
                        for k in set(old_state) | set(new_state)
                        if old_state.get(k) != new_state.get(k)
                    },
                    "last_action": (
                        {
                            "action_id": (
                                self.last_action["action_id"]
                                if self.last_action["action_id"]
                                else None
                            ),
                            "status": (
                                self.last_action["status"]
                                if self.last_action["status"]
                                else None
                            ),
                            "action_name": (
                                self.last_action["action_name"]
                                if self.last_action["action_name"]
                                else None
                            ),
                        }
                        if self.last_action
                        else None
                    ),
                }
            )
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            current_action.update(
                {
                    "action_id": len(self.actions) + 1,
                    "status": False,
                    "error_message": f"error during {func.__name__} action: {e}",
                    "action_name": func.__name__,
                    "state_diff": {
                        k: (old_state.get(k), old_state.get(k)) for k in old_state
                    },
                    "last_action": (
                        {
                            "action_id": (
                                self.last_action["action_id"]
                                if self.last_action["action_id"]
                                else None
                            ),
                            "status": (
                                self.last_action["status"]
                                if self.last_action["status"]
                                else None
                            ),
                            "action_name": (
                                self.last_action["action_name"]
                                if self.last_action["action_name"]
                                else None
                            ),
                        }
                        if self.last_action
                        else None
                    ),
                }
            )
        finally:
            # Append Action to Actions
            self.actions.append(current_action)
            self.last_action = current_action
            return self.last_action

    return wrapper
