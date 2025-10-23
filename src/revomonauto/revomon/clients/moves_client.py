"""
Client for accessing Revomon moves data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class MovesClient(BaseDataClient):
    """
    Client for accessing Revomon moves data.

    Each record contains move information including:
    - id: Move ID (unique identifier)
    - name: Move name
    - category: physical, special, or status
    - type: Move type (neutral, fire, water, etc.)
    - description: Move description
    - accuracy: Move accuracy (0.0 to 1.0)
    - power: Move power (damage)
    - pp: Power points (uses per battle)
    - priority: Move priority in battle
    """

    def __init__(self):
        super().__init__("src/revomonauto/revomon/data/moves.json")

    def get_primary_key_field(self) -> str:
        return "id"

    def get_move_by_id(self, move_id: int) -> Optional[Dict[str, Any]]:
        """
        Get move data by ID.

        Args:
            move_id: The move ID

        Returns:
            Move data, or None if not found
        """
        return self.get_by_primary_key(move_id)

    def get_move_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get move data by name.

        Args:
            name: The move name

        Returns:
            Move data, or None if not found
        """
        return self.find_first_by_field("name", name)

    def get_moves_by_type(self, move_type: str) -> List[Dict[str, Any]]:
        """
        Get all moves of a specific type.

        Args:
            move_type: The move type (neutral, fire, water, etc.)

        Returns:
            List of moves of the specified type
        """
        return self.find_by_field("type", move_type)

    def get_moves_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all moves of a specific category.

        Args:
            category: Move category (physical, special, status)

        Returns:
            List of moves of the specified category
        """
        return self.find_by_field("category", category)

    def get_physical_moves(self) -> List[Dict[str, Any]]:
        """
        Get all physical moves.

        Returns:
            List of physical moves
        """
        return self.get_moves_by_category("physical")

    def get_special_moves(self) -> List[Dict[str, Any]]:
        """
        Get all special moves.

        Returns:
            List of special moves
        """
        return self.get_moves_by_category("special")

    def get_status_moves(self) -> List[Dict[str, Any]]:
        """
        Get all status moves.

        Returns:
            List of status moves
        """
        return self.get_moves_by_category("status")

    def get_moves_by_power_range(self, min_power: int, max_power: int) -> List[Dict[str, Any]]:
        """
        Get moves within a power range.

        Args:
            min_power: Minimum power
            max_power: Maximum power

        Returns:
            List of moves within the power range
        """
        self.load_data()
        return [record.copy() for record in self._data
                if min_power <= record.get("power", 0) <= max_power]

    def get_high_power_moves(self, min_power: int = 100) -> List[Dict[str, Any]]:
        """
        Get moves with high power.

        Args:
            min_power: Minimum power threshold

        Returns:
            List of high power moves
        """
        return self.get_moves_by_power_range(min_power, 999)

    def get_low_pp_moves(self, max_pp: int = 10) -> List[Dict[str, Any]]:
        """
        Get moves with low PP (power points).

        Args:
            max_pp: Maximum PP threshold

        Returns:
            List of moves with low PP
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("pp", 999) <= max_pp]

    def get_priority_moves(self, priority: int = 1) -> List[Dict[str, Any]]:
        """
        Get moves with specific priority.

        Args:
            priority: Priority level (positive = goes first, negative = goes last)

        Returns:
            List of moves with the specified priority
        """
        return self.find_by_field("priority", priority)

    def get_first_strike_moves(self) -> List[Dict[str, Any]]:
        """
        Get moves that always go first (priority > 0).

        Returns:
            List of priority moves
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("priority", 0) > 0]

    def get_last_resort_moves(self) -> List[Dict[str, Any]]:
        """
        Get moves that always go last (priority < 0).

        Returns:
            List of moves with negative priority
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("priority", 0) < 0]

    def get_inaccurate_moves(self, max_accuracy: float = 0.8) -> List[Dict[str, Any]]:
        """
        Get moves with low accuracy.

        Args:
            max_accuracy: Maximum accuracy threshold

        Returns:
            List of moves with low accuracy
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("accuracy", 1.0) <= max_accuracy]

    def get_always_hit_moves(self) -> List[Dict[str, Any]]:
        """
        Get moves that never miss (100% accuracy).

        Returns:
            List of moves with perfect accuracy
        """
        return self.find_by_field("accuracy", 1.0)

    def get_move_type_distribution(self) -> Dict[str, int]:
        """
        Get distribution of moves by type.

        Returns:
            Dictionary mapping move type to count
        """
        self.load_data()
        type_counts = {}
        for record in self._data:
            move_type = record.get("type")
            if move_type:
                type_counts[move_type] = type_counts.get(move_type, 0) + 1
        return type_counts

    def get_moves_with_description_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Get moves with a keyword in their description.

        Args:
            keyword: Keyword to search for

        Returns:
            List of moves containing the keyword
        """
        self.load_data()
        keyword = keyword.lower()
        return [record.copy() for record in self._data
                if keyword in record.get("description", "").lower()]
