# BattleMechanicsClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Advanced battle mechanics simulation and damage calculation system for Revomon, implementing Pokemon-style battle formulas with comprehensive type effectiveness, critical hits, and battle analysis.

## 🎯 Overview

The BattleMechanicsClient provides a complete battle simulation system including:

- **Damage calculation** using Pokemon-style formulas
- **Type effectiveness** (0.0 to 4.0 multipliers)
- **STAB bonuses** (1.5× damage for matching types)
- **Critical hits** with configurable rates
- **Battle turn simulation** with detailed results
- **Team coverage analysis** for optimal type combinations
- **Move effectiveness** analysis and recommendations

## 📊 Features

### Core Battle Mechanics
- **Pokemon Formula**: `Damage = (((2 × Level ÷ 5 + 2) × Attack × Power ÷ Defense) ÷ 50 + 2) × Modifier`
- **Type Effectiveness**: 0.0 (immune) → 0.5 (resistant) → 1.0 (neutral) → 2.0 (weak) → 4.0 (very weak)
- **STAB System**: 1.5× damage when move type matches Revomon type(s)
- **Critical Hits**: 2.0× multiplier with 6.25% base critical rate

### Advanced Analysis
- **Team Coverage**: Identify type weaknesses and optimal team compositions
- **Move Analysis**: Effectiveness ratings and strategic recommendations
- **Counter Strategies**: Find optimal counters for specific Revomon
- **Battle Simulation**: Turn-by-turn combat analysis with detailed breakdowns

## 🚀 Quick Start

### Basic Damage Calculation

```python
from revomonauto.revomon.clients import BattleMechanicsClient, RevomonClient, MovesClient

# Initialize clients
battle_client = BattleMechanicsClient()
revomon_client = RevomonClient()
moves_client = MovesClient()

# Get data
attacker = revomon_client.get_revomon_by_name("gorcano")
defender = revomon_client.get_revomon_by_name("blizzora")
move = moves_client.get_move_by_name("earthquake")

# Calculate damage
result = battle_client.simulate_battle_turn(
    attacker=attacker,
    defender=defender,
    move_name="earthquake",
    attacker_level=50,
    defender_level=50
)

print(f"Damage: {result['damage']}")
print(f"Effectiveness: {result['effectiveness']}")
print(f"Critical hit: {result['critical_hit']}")
```

### Type Coverage Analysis

```python
# Analyze team type coverage
team = [
    revomon_client.get_revomon_by_name("gorcano"),      # Ground/Fire
    revomon_client.get_revomon_by_name("blizzora"),     # Ice/Water
    revomon_client.get_revomon_by_name("electra"),      # Electric
]

coverage = battle_client.analyze_team_coverage(team)
print(f"Weaknesses covered: {len(coverage['types_covered'])}/18")
print(f"Remaining weaknesses: {coverage['uncovered_types']}")
```

### Battle Simulation

```python
# Simulate a full battle turn
battle_result = battle_client.simulate_battle_turn(
    attacker=attacker,
    defender=defender,
    move_name="earthquake",
    attacker_level=50,
    defender_level=50,
    weather="sandstorm",
    attacker_status="burn",
    defender_status="paralysis"
)

print(f"Final damage: {battle_result['damage']}")
print(f"Damage breakdown: {battle_result['damage_breakdown']}")
```

## 📚 API Reference

### Core Methods

#### `simulate_battle_turn(attacker, defender, move_name, attacker_level=50, defender_level=50, **kwargs)`

Simulate a complete battle turn with damage calculation.

**Parameters:**
- `attacker` (dict): Attacking Revomon data
- `defender` (dict): Defending Revomon data
- `move_name` (str): Name of the move to use
- `attacker_level` (int): Attacker level (default: 50)
- `defender_level` (int): Defender level (default: 50)
- `weather` (str): Current weather condition
- `attacker_status` (str): Attacker status condition
- `defender_status` (str): Defender status condition

**Returns:** Dict with damage, effectiveness, critical hit, and breakdown

#### `calculate_damage(attacker, defender, move, attacker_level=50, defender_level=50)`

Calculate damage between two Revomon using a specific move.

#### `get_type_effectiveness(attacker_types, defender_types, move_type)`

Calculate type effectiveness multiplier.

#### `analyze_team_coverage(team, include_legendary=False)`

Analyze type coverage for a team of Revomon.

**Returns:** Coverage analysis with types covered and weaknesses remaining

### Utility Methods

#### `get_move_effectiveness(move_name, defender_types)`

Get effectiveness rating for a move against specific types.

#### `find_optimal_counters(target_revomon, available_revomon, max_results=5)`

Find optimal counter Revomon for a target.

#### `analyze_move_effectiveness(moves, defender_team)`

Analyze move effectiveness against a team.

## 🎮 Usage Examples

### Example 1: Basic Damage Calculation

```python
from revomonauto.revomon.clients import BattleMechanicsClient

battle_client = BattleMechanicsClient()

# Simple damage calculation
damage = battle_client.calculate_damage(
    attacker={"name": "gorcano", "type1": "ground", "type2": "fire", "atk": 120},
    defender={"name": "blizzora", "type1": "ice", "type2": "water", "def": 80},
    move={"name": "earthquake", "type": "ground", "category": "physical", "power": 100, "accuracy": 1.0},
    attacker_level=50,
    defender_level=50
)

print(f"Earthquake deals {damage['damage']} damage!")
```

### Example 2: Team Building Analysis

```python
# Analyze optimal team composition
team = [
    {"name": "gorcano", "type1": "ground", "type2": "fire"},
    {"name": "blizzora", "type1": "ice", "type2": "water"},
    {"name": "electra", "type1": "electric"},
    {"name": "draco", "type1": "dragon"},
    {"name": "psyche", "type1": "psychic"},
    {"name": "umbra", "type1": "dark", "type2": "ghost"}
]

analysis = battle_client.analyze_team_coverage(team)
print(f"Team covers {len(analysis['types_covered'])} types")
print(f"Remaining weaknesses: {analysis['uncovered_types']}")
```

### Example 3: Counter Strategy

```python
# Find best counters for a specific Revomon
target = revomon_client.get_revomon_by_name("legendary_revomon")
counters = battle_client.find_optimal_counters(
    target_revomon=target,
    available_revomon=all_revomon_list,
    max_results=10
)

for counter in counters:
    print(f"{counter['revomon']['name']}: {counter['score']} effectiveness")
```

## 🔧 Advanced Configuration

### Custom Damage Modifiers

```python
# Custom modifiers for specific scenarios
custom_modifiers = {
    "weather": 1.5,        # Rain boost for Water moves
    "terrain": 1.3,        # Electric Terrain boost
    "status": 0.5,         # Paralysis halves speed
    "item": 1.2,           # Choice Band boost
    "ability": 1.5         # Sheer Force removes secondary effects
}

result = battle_client.simulate_battle_turn(
    attacker=attacker,
    defender=defender,
    move_name="thunder",
    custom_modifiers=custom_modifiers
)
```

### Battle Conditions

```python
# Simulate various battle conditions
conditions = {
    "weather": "rain",
    "terrain": "electric_terrain",
    "room": "trick_room",
    "gravity": True,
    "tailwind": True
}

result = battle_client.simulate_battle_turn(
    attacker=attacker,
    defender=defender,
    move_name="earthquake",
    battle_conditions=conditions
)
```

## 📈 Performance

- **Fast calculations**: Optimized damage formulas for real-time battle simulation
- **Cached data**: Move and Revomon data cached for quick access
- **Batch processing**: Support for analyzing multiple matchups efficiently
- **Memory efficient**: Minimal memory footprint for large-scale analysis

## 🧪 Testing

```bash
# Run battle mechanics tests
uv run python -m pytest tests/clients/test_battle_mechanics_client.py

# Performance tests
uv run python tests/performance/test_damage_calculation.py

# Integration tests with real data
uv run python tests/integration/test_battle_simulation.py
```

## 🤝 Contributing

1. Ensure damage calculations are mathematically accurate
2. Add comprehensive tests for new features
3. Update type effectiveness when new types are added
4. Document any formula changes with sources

## 🔄 Version History

### v2.0.0
- Complete Pokemon-style damage formula implementation
- Advanced team coverage analysis
- Counter strategy recommendations
- Battle condition simulation (weather, terrain, etc.)

### v1.0.0
- Basic damage calculation
- Simple type effectiveness
- Individual battle turn simulation

---

**Ready to simulate epic Revomon battles? Let the calculations begin!** ⚔️🧮💥
