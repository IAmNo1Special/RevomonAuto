# TypesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Complete type effectiveness system for Revomon battles, implementing the rock-paper-scissors combat mechanics with 18+ elemental types, dual-type combinations, and comprehensive matchup analysis.

## 🎯 Overview

The TypesClient provides the complete type effectiveness system that powers Revomon battles:

- **18+ Elemental types** with full interaction matrix
- **Dual-type combinations** for complex defensive strategies
- **Effectiveness multipliers**: 0.0 (immune) → 0.5 (resistant) → 1.0 (neutral) → 2.0 (super effective) → 4.0 (very effective)
- **Offensive coverage analysis** for optimal team building
- **Defensive weakness identification** for strategic counterplay
- **Type synergy optimization** for competitive team composition

This client is the foundation of all battle mechanics and strategic analysis in Revomon.

## 📊 Type System Structure

### Core Type Data
- **`types_str`** - Unique type combination identifier (e.g., "fire", "water/electric")
- **`type1`** - Primary elemental type
- **`type2`** - Secondary elemental type (null for single types)
- **Effectiveness matrix** - Multipliers for all attacking types (18+ columns)

### Effectiveness Scale
- **0.0** - Immune (no damage)
- **0.5** - Resistant (half damage)
- **1.0** - Neutral (normal damage)
- **2.0** - Weak (double damage)
- **4.0** - Very weak (quadruple damage)

## 🚀 Quick Start

### Basic Type Effectiveness

```python
from revomonauto.revomon.clients import TypesClient

# Initialize client
types_client = TypesClient()

# Get type effectiveness data
fire_type = types_client.get_type_effectiveness("fire")
print(f"Fire type data: {fire_type}")

# Get all available types
all_types = types_client.get_all_types()
print(f"Total type combinations: {len(all_types)}")

# Single vs dual types
single_types = types_client.get_single_types()
dual_types = types_client.get_dual_types()
print(f"Single types: {len(single_types)}, Dual types: {len(dual_types)}")
```

### Battle Effectiveness Analysis

```python
# Calculate damage multipliers
water_vs_fire = types_client.get_effectiveness_against("water", "fire")
grass_vs_water = types_client.get_effectiveness_against("grass", "water/ground")

print(f"Water vs Fire: {water_vs_fire}x damage")
print(f"Grass vs Water/Ground: {grass_vs_water}x damage")

# Find super effective types
water_weaknesses = types_client.get_super_effective_types("water")
print(f"Water is weak to: {water_weaknesses}")

# Find resistances and immunities
electric_resistances = types_client.get_types_weak_to("electric")
electric_immunities = types_client.get_immune_types("electric")
print(f"Electric resists: {electric_resistances}")
print(f"Electric immunities: {electric_immunities}")
```

## 📚 API Reference

### Core Query Methods

#### `get_type_effectiveness(types_str)`

Get complete effectiveness data for a type combination.

**Parameters:**
- `types_str` (str): Type combination ("fire", "water/electric", etc.)

**Returns:** Type effectiveness record with multipliers for all types

#### `get_all_types()`

Get all available type combinations.

**Returns:** List of all type combination strings

#### `get_single_types()`, `get_dual_types()`

Get single-type or dual-type combinations.

**Returns:** Lists of type records

#### `get_types_by_element(element_type)`

Get all types containing a specific element.

**Parameters:**
- `element_type` (str): Element to search for

**Returns:** List of types containing the element

### Effectiveness Analysis

#### `get_effectiveness_against(attacker_type, defender_type)`

Calculate effectiveness of one type against another.

**Parameters:**
- `attacker_type` (str): Attacking type combination
- `defender_type` (str): Defending type combination

**Returns:** Effectiveness multiplier (0.0 to 4.0)

#### `get_super_effective_types(defender_type)`

Get all types super effective (2.0x+) against a defender.

**Parameters:**
- `defender_type` (str): Defending type combination

**Returns:** List of super effective attacking types

#### `get_types_weak_to(defender_type)`

Get types that a defender is weak to (0.5x effectiveness).

**Parameters:**
- `defender_type` (str): Defending type combination

**Returns:** List of types the defender resists

#### `get_immune_types(defender_type)`

Get types that a defender is immune to (0.0x effectiveness).

**Parameters:**
- `defender_type` (str): Defending type combination

**Returns:** List of types the defender is immune to

## 🎮 Usage Examples

### Example 1: Type Coverage Analysis

```python
from revomonauto.revomon.clients import TypesClient

types_client = TypesClient()

# Analyze type coverage for team building
def analyze_type_coverage():
    coverage_score = {}

    # Get all defensive types
    all_types = types_client.get_all_types()

    for defender_type in all_types[:10]:  # Analyze first 10 types
        super_effective = types_client.get_super_effective_types(defender_type)
        weak_to = types_client.get_types_weak_to(defender_type)
        immune_to = types_client.get_immune_types(defender_type)

        coverage_score[defender_type] = {
            'weaknesses': len(super_effective),
            'resistances': len(weak_to),
            'immunities': len(immune_to),
            'total_exploits': len(super_effective) + len(immune_to) * 2  # Weight immunities
        }

    # Find best coverage
    best_coverage = max(coverage_score.items(), key=lambda x: x[1]['total_exploits'])
    return coverage_score, best_coverage

coverage, best = analyze_type_coverage()
print(f"Best coverage target: {best[0]} ({best[1]['total_exploits']} exploits)")
```

### Example 2: Offensive Type Analysis

```python
# Find optimal attacking types
def find_optimal_attackers(target_types):
    attacker_scores = {}

    for attacker in types_client.get_all_types():
        total_effectiveness = 0

        for defender in target_types:
            effectiveness = types_client.get_effectiveness_against(attacker, defender)
            if effectiveness:
                total_effectiveness += effectiveness

        avg_effectiveness = total_effectiveness / len(target_types)
        attacker_scores[attacker] = avg_effectiveness

    # Sort by effectiveness
    sorted_attackers = sorted(attacker_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_attackers

# Find best attackers against common team types
common_types = ["water", "fire", "grass", "electric"]
optimal_attackers = find_optimal_attackers(common_types)

print("Optimal attackers against common types:")
for attacker, score in optimal_attackers[:5]:
    print(f"  {attacker}: {score:.2f}x average effectiveness")
```

### Example 3: Defensive Type Planning

```python
# Plan defensive typing for team
def plan_defensive_typing():
    defensive_analysis = {}

    # Analyze all types for defensive potential
    all_types = types_client.get_all_types()

    for def_type in all_types:
        # Count weaknesses and resistances
        weaknesses = len(types_client.get_super_effective_types(def_type))
        resistances = len(types_client.get_types_weak_to(def_type))
        immunities = len(types_client.get_immune_types(def_type))

        # Calculate defensive score (lower weaknesses = better)
        defensive_score = (resistances * 0.5) + (immunities * 1.0) - (weaknesses * 1.0)
        defensive_analysis[def_type] = {
            'defensive_score': defensive_score,
            'weaknesses': weaknesses,
            'resistances': resistances,
            'immunities': immunities
        }

    # Find best defensive types
    best_defensive = sorted(defensive_analysis.items(),
                           key=lambda x: x[1]['defensive_score'],
                           reverse=True)

    return defensive_analysis, best_defensive

defensive, best = plan_defensive_typing()
print("Best defensive types:")
for def_type, stats in best[:5]:
    print(f"  {def_type}: Score {stats['defensive_score']:.1f} "
          f"(W:{stats['weaknesses']} R:{stats['resistances']} I:{stats['immunities']})")
```

### Example 4: Type Meta Analysis

```python
# Comprehensive type meta analysis
def analyze_type_meta():
    type_stats = {
        'offensive': {},
        'defensive': {},
        'versatility': {}
    }

    all_types = types_client.get_all_types()

    for def_type in all_types:
        # Offensive potential
        super_effective = types_client.get_super_effective_types(def_type)
        offensive_score = len(super_effective)

        # Defensive quality
        weaknesses = len(types_client.get_super_effective_types(def_type))
        resistances = len(types_client.get_types_weak_to(def_type))
        immunities = len(types_client.get_immune_types(def_type))
        defensive_score = (resistances * 0.5) + (immunities * 1.0) - (weaknesses * 1.0)

        # Versatility (balance of offense and defense)
        versatility_score = (offensive_score * 0.6) + (defensive_score * 0.4)

        type_stats['offensive'][def_type] = offensive_score
        type_stats['defensive'][def_type] = defensive_score
        type_stats['versatility'][def_type] = versatility_score

    # Find best in each category
    best_offensive = max(type_stats['offensive'].items(), key=lambda x: x[1])
    best_defensive = max(type_stats['defensive'].items(), key=lambda x: x[1])
    best_versatile = max(type_stats['versatility'].items(), key=lambda x: x[1])

    return type_stats, {
        'best_offensive': best_offensive,
        'best_defensive': best_defensive,
        'best_versatile': best_versatile
    }

meta, best_types = analyze_type_meta()
print(f"Best offensive: {best_types['best_offensive'][0]} ({best_types['best_offensive'][1]} weaknesses)")
print(f"Best defensive: {best_types['best_defensive'][0]} ({best_types['best_defensive'][1]:.1f} score)")
print(f"Most versatile: {best_types['best_versatile'][0]} ({best_types['best_versatile'][1]:.1f} score)")
```

## 🏆 Advanced Type Analysis

### Type Coverage Optimization

```python
# Find optimal type coverage for team building
def optimize_type_coverage(target_coverage=18):
    """
    Find the minimal set of types that cover all weaknesses
    """
    all_types = types_client.get_all_types()
    covered_types = set()
    selected_types = []

    # Start with types that have most weaknesses
    type_weaknesses = {}
    for def_type in all_types:
        weaknesses = set(types_client.get_super_effective_types(def_type))
        type_weaknesses[def_type] = weaknesses

    # Greedy algorithm: always pick type that covers most remaining types
    remaining_types = set(all_types)

    while remaining_types and len(covered_types) < target_coverage:
        best_type = None
        best_coverage = set()

        for candidate in remaining_types:
            new_coverage = covered_types | type_weaknesses[candidate]
            if len(new_coverage) > len(best_coverage):
                best_coverage = new_coverage
                best_type = candidate

        if best_type:
            selected_types.append(best_type)
            covered_types = best_coverage
            remaining_types.remove(best_type)

    return selected_types, len(covered_types)

optimal_team, coverage = optimize_type_coverage()
print(f"Optimal type coverage team: {optimal_team}")
print(f"Types covered: {coverage}/18")
```

### Type Synergy Analysis

```python
# Analyze type combinations for synergy
def analyze_type_synergy(type1, type2=None):
    """
    Analyze how well types work together offensively and defensively
    """
    if not type2:
        # Single type analysis
        super_effective = set(types_client.get_super_effective_types(type1))
        weaknesses = set(types_client.get_super_effective_types(type1))
        resistances = set(types_client.get_types_weak_to(type1))
        immunities = set(types_client.get_immune_types(type1))

        synergy_score = (len(super_effective) * 1.0) + (len(immunities) * 2.0) - (len(weaknesses) * 1.0)
        return {
            'type': type1,
            'synergy_score': synergy_score,
            'offensive_score': len(super_effective),
            'defensive_score': (len(resistances) * 0.5) + (len(immunities) * 1.0) - (len(weaknesses) * 1.0)
        }
    else:
        # Dual type analysis (more complex)
        dual_type = f"{type1}/{type2}"

        # Check if dual type exists
        if dual_type in types_client.get_all_types():
            return analyze_type_synergy(dual_type)

        # Estimate dual type effectiveness
        type1_data = analyze_type_synergy(type1)
        type2_data = analyze_type_synergy(type2)

        # Combine scores (simplified)
        combined_score = (type1_data['synergy_score'] + type2_data['synergy_score']) / 2
        return {
            'type': dual_type,
            'estimated_synergy_score': combined_score,
            'type1_score': type1_data['synergy_score'],
            'type2_score': type2_data['synergy_score']
        }

# Analyze top type synergies
single_types = types_client.get_single_types()
synergy_scores = []

for type_record in single_types:
    type_name = type_record['type1']
    synergy = analyze_type_synergy(type_name)
    synergy_scores.append((type_name, synergy['synergy_score']))

# Sort by synergy
synergy_scores.sort(key=lambda x: x[1], reverse=True)
print("Top type synergies:")
for type_name, score in synergy_scores[:10]:
    print(f"  {type_name}: {score:.1f} synergy score")
```

## 📈 Performance

- **Fast lookups**: Indexed type combinations for instant effectiveness queries
- **Cached matrix**: Type effectiveness data loaded once and cached
- **Batch analysis**: Support for analyzing multiple type combinations efficiently
- **Memory optimized**: Comprehensive type data with minimal memory footprint

## 🧪 Testing

```bash
# Run types client tests
uv run python -m pytest tests/clients/test_types_client.py

# Test type effectiveness
uv run python tests/integration/test_type_effectiveness.py

# Performance benchmarks
uv run python tests/performance/test_type_analysis.py
```

## 🤝 Contributing

1. Ensure type effectiveness matrix is accurate to game mechanics
2. Add comprehensive tests for new type interactions
3. Update effectiveness when new types are added to the game
4. Document any balance changes with sources

## 🔄 Version History

### v2.0.0
- Complete 18+ type effectiveness system
- Dual-type combination support
- Advanced type synergy and coverage analysis
- Comprehensive type meta analysis tools
- Offensive and defensive optimization algorithms

### v1.0.0
- Basic type effectiveness lookup
- Single type analysis
- Simple super effective/weak/immune queries

---

**Ready to master the elemental battlefield? Let the type analysis begin!** ⚔️🛡️🔥
