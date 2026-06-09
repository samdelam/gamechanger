import type { GameConfig } from './types'

export const defaultConfig: GameConfig = {
  slides: {
    content: [
      'FIRST PROMPT',
      'NEXT SLIDE IS EMPTY',
      '',
      'A VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY VERY BIG PROMPT',
      "DON'T SWEAR",
      'END OF GAME',
    ],
    buttons: {
      slide: true,
      settings: true,
    },
    shortcuts: {
      next: 'ArrowRight',
      previous: 'ArrowLeft',
      settings: 's',
    },
    sounds: {
      slide: true,
    },
  },
  players: [
    { name: 'VIC', startingScore: 50, startingSlide: 1, canWin: true },
    { name: 'JACOB', startingScore: 50, startingSlide: 1, canWin: true },
    { name: 'LOU', startingScore: 50, startingSlide: 1, canWin: true },
    { name: 'SWEAR JAR', startingScore: 0, startingSlide: 5, canWin: false },
  ],
  scoreboard: {
    enabled: true,
    buttons: {
      points: true,
    },
    shortcuts: {
      pointsModifier: 'Shift',
      pointsInverted: false,
    },
    sounds: {
      gainPoints: true,
      gainPointsDelaySeconds: 0.5,
      losePoints: true,
      losePointsDelaySeconds: 0.5,
    },
  },
  cover: {
    enabled: true,
    imageDataUrl: '',
  },
  assets: {
    sounds: {
      slideDataUrl: '',
      gainPointsDataUrl: '',
      losePointsDataUrl: '',
    },
  },
  winner: {
    enabled: true,
    single: {
      title: 'AND THE WINNER IS:',
      scoreText: 'WITH {score} POINTS',
    },
    multiple: {
      title: 'AND THE WINNERS ARE:',
      separator: 'AND',
      scoreText: 'WITH {score} POINTS',
    },
  },
}
