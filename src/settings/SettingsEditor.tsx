import { useMemo, useState } from 'react'
import { defaultConfig } from '../config/defaultConfig'
import type { GameConfig, PlayerConfig } from '../config/types'
import { downloadConfig, readImportedConfig } from '../config/configStorage'

const tabs = ['Players', 'Slides', 'Scoreboard', 'Assets', 'Winner'] as const
type Tab = typeof tabs[number]
const modifierKeys = ['Alt', 'Ctrl', 'Cmd', 'Meta', 'Mod', 'Option', 'Shift'] as const
type SoundAssetKey = keyof GameConfig['assets']['sounds']

type Props = {
  config: GameConfig
  onApply: (config: GameConfig) => void
  onCancel: () => void
  onPreviewSlideSound: (src?: string) => void
  onPreviewGainPointsSound: (src?: string) => void
  onPreviewLosePointsSound: (src?: string) => void
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


function readFileAsDataUrl(file: File): Promise<string> {
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

function Field({ label, children, className = '' }: { label: string; children: React.ReactNode; className?: string }) {
  return (
    <label className={`settings-field ${className}`.trim()}>
      <span>{label}</span>
      {children}
    </label>
  )
}

function NumberStepper({
  value,
  onChange,
  step = 1,
}: {
  value: number
  onChange: (value: number) => void
  step?: number
}) {
  const adjustValue = (direction: -1 | 1) => {
    onChange(Number((value + (step * direction)).toFixed(10)))
  }

  return (
    <div className="number-stepper">
      <input
        type="number"
        step={step}
        value={value}
        onChange={(event) => onChange(Number(event.target.value))}
      />
      <span className="number-stepper-controls">
        <button
          type="button"
          className="number-stepper-button"
          aria-label="Increase value"
          onClick={() => adjustValue(1)}
        >
          ˄
        </button>
        <button
          type="button"
          className="number-stepper-button"
          aria-label="Decrease value"
          onClick={() => adjustValue(-1)}
        >
          ˅
        </button>
      </span>
    </div>
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

type Confirmation = {
  message: string
  confirmClassName: 'danger-button' | 'warning-button'
  onConfirm: () => void
}

export function SettingsEditor({
  config,
  onApply,
  onCancel,
  onPreviewSlideSound,
  onPreviewGainPointsSound,
  onPreviewLosePointsSound,
}: Props) {
  const [draft, setDraft] = useState<GameConfig>(() => structuredClone(config))
  const [activeTab, setActiveTab] = useState<Tab>('Players')
  const [importError, setImportError] = useState('')
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null)
  const firstPlayer = useMemo(() => draft.players[0], [draft.players])

  const updateDraft = (updater: (current: GameConfig) => GameConfig) => {
    setDraft((current) => updater(structuredClone(current)))
  }

  const requestConfirmation = (nextConfirmation: Confirmation) => {
    setConfirmation(nextConfirmation)
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
      const imageDataUrl = await readFileAsDataUrl(file)
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

  const importSoundAsset = async (file: File | null, key: SoundAssetKey) => {
    if (!file) return
    if (!file.type.startsWith('audio/')) {
      setImportError('Please choose an audio file')
      return
    }

    try {
      const soundDataUrl = await readFileAsDataUrl(file)
      updateDraft((current) => {
        current.assets.sounds[key] = soundDataUrl
        return current
      })
      setImportError('')
    } catch (error) {
      setImportError(error instanceof Error ? error.message : 'Could not import sound file')
    }
  }

  return (
    <div className="settings-page">
      <div className="settings-editor">
        <header className="settings-header">
          <div className="settings-title">
            <h1>⚙️ Game Settings</h1>
            <p>Change the game, then apply the settings to return to the presentation.</p>
          </div>
          <div className="settings-import">
            <label className="primary-button settings-upload-button">
              ⬆ Upload config.json
              <input
                className="settings-hidden-file-input"
                type="file"
                accept="application/json,.json"
                onChange={(event) => {
                  importConfig(event.currentTarget.files?.[0] ?? null)
                  event.currentTarget.value = ''
                }}
              />
            </label>
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
              <Group title="Players" description="Use ↑ and ↓ to reorder players.">
                {!draft.scoreboard.enabled && (
                  <p className="settings-warning">Players only appear during the game when the scoreboard is enabled.</p>
                )}
                {draft.players.length === 0 && <p className="settings-empty">No players yet. Add one to get started.</p>}

                {draft.players.map((player, index) => (
                  <details className="settings-expander" key={index}>
                  <summary className="settings-expander-summary">
                    <span>Player {index + 1}: {player.name || `Player ${index + 1}`}</span>
                    <span className="summary-actions">
                      <button
                        type="button"
                        className="secondary-button icon-action-button"
                        disabled={index === 0}
                        title="Move player up"
                        onClick={(event) => {
                          event.preventDefault()
                          event.stopPropagation()
                          updateDraft((current) => {
                            current.players = moveItem(current.players, index, -1)
                            return current
                          })
                        }}
                      >
                        ↑
                      </button>
                      <button
                        type="button"
                        className="secondary-button icon-action-button"
                        disabled={index === draft.players.length - 1}
                        title="Move player down"
                        onClick={(event) => {
                          event.preventDefault()
                          event.stopPropagation()
                          updateDraft((current) => {
                            current.players = moveItem(current.players, index, 1)
                            return current
                          })
                        }}
                      >
                        ↓
                      </button>
                      <button
                        type="button"
                        className="danger-button icon-action-button"
                        title="Remove player"
                        aria-label="Remove player"
                        onClick={(event) => {
                          event.preventDefault()
                          event.stopPropagation()
                          updateDraft((current) => {
                            current.players.splice(index, 1)
                            return current
                          })
                        }}
                      >
                        🗑️
                      </button>
                    </span>
                  </summary>
                  <div className="player-grid">
                    <Field label="Name" className="player-name-field">
                      <input
                        value={player.name}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].name = event.target.value
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Starting score" className="player-compact-field player-number-field player-score-field">
                      <NumberStepper
                        value={player.startingScore}
                        onChange={(value) => updateDraft((current) => {
                          current.players[index].startingScore = value
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Starting slide" className="player-compact-field player-number-field player-slide-field">
                      <NumberStepper
                        value={player.startingSlide}
                        onChange={(value) => updateDraft((current) => {
                          current.players[index].startingSlide = value
                          return current
                        })}
                      />
                    </Field>
                    <Field label="Can win" className="player-compact-field player-checkbox-field">
                      <input
                        type="checkbox"
                        checked={player.canWin}
                        onChange={(event) => updateDraft((current) => {
                          current.players[index].canWin = event.target.checked
                          return current
                        })}
                      />
                    </Field>
                  </div>
                  </details>
                ))}

                <div className="settings-list-footer">
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
                  <button
                    type="button"
                    className="warning-button"
                    onClick={() => {
                      requestConfirmation({
                        message: 'Are you sure you want to reset players?',
                        confirmClassName: 'warning-button',
                        onConfirm: () => updateDraft((current) => {
                          current.players = structuredClone(defaultConfig.players)
                          return current
                        }),
                      })
                    }}
                  >
                    Reset Players
                  </button>
                </div>
              </Group>
            </div>
          )}

          {activeTab === 'Slides' && (
            <div>
              <Group title="Slide controls">
                <div className="settings-grid">
                  <Field label="Show navigation buttons">
                    <input type="checkbox" checked={draft.slides.buttons.slide} onChange={(event) => updateDraft((current) => {
                      current.slides.buttons.slide = event.target.checked
                      return current
                    })} />
                  </Field>
                  <Field label="Show open settings button">
                    <input type="checkbox" checked={draft.slides.buttons.settings} onChange={(event) => updateDraft((current) => {
                      current.slides.buttons.settings = event.target.checked
                      return current
                    })} />
                  </Field>
                  <Field label="Play slide sound">
                    <span className="settings-inline-controls">
                      <input type="checkbox" checked={draft.slides.sounds.slide} onChange={(event) => updateDraft((current) => {
                        current.slides.sounds.slide = event.target.checked
                        return current
                      })} />
                      <button
                        type="button"
                        className="settings-icon-button"
                        title="Preview slide sound"
                        aria-label="Preview slide sound"
                        onClick={() => onPreviewSlideSound(draft.assets.sounds.slideDataUrl)}
                      >
                        🔊
                      </button>
                    </span>
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

              <Group title="Slide content">
                <div className="settings-top-row">
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
                    <button type="button" className="secondary-button icon-action-button" disabled={index === 0} onClick={() => updateDraft((current) => {
                      current.slides.content = moveItem(current.slides.content, index, -1)
                      return current
                    })}>↑</button>
                    <button type="button" className="secondary-button icon-action-button" disabled={index === draft.slides.content.length - 1} onClick={() => updateDraft((current) => {
                      current.slides.content = moveItem(current.slides.content, index, 1)
                      return current
                    })}>↓</button>
                    <button type="button" className="danger-button icon-action-button" title="Remove slide" aria-label={`Remove slide ${index + 1}`} onClick={() => updateDraft((current) => {
                      current.slides.content.splice(index, 1)
                      return current
                    })}>🗑️</button>
                  </div>
                ))}

                <div className="settings-list-footer">
                  <button type="button" className="secondary-button" onClick={() => updateDraft((current) => {
                    current.slides.content.push('')
                    return current
                  })}>➕ Add slide</button>
                  <button
                    type="button"
                    className="warning-button"
                    onClick={() => {
                      requestConfirmation({
                        message: 'Are you sure you want to reset slides?',
                        confirmClassName: 'warning-button',
                        onConfirm: () => updateDraft((current) => {
                          current.slides.content = structuredClone(defaultConfig.slides.content)
                          return current
                        }),
                      })
                    }}
                  >
                    Reset Slides
                  </button>
                </div>
              </Group>
            </div>
          )}

          {activeTab === 'Scoreboard' && (
            <div>
              <Group title="Scoreboard">
                <div className="settings-grid">
                  <Field label="Show scoreboard">
                    <input type="checkbox" checked={draft.scoreboard.enabled} onChange={(event) => updateDraft((current) => {
                      current.scoreboard.enabled = event.target.checked
                      return current
                    })} />
                  </Field>
                  {draft.scoreboard.enabled && (
                    <Field label="Points buttons">
                      <input type="checkbox" checked={draft.scoreboard.buttons.points} onChange={(event) => updateDraft((current) => {
                        current.scoreboard.buttons.points = event.target.checked
                        return current
                      })} />
                    </Field>
                  )}
                </div>
              </Group>

              {draft.scoreboard.enabled && (
                <>
                  <Group
                    title="Scoreboard shortcuts"
                    description={
                      'Point shortcuts are assigned by player order. Press a number key such as 1, 2, 3, and so on to add one point to that player. Press Shift+number, such as Shift+1 or Shift+2, to remove one point.\n' +
                      'Change the Points Modifier key to use a modifier other than Shift.\n' +
                      'Enable Invert point shortcuts to reverse that behavior, making the number key remove points and modifier+number add points instead.'
                    }
                  >
                    <div className="settings-grid">
                      <Field label="Points Modifier key">
                        <select value={draft.scoreboard.shortcuts.pointsModifier} onChange={(event) => updateDraft((current) => {
                          current.scoreboard.shortcuts.pointsModifier = event.target.value
                          return current
                        })}>
                          {modifierKeys.map((key) => (
                            <option key={key} value={key}>{key}</option>
                          ))}
                        </select>
                      </Field>
                      <Field label="Invert point shortcuts">
                        <input type="checkbox" checked={draft.scoreboard.shortcuts.pointsInverted} onChange={(event) => updateDraft((current) => {
                          current.scoreboard.shortcuts.pointsInverted = event.target.checked
                          return current
                        })} />
                      </Field>
                    </div>
                  </Group>

                  <Group
                    title="Scoreboard sounds"
                    description={
                      "The delay is used so multiple addition/removal of points don't play the sound multiple times.\n"+
                      "If the delay is 0.5s, the sound will only play after 0.5s has passed without any new addition/removal of points."
                    }
                  >
                    <div className="sound-columns">
                      <div>
                        <Field label="Gain points sound">
                          <span className="settings-inline-controls">
                            <input type="checkbox" checked={draft.scoreboard.sounds.gainPoints} onChange={(event) => updateDraft((current) => {
                              current.scoreboard.sounds.gainPoints = event.target.checked
                              return current
                            })} />
                            <button
                              type="button"
                              className="settings-icon-button"
                              title="Preview gain points sound"
                              aria-label="Preview gain points sound"
                              onClick={() => onPreviewGainPointsSound(draft.assets.sounds.gainPointsDataUrl)}
                            >
                              🔊
                            </button>
                          </span>
                        </Field>
                        {draft.scoreboard.sounds.gainPoints && (
                          <Field label="Gain sound delay (seconds)">
                            <NumberStepper step={0.1} value={draft.scoreboard.sounds.gainPointsDelaySeconds} onChange={(value) => updateDraft((current) => {
                              current.scoreboard.sounds.gainPointsDelaySeconds = value
                              return current
                            })} />
                          </Field>
                        )}
                      </div>
                      <div>
                        <Field label="Lose points sound">
                          <span className="settings-inline-controls">
                            <input type="checkbox" checked={draft.scoreboard.sounds.losePoints} onChange={(event) => updateDraft((current) => {
                              current.scoreboard.sounds.losePoints = event.target.checked
                              return current
                            })} />
                            <button
                              type="button"
                              className="settings-icon-button"
                              title="Preview lose points sound"
                              aria-label="Preview lose points sound"
                              onClick={() => onPreviewLosePointsSound(draft.assets.sounds.losePointsDataUrl)}
                            >
                              🔊
                            </button>
                          </span>
                        </Field>
                        {draft.scoreboard.sounds.losePoints && (
                          <Field label="Lose sound delay (seconds)">
                            <NumberStepper step={0.1} value={draft.scoreboard.sounds.losePointsDelaySeconds} onChange={(value) => updateDraft((current) => {
                              current.scoreboard.sounds.losePointsDelaySeconds = value
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


          {activeTab === 'Assets' && (
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
                  <div className="settings-field asset-file-field">
                    <span>Import cover image</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(event) => importCoverImage(event.currentTarget.files?.[0] ?? null)}
                    />
                    {draft.cover.imageDataUrl && (
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
                    )}
                  </div>
                </div>

                {draft.cover.imageDataUrl && (
                  <div className="cover-settings-preview-wrap">
                    <img className="cover-settings-preview" src={draft.cover.imageDataUrl} alt="Custom cover preview" />
                  </div>
                )}
              </Group>

              <Group
                title="Sounds"
                description="Import custom sounds to replace the default audio used during the game. Custom sounds are saved inside the exported config.json."
              >
                <div className="asset-sound-grid">
                  <div className="settings-field asset-sound-field">
                    <span className="settings-label-row">
                      Slide change sound
                      <button
                        type="button"
                        className="settings-icon-button"
                        title="Preview slide sound"
                        aria-label="Preview slide sound"
                        onClick={() => onPreviewSlideSound(draft.assets.sounds.slideDataUrl)}
                      >
                        🔊
                      </button>
                    </span>
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={(event) => {
                        importSoundAsset(event.currentTarget.files?.[0] ?? null, 'slideDataUrl')
                      }}
                    />
                    {draft.assets.sounds.slideDataUrl && (
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={() => updateDraft((current) => {
                          current.assets.sounds.slideDataUrl = ''
                          return current
                        })}
                      >
                        Use default slide sound
                      </button>
                    )}
                  </div>
                  <div className="settings-field asset-sound-field">
                    <span className="settings-label-row">
                      Gain points sound
                      <button
                        type="button"
                        className="settings-icon-button"
                        title="Preview gain points sound"
                        aria-label="Preview gain points sound"
                        onClick={() => onPreviewGainPointsSound(draft.assets.sounds.gainPointsDataUrl)}
                      >
                        🔊
                      </button>
                    </span>
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={(event) => {
                        importSoundAsset(event.currentTarget.files?.[0] ?? null, 'gainPointsDataUrl')
                      }}
                    />
                    {draft.assets.sounds.gainPointsDataUrl && (
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={() => updateDraft((current) => {
                          current.assets.sounds.gainPointsDataUrl = ''
                          return current
                        })}
                      >
                        Use default gain sound
                      </button>
                    )}
                  </div>
                  <div className="settings-field asset-sound-field">
                    <span className="settings-label-row">
                      Lose points sound
                      <button
                        type="button"
                        className="settings-icon-button"
                        title="Preview lose points sound"
                        aria-label="Preview lose points sound"
                        onClick={() => onPreviewLosePointsSound(draft.assets.sounds.losePointsDataUrl)}
                      >
                        🔊
                      </button>
                    </span>
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={(event) => {
                        importSoundAsset(event.currentTarget.files?.[0] ?? null, 'losePointsDataUrl')
                      }}
                    />
                    {draft.assets.sounds.losePointsDataUrl && (
                      <button
                        type="button"
                        className="secondary-button"
                        onClick={() => updateDraft((current) => {
                          current.assets.sounds.losePointsDataUrl = ''
                          return current
                        })}
                      >
                        Use default lose sound
                      </button>
                    )}
                  </div>
                </div>
              </Group>
            </div>
          )}

          {activeTab === 'Winner' && (
            <div>
              <Group title="Winner screen">
                {!draft.scoreboard.enabled && (
                  <p className="settings-warning">The winner slide does not work when the scoreboard is disabled.</p>
                )}
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
          <button
            type="button"
            className="danger-button"
            onClick={() => {
              requestConfirmation({
                message: 'Are you sure you want to discard changes?',
                confirmClassName: 'danger-button',
                onConfirm: onCancel,
              })
            }}
          >
            ✕ Cancel
          </button>
          <button
            type="button"
            className="warning-button"
            onClick={() => {
              requestConfirmation({
                message: 'Are you sure you want to reset all settings?',
                confirmClassName: 'warning-button',
                onConfirm: () => setDraft((current) => {
                  const next = structuredClone(defaultConfig)
                  next.players = structuredClone(current.players)
                  next.slides.content = structuredClone(current.slides.content)
                  return next
                }),
              })
            }}
          >
            Reset local settings
          </button>
        </footer>

        {confirmation && (
          <div className="settings-confirm-backdrop" role="presentation">
            <div className="settings-confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="settings-confirm-title">
              <h3 id="settings-confirm-title">Confirm action</h3>
              <p>{confirmation.message}</p>
              <div className="settings-confirm-actions">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setConfirmation(null)}
                >
                  No
                </button>
                <button
                  type="button"
                  className={confirmation.confirmClassName}
                  onClick={() => {
                    const action = confirmation.onConfirm
                    setConfirmation(null)
                    action()
                  }}
                >
                  Yes
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
