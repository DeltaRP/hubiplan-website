# Vereinswebseite mit Daten aus HUBIplan – Konzept

Stand: 2026-10-28, Antworten von Ralf eingearbeitet, noch kein Code geändert.

## 0. Entscheidungen von Ralf (2026-10-28)

| Frage | Entscheidung |
|---|---|
| Bestehende Seite | Unter der Domain des Pilotvereins lag nur eine leere WordPress-Hülle. Sie fällt weg, **kein WordPress mehr**. Die fertige Vereinsseite aus HUBIplan ist der Hauptweg. |
| Kontaktwege | **Kontaktformular und Mailadressen** (Funktionsadressen der Rollen, persönliche Adressen nur mit Einwilligung) |
| Würden | Jede Einheit legt ihre Würden **selbst** an, nichts ist vorgegeben. |
| Majestäten lebender Personen | **Widerspruchsrecht reicht**, keine Einwilligung nötig. |
| Königsliste des Hubertusvereins | Gibt es, kommt aber **nicht ins Repository**. HUBIplan bleibt allgemein; die Liste wird im Echtbetrieb über den Excel-Import eingespielt. |
| Fotos | Ja, **erstmal nur Vorstand, Majestäten und Züge** (Untereinheiten). Keine Bildergalerie vorerst. |
| Wartungsmodus | Pflicht: Während der Entwicklung (und später bei Umbauten) muss Ralf die Seite testen können, ohne dass die Öffentlichkeit sie sieht (siehe 5.2b). |
| Impressum und Datenschutz | Pflicht: Die Webseite bekommt ein Impressum und eigene Datenschutzhinweise, **sinnvoll erzeugt aus den Daten in HUBIplan** (siehe 5.2c). |
| Welche Einheiten | **Nicht jede Einheit bekommt eine Webseite.** Eine Webseite gibt es nur, wo sie ausdrücklich eingerichtet wird. Im Echtbetrieb nur für den Hubertus-Schützenverein, obwohl dort auch Dachverband und Züge hinterlegt sind (siehe 3.0). |
| Statistiken | **Keine** Kennzahlen wie Mitgliederzahl oder Anzahl der Züge auf der Webseite. |
| Seitenaufbau | **Kurze Startseite plus eigene Unterseiten** statt einer langen Scrollseite: Start (Begrüßung, nächste 3 Termine, aktuelles Königspaar, Kontakt-Knopf), Vorstand, Termine (alle + Abo), Züge (Übersicht + je Zug eine Seite), Majestäten (aktuelle + Chronik), Geschichte (Text, Vorsitzende seit Gründung aus der Rollen-Historie, Satzung), Kontakt. Vorstand und Geschichte sind getrennte Seiten (Ralf 2026-10-28). „Geschichte“ ist ein Menüpunkt mit den Unterseiten „Chronik“ (Textseite) und „Ämter“ (Inhaber der Rollen mit „unter Ämter zeigen“), Ralf 2026-10-31. „Geschichte“ ist ein Menüpunkt mit den Unterpunkten „Chronik“ (Textseite) und „Ämter“ (Inhaber der Rollen seit Gründung), Ralf 2026-10-31. Bausteine und Reihenfolge der Startseite stellt die Einheit in HUBIplan unter Webseite › Menü und Bereiche › Startseite ein (Ralf 2026-10-30; Schnittstelle: Liste `home`, Vorlagen `seite/start/<baustein>.html`). Entwurf: https://claude.ai/artifact/P6R8deGuQkct62VGm6XixB |
| Geräte | Die Webseite muss auf **großen Monitoren, Tablets und Smartphones** gleich gut funktionieren. |
| Zusätzlich gewünscht | **Terminkalender**, fürs Smartphone abonnierbar; optional **Links zu Social-Media-Kanälen** je Einheit; **Kontaktformular mit Spam-Schutz** |


> **Kein Rechtsrat.** Stellen, die vor dem Echtbetrieb eine fachkundige Stelle prüfen sollte (Datenschutzbeauftragter, Landesverband, Anwalt), sind mit **⚖** markiert.

## 1. Ziel

Eine öffentliche Webseite für **ausgewählte** Einheiten (im Pilot nur der Verein), deren Inhalte zum großen Teil **automatisch aus HUBIplan** kommen und sich mitändern, wenn sich dort etwas ändert:

- Vorstand und Ansprechpartner mit freigegebenen Kontaktwegen
- Untereinheiten (beim Pilotverein: die Züge) mit eigener Unterseite
- Chronik: wer wann König (Prinz, Kaiser, Zugkönig …) war, frühere Vorsitzende, Ehrenmitglieder
- Termine, Satzung, öffentliche Dokumente, Impressum und Datenschutzhinweise

Leitlinie: **Nichts wird öffentlich, was nicht ausdrücklich freigegeben ist.** Die Webseite liest nie direkt Mitgliederdaten, sondern nur eine schmale, eigens berechnete „öffentliche Sicht“.

## 2. Was HUBIplan heute schon hat

| Vorhanden | Nutzbar für die Webseite |
|---|---|
| Einheiten mit Name, Kurzname, Gründungsjahr, Anschrift, Kontakt, Website, Logo, Farben, Bezeichnung („Zug/Züge“), Baum beliebiger Tiefe | Steckbrief, Liste der Untereinheiten, Jubiläum der Einheit („105 Jahre“), Design |
| Rollen (`access.Role`) mit „Vorstandsrolle“ und „vertritt die Einheit“, Zuordnungen mit von/bis und Bezug zur Person | Vorstand heute **und** Chronik der Vorsitzenden aus der Historie |
| Rollen in Untereinheiten (`DepartmentRole`, z. B. Oberleutnant, Spieß) mit von/bis | Ansprechpartner je Zug |
| Ehrungen mit Verleihung von/bis | Liste der Ehrenmitglieder |
| Öffentlicher Terminkalender als JSON und iCal (`/api/public/…`, schon mit CORS und 5 Minuten Cache, ausdrücklich „für die Vereinswebseite“) | Terminbaustein, ohne Neuentwicklung |
| Satzung öffentlich abrufbar, Dokumentenordner „öffentlich per Link“ | Download-Bereich |
| Impressum und Datenschutzhinweise je Einheit (`/impressum/<key>`), Untereinheiten erben | Pflichtseiten der Webseite |
| Mitgliederfotos mit Einwilligungsdatum, EXIF entfernt | Fotos von Ansprechpartnern und Majestäten, nur mit Einwilligung |

**Was fehlt:** Würden wie König oder Prinz kennt HUBIplan nicht. Es gibt auch kein Kennzeichen „öffentlich zeigen“ an Rollen und keine Einwilligung zur Veröffentlichung (außer für Fotos). Das ist der Kern der neuen Arbeit.

## 3. Inhalte der Webseite (Bausteine)

### 3.0 Welche Einheit hat eine Webseite?
- **Standard: keine.** Eine Einheit hat erst dann eine Webseite, wenn sie in HUBIplan unter „Webseite“ ausdrücklich **eingerichtet** wird. Ohne Einrichtung gibt es weder Seite noch Wartungsseite noch Daten in der Schnittstelle, und der Menüpunkt zeigt nur „Webseite einrichten“.
- **Wer einrichten darf:** Das Modul „Webseite“ wird je Einheit freigeschaltet (wie die anderen Module über `enabled_modules`), danach richtet ein Berechtigter der Einheit die Seite ein. So bleibt es bei anderen Einheiten aus, auch wenn sie das Recht hätten.
- **Untereinheiten bekommen keine eigene Webseite**, sondern erscheinen als **Unterseiten** auf der Seite der Einheit darüber (z. B. `…/zuege/jaegerzug`), mit ihren Ansprechpartnern, Terminen, Zugkönigen und Fotos. Die Einheit mit der Webseite legt fest, welche Untereinheiten erscheinen (alle, ausgewählte, keine).
- **Die Einheit darüber** (Dachverband) bekommt im Pilot keine Webseite. Auf der Vereinsseite kann sie als „Mitglied im …“ mit Link zu ihrer eigenen Website erscheinen (aus dem vorhandenen Feld „Website“).
- Technisch erlaubt das System trotzdem mehrere Webseiten (z. B. später für einen anderen Verein auf derselben Plattform), jede mit eigener Domain.


Jeder Baustein lässt sich auf der Webseite einzeln einschalten.

### 3.1 Steckbrief
Name, Logo, Gründungsjahr und Alter, Anschrift, allgemeine Kontaktadresse, Link zu Satzung und Impressum. Keine Einwilligung nötig, da keine Personendaten. **Keine Statistiken** wie Mitgliederzahlen (Ralf 2026-10-28).

### 3.2 Vorstand und Ansprechpartner
- An jeder Rolle (Vorstand und Untereinheit) ein neues Kennzeichen **„auf der Webseite zeigen“** plus Reihenfolge. So erscheint der 1. Vorsitzende, aber nicht der Datenschutzbeauftragte, wenn der Verein das nicht will.
- Gezeigt wird die Rolle mit dem **aktuellen** Inhaber (aus der von/bis-Zuordnung). Wechselt der Vorsitz in HUBIplan, wechselt die Webseite mit. Unbesetzte Rollen werden ausgeblendet oder als „derzeit unbesetzt“ gezeigt (Einstellung).
- **Namensform** je Einheit: „Max Mustermann“ oder „Max M.“.
- **Kontaktwege**, von sicher nach offen:
  1. **Kontaktformular** je Rolle (entschieden): Die Nachricht geht per Mail an den aktuellen Inhaber, Antwort-an ist der Absender. Keine Adresse wird sichtbar, kein Spam an Privatadressen, Rollenwechsel ohne Pflegeaufwand.
  2. **Funktionsadresse** der Rolle (z. B. vorstand@example.org), wenn der Verein eine pflegt (neues Feld an der Rolle; entschieden). Die Adresse wird gegen einfache Adress-Sammler verschleiert ausgegeben (erst im Browser zusammengesetzt).
  3. **Persönliche E-Mail oder Telefon** aus der Mitgliederakte, nur mit Einwilligung der Person (siehe 4).
- Foto des Inhabers nur mit Foto-Einwilligung **und** Veröffentlichungs-Einwilligung.

### 3.3 Untereinheiten (Züge)
Liste mit Logo, Name, Gründungsjahr (ohne Mitgliederzahl), und je Zug eine Unterseite mit eigenen Ansprechpartnern (Rollen mit Kennzeichen), eigenen Terminen (gibt es schon je Untereinheit) und eigener Chronik (Zugkönige). Ein Zug kann seinen Baustein abschalten. Beim Dachverband zeigt derselbe Baustein die angeschlossenen Vereine.

### 3.4 Chronik und Würdenträger („Wer war wann König?“)
HUBIplan kann Könige heute nicht aus den Mitgliederdaten ermitteln, weil sie nirgends gespeichert sind. Vorschlag: ein kleines neues Modul **Würden** (Bezeichnung frei, z. B. „Majestäten“):

- **Würde** je Einheit, von der Einheit selbst angelegt und frei benannt (nichts vorgegeben), z. B.: König, Königin, Prinz, Schülerprinz, Kaiser, Zugkönig, Regimentskönig, Bester Schütze … mit Reihenfolge und Kennzeichen „öffentlich in der Chronik“.
- **Regentschaft**: Würde, Jahr (Schützenfestjahr) oder von/bis, Person.
  - Person ist entweder ein **Mitglied aus HUBIplan** (verknüpft, erscheint dann auch in der Mitgliederakte unter „Rollen & Ehrungen“) oder ein **Freitext-Name** für die Zeit vor der Datenübernahme (1920 bis heute), für Verstorbene und Nicht-Mitglieder.
  - Begleitpersonen (Königin, Minister, Adjutanten) als weitere Einträge mit Bezug auf die Regentschaft, ebenfalls Mitglied oder Freitext.
  - Optional Foto, Bemerkung („Jubiläumskönig“).
- Daraus **ermittelt** HUBIplan: Königsliste je Jahr, „x-maliger König“, Jubiläen („25 Jahre Silberkönig“, auf Wunsch in der Jubiläumsliste), auf Wunsch eine Regel „Kaiser nach 3 Königswürden“. Die Würde des Zugs fließt in die Chronik des Zugs, die des Vereins in die des Vereins, der Dachverband sieht die Regimentskönige.
- Import: Die Königsliste liegt im Verein meist als Tabelle oder Festschrift vor. Ein Excel-Import (Jahr, Würde, Name, optional Begleitpersonen) mit automatischem Abgleich auf Mitglieder (Vorschlag, Bestätigung durch den Vorstand) spart das Abtippen. Echte Listen (z. B. die des Hubertusvereins) gehören **nie ins Repository**: Sie werden im Echtbetrieb über diesen Import eingespielt. Repository und Testserver enthalten nur erfundene Beispiele.

Warum nicht einfach Ehrungen? Ehrungen verändern Beiträge, hängen nur an Mitgliedern und haben keine Jahresliste und keine Begleitpersonen. Technisch kann das Modul die Bedienung der Ehrungen nachbauen, ist aber eine eigene Tabelle.

Weitere Chroniken ohne neues Modul:
- **Vorsitzende seit …** aus der Rollen-Historie (Rollen mit Kennzeichen „in der Chronik zeigen“). Ältere Vorsitzende lassen sich schon heute als reine Historie ohne Benutzer erfassen.
- **Ehrenmitglieder** aus den Ehrungen (Kennzeichen „öffentlich“ an der Ehrung).

### 3.5 Terminkalender (Pflichtbaustein)
Baut auf dem vorhandenen öffentlichen Kalender auf (JSON und iCal gibt es schon):
- Liste der nächsten Termine und Monatsansicht, Filter nach Kategorie und Untereinheit, Detailseite je Termin mit Ort, Adresse (Link zur Karte) und Absage-Hinweis.
- **Abo fürs Smartphone**: Knopf „Kalender abonnieren“ mit `webcal://`-Link (öffnet direkt die Kalender-App auf iPhone und Android), Anleitung für Google-Kalender, dazu ein QR-Code zum Abscannen. Einzeltermine als .ics zum Hinzufügen.
- Kalender des Vereins enthält auf Wunsch die öffentlichen Termine der Züge mit (Einstellung), jeder Zug hat zusätzlich sein eigenes Abo.

### 3.6 Social Media
- Die Kanäle sind **Stammdaten der Einheit in HUBIplan**, unabhängig von einer Webseite: Jede Einheit (auch Dachverband und Züge) kann sie unter Einstellungen › Organisation neben Website, E-Mail und Telefon hinterlegen (Art: Instagram, Facebook, TikTok, YouTube, WhatsApp-Kanal, Mastodon, Sonstiges; Adresse; Reihenfolge).
- HUBIplan kann sie auch selbst nutzen, z. B. im Fuß von Rundschreiben und im Mitgliederbereich (jeweils abschaltbar).
- Die Webseite nutzt sie **optional**: Schalter „Social-Media-Links zeigen“ in der Verwaltung „Webseite“. Auf den Unterseiten der Züge erscheinen die Kanäle des jeweiligen Zugs, wenn er welche hinterlegt hat.
- Angezeigt werden nur **einfache Links** mit Symbolen (in Kopf- oder Fußzeile und im Steckbrief), keine eingebetteten Beiträge oder Like-Knöpfe: So lädt die Seite nichts von Meta oder Google, und es braucht weder Cookie-Banner noch Einwilligung. Symbole liegen in HUBIplan-Website selbst.

### 3.7 Fotos
- **Personen aus der Mitgliederdatei** (Vorstand, Ansprechpartner, Majestäten): Foto aus der Akte, nur mit Foto-Einwilligung und Veröffentlichungs-Einwilligung.
- **Bilder der Einheit** (Zugfoto, Vereinsheim, Fahne): eigene Bilder je Einheit für Steckbrief und Kopfbereich.
- **Majestäten**: eigenes Foto je Regentschaft (z. B. Königspaar), auch für historische Einträge.
- **Bildergalerie** (später, vorerst nicht gewünscht): Alben, z. B. „Schützenfest 2026“, hochgeladen vom Vorstand, Größe beim Hochladen verkleinert, EXIF entfernt. Für Gruppen- und Festbilder trägt die Einheit die Verantwortung (⚖ Kunsturhebergesetz); ein Hinweis beim Hochladen und ein einfacher Weg „Bild entfernen lassen“ über das Kontaktformular.

### 3.7a Texte und Bilder der Webseite (in HUBIplan gepflegt)
Inhalte, die HUBIplan nicht aus der Vereinsverwaltung kennt (Begrüßung, Geschichte, Anfahrt, Text eines Zugs, historische Fotos), werden **in HUBIplan unter „Webseite › Texte und Bilder“** gepflegt, nicht im Repository und nicht in der Webseite selbst. So bleiben sie in Sicherung und JSON-Export, und die Webseite bleibt reine Darstellung.
- **Textbausteine mit festem Platz**: Begrüßungstext der Startseite, Kurztext je Zug.
- **Textseiten**: Titel, Text mit einfachem Editor (Überschriften, fett, Listen, Links, Bilder), Platz im Menü und Reihenfolge, z. B. „Geschichte“, später „Anfahrt“ oder „Schützenfest“.
- **Bilder** werden in HUBIplan hochgeladen, beim Hochladen verkleinert und von EXIF befreit, mit Bildunterschrift und Alternativtext.
- **Entwurf und Veröffentlichung**: Änderungen sind erst nach „Veröffentlichen“ sichtbar, vorher in der Vorschau. Frühere Fassungen bleiben erhalten und lassen sich zurückholen (wie beim Undo in HUBIplan).
- **Recht** „Webseite: Inhalte bearbeiten“ als eigene Berechtigung, damit z. B. der Schriftführer Texte pflegen kann, ohne die übrigen Einstellungen der Webseite zu ändern.
- Erstbefüllung beim Hubertusverein: Ralf liefert vorhandene Texte (z. B. aus der Festschrift), sie werden im Echtbetrieb in HUBIplan eingetragen, nie ins Repository.

### 3.8 Satzung, Dokumente
Vorhandene öffentliche Links werden als Bausteine eingebunden (Satzung und optional Beitragsordnung und Gründungsurkunde als PDF, öffentlicher Ordner).

### 3.9 Später möglich
- **Neuigkeiten**: ein Rundschreiben zusätzlich „auf der Webseite veröffentlichen“.
- **Online-Aufnahmeantrag**: landet als Antrag in HUBIplan, der Vorstand nimmt auf, inklusive Einwilligungen von Anfang an.
- **Jubilare des Jahres** und Geburtstage nur mit Einwilligung.

## 4. Datenschutz

### 4.1 Rechtsgrundlagen (⚖)
| Angabe | Übliche Einordnung |
|---|---|
| Name und Funktion von Vorstandsmitgliedern | berechtigtes Interesse des Vereins (Art. 6 Abs. 1 f DSGVO), Widerspruch möglich; Datenschutzhinweise der Einheit müssen es erwähnen |
| Private Telefonnummer, private E-Mail, Anschrift | nur mit Einwilligung |
| Fotos | Einwilligung (Kunsturhebergesetz und Art. 6 Abs. 1 a DSGVO), die vorhandene Foto-Einwilligung reicht für die Webseite **nicht** automatisch |
| Majestäten lebender Personen | im Schützenwesen traditionell öffentlich; berechtigtes Interesse mit Widerspruchsrecht (**von Ralf so entschieden**), Hinweis in den Datenschutzhinweisen |
| Verstorbene, Freitext-Einträge aus der Festschrift | DSGVO gilt nicht für Verstorbene; Pietät und Rechte Angehöriger beachten |
| Jubilare, Geburtstage | nur mit Einwilligung |

### 4.2 Umsetzung
- **Veröffentlichungs-Einwilligung je Person** mit Kategorien: Name mit Funktion, Foto, E-Mail, Telefon, Würden und Chronik, Jubiläen. Je Kategorie: Datum, erfasst durch (Vorstand, Mitglied selbst, Papierantrag), Widerruf mit Datum. Verlauf bleibt erhalten (wie bei der Foto-Einwilligung).
- **Widerspruch** gegen „Name mit Funktion“ ist ein eigenes Kennzeichen, das die Grundregel aufhebt.
- **Mitgliederbereich**: Das Mitglied sieht unter „Meine Daten“, was öffentlich über es erscheint, und kann Einwilligungen selbst geben oder widerrufen. Ein Widerruf wirkt sofort (Cache wird geleert).
- **Vorschau** für den Vorstand: „So sieht die Webseite aus“ mit Hinweis, wer wegen fehlender Einwilligung ausgeblendet ist.
- Eine Person ohne Einwilligung bleibt in der Chronik als „N. N.“ oder wird ausgelassen (Einstellung je Einheit).
- Das Kontaktformular speichert Nachrichten nur bis zum Versand (höchstens 7 Tage im Mail-Ausgang), nennt in einem Satz, wohin die Nachricht geht, und verlinkt die Datenschutzhinweise.
- Die vorhandene Vorlage für die Datenschutzhinweise der Einheit bekommt einen Abschnitt „Veröffentlichung auf der Webseite“.

## 5. Technik

### 5.1 Drei Wege, die Daten zu nutzen
1. **Fertige Vereinsseite aus HUBIplan** (Hauptweg, ersetzt beim Hubertusverein die WordPress-Hülle): serverseitig gerenderte Seiten (Django-Templates, kein JavaScript nötig, gut für Suchmaschinen und schnell), Design aus Logo und Farben der Einheit. Adresse z. B. `https://verein.example.org/seite/hubertus` oder eine eigene Domain, die per Hestia-nginx auf diese Seite zeigt.
2. **Bausteine zum Einbetten** für andere Vereine, die eine eigene Seite behalten wollen: ein Skript-Schnipsel `<script src=".../einbetten.js" data-baustein="vorstand" data-schluessel="…">`, das den Baustein in die Seite zeichnet (im Shadow DOM, damit das Design der Seite nicht stört). Kein WordPress-Plugin. Nachrangig, da der Pilot es nicht braucht.
3. **JSON-Schnittstelle** für Webmaster, die alles selbst gestalten, nach dem Muster des vorhandenen Kalender-JSON.

Alle drei nutzen dieselbe öffentliche Sicht, daher gibt es die Datenschutzlogik nur einmal.

### 5.1a Eigenes Repository `hubiplan-website` (Ralfs Vorschlag, 2026-10-28)
Die Webseite wird ein **eigenes Projekt** neben HUBIplan. Aufteilung:

| `hubiplan` (bestehendes Repository) | `hubiplan-website` (neu) |
|---|---|
| Daten und Regeln: Einwilligungen und Widerspruch, Kennzeichen an Rollen, Funktionsadressen, Würden-Modul, Social-Media-Kanäle, Domains je Einheit, Verwaltung „Webseite“ mit Vorschau | Darstellung: Seitenvorlagen, Design aus Logo und Farben, Kalenderansicht, Chronik, Galerie, Kontaktformular-Oberfläche |
| **Öffentliche Schnittstelle** `/api/public/site/…` (nur freigegebene Daten, versioniert, z. B. `v1`) | liest ausschließlich diese Schnittstelle, hat **keinen Zugriff auf die Datenbank** |
| Kontaktformular-Annahme mit Spam-Prüfung und Versand über den Mail-Ausgang | reicht das Formular an HUBIplan durch, Rechenaufgabe im Browser |

Vorteile: Datenschutzregeln liegen nur an einer Stelle; die Webseite kann keine Mitgliederdaten sehen, selbst wenn sie fehlerhaft ist; Webseite und Verwaltung lassen sich getrennt ändern und ausrollen; andere Vereine können die Schnittstelle mit eigener Seite nutzen.
Nachteile: zwei Repositories und ein zusätzlicher Container; die Schnittstelle braucht eine Versionsnummer, damit beide Seiten nicht gleichzeitig geändert werden müssen.

Technik-Vorschlag für `hubiplan-website`: kleines Python-Projekt (Django ohne eigene Datenbank oder vergleichbar schlank) mit serverseitig gerenderten Seiten, Zwischenspeicher für die Antworten der Schnittstelle (wenige Minuten), eigener Docker-Container, Lizenz AGPL wie HUBIplan. Ein Container bedient alle Einheiten; welche gemeint ist, ergibt der Hostname (Domains pflegt HUBIplan). Auf Dogado eigener Port hinter Hestia-nginx (z. B. 127.0.0.1:8111). Gleiche Regeln wie im Hauptprojekt: Tests nur lokal, keine echten Daten im Repository, CI nur von Hand.

### 5.2 Backend (im Repository `hubiplan`)
- Neue App `website`: Tabelle `WebsitePublication`, **nur für Einheiten, deren Webseite eingerichtet ist** (höchstens eine je Einheit; Zustand, öffentlicher Schlüssel bzw. Kurzadresse, eingeschaltete Bausteine, Namensform, Umgang mit fehlenden Einwilligungen, Suchmaschinen erlauben ja/nein).
- Neue App bzw. Modul `honors` für Würden und Regentschaften (mit RLS wie alle Vereinsdaten).
- Einwilligungen als eigene Tabelle an der Person.
- Kennzeichen „auf der Webseite zeigen“, „in der Chronik zeigen“, Funktionsadresse und Reihenfolge an `Role` und `DepartmentRole`; „öffentlich“ an `HonoraryTitle`.
- Öffentliche Endpunkte `/api/public/site/<schlüssel>/…`: nur lesen, ohne Anmeldung, CORS offen, Cache wenige Minuten, Drosselung je IP. Ein zentraler Dienst `website/public_view.py` berechnet aus den Daten die freigegebene Sicht. Keine internen IDs, keine fortlaufenden Nummern.
- Kontaktformular mit **Spam-Schutz in Schichten**, alles selbst gehostet, ohne Google, hCaptcha oder Cookies:
  1. Honigtopf-Feld (für Menschen unsichtbar, Bots füllen es aus)
  2. Zeitprüfung (signierter Zeitstempel: schneller als 3 Sekunden oder älter als 2 Stunden wird abgelehnt)
  3. kleine Rechenaufgabe im Browser (Proof of Work, wie ALTCHA; kostet einen Menschen eine halbe Sekunde, einen Massenversender viel Rechenzeit)
  4. Drosselung je IP und je Einheit, harte Obergrenze (z. B. 20 Formularmails pro Stunde je Einheit, wichtig wegen der 100 Mails pro Stunde je Postfach auf Dogado)
  5. Inhaltsprüfung: zu viele Links, bekannte Spam-Wörter, gleiche Nachricht mehrfach → Nachricht wird zurückgehalten statt verschickt; der Vorstand sieht zurückgehaltene Nachrichten in HUBIplan und kann sie freigeben.
  Versand über den vorhandenen Mail-Ausgang an die gewählte Rolle bzw. die allgemeine Adresse, Antwort-an = Absender, Kopie an den Absender nur auf Wunsch und nur nach bestandener Prüfung (sonst wird das Formular zur Spam-Schleuder).
- Neue Tabelle `SocialLink` an der Einheit (Art, Adresse, Reihenfolge), gepflegt in den Organisations-Einstellungen, Teil des JSON-Exports; die öffentliche Schnittstelle liefert sie nur, wenn die Webseite sie zeigen soll.

### 5.2a Darstellung auf allen Geräten
- **Mobil zuerst** gebaut, mit fließendem Raster: einspaltig auf dem Smartphone, zwei Spalten auf dem Tablet, auf großen Monitoren begrenzte Lesebreite (ca. 1200 px Inhalt, Bilder und Kopfbereich dürfen breiter werden), damit Zeilen nicht endlos lang werden.
- Navigation: auf dem Smartphone ein Menü-Knopf, ab Tablet eine Leiste. Termine als Liste auf dem Smartphone, als Monatsansicht ab Tablet.
- Bilder in mehreren Größen (`srcset`), damit das Smartphone keine Monitor-Bilder lädt; Logo als SVG, wenn vorhanden.
- Tasten groß genug zum Tippen (mind. 44 px), Telefonnummern und Adressen antippbar (Anruf, Karte), Kalender-Abo per `webcal://` direkt in die Kalender-App.
- Barrierearm (Kontraste aus den Vereinsfarben geprüft, Tastaturbedienung), ohne Webschriften von Google, schnell auch über Mobilfunk.
- Getestet wird lokal mit Playwright in drei Breiten (Smartphone, Tablet, großer Monitor) plus axe-core, wie im Hauptprojekt.

### 5.2b Wartungsmodus und Vorschau
Jede eingerichtete Webseite hat einen **Zustand**, eingestellt in HUBIplan unter „Webseite“:

| Zustand | Öffentlichkeit sieht | Berechtigte sehen |
|---|---|---|
| **Aus** | nichts (404) | Vorschau |
| **Wartung** (Standard für neue Seiten) | eine schlichte Wartungsseite: Name und Logo der Einheit, frei wählbarer Hinweistext („Hier entsteht unsere neue Webseite“), Link zu Impressum und Datenschutz | die vollständige Seite mit einem Hinweisband „Vorschau – nicht öffentlich“ |
| **Öffentlich** | die Seite | die Seite |

- **Wie man in die Vorschau kommt:** In HUBIplan unter „Webseite“ gibt es den Knopf „Vorschau öffnen“ (nur mit dem Recht, die Webseite zu verwalten). HUBIplan erzeugt einen kurzlebigen, signierten Vorschau-Schlüssel; die Webseite tauscht ihn gegen ein Vorschau-Cookie (gültig z. B. 8 Stunden, nur für diese Einheit). Ein Knopf im Hinweisband beendet die Vorschau.
- **Vorschau-Link zum Weitergeben** (z. B. an andere Vorstandsmitglieder ohne HUBIplan-Zugang): zeitlich begrenzt (1 bis 14 Tage), jederzeit widerrufbar, Liste der aktiven Links in HUBIplan.
- **Kein Datenleck über die Schnittstelle:** Im Zustand „Aus“ oder „Wartung“ liefert auch die öffentliche Schnittstelle nur die Wartungsangaben. Die vollständigen Daten gibt sie nur mit gültigem Vorschau-Schlüssel heraus. Termine, Kalender-Abo und Kontaktformular sind in der Wartung ebenfalls aus (das bisherige Kalender-Abo aus HUBIplan bleibt davon unberührt).
- **Suchmaschinen:** Wartungsseite mit HTTP-Status 503 und `Retry-After`, `noindex`; Vorschauseiten immer `noindex` und nie im Cache für alle.
- **Testserver:** Dort steht jede Seite zusätzlich hinter einem allgemeinen Schalter „nur Vorschau“ (Umgebungsvariable), damit erfundene Testdaten nie öffentlich wirken.
- **Wartung beim Ausrollen:** ein globaler Schalter im Container (Datei oder Umgebungsvariable) zeigt allen Einheiten kurz die Wartungsseite, z. B. während eines Updates.
- Jede Änderung des Zustands wird in HUBIplan protokolliert (wer, wann).

### 5.2c Impressum und Datenschutzhinweise der Webseite
Beides erscheint auf **jeder Seite im Fuß** und als eigene Seite unter der Domain der Webseite (`/impressum`, `/datenschutz`), auch auf der Wartungsseite. Die Texte entstehen in HUBIplan, die Webseite zeigt sie nur an.

**Impressum** (⚖ § 5 DDG; § 18 Abs. 2 MStV)
- Kommt aus dem vorhandenen Impressum der Einheit (`organizations.Imprint`): Name, Rechtsform, Anschrift, Vertretungsberechtigte (aus Rollen mit „vertritt die Einheit“, also immer aktuell), E-Mail, Telefon, Register, USt-IdNr. Ein Zug erbt wie bisher das Impressum des Vereins; „auf eigenes Impressum verlinken“ wird auf der Webseite als Link angezeigt.
- Wird angezeigt, nicht nur verlinkt, damit es auf derselben Domain „unmittelbar erreichbar“ ist.
- **Verantwortlich nach § 18 Abs. 2 MStV**: Sobald die Seite redaktionelle Inhalte hat (eigene Textseiten, Neuigkeiten, Chronik mit Texten), ist das Feld Pflicht. HUBIplan warnt in der Verwaltung „Webseite“, wenn es leer ist, und schlägt die Inhaber einer gewählten Rolle (z. B. Schriftführer) vor.
- Prüfliste in HUBIplan vor dem Schalten auf „öffentlich“: fehlen Pflichtangaben (Anschrift, zweiter Kontaktweg, Vertretungsberechtigte, Registernummer beim e.V.), lässt sich die Seite nicht veröffentlichen, nur in Wartung testen.

**Datenschutzhinweise der Webseite** (⚖ Art. 13 DSGVO)
Eigener Text, getrennt von den Hinweisen für Mitglieder. Der vorhandene Generator (`organizations/imprint_generator.py`, heute für die Mitglieder-Hinweise) bekommt eine Funktion `website_privacy(org)`, die nur die Abschnitte erzeugt, die auf die Seite tatsächlich zutreffen:

| Abschnitt | Woher HUBIplan das weiß |
|---|---|
| Verantwortlicher, Kontakt, Datenschutzbeauftragter | Impressum der Einheit |
| Hosting und Auftragsverarbeitung (Plattformbetreiber, Rechenzentrum) | Plattform-Einstellungen (Betreiber, Hosting-Anbieter); fehlt der Anbieter, steht ein Platzhalter in eckigen Klammern |
| Server-Protokolle (IP-Adresse, Zeit, Seite, Browser; Speicherdauer) | fester Text, Speicherdauer aus der Betriebseinstellung (z. B. 7 Tage) |
| Cookies | nur wenn nötig: Vorschau-Cookie für Berechtigte; keine Tracking-Cookies, daher kein Cookie-Banner |
| Kontaktformular und E-Mail-Adressen (Zweck, Rechtsgrundlage, Empfänger = Rolleninhaber, Speicherdauer im Mail-Ausgang, Spam-Schutz ohne Drittanbieter) | nur wenn Kontaktformular bzw. Funktionsadressen eingeschaltet |
| Kalender-Abo (Abruf der Kalenderdatei, keine Anmeldung) | nur wenn Terminbaustein eingeschaltet |
| Veröffentlichte Personen: Vorstand (Name, Funktion), Majestäten und Chronik, Fotos; Rechtsgrundlage (berechtigtes Interesse bzw. Einwilligung), **Widerspruchsrecht nach Art. 21** mit Weg dorthin (Kontaktformular, Mitgliederbereich) | aus den eingeschalteten Bausteinen und den Einwilligungsregeln |
| Links zu Social-Media-Kanälen (reine Links, Daten erst beim Anbieter nach dem Klick) | nur wenn Kanäle eingetragen, mit den Namen der Anbieter |
| Rechte der Betroffenen, Beschwerderecht bei der Aufsichtsbehörde | fester Text; Aufsichtsbehörde aus dem Bundesland der Anschrift (z. B. NRW: LDI NRW) |
| Stand | Datum der letzten Erzeugung |

- Wie heute: Knopf „Text aus den Einstellungen erzeugen“, danach frei bearbeitbar. Ändern sich die Bausteine (z. B. Kontaktformular eingeschaltet), zeigt HUBIplan einen Hinweis „Datenschutzhinweise der Webseite passen nicht mehr zu den Einstellungen – neu erzeugen?“.
- Alternativ wie beim bestehenden Impressum: auf eine eigene Datenschutzseite verlinken.
- Die Hinweise für Mitglieder bekommen einen Abschnitt „Veröffentlichung auf der Webseite“ mit Verweis auf diese Seite.

### 5.3 Frontend (Verwaltung, im Repository `hubiplan`)
- Neuer Bereich **Webseite** im Menü der Einheit: Bausteine an/aus, Vorschau, Einbett-Schnipsel zum Kopieren, Adresse der fertigen Seite.
- **Würden** unter Mitglieder › Einrichtung (Würden anlegen) und als eigene Liste „Chronik“ (Regentschaften erfassen, Excel-Import).
- In der Mitgliederakte: Reiter „Rollen & Ehrungen“ zeigt Würden mit, neuer Abschnitt „Veröffentlichung“ mit den Einwilligungen.
- Lernhilfen („Warum?“) für die Einwilligungen.

### 5.4 Betrieb
- Echtbetrieb auf Dogado: HUBIplan läuft dort hinter Hestia-nginx auf 127.0.0.1:8110 (Verwaltung und öffentliche Schnittstelle unter verein.example.org). Die Vereinsseite aus `hubiplan-website` läuft als **eigener Container** auf 127.0.0.1:8111 mit eigener Hestia-Proxy-Vorlage (app-8111) und ruft die Schnittstelle von HUBIplan auf. Sie greift auf nichts anderes im HUBIplan-Stack zu (keine Datenbank, kein Redis).
- Domain: Die WordPress-Hülle unter der Domain des Pilotvereins (mit `www.`) wird erst nach Ralfs ausdrücklichem OK abgeschaltet (mit Sicherung); erst dann zeigt die Hauptdomain auf 8111. Bis dahin läuft die Seite nur unter einer Test-Adresse im Wartungsmodus. `hubiplan-website` erkennt am Hostnamen, welche Einheit gemeint ist (Tabelle „Domains“ je Einheit in HUBIplan).
- Mails des Kontaktformulars gehen über HUBIplans Mail-Ausgang und das Postfach verein@example.org (100 Mails pro Stunde, geteilt mit Rundschreiben), daher die harte Obergrenze für Formularmails.
- Last: Öffentliche Seiten werden gecacht, Bilder in fester Größe ausgeliefert. Für die Größenordnung eines Vereins unkritisch.
- Testserver nur mit erfundenen Daten, wie immer.

## 6. Vorgeschlagene Stufen (nach Ralfs Antworten)

| Stufe | Inhalt | Ergebnis |
|---|---|---|
| 1 | **Wartungsmodus und Vorschau (zuerst)**, **Impressum und erzeugte Datenschutzhinweise der Webseite** mit Prüfliste vor dem Veröffentlichen, Veröffentlichungs-Einwilligungen und Widerspruch, Kennzeichen und Funktionsadressen an Rollen, öffentliche Sicht, **fertige Vereinsseite** (Startseite mit Steckbrief, Vorstand, Untereinheiten mit Unterseiten, **Terminkalender mit Smartphone-Abo**, Satzung, Impressum, Datenschutz), **Social-Media-Links**, **Kontaktformular mit Spam-Schutz**, **Inhalte pflegen (Begrüßung, Geschichte als Textseite, Bilder, Entwurf/Veröffentlichen)**, Verwaltung „Webseite“ mit Vorschau, Webseite nur für eingerichtete Einheiten, Untereinheiten als Unterseiten, Domain | Die WordPress-Hülle kann weg |
| 2 | Modul Würden (je Einheit frei) mit Chronik, Fotos, Begleitpersonen, Excel-Import; Vorsitzende und Ehrenmitglieder | „Wer war wann König?“ |
| 3 | Weitere Textseiten (Anfahrt, Schützenfest), Bilder der Einheit (Zugfotos) | Volle Vereinsseite |
| 4 | Bildergalerie, Neuigkeiten aus Rundschreiben, Online-Aufnahmeantrag, Einbett-Bausteine und JSON für andere Vereine | mehr Leben auf der Seite |

## 7. Noch offen
1. Freigabe zur Umsetzung von Stufe 1.
2. Die Abschaltung der WordPress-Hülle und das Umstellen der Domain auf Dogado geschieht erst nach Ralfs OK und nach dem Echtbetrieb-Umzug (eigener Thread).
