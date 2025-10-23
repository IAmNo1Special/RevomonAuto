# EvolutionClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Advanced evolution chain analysis and optimization system for Revomon, providing complete evolution trees, efficiency analysis, and competitive meta insights for strategic evolution planning.

## 🌳 Overview

The EvolutionClient provides comprehensive evolution analysis including:

- **Complete evolution trees** with branching paths and statistics
- **Evolution path optimization** for desired stat distributions and types
- **Efficiency analysis** with stat growth calculations and progression metrics
- **Evolution requirements** tracking with levels and conditions
- **Competitive meta analysis** for evolution patterns and strategies
- **Breeding optimization** and evolution chain recommendations

## ✨ Features

### Evolution Tree Analysis
- **Complete Trees**: Build full evolution trees including all branching paths
- **Path Finding**: Find shortest evolution paths between any two Revomon
- **Branch Statistics**: Analyze stat totals, types, and rarities for each branch
- **Tree Metrics**: Total members, stat ranges, and diversity analysis

### Optimization & Strategy
- **Optimal Paths**: Find evolution paths that maximize desired characteristics
- **Efficiency Scoring**: Score evolution chains based on stat growth and type matches
- **Meta Analysis**: Analyze evolution patterns across the entire Revomon ecosystem
- **Gap Detection**: Identify potential missing evolution stages

### Requirements & Planning
- **Evolution Requirements**: Detailed requirements for each evolution
- **Level Tracking**: Evolution levels and progression planning
- **Method Detection**: Identify evolution methods (level, items, conditions)
- **Chain Analysis**: Complete analysis of evolution chains with efficiency metrics

## 🚀 Quick Start

### Basic Evolution Tree

```python
from revomonauto.revomon.clients import EvolutionClient, RevomonClient

# Initialize clients
evolution_client = EvolutionClient()
revomon_client = RevomonClient()

# Get complete evolution tree
tree = evolution_client.get_complete_evolution_tree(1)  # Start with Dekute
print(f"Evolution tree has {tree['total_members']} members")
print(f"Branches: {len(tree['branches'])}")

# Explore branches
for branch in tree['branches']:
    print(f"Branch: {branch['parent']['name']} -> {len(branch['children'])} evolutions")
    print(f"Avg stats: {branch['branch_stats']['avg_stat_total']}")
```

### Evolution Path Optimization

```python
# Find optimal evolution paths for specific goals
target_stats = {"atk": 1.0, "spe": 0.8, "spa": 0.6}
target_types = ["fire", "dragon"]

optimal_paths = evolution_client.find_optimal_evolution_path(
    target_stats=target_stats,
    target_types=target_types,
    max_evolutions=3
)

for path in optimal_paths[:5]:  # Top 5 paths
    chain = path['chain']
    print(f"Path score: {path['score']}")
    print(f"Evolution chain: {' -> '.join(r['name'] for r in chain)}")
```

### Evolution Requirements

```python
# Get evolution requirements for a specific Revomon
requirements = evolution_client.get_evolution_requirements(25)

if requirements['can_evolve']:
    print(f"Evolution method: {requirements['evolution_method']}")
    print(f"Evolved form: {requirements['evolved_form']['name']}")

    for req in requirements['requirements']:
        print(f"- {req['description']}")
else:
    print(f"{requirements['current_revomon']['name']} does not evolve")
```

## 📚 API Reference

### Core Methods

#### `get_complete_evolution_tree(start_dex_id)`

Get complete evolution tree starting from a Revomon.

**Parameters:**
- `start_dex_id` (int): Starting Pokedex ID

**Returns:** Complete evolution tree with branches, statistics, and all members

#### `find_optimal_evolution_path(target_stats=None, target_types=None, max_evolutions=3)`

Find evolution paths optimized for specific criteria.

**Parameters:**
- `target_stats` (dict): Desired stat distribution (e.g., {"atk": 1.0, "spe": 0.8})
- `target_types` (list): Desired types to evolve into
- `max_evolutions` (int): Maximum evolution stages to consider

**Returns:** List of optimal evolution paths sorted by score

#### `analyze_evolution_efficiency(evolution_chain)`

Analyze efficiency of an evolution chain.

**Parameters:**
- `evolution_chain` (list): List of Revomon in evolution order

**Returns:** Efficiency analysis with stat growth, type changes, and metrics

#### `get_evolution_requirements(dex_id)`

Get detailed evolution requirements for a Revomon.

**Parameters:**
- `dex_id` (int): Pokedex ID

**Returns:** Evolution requirements and conditions

#### `get_evolution_path(start_dex_id, end_dex_id)`

Find shortest evolution path between two Revomon.

**Parameters:**
- `start_dex_id` (int): Starting Pokedex ID
- `end_dex_id` (int): Ending Pokedex ID

**Returns:** List of Revomon in evolution path, or None if no path

### Analysis Methods

#### `analyze_evolution_meta()`

Analyze evolution patterns for competitive meta insights.

**Returns:** Meta analysis including chain lengths, progression patterns, and statistics

#### `find_evolution_gaps()`

Find potential gaps in evolution chains where intermediate forms might be missing.

**Returns:** List of evolution gaps with stat differences and gap analysis

## 🎯 Usage Examples

### Example 1: Complete Evolution Analysis

```python
from revomonauto.revomon.clients import EvolutionClient

evolution_client = EvolutionClient()

# Analyze a complete evolution tree
tree = evolution_client.get_complete_evolution_tree(1)

print(f"=== {tree['root']['name']} Evolution Tree ===")
print(f"Total members: {tree['total_members']}")
print(f"Tree branches: {len(tree['branches'])}")
print(f"Average stats: {tree['tree_stats']['avg_stat_total']}")
print(f"Stat range: {tree['tree_stats']['min_stat_total']} - {tree['tree_stats']['max_stat_total']}")
print(f"Unique types: {tree['tree_stats']['unique_types']}")
```

### Example 2: Evolution Path Optimization

```python
# Find best evolution paths for a sweeper build
sweeper_stats = {
    "atk": 1.0,    # High attack priority
    "spe": 0.9,    # High speed priority
    "spa": 0.3,    # Lower special attack
    "hp": 0.4,     # Moderate HP
    "def": 0.2,    # Lower defense
    "spd": 0.2     # Lower special defense
}

fire_sweeper_types = ["fire", "dragon", "electric"]

best_paths = evolution_client.find_optimal_evolution_path(
    target_stats=sweeper_stats,
    target_types=fire_sweeper_types,
    max_evolutions=3
)

for i, path in enumerate(best_paths[:3], 1):
    print(f"\n{i}. Best Path (Score: {path['score']})")
    chain = path['chain']
    for j, revomon in enumerate(chain):
        if j > 0:
            print(f"   ↓ (Level {revomon.get('evo_lvl', '?')})")
        print(f"   {revomon['name']} - Total: {revomon.get('stat_total', 0)}")
```

### Example 3: Evolution Requirements Planning

```python
# Plan evolution requirements for team building
target_revomon = [1, 5, 10, 15, 20, 25]  # Example dex IDs

for dex_id in target_revomon:
    req = evolution_client.get_evolution_requirements(dex_id)

    print(f"\n{req['current_revomon']['name']}:")
    if req['can_evolve']:
        print(f"  → Evolves to: {req['evolved_form']['name']}")
        print(f"  Method: {req['evolution_method']}")
        for requirement in req['requirements']:
            print(f"  • {requirement['description']}")
    else:
        print("  Does not evolve")
```

### Example 4: Meta Evolution Analysis

```python
# Analyze evolution patterns across the ecosystem
meta = evolution_client.analyze_evolution_meta()

print("=== Evolution Meta Analysis ===")
print(f"Total evolution trees: {meta['total_evolution_trees']}")
print(f"Average chain length: {meta['avg_chain_length']:.1f}")

print("\nEvolution Trees by Length:")
for length, count in sorted(meta['trees_by_length'].items()):
    print(f"  {length} stages: {count} trees")

print("\nTop Stat Progression Patterns:")
for tree in meta['stat_progression_patterns'][:3]:
    print(f"\n{tree['tree']} Tree:")
    for step in tree['progression']:
        growth_pct = step['growth_percentage']
        print(f"  {step['from']} → {step['to']}: +{growth_pct:.1f}% growth")
```

## 🔍 Advanced Features

### Custom Evolution Scoring

```python
# Custom scoring weights for specific strategies
def custom_evolution_scorer(chain, strategy="balanced"):
    score = 0.0

    if strategy == "sweeper":
        # Prioritize attack and speed
        final_stats = chain[-1]
        score += final_stats.get('atk', 0) * 0.4
        score += final_stats.get('spe', 0) * 0.4
        score += final_stats.get('spa', 0) * 0.2

    elif strategy == "tank":
        # Prioritize HP and defenses
        final_stats = chain[-1]
        score += final_stats.get('hp', 0) * 0.4
        score += final_stats.get('def', 0) * 0.3
        score += final_stats.get('spd', 0) * 0.3

    return score

# Use custom scoring in path finding
# (Implementation would need to be extended in the client)
```

### Evolution Gap Analysis

```python
# Find potential missing evolution stages
gaps = evolution_client.find_evolution_gaps()

print("Potential Missing Evolutions:")
for gap in gaps[:10]:  # Top 10 gaps
    if gap['potential_missing_evolution']:
        print(f"{gap['from']} → {gap['to']}")
        print(f"  Stat gap: {gap['stat_gap']} ({gap['gap_percentage']:.1f}%)")
        print("  → LIKELY missing evolution stage!")
```

## 📊 Performance

- **Efficient tree building**: Optimized breadth-first search algorithms
- **Cached calculations**: Stat calculations and path finding cached
- **Batch processing**: Support for analyzing multiple evolution trees
- **Memory optimized**: Minimal memory usage for large evolution trees

## 🧪 Testing

```bash
# Run evolution tests
uv run python -m pytest tests/clients/test_evolution_client.py

# Test evolution path finding
uv run python tests/integration/test_evolution_paths.py

# Performance benchmarks
uv run python tests/performance/test_evolution_analysis.py
```

## 🤝 Contributing

1. Ensure evolution trees are accurate and complete
2. Add tests for new evolution mechanics
3. Update meta analysis when new evolution patterns are discovered
4. Document evolution requirements with sources

## 🔄 Version History

### v2.0.0
- Complete evolution tree analysis with branching paths
- Evolution path optimization and scoring
- Meta analysis of evolution patterns
- Evolution gap detection and analysis
- Comprehensive efficiency metrics

### v1.0.0
- Basic evolution chain lookup
- Simple evolution requirements
- Individual evolution path finding

---

**Ready to evolve your Revomon strategy? Let the evolution analysis begin!** 🌳✨🔬
