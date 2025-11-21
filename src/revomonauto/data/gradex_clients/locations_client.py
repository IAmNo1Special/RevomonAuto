"""
Client for accessing Revomon spawn location data
"""
from typing import Dict, List, Any, Set
from .base_client import BaseDataClient
from logging import getLogger

logger = getLogger(__name__)


class LocationsClient(BaseDataClient):
    """
    Client for accessing Revomon spawn location data.

    This client extracts and organizes spawn location information from the Revomon dataset,
    providing specialized methods for location-based queries and analytics.

    Each Revomon can spawn in up to 3 locations with associated time periods and spawn rates.
    """

    def __init__(self):
        # Use the same data source as RevomonClient since spawn data is embedded in Revomon records
        super().__init__("src/revomonauto/data/gradex_jsons/revomon.json")

    def get_primary_key_field(self) -> str:
        return "spawn_loc1"  # Not really a primary key, but required by base class

    def get_all_spawn_locations(self) -> List[str]:
        """
        Get all unique spawn locations across all Revomon.

        Returns:
            List of unique location names
        """
        self.load_data()
        locations: Set[str] = set()

        for record in self._data:
            for i in range(1, 4):  # spawn_loc1, spawn_loc2, spawn_loc3
                loc = record.get(f"spawn_loc{i}")
                if loc:
                    locations.add(loc.lower())

        return sorted(list(locations))

    def get_revomon_by_location(self, location: str) -> List[Dict[str, Any]]:
        """
        Get all Revomon that spawn in a specific location.

        Args:
            location: The location name to search for

        Returns:
            List of Revomon that spawn in the specified location
        """
        self.load_data()
        location = location.lower()
        matches = []

        for record in self._data:
            # Check all spawn locations for this Revomon
            for i in range(1, 4):
                loc = record.get(f"spawn_loc{i}")
                if loc and loc.lower() == location:
                    # Get spawn details for this location
                    spawn_info = record.copy()
                    spawn_info["spawn_location"] = loc
                    spawn_info["spawn_time"] = record.get(f"spawn_time{i}")
                    spawn_info["spawn_rate"] = record.get("spawn_rate")
                    matches.append(spawn_info)
                    break  # Don't add the same Revomon multiple times

        return matches

    def get_spawn_details(self, location: str) -> Dict[str, Any]:
        """
        Get detailed spawn information for a location.

        Args:
            location: The location name

        Returns:
            Dictionary with location details and all Revomon that spawn there
        """
        revomon_in_location = self.get_revomon_by_location(location)

        if not revomon_in_location:
            return {"location": location, "revomon_count": 0, "revomon": []}

        # Group by spawn time and rate
        time_slots = {}
        spawn_rates = set()

        for revomon in revomon_in_location:
            time = revomon.get("spawn_time", "Unknown")
            rate = revomon.get("spawn_rate", "Unknown")

            if time not in time_slots:
                time_slots[time] = []
            time_slots[time].append(revomon)

            if rate != "Unknown":
                spawn_rates.add(rate)

        return {
            "location": location,
            "revomon_count": len(revomon_in_location),
            "unique_revomon": len(set(r["name"] for r in revomon_in_location)),
            "spawn_times": list(time_slots.keys()),
            "spawn_rates": list(spawn_rates),
            "time_slots": time_slots,
            "revomon": revomon_in_location
        }

    def get_locations_by_time(self, time_period: str) -> List[str]:
        """
        Get all locations that have Revomon spawning during a specific time period.

        Args:
            time_period: Time period (e.g., "4:00 to 9:59", "10:00 to 15:59")

        Returns:
            List of locations with spawns during the specified time
        """
        self.load_data()
        time_period = time_period.lower()
        locations: Set[str] = set()

        for record in self._data:
            for i in range(1, 4):
                spawn_time = record.get(f"spawn_time{i}")
                if spawn_time and time_period in spawn_time.lower():
                    for j in range(1, 4):
                        loc = record.get(f"spawn_loc{j}")
                        if loc:
                            locations.add(loc)

        return sorted(list(locations))

    def get_location_spawn_times(self, location: str) -> Dict[str, List[str]]:
        """
        Get all spawn times and corresponding Revomon for a location.

        Args:
            location: The location name

        Returns:
            Dictionary mapping time periods to lists of Revomon names
        """
        self.load_data()
        location = location.lower()
        time_revomon = {}

        for record in self._data:
            for i in range(1, 4):
                loc = record.get(f"spawn_loc{i}")
                if loc and loc.lower() == location:
                    spawn_time = record.get(f"spawn_time{i}", "Unknown")
                    revomon_name = record.get("name", "Unknown")

                    if spawn_time not in time_revomon:
                        time_revomon[spawn_time] = []
                    time_revomon[spawn_time].append(revomon_name)

        # Remove duplicates and sort
        for time_period in time_revomon:
            time_revomon[time_period] = sorted(list(set(time_revomon[time_period])))

        return time_revomon

    def get_common_spawn_times(self) -> Dict[str, int]:
        """
        Get the most common spawn time periods and their frequency.

        Returns:
            Dictionary mapping time periods to count of Revomon
        """
        self.load_data()
        time_counts = {}

        for record in self._data:
            for i in range(1, 4):
                spawn_time = record.get(f"spawn_time{i}")
                if spawn_time:
                    time_counts[spawn_time] = time_counts.get(spawn_time, 0) + 1

        # Sort by frequency (most common first)
        return dict(sorted(time_counts.items(), key=lambda x: x[1], reverse=True))

    def get_location_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about spawn locations.

        Returns:
            Dictionary with location analytics
        """
        all_locations = self.get_all_spawn_locations()
        location_stats = {}

        for location in all_locations:
            details = self.get_spawn_details(location)
            location_stats[location] = {
                "total_revomon": details["revomon_count"],
                "unique_revomon": details["unique_revomon"],
                "spawn_times": details["spawn_times"],
                "spawn_rates": details["spawn_rates"]
            }

        # Calculate summary statistics
        total_locations = len(all_locations)
        total_spawns = sum(stats["total_revomon"] for stats in location_stats.values())
        avg_revomon_per_location = total_spawns / total_locations if total_locations > 0 else 0

        return {
            "total_locations": total_locations,
            "total_spawn_entries": total_spawns,
            "avg_revomon_per_location": avg_revomon_per_location,
            "locations": location_stats,
            "common_times": self.get_common_spawn_times()
        }

    def search_locations_by_keyword(self, keyword: str) -> List[str]:
        """
        Search for locations containing a specific keyword.

        Args:
            keyword: Keyword to search for in location names

        Returns:
            List of matching locations
        """
        all_locations = self.get_all_spawn_locations()
        keyword = keyword.lower()

        return [loc for loc in all_locations if keyword in loc]
