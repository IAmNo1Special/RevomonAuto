# AbilitiesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive abilities database for Revomon, providing access to all passive abilities including stat modifications, status effects, weather interactions, and type enhancements for competitive strategy optimization.

## 🎭 Overview

The AbilitiesClient provides complete access to the Revomon ability system:

- **100+ Unique abilities** with detailed effects and mechanics
- **Stat modification abilities** for competitive optimization
- **Status effect abilities** for control and prevention strategies
- **Weather manipulation** for environmental control
- **Type enhancement** for elemental synergy
- **Hidden mechanics** analysis for competitive advantage

This client unlocks the hidden layer of Revomon combat, revealing the passive abilities that often determine the outcome of high-level battles.

## 📊 Ability Data Structure

Each ability contains comprehensive information:

### Core Information
- **`name`** - Unique ability identifier (primary key)
- **`description`** - Detailed explanation of effects and mechanics

### Effect Categories
- **Stat Modifiers** - Attack, Defense, Speed, Special Attack, Special Defense, HP
- **Status Effects** - Poison, Paralysis, Sleep, Freeze, Burn, Confusion, Flinch
- **Weather Control** - Sun, Rain, Sandstorm, Snow manipulation
- **Type Enhancement** - STAB bonuses, type effectiveness modifications
- **Unique Effects** - Entry hazards, priority manipulation, immunity granting

## 🚀 Quick Start

### Basic Ability Lookup

```python
from revomonauto.revomon.clients import AbilitiesClient

# Initialize client
abilities_client = AbilitiesClient()

# Get ability by name
overgrow = abilities_client.get_ability("overgrow")
print(f"Overgrow: {overgrow['description']}")

# Get all abilities
all_abilities = abilities_client.get_all_abilities()
print(f"Total abilities: {len(all_abilities)}")

# Search by description
grass_abilities = abilities_client.search_abilities_by_description("grass")
print(f"Grass-related abilities: {len(grass_abilities)}")
```

### Ability Category Analysis

```python
# Get abilities by effect type
stat_abilities = abilities_client.get_abilities_with_stat_modification()
status_abilities = abilities_client.get_abilities_with_status_effects()
weather_abilities = abilities_client.get_abilities_with_weather_effects()
type_abilities = abilities_client.get_abilities_with_type_effects()

print(f"Stat modifiers: {len(stat_abilities)}")
print(f"Status abilities: {len(status_abilities)}")
print(f"Weather abilities: {len(weather_abilities)}")
print(f"Type abilities: {len(type_abilities)}")
```

## 📚 API Reference

### Core Query Methods

#### `get_ability(ability_name)`

Get ability data by name.

**Parameters:**
- `ability_name` (str): The ability name

**Returns:** Ability data dictionary or None if not found

#### `get_all_abilities()`

Get all available ability names.

**Returns:** List of all ability names

#### `search_abilities_by_description(search_term)`

Search abilities by description content.

**Parameters:**
- `search_term` (str): Text to search for

**Returns:** List of abilities containing the search term

#### `get_abilities_by_keyword(keyword)`

Search abilities by name or description keywords.

**Parameters:**
- `keyword` (str): Keyword to search for

**Returns:** List of matching abilities

### Effect Category Methods

#### `get_abilities_with_stat_modification()`

Get abilities that modify combat stats.

**Returns:** List of stat-modifying abilities

#### `get_abilities_with_status_effects()`

Get abilities that cause or prevent status conditions.

**Returns:** List of status-related abilities

#### `get_abilities_with_weather_effects()`

Get abilities that interact with weather conditions.

**Returns:** List of weather-manipulating abilities

#### `get_abilities_with_type_effects()`

Get abilities that modify type effectiveness or provide type benefits.

**Returns:** List of type-enhancing abilities

## 🎮 Usage Examples

### Example 1: Competitive Ability Analysis

```python
from revomonauto.revomon.clients import AbilitiesClient

abilities_client = AbilitiesClient()

# Analyze competitive ability distribution
def analyze_ability_meta():
    categories = {
        'stat_modifiers': abilities_client.get_abilities_with_stat_modification(),
        'status_control': abilities_client.get_abilities_with_status_effects(),
        'weather_control': abilities_client.get_abilities_with_weather_effects(),
        'type_enhancement': abilities_client.get_abilities_with_type_effects()
    }

    print("=== Ability Meta Analysis ===")
    for category, abilities in categories.items():
        print(f"{category.replace('_', ' ').title()}: {len(abilities)} abilities")

        # Show top examples
        if abilities:
            print(f"  Examples: {[a['name'] for a in abilities[:3]]}")

analyze_ability_meta()
```

### Example 2: Team Ability Synergy

```python
# Find optimal ability combinations for team
def find_ability_synergies(team_types, team_role="balanced"):
    """
    Find abilities that synergize with team composition
    """
    synergies = {
        'speed_control': [],
        'defensive': [],
        'offensive': [],
        'support': []
    }

    # Weather control for weather teams
    if "water" in team_types or "fire" in team_types:
        weather_abilities = abilities_client.get_abilities_with_weather_effects()
        synergies['support'].extend(weather_abilities)

    # Status control for stall teams
    if team_role == "stall":
        status_abilities = abilities_client.get_abilities_with_status_effects()
        synergies['support'].extend(status_abilities)

    # Speed control for offensive teams
    if team_role == "offensive":
        speed_abilities = [a for a in abilities_client.get_abilities_with_stat_modification()
                          if "speed" in a['description'].lower()]
        synergies['speed_control'].extend(speed_abilities)

    # Defensive abilities for tank teams
    if team_role == "tank":
        defensive_abilities = [a for a in abilities_client.get_abilities_with_stat_modification()
                              if any(word in a['description'].lower()
                                    for word in ["defense", "defensive", "tank", "wall"])]
        synergies['defensive'].extend(defensive_abilities)

    return synergies

# Analyze synergies for a water/fire team
team_types = ["water", "fire"]
synergies = find_ability_synergies(team_types, "offensive")

print("Recommended abilities for Water/Fire team:")
for category, abilities in synergies.items():
    if abilities:
        print(f"  {category}: {[a['name'] for a in abilities[:3]]}")
```

### Example 3: Hidden Ability Discovery

```python
# Find powerful hidden abilities for competitive play
def discover_hidden_gems():
    all_abilities = abilities_client.get_all()

    # Look for abilities with multiple effect types
    powerful_abilities = []

    for ability in all_abilities:
        effect_score = 0
        description = ability['description'].lower()

        # Score based on effect types
        if any(word in description for word in ["attack", "damage", "power"]):
            effect_score += 1
        if any(word in description for word in ["speed", "priority", "first"]):
            effect_score += 1
        if any(word in description for word in ["immune", "prevent", "resist"]):
            effect_score += 1
        if any(word in description for word in ["weather", "terrain", "field"]):
            effect_score += 1

        if effect_score >= 2:  # Multi-effect abilities
            powerful_abilities.append({
                'name': ability['name'],
                'score': effect_score,
                'description': ability['description']
            })

    # Sort by power score
    powerful_abilities.sort(key=lambda x: x['score'], reverse=True)
    return powerful_abilities

hidden_gems = discover_hidden_gems()
print("Powerful hidden abilities:")
for gem in hidden_gems[:10]:
    print(f"  {gem['name']}: {gem['description'][:100]}...")
```

### Example 4: Ability Counter Strategy

```python
# Develop counter strategies based on abilities
def develop_ability_counters(target_abilities):
    counters = {
        'status_prevention': [],
        'weather_control': [],
        'stat_reduction': [],
        'type_exploitation': []
    }

    for ability in target_abilities:
        description = ability['description'].lower()

        # Find counter strategies
        if any(word in description for word in ["poison", "paralyze", "sleep", "burn"]):
            # Find prevention abilities
            prevention = [a for a in abilities_client.get_abilities_with_status_effects()
                         if any(word in a['description'].lower()
                               for word in ["prevent", "immune", "resist"])]
            counters['status_prevention'].extend(prevention)

        if any(word in description for word in ["weather", "sun", "rain", "sand"]):
            # Find weather manipulation abilities
            weather_control = abilities_client.get_abilities_with_weather_effects()
            counters['weather_control'].extend(weather_control)

        if any(word in description for word in ["attack", "speed", "stat"]):
            # Find abilities that counter stat boosts
            stat_counters = [a for a in abilities_client.get_abilities_with_stat_modification()
                            if any(word in a['description'].lower()
                                  for word in ["reduce", "lower", "decrease", "weaken"])]
            counters['stat_reduction'].extend(stat_counters)

    return counters

# Find counters for common competitive abilities
competitive_abilities = [
    abilities_client.get_ability("speed boost"),
    abilities_client.get_ability("drizzle"),
    abilities_client.get_ability("tough claws")
]

counters = develop_ability_counters(competitive_abilities)
print("Ability counters:")
for category, counter_abilities in counters.items():
    if counter_abilities:
        print(f"  {category}: {[a['name'] for a in counter_abilities[:3]]}")
```

## 🏆 Advanced Ability Analysis

### Ability Tier Classification

```python
# Classify abilities by competitive tier
def classify_ability_tiers():
    tiers = {
        'S': [],  # Broken/overpowered
        'A': [],  # Very strong
        'B': [],  # Good/situational
        'C': [],  # Niche use
        'D': []   # Weak/minor effects
    }

    all_abilities = abilities_client.get_all()

    for ability in all_abilities:
        tier_score = 0
        description = ability['description'].lower()

        # Tier scoring criteria
        if any(word in description for word in ["boost", "increase", "raise", "enhance"]):
            tier_score += 2
        if any(word in description for word in ["immune", "prevent", "block", "resist"]):
            tier_score += 2
        if any(word in description for word in ["weather", "terrain", "field"]):
            tier_score += 1
        if any(word in description for word in ["priority", "first", "speed"]):
            tier_score += 1
        if any(word in description for word in ["reduce", "lower", "weaken", "decrease"]):
            tier_score -= 1

        # Assign tiers based on score
        if tier_score >= 4:
            tiers['S'].append(ability)
        elif tier_score >= 2:
            tiers['A'].append(ability)
        elif tier_score >= 0:
            tiers['B'].append(ability)
        elif tier_score >= -1:
            tiers['C'].append(ability)
        else:
            tiers['D'].append(ability)

    return tiers

ability_tiers = classify_ability_tiers()
print("Ability tier distribution:")
for tier, abilities in ability_tiers.items():
    print(f"  Tier {tier}: {len(abilities)} abilities")
    if abilities:
        print(f"    Top: {[a['name'] for a in abilities[:3]]}")
```

### Ability Synergy Network

```python
# Analyze ability synergies and combinations
def analyze_ability_synergies():
    synergy_pairs = []

    # Get abilities by category
    stat_abilities = abilities_client.get_abilities_with_stat_modification()
    status_abilities = abilities_client.get_abilities_with_status_effects()
    weather_abilities = abilities_client.get_abilities_with_weather_effects()

    # Find synergies between categories
    for stat_ability in stat_abilities[:10]:  # Limit for performance
        for weather_ability in weather_abilities:
            # Check for potential synergy (e.g., speed + weather)
            if ("speed" in stat_ability['description'].lower() and
                any(word in weather_ability['description'].lower()
                    for word in ["tailwind", "boost", "enhance"])):
                synergy_pairs.append({
                    'abilities': [stat_ability['name'], weather_ability['name']],
                    'synergy_type': 'speed_weather',
                    'description': f"{stat_ability['name']} + {weather_ability['name']}"
                })

    # Find status prevention synergies
    for status_ability in status_abilities:
        if any(word in status_ability['description'].lower()
               for word in ["prevent", "immune", "block"]):
            for stat_ability in stat_abilities:
                if any(word in stat_ability['description'].lower()
                       for word in ["bulk", "tank", "defensive"]):
                    synergy_pairs.append({
                        'abilities': [status_ability['name'], stat_ability['name']],
                        'synergy_type': 'tank_prevention',
                        'description': f"{status_ability['name']} + {stat_ability['name']}"
                    })

    return synergy_pairs

synergies = analyze_ability_synergies()
print("Top ability synergies:")
for synergy in synergies[:10]:
    print(f"  {synergy['description']} ({synergy['synergy_type']})")
```

## 📈 Performance

- **Fast searches**: Indexed ability names and description content
- **Cached data**: Ability database loaded once and cached
- **Efficient filtering**: Optimized keyword matching algorithms
- **Memory optimized**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run abilities client tests
uv run python -m pytest tests/clients/test_abilities_client.py

# Test ability analysis
uv run python tests/integration/test_ability_analysis.py

# Performance benchmarks
uv run python tests/performance/test_ability_queries.py
```

## 🤝 Contributing

1. Ensure all ability descriptions are accurate to game mechanics
2. Add comprehensive tests for new analysis methods
3. Update ability effects when balance changes occur
4. Document any hidden mechanics discovered

## 🔄 Version History

### v2.0.0
- Complete ability database with 100+ abilities
- Advanced filtering by effect categories
- Competitive tier analysis and synergy detection
- Comprehensive meta analysis tools
- Hidden mechanics discovery algorithms

### v1.0.0
- Basic ability lookup by name
- Simple description search
- Basic keyword filtering

---

**Ready to unlock the hidden power of Revomon abilities? Let the strategic analysis begin!** 🎭✨🧙‍♂️
