"""
Client for accessing Revomon natures data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class NaturesClient(BaseDataClient):
    """
    Client for accessing Revomon natures data.

    Each record contains nature information including:
    - name: Nature name (unique identifier)
    - buffs: Stat that gets increased (null if neutral)
    - debuffs: Stat that gets decreased (null if neutral)
    - likes: Flavor liked by Revomon with this nature
    - dislikes: Flavor disliked by Revomon with this nature
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/natures.json")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_nature(self, nature_name: str) -> Optional[Dict[str, Any]]:
        """
        Get nature data by name.

        Args:
            nature_name: The nature name

        Returns:
            Nature data, or None if not found
        """
        return self.get_by_primary_key(nature_name)

    def get_natures_with_stat_buffs(self) -> List[Dict[str, Any]]:
        """
        Get natures that increase stats.

        Returns:
            List of natures with stat buffs
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("buffs") is not None]

    def get_neutral_natures(self) -> List[Dict[str, Any]]:
        """
        Get neutral natures (no stat changes).

        Returns:
            List of neutral natures
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("buffs") is None and record.get("debuffs") is None]

    def get_natures_by_buffed_stat(self, stat: str) -> List[Dict[str, Any]]:
        """
        Get natures that buff a specific stat.

        Args:
            stat: The stat that gets buffed

        Returns:
            List of natures that buff the specified stat
        """
        return self.find_by_field("buffs", stat)

    def get_natures_by_debuffed_stat(self, stat: str) -> List[Dict[str, Any]]:
        """
        Get natures that debuff a specific stat.

        Args:
            stat: The stat that gets debuffed

        Returns:
            List of natures that debuff the specified stat
        """
        return self.find_by_field("debuffs", stat)

    def get_natures_by_flavor_preference(self, flavor: str, preference_type: str = "likes") -> List[Dict[str, Any]]:
        """
        Get natures by flavor preference.

        Args:
            flavor: The flavor (spicy, sour, sweet, dry, bitter)
            preference_type: "likes" or "dislikes"

        Returns:
            List of natures with the specified flavor preference
        """
        return self.find_by_field(preference_type, flavor)

    def get_speed_boosting_natures(self) -> List[Dict[str, Any]]:
        """
        Get natures that boost speed.

        Returns:
            List of speed-boosting natures
        """
        return self.get_natures_by_buffed_stat("spe")

    def get_attack_boosting_natures(self) -> List[Dict[str, Any]]:
        """
        Get natures that boost attack.

        Returns:
            List of attack-boosting natures
        """
        return self.get_natures_by_buffed_stat("atk")
