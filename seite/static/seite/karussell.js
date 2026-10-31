// Bilderkarussell der Startseite: wechselt ruhig von selbst (alle 7 Sekunden,
// danach wieder von vorn), hält beim Darüberfahren, beim Fokus und auf
// Knopfdruck an. Bei „Bewegung reduzieren“ startet es angehalten. Ohne Skript
// lässt sich das Band seitlich wischen bzw. scrollen.
const TAKT = 7000

document.querySelectorAll('[data-karussell]').forEach((box) => {
  const band = box.querySelector('.karussell-band')
  const bilder = Array.from(band.children)
  const zaehler = box.querySelector('.karussell-zaehler')
  const zurueck = box.querySelector('[data-zurueck]')
  const weiter = box.querySelector('[data-weiter]')
  const pause = box.querySelector('[data-pause]')
  const ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  box.querySelector('.karussell-steuerung').hidden = false

  let angehalten = ruhig // vom Besucher angehalten
  let verweilt = false // Maus oder Fokus im Karussell
  let uhr

  const aktuell = () => Math.round(band.scrollLeft / band.clientWidth)
  const zeige = (i) => {
    const ziel = (i + bilder.length) % bilder.length
    band.scrollTo({ left: ziel * band.clientWidth, behavior: ruhig ? 'auto' : 'smooth' })
  }
  const auffrischen = () => {
    zaehler.textContent = `${aktuell() + 1} / ${bilder.length}`
  }
  const planen = () => {
    clearTimeout(uhr)
    if (!angehalten && !verweilt && !document.hidden) {
      uhr = setTimeout(() => {
        zeige(aktuell() + 1)
        planen()
      }, TAKT)
    }
  }
  const setzePause = (an) => {
    angehalten = an
    pause.setAttribute('aria-pressed', String(an))
    pause.setAttribute('aria-label', an ? 'Weiter abspielen' : 'Anhalten')
    pause.textContent = an ? '▶' : '❚❚'
    // Während es läuft, Wechsel nicht ansagen (sonst redet der Screenreader ständig)
    zaehler.setAttribute('aria-live', an ? 'polite' : 'off')
    planen()
  }

  zurueck.addEventListener('click', () => {
    zeige(aktuell() - 1)
    planen()
  })
  weiter.addEventListener('click', () => {
    zeige(aktuell() + 1)
    planen()
  })
  pause.addEventListener('click', () => setzePause(!angehalten))
  band.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      e.preventDefault()
      zeige(aktuell() + (e.key === 'ArrowLeft' ? -1 : 1))
    }
  })
  const halten = (an) => () => {
    verweilt = an
    planen()
  }
  box.addEventListener('mouseenter', halten(true))
  box.addEventListener('mouseleave', halten(false))
  box.addEventListener('focusin', halten(true))
  box.addEventListener('focusout', (e) => {
    if (!box.contains(e.relatedTarget)) halten(false)()
  })
  document.addEventListener('visibilitychange', planen)
  let warte
  band.addEventListener('scroll', () => {
    clearTimeout(warte)
    warte = setTimeout(auffrischen, 80)
  })
  setzePause(angehalten)
  auffrischen()
})
