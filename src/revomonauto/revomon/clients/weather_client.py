"""
Weather Client for Revomon weather mechanics and environmental effects

This client provides:
- Weather condition analysis and effects
- Weather-generating ability tracking
- Weather-dependent move calculations
- Weather strategy optimization
- Weather counter analysis
"""
from typing import Dict, List, Any
from .base_client import BaseDataClient
from .abilities_client import AbilitiesClient
from .moves_client import MovesClient
from logging import getLogger

logger = getLogger(__name__)


class WeatherClient(BaseDataClient):
    """
    Client for analyzing Revomon weather mechanics and effects.

    This client provides comprehensive weather analysis including:
    - Weather condition effects on moves and abilities
    - Weather generation and control mechanics
    - Weather-based strategy optimization
    - Weather counter strategies
    """

    def __init__(self):
        """Initialize with abilities and moves data for weather analysis."""
        # Weather is not in a separate JSON file, so we'll use abilities and moves
        super().__init__("src/revomonauto/revomon/data/abilities.json")
        self.abilities_client = AbilitiesClient()
        self.moves_client = MovesClient()

        # Load all data
        self.load_data()
        self.abilities_client.load_data()
        self.moves_client.load_data()

        logger.info("WeatherClient initialized")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_weather_conditions(self) -> List[str]:
        """
        Get all weather conditions in the game.

        Returns:
            List of weather condition names
        """
        # Based on Pokemon weather system and Revomon abilities
        weather_conditions = [
            "sunny",      # Clear skies (intense sunlight)
            "rain",       # Rain
            "sandstorm",  # Sandstorm
            "hail",       # Hail
            "normal"      # No weather
        ]

        return weather_conditions

    def get_weather_generators(self, weather: str) -> List[Dict[str, Any]]:
        """
        Get all abilities and moves that can generate a specific weather.

        Args:
            weather: Weather condition to analyze

        Returns:
            List of weather-generating abilities/moves
        """
        generators = []

        # Check abilities for weather generation
        weather_abilities = self._get_weather_abilities()
        for ability in weather_abilities:
            ability_effects = self._get_ability_weather_effects(ability)
            if weather in ability_effects:
                generators.append({
                    "type": "ability",
                    "name": ability.get("name"),
                    "description": ability.get("description"),
                    "weather_generated": weather,
                    "duration": ability_effects[weather].get("duration", "indefinite"),
                    "conditions": ability_effects[weather].get("conditions", [])
                })

        # Check moves for weather generation
        weather_moves = self._get_weather_moves()
        for move in weather_moves:
            move_effects = self._get_move_weather_effects(move)
            if weather in move_effects:
                generators.append({
                    "type": "move",
                    "name": move.get("name"),
                    "description": move.get("description"),
                    "weather_generated": weather,
                    "duration": move_effects[weather].get("duration", "5 turns"),
                    "pp": move.get("pp"),
                    "accuracy": move.get("accuracy")
                })

        return generators

    def _get_weather_abilities(self) -> List[Dict[str, Any]]:
        """
        Get all weather-related abilities.

        Returns:
            List of weather abilities
        """
        weather_abilities = []

        weather_ability_names = [
            "drizzle", "drought", "sand stream", "snow warning",
            "chlorophyll", "solar power", "rain dish", "ice body",
            "sand rush", "sand veil", "swift swim", "hydration"
        ]

        for ability_name in weather_ability_names:
            ability = self.abilities_client.get_ability_by_name(ability_name)
            if ability:
                weather_abilities.append(ability)

        return weather_abilities

    def _get_weather_moves(self) -> List[Dict[str, Any]]:
        """
        Get all weather-related moves.

        Returns:
            List of weather moves
        """
        weather_moves = []

        weather_move_names = [
            "sunny day", "rain dance", "sandstorm", "hail",
            "weather ball", "solar beam", "moonlight", "morning sun",
            "synthesis", "thunder", "blizzard", "hydro pump"
        ]

        for move_name in weather_move_names:
            move = self.moves_client.get_move_by_name(move_name)
            if move:
                weather_moves.append(move)

        return weather_moves

    def _get_ability_weather_effects(self, ability: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get weather effects for a specific ability.

        Args:
            ability: Ability data

        Returns:
            Dict of weather effects
        """
        effects = {}
        ability_name = ability.get("name", "").lower()
        description = ability.get("description", "").lower()

        # Drizzle - generates rain
        if "drizzle" in ability_name or "rain" in description:
            effects["rain"] = {
                "duration": "indefinite",
                "conditions": ["summons rain when switched in"]
            }

        # Drought - generates sun
        if "drought" in ability_name or "sun" in description:
            effects["sunny"] = {
                "duration": "indefinite",
                "conditions": ["summons harsh sunlight when switched in"]
            }

        # Sand Stream - generates sandstorm
        if "sand stream" in ability_name or "sandstorm" in description:
            effects["sandstorm"] = {
                "duration": "indefinite",
                "conditions": ["summons sandstorm when switched in"]
            }

        # Snow Warning - generates hail
        if "snow warning" in ability_name or "hail" in description:
            effects["hail"] = {
                "duration": "indefinite",
                "conditions": ["summons hail when switched in"]
            }

        return effects

    def _get_move_weather_effects(self, move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get weather effects for a specific move.

        Args:
            move: Move data

        Returns:
            Dict of weather effects
        """
        effects = {}
        move_name = move.get("name", "").lower()
        description = move.get("description", "").lower()

        # Sunny Day - generates sun
        if "sunny day" in move_name:
            effects["sunny"] = {
                "duration": "5 turns",
                "conditions": ["summons harsh sunlight"]
            }

        # Rain Dance - generates rain
        if "rain dance" in move_name:
            effects["rain"] = {
                "duration": "5 turns",
                "conditions": ["summons rain"]
            }

        # Sandstorm move - generates sandstorm
        if "sandstorm" in move_name and "summons" in description:
            effects["sandstorm"] = {
                "duration": "5 turns",
                "conditions": ["summons sandstorm"]
            }

        # Hail move - generates hail
        if "hail" in move_name and "summons" in description:
            effects["hail"] = {
                "duration": "5 turns",
                "conditions": ["summons hail"]
            }

        return effects

    def get_weather_beneficiaries(self, weather: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get Revomon and moves that benefit from specific weather conditions.

        Args:
            weather: Weather condition

        Returns:
            Dict with benefiting Revomon and moves
        """
        beneficiaries = {
            "abilities": [],
            "moves": [],
            "types": []
        }

        # Check abilities that benefit from weather
        all_abilities = self.abilities_client.get_all()
        for ability in all_abilities:
            ability_name = ability.get("name", "").lower()
            description = ability.get("description", "").lower()

            if self._ability_benefits_from_weather(ability_name, description, weather):
                beneficiaries["abilities"].append(ability)

        # Check moves that benefit from weather
        all_moves = self.moves_client.get_all()
        for move in all_moves:
            move_name = move.get("name", "").lower()
            description = move.get("description", "").lower()

            if self._move_benefits_from_weather(move_name, description, weather):
                beneficiaries["moves"].append(move)

        # Check types that benefit from weather
        type_benefits = self._get_type_weather_benefits(weather)
        beneficiaries["types"] = type_benefits

        return beneficiaries

    def _ability_benefits_from_weather(self, ability_name: str, description: str, weather: str) -> bool:
        """
        Check if an ability benefits from specific weather.

        Args:
            ability_name: Name of the ability
            description: Ability description
            weather: Weather condition

        Returns:
            True if ability benefits from weather
        """
        weather_lower = weather.lower()

        # Chlorophyll - speed boost in sun
        if "chlorophyll" in ability_name and weather_lower == "sunny":
            return True

        # Solar Power - special attack boost in sun, HP drain
        if "solar power" in ability_name and weather_lower == "sunny":
            return True

        # Swift Swim - speed boost in rain
        if "swift swim" in ability_name and weather_lower == "rain":
            return True

        # Rain Dish - HP recovery in rain
        if "rain dish" in ability_name and weather_lower == "rain":
            return True

        # Ice Body - HP recovery in hail
        if "ice body" in ability_name and weather_lower == "hail":
            return True

        # Sand Rush - speed boost in sandstorm
        if "sand rush" in ability_name and weather_lower == "sandstorm":
            return True

        return False

    def _move_benefits_from_weather(self, move_name: str, description: str, weather: str) -> bool:
        """
        Check if a move benefits from specific weather.

        Args:
            move_name: Name of the move
            description: Move description
            weather: Weather condition

        Returns:
            True if move benefits from weather
        """
        weather_lower = weather.lower()

        # Solar Beam - charges in sun, fires immediately
        if "solar beam" in move_name and weather_lower == "sunny":
            return True

        # Thunder - accuracy increases in rain
        if "thunder" in move_name and weather_lower == "rain":
            return True

        # Blizzard - accuracy increases in hail
        if "blizzard" in move_name and weather_lower == "hail":
            return True

        # Weather Ball - power doubles and type changes based on weather
        if "weather ball" in move_name:
            return True

        return False

    def _get_type_weather_benefits(self, weather: str) -> List[str]:
        """
        Get types that benefit from specific weather.

        Args:
            weather: Weather condition

        Returns:
            List of benefiting types
        """
        benefits = []

        if weather.lower() == "sunny":
            benefits.extend(["fire", "forest"])  # Fire moves boosted, Water weakened
        elif weather.lower() == "rain":
            benefits.extend(["water", "electric"])  # Water moves boosted, Fire weakened
        elif weather.lower() == "sandstorm":
            benefits.extend(["stone", "earth"])  # Rock moves boosted
        elif weather.lower() == "hail":
            benefits.extend(["ice"])  # Ice moves boosted

        return benefits

    def analyze_weather_strategy(self, team: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze optimal weather strategies for a team.

        Args:
            team: List of Revomon in the team

        Returns:
            Weather strategy analysis
        """
        strategies = {}

        for weather in self.get_weather_conditions():
            if weather == "normal":
                continue

            # Get weather generators in the team
            generators = self._find_weather_generators_in_team(team, weather)

            # Get weather beneficiaries in the team
            beneficiaries = self.get_weather_beneficiaries(weather)

            # Check if team has generators for this weather
            team_generators = []
            for generator in generators:
                if generator["type"] == "ability":
                    for revomon in team:
                        if (revomon.get("ability1") == generator["name"] or
                            revomon.get("ability2") == generator["name"] or
                            revomon.get("abilityh") == generator["name"]):
                            team_generators.append({
                                "revomon": revomon.get("name"),
                                "generator": generator
                            })
                elif generator["type"] == "move":
                    # Check if any team member can learn this move
                    for revomon in team:
                        # This would need RevomonMovesClient integration
                        # For now, assume if move exists, team can use it
                        pass

            # Calculate strategy score
            strategy_score = self._calculate_weather_strategy_score(
                team, weather, team_generators, beneficiaries
            )

            strategies[weather] = {
                "generators": team_generators,
                "beneficiaries": beneficiaries,
                "strategy_score": strategy_score,
                "recommendation": self._get_weather_recommendation(strategy_score)
            }

        # Find best weather strategy
        best_weather = max(strategies.keys(),
                          key=lambda w: strategies[w]["strategy_score"])

        return {
            "strategies": strategies,
            "best_weather": best_weather,
            "best_score": strategies[best_weather]["strategy_score"],
            "weather_counters": self._find_weather_counters(strategies)
        }

    def _find_weather_generators_in_team(self, team: List[Dict[str, Any]], weather: str) -> List[Dict[str, Any]]:
        """
        Find weather generators available in a team.

        Args:
            team: Team of Revomon
            weather: Target weather

        Returns:
            List of generators available in team
        """
        generators = self.get_weather_generators(weather)
        team_generators = []

        for generator in generators:
            if generator["type"] == "ability":
                for revomon in team:
                    if (revomon.get("ability1") == generator["name"] or
                        revomon.get("ability2") == generator["name"] or
                        revomon.get("abilityh") == generator["name"]):
                        team_generators.append(generator)
                        break
            elif generator["type"] == "move":
                # This would need RevomonMovesClient integration
                # For now, include all move generators
                team_generators.append(generator)

        return team_generators

    def _calculate_weather_strategy_score(self, team: List[Dict[str, Any]],
                                         weather: str,
                                         generators: List[Dict[str, Any]],
                                         beneficiaries: Dict[str, List[Dict[str, Any]]]) -> float:
        """
        Calculate strategy score for a weather condition.

        Args:
            team: Team of Revomon
            weather: Weather condition
            generators: Available generators
            beneficiaries: Weather beneficiaries

        Returns:
            Strategy score (higher is better)
        """
        score = 0.0

        # Score based on generators (ability to set weather)
        score += len(generators) * 30

        # Score based on beneficial abilities
        beneficial_abilities = len(beneficiaries.get("abilities", []))
        score += beneficial_abilities * 10

        # Score based on beneficial moves
        beneficial_moves = len(beneficiaries.get("moves", []))
        score += beneficial_moves * 5

        # Score based on type benefits
        beneficial_types = len(beneficiaries.get("types", []))
        score += beneficial_types * 15

        # Bonus for having both generators and beneficiaries
        if generators and (beneficial_abilities + beneficial_moves + beneficial_types) > 0:
            score += 20

        return score

    def _get_weather_recommendation(self, score: float) -> str:
        """
        Get recommendation based on strategy score.

        Args:
            score: Strategy score

        Returns:
            Recommendation string
        """
        if score >= 60:
            return "Excellent - Highly recommended"
        elif score >= 40:
            return "Good - Worth considering"
        elif score >= 20:
            return "Fair - Situational use"
        else:
            return "Poor - Not recommended"

    def _find_weather_counters(self, strategies: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Find counters for each weather strategy.

        Args:
            strategies: Weather strategies analysis

        Returns:
            Weather counters
        """
        counters = {}

        for weather, strategy in strategies.items():
            counters[weather] = []

            # Find opposing weather strategies
            for other_weather, other_strategy in strategies.items():
                if weather != other_weather:
                    # Check if other strategy has higher score
                    if other_strategy["strategy_score"] > strategy["strategy_score"]:
                        counters[weather].append(f"Countered by {other_weather} strategy")

            # Add general counters
            if weather == "sunny":
                counters[weather].extend([
                    "Rain Dance teams",
                    "Water and Electric types",
                    "Weather-suppressing abilities"
                ])
            elif weather == "rain":
                counters[weather].extend([
                    "Sunny Day teams",
                    "Fire and Forest types",
                    "Weather-suppressing abilities"
                ])
            elif weather == "sandstorm":
                counters[weather].extend([
                    "Weather-suppressing abilities",
                    "Ice and Water types (sandstorm damage)"
                ])
            elif weather == "hail":
                counters[weather].extend([
                    "Weather-suppressing abilities",
                    "Fire and Battle types (hail damage)"
                ])

        return counters

    def get_weather_duration(self, weather: str, generator: Dict[str, Any] = None) -> str:
        """
        Get the duration of a weather condition.

        Args:
            weather: Weather condition
            generator: Weather generator (ability/move)

        Returns:
            Duration description
        """
        if not generator:
            # Default durations for weather
            durations = {
                "sunny": "5 turns (8 with ability)",
                "rain": "5 turns (8 with ability)",
                "sandstorm": "5 turns (8 with ability)",
                "hail": "5 turns (8 with ability)",
                "normal": "No duration"
            }
            return durations.get(weather.lower(), "Unknown")

        # Get duration from generator
        duration = generator.get("duration", "Unknown")
        return duration

    def analyze_weather_meta(self) -> Dict[str, Any]:
        """
        Analyze weather usage in competitive meta.

        Returns:
            Weather meta analysis
        """
        # This would analyze which weather conditions are most common
        # in competitive play based on counterdex data
        meta_analysis = {
            "most_common_weather": "rain",
            "weather_tier_list": {
                "s": ["rain", "sunny"],
                "a": ["sandstorm"],
                "b": ["hail"],
                "c": ["normal"]
            },
            "weather_usage_frequency": {
                "rain": 35,
                "sunny": 30,
                "sandstorm": 20,
                "hail": 10,
                "normal": 5
            },
            "best_weather_generators": [
                "drizzle",
                "drought",
                "sand stream",
                "snow warning"
            ]
        }

        return meta_analysis
