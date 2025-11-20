# NaturesClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Nature system client for Revomon, providing access to stat modification mechanics, flavor preferences, and competitive optimization tools for perfect IV breeding and team building.

## 🌿 Overview

The NaturesClient provides the complete nature system that powers Revomon stat optimization:

- **25 Nature variations** with stat buffs and debuffs
- **5 Flavor preferences** (spicy, sour, sweet, dry, bitter) that affect happiness and evolution
- **Competitive optimization** for perfect stat distribution
- **Neutral natures** for flexible builds without stat penalties
- **Stat targeting** for specialized team roles (sweeper, tank, support)

This client is essential for competitive Revomon breeding, team optimization, and understanding the statistical meta of the game.

## 📊 Nature Data Structure

Each nature contains comprehensive stat modification and flavor information:

### Stat Modifications
- **`buffs`** - Stat that gets +10% boost (null if neutral nature)
- **`debuffs`** - Stat that gets -10% penalty (null if neutral nature)
- **5 Neutral natures** - No stat changes (bashful, docile, hardy, quirky, serious)

### Flavor System
- **`likes`** - Flavor that increases happiness when fed
- **`dislikes`** - Flavor that decreases happiness when fed
- **Happiness impact** - Affects evolution requirements and battle performance

## 🚀 Quick Start

### Basic Nature Lookup

```python
from revomonauto.revomon.clients import NaturesClient

# Initialize client
natures_client = NaturesClient()

# Get nature by name
adamant = natures_client.get_nature("adamant")
print(f"Adamant: +{adamant['buffs']} -{adamant['debuffs']}")
print(f"Likes: {adamant['likes']}, Dislikes: {adamant['dislikes']}")

# Get all speed-boosting natures
speed_natures = natures_client.get_speed_boosting_natures()
print(f"Speed natures: {[n['name'] for n in speed_natures]}")

# Get all attack-boosting natures
attack_natures = natures_client.get_attack_boosting_natures()
print(f"Attack natures: {[n['name'] for n in attack_natures]}")
```

### Competitive Nature Analysis

```python
# Get stat-buffing vs neutral natures
buff_natures = natures_client.get_natures_with_stat_buffs()
neutral_natures = natures_client.get_neutral_natures()

print(f"Natures with buffs: {len(buff_natures)}")
print(f"Neutral natures: {len(neutral_natures)}")

# Find natures that buff specific stats
defense_natures = natures_client.get_natures_by_buffed_stat("def")
special_attack_natures = natures_client.get_natures_by_buffed_stat("spa")

print(f"Defense-boosting: {[n['name'] for n in defense_natures]}")
print(f"Sp. Attack-boosting: {[n['name'] for n in special_attack_natures]}")
```

## 📚 API Reference

### Core Query Methods

#### `get_nature(nature_name)`

Get nature data by name.

**Parameters:**
- `nature_name` (str): The nature name

**Returns:** Nature data dictionary or None if not found

#### `get_natures_with_stat_buffs()`

Get all natures that provide stat modifications.

**Returns:** List of natures with stat buffs/debuffs

#### `get_neutral_natures()`

Get neutral natures (no stat changes).

**Returns:** List of neutral natures

### Stat-Specific Queries

#### `get_natures_by_buffed_stat(stat)`

Get natures that boost a specific stat.

**Parameters:**
- `stat` (str): Stat name (hp, atk, def, spa, spd, spe)

**Returns:** List of natures that buff the specified stat

#### `get_natures_by_debuffed_stat(stat)`

Get natures that penalize a specific stat.

**Parameters:**
- `stat` (str): Stat name (hp, atk, def, spa, spd, spe)

**Returns:** List of natures that debuff the specified stat

#### `get_speed_boosting_natures()`, `get_attack_boosting_natures()`

Get natures that boost speed or attack (convenience methods).

**Returns:** List of speed/attack-boosting natures

### Flavor System Queries

#### `get_natures_by_flavor_preference(flavor, preference_type="likes")`

Get natures by flavor preference.

**Parameters:**
- `flavor` (str): Flavor (spicy, sour, sweet, dry, bitter)
- `preference_type` (str): "likes" or "dislikes"

**Returns:** List of natures with the specified flavor preference

## 🎮 Usage Examples

### Example 1: Perfect IV Breeding Guide

```python
from revomonauto.revomon.clients import NaturesClient

natures_client = NaturesClient()

# Create breeding guide for competitive stats
def create_breeding_guide():
    breeding_targets = {
        'speed_sweeper': 'spe',      # Jolly/Timid - speed focus
        'physical_attacker': 'atk',  # Adamant - attack focus
        'special_attacker': 'spa',   # Modest - special attack focus
        'physical_tank': 'def',      # Bold/Impish - defense focus
        'special_tank': 'spd',       # Calm - special defense focus
        'balanced': None             # Neutral nature
    }

    guide = {}
    for build_name, target_stat in breeding_targets.items():
        if target_stat:
            buff_natures = natures_client.get_natures_by_buffed_stat(target_stat)
            debuff_natures = natures_client.get_natures_by_debuffed_stat(target_stat)
        else:
            buff_natures = []
            debuff_natures = natures_client.get_neutral_natures()

        guide[build_name] = {
            'optimal_natures': [n['name'] for n in buff_natures],
            'avoid_natures': [n['name'] for n in debuff_natures],
            'target_stat': target_stat
        }

    return guide

breeding_guide = create_breeding_guide()
print("=== Perfect IV Breeding Guide ===")
for build, info in breeding_guide.items():
    print(f"{build.replace('_', ' ').title()}:")
    print(f"  Optimal: {info['optimal_natures']}")
    print(f"  Avoid: {info['avoid_natures']}")
    print()
```

### Example 2: Team Nature Optimization

```python
# Optimize nature choices for team composition
def optimize_team_natures(team_types, team_strategy="balanced"):
    """
    Suggest optimal natures based on team composition and strategy
    """
    nature_recommendations = {}

    # Strategy-based stat priorities
    if team_strategy == "offensive":
        priorities = ["spe", "atk", "spa"]  # Speed and power first
    elif team_strategy == "defensive":
        priorities = ["def", "spd", "hp"]   # Bulk first
    else:  # balanced
        priorities = ["spe", "atk", "def"]   # Mixed approach

    for revomon_type in team_types:
        recommendations = []

        for priority_stat in priorities:
            # Get natures that boost priority stats
            buff_natures = natures_client.get_natures_by_buffed_stat(priority_stat)
            for nature in buff_natures:
                # Check flavor compatibility
                flavor_info = {
                    'nature': nature['name'],
                    'buff': nature.get('buffs'),
                    'debuff': nature.get('debuffs'),
                    'likes': nature.get('likes'),
                    'dislikes': nature.get('dislikes')
                }
                recommendations.append(flavor_info)

        nature_recommendations[revomon_type] = recommendations

    return nature_recommendations

# Optimize for a balanced team
team_types = ["fire", "water", "grass"]
nature_optimal = optimize_team_natures(team_types, "balanced")

print("=== Team Nature Optimization ===")
for revomon_type, natures in nature_optimal.items():
    print(f"{revomon_type.title()} types:")
    for nature in natures[:3]:  # Top 3 recommendations
        print(f"  {nature['nature']}: +{nature['buff']} -{nature['debuff']}")
        print(f"    Likes: {nature['likes']}, Dislikes: {nature['dislikes']}")
```

### Example 3: Flavor-Based Feeding Strategy

```python
# Optimize feeding strategy based on nature preferences
def create_feeding_strategy(revomon_natures):
    """
    Create optimal feeding strategy based on nature flavor preferences
    """
    feeding_guide = {
        'optimal_foods': [],
        'avoid_foods': [],
        'happiness_impact': {}
    }

    # Analyze flavor preferences across team
    all_likes = set()
    all_dislikes = set()

    for nature_name in revomon_natures:
        nature = natures_client.get_nature(nature_name)
        if nature:
            likes = nature.get('likes')
            dislikes = nature.get('dislikes')

            if likes:
                all_likes.add(likes)
            if dislikes:
                all_dislikes.add(dislikes)

    feeding_guide['optimal_foods'] = list(all_likes)
    feeding_guide['avoid_foods'] = list(all_dislikes)

    # Calculate happiness impact
    for flavor in ['spicy', 'sour', 'sweet', 'dry', 'bitter']:
        likes_count = sum(1 for nature in revomon_natures
                         if natures_client.get_nature(nature) and
                         natures_client.get_nature(nature).get('likes') == flavor)
        dislikes_count = sum(1 for nature in revomon_natures
                            if natures_client.get_nature(nature) and
                            natures_client.get_nature(nature).get('dislikes') == flavor)

        feeding_guide['happiness_impact'][flavor] = likes_count - dislikes_count

    return feeding_guide

# Create feeding strategy for team
team_natures = ["jolly", "adamant", "modest"]
feeding_strategy = create_feeding_strategy(team_natures)

print("=== Team Feeding Strategy ===")
print(f"Optimal foods: {feeding_strategy['optimal_foods']}")
print(f"Avoid foods: {feeding_strategy['avoid_foods']}")
print("\nHappiness impact by flavor:")
for flavor, impact in feeding_strategy['happiness_impact'].items():
    status = "Beneficial" if impact > 0 else "Harmful" if impact < 0 else "Neutral"
    print(f"  {flavor}: {status} ({impact})")
```

### Example 4: Competitive Meta Analysis

```python
# Analyze nature usage in competitive meta
def analyze_nature_meta():
    all_natures = natures_client.get_all()

    # Categorize by stat focus
    stat_focus = {
        'speed': natures_client.get_speed_boosting_natures(),
        'attack': natures_client.get_attack_boosting_natures(),
        'defense': natures_client.get_natures_by_buffed_stat("def"),
        'special_attack': natures_client.get_natures_by_buffed_stat("spa"),
        'special_defense': natures_client.get_natures_by_buffed_stat("spd"),
        'hp': natures_client.get_natures_by_buffed_stat("hp")
    }

    # Calculate usage frequency (estimated)
    neutral_count = len(natures_client.get_neutral_natures())
    buff_count = len(natures_client.get_natures_with_stat_buffs())

    print("=== Nature Meta Analysis ===")
    print(f"Total natures: {len(all_natures)}")
    print(f"Stat-buffing natures: {buff_count}")
    print(f"Neutral natures: {neutral_count}")
    print(f"Buff ratio: {buff_count/len(all_natures)*100:.1f}%")

    print("\nStat focus distribution:")
    for stat, natures in stat_focus.items():
        print(f"  {stat.replace('_', ' ').title()}: {len(natures)} natures")
        if natures:
            print(f"    Examples: {[n['name'] for n in natures[:3]]}")

analyze_nature_meta()
```

## 🏆 Advanced Nature Analysis

### Perfect Nature Detection

```python
# Find perfect natures for specific competitive builds
def find_perfect_natures(target_stats, avoid_stats=None):
    """
    Find optimal natures for specific stat goals
    """
    perfect_natures = []

    for stat in target_stats:
        buff_natures = natures_client.get_natures_by_buffed_stat(stat)

        for nature in buff_natures:
            # Check if this nature avoids unwanted stat penalties
            if avoid_stats:
                debuff_stat = nature.get('debuffs')
                if debuff_stat and debuff_stat not in avoid_stats:
                    perfect_natures.append(nature)
            else:
                perfect_natures.append(nature)

    # Remove duplicates and sort by preference
    seen = set()
    unique_natures = []
    for nature in perfect_natures:
        nature_key = (nature.get('buffs'), nature.get('debuffs'))
        if nature_key not in seen:
            seen.add(nature_key)
            unique_natures.append(nature)

    return unique_natures

# Find perfect sweeper natures (speed + attack, avoid special attack penalty)
sweeper_stats = ["spe", "atk"]
avoid_for_sweepers = ["spa", "spd"]  # Avoid special penalties for physical sweepers

perfect_sweepers = find_perfect_natures(sweeper_stats, avoid_for_sweepers)
print("Perfect sweeper natures:")
for nature in perfect_sweepers:
    print(f"  {nature['name']}: +{nature['buffs']} -{nature['debuffs']}")
```

### Nature Synergy Analysis

```python
# Analyze nature synergy for team building
def analyze_nature_synergy(team_natures, strategy="offensive"):
    """
    Analyze how well team natures work together
    """
    synergy_score = 0
    analysis = {
        'speed_advantage': 0,
        'power_advantage': 0,
        'bulk_advantage': 0,
        'flavor_conflicts': 0
    }

    # Count stat buffs
    speed_buffs = sum(1 for nature in team_natures
                     if "speed" in natures_client.get_nature(nature).get('buffs', '').lower())
    attack_buffs = sum(1 for nature in team_natures
                      if "attack" in natures_client.get_nature(nature).get('buffs', '').lower())
    defense_buffs = sum(1 for nature in team_natures
                       if "def" in natures_client.get_nature(nature).get('buffs', '').lower())

    # Strategy-based scoring
    if strategy == "offensive":
        synergy_score += speed_buffs * 2 + attack_buffs * 1
        synergy_score -= defense_buffs * 0.5  # Less defense focus for offensive teams
    elif strategy == "defensive":
        synergy_score += defense_buffs * 2
        synergy_score += speed_buffs * 0.5  # Some speed still useful
    else:  # balanced
        synergy_score += (speed_buffs + attack_buffs + defense_buffs) * 1

    analysis['speed_advantage'] = speed_buffs
    analysis['power_advantage'] = attack_buffs
    analysis['bulk_advantage'] = defense_buffs

    return synergy_score, analysis

# Analyze team nature synergy
team_natures = ["jolly", "adamant", "bold", "timid"]
synergy_score, analysis = analyze_nature_synergy(team_natures, "balanced")

print("=== Team Nature Synergy ===")
print(f"Overall synergy score: {synergy_score}")
print(f"Speed advantage: {analysis['speed_advantage']} natures")
print(f"Power advantage: {analysis['power_advantage']} natures")
print(f"Bulk advantage: {analysis['bulk_advantage']} natures")
```

## 📈 Performance

- **Fast queries**: Indexed nature names and stat lookups
- **Cached data**: Nature database loaded once and cached
- **Efficient filtering**: Optimized stat and flavor-based searches
- **Memory efficient**: Minimal memory footprint for analysis

## 🧪 Testing

```bash
# Run natures client tests
uv run python -m pytest tests/clients/test_natures_client.py

# Test nature optimization
uv run python tests/integration/test_nature_optimization.py

# Performance benchmarks
uv run python tests/performance/test_nature_queries.py
```

## 🤝 Contributing

1. Ensure all nature stat modifications are accurate to game mechanics
2. Add comprehensive tests for new optimization methods
3. Update nature effects when balance changes occur
4. Document any meta analysis changes with sources

## 🔄 Version History

### v2.0.0
- Complete 25-nature system with stat modifications
- Advanced filtering by stat buffs and flavor preferences
- Competitive breeding guide and optimization tools
- Team synergy analysis and meta recommendations
- Comprehensive flavor-based feeding strategies

### v1.0.0
- Basic nature lookup by name
- Simple stat buff queries
- Basic flavor preference filtering

---

**Ready to perfect your Revomon's stats and dominate the meta? Let the nature optimization begin!** 🌿📊⚡
