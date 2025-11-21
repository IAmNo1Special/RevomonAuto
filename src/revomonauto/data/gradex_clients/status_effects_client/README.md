# StatusEffectsClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive status condition analysis and management system for Revomon, providing status effects, immunities, curing mechanics, and competitive status strategy optimization.

## 🏥 Overview

The StatusEffectsClient provides complete status condition analysis including:

- **8 Core Status Conditions**: Poison, Toxic, Paralysis, Sleep, Freeze, Burn, Confusion, Flinch
- **Status immunities** through abilities, types, and items
- **Status curing** methods via moves, abilities, and items
- **Status strategy optimization** for team building and competitive play
- **Status vulnerability analysis** and counter strategies
- **Team status management** and status-based recommendations

## ⚕️ Features

### Status Conditions
- **8 Status Types**: Complete coverage of all major status effects
- **Status Effects**: Detailed mechanics for each status condition
- **Status Interactions**: How status conditions interact with each other
- **Status Prevention**: Methods to prevent status application

### Immunity & Prevention
- **Type Immunities**: Types that prevent certain status conditions
- **Ability Immunities**: Abilities that grant status immunity
- **Item Prevention**: Items that prevent or reduce status effects
- **Status Blocking**: Active prevention of status application

### Curing & Management
- **Cure Methods**: Moves, abilities, and items that cure status
- **Auto-Cure**: Automatic status recovery mechanics
- **Status Duration**: How long status conditions last
- **Management Strategies**: Optimal status management approaches

### Strategy Analysis
- **Team Vulnerabilities**: Analyze team weaknesses to status conditions
- **Status Strategies**: Optimal status condition usage strategies
- **Counter Strategies**: Methods to counter status-heavy teams
- **Meta Analysis**: Status usage patterns in competitive play

## 🚀 Quick Start

### Basic Status Analysis

```python
from revomonauto.revomon.clients import StatusEffectsClient

# Initialize client
status_client = StatusEffectsClient()

# Get all status conditions
status_conditions = status_client.get_status_conditions()
print(f"Available status conditions: {status_conditions}")

# Analyze specific status effect
poison_effects = status_client.get_status_effects("poison")
print(f"Poison effects: {poison_effects}")
```

### Status Vulnerability Analysis

```python
# Analyze team vulnerabilities to status conditions
team = [
    {"name": "gorcano", "type1": "ground", "type2": "fire"},
    {"name": "blizzora", "type1": "ice", "type2": "water"},
    {"name": "electra", "type1": "electric"}
]

vulnerability = status_client.analyze_status_vulnerabilities(team)
print(f"Team status vulnerabilities: {vulnerability['vulnerable_to']}")
print(f"Status immunities: {vulnerability['immune_to']}")
```

### Status Strategy Optimization

```python
# Optimize team for status strategy
strategy = status_client.analyze_status_strategy(team)
print(f"Optimal status strategy: {strategy['recommended_strategy']}")
print(f"Status synergy: {strategy['synergy_score']}")
```

## 📚 API Reference

### Core Methods

#### `get_status_conditions()`

Get all available status conditions in the game.

**Returns:** List of status condition names

#### `get_status_effects(status_name)`

Get detailed effects of a specific status condition.

**Parameters:**
- `status_name` (str): Name of the status condition

**Returns:** Dict with status effects, mechanics, and interactions

#### `analyze_status_vulnerabilities(team)`

Analyze team vulnerabilities and immunities to status conditions.

**Parameters:**
- `team` (list): List of Revomon in the team

**Returns:** Status vulnerability analysis with weaknesses and immunities

#### `analyze_status_strategy(team, strategy_type="offensive")`

Analyze team composition for status strategy optimization.

**Parameters:**
- `team` (list): List of Revomon in the team
- `strategy_type` (str): Strategy type ("offensive", "defensive", "balanced")

**Returns:** Status strategy analysis with recommendations

#### `find_status_immunities(revomon)`

Find status immunities for a specific Revomon.

**Parameters:**
- `revomon` (dict): Revomon data

**Returns:** List of status conditions the Revomon is immune to

#### `get_status_cures(status_name)`

Get methods to cure a specific status condition.

**Parameters:**
- `status_name` (str): Status condition to cure

**Returns:** List of cure methods (moves, abilities, items)

### Analysis Methods

#### `calculate_status_synergy(team, target_status)`

Calculate how well a team can apply or resist specific status conditions.

**Parameters:**
- `team` (list): Team composition
- `target_status` (list): Target status conditions

**Returns:** Synergy score and breakdown

#### `analyze_status_meta()`

Analyze status condition usage patterns and meta strategies.

**Returns:** Meta analysis of status usage and effectiveness

#### `get_status_dependent_moves(status)`

Get moves that are affected by specific status conditions.

**Parameters:**
- `status` (str): Status condition

**Returns:** List of moves and their status interactions

## 🩹 Status Conditions & Effects

### Poison
- **Effect**: Deals damage each turn (1/16 of max HP)
- **Prevention**: Steel/Poison types immune, certain abilities
- **Cure**: Antidote, Full Heal, certain moves/abilities
- **Strategy**: Wear down tanks and defensive Revomon

### Toxic (Bad Poison)
- **Effect**: Increasing damage each turn (1/16, 2/16, 3/16, etc.)
- **Prevention**: Steel/Poison types immune, certain abilities
- **Cure**: Full Heal, certain moves/abilities
- **Strategy**: Counter high-HP Revomon and walls

### Paralysis
- **Effect**: 50% chance to be unable to move, Speed reduced
- **Prevention**: Electric types immune, certain abilities
- **Cure**: Paralyze Heal, Full Heal, certain moves/abilities
- **Strategy**: Control fast sweepers and setup Revomon

### Sleep
- **Effect**: Unable to move for 1-7 turns
- **Prevention**: No type immunity, certain abilities prevent
- **Cure**: Full Heal, Chesto Berry, certain moves/abilities
- **Strategy**: Stop dangerous Revomon temporarily

### Freeze
- **Effect**: Unable to move until thawed (20% chance per turn)
- **Prevention**: Ice types immune, certain abilities
- **Cure**: Full Heal, certain moves/abilities
- **Strategy**: Control threats in cold weather

### Burn
- **Effect**: 50% physical attack reduction, 1/16 HP damage per turn
- **Prevention**: Fire types immune, certain abilities
- **Cure**: Burn Heal, Full Heal, certain moves/abilities
- **Strategy**: Reduce physical attacker effectiveness

### Confusion
- **Effect**: 50% chance to hurt self instead of executing move
- **Prevention**: No type immunity, certain abilities prevent
- **Cure**: Persim Berry, certain moves/abilities
- **Strategy**: Disrupt strategy and setup moves

### Flinch
- **Effect**: 100% chance to prevent move execution (single turn)
- **Prevention**: Inner Focus and similar abilities
- **Cure**: Not needed (single turn effect)
- **Strategy**: Interrupt charged moves and setup

## 🎯 Usage Examples

### Example 1: Team Status Analysis

```python
from revomonauto.revomon.clients import StatusEffectsClient

status_client = StatusEffectsClient()

# Analyze team status vulnerabilities
team = [
    {"name": "gorcano", "type1": "ground", "type2": "fire"},
    {"name": "blizzora", "type1": "ice", "type2": "water"},
    {"name": "electra", "type1": "electric"},
    {"name": "psyche", "type1": "psychic"},
    {"name": "umbra", "type1": "dark", "type2": "ghost"},
    {"name": "draco", "type1": "dragon"}
]

analysis = status_client.analyze_status_vulnerabilities(team)

print("=== Team Status Analysis ===")
print(f"Vulnerable to: {analysis['vulnerable_to']}")
print(f"Immune to: {analysis['immune_to']}")
print(f"High risk status: {analysis['high_risk']}")
print(f"Recommended cures: {analysis['recommended_cures']}")
```

### Example 2: Status Strategy Development

```python
# Develop status strategy for team
offensive_strategy = status_client.analyze_status_strategy(
    team,
    strategy_type="offensive"
)

print("=== Offensive Status Strategy ===")
print(f"Strategy: {offensive_strategy['recommended_strategy']}")
print(f"Priority targets: {offensive_strategy['priority_targets']}")
print(f"Status moves: {offensive_strategy['recommended_moves']}")
print(f"Success rate: {offensive_strategy['success_rate']}%")
```

### Example 3: Status Immunity Planning

```python
# Find status immunities for team building
for revomon in team:
    immunities = status_client.find_status_immunities(revomon)
    print(f"{revomon['name']} immunities: {immunities}")

# Get cures for team
all_cures = status_client.get_all_status_cures()
print(f"\nAvailable cures: {all_cures}")
```

### Example 4: Status Meta Analysis

```python
# Analyze status usage in competitive meta
meta = status_client.analyze_status_meta()

print("=== Status Meta Analysis ===")
print(f"Most common status: {meta['most_common_status']}")
print(f"Status usage rate: {meta['usage_rate']}%")

print("\nStatus Effectiveness:")
for status, effectiveness in meta['status_effectiveness'].items():
    print(f"  {status}: {effectiveness['usage_rate']}% usage, {effectiveness['success_rate']}% success")

print("\nPopular Status Strategies:")
for strategy, usage in meta['popular_strategies'].items():
    print(f"  {strategy}: {usage}% usage")
```

## 🛡️ Advanced Status Management

### Status Prevention Planning

```python
# Plan status prevention for team
def plan_status_prevention(team):
    prevention_methods = {
        'abilities': [],
        'items': [],
        'moves': [],
        'team_composition': []
    }

    for revomon in team:
        # Check abilities that prevent status
        abilities = status_client.get_preventive_abilities(revomon)
        prevention_methods['abilities'].extend(abilities)

        # Check items that help with status
        items = status_client.get_preventive_items(revomon)
        prevention_methods['items'].extend(items)

    return prevention_methods

# Get prevention plan
prevention_plan = plan_status_prevention(team)
```

### Status Counter Strategy

```python
# Develop counter strategy for status teams
def counter_status_team(status_team):
    counters = []

    for revomon in status_team:
        # Find Revomon that resist status from this one
        resistant_revomon = status_client.find_status_resistant_revomon(revomon)
        counters.extend(resistant_revomon)

        # Find moves that prevent status
        preventive_moves = status_client.get_preventive_moves(revomon)
        counters.append(preventive_moves)

    return counters

# Get status counters
status_counters = counter_status_team(status_team)
```

## 📊 Performance

- **Fast analysis**: Optimized status calculations and vulnerability analysis
- **Cached effects**: Status effects and immunities cached for quick access
- **Batch processing**: Support for analyzing multiple teams and status conditions
- **Memory efficient**: Minimal memory footprint for large team analysis

## 🧪 Testing

```bash
# Run status effect tests
uv run python -m pytest tests/clients/test_status_effects_client.py

# Test status strategies
uv run python tests/integration/test_status_strategies.py

# Status meta analysis tests
uv run python tests/performance/test_status_analysis.py
```

## 🤝 Contributing

1. Ensure status effects are accurate to game mechanics
2. Add tests for new status conditions or interactions
3. Update immunity tables when new abilities/types are added
4. Document status interactions with sources

## 🔄 Version History

### v2.0.0
- Complete status condition management system
- 8 core status conditions with full mechanics
- Status immunity and prevention analysis
- Status curing and management strategies
- Team status vulnerability analysis and optimization
- Comprehensive status meta analysis

### v1.0.0
- Basic status condition lookup
- Simple status effects
- Individual status immunity checking

---

**Ready to master status conditions and control the battlefield? Let the status analysis begin!** 🏥🛡️💊
