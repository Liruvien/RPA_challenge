UiPath Version - RPA Challenge

Ten folder zawiera próbę automatyzacji zadania przy użyciu UiPath.  
Celem było automatyczne wczytanie danych z pliku Excel oraz wpisanie ich dynamicznie do formularzy na stronie http://rpachallenge.com, a następnie zapisanie wyniku do pliku tekstowego.

Co jest w tym folderze:

- Screenshot workflow UiPath ('RPAChallengeUiPath.jpg)  
  Pokazuje układ głównych aktywności w projekcie — od pobrania pliku Excel, przez pętlę wpisywania danych, do zapisu wyniku.

- Diagram procesu ('diagram.md') 
  Tekstowy schemat pokazujący logiczny przepływ aktywności w projekcie (pobranie danych, wpisywanie, submit, zapis).

- README.md 
  Ten plik z wyjaśnieniami i dokumentacją.

Stan projektu, rozwwiazania zadania wersja uipath:
- Obecna wersja workflow w UiPath nie osiąga jeszcze pełnej funkcjonalności.
- W repozytorium znajduje się w pełni działająca wersja w Pythonie (w osobnym folderze).
- Ten folder pełni rolę dokumentacyjną – przedstawia podejście do automatyzacji w UiPath, strukturę procesu oraz próbę implementacji rozwiązania.

Możliwe kierunki usprawnień
- Ustabilizowanie selektorów dynamicznych, aby poprawić trafność wypełniania pól formularza.
- Lepsze dostosowanie mechanizmów oczekiwania i synchronizacji z ładowaniem strony.
- Dopracowanie logiki mapowania pól formularza, szczególnie w pętlach i warunkach.