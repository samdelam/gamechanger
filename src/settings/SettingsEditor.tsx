import { useMemo, useState } from 'react'
import type { GameConfig, PlayerConfig } from '../config/types'
import { downloadConfig, readImportedConfig } from '../config/configStorage'

const tabs = ['Players', 'Slides', 'Scoreboard', 'Cover', 'Winner'] as const
type Tab = typeof tabs[number]

type Props = {
  config: GameConfig
  onApply: (config: GameConfig) => void
  onCancel: () => void
  onResetDefaults: () => void
}

function moveItem<T>(items: T[], index: number, direction: -1 | 1): T[] {
  const next = [...items]
  const target = index + direction
  if (target < 0 || target >= next.length) return next
  const current = next[index]
  next[index] = next[target]
  next[target] = current
  return next
}

function newPlayer(number: number, template?: PlayerConfig): PlayerConfig {
  return {
    name: `PLAYER ${number}`,
    startingScore: template?.startingScore ?? 0,
    startingSlide: template?.startingSlide ?? 1,
    canWin: template?.canWin ?? true,
  }
}


function readImageAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        resolve(reader.result)
      } else {
        reject(new Error('Could not read image file'))
      }
    }
    reader.onerror = () => reject(new Error('Could not read image file'))
    reader.readAsDataURL(file)
  })
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="settings-field">
      <span>{label}</span>
      {children}
    </label>
  )
}

function Group({ title, description, children }: { title: string; description?: string; children: React.ReactNode }) {
  return (
    <section className="settings-group">
      <h3>{title}</h3>
      {description && (
        <p className="settings-description">
          {description.split('\n').map((line, index) => (
            <span key={index}>
              {line}
              {index < description.split('\n').length - 1 && <br />}
            </span>
          ))}
        </p>
      )}
      {children}
    </section>
  )
}

export function SettingsEditor({ config, onApply, onCancel, onResetDefaults }: Props) {
  const [draft, setDraft] = useState<GameConfig>(() => structuredClone(config))
  const [activeTab, setActiveTab] = useState<Tab>('Players')
  const [importError, setImportError] = useState('')
  const firstPlayer = useMemo(() => draft.players[0], [draft.players])

  const updateDraft = (updater: (current: GameConfig) => GameConfig) => {
    setDraft((current) => updater(structuredClone(current)))
  }

  const importConfig = async (file: File | null) => {
    if (!file) return
    try {
      const imported = await readImportedConfig(file)
      setDraft(imported)
      setImportError('')
    } catch (error) {
      setImportError(error instanceof Error ? error.message : 'Could not import config')
    }
  }


  const importCoverImage = async (file: File | null) => {
    if (!file) return
    if (!file.type.startsWith('image/')) {
      setImportError('Please choose an image file')
      return
    }

    try {
      const imageDataUrl = await readImageAsDataUrl(file)
      updateDraft((current) => {
        current.cover.enabled = true
        current.cover.imageDataUrl = imageDataUrl
        return current
      })
      setImportError('')
    } catch (error) {
      setImportError(error instanceof Error ? error.message : 'Could not import cover image')
    }
  }

  return (
    <div className="settings-page">
      <div className="settings-editor">
        <header className="settings-header">
          <div>
            <h1>⚙️ Game Settings</h1>
            <p>Change the game, then apply the settings to return to the presentation.</p>
          </div>
          <div className="settings-import">
            <input
              type="file"
              accept="application/json,.json"
              onChange={(event) => importConfig(event.currentTarget.files?.[0] ?? null)}
            />
            {importError && <span className="settings-error">{importError}</span>}
          </div>
        </header>

        <nav className="settings-tabs" aria-label="Settings sections">
          {tabs.map((tab) => (
            <button
              key={tab}
              className={activeTab === tab ? 'active' : ''}
              onClick={() => setActiveTab(tab)}
              type="button"
            >
              {tab}
            </button>
          ))}
        </nav>

        <div className="settings-tab-panel">
          {activeTab === 'Players' && (
            <div>
              <div className="settings-top-row">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => updateDraft((current) => {
                    current.players.push(newPlayer(current.players.length + 1, firstPlayer))
                    return current
                  })}
                >
                  ➕ Add player
                </button>
                <span className="settings-hint">Use ↑ and ↓ to reorder players.</span>
              </div>

              {draft.players.length === 0 && <p className="settings-empty">No players yet. Add one to get started.</p>}

              {draft.players.map((player, index) => (
                <details className="settings-expander" key={index}>
                  <summary>Player {index + 1}: {player.name || `Player ${index + 1}`}</summary>
                  <div className="player-grid">
                    <Field label="Name">
                      <input
                        value={player.name}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].name = event.target.value
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Starting score">
                      <input
                        type="number"
                        value={player.startingScore}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].startingScore = Number(event.target.value)
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Starting slide">
                      <input
                        type="number"
                        value={player.startingSlide}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].startingSlide = Number(event.target.value)
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Can win">
                      <input
                        type="checkbox"
                        checked={player.canWin}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].canWin = event.target.checked
                          return current
                        })}
                      />
                    </Field>
                    <div className="row-actions">
                      <button type="button" className="secondary-button" disabled={index === 0} onClick={() => updateDraft((current) => {
                        current.players = moveItem(current.players, index, -1)
                        return current
                      })}>↑</button>
                      <button type="button" className="secondary-button" disabled={index === draft.players.length - 1} onClick={() => updateDraft((current) => {
                        current.players = moveItem(current.players, index, 1)
                        return current
                      })}>↓</button>
                      <button type="button" className="danger-button" onClick={() => updateDraft((current) => {
                        current.players.splice(index, 1)
                        return current
                      })}>🗑️ Remove</button>
                    </div>
                  </div>
                </details>
              ))}
            </div>
          )}

          {activeTab === 'Slides' && (
            <div>
              <Group title="Slide buttons">
                <div className="settings-grid">
                  <Field label="Slide buttons">
                    <input type="checkbox" checked={draft.slides.buttons.slide} onChange={(event) => updateDraft((current) => {
                      current.slides.buttons.slide = event.target.checked
                      return current
                    })} />
                  </Field>
                  <Field label="Settings button">
                    <input type="checkbox" checked={draft.slides.buttons.settings} onChange={(event) => updateDraft((current) => {
                      current.slides.buttons.settings = event.target.checked
                      return current
                    })} />
                  </Field>
                </div>
              </Group>

              <Group title="Slide shortcuts">
                <div className="settings-grid">
                  <Field label="Next slide key">
                    <input value={draft.slides.shortcuts.next} onChange={(event) => updateDraft((current) => {
                      current.slides.shortcuts.next = event.target.value
                      return current
                    })} />
                  </Field>
                  <Field label="Previous slide key">
                    <input value={draft.slides.shortcuts.previous} onChange={(event) => updateDraft((current) => {
                      current.slides.shortcuts.previous = event.target.value
                      return current
                    })} />
                  </Field>
                  <Field label="Open settings key">
                    <input value={draft.slides.shortcuts.settings} onChange={(event) => updateDraft((current) => {
                      current.slides.shortcuts.settings = event.target.value
                      return current
                    })} />
                  </Field>
                </div>
              </Group>

              <Group title="Slide sound">
                <Field label="Slide sound">
                  <input type="checkbox" checked={draft.slides.sounds.slide} onChange={(event) => updateDraft((current) => {
                    current.slides.sounds.slide = event.target.checked
                    return current
                  })} />
                </Field>
              </Group>

              <Group title="Slide content">
                <div className="settings-top-row">
                  <button type="button" className="secondary-button" onClick={() => updateDraft((current) => {
                    current.slides.content.push('')
                    return current
                  })}>➕ Add slide</button>
                  <span className="settings-hint">Empty slides are allowed. Use ↑ and ↓ to reorder slides.</span>
                </div>

                {draft.slides.content.map((slide, index) => (
                  <div className="slide-edit-row" key={index}>
                    <strong>Slide {index + 1}</strong>
                    <input
                      aria-label={`Slide ${index + 1} text`}
                      value={slide}
                      onChange={(event) => updateDraft((current) => {
                        current.slides.content[index] = event.target.value
                        return current
                      })}
                    />
                    <button type="button" className="secondary-button" disabled={index === 0} onClick={() => updateDraft((current) => {
                      current.slides.content = moveItem(current.slides.content, index, -1)
                      return current
                    })}>↑</button>
                    <button type="button" className="secondary-button" disabled={index === draft.slides.content.length - 1} onClick={() => updateDraft((current) => {
                      current.slides.content = moveItem(current.slides.content, index, 1)
                      return current
                    })}>↓</button>
                    <button type="button" className="danger-button" onClick={() => updateDraft((current) => {
                      current.slides.content.splice(index, 1)
                      return current
                    })}>🗑️ Remove</button>
                  </div>
                ))}
              </Group>
            </div>
          )}

          {activeTab === 'Scoreboard' && (
            <div>
              <Group title="Scoreboard">
                <Field label="Show scoreboard">
                  <input type="checkbox" checked={draft.scoreboard.enabled} onChange={(event) => updateDraft((current) => {
                    current.scoreboard.enabled = event.target.checked
                    return current
                  })} />
                </Field>
              </Group>

              {draft.scoreboard.enabled && (
                <>
                  <Group title="Scoreboard buttons">
                    <Field label="Points buttons">
                      <input type="checkbox" checked={draft.scoreboard.buttons.points} onChange={(event) => updateDraft((current) => {
                        current.scoreboard.buttons.points = event.target.checked
                        return current
                      })} />
                    </Field>
                  </Group>

                  <Group
                    title="Scoreboard shortcuts"
                    description={
                      'Point shortcuts are assigned by player order. Press a number key such as 1, 2, 3, and so on to add one point to that player. Press Shift+number, such as Shift+1 or Shift+2, to remove one point.\n' +
                      'Change the Points Modifier key to use a modifier other than Shift. Allowed modifiers: Alt, Ctrl, Cmd, Meta, Mod, Option, Shift.\n' +
                      'Enable Invert point shortcuts to reverse that behavior, making the number key remove points and modifier+number add points instead.'
                    }
                  >
                    <div className="settings-grid">
                      <Field label="Points Modifier key">
                        <input value={draft.scoreboard.shortcuts.pointsModifier} onChange={(event) => updateDraft((current) => {
                          current.scoreboard.shortcuts.pointsModifier = event.target.value
                          return current
                        })} />
                      </Field>
                      <Field label="Invert point shortcuts">
                        <input type="checkbox" checked={draft.scoreboard.shortcuts.pointsInverted} onChange={(event) => updateDraft((current) => {
                          current.scoreboard.shortcuts.pointsInverted = event.target.checked
                          return current
                        })} />
                      </Field>
                    </div>
                  </Group>

                  <Group title="Scoreboard sounds">
                    <div className="sound-columns">
                      <div>
                        <Field label="Gain points sound">
                          <input type="checkbox" checked={draft.scoreboard.sounds.gainPoints} onChange={(event) => updateDraft((current) => {
                            current.scoreboard.sounds.gainPoints = event.target.checked
                            return current
                          })} />
                        </Field>
                        {draft.scoreboard.sounds.gainPoints && (
                          <Field label="Gain sound delay (seconds)">
                            <input type="number" step="0.1" value={draft.scoreboard.sounds.gainPointsDelaySeconds} onChange={(event) => updateDraft((current) => {
                              current.scoreboard.sounds.gainPointsDelaySeconds = Number(event.target.value)
                              return current
                            })} />
                          </Field>
                        )}
                      </div>
                      <div>
                        <Field label="Lose points sound">
                          <input type="checkbox" checked={draft.scoreboard.sounds.losePoints} onChange={(event) => updateDraft((current) => {
                            current.scoreboard.sounds.losePoints = event.target.checked
                            return current
                          })} />
                        </Field>
                        {draft.scoreboard.sounds.losePoints && (
                          <Field label="Lose sound delay (seconds)">
                            <input type="number" step="0.1" value={draft.scoreboard.sounds.losePointsDelaySeconds} onChange={(event) => updateDraft((current) => {
                              current.scoreboard.sounds.losePointsDelaySeconds = Number(event.target.value)
                              return current
                            })} />
                          </Field>
                        )}
                      </div>
                    </div>
                  </Group>
                </>
              )}
            </div>
          )}


          {activeTab === 'Cover' && (
            <div>
              <Group
                title="Cover image"
                description="Import a custom cover image or hide the cover to start directly on the first slide. Custom cover images are saved inside the exported config.json."
              >
                <div className="settings-grid">
                  <Field label="Show cover">
                    <input
                      type="checkbox"
                      checked={draft.cover.enabled}
                      onChange={(event) => updateDraft((current) => {
                        current.cover.enabled = event.target.checked
                        return current
                      })}
                    />
                  </Field>
                  <Field label="Import cover image">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(event) => importCoverImage(event.currentTarget.files?.[0] ?? null)}
                    />
                  </Field>
                </div>

                {draft.cover.imageDataUrl && (
                  <div className="cover-settings-preview-wrap">
                    <img className="cover-settings-preview" src={draft.cover.imageDataUrl} alt="Custom cover preview" />
                    <button
                      type="button"
                      className="secondary-button"
                      onClick={() => updateDraft((current) => {
                        current.cover.imageDataUrl = ''
                        return current
                      })}
                    >
                      Use default cover image
                    </button>
                  </div>
                )}
              </Group>
            </div>
          )}

          {activeTab === 'Winner' && (
            <div>
              <Group title="Winner screen">
                <Field label="Enable winner screen">
                  <input type="checkbox" checked={draft.winner.enabled} onChange={(event) => updateDraft((current) => {
                    current.winner.enabled = event.target.checked
                    return current
                  })} />
                </Field>
              </Group>

              {draft.winner.enabled && (
                <>
                  <Group title="Single winner">
                    <div className="settings-grid">
                      <Field label="Title">
                        <input value={draft.winner.single.title} onChange={(event) => updateDraft((current) => {
                          current.winner.single.title = event.target.value
                          return current
                        })} />
                      </Field>
                      <Field label="Score text">
                        <input value={draft.winner.single.scoreText} onChange={(event) => updateDraft((current) => {
                          current.winner.single.scoreText = event.target.value
                          return current
                        })} />
                      </Field>
                    </div>
                  </Group>
                  <Group title="Multiple winners (Tie)">
                    <div className="settings-grid">
                      <Field label="Title">
                        <input value={draft.winner.multiple.title} onChange={(event) => updateDraft((current) => {
                          current.winner.multiple.title = event.target.value
                          return current
                        })} />
                      </Field>
                      <Field label="Separator">
                        <input value={draft.winner.multiple.separator} onChange={(event) => updateDraft((current) => {
                          current.winner.multiple.separator = event.target.value
                          return current
                        })} />
                      </Field>
                      <Field label="Score text">
                        <input value={draft.winner.multiple.scoreText} onChange={(event) => updateDraft((current) => {
                          current.winner.multiple.scoreText = event.target.value
                          return current
                        })} />
                      </Field>
                    </div>
                  </Group>
                </>
              )}
            </div>
          )}
        </div>

        <footer className="settings-actions">
          <button type="button" className="primary-button" onClick={() => onApply(draft)}>✅ Apply</button>
          <button type="button" className="secondary-button" onClick={() => downloadConfig(draft)}>⬇ Download config.json</button>
          <button type="button" className="secondary-button" onClick={onCancel}>✕ Cancel</button>
          <button type="button" className="secondary-button" onClick={onResetDefaults}>Reset local settings</button>
        </footer>
      </div>
    </div>
  )
}
