import fitz  # pymupdf
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root


def extract_text_from_pdf(pdf_path: str, out_dir=None) -> str:
    if out_dir is None:
        out_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(out_dir, exist_ok=True)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = os.path.join(out_dir, f"{pdf_name}.txt")

    doc = fitz.open(pdf_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            f.write(f"--- Page {page_num} ---\n{text}\n")

    return txt_path, len(doc)
