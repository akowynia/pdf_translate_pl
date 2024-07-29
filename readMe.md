# PDF Translate PL

Projekt `PDF Translate` umożliwia tłumaczenie tekstu e-booków w formacie PDF przy użyciu modelu Llama-3-8B-Instruct.

Uwaga! Projekt tworzy plik z przetłumaczonym samym tekstem(wszystkie grafiki/niestandardowy układ nie jest przerabiany), wszelkie formatowanie tekstu w porównaniu do oryginalnego pliku może nie zostać zachowane, tak samo stosowanie nazw własnych i charakterystycznych dla danego pisarza i zależne jest od tego czy model Meta LLama zna dzieła danego autora.


## Wymagania

- Python 3.6 lub nowszy
- `requests` (można zainstalować za pomocą `pip install requests`)
- `tqdm` (można zainstalować za pomocą `pip install tqdm`)


## Wykorzystany model
Model wykorzystany w projekcie pochodzi z huggingface dostępnego pod adresem:
```
https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF
```
Dostępny też jest w LM studio.

By zmienić model na inny należy edytować następujące pliki:

``translate_ebook.py`` linię 18 gdzie jest adres do pobrania modelu, linię 27 gdzie jest nazwa modelu.

``classes/llm_operations.py`` linię 17 gdzie jest ścieżka do modelu.

## Instalacja

1. Sklonuj repozytorium:

    ```bash
    git clone https://github.com/akowynia/pdf_translate_pl.git
    cd pdf_translate_pl
    ```

2. Zainstaluj niezbędne biblioteki przy uzyciu:
    ```
    pip install -r requirements.txt
    ```

## Użycie

Po skonfigurowaniu środowiska, możesz uruchomić skrypt `translate_ebook.py`, aby przetłumaczyć e-booka:

będąc w folderze wywołujesz za pomocą polecenia:
```
python3 translate_ebook.py <sciezka pliku>
```
Przy pierwszym uruchomieniu następuje pobranie modelu llama oraz utworzenie bazy danych w folderze configs.
Przetłumaczony plik jest zapisywany w tym samym folderze co pierwotny plik z dodaną nazwą _translated.pdf
W przypadku przerwania tłumaczenia, ponowne uruchomienie z tą samą ścieżką pliku kontynuuje dalsze tłumaczenie.

## Zmiana języka docelowego tłumaczenia.
Domyślnym językiem docelowym jest język polski, jeśli jest potrzeba tłumaczenia na inny język należy zmienić w pliku:
``translate_ebook.py``
następujące linie 88 i 119 :
```
translated = llm.generate(chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych. Dostajesz fragmenty ksiąki, zachowaj pierwotne formatowanie. Tylko tłumacz, nie dodawaj niczego.")
```              

## Wydajność
Zależna jest od sprzętu na którym jest uruchomiona, najlepiej jest sprawdzić ustawienia w LM studio
``https://lmstudio.ai`` i dostosować ustawienia w pliku ``llm_operations.py``
