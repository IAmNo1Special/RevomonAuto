"""
Client for accessing Revomon species data
"""

from logging import getLogger
from typing import Any, Dict, List, Optional

from .base_client import BaseDataClient

logger = getLogger(__name__)


class RevomonClient(BaseDataClient):
    """
    Client for accessing Revomon species data.

    Each record contains comprehensive Revomon information including:
    - dex_id: Revodex number
    - name: Revomon name
    - stats: HP, Attack, Defense, Special Attack, Special Defense, Speed
    - abilities: ability1, ability2, hidden ability
    - types: type1, type2
    - evolution: evolution chain and requirements
    - spawn: locations, rates, times
    - images: various image URLs
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/revomon.json")

    def get_primary_key_field(self) -> str:
        return "dex_id"

    def get_revomon_by_id(self, dex_id: int) -> Optional[Dict[str, Any]]:
        """
        Get Revomon data by Revodex ID.

        Args:
            dex_id: The Revodex ID

        Returns:
            Revomon data, or None if not found
        """
        return self.get_by_primary_key(dex_id)

    def get_revomon_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get Revomon data by name.

        Args:
            name: The Revomon name

        Returns:
            Revomon data, or None if not found
        """
        return self.find_first_by_field("name", name)

    def get_revomon_names(self) -> List[str]:
        """
        Get all Revomon names.

        Returns:
            List of all Revomon names
        """
        self.load_data()
        return [record["name"] for record in self._data]

    def get_revomon_by_type(
        self, type1: str, type2: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all Revomon with specific type(s).

        Args:
            type1: Primary type
            type2: Secondary type (optional)

        Returns:
            List of Revomon with the specified types
        """
        self.load_data()
        if type2 is None:
            return [
                record.copy()
                for record in self._data
                if record.get("type1") == type1 or record.get("type2") == type1
            ]
        else:
            return [
                record.copy()
                for record in self._data
                if (record.get("type1") == type1 and record.get("type2") == type2)
                or (record.get("type1") == type2 and record.get("type2") == type1)
            ]

    def get_revomon_by_ability(self, ability: str) -> List[Dict[str, Any]]:
        """
        Get all Revomon with a specific ability.

        Args:
            ability: The ability name

        Returns:
            List of Revomon with the specified ability
        """
        self.load_data()
        matches = []
        for record in self._data:
            if (
                record.get("ability1") == ability
                or record.get("ability2") == ability
                or record.get("abilityh") == ability
            ):
                matches.append(record.copy())
        return matches

    def get_revomon_by_stat_total_range(
        self, min_total: int, max_total: int
    ) -> List[Dict[str, Any]]:
        """
        Get Revomon within a stat total range.

        Args:
            min_total: Minimum stat total
            max_total: Maximum stat total

        Returns:
            List of Revomon within the stat range
        """
        self.load_data()
        return [
            record.copy()
            for record in self._data
            if min_total <= record.get("stat_total", 0) <= max_total
        ]

    def get_highest_stat_total(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get Revomon with the highest stat totals.

        Args:
            limit: Number of results to return

        Returns:
            List of Revomon sorted by stat total (highest first)
        """
        self.load_data()
        sorted_data = sorted(
            self._data, key=lambda x: x.get("stat_total", 0), reverse=True
        )
        return [record.copy() for record in sorted_data[:limit]]

    def get_lowest_stat_total(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get Revomon with the lowest stat totals.

        Args:
            limit: Number of results to return

        Returns:
            List of Revomon sorted by stat total (lowest first)
        """
        self.load_data()
        sorted_data = sorted(self._data, key=lambda x: x.get("stat_total", 0))
        return [record.copy() for record in sorted_data[:limit]]

    def get_evolution_chain(self, dex_id: int) -> List[Dict[str, Any]]:
        """
        Get the complete evolution chain for a Revomon.

        Args:
            dex_id: Starting Revodex ID

        Returns:
            List of Revomon in the evolution chain
        """
        start_revomon = self.get_revomon_by_id(dex_id)
        if not start_revomon:
            return []

        chain = [start_revomon.copy()]
        current = start_revomon

        # Follow evolution chain forward
        while current.get("evo"):
            next_revomon = self.get_revomon_by_name(current["evo"])
            if next_revomon:
                chain.append(next_revomon.copy())
                current = next_revomon
            else:
                break

        return chain

    def get_revomon_by_rarity(self, rarity: str) -> List[Dict[str, Any]]:
        """
        Get Revomon by rarity level.

        Args:
            rarity: Rarity level (common, uncommon, rare, etc.)

        Returns:
            List of Revomon with the specified rarity
        """
        return self.find_by_field("rarity", rarity)

    def get_revomon_type_distribution(self) -> Dict[str, int]:
        """
        Get distribution of Revomon by primary type.

        Returns:
            Dictionary mapping primary type to count
        """
        self.load_data()
        type_counts = {}
        for record in self._data:
            primary_type = record.get("type1")
            if primary_type:
                type_counts[primary_type] = type_counts.get(primary_type, 0) + 1
        return type_counts
