"""
Client for accessing Revomon abilities data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class AbilitiesClient(BaseDataClient):
    """
    Client for accessing Revomon abilities data.

    Each record contains ability information including:
    - name: The ability name (unique identifier)
    - description: Detailed description of the ability's effects
    """

    def __init__(self):
        super().__init__("src/revomonauto/data/gradex_jsons/abilities.json")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_ability(self, ability_name: str) -> Optional[Dict[str, Any]]:
        """
        Get ability data by name.

        Args:
            ability_name: The name of the ability

        Returns:
            Ability data, or None if not found
        """
        return self.get_by_primary_key(ability_name)

    def get_all_abilities(self) -> List[str]:
        """
        Get all available ability names.

        Returns:
            List of all ability names
        """
        self.load_data()
        return [record["name"] for record in self._data]

    def search_abilities_by_description(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search abilities by description text.

        Args:
            search_term: Text to search for in ability descriptions

        Returns:
            List of abilities containing the search term
        """
        self.load_data()
        search_term = search_term.lower()
        return [record.copy() for record in self._data
                if search_term in record["description"].lower()]

    def get_abilities_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Get abilities that contain a keyword in their name or description.

        Args:
            keyword: Keyword to search for

        Returns:
            List of matching abilities
        """
        self.load_data()
        keyword = keyword.lower()
        matches = []
        for record in self._data:
            if (keyword in record["name"].lower() or
                keyword in record["description"].lower()):
                matches.append(record.copy())
        return matches

    def get_abilities_with_stat_modification(self) -> List[Dict[str, Any]]:
        """
        Get abilities that modify stats (attack, defense, speed, etc.).

        Returns:
            List of abilities that affect stat modifications
        """
        stat_keywords = ["attack", "defense", "speed", "special attack", "special defense",
                        "stat", "increases", "raises", "lowers", "decreases"]
        return self._get_abilities_by_keywords(stat_keywords)

    def get_abilities_with_status_effects(self) -> List[Dict[str, Any]]:
        """
        Get abilities that cause or prevent status effects.

        Returns:
            List of abilities related to status effects
        """
        status_keywords = ["poison", "paralyze", "sleep", "freeze", "burn", "confuse",
                          "flinch", "status", "condition", "ailment"]
        return self._get_abilities_by_keywords(status_keywords)

    def get_abilities_with_weather_effects(self) -> List[Dict[str, Any]]:
        """
        Get abilities that interact with weather conditions.

        Returns:
            List of abilities related to weather
        """
        weather_keywords = ["weather", "sun", "rain", "sand", "hail", "sunshine", "sunlight"]
        return self._get_abilities_by_keywords(weather_keywords)

    def get_abilities_with_type_effects(self) -> List[Dict[str, Any]]:
        """
        Get abilities that have type-related effects.

        Returns:
            List of abilities with type modifications
        """
        type_keywords = ["type", "stab", "same-type", "super effective", "not very effective",
                        "immunity", "resistant", "weakness"]
        return self._get_abilities_by_keywords(type_keywords)

    def _get_abilities_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """
        Helper method to find abilities containing any of the specified keywords.

        Args:
            keywords: List of keywords to search for

        Returns:
            List of matching abilities
        """
        self.load_data()
        matches = []
        keywords = [kw.lower() for kw in keywords]

        for record in self._data:
            description = record["description"].lower()
            for keyword in keywords:
                if keyword in description:
                    matches.append(record.copy())
                    break  # Don't add duplicates if multiple keywords match

        return matches
