export type PlayerConfig = {
  name: string
  startingScore: number
  startingSlide: number
  canWin: boolean
}

export type SlidesConfig = {
  content: string[]
  buttons: {
    slide: boolean
    settings: boolean
  }
  shortcuts: {
    next: string
    previous: string
    settings: string
  }
  sounds: {
    slide: boolean
  }
}

export type ScoreboardConfig = {
  enabled: boolean
  buttons: {
    points: boolean
  }
  shortcuts: {
    pointsModifier: string
    pointsInverted: boolean
  }
  sounds: {
    gainPoints: boolean
    gainPointsDelaySeconds: number
    losePoints: boolean
    losePointsDelaySeconds: number
  }
}

export type CoverConfig = {
  enabled: boolean
  imageDataUrl: string
}

export type AssetsConfig = {
  sounds: {
    slideDataUrl: string
    gainPointsDataUrl: string
    losePointsDataUrl: string
  }
}

export type WinnerConfig = {
  enabled: boolean
  single: {
    title: string
    scoreText: string
  }
  multiple: {
    title: string
    separator: string
    scoreText: string
  }
}

export type GameConfig = {
  players: PlayerConfig[]
  slides: SlidesConfig
  scoreboard: ScoreboardConfig
  cover: CoverConfig
  assets: AssetsConfig
  winner: WinnerConfig
}

export type RuntimePlayer = {
  name: string
  score: number
  startingSlide: number
  canWin: boolean
}
