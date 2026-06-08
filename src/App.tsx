import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { AudioManager } from './audio/audioManager'
import { defaultConfig } from './config/defaultConfig'
import { clearStoredConfig, loadRootConfig, loadStoredConfig, saveStoredConfig } from './config/configStorage'
import type { GameConfig } from './config/types'
import { Scoreboard } from './game/Scoreboard'
import { SlideView } from './game/SlideView'
import { buildRuntimePlayers, useGameState } from './game/useGameState'
import { SettingsEditor } from './settings/SettingsEditor'
import { useKeyboardShortcuts } from './keyboard/useKeyboardShortcuts'
import { useVisualViewportHeight } from './hooks/useVisualViewportHeight'

function getTextSlideOffset(hasCover: boolean): number {
  return hasCover ? 1 : 0
}

function defaultCoverSrc(): string {
  return `${import.meta.env.BASE_URL}assets/media/cover.png`
}

export function App() {
  useVisualViewportHeight()

  const [config, setConfig] = useState<GameConfig>(defaultConfig)
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [hasCover, setHasCover] = useState(false)
  const [coverLoaded, setCoverLoaded] = useState<boolean | null>(null)
  const [coverSrc, setCoverSrc] = useState<string | null>(null)
  const audioManager = useRef(new AudioManager(import.meta.env.BASE_URL))
  const lastSlideIndex = useRef(0)

  const {
    slideIndex,
    setSlideIndex,
    players,
    setPlayers,
    changeScore,
    resetPlayersFromConfig,
  } = useGameState(config)

  const textSlideOffset = getTextSlideOffset(hasCover)
  const isCoverSlide = hasCover && slideIndex === 0
  const maxSlide = (config.winner.enabled ? config.slides.content.length : config.slides.content.length - 1) + textSlideOffset

  useEffect(() => {
    let cancelled = false

    async function loadInitialConfig() {
      const stored = loadStoredConfig()
      if (stored) {
        if (!cancelled) {
          setConfig(stored)
          resetPlayersFromConfig(stored)
          setSlideIndex(0)
        }
        return
      }

      const root = await loadRootConfig()
      if (root && !cancelled) {
        setConfig(root)
        resetPlayersFromConfig(root)
        setSlideIndex(0)
      }
    }

    loadInitialConfig()
    return () => {
      cancelled = true
    }
  }, [resetPlayersFromConfig, setSlideIndex])

  useEffect(() => {
    if (!config.cover.enabled) {
      setHasCover(false)
      setCoverLoaded(false)
      setCoverSrc(null)
      return
    }

    if (config.cover.imageDataUrl) {
      setHasCover(true)
      setCoverLoaded(true)
      setCoverSrc(config.cover.imageDataUrl)
      return
    }

    let cancelled = false
    const image = new Image()
    const src = defaultCoverSrc()

    image.onload = () => {
      if (cancelled) return
      setHasCover(true)
      setCoverLoaded(true)
      setCoverSrc(src)
    }
    image.onerror = () => {
      if (cancelled) return
      setHasCover(false)
      setCoverLoaded(false)
      setCoverSrc(null)
    }
    image.src = src

    return () => {
      cancelled = true
    }
  }, [config.cover.enabled, config.cover.imageDataUrl])

  useEffect(() => {
    setSlideIndex((current) => Math.min(current, Math.max(0, maxSlide)))
  }, [maxSlide, setSlideIndex])

  useEffect(() => {
    if (slideIndex !== lastSlideIndex.current && config.slides.sounds.slide) {
      const winnerIndex = config.slides.content.length + textSlideOffset
      const isWinnerSlide = config.winner.enabled && slideIndex === winnerIndex
      if (!isWinnerSlide) audioManager.current.playSlide()
    }
    lastSlideIndex.current = slideIndex
  }, [slideIndex, config.slides.sounds.slide, config.winner.enabled, config.slides.content.length, textSlideOffset])

  const visiblePlayers = useMemo(
    () => players.filter((player) => slideIndex >= player.startingSlide + textSlideOffset - 1),
    [players, slideIndex, textSlideOffset],
  )

  const nextSlide = useCallback(() => {
    audioManager.current.unlock()
    setSlideIndex((current) => Math.min(current + 1, maxSlide))
  }, [maxSlide, setSlideIndex])

  const previousSlide = useCallback(() => {
    audioManager.current.unlock()
    setSlideIndex((current) => Math.max(current - 1, 0))
  }, [setSlideIndex])

  const openSettings = useCallback(() => {
    audioManager.current.unlock()
    setSettingsOpen(true)
  }, [])

  const addPoint = useCallback((visiblePlayerIndex: number) => {
    const player = visiblePlayers[visiblePlayerIndex]
    if (!player) return
    const runtimeIndex = players.indexOf(player)
    if (runtimeIndex < 0) return

    changeScore(runtimeIndex, 1)
    if (config.scoreboard.sounds.gainPoints) {
      audioManager.current.playGain(config.scoreboard.sounds.gainPointsDelaySeconds)
    }
  }, [changeScore, config.scoreboard.sounds.gainPoints, config.scoreboard.sounds.gainPointsDelaySeconds, players, visiblePlayers])

  const removePoint = useCallback((visiblePlayerIndex: number) => {
    const player = visiblePlayers[visiblePlayerIndex]
    if (!player) return
    const runtimeIndex = players.indexOf(player)
    if (runtimeIndex < 0) return

    changeScore(runtimeIndex, -1)
    if (config.scoreboard.sounds.losePoints) {
      audioManager.current.playLose(config.scoreboard.sounds.losePointsDelaySeconds)
    }
  }, [changeScore, config.scoreboard.sounds.losePoints, config.scoreboard.sounds.losePointsDelaySeconds, players, visiblePlayers])

  useKeyboardShortcuts({
    enabled: !settingsOpen,
    config,
    visiblePlayerCount: visiblePlayers.length,
    onNextSlide: nextSlide,
    onPreviousSlide: previousSlide,
    onOpenSettings: openSettings,
    onAddPoint: addPoint,
    onRemovePoint: removePoint,
    unlockAudio: () => audioManager.current.unlock(),
  })

  const applySettings = (nextConfig: GameConfig) => {
    setConfig(nextConfig)
    saveStoredConfig(nextConfig)
    setPlayers((currentPlayers) => {
      const nextPlayers = buildRuntimePlayers(nextConfig)
      return nextPlayers.map((nextPlayer) => {
        const current = currentPlayers.find((player) => player.name === nextPlayer.name)
        return current ? { ...nextPlayer, score: current.score } : nextPlayer
      })
    })
    setSlideIndex((current) => {
      const offset = getTextSlideOffset(hasCover)
      const nextMaxSlide = (nextConfig.winner.enabled ? nextConfig.slides.content.length : nextConfig.slides.content.length - 1) + offset
      return Math.min(current, Math.max(0, nextMaxSlide))
    })
    setSettingsOpen(false)
  }

  const resetLocalSettings = () => {
    clearStoredConfig()
    setConfig(defaultConfig)
    resetPlayersFromConfig(defaultConfig)
    setSlideIndex(0)
    setSettingsOpen(false)
  }

  if (settingsOpen) {
    return (
      <SettingsEditor
        config={config}
        onApply={applySettings}
        onCancel={() => setSettingsOpen(false)}
        onResetDefaults={resetLocalSettings}
      />
    )
  }

  return (
    <div
      className={`game-shell ${config.scoreboard.enabled && !isCoverSlide ? 'with-scoreboard' : 'without-scoreboard'}`}
      onPointerDown={() => audioManager.current.unlock()}
    >
      <SlideView
        slideIndex={slideIndex}
        slides={config.slides.content}
        hasCover={hasCover}
        coverLoaded={coverLoaded}
        coverSrc={coverSrc}
        winnerEnabled={config.winner.enabled}
        winnerConfig={config.winner}
        players={players}
        slideButtonsVisible={config.slides.buttons.slide}
        settingsButtonVisible={config.slides.buttons.settings}
        onPrevious={previousSlide}
        onNext={nextSlide}
        onOpenSettings={openSettings}
      />

      <Scoreboard
        enabled={config.scoreboard.enabled}
        isCoverSlide={isCoverSlide}
        players={players}
        slideIndex={slideIndex}
        textSlideOffset={textSlideOffset}
        config={config.scoreboard}
        onAddPoint={addPoint}
        onRemovePoint={removePoint}
      />
    </div>
  )
}
