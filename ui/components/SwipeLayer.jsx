"use client"
import { useEffect } from "react"

export default function SwipeLayer() {
  useEffect(() => {
    let startX = 0
    const start = e => startX = e.touches[0].clientX
    const end = e => {
      if (startX < 40 && e.changedTouches[0].clientX > 120) {
        document.querySelector("button[aria-label='open-menu']")?.click()
      }
    }

    window.addEventListener("touchstart", start)
    window.addEventListener("touchend", end)
    return () => {
      window.removeEventListener("touchstart", start)
      window.removeEventListener("touchend", end)
    }
  }, [])

  return null
}