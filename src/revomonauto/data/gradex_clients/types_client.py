"""
Client for accessing Revomon types data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class TypesClient(BaseDataClient):
    """
    Client for accessing Revomon type effectiveness data.

    Each record contains type matchup information including:
    - types_str: The type combination identifier (e.g., "battle", "fire/ice")
    - type1: Primary type
    - type2: Secondary type (null if single type)
    - effectiveness multipliers for all types
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/types.json")

    def get_primary_key_field(self) -> str:
        return "types_str"

    def get_type_effectiveness(self, types_str: str) -> Optional[Dict[str, Any]]:
        """
        Get type effectiveness data for a specific type combination.

        Args:
            types_str: The type combination string (e.g., "fire", "water/electric")

        Returns:
            Type effectiveness data, or None if not found
        """
        return self.get_by_primary_key(types_str)

    def get_all_types(self) -> List[str]:
        """
        Get all available type combinations.

        Returns:
            List of all type combination strings
        """
        self.load_data()
        return [record["types_str"] for record in self._data]

    def get_single_types(self) -> List[Dict[str, Any]]:
        """
        Get all single-type entries (no secondary type).

        Returns:
            List of single type records
        """
        return self.find_by_field("type2", None)

    def get_dual_types(self) -> List[Dict[str, Any]]:
        """
        Get all dual-type entries (with secondary type).

        Returns:
            List of dual type records
        """
        self.load_data()
        return [record for record in self._data if record.get("type2") is not None]

    def get_types_by_element(self, element_type: str) -> List[Dict[str, Any]]:
        """
        Get all types that include a specific element.

        Args:
            element_type: The element to search for (e.g., "fire", "water")

        Returns:
            List of types containing the specified element
        """
        self.load_data()
        return [record for record in self._data
                if record.get("type1") == element_type or record.get("type2") == element_type]

    def get_effectiveness_against(self, attacker_type: str, defender_type: str) -> Optional[float]:
        """
        Get the effectiveness multiplier of one type against another.

        Args:
            attacker_type: The attacking type combination
            defender_type: The defending type combination

        Returns:
            Effectiveness multiplier (0.0 = no effect, 0.5 = not very effective,
            1.0 = normal, 2.0 = super effective, 4.0 = very super effective)
        """
        record = self.get_type_effectiveness(defender_type)
        if not record:
            return None

        # Get effectiveness of attacker_type against defender_type
        # The record contains effectiveness values for all types
        return record.get(attacker_type, 1.0)

    def get_super_effective_types(self, defender_type: str) -> List[str]:
        """
        Get all types that are super effective (2.0x or higher) against a given type.

        Args:
            defender_type: The defending type combination

        Returns:
            List of type combinations that are super effective
        """
        record = self.get_type_effectiveness(defender_type)
        if not record:
            return []

        super_effective = []
        for type_name, effectiveness in record.items():
            # Skip metadata fields
            if type_name in ["types_str", "img_url", "type1", "type2"]:
                continue
            if effectiveness >= 2.0:
                super_effective.append(type_name)

        return super_effective

    def get_types_weak_to(self, defender_type: str) -> List[str]:
        """
        Get all types that a given type is weak to (0.5x or lower effectiveness).

        Args:
            defender_type: The defending type combination

        Returns:
            List of type combinations that the defender is weak against
        """
        record = self.get_type_effectiveness(defender_type)
        if not record:
            return []

        weak_to = []
        for type_name, effectiveness in record.items():
            # Skip metadata fields
            if type_name in ["types_str", "img_url", "type1", "type2"]:
                continue
            if 0 < effectiveness < 1.0:
                weak_to.append(type_name)

        return weak_to

    def get_immune_types(self, defender_type: str) -> List[str]:
        """
        Get all types that a given type is immune to (0.0x effectiveness).

        Args:
            defender_type: The defending type combination

        Returns:
            List of type combinations that the defender is immune to
        """
        record = self.get_type_effectiveness(defender_type)
        if not record:
            return []

        immune_to = []
        for type_name, effectiveness in record.items():
            # Skip metadata fields
            if type_name in ["types_str", "img_url", "type1", "type2"]:
                continue
            if effectiveness == 0.0:
                immune_to.append(type_name)

        return immune_to
