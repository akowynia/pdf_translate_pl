import fitz  # PyMuPDF

class pdf_to_text:
    def __init__(self) -> None:
        pass

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        
        text = []

        for page in doc:
            page_text = page.get_text()
            # cleaned_text = page_text.replace('\n', ' ')  # Usuwa przełamania linii
            text.append(page_text)
            
        return text