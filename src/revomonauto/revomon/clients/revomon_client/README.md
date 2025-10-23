# RevomonClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

The core database client for Revomon species data, providing comprehensive access to all Revomon creatures in the game including stats, types, abilities, evolution chains, and spawn information.

## 🦴 Overview

The RevomonClient is the **central database** of the Revomon universe, containing complete information about every Revomon species including:

- **Complete Pokedex data** with stats, types, and abilities
- **Evolution chains** and progression paths
- **Spawn locations** and encounter rates
- **Type distribution** and statistical analysis
- **Competitive viability** metrics and rankings

This client serves as the foundation for all other clients in the Revomon ecosystem, providing the core data that powers team building, battle analysis, and strategic planning.

## 📊 Data Structure

Each Revomon record contains comprehensive information:

### Core Information
- **`dex_id`** - Unique Pokedex number (primary key)
- **`name`** - Revomon species name
- **`rarity`** - Rarity tier (common, uncommon, rare, legendary, shiny)

### Battle Stats (0-255 range)
- **`hp`** - Health Points (determines survival capability)
- **`atk`** - Attack (physical damage potential)
- **`def`** - Defense (physical damage resistance)
- **`spa`** - Special Attack (special damage potential)
- **`spd`** - Special Defense (special damage resistance)
- **`spe`** - Speed (turn order determination)

### Type System (18+ types)
- **`type1`** - Primary elemental type
- **`type2`** - Secondary elemental type (optional)

### Ability System
- **`ability1`** - First regular ability
- **`ability2`** - Second regular ability (optional)
- **`abilityh`** - Hidden ability (rare, optional)

### Evolution & Growth
- **`evo`** - Name of evolved form (if applicable)
- **`evo_lvl`** - Level required for evolution
- **`evo_tree`** - Evolution family grouping
- **`stat_total`** - Sum of all base stats (competitive viability indicator)

### World Integration
- **`spawn_locations`** - Where the Revomon can be found
- **`spawn_times`** - When the Revomon appears
- **`spawn_rates`** - Encounter probability
- **`image_urls`** - Various sprite and 3D model assets

## 🚀 Quick Start

### Basic Species Lookup

```python
from revomonauto.revomon.clients import RevomonClient

# Initialize client
revomon_client = RevomonClient()

# Get Revomon by name
gorcano = revomon_client.get_revomon_by_name("gorcano")
print(f"Gorcano stats: {gorcano['stat_total']} total")
print(f"Types: {gorcano['type1']}/{gorcano.get('type2', 'None')}")

# Get by Pokedex ID
starter = revomon_client.get_revomon_by_id(1)
print(f"Starter Revomon: {starter['name']}")
```

### Type-Based Queries

```python
# Find all Fire-type Revomon
fire_types = revomon_client.get_revomon_by_type("fire")
print(f"Fire-type Revomon: {len(fire_types)}")

# Find dual-type Revomon
fire_water_types = revomon_client.get_revomon_by_type("fire", "water")
print(f"Fire/Water dual types: {len(fire_water_types)}")

# Get type distribution
type_distribution = revomon_client.get_revomon_type_distribution()
print(f"Most common type: {max(type_distribution, key=type_distribution.get)}")
```

### Evolution Chain Analysis

```python
# Get complete evolution chain
chain = revomon_client.get_evolution_chain(1)  # Start with first Revomon
for revomon in chain:
    print(f"{revomon['name']} (Total: {revomon['stat_total']})")

# Find Revomon by ability
ability_users = revomon_client.get_revomon_by_ability("overgrow")
print(f"Revomon with Overgrow: {[r['name'] for r in ability_users]}")
```

## 📚 API Reference

### Core Query Methods

#### `get_revomon_by_id(dex_id)`

Get Revomon data by Pokedex ID.

**Parameters:**
- `dex_id` (int): The Pokedex ID

**Returns:** Revomon data dictionary or None if not found

#### `get_revomon_by_name(name)`

Get Revomon data by species name.

**Parameters:**
- `name` (str): The Revomon name

**Returns:** Revomon data dictionary or None if not found

#### `get_revomon_names()`

Get all Revomon species names.

**Returns:** List of all Revomon names in the database

### Type & Attribute Queries

#### `get_revomon_by_type(type1, type2=None)`

Get Revomon with specific type(s).

**Parameters:**
- `type1` (str): Primary type to search for
- `type2` (str, optional): Secondary type to search for

**Returns:** List of matching Revomon

#### `get_revomon_by_ability(ability)`

Get Revomon with a specific ability.

**Parameters:**
- `ability` (str): Ability name (ability1, ability2, or abilityh)

**Returns:** List of Revomon with the specified ability

#### `get_revomon_by_rarity(rarity)`

Get Revomon by rarity tier.

**Parameters:**
- `rarity` (str): Rarity level (common, uncommon, rare, legendary, shiny)

**Returns:** List of Revomon with the specified rarity

### Statistical Queries

#### `get_revomon_by_stat_total_range(min_total, max_total)`

Get Revomon within a stat total range.

**Parameters:**
- `min_total` (int): Minimum stat total
- `max_total` (int): Maximum stat total

**Returns:** List of Revomon within the range

#### `get_highest_stat_total(limit=10)`

Get Revomon with the highest stat totals (most powerful).

**Parameters:**
- `limit` (int): Number of results to return

**Returns:** List of Revomon sorted by stat total (highest first)

#### `get_lowest_stat_total(limit=10)`

Get Revomon with the lowest stat totals (least powerful).

**Parameters:**
- `limit` (int): Number of results to return

**Returns:** List of Revomon sorted by stat total (lowest first)

### Evolution Analysis

#### `get_evolution_chain(dex_id)`

Get the complete evolution chain for a Revomon.

**Parameters:**
- `dex_id` (int): Starting Pokedex ID

**Returns:** List of Revomon in the evolution chain (base → mid → final)

### Meta Analysis

#### `get_revomon_type_distribution()`

Get distribution of Revomon by primary type.

**Returns:** Dictionary mapping type names to counts

## 🎯 Usage Examples

### Example 1: Team Building Analysis

```python
from revomonauto.revomon.clients import RevomonClient

client = RevomonClient()

# Analyze type coverage for team building
def analyze_type_coverage():
    # Get representatives of each type
    type_representatives = {}
    type_distribution = client.get_revomon_type_distribution()

    for type_name in type_distribution.keys():
        # Get strongest Revomon of each type
        type_members = client.get_revomon_by_type(type_name)
        strongest = max(type_members, key=lambda x: x.get('stat_total', 0))
        type_representatives[type_name] = strongest

    return type_representatives

# Build balanced team
coverage = analyze_type_coverage()
balanced_team = list(coverage.values())[:6]  # First 6 types
```

### Example 2: Competitive Analysis

```python
# Find top competitive Revomon
top_revomon = client.get_highest_stat_total(20)

print("=== Top 20 Competitive Revomon ===")
for i, revomon in enumerate(top_revomon, 1):
    print(f"{i:2d}. {revomon['name']:15} "
          f"Total: {revomon['stat_total']:3d} "
          f"Type: {revomon['type1']}/{revomon.get('type2', '   ')}")
```

### Example 3: Evolution Planning

```python
# Plan evolution paths for team
def plan_evolution_strategy(target_types, min_stats=400):
    candidates = []

    for type1 in target_types:
        # Find Revomon that evolve into the target type
        type_members = client.get_revomon_by_type(type1)
        for revomon in type_members:
            if revomon.get('stat_total', 0) >= min_stats:
                chain = client.get_evolution_chain(revomon['dex_id'])
                if len(chain) > 1:  # Has evolution potential
                    candidates.append({
                        'base': chain[0],
                        'final': chain[-1],
                        'growth': chain[-1]['stat_total'] - chain[0]['stat_total']
                    })

    # Sort by stat growth (most improvement)
    candidates.sort(key=lambda x: x['growth'], reverse=True)
    return candidates

# Find best Fire-type evolution paths
fire_evolution = plan_evolution_strategy(['fire'])
```

### Example 4: Rarity Hunting Strategy

```python
# Analyze rarity distribution for hunting
rarity_analysis = {}
for rarity in ['common', 'uncommon', 'rare', 'legendary']:
    rare_revomon = client.get_revomon_by_rarity(rarity)
    rarity_analysis[rarity] = {
        'count': len(rare_revomon),
        'avg_stats': sum(r.get('stat_total', 0) for r in rare_revomon) / len(rare_revomon),
        'strongest': max(rare_revomon, key=lambda x: x.get('stat_total', 0))['name']
    }

for rarity, data in rarity_analysis.items():
    print(f"{rarity.capitalize()}: {data['count']} species, "
          f"avg stats: {data['avg_stats']:.1f}, "
          f"strongest: {data['strongest']}")
```

## 🏆 Advanced Features

### Statistical Analysis

```python
# Comprehensive stat analysis
def analyze_stat_distribution():
    all_stats = []
    for revomon in client.get_all():
        stats = {
            'name': revomon['name'],
            'total': revomon['stat_total'],
            'hp': revomon['hp'],
            'atk': revomon['atk'],
            'def': revomon['def'],
            'spa': revomon['spa'],
            'spd': revomon['spd'],
            'spe': revomon['spe']
        }
        all_stats.append(stats)

    # Find stat specialists
    attackers = sorted(all_stats, key=lambda x: x['atk'], reverse=True)[:10]
    speedsters = sorted(all_stats, key=lambda x: x['spe'], reverse=True)[:10]
    tanks = sorted(all_stats, key=lambda x: x['hp'] + x['def'], reverse=True)[:10]

    return {
        'top_attackers': attackers,
        'top_speedsters': speedsters,
        'top_tanks': tanks
    }

analysis = analyze_stat_distribution()
print(f"Top attacker: {analysis['top_attackers'][0]['name']} (ATK: {analysis['top_attackers'][0]['atk']})")
```

### Evolution Meta Analysis

```python
# Analyze evolution patterns across the ecosystem
def analyze_evolution_meta():
    evolution_trees = {}
    growth_patterns = []

    for revomon in client.get_all():
        if revomon.get('evo_tree'):
            tree = revomon['evo_tree']
            if tree not in evolution_trees:
                evolution_trees[tree] = []
            evolution_trees[tree].append(revomon)

    for tree_name, members in evolution_trees.items():
        if len(members) > 1:
            # Sort by stat total
            sorted_members = sorted(members, key=lambda x: x['stat_total'])
            total_growth = sorted_members[-1]['stat_total'] - sorted_members[0]['stat_total']
            growth_percentage = (total_growth / sorted_members[0]['stat_total']) * 100

            growth_patterns.append({
                'tree': tree_name,
                'members': len(members),
                'growth': total_growth,
                'growth_percentage': growth_percentage,
                'stages': [r['name'] for r in sorted_members]
            })

    # Sort by growth efficiency
    growth_patterns.sort(key=lambda x: x['growth_percentage'], reverse=True)
    return growth_patterns

evolution_meta = analyze_evolution_meta()
print("Most efficient evolution trees:")
for tree in evolution_meta[:5]:
    print(f"  {tree['tree']}: {tree['growth_percentage']:.1f}% stat growth")
```

## 📈 Performance

- **Fast lookups**: Indexed by Pokedex ID and name for instant access
- **Cached data**: Loaded once and cached for subsequent queries
- **Memory efficient**: Data is copied to prevent mutation
- **Batch operations**: Support for bulk queries and analysis

## 🧪 Testing

```bash
# Run Revomon client tests
uv run python -m pytest tests/clients/test_revomon_client.py

# Test evolution chains
uv run python tests/integration/test_evolution_chains.py

# Performance benchmarks
uv run python tests/performance/test_revomon_queries.py
```

## 🤝 Contributing

1. Ensure all Revomon data is accurate and complete
2. Add comprehensive tests for new query methods
3. Update evolution chains when new Revomon are added
4. Document any data structure changes

## 🔄 Version History

### v2.0.0
- Complete evolution chain analysis
- Advanced statistical queries and rankings
- Type distribution and meta analysis
- Comprehensive filtering and search capabilities

### v1.0.0
- Basic Revomon lookup by ID and name
- Simple type and ability filtering
- Basic stat total queries

---

**Ready to explore the complete Revomon universe? Let the species analysis begin!** 🦴📊🔬
