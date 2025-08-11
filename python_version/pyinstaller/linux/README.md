Generowanie binarnego pliku wykonywalnego na systemie Linux przy pomocy PyInstaller

Instrukcja wygenerowania pliku wykonywalnego ze skryptu rpachallenge.py na systemie Linux:
0. Pobierz repozytorium

1. Otwórz terminal i przejdź do katalogu ze skryptem:
cd ~/RPA_challenge/python_version/script/rpachallenge.py

2. Aktywuj środowisko wirtualne, jeśli używasz: (opcjonalnie) 
source ../venv/bin/activate
Uwaga: domyślna lokalizacja środowiska może się różnić.

3. Zainstaluj wymagane pakiety:
pip install -r ../requirements.txt

4. Wygeneruj plik wykonywalny ze skryptu:
pyinstaller --onefile rpachallenge.py

5. Po zakończeniu procesu plik wykonywalny będzie w folderze dist:
dist/rpachallenge

6. Uruchom automatyzację:
./dist/rpachallenge

Upewnij się, że masz prawa wykonywania tego pliku, jeśli potrzeba nadaj:
chmod +x dist/rpachallenge

Dodatkowo:
W repozytorium dołączony jest plik rpachallenge.spec służący do zbudowania programu z wcześniej przygotowanymi ustawieniami, można go użyć poleceniem:
pyinstaller rpachallenge.spec