import os
import re
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #pylint: disable=invalid-name
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


CHALLENGE_URL = "https://rpachallenge.com"
NAZWA_PLIKU_DO_POBRANIA = "challenge.xlsx"
CZAS_OCZEKIWANIA_NA_PLIK = 30
CZAS_OCZEKIWANIA_NA_ELEMENT = 30


def czyscik_tekstu(tekst):
    """
    Usuwa wszystkie znaki inne niż litery, cyfry, polskie znaki, usuwa spacje z początku i końca, konwertuje cały tekst na małe litery.
    """
    if not tekst:
        return ""
    tekst = str(tekst)
    oczyszczony_tekst = re.sub(r'[^0-9a-zA-ZąęćłńóśżźĄĘĆŁŃÓŚŻŹ]', '', tekst) #usunięcie wszystkich niedozwolonych  znaków z zachowaniem polskich liter
    return oczyszczony_tekst.strip().lower() #usunięcie spacji i zmiana na małe litery


def znajdz_katalog_pobrane():
    """
    Próbuje znaleźć katalog 'Pobrane' lub 'Downloads' w katalogu domowym użytkownika.Jeśli nie istnieje, zwraca ścieżkę katalogu domowego.
    """
    katalog_domowy = Path.home() #pobranie ścieżki katalogu domowego użytkownika
    for nazwa_folderu in ["Downloads", "Pobrane"]: #przeszukanie folderów tam gdzie ma sie pobrac plik
        pobrane = katalog_domowy / nazwa_folderu
        if pobrane.exists() and pobrane.is_dir(): # sprawdzenie istnienia i typu ścieżki
            return str(pobrane)
    return str(katalog_domowy)  #jeśli nie znajdzie folderu pobrań zapisuje w katalogu home


def uruchom_przegladarke(sciezka_pobrane):
    """
    Uruchamia instancję przeglądarki Google Chrome z ustawieniami pozwalającymi na automatyczne pobieranie plików do podanej ścieżki bez pytania.
    """
    opcje = Options() #tworzy obiekt ustawien opcji dla chrome

    ustalenia = {  #ustawienia pobierania plików
        "download.default_directory": sciezka_pobrane,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    opcje.add_experimental_option("prefs", ustalenia) #dodanie usalen do opcji
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcje) #uruchomienie przeglądarki Chrome z konfiguracją i sterownikiem


def oczekiwanie_na_plik(sciezka_katalogu, nazwa_pliku, czas_oczekiwania=CZAS_OCZEKIWANIA_NA_PLIK):
    """
    Oczekuje, aż w podanym katalogu pojawi się plik o określonej nazwie.
    """
    pelna_sciezka = os.path.join(sciezka_katalogu, nazwa_pliku) #utworzenie pełnej ścieżki do pliku
    czas = 0 #inicjalizacja licznika czasu

    while czas < czas_oczekiwania: #pętla bedzie sie wykonywac az znajdzie plik
        if os.path.exists(pelna_sciezka) and not pelna_sciezka.endswith(".crdownload"):
            time.sleep(1) #chwila na zapis pliku
            return pelna_sciezka
        time.sleep(1)
        czas += 1
    raise TimeoutError(f"Plik {nazwa_pliku} nie został znaleziony w {sciezka_katalogu}") #wyrzuca wyjątek, jeśli limit czasu został przekroczony


MOZLIWE_POLA = {
    'firstname': ['first name', 'firstname', 'first', 'given name', 'imie', 'name'],
    'lastname': ['last name', 'lastname', 'surname', 'family name', 'nazwisko'],
    'companyname': ['company', 'company name', 'companyname', 'organization', 'employer'],
    'roleincompany': ['role', 'role in company', 'position', 'job', 'title'],
    'address': ['address', 'street', 'adres', 'address1'],
    'email': ['email', 'e-mail', 'emailaddress', 'mail'],
    'phonenumber': ['phone', 'phone number', 'phonenumber', 'telephone', 'mobile', 'phone no']
} #mozliwosci nazw pól do nazw kolumn


def dopasuj_pole_do_kolumny(etykieta_pola, kolumny):
    """
    Dopasowuje etykietę pola z formularza do kolumny w DataFrame na podstawie mapy MOZLIWE_POLA lub częściowego dopasowania tekstu.
    """
    if not etykieta_pola:  #zwraca None jesli nie ma etykiety
        return None
    zmiejszony_tekst = etykieta_pola.strip().lower()
    oczyszczony_tekst = czyscik_tekstu(zmiejszony_tekst)
    if oczyszczony_tekst in kolumny: #sprawdzenie dopasowania
        return oczyszczony_tekst

    for kolumna, warianty in MOZLIWE_POLA.items(): #sprawdzenie dopasowania z mozliwych pol
        for wzorzec in warianty:
            if wzorzec in zmiejszony_tekst or czyscik_tekstu(wzorzec) == oczyszczony_tekst:
                if kolumna in kolumny:
                    return kolumna

    for kolumna in kolumny: #sprawdzenie częściowego dopasowania
        if oczyszczony_tekst in kolumna or kolumna in oczyszczony_tekst:
            return kolumna
    return None #jak nie dopasuje to nic nie wpisuje


def znajdz_etykiete_pola(przegladarka, pole):
    """
    Identyfikuje opis pola formularza korzystając z kilku strategii:
    1. <label for="id">
    2. Tekst w rodzicu/przodkach elementu
    3. Element poprzedzający
    4. Placeholder
    5. Wybrane atrybuty pola
    Args:
        przegladarka (webdriver.Chrome): Obiekt przeglądarki Selenium.
        pole (WebElement): Pole formularza (input/textarea).
    Returns:
        tuple: (klucz_oczyszczony, etykieta_surowa) lub ('','') jeśli brak dopasowania.
    """
    #wyszukiwanie przez <label for="id">
    try:
        id_pola = pole.get_attribute("id") #pobranie atrybutu id  elementu
        if id_pola:
            etykiety = przegladarka.find_elements(By.XPATH, f"//label[@for='{id_pola}']")
            if etykiety:
                tekst_etykiety = etykiety[0].text.strip()
                if tekst_etykiety:
                    return czyscik_tekstu(tekst_etykiety), tekst_etykiety
    except Exception as e:
        print(f"[Debug] label for: {e}")

    try:  #szukanie w elementach nadrzędnych
        pole_nadrzedne = pole
        for _ in range(6): #sprawdzenie 6 poziomów wyzej
            pole_nadrzedne = pole_nadrzedne.find_element(By.XPATH, "./..") #sprawdzenie w polu nadrzednym
            if not pole_nadrzedne:
                break
            etykiety = pole_nadrzedne.find_elements(By.TAG_NAME, "label")
            if etykiety:
                tekst = etykiety[0].text.strip()
                if tekst:
                    return czyscik_tekstu(tekst), tekst

            for element_podrzedny in pole_nadrzedne.find_elements(By.XPATH, "./*"): #sprawdzenie w polu  podrzednym
                tekst = element_podrzedny.text.strip()
                if tekst:
                    return czyscik_tekstu(tekst), tekst
    except Exception as e:
        print(f"[DBG] pole_nadrzedne: {e}")

    #sprawdzenie poprzedniego elementu
    try:
        poprzednik = pole.find_element(By.XPATH, "preceding-sibling::*[1]")
        tekst = poprzednik.text.strip()
        if tekst:
            return czyscik_tekstu(tekst), tekst
    except Exception as e:
        print(f"[DBG] poprzednik: {e}")


    try:    #pobranie tekstu z placeholdera
        placeholder = pole.get_attribute("placeholder")
        if placeholder and placeholder.strip():
            return czyscik_tekstu(placeholder.strip()), placeholder.strip()
    except Exception as e:
        print(f"[DBG] placeholder: {e}")

    for atrybut in ("aria-label", "name", "id", "type"):    #sprawdzenie wybranych atrybutów
        try:
            wartosc = pole.get_attribute(atrybut)
            if wartosc and str(wartosc).strip():
                tekst = str(wartosc).strip()
                return czyscik_tekstu(tekst), tekst
        except Exception as e:
            print(f"[DBG] atrybut {atrybut}: {e}")

    return "", "" # jak brak dopasowan to nic nie wpisuje


def wypelnij_formularz_z_wiersza(przegladarka, kolumny, wiersz_danych):
    """
    Wypełnia wartości w formularzu na podstawie jednego wiersza danych.
    Args:
        przegladarka:Przeglądarka Selenium
        kolumny: Lista kolumn DataFrame
        wiersz_danych: Wiersz danych z  excela
    Returns:
        tuple: (pola_uzupelnione, liczba_wszystkich_pol)
    """
    pola_formularza = przegladarka.find_elements(  #wyszukiwanie wszystkich widocznych pól formularza
        By.XPATH,
        "//input[not(@type='hidden') and not(@type='submit') and not(@type='button')] | //textarea"
    )
    pola_uzupelnione = 0 #licznik uzupełnionych pól

    for pole in pola_formularza:
        try:
            klucz, etykieta = znajdz_etykiete_pola(przegladarka, pole) #znalezienie etykiety pola
            nazwa_kolumny = dopasuj_pole_do_kolumny(etykieta, kolumny) #dopasowanie kolumny z danymi

            if not nazwa_kolumny and klucz in kolumny: #próba dopasowania po kluczu, jak nie moze dopasowac po etykiecie
                nazwa_kolumny = klucz
            elif not nazwa_kolumny and klucz:
                for nazwa in kolumny:
                    if klucz in nazwa or nazwa in klucz:
                        nazwa_kolumny = nazwa
                        break

            if nazwa_kolumny: #wpisanie wartości do pola
                wartosc = "" if pd.isna(wiersz_danych[nazwa_kolumny]) else str(wiersz_danych[nazwa_kolumny])
                pola_uzupelnione += 1
                print(f"[OK] {etykieta} → {wartosc}")
            else:
                print(f"[KO] {etykieta}")
                wartosc = ""

            try: #przewinięcie do pola, kliknięcie, wyczyszczenie i wpisanie wartości, jeśli sie  da
                pole.click()
                pole.clear()
                if wartosc:
                    pole.send_keys(wartosc)
                pole.send_keys(Keys.TAB) #przejście do kolejnego pola formularza
            except Exception as e:
                print(f"[Debug] wypełnianie: {e}")

            time.sleep(0.2)

        except Exception as e:
            print("Błąd przy polu:", e)
            continue

    return pola_uzupelnione, len(pola_formularza) #zwrócenie liczby prawidłowo uzupełnionych i wszystkich pól


def automatyzacja():
    '''
    główna funkcja zadania:
    -otwiera stronę
    -pobiera plik
    -wypełnia formularz danymi z excela
    -zapisuje wynik do pliku txt
    '''
    katalog_pobrane = znajdz_katalog_pobrane() # ustalenie katalogu do pobrania pliku
    przegladarka = uruchom_przegladarke(katalog_pobrane) #uruchomienie przeglądarki
    oczekiwanie = WebDriverWait(przegladarka, CZAS_OCZEKIWANIA_NA_ELEMENT) #oczekiwania na elementy na stronie

    try:
        przegladarka.get(CHALLENGE_URL) #otworzenie strony
        time.sleep(1) #oczekiwanie na pełne załadowanie strony

        przycisk_pobierz = oczekiwanie.until( #odszukanie i kliknięcie przycisku pobierania
            EC.element_to_be_clickable((By.XPATH,
                "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'download')]"))
        )
        przycisk_pobierz.click()

        sciezka_plik = oczekiwanie_na_plik( #oczekiwanie aż plik .xlsx pojawi się w folderze gdzie ma sie pobrac
            katalog_pobrane, NAZWA_PLIKU_DO_POBRANIA, czas_oczekiwania=CZAS_OCZEKIWANIA_NA_PLIK
        )
        print("Pobrano plik:", sciezka_plik)

        przycisk_start = oczekiwanie.until( #odszukanie i kliknięcie przycisku start
            EC.element_to_be_clickable((By.XPATH,
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'start')]"))
        )
        przycisk_start.click()
        time.sleep(1) #dodatkowy czas na pełne zaladowanie formularza

        dane_z_excela = pd.read_excel(sciezka_plik) #wczytanie pliku excel do dataframe oraz unifikacja nazw kolumn
        kolumny = [czyscik_tekstu(kolumna) for kolumna in dane_z_excela.columns]
        dane_z_excela.columns = kolumny
        print("Kolumny po czyszczeniu:", kolumny)

        liczba_wszystkich_pol = 0 # licznik wszystkich pól formularza
        liczba_uzupelnionych_pol = 0 #licznik prawidlowo uzupelnionych pól formularza

        for _, wiersz in dane_z_excela.iterrows(): #przetworzenie kolejnych wierszy danych jako kolejnych formularzy
            uzupelniono, wszystkie = wypelnij_formularz_z_wiersza(przegladarka, kolumny, wiersz)
            liczba_wszystkich_pol += wszystkie
            liczba_uzupelnionych_pol += uzupelniono

            try: #odszukanie i kliknięcie przycisku submit
                przycisk_submit = oczekiwanie.until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//input[@type='submit'] | //button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'submit')]"))
                )
                przycisk_submit.click()
            except Exception as e:
                print("Nie można kliknąć submit:", e)

            time.sleep(0.5) #opóźnienie po wysłaniu formularza

        try: #odczytanie komunikatu końcowego z wynikiem i wyjatkiem jak nie znajdzie wyniku
            wynik = przegladarka.find_element(By.CLASS_NAME, "message2").text
        except NoSuchElementException:
            try:
                wynik = przegladarka.find_element(By.CSS_SELECTOR, ".message, .message2").text
            except NoSuchElementException:
                wynik = 'Brak wyniku.'

        with open("wynik.txt", "w", encoding="utf-8") as f: # zapis wyniku do pliku txt
            f.write(wynik)

        print(f"Wynik: {wynik}")
        print(f"Pola wpisane prawidłowo: {liczba_uzupelnionych_pol} / {liczba_wszystkich_pol}")

    finally:
        przegladarka.quit() #zamknięcie przeglądarki i zwolnienie zasobów


if __name__ == "__main__":  #kod jako skrypt
    automatyzacja()
