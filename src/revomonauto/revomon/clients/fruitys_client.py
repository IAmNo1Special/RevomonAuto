"""
Client for accessing Revomon fruitys data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class FruitysClient(BaseDataClient):
    """
    Client for accessing Revomon fruitys data.

    Each record contains fruity information including:
    - name: Fruity name (unique identifier)
    - description: Fruity effects and description
    - type: Fruity type (appears to be "held" for all)
    """

    def __init__(self):
        super().__init__("src/revomonauto/revomon/data/fruitys.json")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_fruity(self, fruity_name: str) -> Optional[Dict[str, Any]]:
        """
        Get fruity data by name.

        Args:
            fruity_name: The fruity name

        Returns:
            Fruity data, or None if not found
        """
        return self.get_by_primary_key(fruity_name)

    def get_damage_reducing_fruitys(self) -> List[Dict[str, Any]]:
        """
        Get fruitys that reduce damage from super-effective attacks.

        Returns:
            List of damage-reducing fruitys
        """
        self.load_data()
        damage_keywords = ["super-effective", "halve", "half damage", "reduce damage"]
        matches = []
        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in damage_keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break
        return matches

    def get_healing_fruitys(self) -> List[Dict[str, Any]]:
        """
        Get fruitys that provide healing effects.

        Returns:
            List of healing fruitys
        """
        self.load_data()
        heal_keywords = ["recover", "restore", "heal", "hp"]
        matches = []
        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in heal_keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break
        return matches

    def get_priority_fruitys(self) -> List[Dict[str, Any]]:
        """
        Get fruitys that affect move priority.

        Returns:
            List of priority-affecting fruitys
        """
        self.load_data()
        priority_keywords = ["first", "priority", "go first"]
        matches = []
        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in priority_keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break
        return matches

    def get_fruitys_by_type_effect(self, type_name: str) -> List[Dict[str, Any]]:
        """
        Get fruitys that activate against specific types.

        Args:
            type_name: The type that triggers the fruity (e.g., "toxic", "spirit")

        Returns:
            List of fruitys that respond to the specified type
        """
        self.load_data()
        type_name = type_name.lower()
        return [record.copy() for record in self._data
                if type_name in record.get("description", "").lower()]
