RPA Challenge

Automatyczny skrypt do wypełniania formularzy z danymi z pliku Excel na stronie rpachallenge.com.

Wymagania:
System: Linux (testowane na Ubuntu)
Google Chrome musi być zainstalowany!
Plik wykonywalny znajduje się w katalogu 'dist/'

*wersja na windows w toku*

Jak uruchomić:
1. Otwórz terminal.
2. Przejdź do katalogu projektu, np.:
cd ~/RPA_challenge

3. Przejdź do katalogu z plikiem:
cd python_version/script/dist

4. Uruchom program:
./rpachallenge

Jeśli pojawi się komunikat o braku uprawnień: 'chmod +x rpachallenge' aby nadać prawa uruchomienia.

5. Skrypt pobierze dane z rpachallenge.com, uzupełni formularze i zapisze wynik w pliku 'wynik.txt'.

Informacje dodatkowe:

W przypadku problemów z przeglądarką Chrome – upewnij się, że jest zainstalowana najnowsza wersja Google Chrome.
Jeśli pojawią się błędy, sprawdź wymagania i komunikaty w terminalu.
Aplikacja była budowana za pomocą PyInstaller.

Uruchamianie aplikacji:
Zainstaluj systemowe wymagania (np. Chrome, Python 3.12).

Utwórz i aktywuj środowisko virtualne:
python3 -m venv venv
source venv/bin/activate

Zainstaluj zależności:
pip install -r requirements.txt

Uruchom PyInstaller:
pyinstaller --onefile --name rpachallenge rpachallenge.py
