## Game Changer

A template to create slides with simple prompts and a fixed scoreboard that allows players to keep track of their points

## Installation

Uses Python and Streamlit: https://docs.streamlit.io/get-started/installation

## How to use

- Create your slides in the file `slides.txt`. Each line is a new slide
- Create your players in the file `players.txt` in the format `Name;StartingPoints`
- Run `streamlit run app.py`
- Access localhost:http://localhost:8501/ if it didn't open up automatically

## Shortcuts

- Keyboard directionals `⬅` and `➡` to navigate between slides
- The player number to subtract a point and Shift+n to increase a point. Eg.:
  - Player 1: `1` to subtract and `Shift+1` to add
  - Player 2: `2` to subtract and `Shift+2` to add
  - etc

_Obs.: The players can be named anything, only their order is used to create the shortcuts_
