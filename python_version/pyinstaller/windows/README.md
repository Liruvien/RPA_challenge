Generowanie pliku wykonywalnego .exe zgodnego z systemem Windows przy pomocy PyInstaller

Instrukcja wygenrowania pliku wykonywalnego .exe ze skryptu rpachallenge.py
0. Pobierz repozytorium

1. Przejdź do głównego folderu projektu w terminalu (np. PowerShell):
cd RPA_challenge/python_version/script/rpachallenge.py

2.Aktywuj środowisko virtualne, jeśli używasz: (opcjonalnie)
.\venv\Scripts\Activate

3. Zainstaluj wymagane pakiety:
pip install -r ../requirements.txt

4. Wygeneruj plik .exe:
pyinstaller --onefile rpachallenge.py

5. Po zakończeniu procesu plik znajdziesz w folderze 'dist':
script/dist/rpachallenge.exe

6. Uruchom automatyzacje:
.\dist\rpachallenge.exe

Dodatkowo:
W repozytorium dołączony jest plik rpachallenge.spec służący do zbudowania programu z wcześniej przygotowanymi ustawieniami, można go użyć poleceniem:
pyinstaller rpachallenge.spec