from classes.llm_operations import *
from classes.pdf_to_text import *
from classes.save_pdf import *
from classes.db_operations import *


class translate_ebook:
    def __init__(self) -> None:
        pass

    def split_text_into_chunks(self, text, chunk_size=100):
        words = text.split()
        chunks = [' '.join(words[i:i+chunk_size])
                  for i in range(0, len(words), chunk_size)]
        return chunks

    def start(self, path):
        db = db_operations()
        llm = llm_operations()
        pdf = pdf_to_text()

        if db.checkData(path) == False:

            text = pdf.extract_text_from_pdf(path)
            translated_text = []
            counter = 0
            for page in text:
                print(f"Translating chunk {counter+1}/{len(text)}")
                translated_page = ""
                chunks = self.split_text_into_chunks(page)
                print('-----------------')
                print(chunks)
                print('-----------------')
                print(len(chunks))
                for chunk in chunks:

                    translated = llm.generate(
                        chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych.")
                    translated_page += translated
                translated_text.append(translated_page)

                db.insertData(path, counter, page, translated_page)

                print(translated_page)
                counter += 1

            sv_pdf = save_pdf()
            sv_pdf.create_pdf(
                path[0:-4]+"_translated.pdf", translated_text)
        else:
            print("Book already exists in database")
            db.last_page(path)
            print("Last page: ", db.last_page(path))
            text = pdf.extract_text_from_pdf(path)
            counter = 0
            last_page = int(db.last_page(path)[0][0])

            for page in text:
                if counter > last_page:
                    print(f"Translating chunk {counter+1}/{len(text)}")
                    translated_page = ""
                    chunks = self.split_text_into_chunks(page)

                    for chunk in chunks:

                        translated = llm.generate(
                            chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych.")
                        translated_page += translated
                    db.insertData(path, counter, page, translated_page)
                    print(translated_page)
                counter += 1
            translated = db.selectData(path)
            text = []
            for t in translated:
                text.append(t[0])
            sv_pdf = save_pdf()
            sv_pdf.create_pdf(path[0:-4]+"_translated.pdf", text)


path = "test/django3byexample_2.pdf"
te = translate_ebook()
te.start(path)
