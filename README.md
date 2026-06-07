## Game Changer

A template to create slides with simple prompts and a fixed scoreboard that allows players to keep track of their points

## Installation

Uses Python and Streamlit: https://docs.streamlit.io/get-started/installation

## How to use

- Upload your own first-slide (cover) image with the file name `cover`. Formats accepted are `png`, `jpg`, `jpeg` and `webp`
- Create your slides in the file `slides.txt`. Each line is a new slide
- The `config.json` file allows you to edit several components of the game
  - Create your players in the file config file, in the `players` section
    - _`starting_slide` is used if you want to introduce a player or a counter mid-game, such as a Swear Jar_
    - _`can_win` is a boolean (`true` or `false`) to determine if you want a player to be able to win in the tally made at the last slide (for example, the Swear Jar shouldn't be crowned the winner)_
  - You can enable and disable sounds in the `sounds` section, by changing `true` to `false` in some elements
  - You can also control the delay between changing points and having the sound be played with the `lose_points_delay_seconds` value (in seconds)
    - _Multiple points being deducted will only play one sound after a certain time has passed without points being deducted. Same for increasing points_
  - You can show or hide clickable buttons for changing slides or controlling players points in the `buttons` section
  - You can change shortcuts in the `shortcuts` section
    - By default, keyboard directionals `⬅` and `➡` are used to navigate between slides
    - The player position `n` in the `players` section to add a point and `Shift+n` to subtract a point. Eg.:
      - Player 1: `1` to add and `Shift+1` to subtract
      - Player 2: `2` to add and `Shift+2` to subtract
    - `points_modifier` can be used to change what modifier will be used to swap between adding and subtracting points (Eg.: `"Alt"`)
    - `points_inverted` can be used to make it so the number alone is used as a shortcut to subtract and the modifier is used to add (useful for Sam Says, in which you'll be subtracting more points than adding)
  - For localization purposes, edit the `winner` section in the config file to change what shows up on the last slide that will determine the winner
    - _You can change the `enabled` to `false` to remove the winner slide completely_
- Run `streamlit run app.py`
- Access localhost:http://localhost:8501/ if it didn't open up automatically
- If you change anything in the `config.json` file, reload the browser to apply the changes

## Credits

- Cover, prompt font and slide change sound: Alex on [Reddit](https://www.reddit.com/r/GameChangerTV/comments/1feccfu/here_it_is_a_game_changer_powerpoint_template/), files on [Google Drive](https://drive.google.com/drive/folders/1fzeI7gSl5iFhhU4Wv3XM1ihaxa9uAhbB)
- 7-segment display font (DSEG7): [keshikan.net](https://www.keshikan.net/fonts-e.html) and [GitHub](https://github.com/keshikan/DSEG)
