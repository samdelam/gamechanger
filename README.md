## Game Changer

A template to create slides with simple prompts and a fixed scoreboard that allows players to keep track of their points

## Web version

- If you don't want to install python and streamlit, you can use the [Web Version](https://gamechanger-dropout.streamlit.app/)
  - _The web version is a little laggy, so I do recommend installing and running it locally_
- Make sure you allow autoplay for the webpage on your browser so the sounds play correctly
- On the cover, you'll see a `⚙️` button. Click there to edit the game and Apply the changes when you're done
- Alternatively, you can `Download config.json` file. That file can be imported as a config with the `Upload` button to import all settings next time you visit the page
- The overall structure works on mobile and other devices, but it's not completely responsive, so you might see a few bugs. I recommend using a large monitor or TV to properly display everything

## Installation

- Uses Python and Streamlit: https://docs.streamlit.io/get-started/installation
  - _Built and tested with Python 3.13.5 and Streamlit 1.58.0_

## How to use

- Run `streamlit run app.py`
- Access localhost: http://localhost:8501/ if it didn't open up automatically
- Make sure you allow autoplay for the webpage on your browser so the sounds play correctly
- On the cover, you'll see a `⚙️` button. Click there to edit the game and Apply the changes when you're done
- Alternatively, you can `Download config.json` file. That file can be imported as a config with the `Upload` button to automatically import all settings
- Leaving the exported `config.json` file on the root folder will automatically import the settings when running the code, without the need to import manually
- To change the cover, overwrite the `assets/media/cover` file. Formats accepted are `png`, `jpg`, `jpeg` and `webp`. You can remove the file to automatically jump to the first slide
- To change the audios played, you can overwrite the files in `assets/sounds`

## Credits

- Cover, prompt font and slide change sound: juxtapositionally on [Reddit](https://www.reddit.com/r/GameChangerTV/comments/1feccfu/here_it_is_a_game_changer_powerpoint_template/), files on [Google Drive](https://drive.google.com/drive/folders/1fzeI7gSl5iFhhU4Wv3XM1ihaxa9uAhbB)
- 7-segment display font (DSEG7): [keshikan.net](https://www.keshikan.net/fonts-e.html) and [GitHub](https://github.com/keshikan/DSEG)
- Gain point sound: floraphonic on [pixabay](https://pixabay.com/sound-effects/film-special-effects-copper-bell-ding-25-204990/)
- Lose point sound: eritnhut1992 on [pixabay](https://pixabay.com/sound-effects/film-special-effects-buzzer-or-wrong-answer-20582/)
