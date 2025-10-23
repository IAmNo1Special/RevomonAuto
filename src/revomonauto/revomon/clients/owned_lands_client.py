"""
Client for accessing Revomon owned lands data
"""
from typing import Dict, List, Optional, Any
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class OwnedLandsClient(BaseDataClient):
    """
    Client for accessing Revomon owned lands data.

    Each record contains land NFT information including:
    - token_id: NFT token ID (unique identifier)
    - id: Internal land ID
    - owners_address: Owner's wallet address
    - biome: Land biome type
    - land_type: Type of land (clinic, mine, etc.)
    - rarity: Land rarity level
    - size: Land size (e.g., "2x2", "1x1")
    - img_url: Image URL
    - for_sale: Whether the land is for sale
    """

    def __init__(self):
        super().__init__("src/revomonauto/revomon/data/owned_lands.json")

    def get_primary_key_field(self) -> str:
        return "token_id"

    def get_land(self, token_id: int) -> Optional[Dict[str, Any]]:
        """
        Get land data by token ID.

        Args:
            token_id: The NFT token ID

        Returns:
            Land data, or None if not found
        """
        return self.get_by_primary_key(token_id)

    def get_lands_by_owner(self, owner_address: str) -> List[Dict[str, Any]]:
        """
        Get all lands owned by a specific address.

        Args:
            owner_address: The owner's wallet address

        Returns:
            List of lands owned by the address
        """
        return self.find_by_field("owners_address", owner_address)

    def get_lands_by_biome(self, biome: str) -> List[Dict[str, Any]]:
        """
        Get all lands in a specific biome.

        Args:
            biome: The biome type

        Returns:
            List of lands in the specified biome
        """
        return self.find_by_field("biome", biome)

    def get_lands_by_type(self, land_type: str) -> List[Dict[str, Any]]:
        """
        Get all lands of a specific type.

        Args:
            land_type: The land type (clinic, mine, etc.)

        Returns:
            List of lands of the specified type
        """
        return self.find_by_field("land_type", land_type)

    def get_lands_by_rarity(self, rarity: str) -> List[Dict[str, Any]]:
        """
        Get all lands of a specific rarity.

        Args:
            rarity: The rarity level

        Returns:
            List of lands of the specified rarity
        """
        return self.find_by_field("rarity", rarity)

    def get_lands_by_size(self, size: str) -> List[Dict[str, Any]]:
        """
        Get all lands of a specific size.

        Args:
            size: The land size (e.g., "2x2", "1x1")

        Returns:
            List of lands of the specified size
        """
        return self.find_by_field("size", size)

    def get_lands_for_sale(self) -> List[Dict[str, Any]]:
        """
        Get all lands currently for sale.

        Returns:
            List of lands for sale
        """
        self.load_data()
        return [record.copy() for record in self._data
                if record.get("for_sale", 0) == 1]

    def get_unique_owners(self) -> List[str]:
        """
        Get all unique owner addresses.

        Returns:
            List of unique owner addresses
        """
        self.load_data()
        owners = set()
        for record in self._data:
            owner = record.get("owners_address")
            if owner:
                owners.add(owner)
        return list(owners)

    def get_biome_distribution(self) -> Dict[str, int]:
        """
        Get count of lands by biome.

        Returns:
            Dictionary mapping biome to count
        """
        self.load_data()
        biome_counts = {}
        for record in self._data:
            biome = record.get("biome")
            if biome:
                biome_counts[biome] = biome_counts.get(biome, 0) + 1
        return biome_counts

    def get_rarity_distribution(self) -> Dict[str, int]:
        """
        Get count of lands by rarity.

        Returns:
            Dictionary mapping rarity to count
        """
        self.load_data()
        rarity_counts = {}
        for record in self._data:
            rarity = record.get("rarity")
            if rarity:
                rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        return rarity_counts
