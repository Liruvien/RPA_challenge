import tempfile
import time
import types
import pytest
import pandas as pd
from pathlib import Path
from python_version.script.rpachallenge import (
    czyscik_tekstu,
    znajdz_katalog_pobrane,
    oczekiwanie_na_plik,
    dopasuj_pole_do_kolumny,
    wypelnij_formularz_z_wiersza,
)


def test_czyscik_tekstu():
    assert czyscik_tekstu("  Zażółć Gęślą Jaźń!  ") == "zażółćgęśląjaźń"
    assert czyscik_tekstu("Hello 123 !!!") == "hello123"
    assert czyscik_tekstu("") == ""
    assert czyscik_tekstu(None) == ""
    assert czyscik_tekstu(123) == "123"


def test_znajdz_katalog_pobrane(monkeypatch):
    fake_home = tempfile.TemporaryDirectory()
    pobrane_dir = Path(fake_home.name) / "Downloads"
    pobrane_dir.mkdir()
    monkeypatch.setattr(Path, "home", lambda: Path(fake_home.name))
    assert znajdz_katalog_pobrane() == str(pobrane_dir)


def test_znajdz_katalog_pobrane_brak(monkeypatch):
    fake_home = tempfile.TemporaryDirectory()
    monkeypatch.setattr(Path, "home", lambda: Path(fake_home.name))
    assert znajdz_katalog_pobrane() == fake_home.name


def test_oczekiwanie_na_plik_success(tmp_path):
    plik = tmp_path / "plik.xlsx"

    def create_file_later():
        time.sleep(0.5)
        plik.write_text("data")

    import threading
    threading.Thread(target=create_file_later).start()
    assert oczekiwanie_na_plik(str(tmp_path), "plik.xlsx", czas_oczekiwania=2) == str(plik)


def test_oczekiwanie_na_plik_timeout(tmp_path):
    with pytest.raises(TimeoutError):
        oczekiwanie_na_plik(str(tmp_path), "nie_ma.xlsx", czas_oczekiwania=1)


@pytest.mark.parametrize("etykieta,kolumny,expected", [
    ("First Name", ["firstname", "lastname"], "firstname"),
    ("Nazwisko", ["firstname", "lastname"], "lastname"),
    ("Custom Field", ["customfield"], "customfield"),
    ("Nieistniejące", ["col1"], None),
])
def test_dopasuj_pole_do_kolumny(etykieta, kolumny, expected):
    assert dopasuj_pole_do_kolumny(etykieta, kolumny) == expected


def test_wypelnij_formularz_z_wiersza_minimalnie(monkeypatch):
    class MockPole:
        def __init__(self, label):
            self.label = label
        def click(self): pass
        def clear(self): pass
        def send_keys(self, x): pass

    fields = [MockPole("First Name"), MockPole("Last Name")]

    def fake_znajdz_etykiete_pola(_, pole):
        return pole.label.lower().replace(" ", ""), pole.label

    monkeypatch.setattr("python_version.script.rpachallenge.znajdz_etykiete_pola", fake_znajdz_etykiete_pola)

    przegladarka = types.SimpleNamespace(find_elements=lambda *a, **k: fields)
    kolumny = ["firstname", "lastname"]
    row = pd.DataFrame([{"firstname": "Jan", "lastname": "Kowalski"}]).iloc[0]

    uzupelnione, wszystkie = wypelnij_formularz_z_wiersza(przegladarka, kolumny, row)
    assert uzupelnione == 2
    assert wszystkie == 2
