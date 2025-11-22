# RevomonAuto

A sophisticated automation framework for the Revomon Android game, built on top of the [BluePyll](https://github.com/bluepyll) automation framework. RevomonAuto provides comprehensive UI automation, intelligent battle AI, and extensive game data access through a modular client system.

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![BluePyll](https://img.shields.io/badge/bluepyll-0.1.16-orange.svg)](https://github.com/bluepyll)

## ✨ Key Features

### 🤖 Automation Capabilities
- **Full App Lifecycle Management** - Automated app opening, closing, and login sequences
- **Comprehensive Menu Navigation** - Navigate all main menus and submenus (Wardrobe, Bag, Friends, Settings, Revodex, Market, Discussion, Clan)
- **PVP Queue Management** - Enter and exit PVP queues automatically
- **TV/PC Navigation** - Search and select Revomon in storage with 30 slot support
- **Action Tracking System** - Full audit trail with before/after state diffs for debugging

### ⚔️ Battle Intelligence
- **OCR-Based Move Extraction** - Real-time extraction of move names with PP tracking
- **Health Monitoring** - Pixel-based HP percentage calculation with 95%+ accuracy
- **Pluggable Battle Strategies** - Extensible Strategy pattern for custom battle AI
- **Auto-Run & Auto-Battle Modes** - Flee from battles automatically or engage with custom logic
- **Real-time Battle Info** - Extract mon names, levels, HP percentages during combat

#### Strategy Pattern
```python
from revomonauto.models.strategies import BattleStrategy

class CustomStrategy(BattleStrategy):
    def select_move(self, valid_move_names: list[str]) -> str:
        # Your custom selection logic
        return chosen_move
```

### 📊 Game Data Access

17+ specialized client libraries providing comprehensive game data access:

#### Core Data Clients
- **RevomonClient** - Search by name, type, ability; access complete Revodex
- **MovesClient** - Physical, special, and status moves with power/accuracy data
- **TypesClient** - Complete type effectiveness matrix
- **AbilitiesClient** - Ability mechanics and descriptions
- **ItemsClient** - Equipment, consumables, and utility items
- **NaturesClient** - Stat modifiers and nature effects

#### Advanced Analytics Clients
- **BattleMechanicsClient** - Damage calculation, STAB, type effectiveness, team coverage analysis
- **EvolutionClient** - Evolution trees, optimal path finding, stat projections
- **WeatherClient** - Weather synergy analysis and strategy optimization
- **StatusEffectsClient** - Status condition management and immunities
- **CounterdexClient** - Counter-strategy and matchup analysis

#### World & Collection Clients
- **LocationsClient** - Spawn locations and encounter rates
- **CapsulesClient** - Capsule mechanics and rewards
- **FruitysClient** - Breeding system data
- **RevomonMovesClient** - Move compatibility per species

---

## 📋 Requirements

- **Python**: 3.13 or higher (uses modern type hints and match-case)
- **Operating System**: Windows (BlueStacks integration)
- **BlueStacks**: Android emulator
- **ADB**: Android Debug Bridge (bundled with BlueStacks)

---

## 🚀 Installation

We recommend using [uv](https://docs.astral.sh/uv/) for package management.

### Install as a Dependency

```bash
uv add revomonauto
```

### Development Setup

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
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .

# Run the example
python examples/main.py
```

---

## 🎯 Quick Start

### Basic Automation Workflow

```python
from bluepyll import BluePyllController
from revomonauto.models.revomon_app import RevomonApp

# Initialize app and controller
revomon_app = RevomonApp()
controller = BluePyllController(apps=[revomon_app])

# Start BlueStacks and open app
controller.bluestacks.open()
controller.revomon.open_revomon_app()

# Login sequence
controller.revomon.start_game()
controller.revomon.login()

# Navigate menus
controller.revomon.open_main_menu()
controller.revomon.open_menu_bag()
controller.revomon.close_menu_bag()
controller.revomon.close_main_menu()

# Enter PVP queue
controller.revomon.enter_pvp_queue()
```

### Battle Automation

```python
# Simple random move selection
while True:
    if controller.revomon.is_on_battle_screen():
        controller.revomon.choose_move()  # Uses RandomMove strategy by default

# Custom strategy
from revomonauto.models.strategies import BattleStrategy

class AlwaysFirstMove(BattleStrategy):
    def select_move(self, valid_move_names):
        return valid_move_names[0] if valid_move_names else None

controller.revomon.choose_move(strategy=AlwaysFirstMove())
```

### Auto-Run & Auto-Battle Modes

```python
# Enable auto-run (flee from all battles automatically)
controller.revomon.auto_run = True

# Enable auto-battle (engage with strategy, no auto-run)
controller.revomon.auto_battle = True

# Manual toggle methods
controller.revomon.toggle_auto_run()
controller.revomon.toggle_auto_battle()
```

### Advanced Battle Strategy Example

```python
from revomonauto.models.strategies import BattleStrategy
from revomonauto.data.gradex_clients import MovesClient, TypesClient

class TypeAdvantageStrategy(BattleStrategy):
    def __init__(self):
        self.moves_client = MovesClient()
        self.types_client = TypesClient()
    
    def select_move(self, valid_move_names):
        # Get move data
        moves = [self.moves_client.get_move_by_name(name) 
                 for name in valid_move_names]
        
        # Prioritize moves by power
        moves_with_power = [(m, m.get('power', 0)) for m in moves]
        moves_with_power.sort(key=lambda x: x[1], reverse=True)
        
        return moves_with_power[0][0]['name'] if moves_with_power else valid_move_names[0]

# Use the strategy
controller.revomon.choose_move(strategy=TypeAdvantageStrategy())
```

### Game Data Analysis

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
print(f"Offensive coverage: {len(coverage['offensive_coverage'])} types")
print(f"Weaknesses: {coverage['weaknesses']}")

# Find optimal evolution path
evolution_client = EvolutionClient()
paths = evolution_client.find_optimal_evolution_path(
    target_stats={"spa": 1.0, "spe": 0.7},
    max_evolutions=3
)
```

---

## 📁 Project Structure

```
RevomonAuto/
├── src/revomonauto/
│   ├── models/
│   │   ├── revomon_app.py       # Main automation controller (2100+ lines)
│   │   ├── states.py            # GameState (15) and BattleState (4) enums
│   │   ├── action.py            # Action tracking with state diffs
│   │   ├── strategies.py        # Battle strategy base classes
│   │   └── revomon_ui/          # UI element definitions
│   │       ├── assets/          # Image templates (PNG) for matching
│   │       │   ├── battle_assets/
│   │       │   ├── login_assets/
│   │       │   ├── main_menu_assets/
│   │       │   └── ... (11 asset directories)
│   │       ├── elements/        # Element definitions by screen
│   │       │   ├── battle_elements.py
│   │       │   ├── main_menu_elements.py
│   │       │   ├── tv_elements.py (30 slot support)
│   │       │   └── ... (11 element files)
│   │       └── screens/         # Screen object models
│   │           ├── battle_screen.py
│   │           ├── main_menu_screen.py
│   │           └── ... (11 screen files)
│   └── data/
│       └── gradex_clients/      # 17+ game data clients
│           ├── base_client.py   # Abstract base with lazy loading
│           ├── revomon_client.py
│           ├── moves_client.py
│           ├── battle_mechanics_client.py
│           └── ... (17+ client files)
├── examples/
│   ├── main.py                  # Full automation workflow
│   └── example_client_usage.py # Data client examples
├── tests/                       # Unit tests
│   ├── test_choose_move.py     # Battle strategy tests
│   ├── test_clients.py         # Client tests
│   └── test_states.py          # State machine tests
├── pyproject.toml               # Modern Python config (uv)
└── README.md                    # This file
```

---

## 🧠 Architecture Deep Dive

### Dual State Machine System

RevomonAuto uses a **hierarchical state machine** with two state enums:

#### GameState (15 states)

Primary state tracking app location:

```python
class GameState(Enum):
    # Login Flow
    NOT_STARTED                 # App not launched
    STARTED                     # Title screen
    
    # Main Game
    OVERWORLD                   # Free roaming
    MAIN_MENU                   # Menu overlay open
    
    # Sub-menus
    MENU_BAG                    # Team/Bag screen
    WARDROBE                    # Cosmetics
    FRIENDS_LIST                # Social
    SETTINGS                    # Game settings
    REVODEX                     # Pokédex equivalent
    MARKET                      # Trading
    DISCUSSION                  # Chat/forums
    CLAN                        # Guild system
    
    # Special States
    PVP_QUEUE                   # Waiting for match
    BATTLE                      # In combat (activates BattleState)
    TV                          # PC/storage interface
```

#### BattleState (4 states)

Sub-state active only when `GameState == BATTLE`:

```python
class BattleState(Enum):
    IDLE                        # Can select action
    ATTACKS_MENU_OPEN           # Move selection visible
    BAG_OPEN                    # Bag menu visible
    WAITING_FOR_OPPONENT        # Turn processing
```

### State Validation

The `@requires_state` decorator enforces state preconditions:

```python
@requires_state(GameState.BATTLE)
@action
def choose_move(self, strategy=None):
    # Only executes if in BATTLE state
    # Logs warning and returns early if wrong state
    ...
```

### Action Tracking System

Every action is automatically logged with:
- **Action ID** - Sequential identifier
- **Status** - Success/failure
- **State Diff** - Before/after comparison of all tracked state variables
- **Error Message** - If action failed
- **Last Action** - Reference to previous action

**Tracked State Variables:**
- `game_state`, `battle_sub_state`
- `current_screen`, `app_state`, `bluestacks_state`
- `tv_current_page`, `tv_slot_selected`, `tv_searching_for`
- `current_city`, `current_location`

**Example Action History:**

```python
# Execute actions
controller.revomon.open_main_menu()
controller.revomon.enter_pvp_queue()

# Review action history
for action in controller.revomon.actions:
    print(f"Action {action['action_id']}: {action['action_name']}")
    print(f"  Status: {action['status']}")
    print(f"  State changes: {action['state_diff']}")
```

**Output:**
```
Action 1: open_main_menu
  Status: True
  State changes: {
      'game_state': {'prev': 'OVERWORLD', 'new': 'MAIN_MENU'}
  }
Action 2: enter_pvp_queue
  Status: True
  State changes: {
      'game_state': {'prev': 'MAIN_MENU', 'new': 'PVP_QUEUE'}
  }
```

### Screen Detection Methods

Each screen implements the Screen Object Pattern:

**Detection Techniques:**
1. **Pixel Color Checking** - Fast checks for specific RGB values at coordinates
2. **Image Template Matching** - OpenCV-based template matching
3. **OCR Text Detection** - EasyOCR for text extraction

**Example: Battle Screen Detection**

```python
class BattleScreen(BluePyllScreen):
    def is_current_screen(self, bluepyll_controller, bluepyll_screenshot=None):
        # Check green pixels in both player nameplates
        player1_nameplate_pixel = self.elements["player1_mon_nameplate_pixel"]
        player2_nameplate_pixel = self.elements["player2_mon_nameplate_pixel"]
        
        return all([
            bluepyll_controller.image.check_pixel_color(
                target_coords=player1_nameplate_pixel.center,
                target_color=player1_nameplate_pixel.pixel_color,
                image=bluepyll_screenshot
            ),
            bluepyll_controller.image.check_pixel_color(
                target_coords=player2_nameplate_pixel.center,
                target_color=player2_nameplate_pixel.pixel_color,
                image=bluepyll_screenshot
            )
        ])
```

### Battle Info Extraction

**HP Percentage Calculation:**
```python
def extract_health_percentage(self, image_path, padding=5):
    # Scans middle row of health bar
    # Counts non-black pixels (health) vs black pixels (missing)
    health_percentage = (health_pixels / total_pixels) * 100
    return health_percentage
```

**Move Data Extraction:**
- OCR extracts move name and PP from button regions
- Post-processing fixes common OCR errors: `"h" → "/"`, `"o" → "0"`, `"t" → "1"`
- Filters moves by PP > 0 for valid selections

---

## 🎲 Creating Custom Battle Strategies

### Strategy Interface

```python
from abc import ABC, abstractmethod

class BattleStrategy(ABC):
    @abstractmethod
    def select_move(self, valid_move_names: list[str]) -> str:
        """
        Selects a move from the list of valid move names.
        
        Args:
            valid_move_names: List of moves with PP > 0
        
        Returns:
            The name of the selected move
        """
        pass
```

### Built-in Strategy

```python
class RandomMove(BattleStrategy):
    """Selects a random move from valid options."""
    
    def select_move(self, valid_move_names):
        if not valid_move_names:
            raise RuntimeError("No valid moves available")
        return random.choice(valid_move_names)
```

### Advanced Strategy Examples

#### Type Effectiveness Strategy

```python
from revomonauto.models.strategies import BattleStrategy
from revomonauto.data.gradex_clients import MovesClient, TypesClient

class TypeEffectivenessStrategy(BattleStrategy):
    def __init__(self, opponent_type):
        self.opponent_type = opponent_type
        self.moves_client = MovesClient()
        self.types_client = TypesClient()
    
    def select_move(self, valid_move_names):
        moves = [self.moves_client.get_move_by_name(name) 
                 for name in valid_move_names]
        
        # Score each move by type effectiveness
        scored_moves = []
        for move in moves:
            effectiveness = self.types_client.get_effectiveness(
                move['type'], self.opponent_type
            )
            power = move.get('power', 0)
            score = effectiveness * power
            scored_moves.append((move['name'], score))
        
        # Return highest scoring move
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return scored_moves[0][0]
```

#### PP Conservation Strategy

```python
class PPConservationStrategy(BattleStrategy):
    """Saves high-PP moves for later, uses low-PP moves first."""
    
    def __init__(self, app):
        self.app = app  # Access to mon_on_field data
    
    def select_move(self, valid_move_names):
        # Get full move data with PP
        moves = [m for m in self.app.mon_on_field["moves"] 
                 if m["name"] in valid_move_names]
        
        # Sort by total PP (ascending) - use weakest first
        moves.sort(key=lambda m: m["pp"]["total"])
        return moves[0]["name"]
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests with uv
uv run pytest

# Run specific test
uv run pytest tests/test_choose_move.py

# Run with coverage
uv run pytest --cov=src/revomonauto

# Run with verbose output
uv run pytest -v
```

### Test Structure

```python
# tests/test_choose_move.py
import unittest
from unittest.mock import MagicMock, patch
from revomonauto.models.revomon_app import RevomonApp
from revomonauto.models.strategies import BattleStrategy

class TestChooseMove(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        with patch("revomonauto.models.revomon_app.BattleScreen"):
            self.app = RevomonApp()
        
        self.app.game_state = GameState.BATTLE
        self.app.mon_on_field = {
            "moves": [
                {"name": "Tackle", "pp": {"current": 10}},
                {"name": "Growl", "pp": {"current": 5}},
                {"name": None, "pp": {"current": 0}},
                {"name": "Scratch", "pp": {"current": 0}}  # No PP
            ]
        }
    
    def test_default_random_strategy(self):
        # Should only select from Tackle or Growl (PP > 0)
        ...
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (automatically ignored by git):

```env
# BlueStacks configuration
BLUESTACKS_PATH=C:\Program Files\BlueStacks_nxt\HD-Player.exe
ADB_PATH=C:\Program Files\BlueStacks_nxt\HD-Adb.exe

# Game credentials (optional, for auto-login)
REVOMON_USERNAME=your_username
REVOMON_PASSWORD=your_password
```

### Runtime Configuration

```python
# Modify behavior at runtime
controller.revomon.auto_run = True      # Flee all battles
controller.revomon.auto_battle = True   # Engage with strategy
```

---

## ⚡ Advanced Examples

### Multi-Account Farming

```python
accounts = [
    {"username": "account1", "password": "pass1"},
    {"username": "account2", "password": "pass2"}
]

for account in accounts:
    # Login with different account
    controller.revomon.login(account)
    
    # Enable auto-run to avoid battles
    controller.revomon.toggle_auto_run()
    
    # Farm for 1 hour
    import time
    time.sleep(3600)
    
    # Logout
    controller.revomon.quit_game()
```

### Team Optimization Analysis

```python
from revomonauto.data.gradex_clients import (
    RevomonClient, 
    EvolutionClient, 
    BattleMechanicsClient
)

# Find Revomon with optimal evolution paths
evolution_client = EvolutionClient()
paths = evolution_client.find_optimal_evolution_path(
    target_stats={"spa": 1.0, "spe": 0.8, "spd": 0.6},
    max_evolutions=3
)

# Build a balanced team
revomon_client = RevomonClient()
battle_client = BattleMechanicsClient()

team = [revomon_client.get_by_primary_key(path['id']) 
        for path in paths[:6]]

# Analyze coverage
coverage = battle_client.analyze_type_coverage(team)
print(f"Offensive coverage: {len(coverage['offensive_coverage'])} types")
print(f"Defensive weaknesses: {coverage['weaknesses']}")
print(f"Coverage score: {coverage.get('coverage_score', 0):.2%}")
```

### Battle Damage Simulation

```python
from revomonauto.data.gradex_clients import BattleMechanicsClient, RevomonClient, MovesClient

battle_client = BattleMechanicsClient()
revomon_client = RevomonClient()
moves_client = MovesClient()

# Get Revomon and move data
attacker = revomon_client.get_revomon_by_name("gorcano")
defender = revomon_client.get_revomon_by_name("blizzora")
move = moves_client.get_move_by_name("earthquake")

# Simulate battle turn
result = battle_client.simulate_battle_turn(
    attacker=attacker,
    defender=defender,
    move_name="earthquake",
    attacker_level=50,
    defender_level=50
)

print(f"Damage: {result['damage']}")
print(f"Type effectiveness: {result['type_effectiveness']}")
print(f"Critical hit: {result['critical_hit']}")
print(f"KO: {result['ko']}")
```

---

## ⚠️ Important Notes

### Game Terms of Service

**⚡ Use at your own risk:** Automation may violate Revomon's Terms of Service

- **Account safety**: No guarantees against detection or bans
- **Recommendation**: Use on alternate accounts and add human-like delays
- **Detection risk**: OCR and pixel checks are detectable if monitored

### Known Limitations

- **OCR Accuracy**: ~95% accuracy, occasional errors in move/name detection
- **Fixed Delays**: Uses 1-second delays for state synchronization (may need adjustment)
- **PVP Queue Detection**: Currently assumes success, no visual confirmation (TODO)
- **Battle End Detection**: Requires manual detection or polling
- **Screen Detection**: May require manual intervention in edge cases

### Performance Considerations

- **Screenshot Overhead**: Each action captures 1-3 screenshots (~100-500ms each)
- **OCR Processing**: Move extraction can take 100-500ms
- **State Polling**: Uses fixed delays, no event-driven detection

---

## 🗺️ Roadmap

### High Priority
- [ ] Background screen detection thread (eliminate polling)
- [ ] Robust PVP queue state detection
- [ ] Battle end detection automation
- [ ] Error recovery and retry logic

### Medium Priority
- [ ] Comprehensive test suite (>80% coverage)
- [ ] Performance optimization (reduce sleep delays)
- [ ] Adaptive timing based on device performance
- [ ] CI/CD pipeline with GitHub Actions

### Future Enhancements
- [ ] Docker support for cross-platform compatibility
- [ ] Web UI for remote monitoring
- [ ] Battle replay system
- [ ] Machine learning battle strategy

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Follow existing code style** (modern Python 3.13+, type hints, docstrings)
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to the branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/RevomonAuto.git
cd RevomonAuto

# Install development dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run linter (if configured)
uv run ruff check .

# Format code (if configured)
uv run ruff format .
```

### Code Style Guidelines

- Use **type hints** for all function signatures
- Write **docstrings** for public methods
- Follow **PEP 8** naming conventions
- Use **modern Python features** (match-case, walrus operator, etc.)
- Keep functions **focused** and **single-purpose**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **BluePyll Framework** - Core automation capabilities built on ADB
- **Revomon Community** - Game data and mechanics information
- **Contributors** - All those who have contributed to this project

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/IAmNo1Special/RevomonAuto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/IAmNo1Special/RevomonAuto/discussions)
- **Email**: ivmno1special@gmail.com

---

## 📊 Project Statistics

- **Total Lines of Code**: ~10,000+
- **Main Controller**: 2,113 lines
- **State Definitions**: 19 states (15 GameState + 4 BattleState)
- **Screen Objects**: 11 screens
- **UI Elements**: 100+ defined elements
- **Data Clients**: 17+ specialized clients
- **Action Methods**: 61 automation methods
- **Python Version**: 3.13+ required
- **Test Coverage**: ~40% (expanding)

---

**Disclaimer**: This project is not affiliated with or endorsed by Revomon. Use at your own risk.

**Version**: 0.3.2 | **Last Updated**: 2025-11-22
