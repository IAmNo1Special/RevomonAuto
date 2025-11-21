# RevomonAuto

A powerful automation framework for the Revomon Android game, built on top of the [Bluepyll](https://github.com/bluepyll) automation framework. RevomonAuto provides comprehensive UI automation, battle intelligence, and game data access for Revomon.

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎮 Features

### Automation Capabilities
- **Full App Lifecycle Management**: Automated app opening, closing, and login sequences
- **Menu Navigation**: Navigate all main menus and submenus (Wardrobe, Bag, Friends, Settings, Revodex, Market, Discussion, Clan)
- **PVP Queue Management**: Enter and exit PVP queues automatically
- **Battle Automation**: 
  - OCR-based move extraction with PP tracking
  - Health monitoring via pixel analysis
  - Pluggable battle strategies (Random, Custom AI)
  - Auto-run from battles (background thread)
- **TV/PC Navigation**: Search and select Revomon in storage
- **Action Tracking**: Full audit trail with state diffs for debugging

### Battle Intelligence
- **Real-time OCR**: Extract mon names, levels, HP percentages, and moves
- **Move Validation**: Filter moves by PP availability
- **Strategy Pattern**: Extensible battle AI system
- **Health Bar Analysis**: Pixel-based HP calculation

### Game Data Access
17+ specialized client libraries for querying game data:
- **RevomonClient**: Search by name, type, ability
- **MovesClient**: Physical, special, and status moves
- **BattleMechanicsClient**: Damage calculation, type effectiveness, team coverage analysis
- **EvolutionClient**: Evolution trees and optimal path finding
- **WeatherClient**: Weather synergy analysis
- **StatusEffectsClient**: Status condition strategy
- **TypesClient**, **ItemsClient**, **NaturesClient**, **LocationsClient**, and more

## 📋 Requirements

- **Python**: 3.13 or higher
- **Operating System**: Windows (BlueStacks integration)
- **BlueStacks**: Android emulator
- **ADB**: Android Debug Bridge (included with BlueStacks)

## 🚀 Installation

We recommend using [uv](https://docs.astral.sh/uv/) for package management.

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/IAmNo1Special/RevomonAuto.git
cd RevomonAuto

# Install dependencies with uv
uv sync

# Run the example
uv run examples/main.py
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/IAmNo1Special/RevomonAuto.git
cd RevomonAuto

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the example
python examples/main.py
```

## 🎯 Quick Start

### Basic Automation

```python
from bluepyll import BluePyllController
from revomonauto.models.revomon_app import RevomonApp

# Initialize
controller = BluePyllController()
revomon_app = RevomonApp(controller)

# Start BlueStacks and open app
controller.bluestacks.open()
revomon_app.open_revomon_app()

# Login sequence
revomon_app.start_game()
revomon_app.login()

# Navigate menus
revomon_app.open_main_menu()
revomon_app.open_menu_bag()
revomon_app.close_menu_bag()
revomon_app.close_main_menu()

# Enter PVP queue
revomon_app.enter_pvp_queue()
```

### Battle Automation

```python
# Wait for battle to start, then automate
while True:
    if revomon_app.is_in_battle_scene():
        # Open attacks menu
        revomon_app.open_attacks_menu()
        
        # Choose a random move
        revomon_app.choose_move()
        
        # Or use a custom strategy
        from revomonauto.models.strategies import BattleStrategy
        
        class AlwaysFirstMove(BattleStrategy):
            def select_move(self, valid_move_names):
                return valid_move_names[0]
        
        revomon_app.choose_move(strategy=AlwaysFirstMove())
```

### Auto-Run from Battles

```python
# Enable auto-run (runs from all battles automatically)
revomon_app.toggle_auto_run()

# Your automation continues while battles are automatically escaped
# ...

# Disable when done
revomon_app.toggle_auto_run()
```

### Game Data Access

```python
from revomonauto.data.gradex_clients import (
    RevomonClient,
    MovesClient,
    BattleMechanicsClient,
    EvolutionClient
)

# Initialize clients
revomon_client = RevomonClient()
moves_client = MovesClient()
battle_client = BattleMechanicsClient()

# Find Revomon by type
fire_types = revomon_client.get_revomon_by_type("fire")
print(f"Fire types: {[r['name'] for r in fire_types[:5]]}")

# Get all status moves
status_moves = moves_client.get_status_moves()

# Analyze team type coverage
team = [
    revomon_client.get_revomon_by_name("gorcano"),
    revomon_client.get_revomon_by_name("blizzora")
]
coverage = battle_client.analyze_type_coverage(team)
print(f"Type coverage: {coverage['overall_coverage']:.1%}")

# Find optimal evolution path
evolution_client = EvolutionClient()
paths = evolution_client.find_optimal_evolution_path(
    target_stats={"spa": 1.0, "spe": 0.7},
    max_evolutions=3
)
```

## 📁 Project Structure

```
RevomonAuto/
├── src/revomonauto/
│   ├── models/
│   │   ├── revomon_app.py       # Main automation controller
│   │   ├── states.py            # GameState and BattleState enums
│   │   ├── action.py            # Action tracking system
│   │   ├── strategies.py        # Battle strategy implementations
│   │   └── revomon_ui/          # UI element definitions
│   │       ├── assets/          # Image assets for UI matching
│   │       ├── elements/        # UI element definitions
│   │       └── screens/         # Screen object models
│   └── data/
│       └── gradex_clients/      # Game data client libraries
├── examples/
│   ├── main.py                  # Full automation workflow
│   └── example_client_usage.py # Data client examples
├── tests/                       # Unit tests
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## 🧠 State Management

RevomonAuto uses a dual state machine system for robust automation:

### GameState
- `NOT_STARTED`, `STARTED` - Login flow
- `OVERWORLD` - Free roaming
- `MAIN_MENU` - Menu overlay
- `MENU_BAG`, `WARDROBE`, `FRIENDS_LIST`, `SETTINGS`, `REVODEX`, `MARKET`, `DISCUSSION`, `CLAN` - Submenus
- `PVP_QUEUE` - Waiting for PVP match
- `BATTLE` - In combat
- `TV` - PC/storage interface

### BattleState (Sub-state when in BATTLE)
- `IDLE` - Can attack, use bag, or run
- `ATTACKS_MENU_OPEN` - Move selection visible
- `BAG_OPEN` - Bag menu visible
- `WAITING_FOR_OPPONENT` - Turn being processed

State validation is enforced via the `@requires_state` decorator:

```python
@requires_state(GameState.BATTLE)
@action
def choose_move(self, strategy=None):
    # Only executes if in BATTLE state
    ...
```

## 🎲 Creating Custom Battle Strategies

Extend the `BattleStrategy` abstract base class:

```python
from revomonauto.models.strategies import BattleStrategy
from revomonauto.data.gradex_clients import MovesClient, TypesClient

class SuperEffectiveStrategy(BattleStrategy):
    def __init__(self, opponent_type):
        self.opponent_type = opponent_type
        self.moves_client = MovesClient()
        self.types_client = TypesClient()
    
    def select_move(self, valid_move_names):
        # Get move objects
        moves = [self.moves_client.get_move_by_name(name) 
                 for name in valid_move_names]
        
        # Find super-effective moves
        for move in moves:
            effectiveness = self.types_client.get_effectiveness(
                move['type'], self.opponent_type
            )
            if effectiveness > 1.0:
                return move['name']
        
        # Fallback to first valid move
        return valid_move_names[0]

# Use your custom strategy
revomon_app.choose_move(strategy=SuperEffectiveStrategy("grass"))
```

## 📊 Action Tracking

Every automated action is tracked with full state diffs:

```python
# Execute actions
revomon_app.open_main_menu()
revomon_app.enter_pvp_queue()

# Review action history
for action in revomon_app.actions:
    print(f"Action: {action['action_name']}")
    print(f"Status: {action['status']}")
    print(f"State changes: {action['state_diff']}")
```

Example output:
```
Action: open_main_menu
Status: True
State changes: {
    'game_state': {'prev': 'OVERWORLD', 'new': 'MAIN_MENU'}
}
```

## 🧪 Testing

```bash
# Run tests with uv
uv run pytest

# Run specific test
uv run pytest tests/test_choose_move.py

# Run with coverage
uv run pytest --cov=src/revomonauto
```

## 🔧 Configuration

Create a `.env` file in the project root (not tracked by git):

```env
# BlueStacks configuration
BLUESTACKS_PATH=C:\Program Files\BlueStacks_nxt\HD-Player.exe
ADB_PATH=C:\Program Files\BlueStacks_nxt\HD-Adb.exe

# Game credentials (optional, for auto-login)
REVOMON_USERNAME=your_username
REVOMON_PASSWORD=your_password
```

## ⚠️ Important Notes

### Game Terms of Service
- **Use at your own risk**: Automation may violate Revomon's Terms of Service
- **Account safety**: No guarantees against detection or bans
- **Recommendation**: Use on alternate accounts and add human-like delays

### Limitations
- **Scene detection**: May require manual intervention in some scenarios
- **OCR accuracy**: ~95% accuracy, occasional errors in move/name detection
- **State synchronization**: Uses fixed delays (1 second) which may need adjustment
- **Battle end detection**: Manual input currently required to detect battle completion

## 🗺️ Roadmap

- [ ] Background scene detection thread
- [ ] Robust PVP queue state detection
- [ ] Battle end detection
- [ ] Error recovery and retry logic
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Performance optimization (reduce sleep delays)
- [ ] Docker support

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow existing code style and patterns
4. Add tests for new functionality
5. Update documentation as needed
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/RevomonAuto.git
cd RevomonAuto

# Install development dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Bluepyll Framework**: Core automation capabilities
- **Revomon Community**: Game data and mechanics information
- **Contributors**: All those who have contributed to this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IAmNo1Special/RevomonAuto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/IAmNo1Special/RevomonAuto/discussions)
- **Email**: ivmno1special@gmail.com

## ⚡ Advanced Examples

### Multi-Account Farming

```python
accounts = [
    {"username": "account1", "password": "pass1"},
    {"username": "account2", "password": "pass2"}
]

for account in accounts:
    # Login with different account
    revomon_app.login(account)
    
    # Enable auto-run
    revomon_app.toggle_auto_run()
    
    # Farm for 1 hour
    time.sleep(3600)
    
    # Logout
    revomon_app.quit_game()
```

### Team Optimization

```python
from revomonauto.data.gradex_clients import (
    RevomonClient, EvolutionClient, BattleMechanicsClient
)

# Find Revomon with best special attack evolution path
evolution_client = EvolutionClient()
paths = evolution_client.find_optimal_evolution_path(
    target_stats={"spa": 1.0, "spe": 0.8, "spd": 0.6},
    max_evolutions=3
)

# Build a balanced team
battle_client = BattleMechanicsClient()
team = build_balanced_team(paths[:6])

# Analyze coverage
coverage = battle_client.analyze_type_coverage(team)
print(f"Team covers {coverage['covered_types']}/{coverage['total_types']} types")
```

---

**Disclaimer**: This project is not affiliated with or endorsed by Revomon. Use at your own risk.
