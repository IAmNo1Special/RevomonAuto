# Revomon Client System

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive, modular client system for accessing and analyzing Revomon game data. Built with clean architecture principles for easy maintenance and extensibility.

## 📋 Overview

The Revomon Client System provides a unified interface for accessing various Revomon game datasets including:

- **Revomon species** - Complete Revodex data with stats, types, and evolution chains
- **Moves** - Comprehensive move database with power, accuracy, and effects
- **Abilities** - All Revomon abilities and their mechanics
- **Items** - Equipment, consumables, and utility items
- **Types** - Type system with effectiveness charts
- **Battle mechanics** - Advanced damage calculation and battle simulation
- **Evolution analysis** - Evolution chains, optimization, and meta analysis
- **Weather effects** - Weather mechanics and strategy optimization
- **Status effects** - Status conditions, immunities, and management

## 🏗️ Architecture

### BaseDataClient
All clients inherit from `BaseDataClient`, providing:
- Unified data loading from JSON files
- Caching and performance optimization
- Consistent error handling
- Standardized query methods

### Client Categories

#### Core Data Clients
- **RevomonClient** - Species data and evolution chains
- **MovesClient** - Move database and mechanics
- **AbilitiesClient** - Ability effects and descriptions
- **TypesClient** - Type effectiveness and interactions
- **ItemsClient** - Item database and effects

#### Game Mechanics Clients
- **BattleMechanicsClient** - Damage calculation and battle simulation
- **EvolutionClient** - Evolution analysis and optimization
- **WeatherClient** - Weather mechanics and strategies
- **StatusEffectsClient** - Status condition management

#### World & Collection Clients
- **LocationsClient** - Spawn locations and encounter data
- **CapsulesClient** - Capsule mechanics and rewards
- **FruitysClient** - Fruity system and breeding
- **OwnedLandsClient** - Land ownership and management
- **RevomonMovesClient** - Revomon-specific move compatibility

#### Analysis Clients
- **CounterdexClient** - Counter-strategy and matchup analysis

## 🚀 Quick Start

### Installation

```bash
# Install with uv (recommended)
uv add revomonauto

# Or with pip
pip install revomonauto
```

### Basic Usage

```python
from revomonauto.revomon.clients import RevomonClient, MovesClient

# Initialize clients
revomon_client = RevomonClient()
moves_client = MovesClient()

# Get Revomon data
revomon = revomon_client.get_revomon_by_name("gorcano")
print(f"Found {revomon['name']} with {revomon['stat_total']} total stats")

# Get move data
move = moves_client.get_move_by_name("earthquake")
print(f"Earthquake: {move['power']} power, {move['type']} type")
```

### Advanced Usage

```python
from revomonauto.revomon.clients import BattleMechanicsClient, EvolutionClient

# Battle simulation
battle_client = BattleMechanicsClient()
damage = battle_client.simulate_battle_turn(
    attacker=revomon,
    defender=other_revomon,
    move_name="earthquake",
    attacker_level=50,
    defender_level=50
)

# Evolution analysis
evolution_client = EvolutionClient()
tree = evolution_client.get_complete_evolution_tree(1)
print(f"Evolution tree has {tree['total_members']} members")
```

## 📚 Documentation

Each client has its own detailed README with comprehensive API documentation:

### Core Clients
- [RevomonClient](revomon_client/README.md) - Species data and evolution
- [MovesClient](moves_client/README.md) - Move database
- [AbilitiesClient](abilities_client/README.md) - Ability mechanics
- [TypesClient](types_client/README.md) - Type system
- [ItemsClient](items_client/README.md) - Item database

### Advanced Clients
- [BattleMechanicsClient](battle_mechanics_client/README.md) - Battle simulation
- [EvolutionClient](evolution_client/README.md) - Evolution analysis
- [WeatherClient](weather_client/README.md) - Weather strategies
- [StatusEffectsClient](status_effects_client/README.md) - Status management

### World Clients
- [LocationsClient](locations_client/README.md) - Spawn and encounter data
- [CapsulesClient](capsules_client/README.md) - Capsule mechanics
- [FruitysClient](fruitys_client/README.md) - Breeding system
- [OwnedLandsClient](owned_lands_client/README.md) - Land management
- [RevomonMovesClient](revomon_moves_client/README.md) - Move compatibility

### Analysis Clients
- [CounterdexClient](counterdex_client/README.md) - Counter-strategies

## 🔧 Development

### Project Structure

```
src/revomonauto/revomon/clients/
├── __init__.py                 # Client exports
├── base_client.py              # Base client class
├── revomon_client.py           # Revomon species data
├── moves_client.py             # Move database
├── abilities_client.py         # Ability mechanics
├── types_client.py             # Type effectiveness
├── items_client.py             # Item database
├── battle_mechanics_client.py  # Battle simulation
├── evolution_client.py         # Evolution analysis
├── weather_client.py           # Weather strategies
├── status_effects_client.py    # Status management
├── locations_client.py         # Location data
├── capsules_client.py          # Capsule mechanics
├── fruitys_client.py           # Breeding system
├── owned_lands_client.py       # Land management
├── revomon_moves_client.py     # Move compatibility
└── counterdex_client.py        # Counter analysis
```

### Adding New Clients

1. Inherit from `BaseDataClient`
2. Implement required methods (`get_primary_key_field()`)
3. Add to `__init__.py` exports
4. Create client-specific README
5. Add comprehensive tests

### Testing

```bash
# Run all client tests
uv run python -m pytest tests/clients/

# Test specific client
uv run python tests/clients/test_revomon_client.py

# Integration tests
uv run python tests/integration/test_client_system.py
```

## 🤝 Contributing

1. Follow existing code style and patterns
2. Add comprehensive docstrings
3. Include unit tests for new functionality
4. Update README documentation
5. Ensure all tests pass before submitting

See individual client READMEs for specific contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: See individual client READMEs
- **Examples**: Check `example_usage.py` for comprehensive examples

## 🔄 Version History

### v2.0.0 (Current)
- Complete client system with 17 specialized clients
- Advanced battle mechanics and evolution analysis
- Comprehensive weather and status effect systems
- Full type effectiveness and counter-strategy analysis

### v1.0.0
- Basic client system with core data access
- Simple Revomon and move lookups
- Basic type and ability information

---

**Ready to explore the Revomon universe? Start with the [RevomonClient](revomon_client/README.md) to discover amazing creatures!**
