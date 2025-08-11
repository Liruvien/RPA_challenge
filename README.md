RPA Challenge

Automatyzacja skryptu do wypełniania formularza danymi z pliku excel, odbywa sie na stronie https://rpachallenge.com

Repozytorium zawiera dwa podejścia do rozwiązania zadania automatyzacji:
- Wersja Python – w pełni działający skrypt automatyzujący proces (folder 'python_version').  
- Wersja UiPath – próba implementacji tego samego procesu w narzędziu UiPath (folder 'uipath_version').  
   Ta wersja nie jest w pełni funkcjonalna, lecz zawiera screenshot workflow oraz diagram procesu jako dokumentację podejścia.

Skrypt:
- otwiera przeglądarkę Google Chrome,
- pobiera lub wczytuje plik z danymi 'challenge.xlsx',
- automatycznie wypełnia formularz na stronie,
- zapisuje wynik końcowy do pliku tekstowego 'wynik.txt'.

Wymagania:

System operacyjny:
  - Linux (testowane na Ubuntu) 
  lub
  - Windows (testowane na Windows 10)
- Google Chrome zainstalowany w systemie
- Python 3.10+ zainstalowany w systemie (na systemie linux)
- Dostęp do internetu podczas działania skryptu do otwarcia rpachallenge.com
- Zainstalowane pakiety z 'requirements.txt'

Uwaga: 
Gotowy plik wykonywalny ('.exe' na Windows lub plik binarny na Linux) nie jest dołączony do repozytorium. Należy go wygenerować lokalnie zgodnie z poniższą instrukcją.

Uruchomienie na Windows (generowanie i uruchomienie pliku .exe)
0. Pobierz repozytorium
1. Przejdź do katalogu ze skryptem
cd C:\ścieżka\do\RPA_challenge\python_version\script
2. Aktywuj środowisko virtualne (opcjonalnie) 
.\venv\Scripts\Activate
3. Zainstaluj wymagane pakiety
pip install -r ..\requirements.txt
4. Wygeneruj plik .exe
pyinstaller --onefile rpachallenge.py

Plik powstanie tutaj:
dist\rpachallenge.exe

5. Uruchom program
.\dist\rpachallenge.exe


Uruchomienie na Linux (generowanie i uruchomienie pliku binarnego):
0. Pobierz repozytorium
1. Przejdź do katalogu ze skryptem
cd ~/RPA_challenge/python_version/script
2. Aktywuj środowisko virtualne (opcjonalnie) 
source ../venv/bin/activate
3. Zainstaluj wymagane pakiety
pip install -r ../requirements.txt
4. Wygeneruj plik binarny
pyinstaller --onefile rpachallenge.py

Plik powstanie tutaj:
dist/rpachallenge

5. Nadaj prawo wykonywania (opcjonalnie):
chmod +x dist/rpachallenge
6. Uruchom program
./dist/rpachallenge

Dodatkowo:
W repozytorium dołączony jest plik rpachallenge.spec służący do zbudowania programu z wcześniej przygotowanymi ustawieniami, można go użyć poleceniem:
pyinstaller rpachallenge.spec