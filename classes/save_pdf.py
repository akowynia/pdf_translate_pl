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
        try:
            import pymupdf_fonts
            font = fitz.Font("figo")
        except Exception:
            font = fitz.Font("helv")

        for page_book in pages:
            page = doc.new_page()
            lines = self.split_text_into_lines(page_book, max_line_length=70)
            fontname = page.insert_font(fontname="F0", fontbuffer=font.buffer)
            for i, line in enumerate(lines):
                page.insert_text((72, 20 + i * 14), line, fontsize=12, fontname="F0")
        doc.save(output_path)
        doc.close()

    def create_pdf_layout_preserved(self, original_pdf_path, output_path, translated_pages_blocks):
        """
        Creates a new PDF document by overlaying translated text blocks on top of
        the original PDF layout without modifying the source PDF file.

        Args:
            original_pdf_path (str): Path to the source PDF file.
            output_path (str): Destination path for the translated PDF.
            translated_pages_blocks (list): List of pages, where each page is a list of block dicts:
                [{'bbox': [x0, y0, x1, y1], 'translated_text': str}]
        """
        doc = fitz.open(original_pdf_path)

        try:
            import pymupdf_fonts
            font = fitz.Font("figo")
        except Exception:
            font = fitz.Font("helv")

        for page_idx, page in enumerate(doc):
            if page_idx >= len(translated_pages_blocks):
                break

            blocks = translated_pages_blocks[page_idx]

            # Step 1: Add redaction annotations for old text blocks with 0.5pt padding
            for block in blocks:
                bbox = block.get('bbox')
                if not bbox:
                    continue
                rect = fitz.Rect(bbox[0] - 0.5, bbox[1] - 0.5, bbox[2] + 0.5, bbox[3] + 0.5)
                page.add_redact_annot(rect, fill=(1, 1, 1))

            # Apply redactions to clear original text area
            page.apply_redactions()

            page.insert_font(fontname="F0", fontbuffer=font.buffer)
            font_alias = "F0"

            # Step 2: Insert translated text into bounding boxes with font auto-fit
            for block in blocks:
                bbox = block.get('bbox')
                translated_text = block.get('translated_text', '').strip()
                if not bbox or not translated_text:
                    continue

                rect = fitz.Rect(bbox[0], bbox[1], bbox[2], bbox[3])

                block_h = abs(bbox[3] - bbox[1])
                orig_text = block.get('original_text', '').strip()
                line_cnt = max(1, len(orig_text.splitlines())) if orig_text else 1
                est_size = (block_h / line_cnt) * 0.85

                fontsize = min(12.0, max(6.0, est_size))
                min_fontsize = 5.0
                rc = -1

                while fontsize >= min_fontsize:
                    rc = page.insert_textbox(
                        rect,
                        translated_text,
                        fontsize=fontsize,
                        fontname=font_alias,
                        align=0
                    )
                    if rc >= 0:
                        break
                    fontsize -= 0.5

                if rc < 0:
                    page.insert_textbox(
                        rect,
                        translated_text,
                        fontsize=min_fontsize,
                        fontname=font_alias,
                        align=0
                    )



        doc.save(output_path)
        doc.close()

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
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        lines.append(' '.join(current_line))

        return lines