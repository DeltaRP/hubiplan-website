"""Gesamtaudit 30.10. (I-S01): Der Vorschau-Schlüssel steht in der Adresse und darf nicht
ins Zugriffslog. Gunicorn schreibt deshalb nur den Pfad ohne Abfrage und ohne Referer."""

import json
from pathlib import Path

DOCKERFILE = Path(__file__).resolve().parent.parent / "Dockerfile"


def test_zugriffslog_ohne_abfrage_und_referer():
    line = next(x for x in DOCKERFILE.read_text().splitlines() if x.startswith("CMD "))
    args = json.loads(line[4:])
    fmt = args[args.index("--access-logformat") + 1]
    assert "%(U)s" in fmt
    for leaky in ("%(r)s", "%(q)s", "%(f)s", "{"):
        assert leaky not in fmt
