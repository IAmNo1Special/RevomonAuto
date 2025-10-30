"""
Client for accessing Revomon counterdex data (competitive information)
"""

from logging import getLogger
from typing import Any, Dict, List, Optional

from .base_client import BaseDataClient

logger = getLogger(__name__)


class CounterdexClient(BaseDataClient):
    """
    Client for accessing Revomon counterdex data.

    Each record contains competitive information including:
    - dex_id: Revodex ID
    - name: Revomon name
    - description: Competitive description
    - tier: Competitive tier ranking
    - metamoves: Recommended movesets
    - metabuilds: Recommended builds (EVs, nature, ability)
    - tips: Competitive tips and strategies
    - counters: Revomon that counter this one
    - weakness: Type weaknesses
    """

    def __init__(self):
        super().__init__("src/revomonauto/revomon/data/counterdex.json")

    def get_primary_key_field(self) -> str:
        return "dex_id"

    def get_counterdex_entry(self, dex_id: int) -> Optional[Dict[str, Any]]:
        """
        Get counterdex data by Revodex ID.

        Args:
            dex_id: The Revodex ID

        Returns:
            Counterdex data, or None if not found
        """
        return self.get_by_primary_key(dex_id)

    def get_counterdex_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get counterdex data by Revomon name.

        Args:
            name: The Revomon name

        Returns:
            Counterdex data, or None if not found
        """
        return self.find_first_by_field("name", name)

    def get_revomon_by_tier(self, tier: str) -> List[Dict[str, Any]]:
        """
        Get all Revomon in a specific competitive tier.

        Args:
            tier: The tier (s, a, b, c, etc.)

        Returns:
            List of Revomon in the specified tier
        """
        return self.find_by_field("tier", tier)

    def get_top_tier_revomon(self, min_tier: str = "b") -> List[Dict[str, Any]]:
        """
        Get Revomon in top competitive tiers.

        Args:
            min_tier: Minimum tier to include (s is highest, then a, b, etc.)

        Returns:
            List of high-tier Revomon
        """
        tier_hierarchy = {"s": 5, "a": 4, "b": 3, "c": 2, "d": 1}
        min_value = tier_hierarchy.get(min_tier.lower(), 0)

        self.load_data()
        return [
            record.copy()
            for record in self._data
            if tier_hierarchy.get(record.get("tier", "").lower(), 0) >= min_value
        ]

    def get_revomon_with_specific_counters(
        self, counter_names: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get Revomon that are countered by specific Revomon.

        Args:
            counter_names: List of counter Revomon names

        Returns:
            List of Revomon countered by the specified counters
        """
        self.load_data()
        matches = []
        for record in self._data:
            counters = record.get("counters", "")
            if counters:
                # Split counters by newline and check if any match
                record_counters = [c.strip() for c in counters.split("\n") if c.strip()]
                for counter_name in counter_names:
                    if counter_name.lower() in [c.lower() for c in record_counters]:
                        matches.append(record.copy())
                        break
        return matches

    def get_revomon_by_weakness_count(
        self, min_weaknesses: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Get Revomon with many type weaknesses.

        Args:
            min_weaknesses: Minimum number of weaknesses

        Returns:
            List of Revomon with many weaknesses
        """
        self.load_data()
        matches = []
        for record in self._data:
            weakness_text = record.get("weakness", "")
            if weakness_text:
                # Count weaknesses by splitting on newlines
                weaknesses = [w.strip() for w in weakness_text.split("\n") if w.strip()]
                if len(weaknesses) >= min_weaknesses:
                    matches.append(record.copy())
        return matches

    def get_tank_revomon(self) -> List[Dict[str, Any]]:
        """
        Get Revomon described as tanks in their descriptions.

        Returns:
            List of tank Revomon
        """
        tank_keywords = ["tank", "defensive", "defense", "bulky", "wall"]
        return self._get_revomon_by_keywords(tank_keywords)

    def get_sweeper_revomon(self) -> List[Dict[str, Any]]:
        """
        Get Revomon described as sweepers in their descriptions.

        Returns:
            List of sweeper Revomon
        """
        sweeper_keywords = ["sweeper", "attacker", "offensive", "fast", "speed"]
        return self._get_revomon_by_keywords(sweeper_keywords)

    def get_tier_distribution(self) -> Dict[str, int]:
        """
        Get count of Revomon by competitive tier.

        Returns:
            Dictionary mapping tier to count
        """
        self.load_data()
        tier_counts = {}
        for record in self._data:
            tier = record.get("tier")
            if tier:
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
        return tier_counts

    def _get_revomon_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Helper method to find Revomon containing any of the specified keywords.

        Args:
            keywords: List of keywords to search for

        Returns:
            List of matching Revomon
        """
        self.load_data()
        matches = []
        keywords = [kw.lower() for kw in keywords]

        for record in self._data:
            description = record.get("description", "").lower()
            tips = record.get("tips", "").lower()

            for keyword in keywords:
                if keyword in description or keyword in tips:
                    matches.append(record.copy())
                    break  # Don't add duplicates if multiple keywords match

        return matches
