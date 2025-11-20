# LocationsClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Spawn location and geography system for Revomon, providing comprehensive world exploration data, spawn time analysis, location statistics, and strategic hunting optimization for finding rare species.

## 🌍 Overview

The LocationsClient provides the complete world geography and spawn system for Revomon:

- **Complete spawn locations** across all game maps and areas
- **Spawn time analysis** with temporal patterns and peak hours
- **Revomon distribution** by location and spawn rates
- **Location statistics** and biodiversity analysis
- **Strategic hunting** optimization and route planning
- **Spawn meta analysis** for targeted species hunting

This client transforms Revomon from simple battles into a geographic hunting game, enabling strategic exploration and rare species targeting.

## 📊 Location Data Structure

Spawn data is embedded in Revomon records with location and timing information:

### Location Information
- **`spawn_loc1`**, **`spawn_loc2`**, **`spawn_loc3`** - Up to 3 spawn locations per Revomon
- **`spawn_time1`**, **`spawn_time2`**, **`spawn_time3`** - Time periods for each location
- **`spawn_rate`** - Encounter probability and rarity information

### Geographic Categories
- **Cities** - Drassius City, Marquis Island
- **Routes** - Exploration areas and paths
- **Special Areas** - PVP Arena, NPC Battle Maps, Player Hub
- **Wild Areas** - Natural spawn zones and habitats

## 🚀 Quick Start

### Basic Location Analysis

```python
from revomonauto.revomon.clients import LocationsClient

# Initialize client
locations_client = LocationsClient()

# Get all unique spawn locations
all_locations = locations_client.get_all_spawn_locations()
print(f"Total unique locations: {len(all_locations)}")

# Find Revomon in a specific location
city_revomon = locations_client.get_revomon_by_location("drassius city")
print(f"Revomon in Drassius City: {len(city_revomon)}")

# Get detailed location information
city_details = locations_client.get_spawn_details("drassius city")
print(f"Unique species in city: {city_details['unique_revomon']}")
```

### Spawn Time Analysis

```python
# Get locations by spawn time
morning_locations = locations_client.get_locations_by_time("4:00 to 9:59")
night_locations = locations_client.get_locations_by_time("22:00 to 3:59")
print(f"Morning spawns: {len(morning_locations)} locations")
print(f"Night spawns: {len(night_locations)} locations")

# Get spawn times for a location
city_times = locations_client.get_location_spawn_times("drassius city")
print("Drassius City spawn schedule:")
for time, revomon in city_times.items():
    print(f"  {time}: {len(revomon)} species")
```

## 📚 API Reference

### Core Query Methods

#### `get_all_spawn_locations()`

Get all unique spawn locations.

**Returns:** List of unique location names

#### `get_revomon_by_location(location)`

Get all Revomon that spawn in a specific location.

**Parameters:**
- `location` (str): Location name

**Returns:** List of Revomon with spawn details

#### `get_spawn_details(location)`

Get comprehensive spawn information for a location.

**Parameters:**
- `location` (str): Location name

**Returns:** Detailed location analysis with Revomon, times, and rates

#### `get_locations_by_time(time_period)`

Get locations with spawns during specific time periods.

**Parameters:**
- `time_period` (str): Time period (e.g., "4:00 to 9:59")

**Returns:** List of locations with spawns in that time

#### `get_location_spawn_times(location)`

Get spawn schedule for a location.

**Parameters:**
- `location` (str): Location name

**Returns:** Dictionary mapping time periods to Revomon lists

### Analysis Methods

#### `get_common_spawn_times()`

Get most common spawn time periods.

**Returns:** Dictionary mapping time periods to Revomon counts

#### `get_location_statistics()`

Get comprehensive statistics about all locations.

**Returns:** Location analytics with biodiversity metrics

#### `search_locations_by_keyword(keyword)`

Search locations by name keywords.

**Parameters:**
- `keyword` (str): Keyword to search for

**Returns:** List of matching locations

## 🎮 Usage Examples

### Example 1: Strategic Hunting Routes

```python
from revomonauto.revomon.clients import LocationsClient

locations_client = LocationsClient()

# Plan optimal hunting routes
def plan_hunting_route(target_rarity="rare", time_preference="day"):
    """
    Plan optimal hunting route for specific goals
    """
    # Get locations by time preference
    if time_preference == "day":
        time_filter = "4:00 to 21:59"
    elif time_preference == "night":
        time_filter = "22:00 to 3:59"
    else:
        time_filter = None

    if time_filter:
        active_locations = locations_client.get_locations_by_time(time_filter)
    else:
        active_locations = locations_client.get_all_spawn_locations()

    # Analyze locations for target rarity
    route_plan = []
    for location in active_locations:
        location_details = locations_client.get_spawn_details(location)

        # Estimate rarity potential (simplified)
        rarity_score = 0
        for revomon in location_details['revomon']:
            if "legendary" in revomon.get('rarity', '').lower():
                rarity_score += 3
            elif "rare" in revomon.get('rarity', '').lower():
                rarity_score += 2
            elif "uncommon" in revomon.get('rarity', '').lower():
                rarity_score += 1

        if rarity_score > 0:
            route_plan.append({
                'location': location,
                'rarity_score': rarity_score,
                'revomon_count': location_details['unique_revomon'],
                'spawn_times': location_details['spawn_times']
            })

    # Sort by rarity potential
    route_plan.sort(key=lambda x: x['rarity_score'], reverse=True)
    return route_plan

# Plan rare hunting route for daytime
rare_route = plan_hunting_route("rare", "day")

print("=== Optimal Rare Hunting Route ===")
for stop in rare_route[:5]:
    print(f"{stop['location']}: Rarity score {stop['rarity_score']}")
    print(f"  Species: {stop['revomon_count']}, Times: {stop['spawn_times']}")
```

### Example 2: Spawn Time Optimization

```python
# Optimize hunting by spawn time patterns
def optimize_spawn_times(target_revomon=None):
    """
    Find best times to hunt for rare Revomon
    """
    common_times = locations_client.get_common_spawn_times()

    # Get locations with high activity during peak times
    peak_times = []
    for time_period, count in common_times.items():
        if count > 5:  # High activity threshold
            locations = locations_client.get_locations_by_time(time_period)
            peak_times.append({
                'time': time_period,
                'revomon_count': count,
                'locations': locations[:5]  # Top 5 locations
            })

    # Sort by activity level
    peak_times.sort(key=lambda x: x['revomon_count'], reverse=True)

    return peak_times

# Find optimal hunting times
optimal_times = optimize_spawn_times()

print("=== Optimal Spawn Times ===")
for time_slot in optimal_times[:3]:
    print(f"{time_slot['time']}: {time_slot['revomon_count']} Revomon")
    print(f"  Top locations: {time_slot['locations']}")
```

### Example 3: Location Biodiversity Analysis

```python
# Analyze biodiversity and habitat diversity
def analyze_location_biodiversity():
    """
    Analyze which locations have the most diverse Revomon populations
    """
    biodiversity_analysis = []

    all_locations = locations_client.get_all_spawn_locations()

    for location in all_locations:
        details = locations_client.get_spawn_details(location)

        # Calculate biodiversity metrics
        total_spawns = details['revomon_count']
        unique_species = details['unique_revomon']
        diversity_ratio = unique_species / total_spawns if total_spawns > 0 else 0

        # Habitat diversity (different spawn times)
        habitat_diversity = len(details['spawn_times'])

        biodiversity_analysis.append({
            'location': location,
            'total_spawns': total_spawns,
            'unique_species': unique_species,
            'diversity_ratio': diversity_ratio,
            'habitat_diversity': habitat_diversity,
            'biodiversity_score': diversity_ratio * habitat_diversity
        })

    # Sort by biodiversity
    biodiversity_analysis.sort(key=lambda x: x['biodiversity_score'], reverse=True)

    return biodiversity_analysis

biodiversity = analyze_location_biodiversity()

print("=== Location Biodiversity ===")
for location in biodiversity[:10]:
    print(f"{location['location']}:")
    print(f"  Species: {location['unique_species']}/{location['total_spawns']}")
    print(f"  Diversity: {location['diversity_ratio']:.2f}, Habitats: {location['habitat_diversity']}")
    print(f"  Biodiversity score: {location['biodiversity_score']:.2f}")
    print()
```

### Example 4: Geographic Meta Analysis

```python
# Analyze geographic distribution and meta patterns
def analyze_geographic_meta():
    """
    Analyze how Revomon are distributed across the game world
    """
    stats = locations_client.get_location_statistics()

    print("=== Geographic Meta Analysis ===")
    print(f"Total locations: {stats['total_locations']}")
    print(f"Total spawn entries: {stats['total_spawn_entries']}")
    print(f"Average Revomon per location: {stats['avg_revomon_per_location']:.1f}")

    # Most active locations
    active_locations = sorted(stats['locations'].items(),
                            key=lambda x: x[1]['total_revomon'],
                            reverse=True)

    print("
Most active locations:")
    for location, data in active_locations[:5]:
        print(f"  {location}: {data['total_revomon']} spawns, {data['unique_revomon']} species")

    # Most diverse spawn times
    print("
Common spawn times:")
    for time_period, count in list(stats['common_times'].items())[:5]:
        print(f"  {time_period}: {count} Revomon")

# Analyze the geographic meta
analyze_geographic_meta()
```

## 🏆 Advanced Location Analysis

### Spawn Density Mapping

```python
# Create spawn density maps for strategic hunting
def create_spawn_density_map():
    """
    Create density analysis for strategic route planning
    """
    density_map = {}

    all_locations = locations_client.get_all_spawn_locations()

    for location in all_locations:
        details = locations_client.get_spawn_details(location)

        # Calculate density metrics
        spawn_density = details['revomon_count'] / len(details['spawn_times']) if details['spawn_times'] else 0
        rarity_density = sum(1 for r in details['revomon']
                           if 'rare' in r.get('rarity', '').lower() or
                           'legendary' in r.get('rarity', '').lower())

        density_map[location] = {
            'spawn_density': spawn_density,
            'rarity_density': rarity_density,
            'total_spawns': details['revomon_count'],
            'spawn_times': details['spawn_times']
        }

    # Sort by strategic value (density + rarity)
    strategic_value = {}
    for location, metrics in density_map.items():
        strategic_score = metrics['spawn_density'] + (metrics['rarity_density'] * 2)
        strategic_value[location] = strategic_score

    sorted_locations = sorted(strategic_value.items(), key=lambda x: x[1], reverse=True)

    return density_map, sorted_locations

density_map, strategic_locations = create_spawn_density_map()

print("=== Strategic Hunting Locations ===")
for location, score in strategic_locations[:10]:
    metrics = density_map[location]
    print(f"{location}: Strategic score {score:.1f}")
    print(f"  Density: {metrics['spawn_density']:.1f}, Rarity: {metrics['rarity_density']}")
    print(f"  Times: {metrics['spawn_times']}")
    print()
```

### Temporal Spawn Analysis

```python
# Analyze spawn patterns over time for optimal hunting
def analyze_temporal_patterns():
    """
    Analyze when and where to hunt for best results
    """
    temporal_analysis = {
        'peak_hours': {},
        'location_specialization': {},
        'time_based_strategies': {}
    }

    common_times = locations_client.get_common_spawn_times()

    # Analyze each time period
    for time_period, revomon_count in common_times.items():
        locations = locations_client.get_locations_by_time(time_period)

        # Find locations with highest activity during this time
        location_activity = {}
        for location in locations[:5]:  # Top 5 locations
            details = locations_client.get_spawn_details(location)
            location_activity[location] = details['unique_revomon']

        temporal_analysis['peak_hours'][time_period] = {
            'revomon_count': revomon_count,
            'active_locations': len(locations),
            'top_locations': sorted(location_activity.items(), key=lambda x: x[1], reverse=True)
        }

    return temporal_analysis

temporal = analyze_temporal_patterns()

print("=== Temporal Spawn Analysis ===")
for time_period, analysis in temporal['peak_hours'].items():
    print(f"{time_period}:")
    print(f"  {analysis['revomon_count']} Revomon, {analysis['active_locations']} locations")
    if analysis['top_locations']:
        print(f"  Top location: {analysis['top_locations'][0][0]} ({analysis['top_locations'][0][1]} species)")
```

## 📈 Performance

- **Fast queries**: Indexed location names and spawn data
- **Cached data**: Location database loaded once and cached
- **Efficient analysis**: Optimized biodiversity and density calculations
- **Memory efficient**: Data copied to prevent mutation

## 🧪 Testing

```bash
# Run locations client tests
uv run python -m pytest tests/clients/test_locations_client.py

# Test spawn analysis
uv run python tests/integration/test_spawn_analysis.py

# Performance benchmarks
uv run python tests/performance/test_location_queries.py
```

## 🤝 Contributing

1. Ensure all spawn location data is accurate to game world
2. Add comprehensive tests for new geographic analysis methods
3. Update spawn times when game schedules change
4. Document any new locations or spawn mechanics

## 🔄 Version History

### v2.0.0
- Complete spawn location system with temporal analysis
- Advanced biodiversity and density analysis
- Strategic hunting route optimization
- Geographic meta analysis and spawn pattern tracking
- Comprehensive spawn time optimization tools

### v1.0.0
- Basic location lookup and Revomon filtering
- Simple spawn time queries
- Basic location statistics

---

**Ready to explore the Revomon world and master the hunting meta? Let the location analysis begin!** 🌍🗺️🔍
