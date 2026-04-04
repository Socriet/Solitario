# Solitaire

A Solitaire game built with Python and the [Flet](https://flet.dev/) framework. This project has a graphical user interface, drag-and-drop, and is ready for both desktop and mobile use.

## Features
* **Classic Solitaire Gameplay**: Standard rules with smooth drag-and-drop mechanics.
* **Customizable Rules**: Modify the difficulty by choosing between turning 1 or 3 cards to the waste, and set limits on how many passes through the deck are allowed.
* **Personalization**: Change the table background and card back designs.
* **Live Progress Tracking**: Real-time tracking of your current score, elapsed time, and total moves.
* **Global High Scores**: The game saves your best score, fastest time, and least moves across all sessions.
* **Save & Continue**: Game saves your active game state, plus a manual save button in the top menu bar.
* **Undo Functionality**: Reverse your previous moves, complete with score adjustments.
* **Cross-Platform**: Runs as a web app on desktop and mobile.

## Installation & Running

### Prerequisites
* Python 3.x installed on your system.

### Setup Steps
1. Clone this repository to your local machine:
   ```bash
   git clone <your-repository-url>
   cd solitaire-final
   ```

2. Install the required dependencies using the provided requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:
   ```bash
   python main.py
   ```

## Project Structure
* `main.py`: The start of the app. Contains main menu UI, global high scores, and application routing.
* `solitaire.py`: Contains the game loop, win conditions, saving/loading, and undo logic.
* `card.py`: Defines the `Card` class, drag-and-drop interactions and movement checks.
* `slot.py`: Logic for the different zones on the board (tableau, foundation, waste, stock).
* `layout.py`: Constructs the top AppBar layout, integrating the live counters and menu action buttons.
* `settings.py`: Manages the personalization menu dialog and stores active game configurations.
* `assets/`: Directory containing all graphical assets, including card vectors and web loading icons.

## 🛠️ Built With
* Python - The core programming language.
* Flet - Framework for building interactive multi-platform UI in Python.