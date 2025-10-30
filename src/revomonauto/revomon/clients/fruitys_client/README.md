# FruitysClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Berry and held item system client for Revomon, providing access to damage reduction mechanics, healing effects, priority manipulation, and type-triggered effects for defensive strategy optimization.

## 🍓 Overview

The FruitysClient provides the complete berry and held item system for Revomon:

- **Damage reduction** against super-effective attacks (type-resist berries)
- **Healing effects** and HP restoration mechanics
- **Priority manipulation** for speed control
- **Type-triggered effects** that activate against specific elemental types
- **Defensive strategy** optimization and counter-building
- **Held item** compatibility and team synergy

This client enables the defensive counterplay that balances Revomon's offensive systems and creates strategic depth in team building.

## 📊 Fruity Data Structure

Each fruity (berry/held item) contains comprehensive effect information:

### Core Information
- **`name`** - Unique fruity identifier (primary key)
- **`description`** - Detailed effects and activation conditions
- **`type`** - Item type (appears to be "held" for all entries)

### Effect Categories
- **Damage Reduction** - Resist super-effective attacks
- **Healing Effects** - HP recovery and restoration
- **Priority Manipulation** - Speed control and turn order
- **Type-Triggered** - Effects that activate against specific types

## 🚀 Quick Start

### Basic Fruity Lookup

```python
from revomonauto.revomon.clients import FruitysClient

# Initialize client
fruitys_client = FruitysClient()

# Get fruity by name
orcan_berry = fruitys_client.get_fruity("orcan berry")
if orcan_berry:
    print(f"Orcan Berry: {orcan_berry['description']}")

# Get damage-reducing berries
resist_berries = fruitys_client.get_damage_reducing_fruitys()
print(f"Damage-reducing berries: {len(resist_berries)}")
for berry in resist_berries:
    print(f"  {berry['name']}: {berry['description'][:50]}...")
```

### Healing and Support Analysis

```python
# Get healing berries
healing_fruitys = fruitys_client.get_healing_fruitys()
print(f"Healing berries: {len(healing_fruitys)}")

# Get priority manipulation items
priority_fruitys = fruitys_client.get_priority_fruitys()
print(f"Priority berries: {len(priority_fruitys)}")

# Get type-specific berries
fire_berries = fruitys_client.get_fruitys_by_type_effect("fire")
water_berries = fruitys_client.get_fruitys_by_type_effect("water")
print(f"Fire berries: {len(fire_berries)}, Water berries: {len(water_berries)}")
```

## 📚 API Reference

### Core Query Methods

#### `get_fruity(fruity_name)`

Get fruity data by name.

**Parameters:**
- `fruity_name` (str): The fruity name

**Returns:** Fruity data dictionary or None if not found

### Effect Category Methods

#### `get_damage_reducing_fruitys()`

Get berries that reduce super-effective damage.

**Returns:** List of damage-reducing berries

#### `get_healing_fruitys()`

Get berries with healing or restoration effects.

**Returns:** List of healing berries

#### `get_priority_fruitys()`

Get berries that affect move priority or speed.

**Returns:** List of priority-manipulating berries

#### `get_fruitys_by_type_effect(type_name)`

Get berries that activate against specific types.

**Parameters:**
- `type_name` (str): Type that triggers the berry (e.g., "fire", "water")

**Returns:** List of type-triggered berries

## 🎮 Usage Examples

### Example 1: Defensive Team Building

```python
from revomonauto.revomon.clients import FruitysClient

fruitys_client = FruitysClient()

# Build defensive berry strategy for team
def build_berry_strategy(team_types, strategy="resist"):
    """
    Build optimal berry strategy based on team composition
    """
    berry_strategy = {
        'damage_reduction': [],
        'healing': [],
        'priority': [],
        'type_specific': []
    }

    if strategy == "resist":
        # Focus on type resistance berries
        resist_berries = fruitys_client.get_damage_reducing_fruitys()

        # Match berries to team types
        for team_type in team_types:
            type_berries = fruitys_client.get_fruitys_by_type_effect(team_type)
            berry_strategy['type_specific'].extend(type_berries)

        berry_strategy['damage_reduction'] = resist_berries[:3]  # Top 3 resist berries

    elif strategy == "sustain":
        # Focus on healing berries
        healing_berries = fruitys_client.get_healing_fruitys()
        berry_strategy['healing'] = healing_berries[:4]  # Top 4 healing berries

    elif strategy == "speed":
        # Focus on priority berries
        priority_berries = fruitys_client.get_priority_fruitys()
        berry_strategy['priority'] = priority_berries

    return berry_strategy

# Build strategy for elemental team
team_types = ["fire", "water", "grass", "electric"]
resist_strategy = build_berry_strategy(team_types, "resist")

print("=== Berry Strategy ===")
print(f"Damage reduction: {[b['name'] for b in resist_strategy['damage_reduction']]}")
print(f"Type-specific: {[b['name'] for b in resist_strategy['type_specific']]}")
```

### Example 2: Type Weakness Mitigation

```python
# Mitigate team type weaknesses with berries
def mitigate_type_weaknesses(team_types, known_weaknesses):
    """
    Find berries that help against team weaknesses
    """
    mitigation_plan = []

    for weakness in known_weaknesses:
        # Find berries that resist this weakness type
        resist_berries = fruitys_client.get_fruitys_by_type_effect(weakness)

        if resist_berries:
            mitigation_plan.append({
                'weakness': weakness,
                'berries': resist_berries[:2],  # Top 2 options
                'mitigation_type': 'resistance'
            })
        else:
            # Look for general damage reduction
            general_resist = fruitys_client.get_damage_reducing_fruitys()
            mitigation_plan.append({
                'weakness': weakness,
                'berries': general_resist[:1],  # Fallback option
                'mitigation_type': 'general'
            })

    return mitigation_plan

# Mitigate common weaknesses
team_weaknesses = ["ground", "rock", "ice"]
mitigation = mitigate_type_weaknesses(team_types, team_weaknesses)

print("=== Weakness Mitigation ===")
for weakness in mitigation:
    print(f"{weakness['weakness']} weakness:")
    for berry in weakness['berries']:
        print(f"  {berry['name']}: {berry['description'][:60]}...")
```

### Example 3: Healing Strategy Optimization

```python
# Optimize healing berry usage for different battle lengths
def optimize_healing_strategy(battle_length="medium"):
    """
    Optimize healing berry selection based on battle duration
    """
    healing_berries = fruitys_client.get_healing_fruitys()

    if battle_length == "short":
        # Focus on immediate healing
        immediate_heal = [b for b in healing_berries
                         if "instant" in b['description'].lower() or "immediate" in b['description'].lower()]
        return immediate_heal or healing_berries[:2]

    elif battle_length == "long":
        # Focus on sustained healing
        sustained_heal = [b for b in healing_berries
                         if "recover" in b['description'].lower() or "restore" in b['description'].lower()]
        return sustained_heal or healing_berries[:3]

    else:  # medium
        # Balanced approach
        return healing_berries[:3]

# Optimize for tournament (long battles)
tournament_healing = optimize_healing_strategy("long")
print("=== Tournament Healing Strategy ===")
for berry in tournament_healing:
    print(f"{berry['name']}: {berry['description']}")
```

### Example 4: Competitive Berry Meta

```python
# Analyze berry usage in competitive meta
def analyze_berry_meta():
    """
    Analyze berry effectiveness and usage patterns
    """
    # Categorize all berries
    all_berries = fruitys_client.get_all()

    categories = {
        'damage_reduction': fruitys_client.get_damage_reducing_fruitys(),
        'healing': fruitys_client.get_healing_fruitys(),
        'priority': fruitys_client.get_priority_fruitys(),
        'type_specific': []
    }

    # Get type-specific berries
    common_types = ["fire", "water", "grass", "electric", "ground", "flying"]
    for berry_type in common_types:
        type_berries = fruitys_client.get_fruitys_by_type_effect(berry_type)
        categories['type_specific'].extend(type_berries)

    # Analyze category distribution
    category_sizes = {category: len(berries) for category, berries in categories.items()}

    print("=== Berry Meta Analysis ===")
    print(f"Total berries: {len(all_berries)}")

    print("\nCategory distribution:")
    for category, count in category_sizes.items():
        percentage = (count / len(all_berries)) * 100
        print(f"  {category.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")

    # Show popular berries
    print("\nTop damage reduction berries:")
    for berry in categories['damage_reduction'][:5]:
        print(f"  {berry['name']}: {berry['description'][:50]}...")

analyze_berry_meta()
```

## 🏆 Advanced Fruity Analysis

### Berry Synergy Optimization

```python
# Optimize berry combinations for team synergy
def optimize_berry_synergy(team_types, team_strategy="balanced"):
    """
    Find optimal berry combinations that work well together
    """
    synergy_combinations = []

    # Get berries by category
    resist_berries = fruitys_client.get_damage_reducing_fruitys()
    healing_berries = fruitys_client.get_healing_fruitys()
    priority_berries = fruitys_client.get_priority_fruitys()

    # Create synergistic combinations
    if team_strategy == "defensive":
        # Focus on damage reduction + healing
        for resist_berry in resist_berries[:3]:
            for healing_berry in healing_berries[:2]:
                synergy_combinations.append({
                    'berries': [resist_berry['name'], healing_berry['name']],
                    'synergy_type': 'defensive_sustain',
                    'description': 'Damage reduction + healing for tanky teams'
                })

    elif team_strategy == "offensive":
        # Focus on priority + type advantage
        for priority_berry in priority_berries:
            for team_type in team_types:
                type_berries = fruitys_client.get_fruitys_by_type_effect(team_type)
                if type_berries:
                    synergy_combinations.append({
                        'berries': [priority_berry['name'], type_berries[0]['name']],
                        'synergy_type': 'offensive_control',
                        'description': 'Speed control + type advantage'
                    })

    return synergy_combinations

# Optimize for defensive team
defensive_synergies = optimize_berry_synergy(["steel", "rock"], "defensive")

print("=== Berry Synergies ===")
for synergy in defensive_synergies[:5]:
    print(f"{synergy['synergy_type']}: {synergy['berries']}")
    print(f"  {synergy['description']}")
```

### Weakness Coverage Analysis

```python
# Analyze how well berries cover type weaknesses
def analyze_weakness_coverage(team_types, available_berries=None):
    """
    Analyze berry coverage for team type weaknesses
    """
    if not available_berries:
        available_berries = fruitys_client.get_all()

    coverage_analysis = {
        'covered_weaknesses': set(),
        'uncovered_weaknesses': set(),
        'coverage_quality': {}
    }

    # Get common attacking types that threaten the team
    common_threats = ["fire", "water", "grass", "electric", "ground", "flying", "ice", "rock"]

    for threat in common_threats:
        # Check if any berry helps against this threat
        threat_berries = [b for b in available_berries
                         if threat.lower() in b['description'].lower()]

        if threat_berries:
            coverage_analysis['covered_weaknesses'].add(threat)
            coverage_analysis['coverage_quality'][threat] = len(threat_berries)
        else:
            coverage_analysis['uncovered_weaknesses'].add(threat)

    coverage_percentage = (len(coverage_analysis['covered_weaknesses']) / len(common_threats)) * 100

    return coverage_analysis, coverage_percentage

# Analyze coverage for typical team
coverage, percentage = analyze_weakness_coverage(["fire", "water", "grass"])

print("=== Weakness Coverage ===")
print(f"Covered weaknesses: {len(coverage['covered_weaknesses'])}/{len(['fire', 'water', 'grass', 'electric', 'ground', 'flying', 'ice', 'rock'])}")
print(f"Coverage percentage: {percentage:.1f}%")
print(f"Covered: {sorted(coverage['covered_weaknesses'])}")
print(f"Uncovered: {sorted(coverage['uncovered_weaknesses'])}")
```

## 📈 Performance

- **Fast queries**: Indexed berry names and effect lookups
- **Cached data**: Fruity database loaded once and cached
- **Efficient categorization**: Optimized keyword matching for effects
- **Memory efficient**: Minimal memory footprint for analysis

## 🧪 Testing

```bash
# Run fruitys client tests
uv run python -m pytest tests/clients/test_fruitys_client.py

# Test berry strategies
uv run python tests/integration/test_berry_strategies.py

# Performance benchmarks
uv run python tests/performance/test_fruity_queries.py
```

## 🤝 Contributing

1. Ensure all berry effects are accurate to game mechanics
2. Add comprehensive tests for new berry interactions
3. Update berry effects when balance changes occur
4. Document any new berry types or mechanics

## 🔄 Version History

### v2.0.0
- Complete berry system with damage reduction mechanics
- Advanced categorization by effect types
- Defensive strategy optimization and synergy analysis
- Type weakness mitigation and coverage analysis
- Competitive berry meta analysis tools

### v1.0.0
- Basic berry lookup by name
- Simple effect categorization
- Basic healing and damage reduction queries

---

**Ready to master defensive strategies and turn weaknesses into strengths? Let the berry analysis begin!** 🍓🛡️💊
