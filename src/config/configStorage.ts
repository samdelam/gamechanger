import { defaultConfig } from './defaultConfig'
import type { GameConfig } from './types'

const STORAGE_KEY = 'gamechanger.config.v1'

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

export function deepMerge<T>(base: T, override: unknown): T {
  if (!isObject(base) || !isObject(override)) {
    return (override === undefined ? base : override) as T
  }

  const result: Record<string, unknown> = { ...base }
  for (const [key, value] of Object.entries(override)) {
    const current = result[key]
    if (isObject(current) && isObject(value)) {
      result[key] = deepMerge(current, value)
    } else {
      result[key] = value
    }
  }
  return result as T
}

export function normalizeConfig(raw: unknown): GameConfig {
  return deepMerge(defaultConfig, raw ?? {})
}

export function loadStoredConfig(): GameConfig | null {
  const raw = window.localStorage.getItem(STORAGE_KEY)
  if (!raw) return null

  try {
    return normalizeConfig(JSON.parse(raw))
  } catch {
    return null
  }
}

export function saveStoredConfig(config: GameConfig): void {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(config))
}

export function clearStoredConfig(): void {
  window.localStorage.removeItem(STORAGE_KEY)
}

export async function loadRootConfig(): Promise<GameConfig | null> {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}config.json`, { cache: 'no-store' })
    if (!response.ok) return null

    const text = await response.text()
    const trimmed = text.trim()
    if (!trimmed.startsWith('{')) return null

    return normalizeConfig(JSON.parse(trimmed))
  } catch {
    return null
  }
}

export function downloadConfig(config: GameConfig): void {
  const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'config.json'
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}

export async function readImportedConfig(file: File): Promise<GameConfig> {
  const text = await file.text()
  return normalizeConfig(JSON.parse(text))
}
