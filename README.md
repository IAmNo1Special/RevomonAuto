# RevomonAuto

Automation helpers for the Revomon Android game running under BlueStacks, built on top of the Bluepyll automation framework.

This repository provides a state-machine-driven controller (`RevoAppController`) and a ready-to-run demo script (`test.py`) that exercises typical in-game flows like launching the app, logging in, navigating menus, interacting with the TV, and running basic battle actions.

## Requirements

- Python 3.13+ (project targets `>=3.13` per `pyproject.toml`)
- Windows (tested) with BlueStacks installed

## Installation (UV only)

1. Create and activate a virtual environment:

```powershell
uv venv
# On PowerShell
. .\.venv\Scripts\Activate.ps1
```

1. Install dependencies declared in `pyproject.toml` / `uv.lock`:

```powershell
uv sync
```

1. Verify your Python version is 3.13+:

```powershell
python -V
```

## Project layout

- `src/revomonauto/controllers/revo_controller.py`
   High-level automation API. Inherits from `BluepyllController` and `RevomonApp`. Exposes actions such as `open_revomon_app()`, `start_game()`, `log_in()`, `open_main_menu()`, `open_tv()`, `open_attacks_menu()`, `run_from_battle()`, etc.

- `src/revomonauto/models/revo_app.py`
  App model and state machines: `LoginState`, `BattleState`, `MenuState`, `TVState`. Holds contextual attributes like `tv_current_page`, `tv_slot_selected`, `current_city`, and an `Event` for auto-run.

- `src/revomonauto/models/action.py`
  Action logging utilities:
  - `Action`: dict-like fixed schema for per-action results.
  - `Actions`: list-like container that only accepts `Action`.
  - `@action` decorator: wraps controller methods to capture state diffs and append to `controller.actions` after `wait_for_action()`.

- `src/revomonauto/revomon/revomon_ui.py`
  Static UI descriptors as `UIElement` instances with image template paths, screen `position` and `size`. These drive `click_ui(...)` targeting and define OCR regions for battle info extraction.

- `test.py`
  Example script showing the intended usage of `RevoAppController` end-to-end.

## Running the demo

From the repository root:

```powershell
uv run test.py
```

`test.py` will:

- Instantiate `RevoAppController`.
- Open the Revomon app, start the game, and log in.
- Open/close the main menu and navigate submenus (PVP, Wardrobe, Team/Bag, Friends, Settings, Revodex, Market, Discussion, Clan).
- Interact with the TV (select slots, search for a Revomon).
- In battle: open the attacks menu, OCR current moves, open/close the battle bag, and run from battle.
- Log every action and final `controller.actions` (which includes state diffs).

## How it works

- Controller methods in `revo_controller.py` are annotated with `@action` from `models/action.py`. The decorator:
  - Snapshots state before and after each method call.
  - Calls `self.wait_for_action(action=...)` to let Bluepyll observe the UI state change.
  - Appends a structured `Action` with a `state_diff` into `controller.actions`.

- UI automation is delegated to Bluepyll via methods inherited from `BluepyllController`, including:
  - `click_ui([UIElement, ...], max_tries=...)`
  - `click_coords((x, y))`
  - `capture_screenshot()`
  - App lifecycle helpers: `open_app(app=self, ...)`, `close_app(app=self)`

- OCR flows (battle info):
  - `extract_regions(...)` crops regions from screenshots and saves them to `src/revomonauto/revomon/battles/{label}.png`.
  - The controller then calls `self.img_txt_checker.read_text(path, allowlist=...)` (provided by Bluepyll) to parse text from those images.
  - `extract_health_percentage(...)` scans a midline of the health bar image to estimate percentage filled.

## Adding new automation

1. Define new UI targets in `src/revomonauto/revomon/revomon_ui.py` as `UIElement` entries with accurate `path`, `position`, `size`, and optional `confidence`/`ele_txt`.
2. Implement a controller method in `src/revomonauto/controllers/revo_controller.py`:
   - Decorate with `@action`.
   - Gate behavior on the appropriate state machines (see `models/revo_app.py`).
   - Use Bluepyll helpers like `click_ui`, `click_coords`, and `capture_screenshot`.
3. Update or create a script like `test.py` to exercise the new flow.

## Logs and artifacts

- The demo logs to console and a timestamped file (from `test.py`).
- OCR crops are saved under `src/revomonauto/revomon/battles/` by label.
- If interactions fail, check `controller.actions` at the end of a run to inspect state diffs and the last successful step.

## Troubleshooting

- BlueStacks not detected / ADB not connected:
  - Ensure BlueStacks is installed and running.
  - Bluepyll should auto-connect ADB; check logs for ADB connection attempts.

- UI element not found:
  - Verify your BlueStacks resolution matches what the UI element coordinates expect (the project assumes 1920x1080 based on positions in `revomon_ui.py`).
  - Confirm template image paths exist under `src/revomonauto/revomon/game_ui/...` and have sufficient `confidence`.

- OCR results are noisy:
  - Inspect the cropped images in `src/revomonauto/revomon/battles/`.
  - Adjust region `position`/`size` in `revomon_ui.py` or refine post-processing in the controller.

## License
