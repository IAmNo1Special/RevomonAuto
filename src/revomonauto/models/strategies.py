import random
from abc import ABC, abstractmethod


class BattleStrategy(ABC):
    """
    Abstract base class for battle strategies.
    """

    @abstractmethod
    def select_move(self, valid_move_names: list[str]) -> str:
        """
        Selects a move from the list of valid move names.

        Args:
            valid_move_names (list[str]): A list of valid move names.

        Returns:
            str: The name of the selected move.
        """
        pass


class RandomMove(BattleStrategy):
    """
    A battle strategy that selects a random move.
    """

    def select_move(self, valid_move_names: list[str]) -> str:
        if not valid_move_names:
            raise RuntimeError("No valid moves available for random selection")
        return random.choice(valid_move_names)
