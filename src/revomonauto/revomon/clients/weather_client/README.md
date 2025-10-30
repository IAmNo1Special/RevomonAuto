# WeatherClient

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Comprehensive weather mechanics analysis and strategy optimization system for Revomon, providing weather effects, generation mechanics, and competitive weather strategy analysis.

## 🌤️ Overview

The WeatherClient provides complete weather system analysis including:

- **Weather conditions** and their effects on moves and abilities
- **Weather generation** through abilities, moves, and items
- **Weather strategy optimization** for team building and competitive play
- **Weather counter strategies** and weakness analysis
- **Weather-dependent calculations** for battle simulation
- **Team weather analysis** and weather-based recommendations

## 🌈 Features

### Weather Conditions
- **5 Core Weather Types**: Rain, Sun, Sandstorm, Snow, and Clear
- **Weather Effects**: Move power modifications, accuracy changes, and ability interactions
- **Weather Duration**: Turn-based weather mechanics and control
- **Weather Interactions**: How weather affects different types and moves

### Generation & Control
- **Weather Generators**: Abilities that create or extend weather (Drizzle, Drought, etc.)
- **Weather Moves**: Moves that change weather conditions
- **Weather Items**: Items that affect weather mechanics
- **Weather Control**: Strategies for maintaining or changing weather

### Strategy Analysis
- **Weather Teams**: Analyze teams optimized for specific weather
- **Weather Counters**: Find strategies to counter weather-based teams
- **Weather Optimization**: Optimize team composition for weather conditions
- **Meta Analysis**: Weather usage patterns and competitive strategies

## 🚀 Quick Start

### Basic Weather Analysis

```python
from revomonauto.revomon.clients import WeatherClient, AbilitiesClient

# Initialize clients
weather_client = WeatherClient()
abilities_client = AbilitiesClient()

# Get all weather conditions
weather_conditions = weather_client.get_weather_conditions()
print(f"Available weather: {weather_conditions}")

# Analyze weather effects
effects = weather_client.get_weather_effects("rain")
print(f"Rain effects: {effects}")
```

### Weather Strategy Analysis

```python
# Analyze team for weather optimization
team = [
    {"name": "gorcano", "type1": "ground", "type2": "fire"},
    {"name": "blizzora", "type1": "ice", "type2": "water"},
    {"name": "electra", "type1": "electric"}
]

weather_analysis = weather_client.analyze_weather_strategy(team)
print(f"Optimal weather: {weather_analysis['recommended_weather']}")
print(f"Weather synergy: {weather_analysis['synergy_score']}")
```

### Weather Generation Analysis

```python
# Find weather generators in a team
generators = weather_client.find_weather_generators(team)
print(f"Weather generators found: {len(generators)}")

for generator in generators:
    print(f"- {generator['source']} via {generator['method']}")
```

## 📚 API Reference

### Core Methods

#### `get_weather_conditions()`

Get all available weather conditions in the game.

**Returns:** List of weather condition names

#### `get_weather_effects(weather_name)`

Get effects of a specific weather condition.

**Parameters:**
- `weather_name` (str): Name of the weather condition

**Returns:** Dict with weather effects on moves, types, and abilities

#### `analyze_weather_strategy(team, target_weather=None)`

Analyze team composition for weather strategy optimization.

**Parameters:**
- `team` (list): List of Revomon in the team
- `target_weather` (str): Optional target weather to optimize for

**Returns:** Weather strategy analysis with recommendations

#### `find_weather_generators(team)`

Find weather generation methods in a team.

**Parameters:**
- `team` (list): List of Revomon in the team

**Returns:** List of weather generation methods found

#### `get_weather_counters(weather_name, available_revomon)`

Find optimal counters for weather-based strategies.

**Parameters:**
- `weather_name` (str): Weather condition to counter
- `available_revomon` (list): List of available Revomon

**Returns:** List of optimal weather counters

### Weather Analysis Methods

#### `calculate_weather_synergy(team, weather)`

Calculate how well a team synergizes with specific weather.

**Parameters:**
- `team` (list): Team composition
- `weather` (str): Weather condition

**Returns:** Synergy score and breakdown

#### `analyze_weather_meta()`

Analyze weather usage patterns and meta strategies.

**Returns:** Meta analysis of weather usage and effectiveness

#### `get_weather_dependent_moves(weather)`

Get moves that are affected by specific weather.

**Parameters:**
- `weather` (str): Weather condition

**Returns:** List of moves and their weather modifications

## 🌟 Usage Examples

### Example 1: Weather Strategy Optimization

```python
from revomonauto.revomon.clients import WeatherClient

weather_client = WeatherClient()

# Analyze team for weather optimization
rain_team = [
    {"name": "blizzora", "type1": "ice", "type2": "water"},
    {"name": "electra", "type1": "electric"},
    {"name": "psyche", "type1": "psychic"}
]

rain_analysis = weather_client.analyze_weather_strategy(rain_team, "rain")
print(f"Rain synergy: {rain_analysis['synergy_score']}/100")
print(f"Recommended moves: {rain_analysis['recommended_moves']}")
print(f"Weather benefits: {rain_analysis['weather_benefits']}")
```

### Example 2: Weather Generation Planning

```python
# Plan weather generation for competitive team
sun_team = [
    {"name": "gorcano", "type1": "ground", "type2": "fire"},
    {"name": "draco", "type1": "dragon"},
    {"name": "umbra", "type1": "dark", "type2": "ghost"}
]

generators = weather_client.find_weather_generators(sun_team)
print("Weather Generation Methods:")
for gen in generators:
    print(f"  {gen['method']}: {gen['description']}")
    if gen['source'] == 'ability':
        print(f"    Ability: {gen['ability_name']}")
    elif gen['source'] == 'move':
        print(f"    Move: {gen['move_name']}")
```

### Example 3: Weather Counter Strategy

```python
# Find optimal counters for weather teams
rain_counters = weather_client.get_weather_counters("rain", all_available_revomon)

print("Top Rain Counters:")
for i, counter in enumerate(rain_counters[:5], 1):
    revomon = counter['revomon']
    print(f"{i}. {revomon['name']} (Score: {counter['counter_score']})")
    print(f"   Types: {revomon['type1']}/{revomon.get('type2', 'None')}")
    print(f"   Counter strategy: {counter['strategy']}")
```

### Example 4: Complete Weather Meta Analysis

```python
# Analyze weather patterns in competitive meta
meta_analysis = weather_client.analyze_weather_meta()

print("=== Weather Meta Analysis ===")
print(f"Most common weather: {meta_analysis['most_common_weather']}")
print(f"Weather usage rate: {meta_analysis['usage_rate']}%")

print("\nWeather Effectiveness:")
for weather, effectiveness in meta_analysis['weather_effectiveness'].items():
    print(f"  {weather}: {effectiveness['win_rate']}% win rate")

print("\nPopular Weather Teams:")
for team_type, usage in meta_analysis['popular_combinations'].items():
    print(f"  {team_type}: {usage}% usage")
```

## 🌪️ Weather Types & Effects

### Rain Weather
- **Water moves**: 50% power boost
- **Fire moves**: 50% power reduction
- **Thunder accuracy**: 100% (never misses)
- **Solar Beam**: 50% power reduction

### Sun Weather
- **Fire moves**: 50% power boost
- **Water moves**: 50% power reduction
- **Solar Beam**: 100% power (no charge turn)
- **Thunder accuracy**: 50% (often misses)

### Sandstorm Weather
- **Rock moves**: 50% power boost
- **Non-Rock/Ground/Steel types**: Take damage each turn
- **Special Defense**: Boosted for Rock types

### Snow Weather
- **Ice moves**: 50% power boost
- **Defense**: Boosted for Ice types
- **Freeze chance**: Increased for Ice moves

## 🏆 Advanced Strategies

### Weather Team Building

```python
# Build optimal weather team
def build_weather_team(weather_type, available_revomon, team_size=6):
    analysis = weather_client.analyze_weather_strategy(available_revomon, weather_type)

    # Select best weather generators
    generators = [r for r in available_revomon if weather_client.can_generate_weather(r, weather_type)]

    # Select weather beneficiaries
    beneficiaries = analysis['top_beneficiaries']

    # Combine into optimal team
    team = generators[:2] + beneficiaries[:4]
    return team

# Build rain team
rain_team = build_weather_team("rain", all_revomon)
```

### Weather Control Strategy

```python
# Develop weather control strategy
def develop_weather_control(current_team, target_weather):
    control_methods = weather_client.find_weather_generators(current_team)

    if not control_methods:
        # Recommend adding weather control
        recommendations = weather_client.get_weather_control_recommendations(target_weather)
        return recommendations

    return control_methods

# Get recommendations for sun control
sun_recommendations = develop_weather_control(current_team, "sun")
```

## 📊 Performance

- **Fast analysis**: Optimized weather calculations and team analysis
- **Cached effects**: Weather effects cached for quick access
- **Batch processing**: Support for analyzing multiple teams and weather conditions
- **Memory efficient**: Minimal memory footprint for large team analysis

## 🧪 Testing

```bash
# Run weather tests
uv run python -m pytest tests/clients/test_weather_client.py

# Test weather strategies
uv run python tests/integration/test_weather_strategies.py

# Weather meta analysis tests
uv run python tests/performance/test_weather_analysis.py
```

## 🤝 Contributing

1. Ensure weather effects are accurate to game mechanics
2. Add tests for new weather conditions or effects
3. Update meta analysis when weather strategies evolve
4. Document weather interactions with sources

## 🔄 Version History

### v2.0.0
- Complete weather strategy analysis system
- Weather generation and control mechanics
- Team weather optimization and synergy analysis
- Weather counter strategies and meta analysis
- Comprehensive weather effects database

### v1.0.0
- Basic weather condition lookup
- Simple weather effects
- Individual weather generation methods

---

**Ready to master the weather and dominate the meta? Let the weather analysis begin!** 🌪️⚡🌞
