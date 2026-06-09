import type { KeyboardEvent, PointerEvent } from 'react'
import type { RuntimePlayer, ScoreboardConfig } from '../config/types'

type Props = {
  enabled: boolean
  isCoverSlide: boolean
  players: RuntimePlayer[]
  slideIndex: number
  textSlideOffset: number
  config: ScoreboardConfig
  onAddPoint: (playerIndex: number) => void
  onRemovePoint: (playerIndex: number) => void
}

function handleScorePointerUp(
  event: PointerEvent<HTMLButtonElement>,
  action: () => void,
) {
  // In mobile/responsive browser emulation, a fast mouse/tap interaction can
  // produce compatibility click behavior in addition to pointer events. Score
  // buttons use pointerup as the single source of truth and do not use onClick,
  // which prevents one physical tap/click from being counted more than once.
  if (event.pointerType === 'mouse' && event.button !== 0) return

  event.preventDefault()
  event.stopPropagation()
  action()
}

function handleScoreKeyDown(
  event: KeyboardEvent<HTMLButtonElement>,
  action: () => void,
) {
  if (event.key !== 'Enter' && event.key !== ' ') return

  event.preventDefault()
  event.stopPropagation()
  action()
}

export function Scoreboard({
  enabled,
  isCoverSlide,
  players,
  slideIndex,
  textSlideOffset,
  config,
  onAddPoint,
  onRemovePoint,
}: Props) {
  if (!enabled || isCoverSlide) return null

  const visiblePlayers = players.filter(
    (player) => slideIndex >= player.startingSlide + textSlideOffset - 1,
  )

  if (visiblePlayers.length === 0) return null

  return (
    <footer className={`scoreboard ${config.buttons.points ? 'with-score-buttons' : 'without-score-buttons'}`}>
      <div className="scoreboard-row" style={{ gridTemplateColumns: `repeat(${visiblePlayers.length}, minmax(0, 1fr))` }}>
        {visiblePlayers.map((player, index) => (
          <div className="scoreboard-player" key={`${player.name}-${index}`}>
            <h2>{player.name}</h2>
            <div className="score-value">{player.score}</div>
            {config.buttons.points && (
              <div className="score-buttons">
                <button
                  type="button"
                  className="score-button"
                  onPointerUp={(event) => handleScorePointerUp(event, () => onRemovePoint(index))}
                  onKeyDown={(event) => handleScoreKeyDown(event, () => onRemovePoint(index))}
                  aria-label={`Remove point from ${player.name}`}
                >
                  <span className="score-button-symbol score-button-symbol-minus" aria-hidden="true" />
                </button>
                <button
                  type="button"
                  className="score-button"
                  onPointerUp={(event) => handleScorePointerUp(event, () => onAddPoint(index))}
                  onKeyDown={(event) => handleScoreKeyDown(event, () => onAddPoint(index))}
                  aria-label={`Add point to ${player.name}`}
                >
                  <span className="score-button-symbol score-button-symbol-plus" aria-hidden="true" />
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </footer>
  )
}
