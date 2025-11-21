# RevomonMovesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Move learnset and compatibility system for Revomon, providing comprehensive access to which moves each species can learn, learning methods, level requirements, and competitive move pool optimization.

## 📚 Overview

The RevomonMovesClient provides the complete move learning system for Revomon:

- **Level-up moves** with progression and natural learning
- **TM/HM moves** (capsule system) for teaching compatibility
- **Move requirements** and level prerequisites
- **Learning method analysis** and acquisition strategies
- **Move distribution** across the Revomon ecosystem
- **Competitive move pool** optimization and team building

This client bridges the gap between available moves and Revomon capabilities, essential for understanding move pool distribution and team building limitations.

## 📊 Move Learning Data Structure

Each move learning entry contains comprehensive compatibility information:

### Core Information
- **`mon_dex_id`** - Revomon's Revodex ID
- **`mon_name`** - Revomon species name
- **`move_id`** - Move database ID
- **`move_name`** - Name of the learnable move

### Learning Mechanics
- **`method`** - Learning method (levelup, machine, tutor, etc.)
- **`level`** - Level learned (for levelup method, null for others)

### Acquisition Categories
- **Level-up** - Natural progression moves learned by leveling
- **Machine** - TM/HM moves taught through capsules
- **Tutor** - Special moves taught by move tutors
- **Other** - Special learning methods and requirements

## 🚀 Quick Start

### Basic Move Learning Analysis

```python
from revomonauto.revomon.clients import RevomonMovesClient

# Initialize client
moves_client = RevomonMovesClient()

# Get moves for a specific Revomon
monking_moves = moves_client.get_moves_by_revomon_id(25)
print(f"Monking can learn {len(monking_moves)} moves")

# Get moves by Revomon name
fire_starter_moves = moves_client.get_moves_by_revomon_name("gorlit")
print(f"Gorlit moves: {len(fire_starter_moves)}")

# Get all level-up moves
levelup_moves = moves_client.get_levelup_moves()
print(f"Level-up moves: {len(levelup_moves)}")

# Get machine (TM/HM) moves
machine_moves = moves_client.get_machine_moves()
print(f"Machine moves: {len(machine_moves)}")
```

### Learning Method Analysis

```python
# Analyze learning methods
method_dist = moves_client.get_learning_method_distribution()
print(f"Learning methods: {method_dist}")

# Get moves learned at specific levels
level_10_moves = moves_client.get_moves_learned_at_level(10)
print(f"Moves learned at level 10: {len(level_10_moves)}")

# Get Revomon-specific level moves
monking_level_20 = moves_client.get_revomon_levelup_moves_by_level(25, 20)
print(f"Monking learns at level 20: {[m['move_name'] for m in monking_level_20]}")
```

## 📚 API Reference

### Core Query Methods

#### `get_moves_by_revomon_id(dex_id)`

Get all moves learnable by a Revomon by Revodex ID.

**Parameters:**
- `dex_id` (int): The Revomon's Revodex ID

**Returns:** List of moves the Revomon can learn

#### `get_moves_by_revomon_name(name)`

Get all moves learnable by a Revomon by name.

**Parameters:**
- `name` (str): The Revomon name

**Returns:** List of moves the Revomon can learn

#### `get_all_learnable_moves()`

Get all unique move names that can be learned.

**Returns:** List of all learnable move names

#### `get_move_learning_methods(move_name)`

Get all learning methods for a specific move.

**Parameters:**
- `move_name` (str): The move name

**Returns:** List of learning methods for the move

### Learning Method Queries

#### `get_moves_by_learning_method(method)`

Get all moves learned by a specific method.

**Parameters:**
- `method` (str): Learning method (levelup, machine, tutor)

**Returns:** List of moves learned by the specified method

#### `get_levelup_moves()`, `get_machine_moves()`

Get moves by learning category (convenience methods).

**Returns:** List of moves in the category

#### `get_moves_learned_at_level(level)`

Get all moves learned at a specific level.

**Parameters:**
- `level` (int): The level

**Returns:** List of moves learned at the specified level

#### `get_revomon_levelup_moves_by_level(dex_id, level)`

Get moves a specific Revomon learns at a given level.

**Parameters:**
- `dex_id` (int): The Revomon's Revodex ID
- `level` (int): The level

**Returns:** List of moves learned at that level

### Analysis Methods

#### `get_revomon_with_move(move_name)`

Get all Revomon that can learn a specific move.

**Parameters:**
- `move_name` (str): The move name

**Returns:** List of Revomon that can learn the move

#### `get_learning_method_distribution()`

Get count of moves by learning method.

**Returns:** Dictionary mapping learning method to count

## 🎮 Usage Examples

### Example 1: Move Pool Optimization

```python
from revomonauto.revomon.clients import RevomonMovesClient

moves_client = RevomonMovesClient()

# Optimize move pools for team building
def optimize_move_pools(team_revomon):
    """
    Analyze move pools for optimal team composition
    """
    team_analysis = {}

    for revomon in team_revomon:
        moves = moves_client.get_moves_by_revomon_name(revomon['name'])
        if moves:
            # Categorize moves
            levelup_moves = [m for m in moves if m.get('method') == 'levelup']
            machine_moves = [m for m in moves if m.get('method') == 'machine']
            other_moves = [m for m in moves if m.get('method') not in ['levelup', 'machine']]

            # Analyze move acquisition timeline
            level_timeline = {}
            for move in levelup_moves:
                level = move.get('level', 0)
                if level not in level_timeline:
                    level_timeline[level] = []
                level_timeline[level].append(move['move_name'])

            team_analysis[revomon['name']] = {
                'total_moves': len(moves),
                'levelup_moves': len(levelup_moves),
                'machine_moves': len(machine_moves),
                'other_moves': len(other_moves),
                'level_timeline': level_timeline,
                'move_names': [m['move_name'] for m in moves]
            }

    return team_analysis

# Analyze move pools for starter team
starters = [
    {"name": "gorlit"}, {"name": "zorelle"}, {"name": "dekute"}
]

move_analysis = optimize_move_pools(starters)

print("=== Team Move Pool Analysis ===")
for revomon, analysis in move_analysis.items():
    print(f"{revomon}:")
    print(f"  Total moves: {analysis['total_moves']}")
    print(f"  Level-up: {analysis['levelup_moves']}, Machine: {analysis['machine_moves']}")
    print(f"  Level progression: {list(analysis['level_timeline'].keys())[:5]}")
    print()
```

### Example 2: Learning Progression Planning

```python
# Plan optimal learning progression for competitive training
def plan_learning_progression(revomon_name, target_level=50):
    """
    Plan optimal move learning progression
    """
    moves = moves_client.get_moves_by_revomon_name(revomon_name)
    if not moves:
        return []

    # Separate by learning method
    levelup_moves = [m for m in moves if m.get('method') == 'levelup']
    machine_moves = [m for m in moves if m.get('method') == 'machine']

    # Sort level-up moves by level
    levelup_moves.sort(key=lambda x: x.get('level', 0))

    # Create learning progression
    progression = []

    current_level = 1
    for move in levelup_moves:
        level = move.get('level', 0)
        if level <= target_level:
            progression.append({
                'level': level,
                'move': move['move_name'],
                'method': 'natural',
                'description': f"Learns {move['move_name']} at level {level}"
            })

    # Add machine moves at strategic levels
    machine_moves.sort(key=lambda x: x.get('move_id', 0))
    for move in machine_moves[:6]:  # Top 6 TMs for team
        # Suggest learning at specific competitive levels
        suggested_level = 20 + (machine_moves.index(move) * 5)
        if suggested_level <= target_level:
            progression.append({
                'level': suggested_level,
                'move': move['move_name'],
                'method': 'machine',
                'description': f"Teach {move['move_name']} via capsule at level {suggested_level}"
            })

    # Sort by level
    progression.sort(key=lambda x: x['level'])

    return progression

# Plan progression for a competitive Revomon
progression = plan_learning_progression("monking", 50)

print("=== Learning Progression Plan ===")
for step in progression:
    print(f"Level {step['level']"2d"}: {step['description']}")
```

### Example 3: Move Compatibility Analysis

```python
# Analyze move compatibility across species
def analyze_move_compatibility():
    """
    Analyze which moves are most widely available
    """
    # Get all Revomon-move relationships
    all_entries = moves_client.get_all()

    # Count how many Revomon can learn each move
    move_availability = {}
    for entry in all_entries:
        move_name = entry.get('move_name', '')
        if move_name:
            move_availability[move_name] = move_availability.get(move_name, 0) + 1

    # Find most and least available moves
    sorted_moves = sorted(move_availability.items(), key=lambda x: x[1], reverse=True)

    # Analyze by learning method
    method_analysis = moves_client.get_learning_method_distribution()

    print("=== Move Compatibility Analysis ===")
    print(f"Total move learning relationships: {len(all_entries)}")
    print(f"Unique moves: {len(move_availability)}")
    print(f"Learning methods: {method_analysis}")

    print("
Most available moves:")
    for move, count in sorted_moves[:10]:
        print(f"  {move}: {count} Revomon")

    print("
Least available moves:")
    for move, count in sorted_moves[-10:]:
        print(f"  {move}: {count} Revomon")

analyze_compatibility = analyze_move_compatibility()
```

### Example 4: Competitive Move Set Planning

```python
# Plan competitive move sets based on availability
def plan_competitive_movesets(revomon_list, strategy="coverage"):
    """
    Plan optimal move sets based on learning compatibility
    """
    moveset_plans = {}

    for revomon in revomon_list:
        moves = moves_client.get_moves_by_revomon_name(revomon['name'])
        if not moves:
            continue

        # Categorize moves for competitive planning
        levelup_moves = [m for m in moves if m.get('method') == 'levelup']
        machine_moves = [m for m in moves if m.get('method') == 'machine']

        # Plan early, mid, and late game moves
        early_moves = [m for m in levelup_moves if m.get('level', 0) <= 15]
        mid_moves = [m for m in levelup_moves if 16 <= m.get('level', 0) <= 35]
        late_moves = [m for m in levelup_moves if m.get('level', 0) >= 36]

        # Add TM moves for competitive edge
        tm_moves = machine_moves[:4]  # Top 4 TMs

        moveset_plans[revomon['name']] = {
            'early_game': [m['move_name'] for m in early_moves[:4]],
            'mid_game': [m['move_name'] for m in mid_moves[:4]],
            'late_game': [m['move_name'] for m in late_moves[:4]],
            'tm_additions': [m['move_name'] for m in tm_moves],
            'total_moves': len(moves)
        }

    return moveset_plans

# Plan competitive movesets
competitive_revomon = ["monking", "legendary_fire", "legendary_water"]
moveset_plans = plan_competitive_movesets(competitive_revomon)

print("=== Competitive Move Set Planning ===")
for revomon, plan in moveset_plans.items():
    print(f"{revomon} ({plan['total_moves']} total moves):")
    print(f"  Early: {plan['early_game']}")
    print(f"  Mid: {plan['mid_game']}")
    print(f"  Late: {plan['late_game']}")
    print(f"  TMs: {plan['tm_additions']}")
    print()
```

## 🏆 Advanced Move Learning Analysis

### Move Acquisition Efficiency

```python
# Analyze most efficient ways to acquire moves
def analyze_acquisition_efficiency():
    """
    Analyze the most efficient methods for move acquisition
    """
    efficiency_analysis = {
        'levelup_efficiency': [],
        'machine_efficiency': [],
        'method_comparison': {}
    }

    # Analyze level-up moves by level distribution
    levelup_moves = moves_client.get_levelup_moves()
    machine_moves = moves_client.get_machine_moves()

    # Level acquisition timeline
    level_timeline = {}
    for move in levelup_moves:
        level = move.get('level', 0)
        if level > 0:
            level_timeline[level] = level_timeline.get(level, 0) + 1

    # Find peak learning levels
    peak_learning = sorted(level_timeline.items(), key=lambda x: x[1], reverse=True)

    print("=== Move Acquisition Efficiency ===")
    print(f"Level-up moves: {len(levelup_moves)}")
    print(f"Machine moves: {len(machine_moves)}")
    print(f"Other methods: {len(moves_client.get_all()) - len(levelup_moves) - len(machine_moves)}")

    print("
Peak learning levels:")
    for level, count in peak_learning[:5]:
        print(f"  Level {level}: {count} moves learned")

    # Suggest optimal training levels
    optimal_levels = [level for level, count in peak_learning[:3]]
    print(f"\nSuggested power spike levels: {optimal_levels}")

# Analyze acquisition efficiency
analyze_efficiency = analyze_acquisition_efficiency()
```

### Move Pool Diversity Analysis

```python
# Analyze move pool diversity across species
def analyze_move_pool_diversity():
    """
    Analyze how diverse move pools are across different Revomon
    """
    all_entries = moves_client.get_all()

    # Group by Revomon
    revomon_pools = {}
    for entry in all_entries:
        revomon_name = entry.get('mon_name', '')
        move_name = entry.get('move_name', '')

        if revomon_name not in revomon_pools:
            revomon_pools[revomon_name] = set()
        revomon_pools[revomon_name].add(move_name)

    # Calculate diversity metrics
    pool_sizes = [len(moves) for moves in revomon_pools.values()]
    avg_pool_size = sum(pool_sizes) / len(pool_sizes) if pool_sizes else 0

    # Find most and least diverse move pools
    sorted_pools = sorted(revomon_pools.items(), key=lambda x: len(x[1]), reverse=True)

    print("=== Move Pool Diversity ===")
    print(f"Total Revomon with move data: {len(revomon_pools)}")
    print(f"Average moves per Revomon: {avg_pool_size:.1f}")
    print(f"Largest move pool: {sorted_pools[0][0]} ({len(sorted_pools[0][1])} moves)")
    print(f"Smallest move pool: {sorted_pools[-1][0]} ({len(sorted_pools[-1][1])} moves)")

    # Analyze method diversity
    method_diversity = {}
    for revomon, moves in list(revomon_pools.items())[:10]:  # Top 10 for analysis
        revomon_moves = moves_client.get_moves_by_revomon_name(revomon)

        methods = set()
        for move in revomon_moves:
            methods.add(move.get('method', 'unknown'))

        method_diversity[revomon] = {
            'total_moves': len(moves),
            'methods': list(methods),
            'method_count': len(methods)
        }

    print("
Top 10 method diversity:")
    for revomon, diversity in sorted(method_diversity.items(),
                                   key=lambda x: x[1]['method_count'],
                                   reverse=True):
        print(f"  {revomon}: {diversity['method_count']} methods, {diversity['total_moves']} moves")

analyze_diversity = analyze_move_pool_diversity()
```

## 📈 Performance

- **Fast queries**: Indexed Revomon IDs and move names
- **Cached data**: Move learning database loaded once and cached
- **Efficient analysis**: Optimized pool and timeline calculations
- **Memory efficient**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run revomon moves client tests
uv run python -m pytest tests/clients/test_revomon_moves_client.py

# Test move learning analysis
uv run python tests/integration/test_move_learning.py

# Performance benchmarks
uv run python tests/performance/test_moves_queries.py
```

## 🤝 Contributing

1. Ensure all move learning data is accurate to game mechanics
2. Add comprehensive tests for new learning method analysis
3. Update move compatibility when new Revomon or moves are added
4. Document any new learning methods or requirements

## 🔄 Version History

### v2.0.0
- Complete move learning system with method analysis
- Advanced move pool optimization and diversity analysis
- Competitive move set planning and progression tracking
- Learning efficiency analysis and timeline optimization
- Comprehensive compatibility and acquisition tools

### v1.0.0
- Basic move lookup by Revomon
- Simple learning method filtering
- Basic level progression queries

---

**Ready to master the complete move learning system and optimize your Revomon's potential? Let the learning analysis begin!** 📚🎓⚔️
