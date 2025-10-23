# MovesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive move database client for Revomon, providing access to all combat moves including damage, accuracy, effects, and strategic analysis for optimal team building and battle strategies.

## ⚔️ Overview

The MovesClient provides complete access to the Revomon combat system through:

- **500+ Combat moves** with full statistical data
- **18+ Move types** with elemental properties and interactions
- **3 Move categories**: Physical, Special, and Status moves
- **Priority system** for speed control and turn manipulation
- **PP management** for battle sustainability
- **Move analysis** for competitive team optimization

This client is essential for battle simulation, team building, and understanding the complete Revomon combat meta.

## 📊 Move Data Structure

Each move contains comprehensive combat information:

### Core Combat Stats
- **`id`** - Unique move identifier (primary key)
- **`name`** - Move name
- **`category`** - Move type: "physical", "special", or "status"
- **`type`** - Elemental type (fire, water, ground, etc.)
- **`description`** - Move effects and mechanics description

### Damage & Accuracy
- **`power`** - Base damage potential (0 for status moves, 1-250+ for attacks)
- **`accuracy`** - Hit probability (0.0 to 1.0, where 1.0 = 100% accurate)
- **`pp`** - Power Points (uses per battle, typically 5-40)
- **`priority`** - Turn order control (-7 to +7, 0 = normal speed)

### Advanced Mechanics
- **`crit_rate`** - Critical hit probability modifier
- **`flinch_chance`** - Chance to prevent opponent action
- **`stat_changes`** - Stat modifications applied
- **`status_effects`** - Status conditions inflicted
- **`recoil`** - Self-damage percentage (if applicable)

## 🚀 Quick Start

### Basic Move Lookup

```python
from revomonauto.revomon.clients import MovesClient

# Initialize client
moves_client = MovesClient()

# Get move by name
earthquake = moves_client.get_move_by_name("earthquake")
print(f"Earthquake: {earthquake['power']} power, {earthquake['type']} type")
print(f"Category: {earthquake['category']}, PP: {earthquake['pp']}")

# Get move by ID
move_123 = moves_client.get_move_by_id(123)
print(f"Move #{move_123['id']}: {move_123['name']}")
```

### Category-Based Queries

```python
# Get all moves by category
physical_moves = moves_client.get_physical_moves()
special_moves = moves_client.get_special_moves()
status_moves = moves_client.get_status_moves()

print(f"Physical moves: {len(physical_moves)}")
print(f"Special moves: {len(special_moves)}")
print(f"Status moves: {len(status_moves)}")

# Get moves by type
fire_moves = moves_client.get_moves_by_type("fire")
water_moves = moves_client.get_moves_by_type("water")
print(f"Fire moves: {len(fire_moves)}, Water moves: {len(water_moves)}")
```

### Power & Performance Analysis

```python
# Find high-power moves
nuclear_moves = moves_client.get_high_power_moves(120)  # 120+ power
print(f"Nuclear moves: {len(nuclear_moves)}")
for move in nuclear_moves[:5]:
    print(f"  {move['name']}: {move['power']} power")

# Find priority moves (speed control)
first_strike = moves_client.get_first_strike_moves()
print(f"Priority moves: {len(first_strike)}")

# Find reliable moves (100% accuracy)
perfect_moves = moves_client.get_always_hit_moves()
print(f"Perfect accuracy moves: {len(perfect_moves)}")
```

## 📚 API Reference

### Core Query Methods

#### `get_move_by_id(move_id)`

Get move data by unique ID.

**Parameters:**
- `move_id` (int): The move ID

**Returns:** Move data dictionary or None if not found

#### `get_move_by_name(name)`

Get move data by move name.

**Parameters:**
- `name` (str): The move name

**Returns:** Move data dictionary or None if not found

### Category & Type Queries

#### `get_moves_by_type(move_type)`

Get all moves of a specific elemental type.

**Parameters:**
- `move_type` (str): Elemental type (fire, water, ground, etc.)

**Returns:** List of moves of the specified type

#### `get_moves_by_category(category)`

Get all moves of a specific category.

**Parameters:**
- `category` (str): Move category ("physical", "special", "status")

**Returns:** List of moves of the specified category

#### `get_physical_moves()`, `get_special_moves()`, `get_status_moves()`

Get all moves of specific categories (convenience methods).

### Performance Queries

#### `get_moves_by_power_range(min_power, max_power)`

Get moves within a power range.

**Parameters:**
- `min_power` (int): Minimum power
- `max_power` (int): Maximum power

**Returns:** List of moves within the power range

#### `get_high_power_moves(min_power=100)`

Get moves above a power threshold.

**Parameters:**
- `min_power` (int): Minimum power threshold

**Returns:** List of high-power moves

#### `get_low_pp_moves(max_pp=10)`

Get moves with low PP (limited uses).

**Parameters:**
- `max_pp` (int): Maximum PP threshold

**Returns:** List of moves with limited uses

### Speed Control Queries

#### `get_priority_moves(priority=1)`

Get moves with specific priority.

**Parameters:**
- `priority` (int): Priority level (positive = goes first)

**Returns:** List of moves with the specified priority

#### `get_first_strike_moves()`

Get moves that always go first (priority > 0).

**Returns:** List of priority moves

#### `get_last_resort_moves()`

Get moves that always go last (priority < 0).

**Returns:** List of moves with negative priority

### Accuracy & Reliability

#### `get_inaccurate_moves(max_accuracy=0.8)`

Get moves with low accuracy.

**Parameters:**
- `max_accuracy` (float): Maximum accuracy threshold

**Returns:** List of moves with low hit rates

#### `get_always_hit_moves()`

Get moves with perfect accuracy (100%).

**Returns:** List of moves that never miss

### Analysis & Meta

#### `get_move_type_distribution()`

Get distribution of moves by elemental type.

**Returns:** Dictionary mapping move types to counts

#### `get_moves_with_description_keyword(keyword)`

Search moves by description keywords.

**Parameters:**
- `keyword` (str): Keyword to search for

**Returns:** List of moves containing the keyword

## 🎮 Usage Examples

### Example 1: Team Move Analysis

```python
from revomonauto.revomon.clients import MovesClient

moves_client = MovesClient()

# Analyze move distribution for team building
def analyze_move_meta():
    # Get move type distribution
    type_dist = moves_client.get_move_type_distribution()
    print(f"Most common move type: {max(type_dist, key=type_dist.get)}")

    # Find best coverage moves
    high_power_moves = moves_client.get_high_power_moves(100)
    print(f"High power moves: {len(high_power_moves)}")

    # Find reliable moves
    reliable_moves = moves_client.get_always_hit_moves()
    print(f"Perfect accuracy moves: {len(reliable_moves)}")

    # Find speed control
    priority_moves = moves_client.get_first_strike_moves()
    print(f"Priority moves: {len(priority_moves)}")

analyze_move_meta()
```

### Example 2: Type Coverage Optimization

```python
# Find optimal type coverage moves
def find_coverage_moves():
    coverage_moves = []

    # Get one strong move per type for coverage
    move_types = moves_client.get_move_type_distribution().keys()

    for move_type in move_types:
        type_moves = moves_client.get_moves_by_type(move_type)
        if type_moves:
            # Get strongest physical attack of this type
            strongest = max(type_moves,
                          key=lambda x: x.get('power', 0) if x.get('category') == 'physical' else 0)
            if strongest.get('power', 0) > 0:
                coverage_moves.append(strongest)

    return coverage_moves

coverage = find_coverage_moves()
print(f"Type coverage moves: {len(coverage)}")
for move in coverage[:5]:
    print(f"  {move['name']} ({move['type']}): {move['power']} power")
```

### Example 3: Speed Control Analysis

```python
# Analyze speed control options
def analyze_speed_control():
    speed_options = {
        'first_strike': moves_client.get_first_strike_moves(),
        'last_resort': moves_client.get_last_resort_moves(),
        'perfect_accuracy': moves_client.get_always_hit_moves(),
        'low_pp': moves_client.get_low_pp_moves(10)
    }

    print("=== Speed Control Analysis ===")
    for category, moves in speed_options.items():
        print(f"{category.replace('_', ' ').title()}: {len(moves)} moves")

        # Show best examples
        if moves:
            best = moves[0]
            print(f"  Example: {best['name']} (Priority: {best.get('priority', 0)})")

analyze_speed_control()
```

### Example 4: Competitive Move Pool Analysis

```python
# Analyze competitive move pools
def analyze_competitive_moves():
    # Find moves that are competitively viable
    competitive_criteria = {
        'high_power': moves_client.get_high_power_moves(90),
        'perfect_accuracy': moves_client.get_always_hit_moves(),
        'priority': moves_client.get_first_strike_moves(),
        'efficient': moves_client.get_moves_by_power_range(70, 100)  # Balanced power
    }

    print("=== Competitive Move Analysis ===")
    for category, moves in competitive_criteria.items():
        print(f"{category.replace('_', ' ').title()}: {len(moves)} moves")

        # Show category breakdown
        type_dist = {}
        for move in moves:
            move_type = move.get('type', 'unknown')
            type_dist[move_type] = type_dist.get(move_type, 0) + 1

        print(f"  Type distribution: {dict(list(type_dist.items())[:5])}")

analyze_competitive_moves()
```

## 🏆 Advanced Move Analysis

### Move Efficiency Metrics

```python
# Calculate move efficiency scores
def calculate_move_efficiency(move):
    efficiency = 0

    # Power efficiency (0-100)
    power = move.get('power', 0)
    pp = move.get('pp', 1)
    power_per_pp = power / pp
    efficiency += min(power_per_pp * 2, 50)  # Cap at 50

    # Accuracy bonus
    accuracy = move.get('accuracy', 1.0)
    if accuracy >= 1.0:
        efficiency += 20  # Perfect accuracy bonus
    elif accuracy >= 0.9:
        efficiency += 10  # High accuracy bonus

    # Priority bonus
    priority = move.get('priority', 0)
    if priority > 0:
        efficiency += priority * 15  # Priority bonus
    elif priority < 0:
        efficiency -= abs(priority) * 10  # Priority penalty

    # STAB potential (if type matches user)
    if move.get('category') in ['physical', 'special']:
        efficiency += 10  # STAB potential

    return min(efficiency, 100)  # Cap at 100

# Analyze most efficient moves
all_moves = moves_client.get_all()
efficient_moves = [(move, calculate_move_efficiency(move)) for move in all_moves]
efficient_moves.sort(key=lambda x: x[1], reverse=True)

print("Most Efficient Moves:")
for move, efficiency in efficient_moves[:10]:
    print(f"{move['name']}: {efficiency:.1f}/100 efficiency")
```

### Move Meta Analysis

```python
# Analyze move usage patterns
def analyze_move_meta():
    total_moves = len(moves_client.get_all())

    # Category distribution
    categories = {
        'physical': len(moves_client.get_physical_moves()),
        'special': len(moves_client.get_special_moves()),
        'status': len(moves_client.get_status_moves())
    }

    # Type distribution
    type_dist = moves_client.get_move_type_distribution()

    # Power distribution
    power_ranges = {
        'low': len(moves_client.get_moves_by_power_range(0, 60)),
        'medium': len(moves_client.get_moves_by_power_range(61, 100)),
        'high': len(moves_client.get_moves_by_power_range(101, 150)),
        'nuclear': len(moves_client.get_moves_by_power_range(151, 999))
    }

    print("=== Move Meta Analysis ===")
    print(f"Total moves: {total_moves}")
    print(f"Category distribution: {categories}")
    print(f"Type distribution: {dict(list(type_dist.items())[:5])}")
    print(f"Power distribution: {power_ranges}")

analyze_move_meta()
```

## 📈 Performance

- **Fast queries**: Indexed by ID and name for instant access
- **Cached data**: Move database loaded once and cached
- **Batch analysis**: Support for analyzing large move sets efficiently
- **Memory optimized**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run moves client tests
uv run python -m pytest tests/clients/test_moves_client.py

# Test move analysis
uv run python tests/integration/test_move_analysis.py

# Performance benchmarks
uv run python tests/performance/test_move_queries.py
```

## 🤝 Contributing

1. Ensure all move data is accurate to game mechanics
2. Add comprehensive tests for new analysis methods
3. Update move effectiveness when balance changes occur
4. Document any meta analysis changes with sources

## 🔄 Version History

### v2.0.0
- Complete move database with 500+ moves
- Advanced filtering and analysis capabilities
- Speed control and priority move analysis
- Competitive move efficiency metrics
- Comprehensive meta analysis tools

### v1.0.0
- Basic move lookup by ID and name
- Simple category and type filtering
- Basic power and accuracy queries

---

**Ready to master the complete Revomon combat system? Let the move analysis begin!** ⚔️📊🎯
