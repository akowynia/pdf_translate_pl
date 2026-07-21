import sys
import os
from classes.llm_operations import llm_operations
from classes.pdf_to_text import pdf_to_text
from classes.save_pdf import save_pdf
from classes.db_operations import db_operations


class translate_ebook:
    def __init__(self, model_name: str = "llama3") -> None:
        """
        Initializes the ebook translator using Ollama and layout preservation.

        Args:
            model_name (str): Name of the Ollama model to use (default: "llama3").
        """
        self.model_name = model_name

    def start(self, path):
        """
        Starts the translation process for the given ebook while preserving layout.

        Args:
            path (str): The path of the ebook PDF file.
        """
        if not os.path.exists(path):
            print(f"Error: File '{path}' does not exist.")
            return

        db = db_operations()
        llm = llm_operations(model_name=self.model_name)
        pdf = pdf_to_text()

        system_prompt = (
            "Przetłumacz poprawnie gramatycznie na język polski i zachowaj formatowanie. "
            "Nie dodawaj żadnych dodatkowych znaków interpunkcyjnych ani komentarzy. "
            "Dostajesz fragmenty książki, zachowaj pierwotne formatowanie. Tylko tłumacz, nie dodawaj niczego."
        )

        all_translated_pages_blocks = []

        # If the ebook is not already in the database
        if not db.checkData(path):
            pages_blocks = pdf.extract_blocks_from_pdf(path)
            total_pages = len(pages_blocks)

            for page_idx, page_blocks in enumerate(pages_blocks):
                print(f"Translating page {page_idx + 1}/{total_pages} ({len(page_blocks)} text blocks)")
                translated_page_blocks = []
                chunk_size = 20

                for i in range(0, len(page_blocks), chunk_size):
                    batch_blocks = page_blocks[i:i + chunk_size]
                    payload = {}
                    for b_idx, blk in enumerate(batch_blocks):
                        txt = blk['text'].strip()
                        if txt:
                            payload[str(b_idx)] = txt

                    if payload:
                        translations = llm.generate_batch(payload, system_prompt)
                    else:
                        translations = {}

                    for b_idx, blk in enumerate(batch_blocks):
                        orig_text = blk['text'].strip()
                        str_key = str(b_idx)
                        translated_text = translations.get(str_key, orig_text if not orig_text else "")

                        translated_page_blocks.append({
                            'bbox': blk['bbox'],
                            'original_text': orig_text,
                            'translated_text': str(translated_text),
                            'block_no': blk['block_no']
                        })

                db.insertData(path, page_idx, page_blocks, translated_page_blocks)
                all_translated_pages_blocks.append(translated_page_blocks)

        else:
            print("Book already exists in database. Resuming/loading from DB...")
            last_page_data = db.last_page(path)
            last_page_idx = int(last_page_data[0][0]) if last_page_data else -1

            pages_blocks = pdf.extract_blocks_from_pdf(path)
            total_pages = len(pages_blocks)

            for page_idx, page_blocks in enumerate(pages_blocks):
                if page_idx <= last_page_idx:
                    continue

                print(f"Translating page {page_idx + 1}/{total_pages} ({len(page_blocks)} text blocks)")
                translated_page_blocks = []
                chunk_size = 20

                for i in range(0, len(page_blocks), chunk_size):
                    batch_blocks = page_blocks[i:i + chunk_size]
                    payload = {}
                    for b_idx, blk in enumerate(batch_blocks):
                        txt = blk['text'].strip()
                        if txt:
                            payload[str(b_idx)] = txt

                    if payload:
                        translations = llm.generate_batch(payload, system_prompt)
                    else:
                        translations = {}

                    for b_idx, blk in enumerate(batch_blocks):
                        orig_text = blk['text'].strip()
                        str_key = str(b_idx)
                        translated_text = translations.get(str_key, orig_text if not orig_text else "")

                        translated_page_blocks.append({
                            'bbox': blk['bbox'],
                            'original_text': orig_text,
                            'translated_text': str(translated_text),
                            'block_no': blk['block_no']
                        })

                db.insertData(path, page_idx, page_blocks, translated_page_blocks)

            all_translated_pages_blocks = db.selectBlocksData(path)


        if path.lower().endswith(".pdf"):
            output_pdf = path[:-4] + "_translated.pdf"
        else:
            output_pdf = path + "_translated.pdf"

        sv_pdf = save_pdf()
        sv_pdf.create_pdf_layout_preserved(path, output_pdf, all_translated_pages_blocks)
        print(f"Successfully generated layout-preserved translated PDF: {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 translate_ebook.py <path pdf> [model_name]")
        sys.exit(1)
    else:
        folder = sys.argv[1]
        model = sys.argv[2] if len(sys.argv) == 3 else "llama3"
        te = translate_ebook(model_name=model)
        te.start(folder)
