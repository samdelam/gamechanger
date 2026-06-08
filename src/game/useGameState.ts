import { useCallback, useMemo, useState } from 'react'
import type { GameConfig, RuntimePlayer } from '../config/types'

export function buildRuntimePlayers(config: GameConfig): RuntimePlayer[] {
  return config.players.map((player) => ({
    name: player.name,
    score: player.startingScore,
    startingSlide: player.startingSlide,
    canWin: player.canWin,
  }))
}

export function useGameState(config: GameConfig) {
  const [slideIndex, setSlideIndex] = useState(0)
  const [players, setPlayers] = useState<RuntimePlayer[]>(() => buildRuntimePlayers(config))

  const resetPlayersFromConfig = useCallback((nextConfig: GameConfig) => {
    setPlayers(buildRuntimePlayers(nextConfig))
  }, [])

  const visiblePlayers = useMemo(() => players, [players])

  const changeScore = useCallback((playerIndex: number, delta: number) => {
    setPlayers((current) =>
      current.map((player, index) =>
        index === playerIndex ? { ...player, score: player.score + delta } : player,
      ),
    )
  }, [])

  return {
    slideIndex,
    setSlideIndex,
    players: visiblePlayers,
    setPlayers,
    changeScore,
    resetPlayersFromConfig,
  }
}
