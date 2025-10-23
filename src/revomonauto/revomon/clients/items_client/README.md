# ItemsClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive items database for Revomon, providing access to equipment, consumables, healing items, and utilities for strategic preparation, battle optimization, and economic planning.

## 🎒 Overview

The ItemsClient provides complete access to the Revomon item ecosystem:

- **Equipment and held items** for stat enhancement and strategic advantages
- **Consumable items** for healing, status curing, and temporary boosts
- **Battle items** for in-combat strategy and advantage
- **Economic analysis** for cost optimization and resource management
- **Item acquisition** strategies and source tracking
- **Competitive item** optimization for tournament preparation

This client is essential for understanding the complete Revomon economy and optimizing team preparation for both casual play and competitive battles.

## 📊 Item Data Structure

Each item contains comprehensive information:

### Core Information
- **`name`** - Unique item identifier (primary key)
- **`description`** - Detailed effects, usage, and mechanics
- **`obtained_from`** - Source of acquisition (shop, drops, quests, etc.)
- **`cost`** - Purchase price (null if not purchasable)

### Item Categories
- **Healing Items** - HP restoration and status condition cures
- **Stat Boosters** - Temporary or permanent stat enhancements
- **Battle Items** - In-combat utility and strategic items
- **Held Items** - Equipment that provides passive benefits
- **Consumables** - One-time use items with various effects

## 🚀 Quick Start

### Basic Item Lookup

```python
from revomonauto.revomon.clients import ItemsClient

# Initialize client
items_client = ItemsClient()

# Get item by name
potion = items_client.get_item("potion")
print(f"Potion cost: {potion['cost']}, Source: {potion['obtained_from']}")

# Get purchasable items
shop_items = items_client.get_purchasable_items()
print(f"Shop items: {len(shop_items)}")

# Get free items
free_items = items_client.get_free_items()
print(f"Free items: {len(free_items)}")
```

### Item Category Analysis

```python
# Get items by category
healing_items = items_client.get_healing_items()
stat_boosters = items_client.get_stat_boosting_items()
battle_items = items_client.get_battle_items()
consumables = items_client.get_consumable_items()

print(f"Healing items: {len(healing_items)}")
print(f"Stat boosters: {len(stat_boosters)}")
print(f"Battle items: {len(battle_items)}")
print(f"Consumables: {len(consumables)}")
```

## 📚 API Reference

### Core Query Methods

#### `get_item(item_name)`

Get item data by name.

**Parameters:**
- `item_name` (str): The item name

**Returns:** Item data dictionary or None if not found

#### `get_purchasable_items()`

Get items available for purchase.

**Returns:** List of items with cost information

#### `get_free_items()`

Get items that are free or obtained through other means.

**Returns:** List of free items

#### `get_items_by_source(source)`

Get items from a specific acquisition source.

**Parameters:**
- `source` (str): Source (e.g., "revocenter", "battle reward")

**Returns:** List of items from the specified source

#### `get_items_by_cost_range(min_cost, max_cost)`

Get items within a price range.

**Parameters:**
- `min_cost` (int): Minimum cost
- `max_cost` (int): Maximum cost

**Returns:** List of items within the price range

### Category Methods

#### `get_stat_boosting_items()`

Get items that enhance combat stats.

**Returns:** List of stat-boosting items

#### `get_healing_items()`

Get items that heal HP or cure status conditions.

**Returns:** List of healing and curing items

#### `get_battle_items()`

Get items designed for use in battle.

**Returns:** List of battle utility items

#### `get_consumable_items()`

Get consumable items (used up after use).

**Returns:** List of consumable items

## 🎮 Usage Examples

### Example 1: Shopping Strategy

```python
from revomonauto.revomon.clients import ItemsClient

items_client = ItemsClient()

# Analyze shopping strategy
def plan_shopping_budget(budget=1000):
    shop_items = items_client.get_purchasable_items()

    # Sort by cost efficiency (value per cost)
    item_value = []
    for item in shop_items:
        cost = item.get('cost', 0)
        if cost > 0 and cost <= budget:
            # Simple value heuristic based on description
            value = 1  # Base value
            description = item.get('description', '').lower()

            if 'heal' in description or 'restore' in description:
                value += 2  # Healing is valuable
            if 'stat' in description or 'boost' in description:
                value += 1  # Stat boosts are good
            if 'battle' in description:
                value += 1  # Battle utility

            efficiency = value / cost
            item_value.append({
                'item': item,
                'cost': cost,
                'value': value,
                'efficiency': efficiency
            })

    # Sort by efficiency
    item_value.sort(key=lambda x: x['efficiency'], reverse=True)

    # Plan optimal purchase
    total_cost = 0
    shopping_list = []

    for item_data in item_value:
        if total_cost + item_data['cost'] <= budget:
            shopping_list.append(item_data)
            total_cost += item_data['cost']

    return shopping_list, total_cost

shopping_list, total_cost = plan_shopping_budget(500)
print(f"Optimal shopping list (Cost: {total_cost}):")
for item in shopping_list:
    print(f"  {item['item']['name']}: ${item['cost']} (Efficiency: {item['efficiency']:.3f})")
```

### Example 2: Battle Preparation

```python
# Plan battle preparation items
def prepare_for_battle(budget=200, battle_type="standard"):
    """
    Select optimal items for different battle types
    """
    preparation = {
        'healing': items_client.get_healing_items(),
        'boosters': items_client.get_stat_boosting_items(),
        'battle_items': items_client.get_battle_items()
    }

    # Prioritize based on battle type
    if battle_type == "long":
        # Focus on healing and sustain
        priority_order = ['healing', 'boosters', 'battle_items']
    elif battle_type == "quick":
        # Focus on damage and speed
        priority_order = ['boosters', 'battle_items', 'healing']
    else:
        # Balanced approach
        priority_order = ['healing', 'battle_items', 'boosters']

    selected_items = []
    total_cost = 0

    for category in priority_order:
        items = preparation[category]
        for item in items:
            cost = item.get('cost', 0)
            if cost and total_cost + cost <= budget:
                selected_items.append(item)
                total_cost += cost
                if total_cost >= budget * 0.8:  # Don't spend everything
                    break

    return selected_items, total_cost

# Prepare for a long tournament
tourney_items, cost = prepare_for_battle(300, "long")
print(f"Tournament preparation (Cost: {cost}):")
for item in tourney_items:
    print(f"  {item['name']}: ${item.get('cost', 0)} - {item['description'][:50]}...")
```

### Example 3: Economic Analysis

```python
# Analyze item economy and value
def analyze_item_economy():
    shop_items = items_client.get_purchasable_items()
    free_items = items_client.get_free_items()

    # Cost distribution
    cost_ranges = {
        'cheap': [i for i in shop_items if 0 < i.get('cost', 0) <= 50],
        'moderate': [i for i in shop_items if 51 <= i.get('cost', 0) <= 200],
        'expensive': [i for i in shop_items if 201 <= i.get('cost', 0) <= 1000],
        'premium': [i for i in shop_items if i.get('cost', 0) > 1000]
    }

    # Source analysis
    sources = {}
    for item in shop_items + free_items:
        source = item.get('obtained_from', 'unknown')
        sources[source] = sources.get(source, 0) + 1

    # Value assessment
    healing_items = items_client.get_healing_items()
    stat_items = items_client.get_stat_boosting_items()

    print("=== Item Economy Analysis ===")
    print(f"Total items: {len(shop_items) + len(free_items)}")
    print(f"Shop items: {len(shop_items)}, Free items: {len(free_items)}")

    print("\nCost distribution:")
    for range_name, items in cost_ranges.items():
        print(f"  {range_name}: {len(items)} items")

    print("\nAcquisition sources:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {source}: {count} items")

    print(f"\nSpecialized items:")
    print(f"  Healing items: {len(healing_items)}")
    print(f"  Stat boosters: {len(stat_items)}")

analyze_item_economy()
```

### Example 4: Team Preparation Strategy

```python
# Optimize item selection for team composition
def optimize_team_items(team_types, budget=500):
    """
    Select optimal items based on team composition and strategy
    """
    # Analyze team needs based on types
    team_needs = {
        'healing': 3,      # Base healing need
        'boosting': 2,     # Base stat boosting need
        'utility': 1       # Base utility need
    }

    # Adjust based on team types
    if "fire" in team_types:
        team_needs['healing'] += 1  # Fire teams often need more healing
    if any(t in team_types for t in ["water", "ice"]):
        team_needs['boosting'] += 1  # Weather teams benefit from boosters

    # Select items by priority
    selected_items = []
    total_cost = 0

    # Priority 1: Essential healing
    healing_items = items_client.get_healing_items()
    for item in healing_items:
        if len([i for i in selected_items if 'heal' in i.get('description', '').lower()]) < team_needs['healing']:
            cost = item.get('cost', 0)
            if cost and total_cost + cost <= budget:
                selected_items.append(item)
                total_cost += cost

    # Priority 2: Stat boosters
    stat_items = items_client.get_stat_boosting_items()
    for item in stat_items:
        if len([i for i in selected_items if 'boost' in i.get('description', '').lower()]) < team_needs['boosting']:
            cost = item.get('cost', 0)
            if cost and total_cost + cost <= budget:
                selected_items.append(item)
                total_cost += cost

    return selected_items, total_cost

# Optimize for a balanced team
team_types = ["fire", "water", "grass"]
team_items, cost = optimize_team_items(team_types, 400)

print(f"Team optimization (Cost: {cost}):")
for item in team_items:
    print(f"  {item['name']}: ${item.get('cost', 0)}")
    print(f"    {item['description']}")
    print(f"    Source: {item.get('obtained_from', 'Unknown')}")
    print()
```

## 🏆 Advanced Item Analysis

### Item Efficiency Metrics

```python
# Calculate item efficiency for competitive use
def calculate_item_efficiency(item, context="general"):
    efficiency = 0
    description = item.get('description', '').lower()
    cost = item.get('cost', 1)

    # Base efficiency by category
    if any(word in description for word in ['heal', 'restore', 'recover']):
        efficiency += 30  # Healing is very valuable
    elif any(word in description for word in ['stat', 'boost', 'increase']):
        efficiency += 20  # Stat boosts are valuable
    elif any(word in description for word in ['battle', 'combat', 'fight']):
        efficiency += 15  # Battle utility is useful
    elif any(word in description for word in ['status', 'cure', 'condition']):
        efficiency += 25  # Status curing is valuable

    # Context bonuses
    if context == "tournament" and any(word in description for word in ['heal', 'restore']):
        efficiency += 10  # Extra value in tournaments

    if context == "speedrun" and any(word in description for word in ['speed', 'quick']):
        efficiency += 5  # Speed bonuses for speedruns

    # Cost efficiency (value per cost)
    if cost > 0:
        efficiency = efficiency / cost * 100  # Normalize by cost

    return efficiency

# Analyze most efficient items
shop_items = items_client.get_purchasable_items()
efficient_items = []

for item in shop_items:
    efficiency = calculate_item_efficiency(item, "tournament")
    efficient_items.append({
        'item': item,
        'efficiency': efficiency
    })

# Sort by efficiency
efficient_items.sort(key=lambda x: x['efficiency'], reverse=True)

print("Most efficient tournament items:")
for item_data in efficient_items[:10]:
    item = item_data['item']
    print(f"{item['name']}: {item_data['efficiency']:.1f} efficiency (${item.get('cost', 0)})")
```

### Item Meta Analysis

```python
# Analyze item usage patterns and meta
def analyze_item_meta():
    all_items = items_client.get_all()
    shop_items = items_client.get_purchasable_items()

    # Category analysis
    categories = {
        'healing': items_client.get_healing_items(),
        'stat_boosting': items_client.get_stat_boosting_items(),
        'battle': items_client.get_battle_items(),
        'consumable': items_client.get_consumable_items()
    }

    # Cost analysis
    if shop_items:
        costs = [item.get('cost', 0) for item in shop_items if item.get('cost')]
        avg_cost = sum(costs) / len(costs) if costs else 0

        cost_distribution = {
            'cheap': len([i for i in shop_items if 0 < i.get('cost', 0) <= avg_cost * 0.5]),
            'moderate': len([i for i in shop_items if avg_cost * 0.5 < i.get('cost', 0) <= avg_cost * 1.5]),
            'expensive': len([i for i in shop_items if i.get('cost', 0) > avg_cost * 1.5])
        }

    # Source analysis
    sources = {}
    for item in all_items:
        source = item.get('obtained_from', 'unknown')
        sources[source] = sources.get(source, 0) + 1

    print("=== Item Meta Analysis ===")
    print(f"Total items: {len(all_items)}")
    print(f"Shop items: {len(shop_items)}")

    print("\nCategory distribution:")
    for category, items in categories.items():
        print(f"  {category.replace('_', ' ').title()}: {len(items)} items")

    if shop_items:
        print(f"\nCost analysis (avg: ${avg_cost:.0f}):")
        for cost_range, count in cost_distribution.items():
            print(f"  {cost_range}: {count} items")

    print("\nTop acquisition sources:")
    for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {source}: {count} items")

item_meta = analyze_item_meta()
```

## 📈 Performance

- **Fast queries**: Indexed item names and efficient category filtering
- **Cached data**: Item database loaded once and cached
- **Economic analysis**: Optimized for cost and value calculations
- **Memory efficient**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run items client tests
uv run python -m pytest tests/clients/test_items_client.py

# Test item analysis
uv run python tests/integration/test_item_analysis.py

# Performance benchmarks
uv run python tests/performance/test_item_queries.py
```

## 🤝 Contributing

1. Ensure all item data is accurate to game economy
2. Add comprehensive tests for new analysis methods
3. Update item costs and sources when economy changes
4. Document any new item categories or mechanics

## 🔄 Version History

### v2.0.0
- Complete item database with economic analysis
- Advanced filtering by categories and cost ranges
- Competitive item efficiency metrics
- Shopping strategy optimization
- Comprehensive meta analysis tools

### v1.0.0
- Basic item lookup by name
- Simple category filtering
- Basic cost and source queries

---

**Ready to optimize your Revomon inventory and dominate the economy? Let the item analysis begin!** 🎒💰📊
