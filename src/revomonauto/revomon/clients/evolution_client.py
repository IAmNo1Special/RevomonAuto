"""
Evolution Client for Revomon evolution chain analysis and optimization

This client provides:
- Complete evolution chain analysis
- Evolution path optimization
- Breeding strategy assistance
- Evolution requirements tracking
- Competitive evolution meta analysis
"""

from logging import getLogger
from typing import Any, Dict, List, Optional

from .natures_client import NaturesClient
from .revomon_client import RevomonClient

logger = getLogger(__name__)


class EvolutionClient:
    """
    Client for analyzing Revomon evolution chains and optimization.

    This client extends the basic evolution functionality from RevomonClient
    to provide advanced analysis including:
    - Complete evolution trees and branching paths
    - Statistical progression analysis
    - Evolution efficiency metrics
    - Breeding optimization
    - Competitive meta evolution analysis
    """

    def __init__(self):
        """Initialize with Revomon data."""
        # Note: EvolutionClient doesn't inherit from BaseDataClient since it uses RevomonClient
        self.revomon_client = RevomonClient()
        self.natures_client = NaturesClient()

        # Load all data
        self.revomon_client.load_data()
        self.natures_client.load_data()

        logger.info("EvolutionClient initialized")

    def get_complete_evolution_tree(self, start_dex_id: int) -> Dict[str, Any]:
        """
        Get the complete evolution tree for a Revomon including all branches.

        Args:
            start_dex_id: Starting Revodex ID

        Returns:
            Complete evolution tree with all branches
        """
        start_revomon = self.revomon_client.get_revomon_by_id(start_dex_id)
        if not start_revomon:
            return {"error": f"Revomon with dex_id {start_dex_id} not found"}

        tree = {
            "root": start_revomon.copy(),
            "branches": [],
            "all_members": [start_revomon.copy()],
            "total_members": 1,
        }

        # Build evolution tree using breadth-first search
        to_process = [start_revomon]
        processed = {start_dex_id}

        while to_process:
            current = to_process.pop(0)
            current_id = current.get("dex_id")

            # Find all Revomon that evolve FROM this one
            children = self._find_evolution_children(current_id)

            if children:
                branch = {
                    "parent": current.copy(),
                    "children": children.copy(),
                    "branch_stats": self._calculate_branch_stats(children),
                }

                tree["branches"].append(branch)
                tree["all_members"].extend(children)
                tree["total_members"] += len(children)

                # Add unprocessed children to queue
                for child in children:
                    child_id = child.get("dex_id")
                    if child_id not in processed:
                        to_process.append(child)
                        processed.add(child_id)

        # Calculate tree statistics
        tree["tree_stats"] = self._calculate_tree_stats(tree["all_members"])

        return tree

    def _find_evolution_children(self, parent_dex_id: int) -> List[Dict[str, Any]]:
        """
        Find all Revomon that evolve from a given parent.

        Args:
            parent_dex_id: Parent Revodex ID

        Returns:
            List of child Revomon
        """
        parent = self.revomon_client.get_revomon_by_id(parent_dex_id)
        if not parent:
            return []

        children = []
        parent_name = parent.get("name")

        # Search through all Revomon to find those that evolve from this parent
        for record in self.revomon_client.get_all():
            # Check if this Revomon evolves from the parent
            if record.get("evo") == parent_name:
                children.append(record.copy())

        return children

    def _find_evolution_parents(self, child_dex_id: int) -> List[Dict[str, Any]]:
        """
        Find all Revomon that a given Revomon evolves from.

        Args:
            child_dex_id: Child Revodex ID

        Returns:
            List of parent Revomon
        """
        child = self.revomon_client.get_revomon_by_id(child_dex_id)
        if not child:
            return []

        parents = []
        child_name = child.get("name")

        # Search through all Revomon to find those that evolve TO this child
        for record in self.revomon_client.get_all():
            if record.get("evo") == child_name:
                parents.append(record.copy())

        return parents

    def get_evolution_path(
        self, start_dex_id: int, end_dex_id: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Find the evolution path between two Revomon.

        Args:
            start_dex_id: Starting Revodex ID
            end_dex_id: Ending Revodex ID

        Returns:
            List of Revomon in evolution path, or None if no path exists
        """
        # Use breadth-first search to find shortest path
        start_revomon = self.revomon_client.get_revomon_by_id(start_dex_id)
        end_revomon = self.revomon_client.get_revomon_by_id(end_dex_id)

        if not start_revomon or not end_revomon:
            return None

        # BFS to find path
        queue = [(start_revomon, [start_revomon])]
        visited = {start_dex_id}

        while queue:
            current, path = queue.pop(0)

            # Check if we reached the target
            if current.get("dex_id") == end_dex_id:
                return path

            # Find children and add to queue
            children = self._find_evolution_children(current.get("dex_id"))
            for child in children:
                child_id = child.get("dex_id")
                if child_id not in visited:
                    visited.add(child_id)
                    queue.append((child, path + [child]))

        return None  # No path found

    def analyze_evolution_efficiency(
        self, evolution_chain: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze the efficiency of an evolution chain.

        Args:
            evolution_chain: List of Revomon in evolution order

        Returns:
            Efficiency analysis
        """
        if len(evolution_chain) < 2:
            return {"error": "Evolution chain must have at least 2 members"}

        analysis = {
            "chain_length": len(evolution_chain),
            "total_stat_growth": {},
            "stat_efficiency": {},
            "level_requirements": [],
            "type_changes": [],
            "ability_changes": [],
        }

        # Calculate stat growth
        base_stats = evolution_chain[0]
        final_stats = evolution_chain[-1]

        stat_names = ["hp", "atk", "def", "spa", "spd", "spe"]
        for stat in stat_names:
            base_value = base_stats.get(stat, 0)
            final_value = final_stats.get(stat, 0)
            growth = final_value - base_value
            growth_percentage = (growth / base_value * 100) if base_value > 0 else 0

            analysis["total_stat_growth"][stat] = {
                "growth": growth,
                "growth_percentage": growth_percentage,
                "base_value": base_value,
                "final_value": final_value,
            }

        # Calculate total stat totals
        base_total = sum(base_stats.get(stat, 0) for stat in stat_names)
        final_total = sum(final_stats.get(stat, 0) for stat in stat_names)
        total_growth = final_total - base_total
        total_growth_percentage = (
            (total_growth / base_total * 100) if base_total > 0 else 0
        )

        analysis["total_stat_growth"]["total"] = {
            "growth": total_growth,
            "growth_percentage": total_growth_percentage,
            "base_total": base_total,
            "final_total": final_total,
        }

        # Level requirements
        for revomon in evolution_chain:
            if revomon.get("evo_lvl"):
                analysis["level_requirements"].append(
                    {
                        "name": revomon.get("name"),
                        "level_required": revomon.get("evo_lvl"),
                    }
                )

        # Type changes
        for i in range(len(evolution_chain) - 1):
            current = evolution_chain[i]
            next_rev = evolution_chain[i + 1]

            current_types = {current.get("type1"), current.get("type2")}
            next_types = {next_rev.get("type1"), next_rev.get("type2")}

            if current_types != next_types:
                analysis["type_changes"].append(
                    {
                        "from": current.get("name"),
                        "to": next_rev.get("name"),
                        "type_change": f"{current_types} -> {next_types}",
                    }
                )

        # Ability changes
        for i in range(len(evolution_chain) - 1):
            current = evolution_chain[i]
            next_rev = evolution_chain[i + 1]

            current_abilities = {
                "ability1": current.get("ability1"),
                "ability2": current.get("ability2"),
                "hidden": current.get("abilityh"),
            }
            next_abilities = {
                "ability1": next_rev.get("ability1"),
                "ability2": next_rev.get("ability2"),
                "hidden": next_rev.get("abilityh"),
            }

            if current_abilities != next_abilities:
                analysis["ability_changes"].append(
                    {
                        "from": current.get("name"),
                        "to": next_rev.get("name"),
                        "ability_change": f"{current_abilities} -> {next_abilities}",
                    }
                )

        return analysis

    def find_optimal_evolution_path(
        self,
        target_stats: Dict[str, float] = None,
        target_types: List[str] = None,
        max_evolutions: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Find evolution paths that lead to desired characteristics.

        Args:
            target_stats: Desired stat distribution (e.g., {"atk": 1.0, "spe": 0.8})
            target_types: Desired types
            max_evolutions: Maximum number of evolutions to consider

        Returns:
            List of optimal evolution paths
        """
        if not target_stats and not target_types:
            return []

        optimal_paths = []

        # Get all Revomon as starting points
        for start_revomon in self.revomon_client.get_all():
            if start_revomon.get("evo"):  # Only consider Revomon that can evolve
                # Get complete evolution chain
                chain = self.revomon_client.get_evolution_chain(
                    start_revomon.get("dex_id")
                )
                if len(chain) <= max_evolutions:
                    # Score this evolution chain
                    score = self._score_evolution_chain(
                        chain, target_stats, target_types
                    )
                    if score > 0:
                        optimal_paths.append(
                            {
                                "chain": chain,
                                "score": score,
                                "analysis": self.analyze_evolution_efficiency(chain),
                            }
                        )

        # Sort by score (descending)
        optimal_paths.sort(key=lambda x: x["score"], reverse=True)

        return optimal_paths

    def _score_evolution_chain(
        self,
        chain: List[Dict[str, Any]],
        target_stats: Dict[str, float] = None,
        target_types: List[str] = None,
    ) -> float:
        """
        Score an evolution chain based on target criteria.

        Args:
            chain: Evolution chain to score
            target_stats: Target stat distribution
            target_types: Target types

        Returns:
            Score (higher is better)
        """
        if not chain:
            return 0

        score = 0.0
        final_revomon = chain[-1]

        # Score based on target stats
        if target_stats:
            final_stat_total = final_revomon.get("stat_total", 0)
            # Higher stat total gets higher score (up to a point)
            score += min(final_stat_total / 10, 50)  # Cap at 50 points

        # Score based on target types
        if target_types:
            final_type1 = final_revomon.get("type1")
            final_type2 = final_revomon.get("type2")

            type_match = 0
            if final_type1 in target_types:
                type_match += 1
            if final_type2 and final_type2 in target_types:
                type_match += 1

            score += type_match * 20  # 20 points per matching type

        # Bonus for longer chains (more evolution options)
        score += (len(chain) - 1) * 5

        # Penalty for very low stat totals
        if final_stat_total < 300:
            score -= 20

        return score

    def get_evolution_requirements(self, dex_id: int) -> Dict[str, Any]:
        """
        Get detailed evolution requirements for a Revomon.

        Args:
            dex_id: Revodex ID

        Returns:
            Evolution requirements and conditions
        """
        revomon = self.revomon_client.get_revomon_by_id(dex_id)
        if not revomon:
            return {"error": f"Revomon with dex_id {dex_id} not found"}

        requirements = {
            "current_revomon": revomon.copy(),
            "can_evolve": False,
            "evolution_method": "unknown",
            "requirements": [],
        }

        evo_name = revomon.get("evo")
        if not evo_name:
            requirements["message"] = f"{revomon.get('name')} does not evolve"
            return requirements

        requirements["can_evolve"] = True

        # Find the evolved form
        evolved_form = self.revomon_client.get_revomon_by_name(evo_name)
        if evolved_form:
            requirements["evolved_form"] = evolved_form.copy()

            # Check evolution method
            evo_level = revomon.get("evo_lvl")
            if evo_level:
                requirements["evolution_method"] = "level"
                requirements["requirements"].append(
                    {
                        "type": "level",
                        "value": evo_level,
                        "description": f"Reach level {evo_level}",
                    }
                )
            else:
                # Check for other evolution methods
                requirements["evolution_method"] = "unknown"
                requirements["requirements"].append(
                    {
                        "type": "unknown",
                        "description": "Evolution method unknown - may require items, time, or other conditions",
                    }
                )

        return requirements

    def _calculate_branch_stats(
        self, revomon_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate statistics for a branch of evolution.

        Args:
            revomon_list: List of Revomon in the branch

        Returns:
            Branch statistics
        """
        if not revomon_list:
            return {}

        stats = {
            "count": len(revomon_list),
            "avg_stat_total": sum(r.get("stat_total", 0) for r in revomon_list)
            / len(revomon_list),
            "min_stat_total": min(r.get("stat_total", 0) for r in revomon_list),
            "max_stat_total": max(r.get("stat_total", 0) for r in revomon_list),
            "types": set(),
            "rarities": set(),
        }

        for revomon in revomon_list:
            if revomon.get("type1"):
                stats["types"].add(revomon.get("type1"))
            if revomon.get("type2"):
                stats["types"].add(revomon.get("type2"))
            if revomon.get("rarity"):
                stats["rarities"].add(revomon.get("rarity"))

        stats["types"] = list(stats["types"])
        stats["rarities"] = list(stats["rarities"])

        return stats

    def _calculate_tree_stats(
        self, all_members: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate overall statistics for an evolution tree.

        Args:
            all_members: All members of the evolution tree

        Returns:
            Tree statistics
        """
        if not all_members:
            return {}

        stat_totals = [r.get("stat_total", 0) for r in all_members]

        return {
            "total_members": len(all_members),
            "avg_stat_total": sum(stat_totals) / len(stat_totals),
            "min_stat_total": min(stat_totals),
            "max_stat_total": max(stat_totals),
            "stat_total_range": max(stat_totals) - min(stat_totals),
            "unique_types": len(
                set(
                    t
                    for r in all_members
                    for t in [r.get("type1"), r.get("type2")]
                    if t
                )
            ),
            "rarity_distribution": self._calculate_rarity_distribution(all_members),
        }

    def _calculate_rarity_distribution(
        self, revomon_list: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """
        Calculate rarity distribution in a list of Revomon.

        Args:
            revomon_list: List of Revomon

        Returns:
            Rarity distribution
        """
        distribution = {}
        for revomon in revomon_list:
            rarity = revomon.get("rarity", "unknown")
            distribution[rarity] = distribution.get(rarity, 0) + 1

        return distribution

    def find_evolution_gaps(self) -> List[Dict[str, Any]]:
        """
        Find gaps in evolution chains where intermediate forms might be missing.

        Returns:
            List of potential evolution gaps
        """
        gaps = []

        # Group Revomon by evolution tree
        evolution_trees = self._group_by_evolution_tree()

        for tree_name, members in evolution_trees.items():
            if len(members) < 2:
                continue

            # Sort by stat total
            sorted_members = sorted(members, key=lambda x: x.get("stat_total", 0))

            # Check for large stat gaps that might indicate missing evolutions
            for i in range(len(sorted_members) - 1):
                current = sorted_members[i]
                next_rev = sorted_members[i + 1]

                stat_gap = next_rev.get("stat_total", 0) - current.get("stat_total", 0)

                # If gap is larger than 100 stat points, it might indicate missing evolution
                if stat_gap > 100:
                    gaps.append(
                        {
                            "tree": tree_name,
                            "from": current.get("name"),
                            "to": next_rev.get("name"),
                            "stat_gap": stat_gap,
                            "gap_percentage": (stat_gap / current.get("stat_total", 1))
                            * 100,
                            "potential_missing_evolution": stat_gap > 150,
                        }
                    )

        return gaps

    def _group_by_evolution_tree(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group Revomon by their evolution tree.

        Returns:
            Dict of evolution trees
        """
        trees = {}

        for revomon in self.revomon_client.get_all():
            tree_name = revomon.get("evo_tree", "Unknown")
            if tree_name not in trees:
                trees[tree_name] = []
            trees[tree_name].append(revomon.copy())

        return trees

    def analyze_evolution_meta(self) -> Dict[str, Any]:
        """
        Analyze evolution patterns for competitive meta insights.

        Returns:
            Meta analysis of evolution system
        """
        # Get all evolution trees
        trees = self._group_by_evolution_tree()

        meta_analysis = {
            "total_evolution_trees": len(trees),
            "avg_chain_length": 0,
            "most_common_evolution_method": "level",
            "trees_by_length": {},
            "stat_progression_patterns": [],
            "type_evolution_patterns": [],
        }

        chain_lengths = []
        for tree_name, members in trees.items():
            chain_length = len(members)
            chain_lengths.append(chain_length)

            if chain_length not in meta_analysis["trees_by_length"]:
                meta_analysis["trees_by_length"][chain_length] = 0
            meta_analysis["trees_by_length"][chain_length] += 1

        if chain_lengths:
            meta_analysis["avg_chain_length"] = sum(chain_lengths) / len(chain_lengths)

        # Analyze stat progression patterns
        for tree_name, members in trees.items():
            if len(members) >= 2:
                sorted_members = sorted(members, key=lambda x: x.get("stat_total", 0))
                progression = []

                for i in range(len(sorted_members) - 1):
                    current = sorted_members[i]
                    next_rev = sorted_members[i + 1]
                    growth = next_rev.get("stat_total", 0) - current.get(
                        "stat_total", 0
                    )
                    progression.append(
                        {
                            "from": current.get("name"),
                            "to": next_rev.get("name"),
                            "growth": growth,
                            "growth_percentage": (growth / current.get("stat_total", 1))
                            * 100,
                        }
                    )

                meta_analysis["stat_progression_patterns"].append(
                    {"tree": tree_name, "progression": progression}
                )

        return meta_analysis
