import fitz  # PyMuPDF

class save_pdf:
    def __init__(self) -> None:
        pass
    def create_pdf(self, output_path, pages):
        doc = fitz.open()
        for page_book in pages:
            page = doc.new_page()
            lines = self.split_text_into_lines(page_book, max_line_length=70)
            for i, line in enumerate(lines):
                page.insert_text((72, 20 + i * 14), line, fontsize=12, fontname="FreeSans")
        doc.save(output_path)

    def split_text_into_lines(self, text, max_line_length):
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