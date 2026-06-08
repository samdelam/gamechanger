import { useLayoutEffect } from 'react'

export function useVisualViewportHeight() {
  useLayoutEffect(() => {
    let frame = 0

    const updateViewportHeight = () => {
      cancelAnimationFrame(frame)
      frame = requestAnimationFrame(() => {
        const height = window.visualViewport?.height ?? window.innerHeight
        document.documentElement.style.setProperty('--app-height', `${height}px`)
      })
    }

    updateViewportHeight()

    window.visualViewport?.addEventListener('resize', updateViewportHeight)
    window.visualViewport?.addEventListener('scroll', updateViewportHeight)
    window.addEventListener('resize', updateViewportHeight)
    window.addEventListener('orientationchange', updateViewportHeight)

    return () => {
      cancelAnimationFrame(frame)
      window.visualViewport?.removeEventListener('resize', updateViewportHeight)
      window.visualViewport?.removeEventListener('scroll', updateViewportHeight)
      window.removeEventListener('resize', updateViewportHeight)
      window.removeEventListener('orientationchange', updateViewportHeight)
    }
  }, [])
}
