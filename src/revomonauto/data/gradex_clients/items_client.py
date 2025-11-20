"""
Client for accessing Revomon items data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class ItemsClient(BaseDataClient):
    """
    Client for accessing Revomon items data.

    Each record contains item information including:
    - name: Item name (unique identifier)
    - description: Item description and effects
    - obtained_from: Where/how to obtain the item
    - cost: Item cost (null if not purchasable)
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/items.json")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_item(self, item_name: str) -> Optional[Dict[str, Any]]:
        """
        Get item data by name.

        Args:
            item_name: The item name

        Returns:
            Item data, or None if not found
        """
        return self.get_by_primary_key(item_name)

    def get_purchasable_items(self) -> List[Dict[str, Any]]:
        """
        Get items that can be purchased (have a cost).

        Returns:
            List of purchasable items
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("cost") is not None]

    def get_free_items(self) -> List[Dict[str, Any]]:
        """
        Get items that are free or obtained through other means.

        Returns:
            List of free items
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("cost") is None]

    def get_items_by_source(self, source: str) -> List[Dict[str, Any]]:
        """
        Get items obtained from a specific source.

        Args:
            source: The source (e.g., "revocenter", "battle reward")

        Returns:
            List of items from the specified source
        """
        return self.find_by_field("obtained_from", source)

    def get_items_by_cost_range(self, min_cost: int, max_cost: int) -> List[Dict[str, Any]]:
        """
        Get items within a cost range.

        Args:
            min_cost: Minimum cost
            max_cost: Maximum cost

        Returns:
            List of items within the cost range
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("cost") is not None and
                min_cost <= record.get("cost", 0) <= max_cost]

    def get_stat_boosting_items(self) -> List[Dict[str, Any]]:
        """
        Get items that boost stats.

        Returns:
            List of stat-boosting items
        """
        self.load_data()
        stat_keywords = ["attack", "defense", "speed", "accuracy", "evasion",
                        "special attack", "special defense", "raises", "boost"]
        matches = []
        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in stat_keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break
        return matches

    def get_healing_items(self) -> List[Dict[str, Any]]:
        """
        Get items that heal or cure status effects.

        Returns:
            List of healing/curing items
        """
        self.load_data()
        heal_keywords = ["heal", "cure", "restore", "recover", "burn", "poison",
                        "paralyze", "sleep", "freeze", "confusion"]
        matches = []
        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in heal_keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break
        return matches

    def get_battle_items(self) -> List[Dict[str, Any]]:
        """
        Get items used in battle.

        Returns:
            List of battle items
        """
        battle_keywords = ["battle", "in battle", "during battle", "combat"]
        return self._get_items_by_keywords(battle_keywords)

    def get_consumable_items(self) -> List[Dict[str, Any]]:
        """
        Get consumable items (used up after use).

        Returns:
            List of consumable items
        """
        consumable_keywords = ["consumed", "use", "used up", "one-time"]
        return self._get_items_by_keywords(consumable_keywords)

    def _get_items_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Helper method to find items containing any of the specified keywords.

        Args:
            keywords: List of keywords to search for

        Returns:
            List of matching items
        """
        self.load_data()
        matches = []
        keywords = [kw.lower() for kw in keywords]

        for record in self._data:
            description = record.get("description", "").lower()
            for keyword in keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break  # Don't add duplicates if multiple keywords match

        return matches
