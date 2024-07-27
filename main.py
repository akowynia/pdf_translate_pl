from classes.llm_operations import * 
from classes.pdf_to_text import * 
from classes.save_pdf import *

def split_text_into_chunks(text, chunk_size=150):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

llm = llm_operations()
# test = llm.generate("I love it", "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych.")
# print(test)

pdf = pdf_to_text()
text = pdf.extract_text_from_pdf("test/django3byexample.pdf")
translated_text = []
counter = 0
for page in text:
    print(f"Translating chunk {counter+1}/{len(text)}")
    translated_page= ""
    chunks = split_text_into_chunks(page)
    
    for chunk in chunks:
        
        translated = llm.generate(chunk, "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych.")
        translated_page += translated
    translated_text.append(translated_page)
    print(translated_page)
    counter += 1


sv_pdf = save_pdf()
sv_pdf.create_pdf("test/django3byexample_translated_2.pdf", translated_text)





