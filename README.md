# HUBIplan-Website

Öffentliche Vereinswebseiten mit Daten aus [HUBIplan](https://github.com/DeltaRP/hubiplan),
der webbasierten Vereinsverwaltung. Jede Einheit, für die in HUBIplan eine Webseite
eingerichtet ist (z. B. ein Verein), bekommt eine eigene Seite. Ihre Inhalte ändern sich
mit den Daten in HUBIplan; Untereinheiten (z. B. Züge) erscheinen als Unterseiten.

Konzept: [docs/konzept.md](docs/konzept.md). Betrieb auf Test- und Echtserver:
[docs/betrieb.md](docs/betrieb.md).

## Inhalte

- Startseite aus Bausteinen, die HUBIplan ein- und ausschaltet und ordnet: Begrüßung,
  Bilderkarussell, nächste Termine, Geburtstage, aktuelle Majestäten, Untereinheiten
- Aktuelles: eigene Beiträge der Einheit von Instagram und Facebook
- Vorstand und Ansprechpartner mit Funktionsadressen und Ehrungen
- Untereinheiten mit eigenen Unterseiten (Pfad nach der Bezeichnung in HUBIplan, z. B. `/zuege/`)
- Terminkalender nach Monaten, Filter je Untereinheit, Abo fürs Smartphone mit QR-Code
- Majestäten: Würden mit aktuellen Trägern und Chronik
- Geschichte mit Chronik (Text) und Ämtern (z. B. Vorsitzende seit Gründung), Satzung, Dokumente und weitere Textseiten
- Kontaktformular (der Browser schickt direkt an HUBIplan, Spamschutz dort)
- Impressum und Datenschutzhinweise, auch im Wartungsmodus erreichbar
- Wartungsmodus und Vorschau-Link aus HUBIplan

Die Seite passt sich an Monitor, Tablet und Smartphone an. Alle Adressen stehen in
[docs/betrieb.md](docs/betrieb.md#seiten).

## Aufbau

Die Webseite ist reine **Darstellung**. Sie liest ausschließlich die öffentliche,
versionierte Schnittstelle von HUBIplan (`/api/public/site/v1/…`) und hat keinen Zugriff
auf die Datenbank. Welche Daten öffentlich sind (Einwilligungen, Widerspruch, Kennzeichen
an Rollen), entscheidet allein HUBIplan. So kann auch eine fehlerhafte Webseite keine
Mitgliederdaten zeigen.

Ein Container bedient alle Einheiten; welche Einheit gemeint ist, ergibt sich aus dem
Hostnamen. Bilder und Logos kommen über die Seite selbst (`/medien/…`).

```text
Browser ──HTTPS──> Webserver ──> Container website ──> HUBIplan (/api/public/site/v1/)
```

## Technik

| Teil | Technik |
| --- | --- |
| Anwendung | Python 3.12, Django 5.2 LTS ohne Datenbank |
| Texte | markdown-it-py (Markdown aus HUBIplan) |
| QR-Codes | qrcode (Kalender-Abo) |
| Auslieferung | gunicorn, whitenoise, Docker |

```text
config/           Einstellungen (nur Umgebungsvariablen), URLs
seite/            Abruf der Schnittstelle, Ansichten, Vorlagen, CSS
tests/            pytest mit nachgebildeter Schnittstelle (tests/fake.py)
deploy/           Ausrollen, Servereinrichtung, HestiaCP-Vorlagen
scripts/test.sh   Testlauf vor dem Ausrollen
docs/             Konzept, Betrieb und Lizenzen
```

## Entwicklung

Alle Einstellungen kommen aus Umgebungsvariablen (Vorlage [.env.example](.env.example),
Beschreibung in `config/settings.py`). Lokal gegen ein HUBIplan auf Port 8000:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
DJANGO_DEBUG=1 HUBIPLAN_API_URL=http://localhost:8000 python manage.py runserver 8001
```

## Tests

Tests laufen nur über `scripts/test.sh`, lokal in WSL mit Docker:

```bash
scripts/test.sh <commit>
```

Das Skript prüft den eingecheckten Stand mit ruff und pytest. Die Tests nutzen eine
nachgebildete Schnittstelle mit erfundenen Daten (`tests/fake.py`), nie den Testserver.

Feste Regeln:

- **Tests laufen nie auf dem Testserver**, auch keine Test-Container.
- **Höchstens zwei Testläufe gleichzeitig, jeder höchstens 8 Kerne**, für alle Projekte auf
  Ralfs PC zusammen. `scripts/test.sh` holt sich dafür einen Platz mit `testplatz` (aus
  `hubiplan/scripts/testplatz.sh`, siehe `docs/testserver.md` in hubiplan).
- Keine echten Vereinsdaten im Repository (Namen, Königslisten, Fotos). Echte Daten
  kommen nur im Echtbetrieb über HUBIplan.
- GitHub Actions läuft nur von Hand (workflow_dispatch), nie automatisch.

## Ausrollen

Nur lokal getestete Stände:

```bash
scripts/test.sh origin/main
deploy/deploy.sh origin/main
```

Auf dem Testserver läuft die Seite als Container `website` im Docker-Netz von HUBIplan
hinter Caddy, im Echtbetrieb hinter nginx von HestiaCP. Einzelheiten, Umgebungsvariablen und
Wartungsschalter: [docs/betrieb.md](docs/betrieb.md).

## Lizenz

Copyright © 2026 Ralf Philipsen (Philipsen EDV)

HUBIplan-Website ist freie Software: Sie dürfen sie unter den Bedingungen der **GNU Affero
General Public License**, wie von der Free Software Foundation veröffentlicht, weitergeben
und/oder ändern, entweder gemäß Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren
Version (`AGPL-3.0-or-later`), wie HUBIplan selbst.

Die Software wird in der Hoffnung verbreitet, dass sie nützlich ist, aber **ohne jede
Gewährleistung**, sogar ohne die implizite Gewährleistung der Marktreife oder der Eignung
für einen bestimmten Zweck. Einzelheiten stehen in der Lizenz. Den vollständigen
Lizenztext (englisch, maßgeblich) enthält die Datei [LICENSE](LICENSE).

Wer eine veränderte Fassung der Webseite öffentlich betreibt, muss ihren Quellcode unter
derselben Lizenz zugänglich machen.
