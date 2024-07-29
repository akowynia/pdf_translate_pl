import fitz  # PyMuPDF

class pdf_to_text:
    def __init__(self) -> None:
        pass

    def extract_text_from_pdf(self, pdf_path):
        """
        Extracts text from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            list: A list of strings, where each string represents the text from a page in the PDF.
        """
        doc = fitz.open(pdf_path)
        
        text = []

        for page in doc:
            page_text = page.get_text()
            # cleaned_text = page_text.replace('\n', ' ')  # Removes line breaks
            text.append(page_text)
            
        return text