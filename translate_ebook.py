from classes.llm_operations import *
from classes.pdf_to_text import *
from classes.save_pdf import *
import sqlite3
import os


class translate_ebook:
    def __init__(self) -> None:
        pass

    def createDatabase(self):

        # tworzy folder configs jeśli nie istnieje
        if not os.path.isdir("configs"):
            os.makedirs("configs", exist_ok=True)
            config_path = os.path.abspath("configs")

        # tworzy bazę danych jeśli nie istnieje
        if not os.path.isfile("translate_book.db"):
            try:
                db = sqlite3.connect("translate_book.db")
                cursor = db.cursor()

                # wykonuje kwerendę tworzącą tabele
                cursor.execute('''
        CREATE TABLE BookInformation(
            id integer,
            bookName varchar,
            page varchar,
            originalPage varchar,
            translatedPage varchar,
            PRIMARY KEY(id)

            );

                ''')

                db.commit()
                # cursor.execute(sql,data)
                db.close()
            except:
                print("Błąd tworzenia bazy danych")

    def split_text_into_chunks(self, text, chunk_size=150):
        words = text.split()
        chunks = [' '.join(words[i:i+chunk_size])
                  for i in range(0, len(words), chunk_size)]
        return chunks

    def start(self):
        self.createDatabase()

        llm = llm_operations()
        pdf = pdf_to_text()

        text = pdf.extract_text_from_pdf("test/django3byexample.pdf")
        translated_text = []
        counter = 0
        for page in text:
            print(f"Translating chunk {counter+1}/{len(text)}")
            translated_page = ""
            chunks = split_text_into_chunks(page)

            for chunk in chunks:

                translated = llm.generate(
                    chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych.")
                translated_page += translated
            translated_text.append(translated_page)
            print(translated_page)
            counter += 1

        sv_pdf = save_pdf()
        sv_pdf.create_pdf(
            "test/django3byexample_translated_2.pdf", translated_text)
