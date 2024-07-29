import fitz  # PyMuPDF
import pymupdf_fonts
import pymupdf_fonts

# This is the implementation of the save_pdf class.
# It provides methods for creating and saving a PDF document.

import fitz  # PyMuPDF

class save_pdf:
    def __init__(self) -> None:
        pass

    def create_pdf(self, output_path, pages):
        """
        Creates a PDF document with the given pages and saves it to the specified output path.

        Args:
            output_path (str): The path where the PDF document will be saved.
            pages (list): A list of strings representing the content of each page.
        """
        doc = fitz.open()

        font = fitz.Font("figo")  # "figo" is the code for FiraGO Regular from pymupdf_fonts

        for page_book in pages:
            page = doc.new_page()
            lines = self.split_text_into_lines(page_book, max_line_length=70)
            fontname = page.insert_font(fontname="F0", fontbuffer=font.buffer)
            for i, line in enumerate(lines):
                page.insert_text((72, 20 + i * 14), line, fontsize=12, fontname="F0")
        doc.save(output_path)

    def split_text_into_lines(self, text, max_line_length):
        """
        Splits the given text into lines based on the maximum line length.

        Args:
            text (str): The text to be split into lines.
            max_line_length (int): The maximum length of each line.

        Returns:
            list: A list of strings representing each line of the text.
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) <= max_line_length:
                current_line.append(word)
                current_length += len(word) + 1  # +1 for the space
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        lines.append(' '.join(current_line))  # Add the last line

        return lines