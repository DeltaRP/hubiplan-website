"""Wettbewerbsergebnisse auf der Webseite (Wettbewerbe Schritt 5; alles erfunden).

Ralf 2026-11-01: eigener Baustein „Ergebnisse“ und Block auf der Startseite; live fragt der
Browser alle 15 Sekunden nach dem Stand und lädt die Rangliste nur bei Änderung neu."""

from .fake import BASE, COMP, LIVE, SERIES


def text(response) -> str:
    return response.content.decode()


def mit_ergebnissen(hubiplan, home=None):
    hubiplan.info["results_url"] = BASE + "results/"
    hubiplan.info["nav"] = [{"key": "results", "label": "Ergebnisse", "children": []}]
    if home is not None:
        hubiplan.info["home"] = home


def test_ohne_modul_keine_seite(client, hubiplan):
    assert client.get("/ergebnisse/").status_code == 404
    assert client.get(f"/ergebnisse/{COMP}/").status_code == 404
    assert not any("results/" in c[1] for c in hubiplan.calls)


def test_uebersicht_und_menue(client, hubiplan):
    mit_ergebnissen(hubiplan)
    r = client.get("/ergebnisse/")
    html = text(r)
    assert r.status_code == 200
    assert 'href="/ergebnisse/" aria-current="page"' in html
    assert "Gerade im Gange" in html and "Pokalschießen" in html
    assert f'href="/ergebnisse/{COMP}/"' in html
    assert "<h2>2027</h2>" in html
    assert f'href="/ergebnisse/reihe/{SERIES}/"' in html
    assert "Zugpokal" in html and "Zug 1" in html


def test_rangliste_endgueltig(client, hubiplan):
    mit_ergebnissen(hubiplan)
    html = text(client.get(f"/ergebnisse/{COMP}/"))
    assert "Max M." in html and "ohne Namen" in html and "(Nachbarverein)" in html
    assert "Vereinsmeister 2027" in html
    # Endgültig: kein Nachfragen
    assert "ergebnisse.js" not in html and "data-stand" not in html
    # Rangliste zu genau diesem Stand abgerufen
    assert any(f"results/{COMP}/?stand=v1" in c[1] for c in hubiplan.calls)


def test_live_stand_und_neue_tabelle(client, hubiplan):
    mit_ergebnissen(hubiplan)
    r = client.get(f"/ergebnisse/{LIVE}/")
    html = text(r)
    assert 'data-sekunden="15"' in html and 'data-version="v1"' in html
    assert f'data-stand="/ergebnisse/{LIVE}/stand/"' in html
    assert "ergebnisse.js" in html and ">Aktualisieren</a>" in html
    assert r["Cache-Control"] == "no-cache"
    stand = client.get(f"/ergebnisse/{LIVE}/stand/")
    assert stand.json() == {"version": "v1", "final": False}
    # Neues Ergebnis in HUBIplan → neuer Stand; die Tabelle kommt sofort neu (nicht aus
    # dem Zwischenspeicher), der Stand selbst höchstens wenige Sekunden alt
    from django.core.cache import cache

    hubiplan.versions[LIVE] = "v2"
    cache.clear()
    teil = client.get(f"/ergebnisse/{LIVE}/tabelle/")
    assert teil.status_code == 200 and "<html" not in text(teil) and "Max M." in text(teil)
    assert any(f"results/{LIVE}/?stand=v2" in c[1] for c in hubiplan.calls)


def test_reihe(client, hubiplan):
    mit_ergebnissen(hubiplan)
    html = text(client.get(f"/ergebnisse/reihe/{SERIES}/"))
    assert "Vereinsmeisterschaft" in html and "Karl F." in html
    assert f'<a href="/ergebnisse/{COMP}/">2027</a>' in html
    assert client.get(f"/ergebnisse/reihe/{'0' * 20}/").status_code == 404


def test_startseite_block(client, hubiplan):
    mit_ergebnissen(hubiplan, home=["greeting", "results"])
    html = text(client.get("/"))
    assert "Aktuelle Ergebnisse" in html and "1. Max M." in html
    assert 'href="/ergebnisse/">Alle Ergebnisse' in html
    # Ohne Block auf der Startseite: kein Abruf
    hubiplan.info["home"] = ["greeting"]
    from django.core.cache import cache

    cache.clear()
    hubiplan.calls.clear()
    assert "Aktuelle Ergebnisse" not in text(client.get("/"))
    assert not any("results/" in c[1] for c in hubiplan.calls)
