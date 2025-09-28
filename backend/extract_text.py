import fitz  # pymupdf
import os

def extract_text_from_pdf(pdf_path: str, out_dir="data") -> str:
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, f"{os.path.basename(pdf_path)}.txt")

    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            f.write(f"--- Page {page_num} ---\n{text}\n")
    return txt_path, len(doc)
