"""Einzelteile: Markdown, Adressen, Schnittstelle."""

import pytest

from seite import api, markdown
from seite.site import Site, units_slug

from .fake import BASE, KEY, FakeHubiplan


def test_markdown_sicher():
    html = markdown.render(
        "<img src=x onerror=alert(1)> [a](javascript:alert(1)) [b](https://x.example)"
    )
    assert "<img" not in html
    assert 'href="javascript' not in html
    assert 'rel="noopener noreferrer"' in html


def test_markdown_bild():
    assert "/medien/a/images/abcd1234/?size=small" in markdown.render("![x](bild:abcd1234)")


def test_markdown_links_auf_eigene_seiten():
    html = markdown.render(
        "[T](seite:termine) [G](seite:seite/chronik-alt) [Z](seite:einheiten) "
        "[E](seite:einheit/jaegerzug) [X](seite:gibtsnicht) [Y](seite:seite/../x)",
        units_path="zuege",
    )
    assert '<a href="/termine/">T</a>' in html
    assert '<a href="/seite/chronik-alt/">G</a>' in html
    assert '<a href="/zuege/">Z</a>' in html
    assert '<a href="/zuege/jaegerzug/">E</a>' in html
    # unbekannte Ziele: nur der Text, kein Link
    assert " X " in html and "seite:" not in html
    assert html.count("<a ") == 4


def test_markdown_links_unter_unterpfad(settings):
    from django.urls import clear_script_prefix, set_script_prefix

    set_script_prefix("/webseite/")
    try:
        assert '<a href="/webseite/kontakt/">K</a>' in markdown.render("[K](seite:kontakt)")
    finally:
        clear_script_prefix()


def test_lokale_adressen():
    site = Site(key=KEY, info={})
    assert site.local(BASE + "images/abcd/?size=small") == "/medien/a/images/abcd/?size=small"
    assert site.local("https://hubiplan.example/media/logos/a.png") == "/medien/m/logos/a.png"
    assert site.local("http://backend:8000/media/logos/a.png") == "/medien/m/logos/a.png"
    assert site.local("https://anderswo.example/x.png") is None
    assert site.local(None) is None


def test_theme_nur_farben():
    site = Site(key=KEY, info={"theme": {"primary": "red;}body{display:none", "accent": "#00ff00"}})
    assert site.theme["primary"] == "#1f4e2c"
    assert site.theme["accent"] == "#00ff00"


def test_einheiten_pfad():
    assert units_slug({"unit_label_plural": "Züge"}) == "zuege"
    assert units_slug({"unit_label_plural": "Abteilungen"}) == "einheiten"
    assert units_slug({}) == "einheiten"


def test_api_fehler(monkeypatch):
    fake = FakeHubiplan()
    monkeypatch.setattr(api, "_request", lambda *a, **k: api.Response(500, b"", "text/html"))
    with pytest.raises(api.Unavailable):
        api.get(KEY, "board/", cached=False)
    monkeypatch.setattr(api, "_request", fake)
    with pytest.raises(api.NotFound):
        api.get(KEY, "gibtsnicht/", cached=False)


def test_interner_aufruf_setzt_host(monkeypatch, settings):
    seen = {}

    class Antwort:
        status = 200
        headers = {"Content-Type": "application/json"}

        def read(self, n):
            return b"{}"

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def urlopen(req, timeout):
        seen.update(req.headers)
        seen["url"] = req.full_url
        return Antwort()

    monkeypatch.setattr(api.urllib.request, "urlopen", urlopen)
    settings.HUBIPLAN_HOST = "hubiplan.example"
    api._request("GET", "/api/public/site/v1/x/", preview="abc")
    assert seen["url"] == "http://backend:8000/api/public/site/v1/x/"
    assert seen["Host"] == "hubiplan.example"
    assert seen["X-forwarded-proto"] == "https"
    assert seen["X-preview-session"] == "abc"
