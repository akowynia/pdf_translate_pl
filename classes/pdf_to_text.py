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
            text.append(page_text)
        return text

    def extract_blocks_from_pdf(self, pdf_path):
        """
        Extracts text blocks with coordinates (bbox) from each page of a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            list: A list of pages, where each page contains a list of block dicts.
        """
        doc = fitz.open(pdf_path)
        pages_blocks = []

        for page in doc:
            blocks = page.get_text("blocks")
            page_blocks = []
            for b in blocks:
                # b format: (x0, y0, x1, y1, "text", block_no, block_type)
                # block_type == 0 indicates text
                if len(b) >= 7 and b[6] == 0:
                    text_content = b[4].strip()
                    if text_content:
                        page_blocks.append({
                            'bbox': [b[0], b[1], b[2], b[3]],
                            'text': b[4],
                            'block_no': b[5]
                        })
            pages_blocks.append(page_blocks)

        return pages_blocks