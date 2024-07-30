from classes.llm_operations import *
from classes.pdf_to_text import *
from classes.save_pdf import *
from classes.db_operations import *
import sys
import requests
from tqdm import tqdm

class translate_ebook:
    def __init__(self) -> None:
        # download model from huggingface

        if not os.path.isdir("models"):
            os.makedirs("models", exist_ok=True)
            print("Created models folder")
        #check and download model llama instruct 3 8b 
        if not os.path.isfile("models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"):
            url = 'https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf?download=true'

            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Sprawdza, czy żądanie zakończyło się sukcesem

                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kilobajt

                with open('models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf', 'wb') as file, tqdm(
                    desc='Pobieranie modelu Llama-3-8B-Instruct',
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for data in response.iter_content(block_size):
                        bar.update(len(data))
                        file.write(data)

                print("Downloading sucessfully.")
            except requests.exceptions.RequestException as e:
                print(f"Error with downloaded model: {e}")
        pass



    
    def split_text_into_chunks(self, text, chunk_size=2000):
        """
        Splits the given text into chunks of specified size.

        Args:
            text (str): The text to be split into chunks.
            chunk_size (int, optional): The size of each chunk. Defaults to 100.

        Returns:
            list: A list of text chunks.
        """
        words = text.split()
        chunks = [' '.join(words[i:i+chunk_size])
                  for i in range(0, len(words), chunk_size)]
        return chunks


    #start translation
    def start(self, path):
        """
        Starts the translation process for the given ebook.

        Args:
            path (str): The path of the ebook file.
        """
        db = db_operations()
        llm = llm_operations()
        pdf = pdf_to_text()

        # If the ebook is not already in the database
        if db.checkData(path) == False:
            text = pdf.extract_text_from_pdf(path)
            translated_text = []
            counter = 0
            for page in text:

                print(f"Translating page {counter+1}/{len(text)}")
                translated_page = ""
                chunks = self.split_text_into_chunks(page)

                for chunk in chunks:
                    # Translate each chunk using the llm_operations class
                    translated = llm.generate(
                        chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych. Dostajesz fragmenty ksiąki, zachowaj pierwotne formatowanie. Tylko tłumacz, nie dodawaj niczego.")
                    translated_page += translated
                translated_text.append(translated_page)

                # Insert the original and translated text into the database
                db.insertData(path, counter, page, translated_page)

                print(translated_page)
                counter += 1

            sv_pdf = save_pdf()
            # Create a translated PDF file using the save_pdf class
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
                        # Translate each chunk using the llm_operations class
                        translated = llm.generate(
                            chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych. Dostajesz fragmenty ksiąki, zachowaj pierwotne formatowanie. Tylko tłumacz, nie dodawaj niczego.")
                        translated_page += translated
                    db.insertData(path, counter, page, translated_page)
                    print(translated_page)
                counter += 1
            translated = db.selectData(path)
            text = []
            for t in translated:
                text.append(t[0])
            sv_pdf = save_pdf()
            # Create a translated PDF file using the save_pdf class
            sv_pdf.create_pdf(path[0:-4]+"_translated.pdf", text)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 translate_ebook.py <path pdf>")
        sys.exit(1)
    else:
        folder = sys.argv[1]
        te = translate_ebook()
        te.start(folder)
