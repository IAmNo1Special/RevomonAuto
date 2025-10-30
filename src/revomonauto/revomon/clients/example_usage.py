"""
Example usage of Revomon data clients

This file demonstrates how to use the various client classes to access Revomon data.
"""

from revomonauto.revomon.clients import (
    TypesClient,
    AbilitiesClient,
    RevomonClient,
    MovesClient,
    ItemsClient,
    NaturesClient,
    CounterdexClient,
    FruitysClient,
    CapsulesClient,
    OwnedLandsClient,
    RevomonMovesClient,
    LocationsClient,
    BattleMechanicsClient,
    EvolutionClient,
    WeatherClient,
    StatusEffectsClient
)


def example_usage():
    """Example of how to use the clients."""

    # Initialize clients
    types_client = TypesClient()
    abilities_client = AbilitiesClient()
    revomon_client = RevomonClient()
    moves_client = MovesClient()
    items_client = ItemsClient()
    natures_client = NaturesClient()
    counterdex_client = CounterdexClient()
    fruitys_client = FruitysClient()
    capsules_client = CapsulesClient()
    lands_client = OwnedLandsClient()
    revomon_moves_client = RevomonMovesClient()
    locations_client = LocationsClient()
    battle_client = BattleMechanicsClient()
    evolution_client = EvolutionClient()
    weather_client = WeatherClient()
    status_client = StatusEffectsClient()

    # Example: Get type effectiveness
    print("=== TYPE EFFECTIVENESS EXAMPLE ===")
    types_client.load_data()
    fire_weaknesses = types_client.get_types_weak_to("fire")
    print(f"Types weak to fire: {fire_weaknesses}")

    # Example: Get Revomon by type
    print("\n=== REVOMON BY TYPE EXAMPLE ===")
    revomon_client.load_data()
    fire_types = revomon_client.get_revomon_by_type("fire")
    print(f"Fire-type Revomon: {[r['name'] for r in fire_types[:5]]}")

    # Example: Get moves by category
    print("\n=== MOVES EXAMPLE ===")
    moves_client.load_data()
    status_moves = moves_client.get_status_moves()
    print(f"Status moves: {[m['name'] for m in status_moves[:5]]}")

    # Example: Get high-tier competitive Revomon
    print("\n=== COMPETITIVE EXAMPLE ===")
    counterdex_client.load_data()
    top_tier = counterdex_client.get_top_tier_revomon("b")
    print(f"Top tier Revomon: {[r['name'] for r in top_tier[:5]]}")

    # Example: Get items by cost range
    print("\n=== ITEMS EXAMPLE ===")
    items_client.load_data()
    cheap_items = items_client.get_items_by_cost_range(100, 500)
    print(f"Items costing 100-500: {[i['name'] for i in cheap_items[:5]]}")

    # Example: Spawn locations (using LocationsClient)
    print("\n=== SPAWN LOCATIONS EXAMPLE ===")
    locations_client.load_data()
    all_locations = locations_client.get_all_spawn_locations()
    print(f"All spawn locations: {all_locations[:5]}...")  # Show first 5

    # Get Revomon in a specific location (using LocationsClient)
    town_revomon = locations_client.get_revomon_by_location("drassius town")
    print(f"Revomon in Drassius Town: {[r['name'] for r in town_revomon[:5]]}")

    # Get location statistics
    stats = locations_client.get_location_statistics()
    print(f"Total locations: {stats['total_locations']}")
    print(f"Average Revomon per location: {stats['avg_revomon_per_location']:.1f}")

    # Show spawn times for a location
    if all_locations:
        spawn_times = locations_client.get_location_spawn_times(all_locations[0])
        print(f"Spawn times in {all_locations[0]}: {list(spawn_times.keys())}")

    # Example: Battle Mechanics - Damage Calculation
    print("\n=== BATTLE MECHANICS EXAMPLE ===")
    # Get sample Revomon and move for battle simulation
    gorcano = revomon_client.get_revomon_by_name("gorcano")
    blizzora = revomon_client.get_revomon_by_name("blizzora")
    earthquake = moves_client.get_move_by_name("earthquake")

    if gorcano and blizzora and earthquake:
        damage_result = battle_client.simulate_battle_turn(
            attacker=gorcano,
            defender=blizzora,
            move_name="earthquake",
            attacker_level=50,
            defender_level=50
        )
        print(f"Earthquake damage: {damage_result.get('damage', 'N/A')}")
        print(f"Type effectiveness: {damage_result.get('stab', False)} STAB, {damage_result.get('critical_hit', False)} Crit")

    # Example: Evolution Analysis
    print("\n=== EVOLUTION ANALYSIS EXAMPLE ===")
    evolution_tree = evolution_client.get_complete_evolution_tree(1)  # Dekute evolution
    if "error" not in evolution_tree:
        print(f"Evolution tree for Dekute: {len(evolution_tree['all_members'])} members")
        print(f"Stat progression: {evolution_tree['tree_stats']['stat_total_range']} total stat range")

    # Example: Weather Strategy
    print("\n=== WEATHER STRATEGY EXAMPLE ===")
    sample_team = [gorcano, blizzora] if gorcano and blizzora else []
    if sample_team:
        weather_strategy = weather_client.analyze_weather_strategy(sample_team)
        best_weather = weather_strategy["best_weather"]
        print(f"Best weather for team: {best_weather}")
        print(f"Weather score: {weather_strategy['best_score']}")

    # Example: Status Effects Analysis
    print("\n=== STATUS EFFECTS EXAMPLE ===")
    if sample_team:
        status_strategy = status_client.analyze_status_strategy(sample_team)
        vulnerabilities = status_strategy["status_vulnerabilities"]
        most_vulnerable = max(vulnerabilities.items(), key=lambda x: x[1])
        print(f"Most vulnerable to: {most_vulnerable[0]} (score: {most_vulnerable[1]})")
        print(f"Strategy recommendation: {status_strategy['recommended_status_strategy']}")

    # Example: Type Coverage Analysis
    print("\n=== TYPE COVERAGE EXAMPLE ===")
    if sample_team:
        coverage = battle_client.analyze_type_coverage(sample_team)
        print(f"Team type coverage: {coverage['overall_coverage']:.1%}")
        print(f"Covered types: {coverage['covered_types']}/{coverage['total_types']}")

        weaknesses = coverage.get("weaknesses", {})
        if weaknesses:
            most_common_weakness = max(weaknesses.items(), key=lambda x: len(x[1]))
            print(f"Most common weakness: {most_common_weakness[0]} ({len(most_common_weakness[1])} Revomon)")

    # Example: Evolution Path Optimization
    print("\n=== EVOLUTION OPTIMIZATION EXAMPLE ===")
    # Find evolution paths that lead to high special attack
    target_stats = {"spa": 1.0, "spe": 0.7}  # Prioritize special attack and speed
    optimal_paths = evolution_client.find_optimal_evolution_path(
        target_stats=target_stats,
        max_evolutions=3
    )

    if optimal_paths:
        best_path = optimal_paths[0]
        print(f"Best evolution path score: {best_path['score']:.1f}")
        print(f"Path: {' -> '.join([r['name'] for r in best_path['chain']])}")

    print("\n=== ALL CLIENTS READY FOR USE ===")
    print(f"Types: {types_client.count()} records")
    print(f"Abilities: {abilities_client.count()} records")
    print(f"Revomon: {revomon_client.count()} records")
    print(f"Moves: {moves_client.count()} records")
    print(f"Items: {items_client.count()} records")
    print(f"Natures: {natures_client.count()} records")
    print(f"Counterdex: {counterdex_client.count()} records")
    print(f"Fruitys: {fruitys_client.count()} records")
    print(f"Capsules: {capsules_client.count()} records")
    print(f"Lands: {lands_client.count()} records")
    print(f"Revomon Moves: {revomon_moves_client.count()} records")
    print(f"Locations: {locations_client.count()} records")
    print(f"Battle Mechanics: Advanced damage calculation ready")
    print(f"Evolution Analysis: Evolution chains and optimization ready")
    print(f"Weather Strategy: Weather mechanics and team analysis ready")
    print(f"Status Effects: Status conditions and strategy analysis ready")


if __name__ == "__main__":
    example_usage()
