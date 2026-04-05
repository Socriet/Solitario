# Flet Solitaire

A Klondike Solitaire game built with the [Flet](https://flet.dev/) Python UI framework, running as a web application.

## Project Structure

- `main.py` — App entry point, main menu, high scores, routing
- `solitaire.py` — Core game logic (game loop, win conditions, undo, save/load)
- `card.py` — Card class with drag-and-drop interactions and move validation
- `slot.py` — Tableau, foundation, waste, and stock pile zones
- `layout.py` — App bar with live counters (score, time, moves)
- `settings.py` — Game settings (draw 1 vs draw 3, background color, card backs)
- `assets/` — SVG/PNG card images and app icons
- `requirements.txt` — Python dependencies

## Running the App

```bash
pip install -r requirements.txt
python main.py
```

The app runs on port **5000** in web browser mode (`ft.AppView.WEB_BROWSER`).

## Dependencies

- `flet==0.84.0` — Python UI framework
- `flet-web==0.84.0` — Web server support for Flet

## State Persistence

- `savegame.json` — Current game state (auto-saved)
- `global_stats.json` — High scores (best score, fastest time, fewest moves)

## Workflow

- **Start application**: `python main.py` → port 5000 (webview)
