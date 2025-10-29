"""
Client for accessing Revomon moves data (which moves each Revomon can learn)
"""

from logging import getLogger
from typing import Any, Dict, List

from .base_client import BaseDataClient

logger = getLogger(__name__)


class RevomonMovesClient(BaseDataClient):
    """
    Client for accessing Revomon moves data.

    Each record contains information about which moves a Revomon can learn:
    - mon_dex_id: Revomon's Revodex ID
    - mon_name: Revomon name
    - move_id: Move ID
    - move_name: Move name
    - method: Learning method (levelup, machine, etc.)
    - level: Level learned (for levelup method)
    """

    def __init__(self):
        super().__init__("src/revomonauto/revomon/data/revomon_moves.json")

    def get_primary_key_field(self) -> str:
        # Composite key, but we'll use a combination for unique identification
        return "mon_dex_id"

    def get_moves_by_revomon_id(self, dex_id: int) -> List[Dict[str, Any]]:
        """
        Get all moves learnable by a Revomon by Revodex ID.

        Args:
            dex_id: The Revomon's Revodex ID

        Returns:
            List of moves the Revomon can learn
        """
        self.load_data()
        return [
            record.copy() for record in self._data if record.get("mon_dex_id") == dex_id
        ]

    def get_moves_by_revomon_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Get all moves learnable by a Revomon by name.

        Args:
            name: The Revomon name

        Returns:
            List of moves the Revomon can learn
        """
        self.load_data()
        return [
            record.copy() for record in self._data if record.get("mon_name") == name
        ]

    def get_moves_by_learning_method(self, method: str) -> List[Dict[str, Any]]:
        """
        Get all moves learned by a specific method.

        Args:
            method: Learning method (levelup, machine, etc.)

        Returns:
            List of moves learned by the specified method
        """
        return self.find_by_field("method", method)

    def get_levelup_moves(self) -> List[Dict[str, Any]]:
        """
        Get all moves learned through leveling up.

        Returns:
            List of level-up moves
        """
        return self.get_moves_by_learning_method("levelup")

    def get_machine_moves(self) -> List[Dict[str, Any]]:
        """
        Get all moves learned through TMs/HMs.

        Returns:
            List of machine moves
        """
        return self.get_moves_by_learning_method("machine")

    def get_moves_learned_at_level(self, level: int) -> List[Dict[str, Any]]:
        """
        Get all moves learned at a specific level.

        Args:
            level: The level

        Returns:
            List of moves learned at the specified level
        """
        self.load_data()
        return [
            record.copy()
            for record in self._data
            if record.get("method") == "levelup" and record.get("level") == level
        ]

    def get_revomon_levelup_moves_by_level(
        self, dex_id: int, level: int
    ) -> List[Dict[str, Any]]:
        """
        Get moves a Revomon learns at a specific level.

        Args:
            dex_id: The Revomon's Revodex ID
            level: The level

        Returns:
            List of moves learned at the specified level
        """
        self.load_data()
        return [
            record.copy()
            for record in self._data
            if record.get("mon_dex_id") == dex_id
            and record.get("method") == "levelup"
            and record.get("level") == level
        ]

    def get_all_learnable_moves(self) -> List[str]:
        """
        Get all unique move names that can be learned.

        Returns:
            List of all learnable move names
        """
        self.load_data()
        moves = set()
        for record in self._data:
            moves.add(record.get("move_name", ""))
        return list(moves)

    def get_move_learning_methods(self, move_name: str) -> List[Dict[str, Any]]:
        """
        Get all ways a move can be learned.

        Args:
            move_name: The move name

        Returns:
            List of learning methods for the move
        """
        self.load_data()
        return [
            record.copy()
            for record in self._data
            if record.get("move_name") == move_name
        ]

    def get_revomon_with_move(self, move_name: str) -> List[Dict[str, Any]]:
        """
        Get all Revomon that can learn a specific move.

        Args:
            move_name: The move name

        Returns:
            List of Revomon that can learn the move
        """
        self.load_data()
        return [
            record.copy()
            for record in self._data
            if record.get("move_name") == move_name
        ]

    def get_learning_method_distribution(self) -> Dict[str, int]:
        """
        Get count of moves by learning method.

        Returns:
            Dictionary mapping learning method to count
        """
        self.load_data()
        method_counts = {}
        for record in self._data:
            method = record.get("method")
            if method:
                method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
