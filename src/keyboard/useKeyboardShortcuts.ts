import { useEffect } from 'react'
import type { GameConfig } from '../config/types'

type Args = {
  enabled: boolean
  config: GameConfig
  visiblePlayerCount: number
  onNextSlide: () => void
  onPreviousSlide: () => void
  onOpenSettings: () => void
  onAddPoint: (playerIndex: number) => void
  onRemovePoint: (playerIndex: number) => void
  unlockAudio: () => void
}

function normalizeKey(key: string): string {
  return key.trim().toLowerCase()
}

function isEditingTarget(target: EventTarget | null): boolean {
  const element = target as HTMLElement | null
  if (!element) return false
  const tagName = element.tagName.toLowerCase()
  return tagName === 'input' || tagName === 'textarea' || tagName === 'select' || element.isContentEditable
}

function modifierPressed(event: KeyboardEvent, modifier: string): boolean {
  const key = normalizeKey(modifier)
  if (key === 'shift') return event.shiftKey
  if (key === 'ctrl' || key === 'control') return event.ctrlKey
  if (key === 'alt' || key === 'option') return event.altKey
  if (key === 'cmd' || key === 'meta') return event.metaKey
  if (key === 'mod') return event.ctrlKey || event.metaKey
  return false
}

function playerNumberFromEvent(event: KeyboardEvent): number | null {
  // When Shift is pressed, event.key changes from "1" to symbols like "!" on
  // many keyboard layouts. event.code keeps the physical key as "Digit1", so
  // Shift+number can still be detected reliably.
  const digitMatch = event.code.match(/^Digit([1-9])$/)
  if (digitMatch) return Number(digitMatch[1])

  const numpadMatch = event.code.match(/^Numpad([1-9])$/)
  if (numpadMatch) return Number(numpadMatch[1])

  const fallback = Number(event.key)
  return Number.isInteger(fallback) && fallback >= 1 && fallback <= 9 ? fallback : null
}

export function useKeyboardShortcuts({
  enabled,
  config,
  visiblePlayerCount,
  onNextSlide,
  onPreviousSlide,
  onOpenSettings,
  onAddPoint,
  onRemovePoint,
  unlockAudio,
}: Args) {
  useEffect(() => {
    if (!enabled) return

    const handleKeyDown = (event: KeyboardEvent) => {
      if (isEditingTarget(event.target)) return
      unlockAudio()

      const key = normalizeKey(event.key)
      const slideShortcuts = config.slides.shortcuts
      const scoreboardShortcuts = config.scoreboard.shortcuts

      if (key === normalizeKey(slideShortcuts.next)) {
        event.preventDefault()
        onNextSlide()
        return
      }

      if (key === normalizeKey(slideShortcuts.previous)) {
        event.preventDefault()
        onPreviousSlide()
        return
      }

      if (key === normalizeKey(slideShortcuts.settings)) {
        event.preventDefault()
        onOpenSettings()
        return
      }

      const playerNumber = playerNumberFromEvent(event)
      if (playerNumber === null || playerNumber > visiblePlayerCount) {
        return
      }

      const hasModifier = modifierPressed(event, scoreboardShortcuts.pointsModifier)
      const inverted = scoreboardShortcuts.pointsInverted
      const playerIndex = playerNumber - 1

      event.preventDefault()

      if (inverted) {
        if (hasModifier) onAddPoint(playerIndex)
        else onRemovePoint(playerIndex)
      } else {
        if (hasModifier) onRemovePoint(playerIndex)
        else onAddPoint(playerIndex)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [
    enabled,
    config,
    visiblePlayerCount,
    onNextSlide,
    onPreviousSlide,
    onOpenSettings,
    onAddPoint,
    onRemovePoint,
    unlockAudio,
  ])
}
