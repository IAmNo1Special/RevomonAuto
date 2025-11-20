"""
Status Effects Client for Revomon status conditions and interactions

This client provides:
- Status condition analysis and effects
- Status immunity and prevention tracking
- Status curing mechanics
- Status strategy optimization
- Status counter analysis
"""
from typing import Dict, List, Any
from .base_client import BaseDataClient
from .abilities_client import AbilitiesClient
from .moves_client import MovesClient
from .items_client import ItemsClient
from logging import getLogger

logger = getLogger(__name__)


class StatusEffectsClient(BaseDataClient):
    """
    Client for analyzing Revomon status effects and conditions.

    This client provides comprehensive status effect analysis including:
    - Status condition effects and mechanics
    - Status immunity and prevention
    - Status curing and management
    - Status-based strategy optimization
    - Status counter strategies
    """

    def __init__(self):
        """Initialize with abilities, moves, and items data for status analysis."""
        # Status effects are not in a separate JSON file, so we'll use abilities, moves, and items
        super().__init__("src/revomonauto/data/gradex_jsons/abilities.json")
        self.abilities_client = AbilitiesClient()
        self.moves_client = MovesClient()
        self.items_client = ItemsClient()

        # Load all data
        self.load_data()
        self.abilities_client.load_data()
        self.moves_client.load_data()
        self.items_client.load_data()

        logger.info("StatusEffectsClient initialized")

    def get_primary_key_field(self) -> str:
        return "name"

    def get_status_conditions(self) -> List[Dict[str, Any]]:
        """
        Get all status conditions in the game.

        Returns:
            List of status condition definitions
        """
        status_conditions = [
            {
                "name": "poison",
                "type": "damage_over_time",
                "description": "Deals damage each turn",
                "severity": "moderate",
                "duration": "until cured",
                "cure_methods": ["antidote", "heal", "ability"]
            },
            {
                "name": "toxic",
                "type": "damage_over_time",
                "description": "Deals increasing damage each turn",
                "severity": "high",
                "duration": "until cured",
                "cure_methods": ["antidote", "heal", "ability"]
            },
            {
                "name": "paralysis",
                "type": "speed_reduction",
                "description": "Reduces speed and may prevent actions",
                "severity": "moderate",
                "duration": "until cured",
                "cure_methods": ["cure", "heal", "ability"]
            },
            {
                "name": "sleep",
                "type": "action_prevention",
                "description": "Prevents all actions",
                "severity": "high",
                "duration": "1-7 turns",
                "cure_methods": ["wake", "heal", "ability", "time"]
            },
            {
                "name": "freeze",
                "type": "action_prevention",
                "description": "Prevents all actions",
                "severity": "high",
                "duration": "until cured",
                "cure_methods": ["defrost", "heal", "ability", "fire_move"]
            },
            {
                "name": "burn",
                "type": "damage_over_time",
                "description": "Deals damage and reduces attack",
                "severity": "moderate",
                "duration": "until cured",
                "cure_methods": ["cure", "heal", "ability"]
            },
            {
                "name": "confusion",
                "type": "action_interference",
                "description": "May cause self-damage instead of attacking",
                "severity": "low",
                "duration": "1-4 turns",
                "cure_methods": ["time", "heal", "ability"]
            },
            {
                "name": "flinch",
                "type": "action_prevention",
                "description": "Prevents action for one turn",
                "severity": "low",
                "duration": "1 turn",
                "cure_methods": ["time"]
            }
        ]

        return status_conditions

    def get_status_causers(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all moves and abilities that can cause a specific status condition.

        Args:
            status: Status condition name

        Returns:
            List of status-causing moves and abilities
        """
        causers = []

        # Check moves that cause status
        status_moves = self._get_status_moves()
        for move in status_moves:
            move_effects = self._get_move_status_effects(move)
            if status in move_effects:
                causers.append({
                    "type": "move",
                    "name": move.get("name"),
                    "description": move.get("description"),
                    "accuracy": move.get("accuracy"),
                    "pp": move.get("pp"),
                    "status_caused": status,
                    "chance": move_effects[status].get("chance", 100)
                })

        # Check abilities that cause status
        status_abilities = self._get_status_abilities()
        for ability in status_abilities:
            ability_effects = self._get_ability_status_effects(ability)
            if status in ability_effects:
                causers.append({
                    "type": "ability",
                    "name": ability.get("name"),
                    "description": ability.get("description"),
                    "status_caused": status,
                    "trigger": ability_effects[status].get("trigger", "contact")
                })

        return causers

    def _get_status_moves(self) -> List[Dict[str, Any]]:
        """
        Get all moves that can cause status conditions.

        Returns:
            List of status moves
        """
        status_move_names = [
            "toxic", "poison sting", "poison powder", "smog", "acid",
            "thunder wave", "stun spore", "glare", "nuzzle",
            "sleep powder", "hypnosis", "sing", "spore",
            "blizzard", "ice beam", "ice punch", "powder snow",
            "ember", "flamethrower", "fire punch", "will-o-wisp",
            "confusion", "psybeam", "psychic", "confuse ray",
            "bite", "headbutt", "stomp", "fake out", "rock slide"
        ]

        status_moves = []
        for move_name in status_move_names:
            move = self.moves_client.get_move_by_name(move_name)
            if move:
                status_moves.append(move)

        return status_moves

    def _get_status_abilities(self) -> List[Dict[str, Any]]:
        """
        Get all abilities that can cause status conditions.

        Returns:
            List of status abilities
        """
        status_abilities = []

        status_ability_names = [
            "poison point", "flame body", "static", "cute charm",
            "effect spore", "synchronize", "trace", "stench"
        ]

        for ability_name in status_ability_names:
            ability = self.abilities_client.get_ability_by_name(ability_name)
            if ability:
                status_abilities.append(ability)

        return status_abilities

    def _get_move_status_effects(self, move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get status effects for a specific move.

        Args:
            move: Move data

        Returns:
            Dict of status effects
        """
        effects = {}
        move_name = move.get("name", "").lower()
        description = move.get("description", "").lower()

        # Poison moves
        if any(word in move_name for word in ["toxic", "poison", "smog", "acid"]):
            if "toxic" in move_name or "badly" in description:
                effects["toxic"] = {"chance": 100}
            else:
                effects["poison"] = {"chance": 30}

        # Paralysis moves
        if any(word in move_name for word in ["thunder", "stun", "glare", "nuzzle"]):
            effects["paralysis"] = {"chance": 30}

        # Sleep moves
        if any(word in move_name for word in ["sleep", "hypnosis", "sing", "spore"]):
            effects["sleep"] = {"chance": 100 if "spore" in move_name else 60}

        # Freeze moves
        if any(word in move_name for word in ["blizzard", "ice beam", "ice punch"]):
            effects["freeze"] = {"chance": 10}

        # Burn moves
        if any(word in move_name for word in ["ember", "flamethrower", "fire punch", "will-o-wisp"]):
            if "will-o-wisp" in move_name:
                effects["burn"] = {"chance": 100}
            else:
                effects["burn"] = {"chance": 10}

        # Confusion moves
        if any(word in move_name for word in ["confusion", "psybeam", "psychic", "confuse"]):
            effects["confusion"] = {"chance": 10}

        return effects

    def _get_ability_status_effects(self, ability: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get status effects for a specific ability.

        Args:
            ability: Ability data

        Returns:
            Dict of status effects
        """
        effects = {}
        ability_name = ability.get("name", "").lower()
        _description = ability.get("description", "").lower()

        # Poison Point - poisons on contact
        if "poison point" in ability_name:
            effects["poison"] = {"trigger": "contact", "chance": 30}

        # Flame Body - burns on contact
        if "flame body" in ability_name:
            effects["burn"] = {"trigger": "contact", "chance": 30}

        # Static - paralyzes on contact
        if "static" in ability_name:
            effects["paralysis"] = {"trigger": "contact", "chance": 30}

        # Cute Charm - infatuates on contact (gender-based)
        if "cute charm" in ability_name:
            effects["infatuation"] = {"trigger": "contact", "chance": 30}

        # Effect Spore - random status on contact
        if "effect spore" in ability_name:
            effects["random"] = {"trigger": "contact", "chance": 10,
                               "possible": ["poison", "paralysis", "sleep"]}

        return effects

    def get_status_immunities(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all abilities that provide immunity to a specific status.

        Args:
            status: Status condition name

        Returns:
            List of immunity abilities
        """
        immunities = []

        # Check abilities for status immunity
        all_abilities = self.abilities_client.get_all()
        for ability in all_abilities:
            ability_name = ability.get("name", "").lower()
            _description = ability.get("description", "").lower()

            if self._ability_immunes_status(ability_name, _description, status):
                immunities.append({
                    "name": ability.get("name"),
                    "description": ability.get("description"),
                    "immunity_type": "complete",
                    "status_immuned": status
                })

        # Check types for status immunity (e.g., Electric immune to paralysis)
        type_immunities = self._get_type_status_immunities(status)
        immunities.extend(type_immunities)

        return immunities

    def _ability_immunes_status(self, ability_name: str, description: str, status: str) -> bool:
        """
        Check if an ability provides immunity to a status.

        Args:
            ability_name: Name of the ability
            description: Ability description
            status: Status condition

        Returns:
            True if ability provides immunity
        """
        # Immunity abilities
        immunity_mapping = {
            "poison": ["immunity", "poison heal"],
            "toxic": ["immunity", "poison heal"],
            "paralysis": ["limber"],
            "sleep": ["insomnia", "vital spirit"],
            "freeze": ["magma armor"],
            "burn": ["water veil"],
            "confusion": ["own tempo"]
        }

        if status in immunity_mapping:
            for immunity_ability in immunity_mapping[status]:
                if immunity_ability in ability_name:
                    return True

        return False

    def _get_type_status_immunities(self, status: str) -> List[Dict[str, Any]]:
        """
        Get type-based status immunities.

        Args:
            status: Status condition

        Returns:
            List of type immunities
        """
        immunities = []

        # Electric types are immune to paralysis
        if status == "paralysis":
            immunities.append({
                "name": "Electric type",
                "description": "Electric-type Revomon are immune to paralysis",
                "immunity_type": "type",
                "status_immuned": status,
                "types": ["electric"]
            })

        return immunities

    def get_status_cures(self, status: str) -> List[Dict[str, Any]]:
        """
        Get all methods to cure a specific status condition.

        Args:
            status: Status condition name

        Returns:
            List of cure methods
        """
        cures = []

        # Check items that cure status
        status_items = self._get_status_cure_items()
        for item in status_items:
            item_effects = self._get_item_status_effects(item)
            if status in item_effects:
                cures.append({
                    "type": "item",
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "cost": item.get("cost"),
                    "cures": [status]
                })

        # Check moves that cure status
        status_cure_moves = self._get_status_cure_moves()
        for move in status_cure_moves:
            move_effects = self._get_move_cure_effects(move)
            if status in move_effects:
                cures.append({
                    "type": "move",
                    "name": move.get("name"),
                    "description": move.get("description"),
                    "pp": move.get("pp"),
                    "cures": [status]
                })

        # Check abilities that prevent/cure status
        status_abilities = self.abilities_client.get_all()
        for ability in status_abilities:
            ability_name = ability.get("name", "").lower()
            _description = ability.get("description", "").lower()

            if self._ability_cures_status(ability_name, _description, status):
                cures.append({
                    "type": "ability",
                    "name": ability.get("name"),
                    "description": ability.get("description"),
                    "cures": [status]
                })

        return cures

    def _get_status_cure_items(self) -> List[Dict[str, Any]]:
        """
        Get all items that can cure status conditions.

        Returns:
            List of cure items
        """
        cure_item_names = [
            "antidote", "burn heal", "ice heal", "awakening", "paralyze heal",
            "full heal", "full restore", "heal powder", "energy root"
        ]

        cure_items = []
        for item_name in cure_item_names:
            item = self.items_client.get_item_by_name(item_name)
            if item:
                cure_items.append(item)

        return cure_items

    def _get_status_cure_moves(self) -> List[Dict[str, Any]]:
        """
        Get all moves that can cure status conditions.

        Returns:
            List of cure moves
        """
        cure_move_names = [
            "refresh", "heal bell", "aromatherapy", "jungle healing",
            "purify", "take heart", "sparkly swirl"
        ]

        cure_moves = []
        for move_name in cure_move_names:
            move = self.moves_client.get_move_by_name(move_name)
            if move:
                cure_moves.append(move)

        return cure_moves

    def _get_item_status_effects(self, item: Dict[str, Any]) -> List[str]:
        """
        Get status effects cured by an item.

        Args:
            item: Item data

        Returns:
            List of cured status conditions
        """
        cured_status = []
        item_name = item.get("name", "").lower()
        description = item.get("description", "").lower()

        if "antidote" in item_name or "poison" in description:
            cured_status.append("poison")
            cured_status.append("toxic")
        if "burn" in item_name or "burn" in description:
            cured_status.append("burn")
        if "ice heal" in item_name or "freeze" in description:
            cured_status.append("freeze")
        if "awakening" in item_name or "sleep" in description:
            cured_status.append("sleep")
        if "paral" in item_name or "paralysis" in description:
            cured_status.append("paralysis")
        if "heal" in item_name or "cure" in description:
            cured_status.extend(["poison", "toxic", "burn", "freeze", "sleep", "paralysis", "confusion"])

        return cured_status

    def _get_move_cure_effects(self, move: Dict[str, Any]) -> List[str]:
        """
        Get status effects cured by a move.

        Args:
            move: Move data

        Returns:
            List of cured status conditions
        """
        cured_status = []
        move_name = move.get("name", "").lower()
        _description = move.get("description", "").lower()

        if any(word in move_name for word in ["refresh", "heal bell", "aromatherapy"]):
            cured_status.extend(["poison", "toxic", "burn", "freeze", "sleep", "paralysis", "confusion"])
        if "purify" in move_name:
            cured_status.extend(["poison", "toxic", "burn", "freeze", "sleep", "paralysis", "confusion"])

        return cured_status

    def _ability_cures_status(self, ability_name: str, description: str, status: str) -> bool:
        """
        Check if an ability can cure or prevent a status.

        Args:
            ability_name: Name of the ability
            description: Ability description
            status: Status condition

        Returns:
            True if ability cures the status
        """
        # Hydration - cures status in rain
        if "hydration" in ability_name and "rain" in description:
            return True

        # Natural Cure - cures status when switching out
        if "natural cure" in ability_name:
            return True

        # Shed Skin - may cure status each turn
        if "shed skin" in ability_name:
            return True

        return False

    def analyze_status_strategy(self, team: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze status condition strategies for a team.

        Args:
            team: List of Revomon in the team

        Returns:
            Status strategy analysis
        """
        strategy = {
            "team_immunities": {},
            "team_causers": {},
            "team_cures": {},
            "status_vulnerabilities": {},
            "recommended_status_strategy": ""
        }

        # Analyze team immunities
        for status in ["poison", "toxic", "paralysis", "sleep", "freeze", "burn", "confusion"]:
            immunities = self.get_status_immunities(status)
            team_immunities = []

            for immunity in immunities:
                if immunity["type"] == "ability":
                    for revomon in team:
                        if (revomon.get("ability1") == immunity["name"] or
                            revomon.get("ability2") == immunity["name"] or
                            revomon.get("abilityh") == immunity["name"]):
                            team_immunities.append({
                                "revomon": revomon.get("name"),
                                "immunity": immunity
                            })
                            break
                elif immunity["type"] == "type":
                    for revomon in team:
                        if (revomon.get("type1") in immunity.get("types", []) or
                            revomon.get("type2") in immunity.get("types", [])):
                            team_immunities.append({
                                "revomon": revomon.get("name"),
                                "immunity": immunity
                            })
                            break

            strategy["team_immunities"][status] = team_immunities

        # Analyze team status causers
        for status in ["poison", "toxic", "paralysis", "sleep", "freeze", "burn", "confusion"]:
            causers = self.get_status_causers(status)
            team_causers = []

            for causer in causers:
                if causer["type"] == "move":
                    # Check if team can learn this move
                    for revomon in team:
                        # This would need RevomonMovesClient integration
                        pass
                elif causer["type"] == "ability":
                    for revomon in team:
                        if (revomon.get("ability1") == causer["name"] or
                            revomon.get("ability2") == causer["name"] or
                            revomon.get("abilityh") == causer["name"]):
                            team_causers.append({
                                "revomon": revomon.get("name"),
                                "causer": causer
                            })
                            break

            strategy["team_causers"][status] = team_causers

        # Analyze team cures
        for status in ["poison", "toxic", "paralysis", "sleep", "freeze", "burn", "confusion"]:
            cures = self.get_status_cures(status)
            team_cures = []

            for cure in cures:
                if cure["type"] == "item":
                    team_cures.append(cure)
                elif cure["type"] == "move":
                    # Check if team can learn this move
                    for revomon in team:
                        # This would need RevomonMovesClient integration
                        pass
                elif cure["type"] == "ability":
                    for revomon in team:
                        if (revomon.get("ability1") == cure["name"] or
                            revomon.get("ability2") == cure["name"] or
                            revomon.get("abilityh") == cure["name"]):
                            team_cures.append({
                                "revomon": revomon.get("name"),
                                "cure": cure
                            })
                            break

            strategy["team_cures"][status] = team_cures

        # Calculate vulnerabilities
        strategy["status_vulnerabilities"] = self._calculate_team_vulnerabilities(strategy)

        # Generate recommendations
        strategy["recommended_status_strategy"] = self._generate_status_recommendations(strategy)

        return strategy

    def _calculate_team_vulnerabilities(self, strategy: Dict[str, Any]) -> Dict[str, int]:
        """
        Calculate team vulnerabilities to status conditions.

        Args:
            strategy: Status strategy analysis

        Returns:
            Vulnerability scores by status
        """
        vulnerabilities = {}

        for status in ["poison", "toxic", "paralysis", "sleep", "freeze", "burn", "confusion"]:
            immunities = len(strategy["team_immunities"][status])
            causers = len(strategy["team_causers"][status])
            cures = len(strategy["team_cures"][status])

            # Vulnerability score: higher means more vulnerable
            vulnerability = causers * 2 - immunities * 3 - cures * 1
            vulnerabilities[status] = max(0, vulnerability)  # Minimum 0

        return vulnerabilities

    def _generate_status_recommendations(self, strategy: Dict[str, Any]) -> str:
        """
        Generate status strategy recommendations.

        Args:
            strategy: Status strategy analysis

        Returns:
            Recommendation string
        """
        vulnerabilities = strategy["status_vulnerabilities"]

        # Find most vulnerable status
        most_vulnerable = max(vulnerabilities.items(), key=lambda x: x[1])

        if most_vulnerable[1] > 5:
            return f"High vulnerability to {most_vulnerable[0]} - prioritize prevention"
        elif most_vulnerable[1] > 2:
            return f"Moderate vulnerability to {most_vulnerable[0]} - consider counters"
        else:
            return "Good status resistance - focus on offensive status strategies"

    def get_status_meta_analysis(self) -> Dict[str, Any]:
        """
        Analyze status conditions in competitive meta.

        Returns:
            Status meta analysis
        """
        meta_analysis = {
            "most_common_status": "paralysis",
            "status_tier_list": {
                "s": ["paralysis", "sleep"],
                "a": ["toxic", "burn"],
                "b": ["confusion", "freeze"],
                "c": ["poison"]
            },
            "status_usage_frequency": {
                "paralysis": 40,
                "sleep": 35,
                "toxic": 30,
                "burn": 25,
                "confusion": 15,
                "freeze": 10,
                "poison": 5
            },
            "best_status_preventers": [
                "limber", "insomnia", "vital spirit", "immunity"
            ],
            "best_status_causers": [
                "thunder wave", "sleep powder", "toxic", "will-o-wisp"
            ]
        }

        return meta_analysis
