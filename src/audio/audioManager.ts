export class AudioManager {
  private defaultSlideSrc: string
  private defaultGainSrc: string
  private defaultLoseSrc: string
  private slideAudio: HTMLAudioElement
  private gainAudio: HTMLAudioElement
  private loseAudio: HTMLAudioElement
  private unlocked = false
  private gainTimer: number | null = null
  private loseTimer: number | null = null

  constructor(baseUrl: string) {
    this.defaultSlideSrc = `${baseUrl}assets/sounds/slide.wav`
    this.defaultGainSrc = `${baseUrl}assets/sounds/gain_point.wav`
    this.defaultLoseSrc = `${baseUrl}assets/sounds/lose_point.wav`
    this.slideAudio = this.createAudio(this.defaultSlideSrc)
    this.gainAudio = this.createAudio(this.defaultGainSrc)
    this.loseAudio = this.createAudio(this.defaultLoseSrc)
  }

  private createAudio(src: string): HTMLAudioElement {
    const audio = new Audio(src)
    audio.preload = 'auto'
    return audio
  }

  private setAudioSource(audio: HTMLAudioElement, src: string): void {
    if (audio.src === src) return
    audio.pause()
    audio.src = src
    if (this.unlocked) audio.load()
  }

  setSoundSources(sounds: {
    slideDataUrl?: string
    gainPointsDataUrl?: string
    losePointsDataUrl?: string
  }): void {
    this.setAudioSource(this.slideAudio, sounds.slideDataUrl || this.defaultSlideSrc)
    this.setAudioSource(this.gainAudio, sounds.gainPointsDataUrl || this.defaultGainSrc)
    this.setAudioSource(this.loseAudio, sounds.losePointsDataUrl || this.defaultLoseSrc)
  }

  unlock(): void {
    if (this.unlocked) return
    this.unlocked = true

    // Some browsers only allow audio after a user gesture. Calling load during
    // the first click/key press makes later playback much more reliable.
    this.slideAudio.load()
    this.gainAudio.load()
    this.loseAudio.load()
  }

  private play(audio: HTMLAudioElement): void {
    this.unlock()
    audio.pause()
    audio.currentTime = 0
    audio.play().catch(() => {
      // Autoplay policies can still block sound until the user interacts with
      // the page. Ignore the error; the next user gesture should unlock it.
    })
  }

  private debouncePlay(
    audio: HTMLAudioElement,
    delaySeconds: number,
    timer: number | null,
    setTimer: (timer: number | null) => void,
  ): void {
    if (timer !== null) {
      window.clearTimeout(timer)
      setTimer(null)
    }

    const delayMs = Math.max(0, delaySeconds) * 1000

    if (delayMs === 0) {
      this.play(audio)
      return
    }

    const nextTimer = window.setTimeout(() => {
      setTimer(null)
      this.play(audio)
    }, delayMs)

    setTimer(nextTimer)
  }

  playSlide(srcOverride?: string): void {
    if (srcOverride !== undefined) {
      this.play(this.createAudio(srcOverride || this.defaultSlideSrc))
      return
    }

    this.play(this.slideAudio)
  }

  playGain(delaySeconds = 0, srcOverride?: string): void {
    if (srcOverride !== undefined) {
      this.play(this.createAudio(srcOverride || this.defaultGainSrc))
      return
    }

    this.debouncePlay(
      this.gainAudio,
      delaySeconds,
      this.gainTimer,
      (timer) => {
        this.gainTimer = timer
      },
    )
  }

  playLose(delaySeconds = 0, srcOverride?: string): void {
    if (srcOverride !== undefined) {
      this.play(this.createAudio(srcOverride || this.defaultLoseSrc))
      return
    }

    this.debouncePlay(
      this.loseAudio,
      delaySeconds,
      this.loseTimer,
      (timer) => {
        this.loseTimer = timer
      },
    )
  }
}
