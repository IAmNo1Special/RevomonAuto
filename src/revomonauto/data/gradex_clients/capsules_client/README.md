# CapsulesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Move capsule system client for Revomon, providing access to TM/HM-style move teaching mechanics, move acquisition tracking, and competitive move pool analysis for optimal team building.

## 💊 Overview

The CapsulesClient provides the complete move teaching system for Revomon:

- **Move capsules** equivalent to Pokémon TMs/HMs
- **Move acquisition** tracking and compatibility
- **Learning mechanics** and move distribution analysis
- **Competitive move pools** and accessibility optimization
- **Move discovery** tools for team building and strategy

This client bridges the gap between available moves and what Revomon can actually learn, essential for understanding move pool distribution and team optimization.

## 📊 Capsule Data Structure

Each capsule contains move teaching information:

### Core Information
- **`cap_num`** - Unique capsule number (primary key)
- **`move_id`** - Associated move ID for linking to MovesClient
- **`move_name`** - Name of the move contained in the capsule

### Learning System
- **Move acquisition** through capsule mechanics
- **Compatibility** with different Revomon species
- **Teaching methods** and requirements
- **Move distribution** across the Revomon ecosystem

## 🚀 Quick Start

### Basic Capsule Lookup

```python
from revomonauto.revomon.clients import CapsulesClient

# Initialize client
capsules_client = CapsulesClient()

# Get capsule by number
capsule_1 = capsules_client.get_capsule(1)
if capsule_1:
    print(f"Capsule {capsule_1['cap_num']}: {capsule_1['move_name']}")

# Get capsule by move ID
earthquake_capsule = capsules_client.get_capsule_by_move_id(123)
if earthquake_capsule:
    print(f"Earthquake is in capsule #{earthquake_capsule['cap_num']}")

# Get capsule by move name
fire_capsule = capsules_client.get_capsule_by_move_name("flamethrower")
if fire_capsule:
    print(f"Flamethrower capsule: #{fire_capsule['cap_num']}")
```

### Move Pool Analysis

```python
# Get all moves available in capsules
capsule_moves = capsules_client.get_all_moves_in_capsules()
print(f"Moves available in capsules: {len(capsule_moves)}")

# Search capsules by move name pattern
earth_moves = capsules_client.get_capsules_by_move_name_pattern("earth")
print(f"Earth-related moves: {len(earth_moves)}")
for move in earth_moves:
    print(f"  {move['move_name']} (Capsule #{move['cap_num']})")
```

## 📚 API Reference

### Core Query Methods

#### `get_capsule(cap_num)`

Get capsule data by capsule number.

**Parameters:**
- `cap_num` (int): The capsule number

**Returns:** Capsule data dictionary or None if not found

#### `get_capsule_by_move_id(move_id)`

Get capsule containing a specific move by ID.

**Parameters:**
- `move_id` (int): The move ID

**Returns:** Capsule data dictionary or None if not found

#### `get_capsule_by_move_name(move_name)`

Get capsule containing a specific move by name.

**Parameters:**
- `move_name` (str): The move name

**Returns:** Capsule data dictionary or None if not found

#### `get_all_moves_in_capsules()`

Get all move names available through capsules.

**Returns:** List of move names in capsule system

#### `get_capsules_by_move_name_pattern(pattern)`

Search capsules by move name patterns.

**Parameters:**
- `pattern` (str): Pattern to search for in move names

**Returns:** List of capsules matching the pattern

## 🎮 Usage Examples

### Example 1: Move Acquisition Planning

```python
from revomonauto.revomon.clients import CapsulesClient

capsules_client = CapsulesClient()

# Plan move acquisition for team building
def plan_move_acquisition(target_moves, budget=None):
    """
    Plan which capsules to acquire for specific moves
    """
    acquisition_plan = []

    for move_name in target_moves:
        capsule = capsules_client.get_capsule_by_move_name(move_name)
        if capsule:
            acquisition_plan.append({
                'move': move_name,
                'capsule_number': capsule['cap_num'],
                'move_id': capsule['move_id'],
                'priority': 'essential' if move_name in ['earthquake', 'ice beam', 'thunderbolt'] else 'useful'
            })

    # Sort by priority and capsule number
    priority_order = {'essential': 3, 'useful': 2, 'nice': 1}
    acquisition_plan.sort(key=lambda x: (priority_order.get(x['priority'], 0), x['capsule_number']),
                         reverse=True)

    return acquisition_plan

# Plan acquisition for coverage moves
coverage_moves = ["earthquake", "ice beam", "thunderbolt", "flamethrower", "psychic"]
acquisition_plan = plan_move_acquisition(coverage_moves)

print("=== Move Acquisition Plan ===")
for item in acquisition_plan:
    print(f"{item['move']}: Capsule #{item['capsule_number']} (Priority: {item['priority']})")
```

### Example 2: Move Distribution Analysis

```python
# Analyze move distribution across capsules
def analyze_move_distribution():
    all_moves = capsules_client.get_all_moves_in_capsules()

    # Categorize moves by type (would need integration with MovesClient)
    move_categories = {
        'physical': [],
        'special': [],
        'status': [],
        'unknown': []
    }

    # Count capsules by move power levels (estimated)
    power_ranges = {
        'low': [],
        'medium': [],
        'high': [],
        'nuclear': []
    }

    print("=== Move Distribution Analysis ===")
    print(f"Total capsule moves: {len(all_moves)}")
    print(f"Unique moves: {len(set(all_moves))}")

    # Show most common moves
    move_counts = {}
    for move in all_moves:
        move_counts[move] = move_counts.get(move, 0) + 1

    common_moves = sorted(move_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nMost available moves:")
    for move, count in common_moves[:10]:
        print(f"  {move}: {count} capsules")

analyze_move_distribution()
```

### Example 3: Competitive Move Pool Optimization

```python
# Find optimal moves for competitive team building
def optimize_move_pool(team_types, strategy="balanced"):
    """
    Find the best moves available through capsules for team composition
    """
    # Key competitive moves by type
    essential_moves = {
        'fire': ['flamethrower', 'fire blast', 'overheat'],
        'water': ['surf', 'hydro pump', 'ice beam'],
        'grass': ['solar beam', 'petal dance', 'razor leaf'],
        'electric': ['thunderbolt', 'thunder', 'thunder wave'],
        'ground': ['earthquake', 'earth power', 'dig'],
        'psychic': ['psychic', 'psyshock', 'calm mind']
    }

    available_moves = []
    for team_type in team_types:
        if team_type in essential_moves:
            for move in essential_moves[team_type]:
                capsule = capsules_client.get_capsule_by_move_name(move)
                if capsule:
                    available_moves.append({
                        'move': move,
                        'type': team_type,
                        'capsule': capsule['cap_num'],
                        'competitive_rating': 'high' if move in ['earthquake', 'ice beam', 'thunderbolt'] else 'medium'
                    })

    # Sort by competitive importance
    rating_order = {'high': 3, 'medium': 2, 'low': 1}
    available_moves.sort(key=lambda x: (rating_order.get(x['competitive_rating'], 0), x['capsule']))

    return available_moves

# Optimize move pool for balanced team
team_types = ["fire", "water", "electric"]
optimal_moves = optimize_move_pool(team_types)

print("=== Optimal Move Pool ===")
for move in optimal_moves:
    print(f"{move['move']} ({move['type']}): Capsule #{move['capsule']} - {move['competitive_rating']} priority")
```

### Example 4: Move Discovery and Exploration

```python
# Discover new moves for team building
def discover_move_options(search_patterns):
    """
    Discover moves using pattern matching
    """
    discovered_moves = []

    for pattern in search_patterns:
        capsules = capsules_client.get_capsules_by_move_name_pattern(pattern)
        for capsule in capsules:
            move_info = {
                'move_name': capsule['move_name'],
                'capsule_number': capsule['cap_num'],
                'move_id': capsule['move_id'],
                'search_pattern': pattern
            }
            discovered_moves.append(move_info)

    # Remove duplicates
    seen_moves = set()
    unique_moves = []
    for move in discovered_moves:
        if move['move_name'] not in seen_moves:
            seen_moves.add(move['move_name'])
            unique_moves.append(move)

    return unique_moves

# Discover moves by attack patterns
attack_patterns = ["blast", "beam", "punch", "kick", "bite", "claw"]
discovered = discover_move_options(attack_patterns)

print("=== Discovered Moves ===")
for move in discovered[:15]:  # Show first 15 discoveries
    print(f"{move['move_name']}: Capsule #{move['capsule_number']} (found via '{move['search_pattern']}')")
```

## 🏆 Advanced Capsule Analysis

### Move Accessibility Analysis

```python
# Analyze move accessibility and acquisition difficulty
def analyze_move_accessibility():
    """
    Analyze how accessible moves are through the capsule system
    """
    accessibility_analysis = {
        'common_moves': [],
        'rare_moves': [],
        'utility_moves': []
    }

    all_capsules = capsules_client.get_all()
    move_frequency = {}

    # Count how often each move appears
    for capsule in all_capsules:
        move_name = capsule['move_name']
        move_frequency[move_name] = move_frequency.get(move_name, 0) + 1

    # Categorize by frequency
    for move, frequency in move_frequency.items():
        if frequency >= 3:
            accessibility_analysis['common_moves'].append({'move': move, 'frequency': frequency})
        elif frequency == 1:
            accessibility_analysis['rare_moves'].append({'move': move, 'frequency': frequency})
        else:
            accessibility_analysis['utility_moves'].append({'move': move, 'frequency': frequency})

    # Sort by frequency
    for category in accessibility_analysis.values():
        category.sort(key=lambda x: x['frequency'], reverse=True)

    return accessibility_analysis

accessibility = analyze_move_accessibility()

print("=== Move Accessibility Analysis ===")
print(f"Common moves (3+ capsules): {len(accessibility['common_moves'])}")
print(f"Rare moves (1 capsule): {len(accessibility['rare_moves'])}")
print(f"Utility moves (2 capsules): {len(accessibility['utility_moves'])}")

print("\nMost accessible moves:")
for move in accessibility['common_moves'][:5]:
    print(f"  {move['move']}: {move['frequency']} capsules")
```

### Capsule Collection Strategy

```python
# Develop strategy for collecting optimal capsules
def develop_capsule_strategy(budget=50, team_strategy="coverage"):
    """
    Develop capsule collection strategy based on team needs
    """
    if team_strategy == "coverage":
        # Focus on type coverage moves
        coverage_moves = [
            "earthquake", "ice beam", "thunderbolt", "flamethrower",
            "solar beam", "sludge bomb", "psychic", "dark pulse"
        ]
    elif team_strategy == "offensive":
        # Focus on high-power moves
        coverage_moves = [
            "hyper beam", "giga impact", "blast burn", "hydro cannon",
            "frenzy plant", "volt tackle", "dragon claw", "close combat"
        ]
    else:  # utility
        # Focus on utility moves
        coverage_moves = [
            "toxic", "thunder wave", "hypnosis", "confuse ray",
            "stealth rock", "rapid spin", "heal bell", "aromatherapy"
        ]

    strategy = []
    total_cost = 0

    for move in coverage_moves:
        capsule = capsules_client.get_capsule_by_move_name(move)
        if capsule:
            # Estimate capsule cost (would need ItemsClient integration)
            estimated_cost = capsule['cap_num']  # Simplified cost model

            if total_cost + estimated_cost <= budget:
                strategy.append({
                    'move': move,
                    'capsule': capsule['cap_num'],
                    'estimated_cost': estimated_cost,
                    'priority': 'high'
                })
                total_cost += estimated_cost

    return strategy, total_cost

# Develop coverage strategy
coverage_strategy, total_cost = develop_capsule_strategy(100, "coverage")

print("=== Capsule Collection Strategy ===")
print(f"Total estimated cost: {total_cost}")
print("\nMoves to collect:")
for item in coverage_strategy:
    print(f"  {item['move']}: Capsule #{item['capsule']} (Cost: {item['estimated_cost']})")
```

## 📈 Performance

- **Fast lookups**: Indexed capsule numbers and move names
- **Cached data**: Capsule database loaded once and cached
- **Efficient searches**: Optimized pattern matching for move discovery
- **Memory efficient**: Minimal memory footprint for analysis

## 🧪 Testing

```bash
# Run capsules client tests
uv run python -m pytest tests/clients/test_capsules_client.py

# Test move acquisition
uv run python tests/integration/test_move_acquisition.py

# Performance benchmarks
uv run python tests/performance/test_capsule_queries.py
```

## 🤝 Contributing

1. Ensure all capsule data is accurate to game move teaching mechanics
2. Add comprehensive tests for new acquisition methods
3. Update capsule contents when new moves are added
4. Document any move distribution changes

## 🔄 Version History

### v2.0.0
- Complete capsule system with move acquisition tracking
- Advanced move discovery and pattern matching
- Competitive move pool optimization
- Capsule collection strategy tools
- Comprehensive accessibility analysis

### v1.0.0
- Basic capsule lookup by number
- Simple move name searches
- Basic move availability queries

---

**Ready to unlock the complete move arsenal and master the capsule system? Let the move acquisition begin!** 💊🎯📚
