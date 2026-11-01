#!/usr/bin/env bash
# Sammelt die Texte der Webseite neu in locale/en/LC_MESSAGES/django.po (Vorlagen, Python,
# Skripttexte in seite/templatetags/seite.py JS_TEXTE). Neue Texte danach übersetzen;
# tests/test_sprache.py prüft, dass keiner fehlt. Braucht GNU gettext.
set -euo pipefail
cd "$(dirname "$0")/.."
DJANGO_DEBUG=true DJANGO_SECRET_KEY=nur-zum-sammeln python manage.py makemessages -l en \
    --no-location --no-obsolete -i 'tests/*' -i 'staticfiles/*' -v0
grep -c '^msgid ' locale/en/LC_MESSAGES/django.po | xargs -I{} echo "{} Texte im Katalog"
