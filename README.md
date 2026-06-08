## Game Changer

A template to create slides with simple prompts and a fixed scoreboard that allows players to keep track of their points

## Requirements

- [Node.js](https://nodejs.org/en/download)
- npm (installed with node)
  - _Built and tested with node v25.0.0_

## Run locally

```bash
npm install
npm run dev
```

Open the local URL shown by Vite, usually `http://localhost:5173/`.

## Configuration

- Make sure you allow autoplay for the webpage on your browser so the sounds play correctly
- On the cover, you'll see a `⚙️` button. Click there (or press `S`) to edit the game and `Apply` the changes when you're done
- Settings are saved on your local storage on your browser
- Alternatively, you can `Download config.json` file. That file can later be imported with the button on the top right of the settings page to automatically import all settings
  - _When making lots of changes, such as creating players and prompts, make sure to export this file as a backup_
- Leaving the exported `config.json` file on the `public` folder will automatically import the settings when running the code, however, local storage still has a higher priority
- To change the audios played, you can overwrite the files in `public/assets/sounds`

## Credits

- Cover, prompt font and slide change sound: juxtapositionally on [Reddit](https://www.reddit.com/r/GameChangerTV/comments/1feccfu/here_it_is_a_game_changer_powerpoint_template/), files on [Google Drive](https://drive.google.com/drive/folders/1fzeI7gSl5iFhhU4Wv3XM1ihaxa9uAhbB)
- 7-segment display font (DSEG7): [keshikan.net](https://www.keshikan.net/fonts-e.html) and [GitHub](https://github.com/keshikan/DSEG)
- Gain point sound: floraphonic on [pixabay](https://pixabay.com/sound-effects/film-special-effects-copper-bell-ding-25-204990/)
- Lose point sound: eritnhut1992 on [pixabay](https://pixabay.com/sound-effects/film-special-effects-buzzer-or-wrong-answer-20582/)
