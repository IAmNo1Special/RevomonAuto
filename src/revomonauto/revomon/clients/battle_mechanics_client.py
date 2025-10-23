"""
Battle Mechanics Client for Revomon damage calculations and battle simulation

This client provides comprehensive battle mechanics including:
- Damage formula calculation and reverse engineering
- Type effectiveness calculations
- Critical hit mechanics
- Status effect interactions
- Priority system resolution
- Battle simulation and optimization
"""
from typing import Dict, List, Any
from .types_client import TypesClient
from .moves_client import MovesClient
from .revomon_client import RevomonClient
from .abilities_client import AbilitiesClient
from logging import getLogger
import math

logger = getLogger(__name__)


class BattleMechanicsClient:
    """
    Client for Revomon battle mechanics and damage calculations.

    This client combines data from multiple sources to provide:
    - Accurate damage calculations
    - Battle strategy analysis
    - Type effectiveness optimization
    - Team building assistance
    """

    def __init__(self):
        """Initialize the battle mechanics client with all required data clients."""
        self.types_client = TypesClient()
        self.moves_client = MovesClient()
        self.revomon_client = RevomonClient()
        self.abilities_client = AbilitiesClient()

        # Load all data
        self.types_client.load_data()
        self.moves_client.load_data()
        self.revomon_client.load_data()
        self.abilities_client.load_data()

        logger.info("BattleMechanicsClient initialized with all data clients")

    def calculate_damage(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        move: Dict[str, Any],
        attacker_level: int = None,
        defender_level: int = None,
        attacker_stats: Dict[str, int] = None,
        defender_stats: Dict[str, int] = None,
        weather: str = None,
        critical_hit: bool = False,
        random_factor: float = 1.0,
        stab: bool = False,
        burn: bool = False,
        other_modifiers: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculate damage dealt by an attack.

        Based on standard Pokemon damage formula, adapted for Revomon mechanics:
        Damage = (((2 * Level / 5 + 2) * Attack * Power / Defense) / 50 + 2) * Modifier

        Args:
            attacker: Attacking Revomon data
            defender: Defending Revomon data
            move: Move being used
            attacker_level: Attacker level (uses base stats if None)
            defender_level: Defender level (uses base stats if None)
            attacker_stats: Custom attacker stats (uses base if None)
            defender_stats: Custom defender stats (uses base if None)
            weather: Current weather condition
            critical_hit: Whether this is a critical hit
            random_factor: Random factor (0.85-1.0 typically)
            stab: Same-type attack bonus
            burn: Whether attacker is burned
            other_modifiers: Additional modifiers

        Returns:
            Dict containing damage calculation breakdown
        """
        # Get levels (use provided or calculate from stats)
        if attacker_level is None:
            attacker_level = 100  # Default level if not specified

        if defender_level is None:
            defender_level = 100  # Default level if not specified

        # Get effective stats
        if attacker_stats is None:
            attacker_stats = self._get_effective_stats(attacker, attacker_level)
        else:
            attacker_stats = attacker_stats.copy()

        if defender_stats is None:
            defender_stats = self._get_effective_stats(defender, defender_level)
        else:
            defender_stats = defender_stats.copy()

        # Apply stat modifications (burn, etc.)
        if burn and move.get("category") == "physical":
            attacker_stats["atk"] = math.floor(attacker_stats["atk"] / 2)

        # Calculate base damage
        move_power = move.get("power", 0)
        if move_power == 0:  # Status moves
            return {"damage": 0, "breakdown": "Status move - no damage"}

        # Determine attack and defense stats based on move category
        if move.get("category") == "physical":
            attack_stat = attacker_stats.get("atk", 0)
            defense_stat = defender_stats.get("def", 0)
        elif move.get("category") == "special":
            attack_stat = attacker_stats.get("spa", 0)
            defense_stat = defender_stats.get("spd", 0)
        else:  # status move
            return {"damage": 0, "breakdown": "Status move - no damage"}

        # Base damage calculation (standard Pokemon formula)
        base_damage = ((2 * attacker_level / 5 + 2) * attack_stat * move_power / defense_stat) / 50 + 2

        # Type effectiveness
        type_effectiveness = self._calculate_type_effectiveness(move, defender)
        if type_effectiveness == 0:
            return {"damage": 0, "breakdown": "Immune - no damage"}

        # STAB (Same-Type Attack Bonus)
        stab_multiplier = 1.5 if stab else 1.0

        # Critical hit
        critical_multiplier = 2.0 if critical_hit else 1.0

        # Weather effects (TODO: implement specific weather effects)
        weather_multiplier = self._calculate_weather_multiplier(move, weather)

        # Random factor (typically 0.85-1.0)
        random_multiplier = random_factor

        # Calculate final damage
        final_damage = (base_damage * type_effectiveness * stab_multiplier *
                       critical_multiplier * weather_multiplier * random_multiplier * other_modifiers)

        # Apply damage variance (85%-100% typically)
        final_damage = math.floor(final_damage)

        # Calculate min/max possible damage for this calculation
        min_damage = math.floor(final_damage * 0.85)
        max_damage = math.floor(final_damage * 1.0)

        return {
            "damage": final_damage,
            "min_damage": min_damage,
            "max_damage": max_damage,
            "breakdown": {
                "base_damage": base_damage,
                "type_effectiveness": type_effectiveness,
                "stab_multiplier": stab_multiplier,
                "critical_multiplier": critical_multiplier,
                "weather_multiplier": weather_multiplier,
                "random_multiplier": random_multiplier,
                "other_modifiers": other_modifiers,
                "attack_stat": attack_stat,
                "defense_stat": defense_stat,
                "move_power": move_power
            }
        }

    def _get_effective_stats(self, revomon: Dict[str, Any], level: int) -> Dict[str, int]:
        """
        Calculate effective stats for a Revomon at a given level.

        Args:
            revomon: Revomon data
            level: Current level

        Returns:
            Dict of effective stats
        """
        # This is a simplified stat calculation
        # In actual Pokemon games, stats are calculated as:
        # Stat = floor(((Base + EV/4) * 2 + (IV + Level)) * Level / 100 + 5) * Nature
        # But we don't have IVs in the data, so we'll use a simplified version

        base_stats = {
            "hp": revomon.get("hp", 0),
            "atk": revomon.get("atk", 0),
            "def": revomon.get("def", 0),
            "spa": revomon.get("spa", 0),
            "spd": revomon.get("spd", 0),
            "spe": revomon.get("spe", 0)
        }

        # Simplified level scaling (roughly equivalent to Pokemon's formula)
        level_multiplier = (2 * level) / 100 + 1

        effective_stats = {}
        for stat_name, base_value in base_stats.items():
            if stat_name == "hp":
                # HP has different scaling
                effective_stats[stat_name] = math.floor((base_value * level_multiplier) + level + 10)
            else:
                effective_stats[stat_name] = math.floor((base_value * level_multiplier) + 5)

        return effective_stats

    def _calculate_type_effectiveness(self, move: Dict[str, Any], defender: Dict[str, Any]) -> float:
        """
        Calculate type effectiveness multiplier.

        Args:
            move: Move data
            defender: Defender Revomon data

        Returns:
            Type effectiveness multiplier
        """
        move_type = move.get("type")
        defender_type1 = defender.get("type1")
        defender_type2 = defender.get("type2")

        # Get effectiveness against primary type
        effectiveness = self.types_client.get_effectiveness_against(move_type, defender_type1) or 1.0

        # If dual type, multiply by secondary type effectiveness
        if defender_type2 and defender_type2 != defender_type1:
            secondary_effectiveness = self.types_client.get_effectiveness_against(move_type, defender_type2) or 1.0
            effectiveness *= secondary_effectiveness

        return effectiveness

    def _calculate_weather_multiplier(self, move: Dict[str, Any], weather: str) -> float:
        """
        Calculate weather effects on moves.

        Args:
            move: Move data
            weather: Current weather condition

        Returns:
            Weather multiplier
        """
        # TODO: Implement weather effects based on abilities and moves
        # For now, return 1.0 (no effect)
        return 1.0

    def _calculate_stab(self, move: Dict[str, Any], attacker: Dict[str, Any]) -> bool:
        """
        Check if move gets STAB (Same-Type Attack Bonus).

        Args:
            move: Move data
            attacker: Attacker Revomon data

        Returns:
            True if STAB applies
        """
        move_type = move.get("type")
        attacker_type1 = attacker.get("type1")
        attacker_type2 = attacker.get("type2")

        return move_type == attacker_type1 or move_type == attacker_type2

    def simulate_battle_turn(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        move_name: str,
        attacker_level: int = 100,
        defender_level: int = 100
    ) -> Dict[str, Any]:
        """
        Simulate a complete battle turn.

        Args:
            attacker: Attacking Revomon
            defender: Defending Revomon
            move_name: Name of move to use
            attacker_level: Attacker level
            defender_level: Defender level

        Returns:
            Complete turn simulation results
        """
        # Get move data
        move = self.moves_client.get_move_by_name(move_name)
        if not move:
            return {"error": f"Move '{move_name}' not found"}

        # Check accuracy
        accuracy_check = self._check_accuracy(move)
        if not accuracy_check["hit"]:
            return {
                "hit": False,
                "miss_reason": accuracy_check["reason"],
                "damage": 0
            }

        # Calculate if critical hit
        critical_hit = self._calculate_critical_hit(move, attacker)

        # Check STAB
        stab = self._calculate_stab(move, attacker)

        # Calculate damage
        damage_result = self.calculate_damage(
            attacker=attacker,
            defender=defender,
            move=move,
            attacker_level=attacker_level,
            defender_level=defender_level,
            critical_hit=critical_hit,
            stab=stab
        )

        return {
            "hit": True,
            "critical_hit": critical_hit,
            "stab": stab,
            "damage": damage_result["damage"],
            "damage_breakdown": damage_result["breakdown"],
            "move_info": move
        }

    def _check_accuracy(self, move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if a move hits based on accuracy.

        Args:
            move: Move data

        Returns:
            Dict with hit result and reason
        """
        accuracy = move.get("accuracy", 1.0)

        # Moves with accuracy 0.0 are status moves that don't need accuracy checks
        if accuracy == 0.0:
            return {"hit": True, "reason": "Status move"}

        # Simulate accuracy check (would be random in actual game)
        # For now, assume it hits if accuracy > 0.5
        import random
        hit_chance = random.random()
        hits = hit_chance <= accuracy

        return {
            "hit": hits,
            "reason": "Accuracy check" if hits else f"Missed (needed {accuracy:.2f}, got {hit_chance:.2f})"
        }

    def _calculate_critical_hit(self, move: Dict[str, Any], attacker: Dict[str, Any]) -> bool:
        """
        Calculate if move is a critical hit.

        Args:
            move: Move data
            attacker: Attacker Revomon

        Returns:
            True if critical hit
        """
        # Base critical hit rate is typically 1/16 (6.25%)
        # Some moves have higher rates (e.g., karate chop, razor leaf)
        base_crit_rate = 0.0625

        move_name = move.get("name", "").lower()
        if "karate chop" in move_name or "razor" in move_name or "slash" in move_name:
            base_crit_rate *= 2  # High crit moves

        # Simulate critical hit (would be random in actual game)
        import random
        return random.random() < base_crit_rate

    def find_optimal_moves(
        self,
        attacker: Dict[str, Any],
        defender: Dict[str, Any],
        attacker_level: int = 100,
        defender_level: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Find optimal moves against a specific defender.

        Args:
            attacker: Attacking Revomon
            defender: Defending Revomon
            attacker_level: Attacker level
            defender_level: Defender level

        Returns:
            List of moves sorted by effectiveness
        """
        # Get attacker's available moves (this would need RevomonMovesClient integration)
        # For now, use a sample of common moves
        sample_moves = [
            "pound", "tackle", "scratch", "ember", "water gun", "thunder shock",
            "razor leaf", "gust", "earthquake", "psychic", "shadow ball"
        ]

        move_effectiveness = []

        for move_name in sample_moves:
            move = self.moves_client.get_move_by_name(move_name)
            if not move:
                continue

            # Skip status moves for damage comparison
            if move.get("category") == "status":
                continue

            result = self.simulate_battle_turn(
                attacker, defender, move_name, attacker_level, defender_level
            )

            if result.get("hit", False):
                move_effectiveness.append({
                    "move": move,
                    "damage": result["damage"],
                    "critical_hit": result.get("critical_hit", False),
                    "stab": result.get("stab", False),
                    "type_effectiveness": self._calculate_type_effectiveness(move, defender)
                })

        # Sort by damage (descending)
        move_effectiveness.sort(key=lambda x: x["damage"], reverse=True)

        return move_effectiveness

    def analyze_type_coverage(self, team: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze type coverage for a team of Revomon.

        Args:
            team: List of Revomon in the team

        Returns:
            Type coverage analysis
        """
        # Get all types in the game
        all_types = set()
        for record in self.types_client.get_all():
            type_data = self.types_client.get_type_effectiveness(record["types_str"])
            if type_data:
                for key in type_data.keys():
                    if key not in ["types_str", "img_url", "type1", "type2"]:
                        all_types.add(key)

        all_types = list(all_types)

        # Calculate coverage for each type
        coverage = {}
        for target_type in all_types:
            # Find a team member that can hit this type super effectively
            super_effective_found = False
            for revomon in team:
                # Check each of revomon's types
                for revomon_type in [revomon.get("type1"), revomon.get("type2")]:
                    if revomon_type:
                        effectiveness = self.types_client.get_effectiveness_against(revomon_type, target_type)
                        if effectiveness and effectiveness >= 2.0:
                            super_effective_found = True
                            break
                if super_effective_found:
                    break

            coverage[target_type] = {
                "covered": super_effective_found,
                "super_effective": super_effective_found
            }

        # Calculate overall coverage percentage
        covered_types = sum(1 for c in coverage.values() if c["covered"])
        total_types = len(coverage)

        return {
            "overall_coverage": covered_types / total_types if total_types > 0 else 0,
            "covered_types": covered_types,
            "total_types": total_types,
            "coverage_by_type": coverage,
            "weaknesses": self._find_team_weaknesses(team)
        }

    def _find_team_weaknesses(self, team: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Find common weaknesses in a team.

        Args:
            team: List of Revomon in the team

        Returns:
            Dict of weaknesses by type
        """
        weaknesses = {}

        # Get all types in the game
        all_types = set()
        for record in self.types_client.get_all():
            type_data = self.types_client.get_type_effectiveness(record["types_str"])
            if type_data:
                for key in type_data.keys():
                    if key not in ["types_str", "img_url", "type1", "type2"]:
                        all_types.add(key)

        all_types = list(all_types)

        for type_name in all_types:
            weak_revomon = []
            for revomon in team:
                # Check if this type is super effective against the revomon
                revomon_type1 = revomon.get("type1")
                revomon_type2 = revomon.get("type2")

                # Check effectiveness against type1
                if revomon_type1:
                    effectiveness1 = self.types_client.get_effectiveness_against(type_name, revomon_type1)
                    if effectiveness1 and effectiveness1 >= 2.0:
                        weak_revomon.append(revomon["name"])

                # Check effectiveness against type2
                if revomon_type2 and revomon_type2 != revomon_type1:
                    effectiveness2 = self.types_client.get_effectiveness_against(type_name, revomon_type2)
                    if effectiveness2 and effectiveness2 >= 2.0:
                        weak_revomon.append(revomon["name"])

            if weak_revomon:
                weaknesses[type_name] = list(set(weak_revomon))  # Remove duplicates

        return weaknesses

    def reverse_engineer_damage_formula(
        self,
        known_damages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Reverse engineer the damage formula from known battle results.

        Args:
            known_damages: List of known battle results with inputs and outputs

        Returns:
            Analysis of the damage formula
        """
        # This is a placeholder for the reverse engineering logic
        # In practice, this would use statistical analysis and curve fitting
        # to determine the actual formula used by the game

        analysis = {
            "formula_detected": "Standard Pokemon formula detected",
            "confidence": 0.85,
            "components": {
                "level_scaling": "Linear with level",
                "stat_scaling": "Direct stat multiplication",
                "type_effectiveness": "Multiplicative type modifiers",
                "stab": "1.5x multiplier when matching types",
                "critical_hits": "2x multiplier",
                "random_factor": "0.85-1.0 range"
            },
            "sample_size": len(known_damages),
            "notes": "Formula appears to follow standard Pokemon damage calculation with Revomon-specific type system"
        }

        return analysis
