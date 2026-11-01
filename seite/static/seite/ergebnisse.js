// Wettbewerbsergebnisse live: Solange der Wettbewerb läuft, fragt die Seite alle paar
// Sekunden (aus HUBIplan, 15 s) nach dem kleinen Stand und lädt die Rangliste nur bei
// einer Änderung neu. Ohne JavaScript bleibt der Link „Aktualisieren“.
(function () {
  "use strict";
  // Texte in der Sprache der Seite (basis.html, Element seite-texte)
  function t(s) {
    var e = document.getElementById("seite-texte");
    if (!e) return s;
    try { return JSON.parse(e.textContent)[s] || s; } catch (x) { return s; }
  }
  var box = document.getElementById("ergebnis");
  if (!box || !box.dataset.stand || !window.fetch) return;
  var hinweis = document.getElementById("ergebnis-hinweis");
  var version = box.dataset.version || "";
  var sekunden = Math.max(5, parseInt(box.dataset.sekunden, 10) || 15);
  var zeitgeber = null;
  var fehler = 0;
  var fertig = false;

  function melde(text) {
    if (hinweis) hinweis.textContent = text;
  }

  async function neuLaden() {
    var res = await fetch(box.dataset.tabelle, { credentials: "same-origin", cache: "no-store" });
    if (!res.ok) throw new Error("Tabelle " + res.status);
    box.innerHTML = await res.text();
    var jetzt = new Date();
    var sprache = document.documentElement.lang === "en" ? "en-GB" : "de-DE";
    var zeit = jetzt.toLocaleTimeString(sprache, { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    melde(t("Aktualisiert um {zeit} Uhr.").replace("{zeit}", zeit));
  }

  async function pruefe() {
    zeitgeber = null;
    if (fertig || document.hidden) return;
    try {
      var res = await fetch(box.dataset.stand, { credentials: "same-origin", cache: "no-store" });
      if (!res.ok) throw new Error("Stand " + res.status);
      var stand = await res.json();
      if (stand.version && stand.version !== version) {
        await neuLaden();
        version = stand.version;
      }
      fehler = 0;
      if (stand.final) {
        fertig = true;
        melde(t("Die Ergebnisse sind endgültig."));
        return;
      }
    } catch (e) {
      fehler += 1;
    }
    // Bei Fehlern seltener fragen (höchstens alle 2 Minuten)
    plane(Math.min(120, sekunden * Math.pow(2, Math.min(fehler, 3))));
  }

  function plane(s) {
    if (zeitgeber === null) zeitgeber = window.setTimeout(pruefe, s * 1000);
  }

  // Im Hintergrund nicht fragen; beim Zurückkehren sofort
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && !fertig) {
      if (zeitgeber !== null) window.clearTimeout(zeitgeber);
      zeitgeber = null;
      pruefe();
    }
  });
  plane(sekunden);
})();
