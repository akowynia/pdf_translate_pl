# PDF Translate PL

Projekt `PDF Translate` umożliwia tłumaczenie tekstu e-booków w formacie PDF przy użyciu modeli LLM uruchomionych w serwisie **Ollama** (domyślnie `llama3`).

> [!WARNING]
> **Ostrzeżenie dotyczące tłumaczenia i ograniczeń modeli:**
> - **Układ i formatowanie:** Precyzyjne zachowanie struktury i formatowania dokumentu PDF jest trudnym zadaniem. Projekt przetwarza i tłumaczy sam tekst – grafiki, niestandardowy układ oraz zaawansowane formatowanie z oryginalnego pliku PDF nie są odtwarzane.
> - **Dokładność i spójność:** Tłumaczenie generowane przez modele LLM może nie być w pełni dokładne. Ze względu na ograniczenia modeli (np. brak pełnego kontekstu całej książki, limity pamięci/okna kontekstowego):
>   - Model może nie znać oficjalnych polskich tłumaczeń specyficznych terminów, nazw własnych, nazwisk czy imion postaci z danej książki.
>   - Przekład nazewnictwa oraz stylu autora może być niespójny pomiędzy poszczególnymi fragmentami tekstu.


## Wymagania

- Python 3.13 lub nowszy
- Uruchomiona aplikacja/serwer **Ollama** (do pobrania z [ollama.com](https://ollama.com))
- Pobrany model w Ollama (np. `ollama pull llama3`)

## Wykorzystanie modeli Ollama

Domyślnym modelem używanym przez aplikację jest `llama3`. Możesz pobrać go wykonując w terminalu polecenie:
```bash
ollama pull llama3
```

Możesz także użyć dowolnego innego modelu dostępnego w Ollama (np. `mistral`, `gemma2`, `llama3:8b`, `qwen2.5`):
```bash
ollama pull mistral
```

## Instalacja

1. Sklonuj repozytorium:
    ```bash
    git clone https://github.com/akowynia/pdf_translate_pl.git
    cd pdf_translate_pl
    ```

2. Zainstaluj niezbędne biblioteki Python:
    ```bash
    pip install -r requirements.txt
    ```

## Użycie

Po upewnieniu się, że usługa Ollama działa w tle, możesz uruchomić skrypt `translate_ebook.py`:

```bash
python3 translate_ebook.py <sciezka_do_pdf> [nazwa_modelu]
```

Przykłady:
- Użycie domyślnego modelu `llama3`:
    ```bash
    python3 translate_ebook.py ksiazka.pdf
    ```
- Użycie innego modelu, np. `mistral`:
    ```bash
    python3 translate_ebook.py ksiazka.pdf mistral
    ```

Przetłumaczony plik zostanie zapisany w tym samym folderze z dopiskiem `_translated.pdf`.
W przypadku przerwania tłumaczenia, ponowne uruchomienie z tą samą ścieżką pliku kontynuuje tłumaczenie od ostatnio przetłumaczonej strony.

## Zmiana języka docelowego tłumaczenia

Domyślnym językiem docelowym jest język polski. Jeśli chcesz zmienić język docelowy, zmień instrukcję (prompt) w pliku `translate_ebook.py` w wywołaniach `llm.generate(...)`.
