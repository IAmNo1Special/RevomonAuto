# CounterdexClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Competitive intelligence and counter-strategy system for Revomon, providing tier rankings, metagame builds, counter strategies, and competitive tips for tournament preparation and team optimization.

## 🏆 Overview

The CounterdexClient provides the competitive knowledge base for Revomon:

- **Tier rankings** (S/A/B/C/D) for metagame positioning
- **Optimal builds** with EVs, natures, and abilities
- **Counter strategies** and matchup analysis
- **Competitive tips** from pro players and meta analysis
- **Type weaknesses** and exploitation strategies
- **Role identification** (sweeper, tank, support) for team building

This client contains the distilled competitive knowledge that separates casual players from tournament champions.

## 📊 Counterdex Data Structure

Each entry contains comprehensive competitive information:

### Competitive Analysis
- **`dex_id`** - Revodex ID (primary key)
- **`name`** - Revomon species name
- **`description`** - Competitive role and strategy description
- **`tier`** - Competitive tier ranking (S = highest, D = lowest)

### Optimal Builds
- **`metamoves`** - Recommended movesets for competitive play
- **`metabuilds`** - Optimal EV spreads, natures, and abilities
- **`tips`** - Pro-level strategies and tactics

### Counter Intelligence
- **`counters`** - Revomon that counter this species
- **`weakness`** - Type weaknesses and exploitation methods

## 🚀 Quick Start

### Basic Competitive Lookup

```python
from revomonauto.revomon.clients import CounterdexClient

# Initialize client
counterdex_client = CounterdexClient()

# Get competitive data by Revodex ID
monking_data = counterdex_client.get_counterdex_entry(25)
if monking_data:
    print(f"Monking tier: {monking_data['tier']}")
    print(f"Description: {monking_data['description']}")
    print(f"Tips: {monking_data['tips']}")

# Get by Revomon name
legendary_data = counterdex_client.get_counterdex_by_name("legendary_revomon")
if legendary_data:
    print(f"Legendary tier: {legendary_data['tier']}")
```

### Tier Analysis

```python
# Get Revomon by competitive tier
s_tier = counterdex_client.get_revomon_by_tier("s")
a_tier = counterdex_client.get_revomon_by_tier("a")
print(f"S-tier Revomon: {len(s_tier)}")
print(f"A-tier Revomon: {len(a_tier)}")

# Get top competitive Revomon
top_tier = counterdex_client.get_top_tier_revomon("b")  # B-tier and above
print(f"Competitive Revomon: {len(top_tier)}")
for revomon in top_tier[:5]:
    print(f"  {revomon['name']} (Tier {revomon['tier']})")
```

## 📚 API Reference

### Core Query Methods

#### `get_counterdex_entry(dex_id)`

Get competitive data by Revodex ID.

**Parameters:**
- `dex_id` (int): The Revodex ID

**Returns:** Counterdex data dictionary or None if not found

#### `get_counterdex_by_name(name)`

Get competitive data by Revomon name.

**Parameters:**
- `name` (str): The Revomon name

**Returns:** Counterdex data dictionary or None if not found

#### `get_revomon_by_tier(tier)`

Get all Revomon in a specific competitive tier.

**Parameters:**
- `tier` (str): Tier level (s, a, b, c, d)

**Returns:** List of Revomon in the specified tier

#### `get_top_tier_revomon(min_tier="b")`

Get Revomon in top competitive tiers.

**Parameters:**
- `min_tier` (str): Minimum tier to include (s = highest)

**Returns:** List of high-tier competitive Revomon

### Counter Strategy Methods

#### `get_revomon_with_specific_counters(counter_names)`

Get Revomon countered by specific Revomon.

**Parameters:**
- `counter_names` (list): List of counter Revomon names

**Returns:** List of Revomon countered by the specified counters

#### `get_revomon_by_weakness_count(min_weaknesses=4)`

Get Revomon with many type weaknesses.

**Parameters:**
- `min_weaknesses` (int): Minimum number of type weaknesses

**Returns:** List of Revomon with exploitable weaknesses

#### `get_tank_revomon()`, `get_sweeper_revomon()`

Get Revomon by competitive role (convenience methods).

**Returns:** List of Revomon matching the role

### Meta Analysis

#### `get_tier_distribution()`

Get count of Revomon by competitive tier.

**Returns:** Dictionary mapping tier to Revomon count

## 🎮 Usage Examples

### Example 1: Tournament Team Building

```python
from revomonauto.revomon.clients import CounterdexClient

counterdex_client = CounterdexClient()

# Build tournament-viable team
def build_tournament_team(max_per_tier=2):
    """
    Build a balanced tournament team with tier restrictions
    """
    team = []
    tier_counts = {'s': 0, 'a': 0, 'b': 0}

    # Get top tier Revomon
    s_tier = counterdex_client.get_revomon_by_tier("s")
    a_tier = counterdex_client.get_revomon_by_tier("a")
    b_tier = counterdex_client.get_revomon_by_tier("b")

    # Add S-tier (limited)
    for revomon in s_tier:
        if tier_counts['s'] < max_per_tier:
            team.append({
                'name': revomon['name'],
                'tier': revomon['tier'],
                'role': 'primary' if tier_counts['s'] == 0 else 'secondary'
            })
            tier_counts['s'] += 1

    # Add A-tier (moderate)
    for revomon in a_tier:
        if tier_counts['a'] < max_per_tier:
            team.append({
                'name': revomon['name'],
                'tier': revomon['tier'],
                'role': 'support'
            })
            tier_counts['a'] += 1

    # Fill with B-tier
    for revomon in b_tier:
        if len(team) < 6 and tier_counts['b'] < 3:
            team.append({
                'name': revomon['name'],
                'tier': revomon['tier'],
                'role': 'utility'
            })
            tier_counts['b'] += 1

    return team

tournament_team = build_tournament_team()
print("=== Tournament Team Composition ===")
for member in tournament_team:
    print(f"{member['name']} (Tier {member['tier']}) - {member['role']}")
```

### Example 2: Counter Strategy Development

```python
# Develop counter strategies for common threats
def develop_counter_strategies(target_revomon, available_pool):
    """
    Find optimal counters for specific threats
    """
    # Find Revomon weak to many types (easy to counter)
    exploitable = counterdex_client.get_revomon_by_weakness_count(4)

    # Find specific counters mentioned in counterdex
    counter_mentions = counterdex_client.get_revomon_with_specific_counters([target_revomon])

    # Find tanks that can wall the threat
    tanks = counterdex_client.get_tank_revomon()

    # Find fast sweepers that can outpace
    sweepers = counterdex_client.get_sweeper_revomon()

    # Compile counter strategy
    counters = {
        'exploitable': exploitable[:3],  # Easy type advantage
        'specific': counter_mentions[:3],  # Known counters
        'defensive': tanks[:3],           # Wall strategy
        'offensive': sweepers[:3]         # Speed strategy
    }

    return counters

# Develop counters for common threats
threats = ["legendary_fire", "legendary_water", "monking"]
for threat in threats:
    print(f"\n=== Counters for {threat} ===")
    counters = develop_counter_strategies(threat, "available_revomon")

    for strategy, revomon_list in counters.items():
        print(f"{strategy.title()}:")
        for revomon in revomon_list:
            print(f"  {revomon['name']} (Tier {revomon.get('tier', 'Unknown')})")
```

### Example 3: Meta Analysis and Trends

```python
# Analyze current meta trends and tier distribution
def analyze_meta_trends():
    """
    Analyze current competitive meta and identify trends
    """
    tier_dist = counterdex_client.get_tier_distribution()

    # Calculate meta health metrics
    total_revomon = sum(tier_dist.values())
    s_a_count = tier_dist.get('s', 0) + tier_dist.get('a', 0)
    meta_diversity = len([tier for tier, count in tier_dist.items() if count > 0])

    # Get role distribution
    tanks = counterdex_client.get_tank_revomon()
    sweepers = counterdex_client.get_sweeper_revomon()

    print("=== Meta Analysis ===")
    print(f"Total competitive Revomon: {total_revomon}")
    print(f"Top-tier (S+A): {s_a_count} ({s_a_count/total_revomon*100:.1f}%)")
    print(f"Meta diversity: {meta_diversity} active tiers")

    print(f"\nRole distribution:")
    print(f"  Tanks: {len(tanks)}")
    print(f"  Sweepers: {len(sweepers)}")
    print(f"  Other roles: {total_revomon - len(tanks) - len(sweepers)}")

    print("
Tier distribution:")
    for tier, count in sorted(tier_dist.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_revomon) * 100
        print(f"  Tier {tier.upper()}: {count} ({percentage:.1f}%)")

analyze_meta_trends()
```

### Example 4: Team Composition Optimization

```python
# Optimize team composition for competitive balance
def optimize_team_composition(current_team, strategy="balanced"):
    """
    Suggest improvements to team composition
    """
    # Analyze current team tiers and roles
    team_analysis = {
        'tiers': {},
        'roles': {},
        'weaknesses': []
    }

    for revomon in current_team:
        # Get competitive data
        comp_data = counterdex_client.get_counterdex_by_name(revomon['name'])
        if comp_data:
            tier = comp_data.get('tier', 'unknown')
            team_analysis['tiers'][tier] = team_analysis['tiers'].get(tier, 0) + 1

            # Determine role from description
            desc = comp_data.get('description', '').lower()
            if any(word in desc for word in ['tank', 'defensive', 'wall']):
                team_analysis['roles']['tank'] = team_analysis['roles'].get('tank', 0) + 1
            elif any(word in desc for word in ['sweeper', 'attacker', 'offensive']):
                team_analysis['roles']['sweeper'] = team_analysis['roles'].get('sweeper', 0) + 1
            else:
                team_analysis['roles']['support'] = team_analysis['roles'].get('support', 0) + 1

    # Suggest improvements
    suggestions = []

    # Check tier balance
    high_tier_count = team_analysis['tiers'].get('s', 0) + team_analysis['tiers'].get('a', 0)
    if high_tier_count < 2:
        suggestions.append("Consider adding more S/A tier Revomon for competitive viability")

    # Check role balance
    if team_analysis['roles'].get('tank', 0) == 0:
        suggestions.append("Add a tank Revomon for defensive stability")
    if team_analysis['roles'].get('sweeper', 0) < 2:
        suggestions.append("Add sweepers for offensive pressure")

    return team_analysis, suggestions

# Analyze current team
current_team = [
    {"name": "fire_starter"}, {"name": "water_starter"}, {"name": "grass_starter"},
    {"name": "electric_type"}, {"name": "ground_type"}, {"name": "flying_type"}
]

analysis, suggestions = optimize_team_composition(current_team)

print("=== Team Analysis ===")
print("Tier distribution:", analysis['tiers'])
print("Role distribution:", analysis['roles'])

print("\nSuggestions:")
for suggestion in suggestions:
    print(f"  • {suggestion}")
```

## 🏆 Advanced Competitive Analysis

### Meta Tier Evolution

```python
# Track how meta tiers change over time
def analyze_meta_evolution(current_meta, previous_meta=None):
    """
    Analyze how the competitive meta has evolved
    """
    if not previous_meta:
        # Initial meta analysis
        tier_dist = counterdex_client.get_tier_distribution()
        top_revomon = counterdex_client.get_top_tier_revomon("b")

        return {
            'current_meta': tier_dist,
            'top_picks': [r['name'] for r in top_revomon[:10]],
            'meta_health': len(tier_dist),  # Number of active tiers
            'power_concentration': tier_dist.get('s', 0) / sum(tier_dist.values()) if tier_dist else 0
        }
    else:
        # Compare with previous meta
        evolution = {}

        for tier in ['s', 'a', 'b', 'c', 'd']:
            current_count = current_meta.get('current_meta', {}).get(tier, 0)
            previous_count = previous_meta.get('current_meta', {}).get(tier, 0)
            change = current_count - previous_count
            evolution[tier] = change

        # Find new top picks
        current_tops = set(current_meta.get('top_picks', []))
        previous_tops = set(previous_meta.get('top_picks', []))
        new_rising = current_tops - previous_tops
        fallen_out = previous_tops - current_tops

        return {
            'tier_changes': evolution,
            'new_rising': list(new_rising),
            'fallen_out': list(fallen_out),
            'meta_shift': len(new_rising) + len(fallen_out)
        }

# Analyze current meta
current_analysis = analyze_meta_evolution(None)
print("=== Current Meta State ===")
print(f"Meta health: {current_analysis['meta_health']} active tiers")
print(f"Power concentration: {current_analysis['power_concentration']:.1%} in S-tier")
print(f"Top picks: {current_analysis['top_picks']}")
```

### Counter Network Analysis

```python
# Analyze counter relationships in the meta
def analyze_counter_network():
    """
    Build a network of counter relationships
    """
    counter_network = {
        'mutual_counters': [],
        'one_way_counters': [],
        'counter_clusters': []
    }

    # Get all counterdex entries
    all_entries = counterdex_client.get_all()

    # Analyze counter relationships
    for revomon in all_entries[:20]:  # Limit for performance
        revomon_name = revomon['name']
        counters_text = revomon.get('counters', '')

        if counters_text:
            counters = [c.strip() for c in counters_text.split('\n') if c.strip()]

            # Check if counters counter back
            for counter in counters:
                counter_data = counterdex_client.get_counterdex_by_name(counter)
                if counter_data:
                    counter_counters = counter_data.get('counters', '')
                    if counter_counters and revomon_name.lower() in counter_counters.lower():
                        counter_network['mutual_counters'].append({
                            'revomon1': revomon_name,
                            'revomon2': counter
                        })
                    else:
                        counter_network['one_way_counters'].append({
                            'revomon': revomon_name,
                            'counter': counter
                        })

    return counter_network

counter_network = analyze_counter_network()

print("=== Counter Network Analysis ===")
print(f"Mutual counters: {len(counter_network['mutual_counters'])}")
print(f"One-way counters: {len(counter_network['one_way_counters'])}")

print("\nMutual counter pairs:")
for pair in counter_network['mutual_counters'][:5]:
    print(f"  {pair['revomon1']} ↔ {pair['revomon2']}")
```

## 📈 Performance

- **Fast queries**: Indexed Revodex IDs and tier lookups
- **Cached data**: Counterdex database loaded once and cached
- **Efficient analysis**: Optimized counter relationship calculations
- **Memory efficient**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run counterdex client tests
uv run python -m pytest tests/clients/test_counterdex_client.py

# Test competitive analysis
uv run python tests/integration/test_competitive_analysis.py

# Performance benchmarks
uv run python tests/performance/test_counterdex_queries.py
```

## 🤝 Contributing

1. Ensure all tier rankings are accurate to current meta
2. Add comprehensive tests for new competitive analysis methods
3. Update counter strategies when meta shifts occur
4. Document any competitive insights with sources

## 🔄 Version History

### v2.0.0
- Complete competitive intelligence system with tier rankings
- Advanced counter strategy analysis and meta tracking
- Tournament team building and optimization tools
- Comprehensive counter network analysis
- Meta evolution tracking and trend analysis

### v1.0.0
- Basic tier lookup and competitive data
- Simple counter strategy queries
- Basic meta analysis tools

---

**Ready to dominate the competitive scene and master the meta? Let the counter analysis begin!** 🏆⚔️📊
