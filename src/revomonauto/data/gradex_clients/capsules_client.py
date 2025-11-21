"""
Client for accessing Revomon capsules data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class CapsulesClient(BaseDataClient):
    """
    Client for accessing Revomon capsules data.

    Each record contains capsule information including:
    - cap_num: Capsule number (unique identifier)
    - move_id: Associated move ID
    - move_name: Name of the move in the capsule
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/capsules.json")

    def get_primary_key_field(self) -> str:
        return "cap_num"

    def get_capsule(self, cap_num: int) -> Optional[Dict[str, Any]]:
        """
        Get capsule data by capsule number.

        Args:
            cap_num: The capsule number

        Returns:
            Capsule data, or None if not found
        """
        return self.get_by_primary_key(cap_num)

    def get_capsule_by_move_id(self, move_id: int) -> Optional[Dict[str, Any]]:
        """
        Get capsule data by move ID.

        Args:
            move_id: The move ID

        Returns:
            Capsule data, or None if not found
        """
        return self.find_first_by_field("move_id", move_id)

    def get_capsule_by_move_name(self, move_name: str) -> Optional[Dict[str, Any]]:
        """
        Get capsule data by move name.

        Args:
            move_name: The move name

        Returns:
            Capsule data, or None if not found
        """
        return self.find_first_by_field("move_name", move_name)

    def get_all_moves_in_capsules(self) -> List[str]:
        """
        Get all move names available in capsules.

        Returns:
            List of move names in capsules
        """
        self.load_data()
        return [record["move_name"] for record in self._data]

    def get_capsules_by_move_name_pattern(self, pattern: str) -> List[Dict[str, Any]]:
        """
        Get capsules containing moves with names matching a pattern.

        Args:
            pattern: Pattern to search for in move names

        Returns:
            List of matching capsules
        """
        self.load_data()
        pattern = pattern.lower()
        return [record.copy() for record in self._data
                if pattern in record["move_name"].lower()]
