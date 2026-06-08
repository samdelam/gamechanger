import type { RuntimePlayer, WinnerConfig } from '../config/types'

type Props = {
  slideIndex: number
  slides: string[]
  hasCover: boolean
  coverLoaded: boolean | null
  coverSrc: string | null
  winnerEnabled: boolean
  winnerConfig: WinnerConfig
  players: RuntimePlayer[]
  slideButtonsVisible: boolean
  settingsButtonVisible: boolean
  onPrevious: () => void
  onNext: () => void
  onOpenSettings: () => void
}

function textSlideOffset(hasCover: boolean): number {
  return hasCover ? 1 : 0
}

function textFontSize(text: string): number {
  if (!text) return 15
  return Math.max(4.5, Math.min(15, 70 / Math.sqrt(text.length)))
}

function WinnerScreen({ players, winnerConfig }: { players: RuntimePlayer[]; winnerConfig: WinnerConfig }) {
  const eligible = players.filter((player) => player.canWin)
  if (eligible.length === 0) {
    return <div className="winner-title">NO ELIGIBLE WINNERS</div>
  }

  const highestScore = Math.max(...eligible.map((player) => player.score))
  const winners = eligible.filter((player) => player.score === highestScore).map((player) => player.name)

  let title = winnerConfig.single.title
  let names = winners[0]
  let score = winnerConfig.single.scoreText.replace('{score}', String(highestScore))

  if (winners.length > 1) {
    title = winnerConfig.multiple.title
    score = winnerConfig.multiple.scoreText.replace('{score}', String(highestScore))
    const separator = winnerConfig.multiple.separator
    names = winners.length === 2
      ? `${winners[0]} ${separator} ${winners[1]}`
      : `${winners.slice(0, -1).join(', ')} ${separator} ${winners[winners.length - 1]}`
  }

  return (
    <div className="winner-screen">
      <div className="winner-title">{title}</div>
      <div className="winner-names">{names}</div>
      <div className="winner-score">{score}</div>
    </div>
  )
}

export function SlideView({
  slideIndex,
  slides,
  hasCover,
  coverLoaded,
  coverSrc,
  winnerEnabled,
  winnerConfig,
  players,
  slideButtonsVisible,
  settingsButtonVisible,
  onPrevious,
  onNext,
  onOpenSettings,
}: Props) {
  const offset = textSlideOffset(hasCover)
  const isCoverSlide = hasCover && slideIndex === 0
  const winnerIndex = slides.length + offset
  const isWinnerSlide = winnerEnabled && slideIndex === winnerIndex
  const textIndex = slideIndex - offset
  const currentSlide = textIndex >= 0 && textIndex < slides.length ? slides[textIndex] : ''
  const maxSlide = (winnerEnabled ? slides.length : slides.length - 1) + offset

  return (
    <main className={`slide-card ${isCoverSlide ? 'cover-slide' : ''}`}>
      {coverLoaded !== false && (
        <img
          className="cover-preload"
          src={coverSrc ?? ''}
          alt=""
          onLoad={() => undefined}
        />
      )}

      {isCoverSlide ? (
        coverSrc ? <img className="cover-image" src={coverSrc} alt="Cover" /> : null
      ) : isWinnerSlide ? (
        <WinnerScreen players={players} winnerConfig={winnerConfig} />
      ) : (
        <div className="slide-text" style={{ fontSize: `${textFontSize(currentSlide)}vmin` }}>
          {currentSlide}
        </div>
      )}

      <div className="slide-navigation">
        <div className="slide-nav-left">
          {slideIndex > 0 ? (
            <button className={slideButtonsVisible ? 'game-button' : 'hidden-button'} onClick={onPrevious}>⬅</button>
          ) : (
            <button className={settingsButtonVisible ? 'game-button' : 'hidden-button'} onClick={onOpenSettings}>⚙️</button>
          )}
        </div>
        <div className="slide-nav-right">
          {slideIndex < maxSlide && (
            <button className={slideButtonsVisible ? 'game-button' : 'hidden-button'} onClick={onNext}>➡</button>
          )}
        </div>
      </div>
    </main>
  )
}
